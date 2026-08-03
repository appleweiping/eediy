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
NEW_PAGES = {
    "books.md",
    "math-foundations.md",
    "math-advanced.md",
    "postscript.md",
    "en/books.md",
    "en/math-foundations.md",
    "en/math-advanced.md",
    "en/postscript.md",
}


def _project_navigation() -> list[dict[str, object]]:
    return generate_navigation(
        load_json(ROOT / "data" / "courses.json"),
        load_json(ROOT / "data" / "tracks.json"),
        load_json(ROOT / "data" / "routes.json"),
        docs_root=ROOT / "docs",
    )


def test_generated_navigation_lists_every_page_exactly_once() -> None:
    navigation = _project_navigation()
    targets = list(nav_targets(navigation))
    counts = Counter(targets)
    existing = {
        path.relative_to(ROOT / "docs").as_posix()
        for path in (ROOT / "docs").rglob("*.md")
    }
    assert set(targets) == existing | NEW_PAGES
    assert all(count == 1 for count in counts.values())


def test_generated_navigation_follows_group_track_and_course_order() -> None:
    navigation = _project_navigation()
    zh_items = navigation[0]["中文"]
    zh_labels = [next(iter(item)) for item in zh_items]
    assert "课程导航" not in zh_labels
    assert "数理与工程基础" not in zh_labels
    assert "电子工程核心" not in zh_labels
    assert "数字、系统与智能硬件" not in zh_labels

    catalog = zh_labels.index("课程总览")
    mathematics = zh_labels.index("工程数学")
    probability = zh_labels.index("概率、统计与随机过程")
    physics = zh_labels.index("物理基础")
    circuits = zh_labels.index("电路分析")
    computer_architecture = zh_labels.index("计算机体系结构")
    assert (
        catalog
        < mathematics
        < probability
        < physics
        < circuits
        < computer_architecture
    )
    assert probability == mathematics + 1

    en_items = navigation[1]["English"]
    en_labels = [next(iter(item)) for item in en_items]
    assert "Course Catalog" in en_labels
    assert "Mathematical and Engineering Foundations" not in en_labels

    rendered = render_navigation(navigation)
    mathematics = rendered.index('"工程数学"')
    probability = rendered.index('"概率、统计与随机过程"', mathematics)
    physics = rendered.index('"物理基础"', probability)
    assert mathematics < probability < physics

    first_math = rendered.index(
        '"courses/mathematics/001-18-01sc.md"',
        mathematics,
    )
    second_math = rendered.index(
        '"courses/mathematics/002-18-02sc.md"',
        first_math,
    )
    assert first_math < second_math


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
        "--docs-dir",
        str(ROOT / "docs"),
    ]
    assert main([*common, "--check"]) == 1
    assert main([*common, "--write"]) == 0
    assert main([*common, "--check"]) == 0
