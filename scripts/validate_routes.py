from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

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

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def route_issues(
    route_data: Any,
    catalogue: Any,
    *,
    source: str = "data/routes.json",
    minimum_routes: int = 10,
    minimum_unique_courses: int = 100,
) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(route_data, Mapping) or not isinstance(route_data.get("routes"), list):
        return [Issue("error", "routes.shape", "routes data must contain routes[]", source)]
    if not isinstance(catalogue, Mapping) or not isinstance(catalogue.get("courses"), list):
        return [
            Issue(
                "error",
                "routes.catalogue_shape",
                "canonical catalogue must contain courses[]",
                "data/courses.json",
            )
        ]
    routes = route_data["routes"]
    if len(routes) < minimum_routes:
        issues.append(
            Issue(
                "error",
                "routes.count",
                f"expected at least {minimum_routes} routes, found {len(routes)}",
                source,
            )
        )
    courses_by_id = {
        course.get("source_id"): course
        for course in catalogue["courses"]
        if isinstance(course, Mapping) and isinstance(course.get("source_id"), int)
    }
    course_ids = set(courses_by_id)
    route_ids: set[str] = set()
    referenced: Counter[int] = Counter()
    exit_pairs: set[tuple[str, str]] = set()
    for route_index, route in enumerate(routes):
        path = f"{source}:routes/{route_index}"
        if not isinstance(route, Mapping):
            issues.append(Issue("error", "routes.item", "route must be an object", path))
            continue
        route_id = route.get("id")
        if route_id in route_ids:
            issues.append(Issue("error", "routes.id_duplicate", str(route_id), path))
        elif isinstance(route_id, str):
            route_ids.add(route_id)
        for key in (
            "title_zh",
            "title_en",
            "audience_zh",
            "audience_en",
            "outcome_zh",
            "outcome_en",
        ):
            if not isinstance(route.get(key), str) or not route[key].strip():
                issues.append(
                    Issue("error", "routes.translation", f"{key} must be non-empty", path)
                )
        stages = route.get("stages")
        if not isinstance(stages, list) or not stages:
            issues.append(Issue("error", "routes.stages", "route needs a non-empty stage", path))
            continue
        seen_in_route: set[int] = set()
        guaranteed_before_stage: set[int] = set()
        for stage_index, stage in enumerate(stages):
            stage_path = f"{path}/stages/{stage_index}"
            if not isinstance(stage, Mapping):
                issues.append(Issue("error", "routes.stage_type", "stage must be an object", stage_path))
                continue
            for key in ("name_zh", "name_en", "exit_zh", "exit_en"):
                if not isinstance(stage.get(key), str) or not stage[key].strip():
                    issues.append(
                        Issue("error", "routes.stage_translation", f"{key} is required", stage_path)
                    )
            ids = stage.get("course_ids")
            if not isinstance(ids, list) or not ids:
                issues.append(
                    Issue("error", "routes.stage_empty", "course_ids must be non-empty", stage_path)
                )
                continue
            stage_id_set = {
                course_id
                for course_id in ids
                if isinstance(course_id, int) and not isinstance(course_id, bool)
            }
            if len(stage_id_set) != len(ids):
                issues.append(
                    Issue(
                        "error",
                        "routes.stage_course_duplicate",
                        "course_ids must contain unique integer course identifiers",
                        stage_path,
                    )
                )
            raw_path_options = stage.get("path_options")
            if raw_path_options is None:
                path_options: list[Any] = []
            elif not isinstance(raw_path_options, list):
                issues.append(
                    Issue(
                        "error",
                        "routes.stage_path_type",
                        "path_options must be an array",
                        stage_path,
                    )
                )
                path_options = []
            else:
                path_options = raw_path_options
                if len(path_options) < 2:
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_path_count",
                            "path_options must contain at least two complete alternatives",
                            stage_path,
                        )
                    )
            required_ids = stage.get("required_course_ids")
            if not isinstance(required_ids, list):
                issues.append(
                    Issue(
                        "error",
                        "routes.stage_required_type",
                        "required_course_ids must be an array",
                        stage_path,
                    )
                )
                required_ids = []
            required_set = {
                course_id
                for course_id in required_ids
                if isinstance(course_id, int) and not isinstance(course_id, bool)
            }
            if len(required_set) != len(required_ids):
                issues.append(
                    Issue(
                        "error",
                        "routes.stage_required_duplicate",
                        "required_course_ids must contain unique integer course identifiers",
                        stage_path,
                    )
                )
            if not required_ids and not path_options:
                issues.append(
                    Issue(
                        "error",
                        "routes.stage_required_empty",
                        "a stage needs required courses or complete path options",
                        stage_path,
                    )
                )
            if not required_set.issubset(stage_id_set):
                issues.append(
                    Issue(
                        "error",
                        "routes.stage_required_subset",
                        "required_course_ids must be a subset of course_ids",
                        stage_path,
                    )
                )
            elif [course_id for course_id in ids if course_id in required_set] != required_ids:
                issues.append(
                    Issue(
                        "error",
                        "routes.stage_required_order",
                        "required_course_ids must preserve the order in course_ids",
                        stage_path,
                    )
                )
            for course_id in required_ids:
                course = courses_by_id.get(course_id)
                if isinstance(course, Mapping) and course.get("role") != "mainline":
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_required_not_mainline",
                            f"required course_id {course_id!r} is not a mainline course",
                            stage_path,
                        )
                    )
            path_ids: set[str] = set()
            path_labels: dict[str, set[str]] = {"label_zh": set(), "label_en": set()}
            path_course_ids: set[int] = set()
            for option_index, option in enumerate(path_options):
                option_path = f"{stage_path}/path_options/{option_index}"
                if not isinstance(option, Mapping):
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_path_item",
                            "each path option must be an object",
                            option_path,
                        )
                    )
                    continue
                option_id = option.get("id")
                if not isinstance(option_id, str) or not _SLUG_RE.fullmatch(option_id):
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_path_id",
                            "path option id must be a non-empty lowercase slug",
                            option_path,
                        )
                    )
                elif option_id in path_ids:
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_path_id_duplicate",
                            f"path option id {option_id!r} is duplicated",
                            option_path,
                        )
                    )
                else:
                    path_ids.add(option_id)
                for key in ("label_zh", "label_en"):
                    label = option.get(key)
                    normalized = label.strip().casefold() if isinstance(label, str) else ""
                    if not normalized:
                        issues.append(
                            Issue(
                                "error",
                                "routes.stage_path_translation",
                                f"{key} must be non-empty",
                                option_path,
                            )
                        )
                    elif normalized in path_labels[key]:
                        issues.append(
                            Issue(
                                "error",
                                "routes.stage_path_label_duplicate",
                                f"{key} must uniquely identify the path option",
                                option_path,
                            )
                        )
                    else:
                        path_labels[key].add(normalized)
                option_ids = option.get("course_ids")
                if not isinstance(option_ids, list) or not option_ids:
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_path_empty",
                            "path option course_ids must be a non-empty array",
                            option_path,
                        )
                    )
                    continue
                option_set = {
                    course_id
                    for course_id in option_ids
                    if isinstance(course_id, int) and not isinstance(course_id, bool)
                }
                if len(option_set) != len(option_ids):
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_path_duplicate",
                            "path option course_ids must contain unique integer identifiers",
                            option_path,
                        )
                    )
                if not option_set.issubset(stage_id_set):
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_path_subset",
                            "path option course_ids must be a subset of stage course_ids",
                            option_path,
                        )
                    )
                elif [course_id for course_id in ids if course_id in option_set] != option_ids:
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_path_order",
                            "path option course_ids must preserve the order in stage course_ids",
                            option_path,
                        )
                    )
                overlap_required = option_set.intersection(required_set)
                if overlap_required:
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_path_required_overlap",
                            "path option courses cannot also be required courses",
                            option_path,
                        )
                    )
                overlap_paths = option_set.intersection(path_course_ids)
                if overlap_paths:
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_path_course_duplicate",
                            "a course cannot appear in more than one complete path option",
                            option_path,
                        )
                    )
                path_course_ids.update(option_set)
            remaining_ids = [
                course_id
                for course_id in ids
                if course_id not in required_set and course_id not in path_course_ids
            ]
            raw_elective_ids = stage.get("elective_course_ids")
            explicit_elective_pool = raw_elective_ids is not None
            if raw_elective_ids is None:
                elective_candidates = (
                    remaining_ids if stage.get("elective_count") != 0 else []
                )
            elif not isinstance(raw_elective_ids, list) or not raw_elective_ids:
                issues.append(
                    Issue(
                        "error",
                        "routes.stage_elective_pool_empty",
                        "elective_course_ids must be a non-empty array when provided",
                        stage_path,
                    )
                )
                elective_candidates = []
            else:
                elective_candidates = raw_elective_ids
                elective_set = {
                    course_id
                    for course_id in elective_candidates
                    if isinstance(course_id, int) and not isinstance(course_id, bool)
                }
                if len(elective_set) != len(elective_candidates):
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_elective_pool_duplicate",
                            "elective_course_ids must contain unique integer identifiers",
                            stage_path,
                        )
                    )
                if not elective_set.issubset(set(remaining_ids)):
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_elective_pool_subset",
                            "elective_course_ids must be stage courses outside required and path options",
                            stage_path,
                        )
                    )
                elif [
                    course_id for course_id in ids if course_id in elective_set
                ] != elective_candidates:
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_elective_pool_order",
                            "elective_course_ids must preserve the order in course_ids",
                            stage_path,
                        )
                    )
            elective_count = stage.get("elective_count")
            remaining = len(elective_candidates)
            if (
                isinstance(elective_count, bool)
                or not isinstance(elective_count, int)
                or elective_count < 0
                or elective_count > remaining
            ):
                issues.append(
                    Issue(
                        "error",
                        "routes.stage_elective_count",
                        f"elective_count must be an integer from 0 to {remaining}",
                        stage_path,
                    )
                )
            if explicit_elective_pool and elective_count == 0:
                issues.append(
                    Issue(
                        "error",
                        "routes.stage_elective_pool_unused",
                        "elective_course_ids cannot be provided when elective_count is 0",
                        stage_path,
                    )
                )
            if path_options and elective_count != 0:
                issues.append(
                    Issue(
                        "error",
                        "routes.stage_path_elective_conflict",
                        "elective_count must be 0 when complete path options are present",
                        stage_path,
                    )
                )
            for course_id in required_ids:
                course = courses_by_id.get(course_id)
                if not isinstance(course, Mapping):
                    continue
                prerequisites = {
                    prerequisite_id
                    for prerequisite_id in course.get("prerequisite_course_ids", [])
                    if isinstance(prerequisite_id, int)
                    and not isinstance(prerequisite_id, bool)
                }
                missing = prerequisites.difference(guaranteed_before_stage)
                if missing:
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_required_prerequisite",
                            f"required course_id {course_id} has hard prerequisites "
                            f"{sorted(missing)} that are not guaranteed by previous stages",
                            stage_path,
                        )
                    )
            for option_index, option in enumerate(path_options):
                if not isinstance(option, Mapping):
                    continue
                earlier_in_path: set[int] = set()
                for course_id in option.get("course_ids", []):
                    course = courses_by_id.get(course_id)
                    if not isinstance(course, Mapping):
                        continue
                    prerequisites = {
                        prerequisite_id
                        for prerequisite_id in course.get("prerequisite_course_ids", [])
                        if isinstance(prerequisite_id, int)
                        and not isinstance(prerequisite_id, bool)
                    }
                    missing = prerequisites.difference(
                        guaranteed_before_stage | earlier_in_path
                    )
                    if missing:
                        issues.append(
                            Issue(
                                "error",
                                "routes.stage_path_prerequisite",
                                f"path course_id {course_id} has hard prerequisites "
                                f"{sorted(missing)} that are neither guaranteed by previous "
                                "stages nor completed earlier in this path",
                                f"{stage_path}/path_options/{option_index}",
                            )
                        )
                    if isinstance(course_id, int) and not isinstance(course_id, bool):
                        earlier_in_path.add(course_id)
            if (
                isinstance(elective_count, int)
                and not isinstance(elective_count, bool)
                and elective_count > 0
                and not path_options
            ):
                for course_id in elective_candidates:
                    course = courses_by_id.get(course_id)
                    if not isinstance(course, Mapping):
                        continue
                    prerequisites = {
                        prerequisite_id
                        for prerequisite_id in course.get("prerequisite_course_ids", [])
                        if isinstance(prerequisite_id, int)
                        and not isinstance(prerequisite_id, bool)
                    }
                    missing = prerequisites.difference(guaranteed_before_stage)
                    if missing:
                        issues.append(
                            Issue(
                                "error",
                                "routes.stage_elective_prerequisite",
                                f"elective course_id {course_id} has hard prerequisites "
                                f"{sorted(missing)} that are not guaranteed by previous stages; "
                                "model the dependent sequence as one complete path option",
                                stage_path,
                            )
                        )
            exit_pair = (
                str(stage.get("exit_zh", "")).strip(),
                str(stage.get("exit_en", "")).strip(),
            )
            if all(exit_pair):
                if exit_pair in exit_pairs:
                    issues.append(
                        Issue(
                            "error",
                            "routes.stage_exit_duplicate",
                            "stage exit criteria must be specific rather than duplicated boilerplate",
                            stage_path,
                        )
                    )
                exit_pairs.add(exit_pair)
            for course_id in ids:
                if course_id not in course_ids:
                    issues.append(
                        Issue(
                            "error",
                            "routes.course_missing",
                            f"course_id {course_id!r} is not in the canonical catalogue",
                            stage_path,
                        )
                    )
                if course_id in seen_in_route:
                    issues.append(
                        Issue(
                            "warning",
                            "routes.course_repeated",
                            f"course_id {course_id!r} appears twice in this route",
                            stage_path,
                        )
                    )
                if isinstance(course_id, int):
                    seen_in_route.add(course_id)
                    referenced[course_id] += 1
            guaranteed_before_stage.update(required_set.intersection(course_ids))
            if path_options:
                valid_path_sets = [
                    {
                        course_id
                        for course_id in option.get("course_ids", [])
                        if isinstance(course_id, int)
                        and not isinstance(course_id, bool)
                        and course_id in course_ids
                    }
                    for option in path_options
                    if isinstance(option, Mapping)
                ]
                if valid_path_sets:
                    guaranteed_before_stage.update(set.intersection(*valid_path_sets))
            elif (
                isinstance(elective_count, int)
                and not isinstance(elective_count, bool)
                and elective_count == len(elective_candidates)
            ):
                guaranteed_before_stage.update(
                    course_id
                    for course_id in elective_candidates
                    if course_id in course_ids
                )
    if not referenced:
        issues.append(Issue("error", "routes.coverage", "routes reference no courses", source))
    elif len(referenced) < minimum_unique_courses:
        issues.append(
            Issue(
                "error",
                "routes.course_coverage",
                f"expected at least {minimum_unique_courses} unique referenced courses, "
                f"found {len(referenced)}",
                source,
            )
        )
    return issues


