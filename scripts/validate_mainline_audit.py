from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit, urlunsplit

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.quality_common import (
    Issue,
    QualityError,
    emit_issues,
    exit_code,
    load_json,
    repo_path,
    write_json_report,
)


REQUIRED_FIELDS = {
    "track",
    "course_id",
    "status",
    "preferred",
    "official_url",
    "checks",
    "limitation_zh",
    "limitation_en",
    "rationale_zh",
    "rationale_en",
    "verified_at",
}
CHECK_FIELDS = {
    "identity",
    "resources",
    "mainline_fit",
    "limitations",
}
RESULTS = {"pass", "review"}


def normalize_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            parsed.query,
            "",
        )
    )


def parse_iso_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def mainline_audit_issues(
    audit_data: Any,
    candidates: Any,
    taxonomy: Any,
    resources: Any,
    *,
    source: str = "data/mainline_audit.json",
    today: date | None = None,
) -> list[Issue]:
    issues: list[Issue] = []
    utc_today = today or datetime.now(timezone.utc).date()
    latest_valid_date = utc_today + timedelta(days=1)
    if not isinstance(audit_data, Mapping) or not isinstance(
        audit_data.get("audits"), list
    ):
        return [
            Issue(
                "error",
                "mainline_audit.shape",
                "audit data must contain audits[]",
                source,
            )
        ]
    if not isinstance(candidates, list):
        return [
            Issue(
                "error",
                "mainline_audit.candidates_shape",
                "course candidates must be an array",
                "data/course_candidates.json",
            )
        ]
    if not isinstance(taxonomy, Mapping) or not isinstance(
        taxonomy.get("tracks"), list
    ):
        return [
            Issue(
                "error",
                "mainline_audit.taxonomy_shape",
                "track taxonomy must contain tracks[]",
                "data/tracks.json",
            )
        ]
    if not isinstance(resources, Mapping) or not isinstance(
        resources.get("resources"), list
    ):
        return [
            Issue(
                "error",
                "mainline_audit.resources_shape",
                "resource evidence must contain resources[]",
                "data/course_resources.json",
            )
        ]

    track_ids = {
        track.get("id")
        for track in taxonomy["tracks"]
        if isinstance(track, Mapping) and isinstance(track.get("id"), str)
    }
    if len(track_ids) != 35:
        issues.append(
            Issue(
                "error",
                "mainline_audit.track_count",
                f"expected exactly 35 taxonomy tracks, found {len(track_ids)}",
                "data/tracks.json",
            )
        )

    candidate_by_id: dict[int, Mapping[str, Any]] = {}
    expected_mainlines: dict[int, Mapping[str, Any]] = {}
    mainlines_by_track: defaultdict[str, set[int]] = defaultdict(set)
    for index, candidate in enumerate(candidates):
        path = f"data/course_candidates.json:{index}"
        if not isinstance(candidate, Mapping):
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.candidate_type",
                    "candidate must be an object",
                    path,
                )
            )
            continue
        course_id = candidate.get("id")
        if not isinstance(course_id, int):
            continue
        if course_id in candidate_by_id:
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.candidate_duplicate",
                    f"duplicate candidate id {course_id}",
                    path,
                )
            )
        candidate_by_id[course_id] = candidate
        if candidate.get("role") == "mainline":
            expected_mainlines[course_id] = candidate
            track = candidate.get("track")
            if isinstance(track, str):
                mainlines_by_track[track].add(course_id)

    empty_tracks = sorted(track_ids - set(mainlines_by_track))
    for track in empty_tracks:
        issues.append(
            Issue(
                "error",
                "mainline_audit.track_without_mainline",
                f"{track} has no role=mainline candidate",
                "data/course_candidates.json",
            )
        )

    resource_course_ids = {
        item.get("course_id")
        for item in resources["resources"]
        if isinstance(item, Mapping) and isinstance(item.get("course_id"), int)
    }

    seen: Counter[int] = Counter()
    audited_by_track: defaultdict[str, set[int]] = defaultdict(set)
    preferred_by_track: defaultdict[str, list[int]] = defaultdict(list)
    status_counts: Counter[str] = Counter()
    for index, record in enumerate(audit_data["audits"]):
        path = f"{source}:audits/{index}"
        if not isinstance(record, Mapping):
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.record_type",
                    "audit record must be an object",
                    path,
                )
            )
            continue
        missing = sorted(REQUIRED_FIELDS - set(record))
        if missing:
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.fields",
                    "missing required fields: " + ", ".join(missing),
                    path,
                )
            )
        course_id = record.get("course_id")
        track = record.get("track")
        if not isinstance(course_id, int):
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.course_id",
                    "course_id must be an integer",
                    path,
                )
            )
            continue
        seen[course_id] += 1
        candidate = candidate_by_id.get(course_id)
        if candidate is None:
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.unknown_course",
                    f"course_id {course_id} is not a candidate",
                    path,
                )
            )
            continue
        if candidate.get("role") != "mainline":
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.not_mainline",
                    f"course_id {course_id} has role={candidate.get('role')!r}",
                    path,
                )
            )
        if track != candidate.get("track"):
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.track_mismatch",
                    f"record track {track!r} does not match candidate track "
                    f"{candidate.get('track')!r}",
                    path,
                )
            )
        if isinstance(track, str):
            audited_by_track[track].add(course_id)

        status = record.get("status")
        checks = record.get("checks")
        if status not in RESULTS:
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.status",
                    f"status must be one of {sorted(RESULTS)}",
                    path,
                )
            )
        else:
            status_counts[status] += 1
        if not isinstance(checks, Mapping) or set(checks) != CHECK_FIELDS:
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.checks",
                    f"checks must contain exactly {sorted(CHECK_FIELDS)}",
                    path,
                )
            )
        else:
            bad_results = {
                key: value for key, value in checks.items() if value not in RESULTS
            }
            if bad_results:
                issues.append(
                    Issue(
                        "error",
                        "mainline_audit.check_result",
                        f"invalid check results: {bad_results}",
                        path,
                    )
                )
            expected_status = (
                "review" if "review" in checks.values() else "pass"
            )
            if status in RESULTS and status != expected_status:
                issues.append(
                    Issue(
                        "error",
                        "mainline_audit.status_inconsistent",
                        f"status={status!r}, but checks imply {expected_status!r}",
                        path,
                    )
                )

        preferred = record.get("preferred")
        if not isinstance(preferred, bool):
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.preferred_type",
                    "preferred must be boolean",
                    path,
                )
            )
        elif preferred and isinstance(track, str):
            preferred_by_track[track].append(course_id)

        official_url = record.get("official_url")
        candidate_urls = [
            candidate.get("url"),
            *(
                candidate.get("alternate_urls", [])
                if isinstance(candidate.get("alternate_urls"), list)
                else []
            ),
        ]
        allowed_urls = {
            normalize_url(url)
            for url in candidate_urls
            if isinstance(url, str) and url.strip()
        }
        if (
            not isinstance(official_url, str)
            or urlsplit(official_url).scheme.lower() != "https"
            or normalize_url(official_url) not in allowed_urls
        ):
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.official_url",
                    "official_url must be an HTTPS primary or alternate candidate URL",
                    path,
                )
            )

        for key in ("limitation_zh", "limitation_en", "rationale_zh", "rationale_en"):
            if not isinstance(record.get(key), str) or not record[key].strip():
                issues.append(
                    Issue(
                        "error",
                        "mainline_audit.localized_text",
                        f"{key} must be non-empty",
                        path,
                    )
                )
        verified_at = parse_iso_date(record.get("verified_at"))
        candidate_verified = parse_iso_date(candidate.get("verified_at"))
        if verified_at is None:
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.verified_at",
                    "verified_at must be an ISO date",
                    path,
                )
            )
        else:
            if verified_at > latest_valid_date:
                issues.append(
                    Issue(
                        "error",
                        "mainline_audit.future_date",
                        (
                            f"verified_at {verified_at.isoformat()} is more than one "
                            "civil day ahead of UTC"
                        ),
                        path,
                    )
                )
            if candidate_verified and verified_at < candidate_verified:
                issues.append(
                    Issue(
                        "error",
                        "mainline_audit.stale_date",
                        "audit predates the candidate verification",
                        path,
                    )
                )
        if course_id not in resource_course_ids:
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.resource_evidence_missing",
                    f"course_id {course_id} has no resource-manifest evidence",
                    path,
                )
            )
        if not isinstance(candidate.get("risk"), str) or not candidate["risk"].strip():
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.risk_missing",
                    f"course_id {course_id} has no learner-facing risk disclosure",
                    "data/course_candidates.json",
                )
            )

    expected_ids = set(expected_mainlines)
    audited_ids = set(seen)
    for course_id in sorted(expected_ids - audited_ids):
        issues.append(
            Issue(
                "error",
                "mainline_audit.missing",
                f"mainline course_id {course_id} has no audit record",
                source,
            )
        )
    for course_id in sorted(audited_ids - expected_ids):
        issues.append(
            Issue(
                "error",
                "mainline_audit.unexpected",
                f"course_id {course_id} is audited but is not a mainline candidate",
                source,
            )
        )
    for course_id, count in sorted(seen.items()):
        if count != 1:
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.duplicate",
                    f"course_id {course_id} has {count} audit records",
                    source,
                )
            )

    for track in sorted(track_ids):
        expected = mainlines_by_track.get(track, set())
        actual = audited_by_track.get(track, set())
        if actual != expected:
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.track_coverage",
                    f"{track}: expected mainlines {sorted(expected)}, audited "
                    f"{sorted(actual)}",
                    source,
                )
            )
        preferred = preferred_by_track.get(track, [])
        if len(preferred) != 1:
            issues.append(
                Issue(
                    "error",
                    "mainline_audit.preferred_count",
                    f"{track} must have exactly one preferred mainline; found "
                    f"{preferred}",
                    source,
                )
            )

    summary = audit_data.get("summary")
    expected_summary = {
        "track_count": len(track_ids),
        "mainline_count": len(expected_mainlines),
        "preferred_count": sum(len(ids) for ids in preferred_by_track.values()),
        "pass_count": status_counts["pass"],
        "review_count": status_counts["review"],
    }
    if not isinstance(summary, Mapping):
        issues.append(
            Issue(
                "error",
                "mainline_audit.summary",
                "summary must be an object",
                source,
            )
        )
    else:
        for key, value in expected_summary.items():
            if summary.get(key) != value:
                issues.append(
                    Issue(
                        "error",
                        "mainline_audit.summary_mismatch",
                        f"summary.{key}={summary.get(key)!r}; expected {value}",
                        source,
                    )
                )
    return list(dict.fromkeys(issues))


