from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.course_guides import load_course_guides
from scripts.quality_common import (
    Issue,
    QualityError,
    emit_issues,
    exit_code,
    load_json,
    repo_path,
    write_json_report,
)

MINIMUM_RESEARCHED_GUIDES = 60


def track_coverage_issues(
    catalogue: Mapping[str, Any],
    guides: Mapping[int, Mapping[str, Any]],
    *,
    source: str = "data/course_guides.json",
) -> tuple[list[Issue], dict[str, int]]:
    courses = [
        course
        for course in catalogue.get("courses", [])
        if isinstance(course, Mapping)
        and isinstance(course.get("source_id"), int)
        and isinstance(course.get("track"), str)
    ]
    populated_tracks = {str(course["track"]) for course in courses}
    course_tracks = {
        int(course["source_id"]): str(course["track"]) for course in courses
    }
    covered_tracks = {
        course_tracks[course_id]
        for course_id in guides
        if course_id in course_tracks
    }
    missing = sorted(populated_tracks - covered_tracks)
    issues = []
    if missing:
        issues.append(
            Issue(
                "error",
                "guide.track_coverage",
                f"{len(missing)} populated track(s) lack a researched guide",
                source,
                context=", ".join(missing),
            )
        )
    return issues, {
        "tracks_populated": len(populated_tracks),
        "tracks_covered": len(covered_tracks),
    }


def mainline_guide_coverage_issues(
    mainline_audit: Mapping[str, Any] | None,
    guides: Mapping[int, Mapping[str, Any]],
    *,
    source: str = "data/course_guides.json",
    audit_source: str = "data/mainline_audit.json",
) -> tuple[list[Issue], dict[str, int]]:
    records = (
        mainline_audit.get("audits")
        if isinstance(mainline_audit, Mapping)
        else None
    )
    if not isinstance(records, list):
        return [
            Issue(
                "error",
                "guide.mainline_audit_shape",
                "mainline audit must contain an audits array",
                audit_source,
            )
        ], {
            "mainlines_audited": 0,
            "mainlines_covered": 0,
        }

    audited_ids = {
        int(record["course_id"])
        for record in records
        if isinstance(record, Mapping)
        and isinstance(record.get("course_id"), int)
        and not isinstance(record.get("course_id"), bool)
    }
    if not audited_ids:
        return [
            Issue(
                "error",
                "guide.mainline_audit_empty",
                "mainline audit contains no valid course IDs",
                audit_source,
            )
        ], {
            "mainlines_audited": 0,
            "mainlines_covered": 0,
        }

    covered_ids = audited_ids & set(guides)
    missing = sorted(audited_ids - covered_ids)
    issues: list[Issue] = []
    if missing:
        issues.append(
            Issue(
                "error",
                "guide.mainline_coverage",
                f"{len(missing)} audited mainline course(s) lack a researched guide",
                source,
                context=", ".join(f"{course_id:03d}" for course_id in missing),
            )
        )
    return issues, {
        "mainlines_audited": len(audited_ids),
        "mainlines_covered": len(covered_ids),
    }


def release_gate_issues(
    catalogue: Mapping[str, Any],
    guides: Mapping[int, Mapping[str, Any]],
    *,
    mainline_audit: Mapping[str, Any] | None = None,
    minimum_guides: int = MINIMUM_RESEARCHED_GUIDES,
    require_track_coverage: bool = True,
    require_mainline_coverage: bool = True,
    source: str = "data/course_guides.json",
    audit_source: str = "data/mainline_audit.json",
) -> tuple[list[Issue], dict[str, int]]:
    issues: list[Issue] = []
    if len(guides) < minimum_guides:
        issues.append(
            Issue(
                "error",
                "guide.minimum_count",
                f"expected at least {minimum_guides} researched guides, found {len(guides)}",
                source,
            )
        )
    coverage_issues, coverage = track_coverage_issues(
        catalogue,
        guides,
        source=source,
    )
    if require_track_coverage:
        issues.extend(coverage_issues)
    mainline_issues, mainline_coverage = mainline_guide_coverage_issues(
        mainline_audit,
        guides,
        source=source,
        audit_source=audit_source,
    )
    if require_mainline_coverage:
        issues.extend(mainline_issues)
    return issues, {
        "guides": len(guides),
        "minimum_guides": minimum_guides,
        **coverage,
        **mainline_coverage,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate bilingual researched course guides and evidence boundaries."
    )
    parser.add_argument("--catalogue", default="data/courses.json")
    parser.add_argument("--manifest", default="data/course_guides.json")
    parser.add_argument("--mainline-audit", default="data/mainline_audit.json")
    parser.add_argument("--schema", default="data/course-guide.schema.json")
    parser.add_argument(
        "--minimum-guides",
        type=int,
        default=MINIMUM_RESEARCHED_GUIDES,
    )
    coverage = parser.add_mutually_exclusive_group()
    coverage.add_argument(
        "--require-track-coverage",
        dest="require_track_coverage",
        action="store_true",
        help="require at least one researched guide in every populated track (default)",
    )
    coverage.add_argument(
        "--allow-partial-track-coverage",
        dest="require_track_coverage",
        action="store_false",
        help="development-only escape hatch for deliberately partial fixtures",
    )
    parser.set_defaults(require_track_coverage=True)
    mainline_coverage = parser.add_mutually_exclusive_group()
    mainline_coverage.add_argument(
        "--require-mainline-coverage",
        dest="require_mainline_coverage",
        action="store_true",
        help="require a researched guide for every independently audited mainline course (default)",
    )
    mainline_coverage.add_argument(
        "--allow-partial-mainline-coverage",
        dest="require_mainline_coverage",
        action="store_false",
        help="development-only escape hatch for deliberately partial fixtures",
    )
    parser.set_defaults(require_mainline_coverage=True)
    parser.add_argument("--json-report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        catalogue = load_json(repo_path(args.catalogue))
    except (OSError, QualityError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    mainline_audit: Mapping[str, Any] | None = None
    if args.require_mainline_coverage:
        try:
            mainline_audit = load_json(repo_path(args.mainline_audit))
        except (OSError, QualityError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
    guides, issues = load_course_guides(
        repo_path(args.manifest),
        catalogue,
        repo_path(args.schema),
    )
    release_issues, statistics = release_gate_issues(
        catalogue,
        guides,
        mainline_audit=mainline_audit,
        minimum_guides=args.minimum_guides,
        require_track_coverage=args.require_track_coverage,
        require_mainline_coverage=args.require_mainline_coverage,
        source=args.manifest,
        audit_source=args.mainline_audit,
    )
    issues.extend(release_issues)
    emit_issues(issues)
    print(
        f"Course guides: {len(guides)} researched bilingual guide"
        f"{'s' if len(guides) != 1 else ''}; "
        f"{statistics['tracks_covered']}/{statistics['tracks_populated']} populated tracks; "
        f"{statistics['mainlines_covered']}/{statistics['mainlines_audited']} audited mainlines"
    )
    write_json_report(
        repo_path(args.json_report) if args.json_report else None,
        {
            "ok": exit_code(issues) == 0,
            **statistics,
            "issues": [issue.to_dict() for issue in issues],
        },
    )
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
