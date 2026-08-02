from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from scripts.check_navigation import nav_targets
from scripts.quality_common import QualityError, load_json
from scripts.sync_navigation import (
    BEGIN_MARKER,
    END_MARKER,
    generate_navigation,
    generated_navigation_body,
    main,
    render_navigation,
    replace_generated_navigation,
)


ROOT = Path(__file__).resolve().parents[1]


def _project_navigation() -> list[dict[str, object]]:
    return generate_navigation(
        load_json(ROOT / "data" / "courses.json"),
        load_json(ROOT / "data" / "tracks.json"),
        load_json(ROOT / "data" / "routes.json"),
        course_guides_value=load_json(ROOT / "data" / "course_guides.json"),
        docs_root=ROOT / "docs",
    )


def _is_course_detail(path: str) -> bool:
    parts = path.split("/")
    if parts and parts[0] == "en":
        parts = parts[1:]
    return (
        len(parts) == 3
        and parts[0] == "courses"
        and parts[2] != "index.md"
    )


def test_generated_navigation_lists_every_non_course_page_once() -> None:
    navigation = _project_navigation()
    targets = list(nav_targets(navigation))
    counts = Counter(targets)
    existing = {
        path.relative_to(ROOT / "docs").as_posix()
        for path in (ROOT / "docs").rglob("*.md")
    }
    expected = {path for path in existing if not _is_course_detail(path)}
    assert set(targets) == expected
    assert all(count == 1 for count in counts.values())
    course_detail_paths = {path for path in existing if _is_course_detail(path)}
    assert course_detail_paths
    assert set(targets).isdisjoint(course_detail_paths)


def test_generated_navigation_has_five_compact_entry_groups() -> None:
    navigation = _project_navigation()
    zh_items = navigation[0]["中文"]
    zh_labels = [next(iter(item)) for item in zh_items]
    assert zh_labels == [
        "开始学习",
        "路线",
        "课程方向",
        "实践",
        "资源与共建",
    ]

    en_items = navigation[1]["English"]
    en_labels = [next(iter(item)) for item in en_items]
    assert en_labels == [
        "Start Learning",
        "Routes",
        "Course Directions",
        "Practice",
        "Resources and Community",
    ]


def test_course_directions_follow_group_and_track_order_without_course_details() -> None:
    navigation = _project_navigation()
    tracks = load_json(ROOT / "data" / "tracks.json")

    for language_root, group_label, prefix in (
        ("中文", "课程方向", ""),
        ("English", "Course Directions", "en/"),
    ):
        language_items = next(
            item[language_root] for item in navigation if language_root in item
        )
        course_tree = next(
            item[group_label] for item in language_items if group_label in item
        )
        targets = list(nav_targets(course_tree))
        expected = {
            f"{prefix}courses/index.md",
            *(
                f"{prefix}courses/{track['id']}/index.md"
                for track in tracks["tracks"]
            ),
        }
        assert set(targets) == expected
        assert len(targets) == len(expected) == len(tracks["tracks"]) + 1

    zh_items = navigation[0]["中文"]
    course_directions = next(
        item["课程方向"] for item in zh_items if "课程方向" in item
    )
    assert course_directions[0] == {"课程总览": "courses/index.md"}

    group_labels = [next(iter(item)) for item in course_directions[1:]]
    assert group_labels == [group["title_zh"] for group in tracks["groups"]]

    foundations = course_directions[1]["数理与工程基础"]
    assert foundations[:3] == [
        {"工程数学": "courses/mathematics/index.md"},
        {"概率、统计与随机过程": "courses/probability-statistics/index.md"},
        {"物理基础": "courses/physics/index.md"},
    ]
    assert all(
        isinstance(target, str) and target.endswith("/index.md")
        for group in course_directions[1:]
        for track_entry in next(iter(group.values()))
        for target in track_entry.values()
    )

    rendered = render_navigation(navigation)
    assert '"courses/mathematics/index.md"' in rendered
    assert '"courses/mathematics/001-18-01sc.md"' not in rendered


def test_marker_replacement_is_stable() -> None:
    rendered = render_navigation(
        [{"中文": [{"前言": "index.md"}]}]
    )
    original = (
        "site_name: Example\n"
        f"{BEGIN_MARKER}\n"
        "nav:\n"
        "  - stale: stale.md\n"
        f"{END_MARKER}\n"
        "strict: true\n"
    )
    updated = replace_generated_navigation(original, rendered)
    assert generated_navigation_body(updated) == rendered.rstrip()
    assert updated.startswith("site_name: Example\n")
    assert updated.endswith("strict: true\n")
    assert replace_generated_navigation(updated, rendered) == updated


def test_marker_replacement_requires_one_ordered_pair() -> None:
    with pytest.raises(QualityError):
        replace_generated_navigation("nav: []\n", "nav: []\n")
    with pytest.raises(QualityError):
        replace_generated_navigation(
            f"{END_MARKER}\n{BEGIN_MARKER}\n",
            "nav: []\n",
        )


def test_cli_check_and_write_round_trip(tmp_path: Path) -> None:
    config = tmp_path / "mkdocs.yml"
    config.write_text(
        "site_name: Example\n"
        f"{BEGIN_MARKER}\n"
        "nav:\n"
        "  - stale: stale.md\n"
        f"{END_MARKER}\n",
        encoding="utf-8",
    )
    common = [
        "--config",
        str(config),
        "--courses",
        str(ROOT / "data" / "courses.json"),
        "--tracks",
        str(ROOT / "data" / "tracks.json"),
        "--routes",
        str(ROOT / "data" / "routes.json"),
        "--course-guides",
        str(ROOT / "data" / "course_guides.json"),
        "--docs-dir",
        str(ROOT / "docs"),
    ]
    stale = config.read_bytes()
    assert main([*common, "--check"]) == 1
    assert config.read_bytes() == stale
    assert main([*common, "--write"]) == 0
    first_write = config.read_bytes()
    assert main([*common, "--write"]) == 0
    assert config.read_bytes() == first_write
    assert main([*common, "--check"]) == 0
