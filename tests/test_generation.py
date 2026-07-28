from __future__ import annotations

import json
from pathlib import Path

from scripts.check_markdown_links import markdown_link_issues
from scripts.generate_course_pages import (
    GENERATED_MARKER,
    build_expected_pages,
    generated_page_issues,
    mainline_audit_annotations,
    render_nav_fragment,
    render_route_page,
    write_pages,
)
from scripts.quality_common import markdown_headings


def test_generator_builds_complete_bilingual_graph(
    tmp_path: Path, catalogue: dict, routes_data: dict
) -> None:
    docs_root = tmp_path / "docs"
    expected = build_expected_pages(catalogue, routes_data, docs_root)
    assert len(expected) == 10
    assert docs_root / "courses" / "index.md" in expected
    assert docs_root / "en" / "courses" / "index.md" in expected
    assert docs_root / "routes" / "starter.md" in expected
    assert docs_root / "en" / "routes" / "starter.md" in expected
    assert all(GENERATED_MARKER in content for content in expected.values())
    assert write_pages(expected, docs_root) == []
    assert generated_page_issues(expected, docs_root) == []
    link_issues, statistics = markdown_link_issues(docs_root)
    assert link_issues == []
    assert statistics["links_internal"] > 0


def test_reviewing_mainline_is_visible_on_track_and_course_pages(
    tmp_path: Path, catalogue: dict, routes_data: dict
) -> None:
    audit = {
        "audits": [
            {
                "course_id": 1,
                "status": "review",
                "limitation_zh": "公开反馈仍需复核。",
                "limitation_en": "Public feedback still needs review.",
                "verified_at": "2026-07-29",
            }
        ]
    }

    expected = build_expected_pages(
        catalogue,
        routes_data,
        tmp_path / "docs",
        mainline_audit=audit,
    )
    zh_track = expected[tmp_path / "docs" / "courses" / "mathematics" / "index.md"]
    en_course = expected[
        tmp_path
        / "docs"
        / "en"
        / "courses"
        / "mathematics"
        / "001-ee-101.md"
    ]

    assert "主线审计复核中" in zh_track
    assert "公开反馈仍需复核" in zh_track
    assert "Mainline audit review" in en_course
    assert "Public feedback still needs review" in en_course


def test_mainline_audit_annotation_requires_every_mainline(catalogue: dict) -> None:
    annotations, issues = mainline_audit_annotations({"audits": []}, catalogue)

    assert annotations == {}
    assert any(issue.code == "generated.mainline_audit_missing" for issue in issues)


def test_generated_translation_heading_structure_matches(
    tmp_path: Path, catalogue: dict, routes_data: dict
) -> None:
    expected = build_expected_pages(catalogue, routes_data, tmp_path / "docs")
    zh = expected[
        tmp_path
        / "docs"
        / "courses"
        / "mathematics"
        / "001-ee-101.md"
    ]
    en = expected[
        tmp_path
        / "docs"
        / "en"
        / "courses"
        / "mathematics"
        / "001-ee-101.md"
    ]
    assert [level for level, _, _ in markdown_headings(zh)] == [
        level for level, _, _ in markdown_headings(en)
    ]
    assert "maintainer planning estimate" in en
    assert "维护者规划估计" in zh
    en_route = expected[tmp_path / "docs" / "en" / "routes" / "starter.md"]
    assert "**Stage exit criterion:**" in en_route
    assert "criterion：**" not in en_route
    assert "**Required**" in en_route
    assert "**Selection rule:** Complete all 1 required course." in en_route
    assert "1. Foundation" not in en_route


