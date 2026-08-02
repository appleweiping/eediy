from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.course_data import (
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


VIDEO_RESOURCE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "youtu.be",
    "vimeo.com",
    "www.vimeo.com",
}
PLATFORM_RESOURCE_HOSTS = {
    "coursera.org",
    "www.coursera.org",
    "edx.org",
    "www.edx.org",
}
PUBLISHER_RESOURCE_HOSTS = {
    "mitpress.mit.edu",
    "www.mitpress.mit.edu",
}
AUTH_GATED_RESOURCE_HOSTS = {
    "mediaspace.illinois.edu",
}
RESTRICTED_RESOURCE_PATH_RE = re.compile(
    r"/(?:secure|restricted|protected)(?:/|$)",
    re.IGNORECASE,
)
MACHINE_RESOURCE_SUFFIXES = {
    ".7z",
    ".c",
    ".cc",
    ".cpp",
    ".csv",
    ".gz",
    ".h",
    ".ipynb",
    ".m",
    ".mat",
    ".py",
    ".rar",
    ".sv",
    ".tar",
    ".tgz",
    ".v",
    ".vhd",
    ".zip",
}


def _looks_like_machine_resource(resource: Mapping[str, Any]) -> bool:
    """Return whether a code record points to a repository, file, or code index."""

    url = str(resource.get("url", ""))
    title = str(resource.get("title", {}).get("en", ""))
    if not title and isinstance(resource.get("title"), str):
        title = str(resource["title"])
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    path = parts.path.lower()
    if host in {"github.com", "www.github.com", "gitlab.com", "www.gitlab.com"}:
        return True
    if Path(path).suffix.lower() in MACHINE_RESOURCE_SUFFIXES:
        return True
    if any(
        token in path
        for token in (
            "/code",
            "/download",
            "/examples",
            "/labs",
            "/notebook",
            "/programming-assignments",
            "/software",
        )
    ):
        return True
    return bool(
        re.search(
            r"\b(?:archive|code|dataset|examples?|files?|notebooks?|repository|"
            r"software|source|starter)\b",
            title,
            re.IGNORECASE,
        )
    )


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
    maximum_age_days: int = 400,
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
    course_ids: set[str] = set()
    slugs_by_track: set[tuple[str, str]] = set()
    source_ids: set[int] = set()
    used_tracks: Counter[str] = Counter()
    primary_urls: dict[str, str] = {}
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
        for key in (
            "prerequisites",
            "official_prerequisites",
            "recommended_background",
        ):
            issues.extend(
                _localized_issues(course.get(key), f"{path}/{key}", list_value=True)
            )
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
                parts = urlsplit(url)
                host = (parts.hostname or "").lower()
                kind = str(resource.get("kind", ""))
                if kind == "code" and host in VIDEO_RESOURCE_HOSTS:
                    issues.append(
                        Issue(
                            "error",
                            "resource.kind_host_conflict",
                            "video-hosted material must not be classified as code",
                            resource_path,
                        )
                    )
                if (
                    kind in {"code", "projects"}
                    and host in PLATFORM_RESOURCE_HOSTS
                    and re.match(r"^/(?:learn|course)/", parts.path, re.IGNORECASE)
                ):
                    issues.append(
                        Issue(
                            "error",
                            "resource.kind_host_conflict",
                            "a platform course-product page is not a code or project artifact",
                            resource_path,
                        )
                    )
                if kind == "code" and host in PUBLISHER_RESOURCE_HOSTS:
                    issues.append(
                        Issue(
                            "error",
                            "resource.kind_host_conflict",
                            "a publisher product page is not a code artifact",
                            resource_path,
                        )
                    )
                if (
                    RESTRICTED_RESOURCE_PATH_RE.search(parts.path)
                    or host in AUTH_GATED_RESOURCE_HOSTS
                ) and resource.get("access") != "institutional":
                    issues.append(
                        Issue(
                            "error",
                            "resource.access_wall",
                            "known restricted or authentication-gated target must be marked institutional",
                            resource_path,
                        )
                    )
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
        coverage_kind_map = {
            "video": {"video"},
            "notes": {"notes", "textbook"},
            "practice": {"assignments", "projects"},
            "labs": {"labs"},
            "exams": {"exams"},
            "code": {"code"},
        }
        coverage = course.get("resource_coverage", {})
        if isinstance(coverage, Mapping):
            published_kinds = {
                str(resource.get("kind"))
                for resource in resources
                if isinstance(resource, Mapping)
                and resource.get("status") in {"available", "degraded", "archived"}
            }
            for coverage_key, resource_kinds in coverage_kind_map.items():
                if coverage.get(coverage_key) != 0:
                    continue
                conflicting_kinds = sorted(published_kinds.intersection(resource_kinds))
                if conflicting_kinds:
                    issues.append(
                        Issue(
                            "error",
                            "resource.coverage_kind_conflict",
                            f"{coverage_key} coverage is 0 but published resources use "
                            f"{', '.join(conflicting_kinds)}",
                            f"{path}/resource_coverage/{coverage_key}",
                        )
                    )
            if coverage.get("code") == 2:
                code_evidence = [
                    resource
                    for resource in resources
                    if isinstance(resource, Mapping)
                    and resource.get("kind") == "code"
                    and resource.get("status") in {"available", "degraded", "archived"}
                    and _looks_like_machine_resource(resource)
                ]
                if not code_evidence:
                    issues.append(
                        Issue(
                            "error",
                            "resource.code_coverage_evidence",
                            "code coverage 2 requires a reviewed repository, machine file, or course-specific code index",
                            f"{path}/resource_coverage/code",
                        )
                    )
    issues.extend(_course_prerequisite_issues(courses, source))
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
    maximum_age_days: int = 400,
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
            maximum_age_days=maximum_age_days,
        )
    )
    # Remove identical errors emitted by both schema and semantic checks.
    issues = list(dict.fromkeys(issues))
    return catalogue if isinstance(catalogue, dict) else None, issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the canonical course catalogue.")
    parser.add_argument("--catalogue", default="data/courses.json")
    parser.add_argument("--schema", default="data/course.schema.json")
    parser.add_argument("--maximum-age-days", type=int, default=400)
    parser.add_argument("--json-report")
    parser.add_argument("--warnings-as-errors", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    catalogue, issues = validate_file(
        repo_path(args.catalogue),
        repo_path(args.schema),
        maximum_age_days=args.maximum_age_days,
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
