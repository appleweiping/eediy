from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.check_forbidden_terms import forbidden_issues
from scripts.check_markdown_links import markdown_link_issues
from scripts.check_navigation import navigation_issues
from scripts.check_translations import translation_issues
from scripts.course_data import catalogue_statistics
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
from scripts.validate_courses import validate_file
from scripts.validate_mainline_audit import validate_mainline_audit_files
from scripts.validate_routes import validate_route_files


def _execution_statistics(catalogue: Mapping[str, Any]) -> dict[str, Any]:
    courses = catalogue.get("courses", [])
    workload_explicit = 0
    tooling_complete = 0
    safety_complete = 0
    evidence_complete = 0
    safety_levels: Counter[str] = Counter()
    resource_statuses: Counter[str] = Counter()
    for course in courses:
        study = course.get("study_plan", {})
        note = study.get("note", {})
        if (
            "estimated_weeks" in study
            and "hours_per_week" in study
            and all(note.get(language) for language in ("zh", "en"))
        ):
            workload_explicit += 1
        tooling = course.get("tooling", {})
        if all(
            tooling.get(key, {}).get(language)
            for key in ("software", "hardware")
            for language in ("zh", "en")
        ) and all(tooling.get("cost_note", {}).get(language) for language in ("zh", "en")):
            tooling_complete += 1
        safety = course.get("safety", {})
        if safety.get("level") and all(
            safety.get("note", {}).get(language) for language in ("zh", "en")
        ):
            safety_complete += 1
            safety_levels[str(safety["level"])] += 1
        evidence = course.get("completion_evidence", {})
        if all(evidence.get(language) for language in ("zh", "en")):
            evidence_complete += 1
        for resource in course.get("resources", []):
            resource_statuses[str(resource.get("status"))] += 1
    total = len(courses)

    def percentage(value: int) -> float:
        return round(value * 100 / total, 2) if total else 0.0

    return {
        "workload_explicit": workload_explicit,
        "workload_explicit_percent": percentage(workload_explicit),
        "tooling_complete": tooling_complete,
        "tooling_complete_percent": percentage(tooling_complete),
        "safety_complete": safety_complete,
        "safety_complete_percent": percentage(safety_complete),
        "completion_evidence_complete": evidence_complete,
        "completion_evidence_complete_percent": percentage(evidence_complete),
        "safety_levels": dict(sorted(safety_levels.items())),
        "resource_statuses": dict(sorted(resource_statuses.items())),
    }


def _external_statistics(
    path: Path,
    *,
    require_external: bool = False,
    skip_external: bool = False,
    max_age_days: float = 14,
) -> tuple[dict[str, Any] | None, list[Issue]]:
    if skip_external:
        return None, []
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
        age = datetime.now(timezone.utc) - generated
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

    return summary, issues


def _markdown_report(payload: Mapping[str, Any]) -> str:
    status = "PASS" if payload["ok"] else "FAIL"
    catalogue = payload["catalogue"]
    execution = payload["execution"]
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
        "## Coverage gates",
        "",
        "| Gate | Result | Required |",
        "|---|---:|---:|",
        f"| Courses | {catalogue['courses']} | ≥ 125 |",
        f"| Tracks with courses | {catalogue['tracks_used']} | ≥ 24 |",
        f"| Resource metadata | {catalogue['resource_metadata_percent']:.2f}% | 100% |",
        f"| Unique high-value resources | {catalogue['unique_high_value_resources']} | ≥ 550 |",
        f"| Courses with projects | {catalogue['courses_with_projects']} | ≥ 100 |",
        f"| Audited mainline tracks | {mainline_audit['tracks']} | = 35 |",
        f"| Audited mainline courses | {mainline_audit['mainlines']} | exact candidate set |",
        f"| Tracks with one preferred mainline | {mainline_audit['preferred']} | = 35 |",
        f"| Bilingual page pairs | {docs['translation']['pair_coverage_percent']:.2f}% | 100% |",
        f"| Substantive bilingual guides | {docs['translation']['substantive_guide_pairs']} | ≥ 16 |",
        f"| Navigation reachability | {docs['navigation']['reachability_percent']:.2f}% | 100% |",
        f"| Route course coverage | {routes['catalogue_coverage_percent']:.2f}% | report |",
        "",
        "## Course executability",
        "",
        "| Field | Complete | Coverage |",
        "|---|---:|---:|",
        f"| Workload with provenance and calibration | {execution['workload_explicit']} | {execution['workload_explicit_percent']:.2f}% |",
        f"| Software, hardware, and cost | {execution['tooling_complete']} | {execution['tooling_complete_percent']:.2f}% |",
        f"| Safety level and note | {execution['safety_complete']} | {execution['safety_complete_percent']:.2f}% |",
        f"| Completion evidence | {execution['completion_evidence_complete']} | {execution['completion_evidence_complete_percent']:.2f}% |",
        "",
        "## Catalogue distribution",
        "",
        f"- Tier: `{json.dumps(catalogue['courses_by_tier'], ensure_ascii=False, sort_keys=True)}`",
        f"- Role: `{json.dumps(catalogue['courses_by_role'], ensure_ascii=False, sort_keys=True)}`",
        f"- Safety: `{json.dumps(execution['safety_levels'], ensure_ascii=False, sort_keys=True)}`",
        f"- Resource status: `{json.dumps(execution['resource_statuses'], ensure_ascii=False, sort_keys=True)}`",
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
                f"- Failed: {external.get('failed', 0)}",
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
    docs_root: Path,
    config_path: Path,
    external_report_path: Path,
    require_external: bool = False,
    skip_external: bool = False,
    external_max_age_days: float = 14,
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
    execution = _execution_statistics(catalogue)
    for metric in (
        "workload_explicit_percent",
        "tooling_complete_percent",
        "safety_complete_percent",
        "completion_evidence_complete_percent",
    ):
        if execution[metric] != 100.0:
            issues.append(
                Issue("error", f"execution.{metric}", "course execution metadata must be 100%")
            )
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ok": exit_code(issues) == 0,
        "catalogue": catalogue_statistics_value,
        "execution": execution,
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
        docs_root=repo_path(args.docs_root),
        config_path=repo_path(args.config),
        external_report_path=repo_path(args.external_report),
        require_external=args.require_external,
        skip_external=args.skip_external,
        external_max_age_days=args.external_max_age_days,
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