def test_check_detects_drift_without_overwriting(
    tmp_path: Path, catalogue: dict, routes_data: dict
) -> None:
    docs_root = tmp_path / "docs"
    expected = build_expected_pages(catalogue, routes_data, docs_root)
    write_pages(expected, docs_root)
    target = docs_root / "courses" / "index.md"
    target.write_text(target.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
    issues = generated_page_issues(expected, docs_root)
    assert any(issue.code == "generated.drift" for issue in issues)


def test_check_detects_unexpected_file_in_managed_directory(
    tmp_path: Path, catalogue: dict, routes_data: dict
) -> None:
    docs_root = tmp_path / "docs"
    expected = build_expected_pages(catalogue, routes_data, docs_root)
    write_pages(expected, docs_root)
    unexpected = docs_root / "en" / "courses" / "mathematics" / "tmp-orphan"
    unexpected.write_text("orphaned atomic-write file", encoding="utf-8")

    issues = generated_page_issues(expected, docs_root)

    assert any(
        issue.code == "generated.unexpected_file"
        and issue.path == unexpected.as_posix()
        for issue in issues
    )


def test_writer_protects_hand_authored_collision(
    tmp_path: Path, catalogue: dict, routes_data: dict
) -> None:
    docs_root = tmp_path / "docs"
    expected = build_expected_pages(catalogue, routes_data, docs_root)
    target = docs_root / "courses" / "index.md"
    target.parent.mkdir(parents=True)
    target.write_text("# Hand-authored\n", encoding="utf-8")
    issues = write_pages(expected, docs_root)
    assert any(issue.code == "generated.protected_collision" for issue in issues)
    assert target.read_text(encoding="utf-8") == "# Hand-authored\n"


def test_nav_fragment_lists_only_track_indexes(catalogue: dict, routes_data: dict) -> None:
    fragment = render_nav_fragment(catalogue, routes_data)
    assert "courses/mathematics/index.md" in fragment
    assert "001-ee-101.md" not in fragment


def test_control_robotics_renders_complete_paths_in_order() -> None:
    root = Path(__file__).resolve().parents[1]
    catalogue = json.loads((root / "data" / "courses.json").read_text(encoding="utf-8"))
    routes = json.loads((root / "data" / "routes.json").read_text(encoding="utf-8"))["routes"]
    route = next(item for item in routes if item["id"] == "control-robotics")
    courses_by_source = {course["source_id"]: course for course in catalogue["courses"]}

    en = render_route_page(route, courses_by_source, "en")
    zh = render_route_page(route, courses_by_source, "zh")

    assert (
        "**Selection rule:** choose 1 of the 2 complete paths below and finish every "
        "course in the selected path in the listed order."
    ) in en
    assert "**Complete path option — MIT Robotics path (complete in the listed order)**" in en
    assert (
        "**Complete path option — Complete Modern Robotics path (Courses 1–6 in order; "
        "full platform access may be paid) "
        "(complete in the listed order)**"
    ) in en
    modern_titles = [
        courses_by_source[source_id]["title"]["en"]
        for source_id in (77, 78, 79, 80, 81, 82)
    ]
    assert [en.index(f"{index}. [{title}]") for index, title in enumerate(modern_titles, 1)] == sorted(
        en.index(f"{index}. [{title}]") for index, title in enumerate(modern_titles, 1)
    )
    course_six_line = next(
        line for line in en.splitlines() if f"6. [{modern_titles[-1]}]" in line
    )
    assert "**Course in selected path**" in course_six_line
    assert "**Elective option**" not in course_six_line
    assert "从以下 2 条完整路径中选择 1 条，并按列出顺序完成所选路径的全部课程。" in zh
    assert (
        "**完整路径选项 — Modern Robotics 完整路径（课程 1–6 按序；"
        "平台完整访问可能收费）（按序完成）**"
    ) in zh


def test_exact_course_prerequisites_render_as_links() -> None:
    root = Path(__file__).resolve().parents[1]
    catalogue = json.loads((root / "data" / "courses.json").read_text(encoding="utf-8"))
    routes = json.loads((root / "data" / "routes.json").read_text(encoding="utf-8"))
    courses_by_source = {course["source_id"]: course for course in catalogue["courses"]}
    course = courses_by_source[82]
    track = next(track for track in catalogue["tracks"] if track["id"] == course["track"])

    rendered = build_expected_pages(
        catalogue,
        routes,
        root / "build" / "test-prerequisite-pages",
    )[
        root
        / "build"
        / "test-prerequisite-pages"
        / "en"
        / "courses"
        / course["track"]
        / f"{course['slug']}.md"
    ]

    for prerequisite_id in course["prerequisite_course_ids"]:
        prerequisite = courses_by_source[prerequisite_id]
        assert (
            f"[{prerequisite['title']['en']}]"
            f"(../{prerequisite['track']}/{prerequisite['slug']}.md)"
        ) in rendered


def test_review_courses_render_as_optional_not_counted_electives() -> None:
    root = Path(__file__).resolve().parents[1]
    catalogue = json.loads((root / "data" / "courses.json").read_text(encoding="utf-8"))
    routes = json.loads((root / "data" / "routes.json").read_text(encoding="utf-8"))["routes"]
    audit_data = json.loads(
        (root / "data" / "mainline_audit.json").read_text(encoding="utf-8")
    )
    audits_by_course, issues = mainline_audit_annotations(audit_data, catalogue)
    assert issues == []
    courses_by_source = {course["source_id"]: course for course in catalogue["courses"]}
    route_map = {route["id"]: route for route in routes}
    cases = (
        ("analog-ic", 36),
        ("control-robotics", 73),
        ("rf-wireless", 112),
        ("photonics-mems", 133),
    )
    for route_id, course_id in cases:
        rendered = render_route_page(
            route_map[route_id],
            courses_by_source,
            "en",
            audits_by_course,
        )
        title = courses_by_source[course_id]["title"]["en"]
        course_line = next(
            line
            for line in rendered.splitlines()
            if f"[{title}]" in line and "**Optional supplement**" in line
        )
        assert "**Optional supplement**" in course_line
        assert "**Elective option**" not in course_line
        assert "**Audit review**" in course_line
        assert audits_by_course[course_id]["limitation_en"] in rendered
