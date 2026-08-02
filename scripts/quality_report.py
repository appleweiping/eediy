from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.check_editorial_quality import editorial_quality_issues, load_guide_pairs
from scripts.check_external_links import (
    EVIDENCE_REVIEW_REASON_CODES,
    MANUAL_REVIEW_REASON_CODES,
    reason_code_matches_result,
)
from scripts.check_course_guides import corpus_style_issues, release_gate_issues
from scripts.check_forbidden_terms import forbidden_issues
from scripts.check_markdown_links import markdown_link_issues
from scripts.check_navigation import navigation_issues
from scripts.check_translations import translation_issues
from scripts.course_data import catalogue_statistics
from scripts.course_guides import load_course_guides
from scripts.generate_course_pages import build_expected_pages, generated_page_issues
from scripts.quality_common import (
    Issue,
    QualityError,
    atomic_write,
    emit_issues,
    exit_code,
    load_json,
    repo_path,
    stable_json,
)
from scripts.track_guides import load_track_guides
from scripts.validate_courses import validate_file
from scripts.validate_mainline_audit import validate_mainline_audit_files
from scripts.validate_routes import validate_route_files


def _resource_statistics(catalogue: Mapping[str, Any]) -> dict[str, Any]:
    """Summarize reviewed resource states without inventing course metadata."""

    resource_statuses: Counter[str] = Counter()
    for course in catalogue.get("courses", []):
        for resource in course.get("resources", []):
            resource_statuses[str(resource.get("status"))] += 1
    return {"resource_statuses": dict(sorted(resource_statuses.items()))}


def _report_ok(
    issues: list[Issue],
    *,
    warnings_as_errors: bool,
) -> bool:
    return exit_code(issues, warnings_as_errors=warnings_as_errors) == 0