def schema_issues(route_data: Any, schema: Any, source: str) -> list[Issue]:
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
    return [
        Issue(
            "error",
            "schema",
            error.message,
            f"{source}:{'/'.join(str(part) for part in error.absolute_path)}",
        )
        for error in sorted(validator.iter_errors(route_data), key=lambda item: list(item.path))
    ]


def validate_route_files(
    routes_path: Path,
    catalogue_path: Path,
    schema_path: Path,
    *,
    minimum_routes: int = 10,
    minimum_unique_courses: int = 100,
) -> tuple[dict[str, Any] | None, list[Issue], dict[str, Any]]:
    try:
        route_data = load_json(routes_path)
        catalogue = load_json(catalogue_path)
        schema = load_json(schema_path)
    except (OSError, QualityError) as exc:
        return None, [Issue("error", "routes.input", str(exc))], {}
    issues = schema_issues(route_data, schema, routes_path.as_posix())
    issues.extend(
        route_issues(
            route_data,
            catalogue,
            source=routes_path.as_posix(),
            minimum_routes=minimum_routes,
            minimum_unique_courses=minimum_unique_courses,
        )
    )
    referenced = {
        course_id
        for route in route_data.get("routes", [])
        if isinstance(route, Mapping)
        for stage in route.get("stages", [])
        if isinstance(stage, Mapping)
        for course_id in stage.get("course_ids", [])
        if isinstance(course_id, int)
    }
    statistics = {
        "routes": len(route_data.get("routes", [])),
        "stages": sum(
            len(route.get("stages", []))
            for route in route_data.get("routes", [])
            if isinstance(route, Mapping)
        ),
        "unique_courses_referenced": len(referenced),
        "required_course_slots": sum(
            len(stage.get("required_course_ids", []))
            for route in route_data.get("routes", [])
            if isinstance(route, Mapping)
            for stage in route.get("stages", [])
            if isinstance(stage, Mapping)
            and isinstance(stage.get("required_course_ids", []), list)
        ),
        "elective_course_slots": sum(
            stage.get("elective_count", 0)
            for route in route_data.get("routes", [])
            if isinstance(route, Mapping)
            for stage in route.get("stages", [])
            if isinstance(stage, Mapping)
            and isinstance(stage.get("elective_count", 0), int)
            and not isinstance(stage.get("elective_count", 0), bool)
        ),
        "path_option_groups": sum(
            1
            for route in route_data.get("routes", [])
            if isinstance(route, Mapping)
            for stage in route.get("stages", [])
            if isinstance(stage, Mapping) and stage.get("path_options")
        ),
        "path_option_course_slots": sum(
            len(option.get("course_ids", []))
            for route in route_data.get("routes", [])
            if isinstance(route, Mapping)
            for stage in route.get("stages", [])
            if isinstance(stage, Mapping)
            for option in stage.get("path_options", [])
            if isinstance(option, Mapping)
            and isinstance(option.get("course_ids", []), list)
        ),
        "catalogue_coverage_percent": (
            round(len(referenced) * 100 / len(catalogue.get("courses", [])), 2)
            if catalogue.get("courses")
            else 0.0
        ),
    }
    return route_data, list(dict.fromkeys(issues)), statistics


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate learning routes and course references.")
    parser.add_argument("--routes", default="data/routes.json")
    parser.add_argument("--catalogue", default="data/courses.json")
    parser.add_argument("--schema", default="data/route.schema.json")
    parser.add_argument("--minimum-routes", type=int, default=10)
    parser.add_argument("--minimum-unique-courses", type=int, default=100)
    parser.add_argument("--json-report")
    parser.add_argument("--warnings-as-errors", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _, issues, statistics = validate_route_files(
        repo_path(args.routes),
        repo_path(args.catalogue),
        repo_path(args.schema),
        minimum_routes=args.minimum_routes,
        minimum_unique_courses=args.minimum_unique_courses,
    )
    emit_issues(issues)
    print(
        f"Routes: {statistics.get('routes', 0)} routes, "
        f"{statistics.get('stages', 0)} stages, "
        f"{statistics.get('unique_courses_referenced', 0)} unique courses"
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
