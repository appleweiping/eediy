from __future__ import annotations

import argparse
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.course_data import (
    HIGH_VALUE_RESOURCE_KINDS,
    RESOURCE_ACCESS,
    RESOURCE_STATUSES,
    _track_cycle_issues,
    catalogue_statistics,
    normalize_url,
    parse_iso_date,
)
from scripts.quality_common import (
    Issue,
    QualityError,
    emit_issues,
    exit_code,
    load_json,
    repo_path,
    write_json_report,
)


HIGH_RISK_PROJECT_TRACKS = {
    "fabrication-mems",
    "optics-photonics",
    "power-electronics",
    "power-systems-machines",
    "energy-storage-pv",
    "rf-microwave-antennas",
    "robotics",
    "capstone-practice",
}
LOW_ENERGY_PROJECT_TRACKS = {
    "ee-introduction",
    "circuits",
    "electronics-laboratory",
    "analog-electronics",
    "fpga-soc",
    "embedded-systems",
    "pcb-eda",
    "sensors-instrumentation",
}


def _jsonschema_issues(catalogue: Any, schema: Any, source: str) -> list[Issue]:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:
        return [
            Issue(
                "error",
                "schema.dependency",
                "jsonschema is required; install requirements-dev.txt",
                source,
            )
        ]
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    issues: list[Issue] = []
    for error in sorted(validator.iter_errors(catalogue), key=lambda item: list(item.path)):
        pointer = "/".join(str(part) for part in error.absolute_path)
        path = f"{source}:{pointer}" if pointer else source
        issues.append(Issue("error", "schema", error.message, path))
    return issues


def _localized_issues(value: Any, path: str, *, list_value: bool = False) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(value, Mapping):
        return [Issue("error", "translation.type", "localized value must be an object", path)]
    for language in ("zh", "en"):
        translated = value.get(language)
        if list_value:
            if not isinstance(translated, list):
                issues.append(
                    Issue("error", "translation.list", f"{language} must be a list", path)
                )
            elif any(not isinstance(item, str) or not item.strip() for item in translated):
                issues.append(
                    Issue(
                        "error",
                        "translation.empty_item",
                        f"{language} contains an empty translation",
                        path,
                    )
                )
        elif not isinstance(translated, str) or not translated.strip():
            issues.append(
                Issue("error", "translation.missing", f"{language} translation is empty", path)
            )
    if list_value and isinstance(value.get("zh"), list) and isinstance(value.get("en"), list):
        if len(value["zh"]) != len(value["en"]):
            issues.append(
                Issue(
                    "error",
                    "translation.cardinality",
                    "zh and en lists must have the same number of items",
                    path,
                )
            )
    return issues


def _course_prerequisite_issues(
    courses: Sequence[Any], source: str
) -> list[Issue]:
    graph = {
        int(course["source_id"]): [
            prerequisite_id
            for prerequisite_id in course.get("prerequisite_course_ids", [])
            if isinstance(prerequisite_id, int)
            and not isinstance(prerequisite_id, bool)
        ]
        for course in courses
        if isinstance(course, Mapping)
        and isinstance(course.get("source_id"), int)
        and not isinstance(course.get("source_id"), bool)
    }
    issues: list[Issue] = []
    for index, course in enumerate(courses):
        if not isinstance(course, Mapping):
            continue
        source_id = course.get("source_id")
        prerequisite_ids = course.get("prerequisite_course_ids", [])
        if not isinstance(prerequisite_ids, list):
            continue
        for prerequisite_id in prerequisite_ids:
            if prerequisite_id == source_id:
                issues.append(
                    Issue(
                        "error",
                        "course.prerequisite_self",
                        "a course cannot require itself",
                        f"{source}:courses/{index}/prerequisite_course_ids",
                    )
                )
            elif prerequisite_id not in graph:
                issues.append(
                    Issue(
                        "error",
                        "course.prerequisite_missing",
                        f"unknown prerequisite course id {prerequisite_id!r}",
                        f"{source}:courses/{index}/prerequisite_course_ids",
                    )
                )

    visiting: set[int] = set()
    visited: set[int] = set()
    stack: list[int] = []

    def visit(node: int) -> None:
        if node in visited:
            return
        if node in visiting:
            start = stack.index(node)
            cycle = stack[start:] + [node]
            issues.append(
                Issue(
                    "error",
                    "course.prerequisite_cycle",
                    " -> ".join(str(course_id) for course_id in cycle),
                    source,
                )
            )
            return
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for source_id in graph:
        visit(source_id)
    return list(dict.fromkeys(issues))


