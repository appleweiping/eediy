from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.quality_common import (
    QualityError,
    atomic_write,
    load_json,
    repo_path,
    split_front_matter,
)


BEGIN_MARKER = "# BEGIN GENERATED NAV"
END_MARKER = "# END GENERATED NAV"

LANGUAGE_ROOTS = {
    "zh": ("中文", ""),
    "en": ("English", "en/"),
}

PAGE_LABELS = {
    "zh": {
        "start_learning": "开始学习",
        "learning_routes": "路线",
        "course_directions": "课程方向",
        "resources_community": "资源与共建",
        "home": "前言",
        "getting_started": "如何使用",
        "roadmap": "总体规划",
        "routes": "路线总览",
        "tools": "必学工具",
        "books": "好书推荐",
        "math_foundations": "数学基础",
        "math_advanced": "数学进阶",
        "course_index": "课程总览",
        "practice": "实践",
        "contributing": "贡献指南",
        "license": "许可与引用",
        "postscript": "编辑说明",
    },
    "en": {
        "start_learning": "Start Learning",
        "learning_routes": "Routes",
        "course_directions": "Course Directions",
        "resources_community": "Resources and Community",
        "home": "Preface",
        "getting_started": "How to Use This Guide",
        "roadmap": "Overall Plan",
        "routes": "Route Index",
        "tools": "Essential Tools",
        "books": "Recommended Books",
        "math_foundations": "Mathematical Foundations",
        "math_advanced": "Advanced Mathematics",
        "course_index": "Course Catalog",
        "practice": "Practice",
        "contributing": "Contribution Guide",
        "license": "Licensing and Attribution",
        "postscript": "Editorial Notes",
    },
}

GUIDES: tuple[tuple[str, str, str], ...] = (
    ("index.md", "指南总览", "Guide Index"),
    ("safety.md", "实验安全", "Laboratory Safety"),
    ("version-control.md", "版本控制与工程协作", "Version Control and Collaboration"),
    ("python-jupyter.md", "Python、Jupyter 与工程计算", "Python and Jupyter"),
    ("c-cmake.md", "C、构建系统与硬件邻近编程", "C and Build Systems"),
    ("numerical-computing.md", "数值计算与模型验证", "Numerical Computing"),
    ("spice-simulation.md", "SPICE 电路仿真", "SPICE Circuit Simulation"),
    ("pcb-kicad.md", "PCB 与 KiCad 工作流", "PCB and KiCad"),
    ("hdl-fpga.md", "HDL、仿真与 FPGA", "HDL and FPGA"),
    ("embedded-toolchains.md", "嵌入式工具链与板级调试", "Embedded Toolchains"),
    (
        "instrumentation-measurement.md",
        "仪器、测量与不确定度",
        "Instrumentation and Measurement",
    ),
    ("data-lab-notebooks.md", "数据与实验记录", "Data and Laboratory Records"),
    ("literature-research.md", "文献检索与证据评估", "Literature Research"),
    ("technical-writing.md", "技术写作与设计评审", "Technical Writing"),
    ("reproducibility.md", "可复现工程与自动验证", "Reproducible Engineering"),
    ("projects.md", "项目实践", "Project Practice"),
)


