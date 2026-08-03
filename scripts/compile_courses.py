from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.course_data import compile_catalogue, load_taxonomy, validate_candidates
from scripts.course_data import validate_resource_manifest
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


def compile_from_files(
    candidates_path: Path,
    taxonomy_path: Path,
    output_path: Path,
    resources_path: Path | None = None,
) -> tuple[dict[str, Any] | None, list[Issue]]:
    try:
        candidates = load_json(candidates_path)
        taxonomy = load_json(taxonomy_path)
    except (OSError, QualityError) as exc:
        return None, [Issue("error", "compile.input", str(exc))]
    taxonomy_tracks, issues = load_taxonomy(taxonomy)
    taxonomy_ids = {
        str(track.get("id"))
        for track in taxonomy_tracks
        if isinstance(track, dict) and track.get("id")
    }
    issues.extend(validate_candidates(candidates, taxonomy_ids=taxonomy_ids))
    resource_records: list[dict[str, Any]] = []
    if resources_path is not None and resources_path.exists():
        try:
            resource_value = load_json(resources_path)
        except (OSError, QualityError) as exc:
            issues.append(Issue("error", "resource_manifest.input", str(exc)))
        else:
            records, resource_issues = validate_resource_manifest(
                resource_value,
                candidate_ids={
                    int(item["id"])
                    for item in candidates
                    if isinstance(item, dict) and isinstance(item.get("id"), int)
                },
                source=resources_path.as_posix(),
            )
            resource_records = [dict(record) for record in records]
            issues.extend(resource_issues)
    if any(issue.severity == "error" for issue in issues):
        return None, issues
    existing: dict[str, Any] | None = None
    if output_path.exists():
        try:
            loaded = load_json(output_path)
            if isinstance(loaded, dict):
                existing = loaded
            else:
                issues.append(
                    Issue("error", "compile.existing_type", "canonical catalogue must be an object")
                )
        except (OSError, QualityError) as exc:
            issues.append(Issue("error", "compile.existing", str(exc)))
    if any(issue.severity == "error" for issue in issues):
        return None, issues
    try:
        result = compile_catalogue(
            candidates,
            taxonomy_tracks,
            existing,
            resource_records=resource_records,
        )
    except (KeyError, TypeError, ValueError, QualityError) as exc:
        issues.append(Issue("error", "compile.catalogue", str(exc)))
        return None, issues
    return result, issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compile reviewed candidates into the bilingual canonical course catalogue."
    )
    parser.add_argument("--candidates", default="data/course_candidates.json")
    parser.add_argument("--taxonomy", default="data/tracks.json")
    parser.add_argument("--output", default="data/courses.json")
    parser.add_argument(
        "--resources",
        default="data/course_resources.json",
        help="Optional evidence manifest merged into canonical resources when present.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when the canonical file is missing or differs; do not write it.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    candidates_path = repo_path(args.candidates)
    taxonomy_path = repo_path(args.taxonomy)
    output_path = repo_path(args.output)
    resources_path = repo_path(args.resources) if args.resources else None
    result, issues = compile_from_files(
        candidates_path,
        taxonomy_path,
        output_path,
        resources_path,
    )
    if result is None:
        emit_issues(issues)
        return exit_code(issues)
    expected = stable_json(result)
    if args.check:
        if not output_path.exists():
            issues.append(
                Issue(
                    "error",
                    "compile.missing",
                    f"run scripts/compile_courses.py to create {args.output}",
                    args.output,
                )
            )
        else:
            current = output_path.read_text(encoding="utf-8")
            if current != expected:
                diff = "".join(
                    difflib.unified_diff(
                        current.splitlines(keepends=True),
                        expected.splitlines(keepends=True),
                        fromfile=args.output,
                        tofile=f"{args.output} (expected)",
                        n=2,
                    )
                )
                preview = "\n".join(diff.splitlines()[:30])
                issues.append(
                    Issue(
                        "error",
                        "compile.drift",
                        "canonical catalogue is stale; run scripts/compile_courses.py",
                        args.output,
                        context=preview,
                    )
                )
    else:
        atomic_write(output_path, expected)
        print(f"Wrote {args.output}: {len(result['courses'])} courses, {len(result['tracks'])} tracks")
    emit_issues(issues)
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