def _external_statistics(
    path: Path,
    *,
    require_external: bool = False,
    skip_external: bool = False,
    max_age_days: float = 14,
) -> tuple[dict[str, Any] | None, list[Issue]]:
    if skip_external:
        return None, []
    if not math.isfinite(max_age_days) or max_age_days < 0:
        return None, [
            Issue(
                "error",
                "external.max_age",
                "external-link report max age must be a finite non-negative number",
                path.as_posix(),
            )
        ]
    missing_severity = "error" if require_external else "warning"
    if not path.exists():
        return None, [
            Issue(
                missing_severity,
                "external.report_missing",
                "no fresh external-link report is present; run the external checker",
                path.as_posix(),
            )
        ]
    try:
        payload = load_json(path)
    except (OSError, QualityError) as exc:
        return None, [
            Issue(missing_severity, "external.report_invalid", str(exc), path.as_posix())
        ]
    if not isinstance(payload, Mapping) or not isinstance(payload.get("summary"), Mapping):
        return None, [
            Issue(
                missing_severity,
                "external.report_shape",
                "external-link report has an invalid shape",
                path.as_posix(),
            )
        ]

    issues: list[Issue] = []
    summary = dict(payload["summary"])
    count_keys = ("total", "ok", "review", "failed")
    summary_counts_valid = False
    if any(
        not isinstance(summary.get(key), int)
        or isinstance(summary.get(key), bool)
        or summary[key] < 0
        for key in count_keys
    ):
        issues.append(
            Issue(
                "error",
                "external.summary_counts",
                "external-link summary counts must be non-negative integers",
                path.as_posix(),
            )
        )
    else:
        summary_counts_valid = True
        classified = summary["ok"] + summary["review"] + summary["failed"]
        if summary["total"] != classified:
            issues.append(
                Issue(
                    "error",
                    "external.summary_total",
                    "external-link total does not equal ok + review + failed",
                    path.as_posix(),
                )
            )
        if summary["failed"]:
            issues.append(
                Issue(
                    "error",
                    "external.failed",
                    f"{summary['failed']} externally checked URL(s) failed",
                    path.as_posix(),
                )
            )

    results = payload.get("results")
    if not isinstance(results, list):
        issues.append(
            Issue(
                missing_severity,
                "external.results_missing",
                "external-link report must include its checked results",
                path.as_posix(),
            )
        )
    elif isinstance(summary.get("total"), int) and len(results) != summary["total"]:
        issues.append(
            Issue(
                "error",
                "external.results_total",
                "external-link result count does not match the summary total",
                path.as_posix(),
            )
        )
    if isinstance(results, list) and summary_counts_valid:
        actual_outcomes = {"ok": 0, "review": 0, "failed": 0}
        invalid_outcome = False
        inconsistent_result = False
        for result in results:
            if not isinstance(result, Mapping) or result.get("outcome") not in {
                "ok",
                "review",
                "failed",
            }:
                invalid_outcome = True
                continue
            actual_outcomes[str(result["outcome"])] += 1
            if not reason_code_matches_result(result):
                inconsistent_result = True
        if invalid_outcome:
            issues.append(
                Issue(
                    "error",
                    "external.result_outcome",
                    "every external-link result must have an ok, review, or "
                    "failed outcome",
                    path.as_posix(),
                )
            )
        if any(summary[key] != actual_outcomes[key] for key in actual_outcomes):
            issues.append(
                Issue(
                    "error",
                    "external.summary_results",
                    "ok/review/failed summary counters do not match result outcomes",
                    path.as_posix(),
                )
            )
        if inconsistent_result:
            issues.append(
                Issue(
                    "error",
                    "external.result_inconsistent",
                    "every external-link result must have mutually consistent "
                    "outcome, HTTP status, reason, and structured reason code",
                    path.as_posix(),
                )
            )

    role_count_keys = (
        "target_total",
        "target_ok",
        "target_review",
        "target_failed",
        "evidence_total",
        "evidence_ok",
        "evidence_review",
        "evidence_failed",
        "evidence_only",
    )
    role_counts_present = any(key in summary for key in role_count_keys)
    role_counts_valid = False
    if require_external and not role_counts_present:
        issues.append(
            Issue(
                "error",
                "external.role_counts_required",
                "release reports must use the role-aware target/evidence format",
                path.as_posix(),
            )
        )
    if role_counts_present:
        if not all(key in summary for key in role_count_keys):
            issues.append(
                Issue(
                    "error",
                    "external.role_counts_missing",
                    "external-link role summary must include all target and "
                    "evidence counters",
                    path.as_posix(),
                )
            )
        elif any(
            not isinstance(summary.get(key), int)
            or isinstance(summary.get(key), bool)
            or summary[key] < 0
            for key in role_count_keys
        ):
            issues.append(
                Issue(
                    "error",
                    "external.role_counts",
                    "external-link target and evidence counters must be "
                    "non-negative integers",
                    path.as_posix(),
                )
            )
        else:
            role_counts_valid = True
            if summary["target_total"] != (
                summary["target_ok"]
                + summary["target_review"]
                + summary["target_failed"]
            ):
                issues.append(
                    Issue(
                        "error",
                        "external.target_total",
                        "target_total does not equal target_ok + target_review "
                        "+ target_failed",
                        path.as_posix(),
                    )
                )
            if summary["evidence_total"] != (
                summary["evidence_ok"]
                + summary["evidence_review"]
                + summary["evidence_failed"]
            ):
                issues.append(
                    Issue(
                        "error",
                        "external.evidence_total",
                        "evidence_total does not equal evidence_ok + "
                        "evidence_review + evidence_failed",
                        path.as_posix(),
                    )
                )
            if summary["evidence_only"] > summary["evidence_total"]:
                issues.append(
                    Issue(
                        "error",
                        "external.evidence_only",
                        "evidence_only cannot exceed evidence_total",
                        path.as_posix(),
                    )
                )

    if isinstance(results, list) and role_counts_valid:
        actual_role_counts = {
            "target_total": 0,
            "target_ok": 0,
            "target_review": 0,
            "target_failed": 0,
            "evidence_total": 0,
            "evidence_ok": 0,
            "evidence_review": 0,
            "evidence_failed": 0,
            "evidence_only": 0,
        }
        role_shape_valid = True
        evidence_result_urls: set[str] = set()
        target_evidence_references: list[tuple[str, list[str]]] = []

        def review_date_is_current(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            try:
                parsed = date.fromisoformat(value)
            except ValueError:
                return False
            # Release evidence is produced on UTC runners. A Shanghai review
            # entered before UTC midnight is represented by the preceding UTC
            # calendar date in the ledger, so no future-date exception is needed.
            today_utc = datetime.now(timezone.utc).date()
            age = (today_utc - parsed).days
            return 0 <= age <= max_age_days

        for result in results:
            if not isinstance(result, Mapping):
                role_shape_valid = False
                continue
            roles = result.get("link_roles")
            if (
                not isinstance(roles, list)
                or any(role not in {"target", "evidence"} for role in roles)
                or len(set(roles)) != len(roles)
                or not roles
            ):
                role_shape_valid = False
                continue
            outcome = result.get("outcome")
            if outcome not in {"ok", "review", "failed"}:
                role_shape_valid = False
                continue
            if "target" in roles:
                actual_role_counts["target_total"] += 1
                actual_role_counts[f"target_{outcome}"] += 1
                if outcome == "review":
                    adjudication = result.get("review_adjudication")
                    reason_code = result.get("reason_code")
                    allowed_reason_codes = (
                        adjudication.get("allowed_reason_codes")
                        if isinstance(adjudication, Mapping)
                        else None
                    )
                    evidence = (
                        adjudication.get("evidence")
                        if isinstance(adjudication, Mapping)
                        else None
                    )
                    valid_adjudication = (
                        isinstance(adjudication, Mapping)
                        and adjudication.get("recorded") is True
                        and adjudication.get("decision") == "retain"
                        and adjudication.get("approved") is True
                        and isinstance(adjudication.get("reviewer"), str)
                        and bool(str(adjudication.get("reviewer")).strip())
                        and isinstance(adjudication.get("automation_reason"), str)
                        and bool(str(adjudication.get("automation_reason")).strip())
                        and isinstance(adjudication.get("method"), str)
                        and bool(str(adjudication.get("method")).strip())
                        and review_date_is_current(adjudication.get("reviewed_at"))
                        and isinstance(reason_code, str)
                        and reason_code in MANUAL_REVIEW_REASON_CODES
                        and reason_code_matches_result(result)
                        and isinstance(allowed_reason_codes, list)
                        and bool(allowed_reason_codes)
                        and all(
                            isinstance(code, str)
                            and code in MANUAL_REVIEW_REASON_CODES
                            for code in allowed_reason_codes
                        )
                        and len(set(allowed_reason_codes))
                        == len(allowed_reason_codes)
                        and reason_code in allowed_reason_codes
                        and isinstance(evidence, list)
                        and bool(evidence)
                        and all(
                            isinstance(url, str) and url.startswith("https://")
                            for url in evidence
                        )
                        and len(set(evidence)) == len(evidence)
                    )
                    if not valid_adjudication:
                        issues.append(
                            Issue(
                                "error",
                                "external.review_adjudication_invalid",
                                "each reviewed target needs a current, complete retain "
                                "adjudication whose allowed reason code matches the "
                                "structured checker result",
                                str(result.get("url", path.as_posix())),
                            )
                        )
                    elif isinstance(evidence, list):
                        target_evidence_references.append(
                            (str(result.get("url", "")), list(evidence))
                        )
            if "evidence" in roles:
                actual_role_counts["evidence_total"] += 1
                actual_role_counts[f"evidence_{outcome}"] += 1
                evidence_result_urls.add(str(result.get("url", "")))
                if "target" not in roles:
                    actual_role_counts["evidence_only"] += 1
                if outcome == "review":
                    attestation = result.get("evidence_attestation")
                    reason_code = result.get("reason_code")
                    if not (
                        isinstance(attestation, Mapping)
                        and attestation.get("recorded") is True
                        and attestation.get("manually_verified") is True
                        and isinstance(attestation.get("reviewer"), str)
                        and bool(str(attestation.get("reviewer")).strip())
                        and review_date_is_current(attestation.get("reviewed_at"))
                        and isinstance(reason_code, str)
                        and reason_code in EVIDENCE_REVIEW_REASON_CODES
                        and reason_code_matches_result(result)
                    ):
                        issues.append(
                            Issue(
                                "error",
                                "external.evidence_review_unapproved",
                                "every evidence review, including a target/evidence "
                                "overlap, needs a current manual attestation and a "
                                "structured robots_denied or http_403 result",
                                str(result.get("url", path.as_posix())),
                            )
                        )
        if not role_shape_valid:
            issues.append(
                Issue(
                    "error",
                    "external.result_roles",
                    "each role-aware result must declare a non-empty, unique "
                    "link_roles list and a supported outcome",
                    path.as_posix(),
                )
            )
        if actual_role_counts != {
            key: summary[key] for key in role_count_keys
        }:
            issues.append(
                Issue(
                    "error",
                    "external.role_count_results",
                    "target/evidence summary counters do not match result roles",
                    path.as_posix(),
                )
            )
        missing_evidence_references = [
            (target, evidence_url)
            for target, evidence_urls in target_evidence_references
            for evidence_url in evidence_urls
            if evidence_url not in evidence_result_urls
        ]
        if missing_evidence_references:
            target, evidence_url = missing_evidence_references[0]
            issues.append(
                Issue(
                    "error",
                    "external.review_evidence_missing",
                    "review adjudication evidence is not present as an independently "
                    f"checked evidence result: {evidence_url}",
                    target or path.as_posix(),
                )
            )

    review_count = summary.get(
        "target_review" if role_counts_present else "review"
    )
    review_fields = ("review_approved", "review_unapproved")
    review_fields_present = any(key in summary for key in review_fields)
    review_fields_required = (
        require_external
        and isinstance(review_count, int)
        and not isinstance(review_count, bool)
        and review_count > 0
    )
    review_counts_valid = False
    if review_fields_present or review_fields_required:
        if not all(key in summary for key in review_fields):
            issues.append(
                Issue(
                    "error",
                    "external.review_adjudication_missing",
                    "external-link summary must include both review_approved "
                    "and review_unapproved",
                    path.as_posix(),
                )
            )
        elif any(
            not isinstance(summary.get(key), int)
            or isinstance(summary.get(key), bool)
            or summary[key] < 0
            for key in review_fields
        ):
            issues.append(
                Issue(
                    "error",
                    "external.review_adjudication_counts",
                    "review_approved and review_unapproved must be "
                    "non-negative integers",
                    path.as_posix(),
                )
            )
        else:
            review_counts_valid = True
            if isinstance(review_count, int) and (
                summary["review_approved"] + summary["review_unapproved"]
                != review_count
            ):
                issues.append(
                    Issue(
                        "error",
                        "external.review_adjudication_total",
                        "review_approved + review_unapproved must equal review",
                        path.as_posix(),
                    )
                )
            if require_external and summary["review_unapproved"] > 0:
                issues.append(
                    Issue(
                        "error",
                        "external.review_unapproved",
                        f"{summary['review_unapproved']} manual-review URL(s) "
                        "lack a retain decision",
                        path.as_posix(),
                    )
                )

    if isinstance(results, list) and review_counts_valid:
        result_review_approved = 0
        result_review_unapproved = 0
        for result in results:
            if not isinstance(result, Mapping) or result.get("outcome") != "review":
                continue
            roles = result.get("link_roles")
            if isinstance(roles, list) and "target" not in roles:
                continue
            adjudication = result.get("review_adjudication")
            decision = (
                adjudication.get("decision")
                if isinstance(adjudication, Mapping)
                else None
            )
            if decision == "retain":
                result_review_approved += 1
            else:
                result_review_unapproved += 1
        if (
            result_review_approved != summary["review_approved"]
            or result_review_unapproved != summary["review_unapproved"]
        ):
            issues.append(
                Issue(
                    "error",
                    "external.review_adjudication_results",
                    "review approval counts do not match result adjudications",
                    path.as_posix(),
                )
            )

    now = datetime.now(timezone.utc)
    generated_at = payload.get("generated_at")
    generated: datetime | None = None
    if isinstance(generated_at, str):
        try:
            generated = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
            if generated.tzinfo is None:
                raise ValueError("timestamp has no timezone")
            generated = generated.astimezone(timezone.utc)
        except ValueError:
            generated = None
    if generated is None:
        issues.append(
            Issue(
                missing_severity,
                "external.generated_at",
                "external-link report needs a valid timezone-aware generated_at timestamp",
                path.as_posix(),
            )
        )
    else:
        age = now - generated
        summary["generated_at"] = generated.isoformat()
        summary["report_age_hours"] = round(age.total_seconds() / 3600, 2)
        if age < -timedelta(minutes=15):
            issues.append(
                Issue(
                    missing_severity,
                    "external.report_future",
                    "external-link report timestamp is unexpectedly in the future",
                    path.as_posix(),
                )
            )
        if require_external and age > timedelta(days=max_age_days):
            issues.append(
                Issue(
                    "error",
                    "external.report_stale",
                    f"external-link report is older than {max_age_days:g} days",
                    path.as_posix(),
                )
            )

    if require_external and isinstance(results, list):
        freshness_failures: dict[str, list[str]] = {
            "external.result_cache_flag": [],
            "external.result_cached": [],
            "external.result_checked_at": [],
            "external.result_checked_at_future": [],
            "external.result_checked_at_stale": [],
            "external.result_after_report": [],
        }

        def record_failure(code: str, result: Mapping[str, Any]) -> None:
            value = result.get("url")
            freshness_failures[code].append(
                str(value) if isinstance(value, str) and value else "<unknown URL>"
            )

        for result in results:
            if not isinstance(result, Mapping):
                continue

            from_cache = result.get("from_cache")
            if from_cache is True:
                record_failure("external.result_cached", result)
            elif from_cache is not False:
                record_failure("external.result_cache_flag", result)

            checked_at = result.get("checked_at")
            checked: datetime | None = None
            if isinstance(checked_at, str):
                try:
                    checked = datetime.fromisoformat(
                        checked_at.replace("Z", "+00:00")
                    )
                    if checked.tzinfo is None:
                        raise ValueError("timestamp has no timezone")
                    checked = checked.astimezone(timezone.utc)
                except ValueError:
                    checked = None
            if checked is None:
                record_failure("external.result_checked_at", result)
                continue

            if checked > now:
                record_failure("external.result_checked_at_future", result)
            if now - checked > timedelta(days=max_age_days):
                record_failure("external.result_checked_at_stale", result)
            if generated is not None and checked > generated:
                record_failure("external.result_after_report", result)

        failure_messages = {
            "external.result_cache_flag": (
                "external-link result(s) need an explicit boolean from_cache flag"
            ),
            "external.result_cached": (
                "release evidence cannot contain cached external-link result(s)"
            ),
            "external.result_checked_at": (
                "external-link result(s) need a valid timezone-aware checked_at "
                "timestamp"
            ),
            "external.result_checked_at_future": (
                "external-link result checked_at timestamp(s) are in the future"
            ),
            "external.result_checked_at_stale": (
                f"external-link result(s) are older than {max_age_days:g} days"
            ),
            "external.result_after_report": (
                "external-link result checked_at timestamp(s) are later than the "
                "report generated_at timestamp"
            ),
        }
        for code, urls in freshness_failures.items():
            if not urls:
                continue
            examples = ", ".join(urls[:3])
            if len(urls) > 3:
                examples += f", and {len(urls) - 3} more"
            issues.append(
                Issue(
                    "error",
                    code,
                    f"{failure_messages[code]} ({len(urls)} affected: {examples})",
                    path.as_posix(),
                )
            )

    return summary, issues


def _markdown_report(payload: Mapping[str, Any]) -> str:
    status = "PASS" if payload["ok"] else "FAIL"
    catalogue = payload["catalogue"]
    resources = payload["resources"]
    editorial = payload["editorial"]
    guide_release = payload["course_guides"]
    mainline_audit = payload["mainline_audit"]
    routes = payload["routes"]
    docs = payload["docs"]
    external = payload.get("external")
    lines = [
        "# EEDIY Quality Report",
        "",
        f"**Verdict:** {status}",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "## Catalogue health",
        "",
        "| Check | Result |",
        "|---|---:|",
        f"| Courses | {catalogue['courses']} |",
        f"| Tracks with courses | {catalogue['tracks_used']} |",
        f"| Resource metadata complete | {catalogue['resource_metadata_percent']:.2f}% |",
        f"| Audited mainline tracks | {mainline_audit['tracks']} |",
        f"| Audited mainline courses | {mainline_audit['mainlines']} |",
        f"| Tracks with one preferred mainline | {mainline_audit['preferred']} |",
        f"| Authored bilingual course records | {guide_release['authored_guides']} |",
        f"| Deep course guides | {guide_release['deep_guides']} |",
        f"| Catalogue-only course records | {guide_release['catalogue_guides']} |",
        f"| Tracks with a deep guide | {guide_release['tracks_deep_covered']} / {guide_release['tracks_populated']} |",
        f"| Audited mainlines with a deep guide | {guide_release['mainlines_deep_covered']} / {guide_release['mainlines_audited']} |",
        f"| Editorial guide pairs checked | {editorial['guides_checked']} / {editorial['guides_total']} |",
        f"| Editorial errors / warnings | {editorial['errors']} / {editorial['warnings']} |",
        f"| Bilingual page pairs | {docs['translation']['pair_coverage_percent']:.2f}% |",
        f"| Navigation reachability | {docs['navigation']['reachability_percent']:.2f}% |",
        f"| Route course coverage | {routes['catalogue_coverage_percent']:.2f}% |",
        "",
        "## Catalogue distribution",
        "",
        f"- Tier: `{json.dumps(catalogue['courses_by_tier'], ensure_ascii=False, sort_keys=True)}`",
        f"- Role: `{json.dumps(catalogue['courses_by_role'], ensure_ascii=False, sort_keys=True)}`",
        f"- Resource status: `{json.dumps(resources['resource_statuses'], ensure_ascii=False, sort_keys=True)}`",
        f"- Mainline audit: `{mainline_audit['pass']} pass, {mainline_audit['review']} review`",
        "",
        "## Documentation",
        "",
        f"- Expected generated pages: {docs['generated_expected']}",
        f"- Markdown files checked: {docs['links']['markdown_files']}",
        f"- Internal links checked: {docs['links']['links_internal']}",
        f"- External URLs discovered in Markdown: {docs['links']['unique_external_urls']}",
        "",
        "## External links",
        "",
    ]
    if external:
        lines.extend(
            [
                f"- Healthy: {external.get('ok', 0)}",
                f"- Manual review (not counted healthy): {external.get('review', 0)}",
                f"- Manual review approved: {external.get('review_approved', 0)}",
                f"- Manual review unapproved: {external.get('review_unapproved', 0)}",
                f"- Failed: {external.get('failed', 0)}",
                f"- Content targets: {external.get('target_total', external.get('total', 0))} "
                f"({external.get('target_review', external.get('review', 0))} review, "
                f"{external.get('target_failed', external.get('failed', 0))} failed)",
                f"- Manual-review evidence URLs: {external.get('evidence_total', 0)} "
                f"({external.get('evidence_review', 0)} review, "
                f"{external.get('evidence_failed', 0)} failed; "
                f"{external.get('evidence_only', 0)} evidence-only)",
                f"- Healthy percentage: {external.get('healthy_percent', 0):.2f}%",
                f"- Checked: {external.get('generated_at', 'unknown')}",
                f"- Report age: {external.get('report_age_hours', 'unknown')} hours",
            ]
        )
    else:
        lines.append("- No fresh report. Run `python scripts/check_external_links.py`.")
    lines.extend(["", "## Findings", ""])
    if payload["issues"]:
        for issue in payload["issues"]:
            location = f" ({issue['path']})" if issue.get("path") else ""
            lines.append(
                f"- **{issue['severity'].upper()} · {issue['code']}**{location}: "
                f"{issue['message']}"
            )
    else:
        lines.append("- No findings.")
    return "\n".join(lines) + "\n"


def build_report(
    *,
    catalogue_path: Path,
    course_schema_path: Path,
    routes_path: Path,
    route_schema_path: Path,
    mainline_audit_path: Path,
    candidates_path: Path,
    tracks_path: Path,
    resources_path: Path,
    course_guides_path: Path,
    course_guide_schema_path: Path,
    track_guides_root: Path,
    docs_root: Path,
    config_path: Path,
    external_report_path: Path,
    require_external: bool = False,
    skip_external: bool = False,
    external_max_age_days: float = 14,
    warnings_as_errors: bool = False,
) -> tuple[dict[str, Any], list[Issue]]:
    catalogue, issues = validate_file(catalogue_path, course_schema_path)
    routes_data, route_issues, route_statistics = validate_route_files(
        routes_path, catalogue_path, route_schema_path
    )
    issues.extend(route_issues)
    mainline_audit_data, mainline_issues, mainline_statistics = (
        validate_mainline_audit_files(
            mainline_audit_path,
            candidates_path,
            tracks_path,
            resources_path,
        )
    )
    issues.extend(mainline_issues)
    if catalogue is None:
        catalogue = {"tracks": [], "courses": []}
    if routes_data is None:
        routes_data = {"routes": []}
    course_guides, course_guide_issues = load_course_guides(
        course_guides_path,
        catalogue,
        course_guide_schema_path,
    )
    issues.extend(course_guide_issues)
    track_guides, track_guide_issues = load_track_guides(
        catalogue,
        track_guides_root,
    )
    issues.extend(track_guide_issues)
    guide_release_issues, guide_release_statistics = release_gate_issues(
        catalogue,
        course_guides,
        mainline_audit=mainline_audit_data,
        source=course_guides_path.as_posix(),
        audit_source=mainline_audit_path.as_posix(),
    )
    issues.extend(guide_release_issues)
    guide_style_issues, guide_style_statistics = corpus_style_issues(
        catalogue,
        course_guides,
        source=course_guides_path.as_posix(),
    )
    issues.extend(guide_style_issues)
    guide_release_statistics = {
        **guide_release_statistics,
        **guide_style_statistics,
    }
    guide_pairs, guide_pair_issues = load_guide_pairs(
        course_guides_path,
        catalogue_path,
    )
    issues.extend(guide_pair_issues)
    editorial_findings, editorial_statistics = editorial_quality_issues(
        guide_pairs,
    )
    issues.extend(editorial_findings)
    translation_findings, translation_statistics = translation_issues(docs_root)
    navigation_findings, navigation_statistics = navigation_issues(config_path)
    link_findings, link_statistics = markdown_link_issues(docs_root)
    forbidden_findings = forbidden_issues(repo_path("."))
    issues.extend(translation_findings)
    issues.extend(navigation_findings)
    issues.extend(link_findings)
    issues.extend(forbidden_findings)
    expected = build_expected_pages(
        catalogue,
        routes_data,
        docs_root,
        mainline_audit=mainline_audit_data,
        course_guides=course_guides,
        track_guides=track_guides,
    )
    generated_findings = generated_page_issues(expected, docs_root)
    issues.extend(generated_findings)
    external_statistics, external_findings = _external_statistics(
        external_report_path,
        require_external=require_external,
        skip_external=skip_external,
        max_age_days=external_max_age_days,
    )
    issues.extend(external_findings)
    catalogue_statistics_value = catalogue_statistics(catalogue)
    resources = _resource_statistics(catalogue)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ok": _report_ok(
            issues,
            warnings_as_errors=warnings_as_errors,
        ),
        "warnings_as_errors": warnings_as_errors,
        "catalogue": catalogue_statistics_value,
        "resources": resources,
        "editorial": editorial_statistics,
        "course_guides": guide_release_statistics,
        "mainline_audit": mainline_statistics,
        "routes": route_statistics,
        "docs": {
            "translation": translation_statistics,
            "navigation": navigation_statistics,
            "links": link_statistics,
            "generated_expected": len(expected),
        },
        "external": external_statistics,
        "issues": [
            issue.to_dict()
            for issue in sorted(
                set(issues),
                key=lambda item: (
                    item.severity,
                    item.code,
                    item.path,
                    item.line if item.line is not None else -1,
                    item.message,
                ),
            )
        ],
    }
    return payload, list(
        sorted(
            set(issues),
            key=lambda item: (
                item.severity,
                item.code,
                item.path,
                item.line if item.line is not None else -1,
                item.message,
            ),
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the consolidated quality report.")
    parser.add_argument("--catalogue", default="data/courses.json")
    parser.add_argument("--course-schema", default="data/course.schema.json")
    parser.add_argument("--routes", default="data/routes.json")
    parser.add_argument("--route-schema", default="data/route.schema.json")
    parser.add_argument("--mainline-audit", default="data/mainline_audit.json")
    parser.add_argument("--candidates", default="data/course_candidates.json")
    parser.add_argument("--tracks", default="data/tracks.json")
    parser.add_argument("--resources", default="data/course_resources.json")
    parser.add_argument("--course-guides", default="data/course_guides.json")
    parser.add_argument(
        "--course-guide-schema",
        default="data/course-guide.schema.json",
    )
    parser.add_argument("--track-guides-root", default="content/track-guides")
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--config", default="mkdocs.yml")
    parser.add_argument("--external-report", default="build/external-links.json")
    external_mode = parser.add_mutually_exclusive_group()
    external_mode.add_argument(
        "--require-external",
        action="store_true",
        help="Fail when the external-link report is missing, invalid, or stale.",
    )
    external_mode.add_argument(
        "--skip-external",
        action="store_true",
        help="Explicitly omit external-link evidence from this report.",
    )
    parser.add_argument(
        "--external-max-age-days",
        type=float,
        default=14,
        help="Maximum report age accepted with --require-external (default: 14).",
    )
    parser.add_argument("--json-output", default="build/quality-report.json")
    parser.add_argument("--markdown-output", default="build/quality-report.md")
    parser.add_argument("--warnings-as-errors", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    payload, issues = build_report(
        catalogue_path=repo_path(args.catalogue),
        course_schema_path=repo_path(args.course_schema),
        routes_path=repo_path(args.routes),
        route_schema_path=repo_path(args.route_schema),
        mainline_audit_path=repo_path(args.mainline_audit),
        candidates_path=repo_path(args.candidates),
        tracks_path=repo_path(args.tracks),
        resources_path=repo_path(args.resources),
        course_guides_path=repo_path(args.course_guides),
        course_guide_schema_path=repo_path(args.course_guide_schema),
        track_guides_root=repo_path(args.track_guides_root),
        docs_root=repo_path(args.docs_root),
        config_path=repo_path(args.config),
        external_report_path=repo_path(args.external_report),
        require_external=args.require_external,
        skip_external=args.skip_external,
        external_max_age_days=args.external_max_age_days,
        warnings_as_errors=args.warnings_as_errors,
    )
    atomic_write(repo_path(args.json_output), stable_json(payload))
    atomic_write(repo_path(args.markdown_output), _markdown_report(payload))
    emit_issues(issues)
    print(
        f"Quality report: {'PASS' if payload['ok'] else 'FAIL'}; "
        f"{len(issues)} finding(s)"
    )
    return exit_code(issues, warnings_as_errors=args.warnings_as_errors)


if __name__ == "__main__":
    raise SystemExit(main())