def validate_mainline_audit_files(
    audit_path: Path,
    candidates_path: Path,
    tracks_path: Path,
    resources_path: Path,
    *,
    today: date | None = None,
) -> tuple[dict[str, Any] | None, list[Issue], dict[str, int]]:
    try:
        audit_data = load_json(audit_path)
        candidates = load_json(candidates_path)
        taxonomy = load_json(tracks_path)
        resources = load_json(resources_path)
    except (OSError, QualityError) as exc:
        return (
            None,
            [Issue("error", "mainline_audit.input", str(exc))],
            {},
        )
    issues = mainline_audit_issues(
        audit_data,
        candidates,
        taxonomy,
        resources,
        source=audit_path.as_posix(),
        today=today,
    )
    audits: Sequence[Mapping[str, Any]] = [
        item for item in audit_data.get("audits", []) if isinstance(item, Mapping)
    ]
    statistics = {
        "tracks": len(
            {
                item.get("track")
                for item in audits
                if isinstance(item.get("track"), str)
            }
        ),
        "mainlines": len(audits),
        "preferred": sum(item.get("preferred") is True for item in audits),
        "pass": sum(item.get("status") == "pass" for item in audits),
        "review": sum(item.get("status") == "review" for item in audits),
    }
    return audit_data, issues, statistics


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the independent audit of every mainline course."
    )
    parser.add_argument("--audit", default="data/mainline_audit.json")
    parser.add_argument("--candidates", default="data/course_candidates.json")
    parser.add_argument("--tracks", default="data/tracks.json")
    parser.add_argument("--resources", default="data/course_resources.json")
    parser.add_argument("--json-report")
    parser.add_argument("--warnings-as-errors", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _, issues, statistics = validate_mainline_audit_files(
        repo_path(args.audit),
        repo_path(args.candidates),
        repo_path(args.tracks),
        repo_path(args.resources),
    )
    emit_issues(issues)
    print(
        "Mainline audit: "
        f"{statistics.get('tracks', 0)} tracks, "
        f"{statistics.get('mainlines', 0)} mainlines, "
        f"{statistics.get('preferred', 0)} preferred, "
        f"{statistics.get('pass', 0)} pass, "
        f"{statistics.get('review', 0)} review"
    )
    write_json_report(
        repo_path(args.json_report) if args.json_report else None,
        {
            "ok": exit_code(issues, warnings_as_errors=args.warnings_as_errors) == 0,
            "statistics": statistics,
            "issues": [issue.to_dict() for issue in issues],
        },
    )
    return exit_code(issues, warnings_as_errors=args.warnings_as_errors)


if __name__ == "__main__":
    raise SystemExit(main())