def semantic_issues(
    catalogue: Any,
    *,
    source: str = "data/courses.json",
    minimum_courses: int = 125,
    minimum_used_tracks: int = 24,
    maximum_age_days: int = 400,
    minimum_unique_resources: int = 550,
    minimum_project_courses: int = 100,
    today: date | None = None,
) -> list[Issue]:
    issues: list[Issue] = []
    today = today or date.today()
    if not isinstance(catalogue, Mapping):
        return [Issue("error", "catalogue.type", "catalogue must be an object", source)]
    tracks = catalogue.get("tracks", [])
    courses = catalogue.get("courses", [])
    if not isinstance(tracks, list) or not isinstance(courses, list):
        return [Issue("error", "catalogue.shape", "tracks and courses must be arrays", source)]
    if len(courses) < minimum_courses:
        issues.append(
            Issue(
                "error",
                "catalogue.course_count",
                f"expected at least {minimum_courses} courses, found {len(courses)}",
                source,
            )
        )
    track_ids: set[str] = set()
    track_orders: set[int] = set()
    for index, track in enumerate(tracks):
        path = f"{source}:tracks/{index}"
        if not isinstance(track, Mapping):
            continue
        track_id = track.get("id")
        if track_id in track_ids:
            issues.append(Issue("error", "track.duplicate", str(track_id), path))
        elif isinstance(track_id, str):
            track_ids.add(track_id)
        order = track.get("order")
        if isinstance(order, int) and order in track_orders:
            issues.append(Issue("error", "track.order_duplicate", str(order), path))
        elif isinstance(order, int):
            track_orders.add(order)
        for key in ("title", "summary"):
            issues.extend(_localized_issues(track.get(key), f"{path}/{key}"))
        issues.extend(_localized_issues(track.get("outcomes"), f"{path}/outcomes", list_value=True))
    for index, track in enumerate(tracks):
        if not isinstance(track, Mapping):
            continue
        for prerequisite in track.get("prerequisite_tracks", []):
            if prerequisite not in track_ids:
                issues.append(
                    Issue(
                        "error",
                        "track.prerequisite_missing",
                        f"{prerequisite!r} does not name a canonical track",
                        f"{source}:tracks/{index}",
                    )
                )
    issues.extend(_track_cycle_issues(tracks))
    track_titles = {
        str(track.get("id")): track.get("title", {})
        for track in tracks
        if isinstance(track, Mapping) and track.get("id")
    }

    course_ids: set[str] = set()
    slugs_by_track: set[tuple[str, str]] = set()
    source_ids: set[int] = set()
    used_tracks: Counter[str] = Counter()
    primary_urls: dict[str, str] = {}
    high_value_urls: set[str] = set()
    project_course_count = 0
    for index, course in enumerate(courses):
        path = f"{source}:courses/{index}"
        if not isinstance(course, Mapping):
            continue
        course_id = course.get("id")
        if course_id in course_ids:
            issues.append(Issue("error", "course.duplicate", str(course_id), path))
        elif isinstance(course_id, str):
            course_ids.add(course_id)
        source_id = course.get("source_id")
        if isinstance(source_id, int) and source_id in source_ids:
            issues.append(Issue("error", "course.source_duplicate", str(source_id), path))
        elif isinstance(source_id, int):
            source_ids.add(source_id)
        track = course.get("track")
        if track not in track_ids:
            issues.append(
                Issue("error", "course.track_missing", f"unknown track {track!r}", path)
            )
        elif isinstance(track, str):
            used_tracks[track] += 1
        slug_key = (str(track), str(course.get("slug")))
        if slug_key in slugs_by_track:
            issues.append(
                Issue("error", "course.slug_duplicate", f"{slug_key[0]}/{slug_key[1]}", path)
            )
        slugs_by_track.add(slug_key)
        for key in ("title", "summary", "selection_note", "review_note"):
            issues.extend(_localized_issues(course.get(key), f"{path}/{key}"))
        for key in ("prerequisites", "outcomes"):
            issues.extend(
                _localized_issues(course.get(key), f"{path}/{key}", list_value=True)
            )
        issues.extend(
            _localized_issues(
                course.get("completion_evidence"),
                f"{path}/completion_evidence",
                list_value=True,
            )
        )
        completion_evidence = course.get("completion_evidence", {})
        if isinstance(completion_evidence, Mapping):
            for language in ("zh", "en"):
                if not completion_evidence.get(language):
                    issues.append(
                        Issue(
                            "error",
                            "course.completion_evidence_empty",
                            f"{language} completion evidence must not be empty",
                            path,
                        )
                    )
        study_plan = course.get("study_plan")
        if isinstance(study_plan, Mapping):
            issues.extend(
                _localized_issues(study_plan.get("note"), f"{path}/study_plan/note")
            )
            note = study_plan.get("note", {})
            zh_note = str(note.get("zh", "")) if isinstance(note, Mapping) else ""
            en_note = str(note.get("en", "")).casefold() if isinstance(note, Mapping) else ""
            if not (
                any(token in zh_note for token in ("提供方", "维护者"))
                and any(token in en_note for token in ("provider", "maintainer"))
            ):
                issues.append(
                    Issue(
                        "error",
                        "course.workload_provenance_missing",
                        "workload must identify a provider source or a maintainer estimate in both languages",
                        path,
                    )
                )
            if "两周" not in zh_note or "two weeks" not in en_note:
                issues.append(
                    Issue(
                        "error",
                        "course.workload_calibration_missing",
                        "workload guidance must include the bilingual two-week calibration step",
                        path,
                    )
                )
        tooling = course.get("tooling")
        if isinstance(tooling, Mapping):
            for key in ("software", "hardware"):
                issues.extend(
                    _localized_issues(
                        tooling.get(key), f"{path}/tooling/{key}", list_value=True
                    )
                )
            issues.extend(
                _localized_issues(tooling.get("cost_note"), f"{path}/tooling/cost_note")
            )
        safety = course.get("safety")
        if isinstance(safety, Mapping):
            issues.extend(_localized_issues(safety.get("note"), f"{path}/safety/note"))
        reviewed = parse_iso_date(course.get("last_reviewed"))
        if reviewed is not None:
            if reviewed > today:
                issues.append(
                    Issue("error", "course.review_future", str(course["last_reviewed"]), path)
                )
            elif (today - reviewed).days > maximum_age_days:
                issues.append(
                    Issue(
                        "error",
                        "course.review_stale",
                        f"last reviewed {(today - reviewed).days} days ago",
                        path,
                    )
                )
        resources = course.get("resources", [])
        if not resources:
            issues.append(Issue("error", "resource.missing", "at least one resource required", path))
        resource_ids: set[str] = set()
        resource_urls_in_course: set[str] = set()
        for resource_index, resource in enumerate(resources):
            resource_path = f"{path}/resources/{resource_index}"
            if not isinstance(resource, Mapping):
                continue
            resource_id = resource.get("id")
            if resource_id in resource_ids:
                issues.append(
                    Issue("error", "resource.id_duplicate", str(resource_id), resource_path)
                )
            elif isinstance(resource_id, str):
                resource_ids.add(resource_id)
            issues.extend(_localized_issues(resource.get("title"), f"{resource_path}/title"))
            for key in ("access", "license", "status", "last_verified"):
                if not resource.get(key):
                    issues.append(
                        Issue(
                            "error",
                            "resource.metadata",
                            f"{key} is required for every resource",
                            resource_path,
                        )
                    )
            if resource.get("access") not in RESOURCE_ACCESS:
                issues.append(
                    Issue(
                        "error",
                        "resource.access",
                        f"unsupported access state {resource.get('access')!r}",
                        resource_path,
                    )
                )
            if resource.get("status") not in RESOURCE_STATUSES:
                issues.append(
                    Issue(
                        "error",
                        "resource.status",
                        f"unsupported status {resource.get('status')!r}",
                        resource_path,
                    )
                )
            verified = parse_iso_date(resource.get("last_verified"))
            if verified is not None:
                if verified > today:
                    issues.append(
                        Issue(
                            "error",
                            "resource.verified_future",
                            str(resource["last_verified"]),
                            resource_path,
                        )
                    )
                elif (today - verified).days > maximum_age_days:
                    issues.append(
                        Issue(
                            "error",
                            "resource.verified_stale",
                            f"last verified {(today - verified).days} days ago",
                            resource_path,
                        )
                    )
            url = resource.get("url")
            if isinstance(url, str):
                normalized_url = normalize_url(url)
                if normalized_url in resource_urls_in_course:
                    issues.append(
                        Issue(
                            "error",
                            "resource.url_duplicate",
                            f"duplicate normalized URL within course: {normalized_url}",
                            resource_path,
                        )
                    )
                resource_urls_in_course.add(normalized_url)
                query_keys = {
                    part.split("=", 1)[0].casefold()
                    for part in url.split("?", 1)[1].split("&")
                } if "?" in url else set()
                if any(
                    key.startswith("utm_") or key in {"fbclid", "gclid", "mc_cid", "mc_eid"}
                    for key in query_keys
                ):
                    issues.append(
                        Issue(
                            "error",
                            "resource.tracking_url",
                            "remove tracking parameters from the resource URL",
                            resource_path,
                        )
                    )
                if (
                    resource.get("kind") in HIGH_VALUE_RESOURCE_KINDS
                    and resource.get("status") in {"available", "degraded", "archived"}
                ):
                    high_value_urls.add(normalized_url)
            if isinstance(url, str) and resource_index == 0:
                if url in primary_urls and primary_urls[url] != course_id:
                    issues.append(
                        Issue(
                            "warning",
                            "resource.primary_duplicate",
                            f"primary URL also belongs to {primary_urls[url]}",
                            resource_path,
                        )
                    )
                else:
                    primary_urls[url] = str(course_id)
        projects = course.get("projects", [])
        if projects:
            project_course_count += 1
        for project_index, project in enumerate(projects):
            if not isinstance(project, Mapping):
                continue
            project_path = f"{path}/projects/{project_index}"
            for key in ("title", "brief"):
                issues.extend(_localized_issues(project.get(key), f"{project_path}/{key}"))
            for key in ("deliverables", "verification"):
                issues.extend(
                    _localized_issues(project.get(key), f"{project_path}/{key}", list_value=True)
                )
                value = project.get(key)
                if isinstance(value, Mapping):
                    for language in ("zh", "en"):
                        items = value.get(language)
                        if isinstance(items, list) and len(items) < 4:
                            issues.append(
                                Issue(
                                    "error",
                                    "project.evidence_count",
                                    f"{language} {key} requires at least 4 items",
                                    f"{project_path}/{key}",
                                )
                            )
            issues.extend(
                _localized_issues(
                    project.get("reproducibility"),
                    f"{project_path}/reproducibility",
                    list_value=True,
                )
            )
            reproducibility = project.get("reproducibility")
            if isinstance(reproducibility, Mapping):
                for language in ("zh", "en"):
                    items = reproducibility.get(language)
                    if isinstance(items, list) and len(items) < 3:
                        issues.append(
                            Issue(
                                "error",
                                "project.evidence_count",
                                f"{language} reproducibility requires at least 3 items",
                                f"{project_path}/reproducibility",
                            )
                        )
            issues.extend(
                _localized_issues(
                    project.get("safety_note"),
                    f"{project_path}/safety_note",
                )
            )
            if project.get("origin") == "suggested":
                brief = project.get("brief", {})
                if isinstance(brief, Mapping):
                    if (
                        "维护者" not in str(brief.get("zh", ""))
                        or "不是课程官方作业" not in str(brief.get("zh", ""))
                        or "maintainer-suggested"
                        not in str(brief.get("en", "")).casefold()
                        or "not an official course assignment"
                        not in str(brief.get("en", "")).casefold()
                    ):
                        issues.append(
                            Issue(
                                "error",
                                "project.origin_disclosure",
                                "suggested project must be disclosed as maintainer-authored and non-official in both languages",
                                f"{project_path}/brief",
                            )
                        )
            course_title = course.get("title", {})
            project_title = project.get("title", {})
            project_brief = project.get("brief", {})
            canonical_track_title = track_titles.get(str(track), {})
            if all(
                isinstance(value, Mapping)
                for value in (course_title, project_title, project_brief, canonical_track_title)
            ):
                for language in ("zh", "en"):
                    rendered = " ".join(
                        (
                            str(project_title.get(language, "")),
                            str(project_brief.get(language, "")),
                        )
                    )
                    expected_context = (
                        str(course_title.get(language, "")),
                        str(canonical_track_title.get(language, "")),
                    )
                    if not any(value and value in rendered for value in expected_context):
                        issues.append(
                            Issue(
                                "error",
                                "project.context",
                                f"{language} project must name its course or track context",
                                project_path,
                            )
                        )
            safety_level = project.get("safety_level")
            if track in HIGH_RISK_PROJECT_TRACKS and safety_level not in {
                "simulation-only",
                "supervised",
            }:
                issues.append(
                    Issue(
                        "error",
                        "project.high_risk_safety",
                        "high-risk project must be simulation-only or supervised",
                        project_path,
                    )
                )
            safety_note = project.get("safety_note")
            if track in LOW_ENERGY_PROJECT_TRACKS and isinstance(safety_note, Mapping):
                zh_note = str(safety_note.get("zh", ""))
                en_note = str(safety_note.get("en", "")).casefold()
                if (
                    not all(token in zh_note for token in ("限流", "额定值", "断电"))
                    or not all(
                        token in en_note
                        for token in ("current-limit", "rating", "power removed")
                    )
                ):
                    issues.append(
                        Issue(
                            "error",
                            "project.low_energy_safety",
                            "low-energy project must require current limiting, rating checks, and unpowered wiring in both languages",
                            f"{project_path}/safety_note",
                        )
                    )
            if track == "biomedical" and isinstance(safety_note, Mapping):
                combined = " ".join(str(value) for value in safety_note.values()).casefold()
                required_tokens = ("公开", "合成", "public", "synthetic", "人体", "human")
                if not all(token.casefold() in combined for token in required_tokens):
                    issues.append(
                        Issue(
                            "error",
                            "project.biomedical_safety",
                            "biomedical project must use public or synthetic data and prohibit human collection",
                            f"{project_path}/safety_note",
                        )
                    )
    issues.extend(_course_prerequisite_issues(courses, source))
    if len(used_tracks) < minimum_used_tracks:
        issues.append(
            Issue(
                "error",
                "catalogue.used_track_count",
                f"expected at least {minimum_used_tracks} tracks with courses, found {len(used_tracks)}",
                source,
            )
        )
    if len(high_value_urls) < minimum_unique_resources:
        issues.append(
            Issue(
                "error",
                "catalogue.resource_count",
                f"expected at least {minimum_unique_resources} unique high-value resources, "
                f"found {len(high_value_urls)}",
                source,
            )
        )
    if project_course_count < minimum_project_courses:
        issues.append(
            Issue(
                "error",
                "catalogue.project_course_count",
                f"expected at least {minimum_project_courses} courses with projects, "
                f"found {project_course_count}",
                source,
            )
        )
    empty_mainlines = sorted(
        track_id
        for track_id in used_tracks
        if not any(
            course.get("track") == track_id and course.get("role") == "mainline"
            for course in courses
            if isinstance(course, Mapping)
        )
    )
    for track_id in empty_mainlines:
        issues.append(
            Issue(
                "warning",
                "track.no_mainline",
                f"{track_id} has courses but no mainline recommendation",
                source,
            )
        )
    return issues