def _as_mapping(value: Any, source: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise QualityError(f"{source} must contain a JSON object")
    return value


def _as_list(value: Any, source: str) -> list[Any]:
    if not isinstance(value, list):
        raise QualityError(f"{source} must contain an array")
    return value


def _guide_course_ids(value: Any | None) -> set[int] | None:
    if value is None:
        return None
    data = _as_mapping(value, "course guide data")
    guides = _as_list(data.get("guides"), "course guide data.guides")
    course_ids: set[int] = set()
    for index, raw_guide in enumerate(guides):
        guide = _as_mapping(raw_guide, f"course guide data.guides[{index}]")
        course_id = guide.get("course_id")
        if (
            not isinstance(course_id, int)
            or isinstance(course_id, bool)
            or course_id < 1
        ):
            raise QualityError(
                f"course guide data.guides[{index}].course_id must be a positive integer"
            )
        if course_id in course_ids:
            raise QualityError(f"duplicate course guide id: {course_id}")
        course_ids.add(course_id)
    return course_ids


def _localized(
    value: Mapping[str, Any],
    language: str,
    *,
    nested_key: str | None = None,
    flat_key: str | None = None,
    source: str,
) -> str:
    candidate: Any = None
    if nested_key is not None:
        nested = value.get(nested_key)
        if isinstance(nested, Mapping):
            candidate = nested.get(language)
    if candidate is None and flat_key is not None:
        candidate = value.get(f"{flat_key}_{language}")
    if not isinstance(candidate, str) or not candidate.strip():
        raise QualityError(f"{source} is missing a non-empty {language} title")
    return candidate.strip()


def _entry(label: str, value: Any) -> dict[str, Any]:
    return {label: value}


def _prefixed(prefix: str, path: str) -> str:
    return f"{prefix}{path}"


def _integer_order(value: Any, fallback: int) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    return fallback


def _front_matter_title(path: Path) -> str | None:
    try:
        metadata, body = split_front_matter(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, QualityError):
        return None
    title = metadata.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    match = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def _guide_specs(docs_root: Path | None) -> list[tuple[str, str, str]]:
    ordered = list(GUIDES)
    known = {path for path, _, _ in ordered}
    if docs_root is None:
        return ordered

    zh_root = docs_root / "guides"
    en_root = docs_root / "en" / "guides"
    discovered: set[str] = set()
    for root in (zh_root, en_root):
        if root.is_dir():
            discovered.update(
                path.relative_to(root).as_posix()
                for path in root.rglob("*.md")
            )
    for relative in sorted(discovered - known - {"tools.md"}):
        fallback = Path(relative).stem.replace("-", " ").title()
        zh_title = _front_matter_title(zh_root / relative) or fallback
        en_title = _front_matter_title(en_root / relative) or fallback
        ordered.append((relative, zh_title, en_title))
    return ordered


def generate_navigation(
    courses_value: Any,
    tracks_value: Any,
    routes_value: Any,
    *,
    course_guides_value: Any | None = None,
    docs_root: Path | None = None,
) -> list[dict[str, Any]]:
    """Build the compact bilingual MkDocs navigation tree.

    Track groups follow their declaration order and tracks follow their
    explicit ``order`` values in ``tracks.json``. Course detail pages are not
    listed directly: every track title links to its generated index, which in
    turn links to all course pages. MkDocs still builds and indexes those
    detail pages for search and direct navigation.
    """

    courses_data = _as_mapping(courses_value, "courses data")
    tracks_data = _as_mapping(tracks_value, "tracks data")
    routes_data = _as_mapping(routes_value, "routes data")

    groups = _as_list(tracks_data.get("groups"), "tracks.groups")
    tracks = _as_list(tracks_data.get("tracks"), "tracks.tracks")
    courses = _as_list(courses_data.get("courses"), "courses.courses")
    routes = _as_list(routes_data.get("routes"), "routes.routes")
    guide_course_ids = _guide_course_ids(course_guides_value)

    group_ids: set[str] = set()
    for index, raw_group in enumerate(groups):
        group = _as_mapping(raw_group, f"tracks.groups[{index}]")
        group_id = group.get("id")
        if not isinstance(group_id, str) or not group_id:
            raise QualityError(f"tracks.groups[{index}].id must be non-empty")
        if group_id in group_ids:
            raise QualityError(f"duplicate track group id: {group_id}")
        group_ids.add(group_id)

    tracks_by_group: dict[str, list[Mapping[str, Any]]] = {
        group_id: [] for group_id in group_ids
    }
    tracks_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw_track in enumerate(tracks):
        track = _as_mapping(raw_track, f"tracks.tracks[{index}]")
        track_id = track.get("id")
        group_id = track.get("group")
        if not isinstance(track_id, str) or not track_id:
            raise QualityError(f"tracks.tracks[{index}].id must be non-empty")
        if track_id in tracks_by_id:
            raise QualityError(f"duplicate track id: {track_id}")
        if not isinstance(group_id, str) or group_id not in tracks_by_group:
            raise QualityError(
                f"track {track_id} references unknown group {group_id!r}"
            )
        tracks_by_id[track_id] = track
        tracks_by_group[group_id].append(track)

    course_paths: set[tuple[str, str]] = set()
    catalogue_course_ids: set[int] = set()
    for index, raw_course in enumerate(courses):
        course = _as_mapping(raw_course, f"courses.courses[{index}]")
        track_id = course.get("track")
        slug = course.get("slug")
        source_id = course.get("source_id")
        if not isinstance(track_id, str) or track_id not in tracks_by_id:
            raise QualityError(
                f"course at index {index} references unknown track {track_id!r}"
            )
        if not isinstance(slug, str) or not slug:
            raise QualityError(f"courses.courses[{index}].slug must be non-empty")
        if (
            not isinstance(source_id, int)
            or isinstance(source_id, bool)
            or source_id < 1
        ):
            raise QualityError(
                f"courses.courses[{index}].source_id must be a positive integer"
            )
        if source_id in catalogue_course_ids:
            raise QualityError(f"duplicate course source id: {source_id}")
        catalogue_course_ids.add(source_id)
        key = (track_id, slug)
        if key in course_paths:
            raise QualityError(f"duplicate course path: {track_id}/{slug}.md")
        course_paths.add(key)
    if guide_course_ids is not None:
        missing_guide_ids = sorted(guide_course_ids - catalogue_course_ids)
        if missing_guide_ids:
            raise QualityError(
                "course guide ids are missing from the catalogue: "
                + ", ".join(str(course_id) for course_id in missing_guide_ids)
            )

    route_ids: set[str] = set()
    normalized_routes: list[Mapping[str, Any]] = []
    for index, raw_route in enumerate(routes):
        route = _as_mapping(raw_route, f"routes.routes[{index}]")
        route_id = route.get("id")
        if not isinstance(route_id, str) or not route_id:
            raise QualityError(f"routes.routes[{index}].id must be non-empty")
        if route_id in route_ids:
            raise QualityError(f"duplicate route id: {route_id}")
        route_ids.add(route_id)
        normalized_routes.append(route)

    guide_specs = _guide_specs(docs_root)
    output: list[dict[str, Any]] = []
    for language, (language_title, prefix) in LANGUAGE_ROOTS.items():
        labels = PAGE_LABELS[language]

        route_items: list[dict[str, Any]] = [
            _entry(labels["roadmap"], _prefixed(prefix, "roadmap.md")),
            _entry(labels["routes"], _prefixed(prefix, "routes/index.md")),
        ]
        for index, route in enumerate(normalized_routes):
            route_title = _localized(
                route,
                language,
                flat_key="title",
                source=f"routes.routes[{index}]",
            )
            route_items.append(
                _entry(
                    route_title,
                    _prefixed(prefix, f"routes/{route['id']}.md"),
                )
            )

        course_group_items: list[dict[str, Any]] = []
        for group_index, raw_group in enumerate(groups):
            group = _as_mapping(raw_group, f"tracks.groups[{group_index}]")
            group_id = str(group["id"])
            group_title = _localized(
                group,
                language,
                flat_key="title",
                source=f"track group {group_id}",
            )
            sorted_tracks = sorted(
                tracks_by_group[group_id],
                key=lambda track: (
                    _integer_order(track.get("order"), 1_000_000),
                    str(track.get("id", "")),
                ),
            )
            track_items: list[dict[str, Any]] = []
            for track in sorted_tracks:
                track_id = str(track["id"])
                track_title = _localized(
                    track,
                    language,
                    flat_key="title",
                    source=f"track {track_id}",
                )
                track_items.append(
                    _entry(
                        track_title,
                        _prefixed(prefix, f"courses/{track_id}/index.md"),
                    )
                )
            if track_items:
                course_group_items.append(_entry(group_title, track_items))

        guide_items: list[dict[str, Any]] = []
        for relative, title_zh, title_en in guide_specs:
            title = title_zh if language == "zh" else title_en
            guide_items.append(
                _entry(title, _prefixed(prefix, f"guides/{relative}"))
            )

        start_items = [
            _entry(labels["home"], _prefixed(prefix, "index.md")),
            _entry(
                labels["getting_started"],
                _prefixed(prefix, "getting-started.md"),
            ),
        ]
        route_items.extend(
            [
                _entry(
                    labels["math_foundations"],
                    _prefixed(prefix, "math-foundations.md"),
                ),
                _entry(
                    labels["math_advanced"],
                    _prefixed(prefix, "math-advanced.md"),
                ),
            ]
        )
        course_direction_items = [
            _entry(
                labels["course_index"],
                _prefixed(prefix, "courses/index.md"),
            ),
            *course_group_items,
        ]
        practice_items = [
            _entry(labels["tools"], _prefixed(prefix, "guides/tools.md")),
            *guide_items,
        ]
        resource_items = [
            _entry(labels["books"], _prefixed(prefix, "books.md")),
            _entry(
                labels["contributing"],
                _prefixed(prefix, "contributing.md"),
            ),
            _entry(
                labels["license"],
                _prefixed(prefix, "about/license.md"),
            ),
            _entry(labels["postscript"], _prefixed(prefix, "postscript.md")),
        ]
        language_items = [
            _entry(labels["start_learning"], start_items),
            _entry(labels["learning_routes"], route_items),
            _entry(labels["course_directions"], course_direction_items),
            _entry(labels["practice"], practice_items),
            _entry(labels["resources_community"], resource_items),
        ]
        output.append(_entry(language_title, language_items))
    return output


def _yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _render_items(items: Sequence[Any], indent: int) -> list[str]:
    lines: list[str] = []
    prefix = " " * indent
    for item in items:
        if isinstance(item, str):
            lines.append(f"{prefix}- {_yaml_scalar(item)}")
            continue
        if not isinstance(item, Mapping) or len(item) != 1:
            raise QualityError("navigation items must be strings or single-key mappings")
        label, value = next(iter(item.items()))
        if not isinstance(label, str):
            raise QualityError("navigation labels must be strings")
        if isinstance(value, str):
            lines.append(
                f"{prefix}- {_yaml_scalar(label)}: {_yaml_scalar(value)}"
            )
        elif isinstance(value, list):
            lines.append(f"{prefix}- {_yaml_scalar(label)}:")
            lines.extend(_render_items(value, indent + 4))
        else:
            raise QualityError(
                f"navigation value for {label!r} must be a string or list"
            )
    return lines


def render_navigation(navigation: Sequence[Any]) -> str:
    return "\n".join(["nav:", *_render_items(navigation, 2)]) + "\n"


def _marker_matches(config_text: str, marker: str) -> list[re.Match[str]]:
    return list(
        re.finditer(
            rf"(?m)^{re.escape(marker)}[ \t]*\r?$",
            config_text,
        )
    )


def generated_navigation_body(config_text: str) -> str:
    starts = _marker_matches(config_text, BEGIN_MARKER)
    ends = _marker_matches(config_text, END_MARKER)
    if len(starts) != 1 or len(ends) != 1:
        raise QualityError(
            "mkdocs.yml must contain exactly one generated navigation marker pair"
        )
    if starts[0].end() >= ends[0].start():
        raise QualityError("generated navigation markers are out of order")
    return config_text[starts[0].end() : ends[0].start()].strip("\r\n")


def replace_generated_navigation(config_text: str, rendered_nav: str) -> str:
    starts = _marker_matches(config_text, BEGIN_MARKER)
    ends = _marker_matches(config_text, END_MARKER)
    if len(starts) != 1 or len(ends) != 1:
        raise QualityError(
            "mkdocs.yml must contain exactly one generated navigation marker pair"
        )
    start = starts[0]
    end = ends[0]
    if start.end() >= end.start():
        raise QualityError("generated navigation markers are out of order")
    return (
        config_text[: start.end()]
        + "\n"
        + rendered_nav.rstrip("\r\n")
        + "\n"
        + config_text[end.start() :]
    )


def _load_navigation(
    courses_path: Path,
    tracks_path: Path,
    routes_path: Path,
    course_guides_path: Path,
    docs_root: Path,
) -> str:
    navigation = generate_navigation(
        load_json(courses_path),
        load_json(tracks_path),
        load_json(routes_path),
        course_guides_value=load_json(course_guides_path),
        docs_root=docs_root,
    )
    return render_navigation(navigation)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate and synchronize the complete bilingual MkDocs navigation."
    )
    parser.add_argument("--config", default="mkdocs.yml")
    parser.add_argument("--courses", default="data/courses.json")
    parser.add_argument("--tracks", default="data/tracks.json")
    parser.add_argument("--routes", default="data/routes.json")
    parser.add_argument("--course-guides", default="data/course_guides.json")
    parser.add_argument("--docs-dir", default="docs")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config_path = repo_path(args.config)
    try:
        rendered = _load_navigation(
            repo_path(args.courses),
            repo_path(args.tracks),
            repo_path(args.routes),
            repo_path(args.course_guides),
            repo_path(args.docs_dir),
        )
        config_text = config_path.read_text(encoding="utf-8")
        updated = replace_generated_navigation(config_text, rendered)
    except (OSError, UnicodeDecodeError, QualityError) as exc:
        print(f"ERROR navigation.sync: {exc}", file=sys.stderr)
        return 1

    if args.write:
        if updated != config_text:
            atomic_write(config_path, updated)
            print(f"Updated generated navigation in {config_path.as_posix()}")
        else:
            print(f"Generated navigation is already current in {config_path.as_posix()}")
        return 0

    try:
        current = generated_navigation_body(config_text)
    except QualityError as exc:
        print(f"ERROR navigation.sync: {exc}", file=sys.stderr)
        return 1
    expected = rendered.rstrip("\r\n")
    if current != expected:
        print(
            "ERROR navigation.sync: generated navigation is stale; "
            "run scripts/sync_navigation.py --write",
            file=sys.stderr,
        )
        return 1
    print("Generated navigation is current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