def validate_file(
    catalogue_path: Path,
    schema_path: Path,
    *,
    minimum_courses: int = 125,
    minimum_used_tracks: int = 24,
    maximum_age_days: int = 400,
    minimum_unique_resources: int = 550,
    minimum_project_courses: int = 100,
) -> tuple[dict[str, Any] | None, list[Issue]]:
    try:
        catalogue = load_json(catalogue_path)
        schema = load_json(schema_path)
    except (OSError, QualityError) as exc:
        return None, [Issue("error", "catalogue.input", str(exc))]
    source = catalogue_path.as_posix()
    issues = _jsonschema_issues(catalogue, schema, source)
    issues.extend(
        semantic_issues(
            catalogue,
            source=source,
            minimum_courses=minimum_courses,
            minimum_used_tracks=minimum_used_tracks,
            maximum_age_days=maximum_age_days,
            minimum_unique_resources=minimum_unique_resources,
            minimum_project_courses=minimum_project_courses,
        )
    )
    # Remove identical errors emitted by both schema and semantic checks.
    issues = list(dict.fromkeys(issues))
    return catalogue if isinstance(catalogue, dict) else None, issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the canonical course catalogue.")
    parser.add_argument("--catalogue", default="data/courses.json")
    parser.add_argument("--schema", default="data/course.schema.json")
    parser.add_argument("--minimum-courses", type=int, default=125)
    parser.add_argument("--minimum-used-tracks", type=int, default=24)
    parser.add_argument("--maximum-age-days", type=int, default=400)
    parser.add_argument("--minimum-unique-resources", type=int, default=550)
    parser.add_argument("--minimum-project-courses", type=int, default=100)
    parser.add_argument("--json-report")
    parser.add_argument("--warnings-as-errors", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    catalogue, issues = validate_file(
        repo_path(args.catalogue),
        repo_path(args.schema),
        minimum_courses=args.minimum_courses,
        minimum_used_tracks=args.minimum_used_tracks,
        maximum_age_days=args.maximum_age_days,
        minimum_unique_resources=args.minimum_unique_resources,
        minimum_project_courses=args.minimum_project_courses,
    )
    statistics = catalogue_statistics(catalogue or {})
    emit_issues(issues)
    print(
        f"Catalogue: {statistics['courses']} courses, "
        f"{statistics['tracks_used']} used tracks, "
        f"{statistics['resource_metadata_percent']:.2f}% resource metadata"
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
