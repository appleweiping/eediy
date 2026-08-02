from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from scripts.check_markdown_links import markdown_link_issues
from scripts.course_data import normalize_url
from scripts.course_guides import load_course_guides
from scripts.generate_course_pages import (
    GENERATED_MARKER,
    _course_metadata,
    _curated_resources,
    _eediy_example_links,
    _human_resource_title,
    _is_low_signal_compact_resource,
    _nest_first_guide_section_under_overview,
    _resource_access_summary,
    _resource_label,
    _render_resource_index,
    _render_selected_resources,
    build_expected_pages,
    generated_page_issues,
    mainline_audit_annotations,
    render_course_page,
    render_nav_fragment,
    render_route_index,
    render_route_page,
    render_track_page,
    write_pages,
)
from scripts.quality_common import markdown_headings


def test_all_authored_course_sections_nest_under_course_overview() -> None:
    body = (
        "## Direct course judgment\n\n"
        "Choose this course for its project.\n\n"
        "## Distinctive work\n\n"
        "Build the project.\n\n"
        "### One difficult checkpoint\n\n"
        "Explain the failure."
    )

    nested = _nest_first_guide_section_under_overview(body)

    assert nested.startswith("### Direct course judgment")
    assert "Choose this course for its project." in nested
    assert "### Distinctive work" in nested
    assert "#### One difficult checkpoint" in nested
    assert "\n## " not in nested


def test_course_subpage_resource_label_localizes_only_the_generic_title() -> None:
    resource = {
        "kind": "course",
        "title": {"zh": "Syllabus", "en": "Syllabus"},
    }

    assert _resource_label(resource, "zh") == "课程大纲"
    assert _resource_label(resource, "en") == "Syllabus"


def test_machine_disambiguators_are_replaced_with_human_resource_titles() -> None:
    exam = {
        "kind": "exams",
        "title": {
            "zh": "Exam — ocw.mit.edu/exam — resource b9c9033a",
            "en": "Exam — ocw.mit.edu/exam — resource b9c9033a",
        },
        "url": (
            "https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-"
            "fall-2010/pages/3.-double-integrals/exam-3/exam"
        ),
    }
    syllabus = {
        "kind": "course",
        "title": {
            "zh": "Syllabus — ocw.mit.edu/syllabus",
            "en": "Syllabus — ocw.mit.edu/syllabus",
        },
        "url": (
            "https://ocw.mit.edu/courses/6-004-computation-structures-"
            "spring-2017/pages/syllabus"
        ),
    }

    assert _human_resource_title(exam, "zh") == "考试 3"
    assert _human_resource_title(exam, "en") == "Exam 3"
    assert _human_resource_title(syllabus, "zh") == "2017 春季课程大纲"
    assert _human_resource_title(syllabus, "en") == "Spring 2017 syllabus"


def test_generic_resource_titles_are_localized_without_translating_topics() -> None:
    cases = (
        (
            "Homework 2: Visualizing Data (PDF)",
            "作业 2：Visualizing Data（PDF）",
        ),
        ("Assignment resource: botclient (PDF)", "作业资源：botclient（PDF）"),
        (
            "Lab 2 — Cadence introduction and device characterization",
            "实验 2：Cadence introduction and device characterization",
        ),
        (
            "Lecture 36: Alan Edelman and Julia Language",
            "第 36 讲：Alan Edelman and Julia Language",
        ),
        ("Exam 1 Formula Sheet (PDF)", "考试 1 公式表（PDF）"),
        ("Midterm 2016", "2016 年期中考试"),
        (
            "Final Exam (Fall 2015) Solutions",
            "期末考试（2015 秋季）解答",
        ),
        ("Problem Set 3 Solutions (PDF)", "习题 3 解答（PDF）"),
        ("Syllabus", "课程大纲"),
        ("Lecture video transcript (PDF)", "课程视频文字稿（PDF）"),
        ("Course Notes", "课程讲义"),
        ("Resource Index", "资源索引"),
    )

    for title, expected_zh in cases:
        resource = {
            "kind": "other",
            "title": {"zh": title, "en": title},
            "url": "https://example.edu/material",
        }
        snapshot = json.dumps(resource, sort_keys=True)

        assert _human_resource_title(resource, "zh") == expected_zh
        assert _human_resource_title(resource, "en") == title
        assert json.dumps(resource, sort_keys=True) == snapshot


def test_formal_titles_and_course_codes_bypass_generic_localization() -> None:
    titles = (
        "Ideal Solution Model, Linear Sweep Voltammetry (PDF)",
        "Least squares and least norm solutions using Matlab",
        "Approximate Dynamic Programming, Lecture 1, Part 1",
        "The Feynman Lectures on Physics",
        "CS 61C Fall 2024 lab starter repository",
    )

    for title in titles:
        resource = {
            "kind": "other",
            "title": {"zh": title, "en": title},
            "url": "https://example.edu/formal-title",
        }

        assert _human_resource_title(resource, "zh") == title
        assert _human_resource_title(resource, "en") == title


def test_full_course_render_preserves_resource_urls_and_bilingual_row_counts() -> None:
    root = Path(__file__).resolve().parents[1]
    catalogue = json.loads(
        (root / "data" / "courses.json").read_text(encoding="utf-8")
    )
    guides, issues = load_course_guides(
        root / "data" / "course_guides.json",
        catalogue,
    )
    assert issues == []
    courses_by_source = {
        int(course["source_id"]): course for course in catalogue["courses"]
    }
    tracks_by_id = {track["id"]: track for track in catalogue["tracks"]}
    link_line_re = re.compile(
        r"^(?:- |\| )\[([^\]]+)\]\((https://[^)]+)\)(?:\s+\||\s*$)",
        flags=re.MULTILINE,
    )
    machine_label_re = re.compile(
        r"(?:[a-z0-9.-]+\.[a-z]{2,}/\S+|resource\s+[0-9a-f]{8})",
        flags=re.IGNORECASE,
    )
    totals = {"zh": 0, "en": 0}
    provider_totals = {"zh": 0, "en": 0}

    for course_id, course in courses_by_source.items():
        links_by_language: dict[str, list[tuple[str, str]]] = {}
        for language, heading in (
            ("zh", "课程资源"),
            ("en", "Course Resources"),
        ):
            rendered = render_course_page(
                course,
                tracks_by_id[str(course["track"])],
                language,
                courses_by_source,
                guide=guides[course_id],
            )
            parts = re.split(
                rf"^## {re.escape(heading)}\r?$",
                rendered,
                maxsplit=1,
                flags=re.MULTILINE,
            )
            assert len(parts) == 2, (course_id, language)
            links = link_line_re.findall(parts[1])
            links_by_language[language] = links
            totals[language] += len(links)
            assert not [
                label for label, _url in links if machine_label_re.search(label)
            ], (course_id, language)

            provider_urls = {
                normalize_url(str(resource["url"]))
                for resource in course["resources"]
            }
            rendered_provider_urls = sorted(
                normalize_url(url)
                for _label, url in links
                if normalize_url(url) in provider_urls
            )
            expected_provider_urls = (
                []
                if guides[course_id].get(
                    "resource_index_mode",
                    "structured",
                )
                == "inline-only"
                else sorted(
                    normalize_url(str(resource["url"]))
                    for resource in course["resources"]
                    if not _is_low_signal_compact_resource(resource)
                )
            )
            assert rendered_provider_urls == expected_provider_urls, (
                course_id,
                language,
            )
            provider_totals[language] += len(rendered_provider_urls)

        assert len(links_by_language["zh"]) == len(
            links_by_language["en"]
        ), course_id
        assert Counter(
            normalize_url(url) for _label, url in links_by_language["zh"]
        ) == Counter(
            normalize_url(url) for _label, url in links_by_language["en"]
        ), course_id

    assert totals == {"zh": 1530, "en": 1530}
    assert provider_totals == {"zh": 1525, "en": 1525}


def test_generic_resource_label_collapses_only_for_its_own_kind() -> None:
    resource = {
        "kind": "assignments",
        "title": {"zh": "作业", "en": "Assignments"},
    }

    assert _resource_label(resource, "zh") == "作业"
    assert _resource_label(resource, "en") == "Assignments"

    numbered = {
        "kind": "assignments",
        "title": {"zh": "Homework 3", "en": "Homework 3"},
        "url": "https://example.edu/homework-3",
    }
    assert _resource_label(numbered, "zh") == "作业 3"
    assert _resource_label(numbered, "en") == "Assignments · Homework 3"


def test_course_resource_index_repeats_core_links_cited_in_the_guide() -> None:
    course = {
        "resources": [
            {
                "id": "primary",
                "kind": "course",
                "title": {"zh": "课程主页", "en": "Course home"},
                "url": "https://example.edu/ee101/",
                "access": "open",
                "status": "available",
                "last_verified": "2026-07-30",
            }
        ]
    }

    rendered = _render_selected_resources(
        course,
        "en",
        narrative_urls={"https://example.edu/ee101/"},
    )

    assert "[Course home](https://example.edu/ee101/)" in rendered
    assert "linked in the guide above" not in rendered


def test_eediy_executable_example_is_repeated_in_resource_summary() -> None:
    body = (
        "Run the [verified FIFO starter]"
        "(https://github.com/appleweiping/eediy/tree/main/examples/sync-fifo). "
        "The [course site](https://example.edu/course) remains the official source."
    )
    examples = _eediy_example_links(body)

    rendered = _render_selected_resources(
        {
            "resources": [
                {
                    "id": "primary",
                    "kind": "course",
                    "title": {"zh": "课程主页", "en": "Course home"},
                    "url": "https://example.edu/course",
                    "access": "open",
                    "status": "available",
                    "last_verified": "2026-07-31",
                }
            ]
        },
        "en",
        narrative_urls={"https://example.edu/course"},
        eediy_examples=examples,
    )

    assert examples == [
        (
            "verified FIFO starter",
            "https://github.com/appleweiping/eediy/tree/main/examples/sync-fifo",
        )
    ]
    summary = rendered.split("## Resource Summary\n\n", 1)[1]
    assert "[verified FIFO starter]" in summary
    assert "Every public entry point verified" not in summary


def test_compact_course_metadata_does_not_repeat_link_only_sequence_entries() -> None:
    course = {
        "institution": "Example University",
        "course_code": "EE-201",
        "prerequisite_course_ids": [1],
        "official_prerequisites": {
            "zh": [
                "正式要求 EE-101",
                "先完成《EE-101》",
            ],
            "en": [
                "EE-101 is required",
                "Complete EE-101 first",
            ],
        },
        "recommended_background": {"zh": [], "en": []},
        "prerequisites": {"zh": [], "en": []},
        "resources": [
            {
                "access": "open",
                "status": "available",
            }
        ],
    }

    rendered = _course_metadata(
        course,
        "en",
        reviewed_at="2026-07-31",
        editorial_status="researched",
    )

    assert "Official prerequisites:** EE-101 is required" in rendered
    assert "Official prerequisites:** Official prerequisite" not in rendered
    assert "EEDIY preparation:** Recommended background" not in rendered
    assert "Course-sequence requirement" not in rendered


def test_course_metadata_names_the_review_relationship() -> None:
    course = {
        "institution": "Example University",
        "course_code": "EE-201",
        "prerequisites": {"zh": [], "en": []},
        "resources": [{"access": "open", "status": "available"}],
    }

    same_run = _course_metadata(
        course,
        "en",
        reviewed_at="2026-07-31",
        editorial_status="learner-reviewed",
        review_relationship="same-course-other-run",
    )
    successor = _course_metadata(
        course,
        "zh",
        reviewed_at="2026-07-31",
        editorial_status="researched",
        review_relationship="successor-course",
    )

    assert "Learner-reviewed (another run of the same course)" in same_run
    assert "后继课程复盘仅作背景" in successor


def test_course_page_frontmatter_exposes_review_relationship_to_comments() -> None:
    course = {
        "id": "course-201",
        "source_id": 201,
        "title": {"zh": "示例课程", "en": "Example Course"},
        "summary": {"zh": "课程摘要", "en": "Course summary"},
        "institution": "Example University",
        "course_code": "EE-201",
        "prerequisites": {"zh": [], "en": []},
        "resources": [
            {
                "kind": "course",
                "title": {"zh": "课程主页", "en": "Course home"},
                "url": "https://example.edu/ee-201",
                "access": "open",
                "status": "available",
            }
        ],
        "last_reviewed": "2026-07-31",
    }
    guide = {
        "editorial_status": "learner-reviewed",
        "evidence_level": "R3",
        "reviewed_at": "2026-07-31",
        "resource_index_mode": "inline-only",
        "learner_reviews": [{"relationship": "same-course-other-run"}],
        "bodies": {
            "en": (
                "## What this course covers\n\n"
                "The linked course is the version discussed on this page."
            )
        },
    }

    rendered = render_course_page(
        course,
        {"id": "example"},
        "en",
        {201: course},
        guide=guide,
    )

    assert 'editorial_status: "learner-reviewed"' in rendered
    assert 'review_relationship: "same-course-other-run"' in rendered
    assert "discussion_term:" not in rendered
    assert "another run of the same course" in rendered


def test_inline_only_guide_keeps_the_standard_heading_without_relabeling_links() -> None:
    course = {
        "id": "course-116",
        "source_id": 116,
        "title": {"zh": "变换器电路", "en": "Converter Circuits"},
        "summary": {"zh": "课程摘要", "en": "Course summary"},
        "institution": "University of Colorado Boulder",
        "course_code": "Power Electronics 2",
        "prerequisites": {"zh": [], "en": []},
        "resources": [
            {
                "id": "primary",
                "kind": "course",
                "title": {"zh": "课程主页", "en": "Course home"},
                "url": "https://www.coursera.org/learn/converter-circuits",
                "access": "open-registration",
                "status": "available",
                "last_verified": "2026-07-31",
            }
        ],
        "last_reviewed": "2026-07-31",
    }
    guide = {
        "editorial_status": "researched",
        "evidence_level": "R0",
        "reviewed_at": "2026-07-31",
        "resource_index_mode": "inline-only",
        "bodies": {
            "en": (
                "## Read the sequence literally\n\n"
                "The [preceding course](https://www.coursera.org/learn/power-electronics) "
                "is context, not a resource belonging to this course."
            )
        },
    }

    rendered = render_course_page(
        course,
        {"id": "power-electronics"},
        "en",
        {116: course},
        guide=guide,
    )

    assert "## Course Resources" in rendered
    assert "links each core resource where its version" in rendered
    assert "[preceding course](https://www.coursera.org/learn/power-electronics)" in rendered
    assert "https://www.coursera.org/learn/converter-circuits" not in rendered


def test_selected_resource_summary_never_exceeds_five_links() -> None:
    resources = [
        {
            "id": f"resource-{index}",
            "kind": "assignments",
            "title": {"zh": f"作业 {index}", "en": f"Homework {index}"},
            "url": f"https://example.edu/ee101/homework-{index}",
            "access": "open",
            "status": "available",
            "last_verified": "2026-07-31",
        }
        for index in range(1, 7)
    ]

    rendered = _render_selected_resources(
        {"resources": resources},
        "en",
        narrative_urls=[resource["url"] for resource in resources[:5]],
    )
    summary = rendered.split('<details markdown="1">', 1)[0]

    assert summary.count("](https://") == 5


def test_course_resource_section_omits_staff_pages_and_hash_only_transcripts() -> None:
    def resource(
        resource_id: str,
        kind: str,
        title: str,
        url: str,
    ) -> dict:
        return {
            "id": resource_id,
            "kind": kind,
            "title": {"zh": title, "en": title},
            "url": url,
            "access": "open",
            "status": "available",
            "last_verified": "2026-07-31",
        }

    course = {
        "resources": [
            resource("primary", "course", "Course home", "https://example.edu/course"),
            resource(
                "team",
                "course",
                "Meet the TAs",
                "https://example.edu/course/meet-the-tas",
            ),
            resource(
                "syllabus",
                "course",
                "Syllabus",
                "https://example.edu/course/syllabus",
            ),
            resource(
                "assignments",
                "assignments",
                "Assignments",
                "https://example.edu/course/assignments",
            ),
            resource(
                "exams",
                "exams",
                "Final exam",
                "https://example.edu/course/exams",
            ),
            resource(
                "transcript",
                "notes",
                "Lecture video transcript (PDF) — ocw.mit.edu/hgc1l_6yskc-1",
                "https://example.edu/course/resources/hgc1l_6yskc-1",
            ),
        ]
    }

    selected = _curated_resources(course, limit=5)

    assert {item["id"] for item in selected} == {
        "primary",
        "syllabus",
        "assignments",
        "exams",
    }
    rendered = _render_selected_resources(
        course,
        "en",
        narrative_urls={
            "https://example.edu/course/meet-the-tas",
            "https://example.edu/course/resources/hgc1l_6yskc-1",
        },
    )
    assert "Meet the TAs" not in rendered
    assert "video transcript" not in rendered


def test_flagship_math_pages_lead_with_course_indexes_not_crawler_debris() -> None:
    root = Path(__file__).resolve().parents[1]
    catalogue = json.loads((root / "data" / "courses.json").read_text(encoding="utf-8"))
    guides, issues = load_course_guides(
        root / "data" / "course_guides.json",
        catalogue,
    )
    assert issues == []
    courses_by_source = {
        int(course["source_id"]): course for course in catalogue["courses"]
    }
    tracks_by_id = {track["id"]: track for track in catalogue["tracks"]}

    for course_id, resource_index in (
        (
            4,
            "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/resource-index",
        ),
        (
            7,
            "https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/pages/resource-index",
        ),
    ):
        course = courses_by_source[course_id]
        rendered = render_course_page(
            course,
            tracks_by_id[str(course["track"])],
            "en",
            courses_by_source,
            guide=guides[course_id],
        )
        resources = rendered.split("## Course Resources\n\n", 1)[1]
        top_links = resources.split('<details markdown="1">', 1)[0]

        assert f"]({resource_index})" in top_links
        assert "Meet the TAs" not in resources
        assert "Meet The Team" not in resources
        assert "video transcript (PDF) — ocw.mit.edu/" not in resources


def test_course_resource_summaries_expose_every_executable_starter() -> None:
    root = Path(__file__).resolve().parents[1]
    catalogue = json.loads((root / "data" / "courses.json").read_text(encoding="utf-8"))
    guides, issues = load_course_guides(
        root / "data" / "course_guides.json",
        catalogue,
    )
    assert issues == []
    courses_by_source = {
        int(course["source_id"]): course for course in catalogue["courses"]
    }
    tracks_by_id = {track["id"]: track for track in catalogue["tracks"]}
    examples = {
        16: "ring-buffer",
        21: "rc-lowpass",
        37: "sync-fifo",
        55: "tmp117-kicad",
        57: "sensor-sampler",
    }

    for course_id, example_slug in examples.items():
        course = courses_by_source[course_id]
        rendered = render_course_page(
            course,
            tracks_by_id[str(course["track"])],
            "en",
            courses_by_source,
            guide=guides[course_id],
        )
        summary = rendered.split("## Resource Summary\n\n", 1)[1]
        assert (
            "https://github.com/appleweiping/eediy/tree/main/examples/"
            f"{example_slug}"
        ) in summary


def test_collapsed_resource_index_uses_natural_number_order() -> None:
    resources = [
        {
            "id": f"homework-{number}",
            "kind": "assignments",
            "title": {"zh": f"作业 {number}", "en": f"Homework {number}"},
            "url": f"https://example.edu/ee101/homework-{number}",
            "access": "open",
            "status": "available",
            "last_verified": "2026-07-31",
        }
        for number in (1, 10, 11, 2, 9)
    ]

    rendered = _render_resource_index(
        {"resources": resources},
        "en",
        show_coverage=False,
    )

    assert rendered.index("[Homework 1]") < rendered.index("[Homework 2]")
    assert rendered.index("[Homework 2]") < rendered.index("[Homework 9]")
    assert rendered.index("[Homework 9]") < rendered.index("[Homework 10]")
    assert rendered.index("[Homework 10]") < rendered.index("[Homework 11]")


def test_access_summary_uses_resource_access_not_course_tier() -> None:
    course = {
        "tier": "A",
        "resources": [
            {
                "access": "open-registration",
                "status": "available",
            }
        ],
    }

    assert _resource_access_summary(course, "zh") == "需注册；可用范围以平台为准"
    assert (
        _resource_access_summary(course, "en")
        == "Registration required; scope varies by platform"
    )


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
    assert 'track_id: "track-mathematics"' in expected[
        docs_root / "courses" / "mathematics" / "index.md"
    ]
    assert 'route_id: "route-starter"' in expected[
        docs_root / "routes" / "starter.md"
    ]
    assert "comments: true" in expected[
        docs_root / "courses" / "mathematics" / "index.md"
    ]
    assert "comments: true" in expected[docs_root / "routes" / "starter.md"]
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

    assert "开始前请确认这些课程的材料限制" in zh_track
    assert "公开反馈仍需复核" in zh_track
    assert "Check the material limits before starting" in en_course
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
    zh_headings = markdown_headings(zh)
    en_headings = markdown_headings(en)
    assert [level for level, _, _ in zh_headings] == [
        level for level, _, _ in en_headings
    ]
    assert [(level, title) for level, title, _ in zh_headings if level == 2] == [
        (2, "课程简介"),
        (2, "课程资源"),
        (2, "资源汇总"),
    ]
    assert [(level, title) for level, title, _ in en_headings if level == 2] == [
        (2, "Course Overview"),
        (2, "Course Resources"),
        (2, "Resource Summary"),
    ]
    assert all(level in {1, 2, 3, 4} for level, _, _ in zh_headings)
    assert all(level in {1, 2, 3, 4} for level, _, _ in en_headings)
    zh_overview = zh.split("## 课程简介\n\n", 1)[1].split("\n## 课程资源", 1)[0]
    en_overview = en.split("## Course Overview\n\n", 1)[1].split(
        "\n## Course Resources", 1
    )[0]
    assert [line for line in zh.splitlines() if line.startswith("- **")][:6] == [
        "- **所属大学：** Example University",
        "- **课程编号：** EE-101",
        "- **官方先修：** 本次未核到提供方公布的硬性先修；开始前请复核课程主页",
        "- **本站建议背景：** 本站未另设准备条件",
        "- **访问条件：** 无需注册公开访问",
        "- **资料状态：** 2026-07-28；资料索引",
    ]
    assert [line for line in en.splitlines() if line.startswith("- **")][:6] == [
        "- **University:** Example University",
        "- **Course code:** EE-101",
        "- **Official prerequisites:** No provider-published hard prerequisite verified; recheck the course page",
        "- **EEDIY preparation:** No additional EEDIY preparation requirement",
        "- **Access:** Open without registration",
        "- **Material status:** 2026-07-28; resource catalogue",
    ]
    assert (
        "# Example University EE-101: Signals Through Calculus" in zh
        and "## 课程简介" in zh
    )
    assert (
        "# Example University EE-101: Signals Through Calculus" in en
        and "## Course Overview" in en
    )
    zh_index = expected[tmp_path / "docs" / "courses" / "index.md"]
    en_index = expected[tmp_path / "docs" / "en" / "courses" / "index.md"]
    assert "尚无完整学习复盘，会直接说明" in zh_index
    assert "based only on public materials says so plainly" in en_index
    assert "S 级" not in zh_index
    assert "S tier" not in en_index
    assert "以页面列出的完成证据为退出标准" not in zh_index
    assert "Meet the page's completion-evidence standard" not in en_index
    assert "**说明：** 本页目前只整理了课程身份和材料入口" not in zh
    assert "**Note:** This page currently records the course identity" not in en
    assert "## 资源汇总" in zh
    assert "本次核对的公开入口已全部列在上方" in zh
    assert "## Resource Summary" in en
    assert "Every public entry point verified in this review is listed above" in en
    assert "逐讲链接和历史试卷" not in zh
    assert "Per-lecture files and historical exams" not in en
    assert "只表示本次未核到，不能反推提供方一定没有" in zh
    assert "absence is not proof that the provider has none" in en
    assert "### 材料覆盖" not in zh
    assert "### Material coverage" not in en
    assert "Show more official resources" not in en
    assert "维护者规划估计" not in zh
    assert "maintainer planning estimate" not in en
    assert "实践闭环" not in zh
    assert "Practice loop" not in en
    assert 'course_id: "course-001"' in zh
    assert "discussion_term:" not in zh
    assert 'reviewed_at: "2026-07-28"' in zh
    assert "comments: true" in en
    en_route = expected[tmp_path / "docs" / "en" / "routes" / "starter.md"]
    assert "**Move on when:**" in en_route
    assert "criterion：**" not in en_route
    assert "**Page: Resource catalogue**" not in en_route
    assert "## Notes on sources and practice" not in en_route
    assert re.search(r"; [SAB](?:;|$)", en_route, re.MULTILINE) is None
    assert "complete every required course" not in en_route
    assert "**Required**" in en_route
    assert (
        "**Why these courses:** Complete the foundation course first, then use the "
        "stage artifact to decide whether to continue." in en_route
    )
    assert "## Diagnose first" in en_route
    assert "Begin with one diagnostic problem before opening the course." in en_route
    assert "## Close the loop" in en_route
    assert "- Complete one repeatable foundation exercise." in en_route
    assert "- Skip units you already command." in en_route
    assert "- Stop when the result reproduces independently on new parameters." in en_route
    assert "## Start here" not in en_route
    assert "## Do this" not in en_route
    assert "## Skip for now" not in en_route
    assert "## Stop when" not in en_route
    assert "Use all 1 core course" not in en_route
    assert "使用全部 1 门核心课程取材" not in "\n".join(
        expected[path]
        for path in expected
        if path.parts[-2] == "routes"
    )
    assert "1. Foundation" not in en_route


def test_committed_generated_pages_do_not_repeat_an_h2() -> None:
    root = Path(__file__).resolve().parents[1]
    generated_roots = (
        root / "docs" / "courses",
        root / "docs" / "routes",
        root / "docs" / "en" / "courses",
        root / "docs" / "en" / "routes",
    )

    for generated_root in generated_roots:
        for path in generated_root.rglob("*.md"):
            h2_titles = [
                title.strip().casefold()
                for level, title, _ in markdown_headings(
                    path.read_text(encoding="utf-8")
                )
                if level == 2
            ]
            assert len(h2_titles) == len(set(h2_titles)), (
                path.relative_to(root),
                "generated page repeats an H2 label",
            )


def test_committed_course_pages_follow_csdiy_three_section_template() -> None:
    root = Path(__file__).resolve().parents[1]
    expectations = (
        (root / "docs" / "courses", ["课程简介", "课程资源", "资源汇总"]),
        (
            root / "docs" / "en" / "courses",
            ["Course Overview", "Course Resources", "Resource Summary"],
        ),
    )

    checked = 0
    for generated_root, expected_h2 in expectations:
        for path in generated_root.rglob("*.md"):
            content = path.read_text(encoding="utf-8")
            if 'page_type: course' not in content:
                continue
            h2_titles = [
                title
                for level, title, _ in markdown_headings(content)
                if level == 2
            ]
            assert h2_titles == expected_h2, path.relative_to(root)
            checked += 1

    catalogue = json.loads(
        (root / "data" / "courses.json").read_text(encoding="utf-8")
    )
    assert checked == 2 * len(catalogue["courses"])


def test_generated_pages_do_not_render_inline_language_switches(
    tmp_path: Path, catalogue: dict, routes_data: dict
) -> None:
    expected = build_expected_pages(catalogue, routes_data, tmp_path / "docs")

    for content in expected.values():
        assert "[English](" not in content
        assert "[中文](" not in content

    detail_pages = [
        content
        for path, content in expected.items()
        if path.name != "index.md" or path.parent.name == "mathematics"
    ]
    assert detail_pages
    assert all("[← " not in content for content in detail_pages)


def test_authored_track_guide_replaces_generic_track_boilerplate(
    tmp_path: Path, catalogue: dict, routes_data: dict
) -> None:
    track_guides = {
        "mathematics": {
            "bodies": {
                "zh": (
                    "## 具体课程怎么选\n\n[课程](001-ee-101.md)的取舍。\n\n"
                    "## 先后关系\n\n先做诊断。\n\n## 退出证据\n\n保留可复核产物。\n"
                ),
                "en": (
                    "## How the courses differ\n\nCompare the [course](001-ee-101.md).\n\n"
                    "## Sequence\n\nBegin with a diagnostic.\n\n"
                    "## Exit evidence\n\nRetain a reviewable artifact.\n"
                ),
            }
        }
    }

    expected = build_expected_pages(
        catalogue,
        routes_data,
        tmp_path / "docs",
        track_guides=track_guides,
    )
    zh = expected[tmp_path / "docs" / "courses" / "mathematics" / "index.md"]
    en = expected[
        tmp_path / "docs" / "en" / "courses" / "mathematics" / "index.md"
    ]

    assert "## 具体课程怎么选" in zh
    assert "## How the courses differ" in en
    assert "掌握工程数学的核心概念" not in zh
    assert "Explain the core concepts" not in en
    assert "## 方向验收" not in zh
    assert "## Track completion" not in en
    assert 'track_id: "track-mathematics"' in zh
    assert 'track_id: "track-mathematics"' in en
    assert "comments: true" in zh
    assert "comments: true" in en


def test_track_table_exposes_all_editorial_evidence_states(
    tmp_path: Path, catalogue: dict, routes_data: dict
) -> None:
    expected_labels = {
        "catalogue": (
            "资料索引；不是完整课程替代",
            "Catalogue only; not a complete course substitute",
        ),
        "researched": ("公开材料导读", "Public-material guide"),
        "learner-reviewed": ("学习者复核", "Learner-reviewed"),
    }

    track = catalogue["tracks"][0]
    tracks_by_id = {track["id"]: track}
    for status, (zh_label, en_label) in expected_labels.items():
        zh = render_track_page(
            track,
            catalogue["courses"],
            tracks_by_id,
            "zh",
            course_guides={1: {"editorial_status": status}},
        )
        en = render_track_page(
            track,
            catalogue["courses"],
            tracks_by_id,
            "en",
            course_guides={1: {"editorial_status": status}},
        )

        assert "| 编辑证据 |" in zh
        assert "| Editorial evidence |" in en
        assert f"| {zh_label} |" in zh
        assert f"| {en_label} |" in en


def test_track_table_does_not_treat_a_successor_course_report_as_course_completion(
    catalogue: dict,
) -> None:
    track = catalogue["tracks"][0]
    tracks_by_id = {track["id"]: track}
    course_id = int(catalogue["courses"][0]["source_id"])
    same_course_guide = {
        "editorial_status": "learner-reviewed",
        "learner_reviews": [{"relationship": "same-course-other-run"}],
    }
    successor_guide = {
        "editorial_status": "researched",
        "learner_reviews": [{"relationship": "successor-course"}],
    }

    same_course = render_track_page(
        track,
        catalogue["courses"],
        tracks_by_id,
        "en",
        course_guides={course_id: same_course_guide},
    )
    successor = render_track_page(
        track,
        catalogue["courses"],
        tracks_by_id,
        "zh",
        course_guides={course_id: successor_guide},
    )

    assert "Learner-reviewed (another run of the same course)" in same_course
    assert "后继课程复盘仅作背景" in successor
    assert "学习者复核（对应开课）" not in successor


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
    guide_data = json.loads(
        (root / "data" / "course_guides.json").read_text(encoding="utf-8")
    )
    researched_ids = {
        guide["course_id"]
        for guide in guide_data["guides"]
        if guide["editorial_status"] in {"researched", "learner-reviewed"}
    }

    en = render_route_page(
        route,
        courses_by_source,
        "en",
        researched_course_ids=researched_ids,
    )
    zh = render_route_page(
        route,
        courses_by_source,
        "zh",
        researched_course_ids=researched_ids,
    )

    assert (
        "**Why these courses:** Complete one coherent path. The MIT path runs 6.4210 "
        "then 6.832 for manipulation and underactuated systems; the Modern Robotics "
        "path runs Courses 1–6 in order and may require paid platform access."
    ) in en
    assert "**Complete path — MIT Robotics path (take these in the listed order)**" in en
    assert (
        "**Complete path — Complete Modern Robotics path (Courses 1–6 in order; "
        "full platform access may be paid) "
        "(take these in the listed order)**"
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
    assert "**Course in this path**" in course_six_line
    assert "**Page: Researched guide**" not in course_six_line
    assert re.search(r"; [SAB](?:;|$)", course_six_line) is None
    assert "**Choose from these**" not in course_six_line
    assert (
        "两条路径择一并完整走通：MIT 路线按 6.4210→6.832 聚焦 manipulation "
        "与欠驱动系统；Modern Robotics 路线按 Course 1–6 顺序完成"
    ) in zh
    assert (
        "**完整路线 — Modern Robotics 完整路径（课程 1–6 按序；"
        "平台完整访问可能收费）（按列出顺序学习）**"
    ) in zh


def test_digital_route_renders_branch_specific_stop_conditions() -> None:
    root = Path(__file__).resolve().parents[1]
    catalogue = json.loads((root / "data" / "courses.json").read_text(encoding="utf-8"))
    routes = json.loads((root / "data" / "routes.json").read_text(encoding="utf-8"))[
        "routes"
    ]
    route = next(item for item in routes if item["id"] == "digital-fpga-architecture")
    courses_by_source = {course["source_id"]: course for course in catalogue["courses"]}

    en = render_route_page(route, courses_by_source, "en")
    zh = render_route_page(route, courses_by_source, "zh")

    assert en.count("**This branch is done when:**") == 2
    assert "This accepts a software stack only" in en
    assert "This artifact can feed the later RTL/FPGA stage." in en
    assert zh.count("**这条分支做到哪里：**") == 2
    assert "这里只验收软件栈" in zh
    assert "可以接入后面的 RTL/FPGA 阶段" in zh


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
    guide_data = json.loads(
        (root / "data" / "course_guides.json").read_text(encoding="utf-8")
    )
    researched_ids = {
        guide["course_id"]
        for guide in guide_data["guides"]
        if guide["editorial_status"] in {"researched", "learner-reviewed"}
    }
    audits_by_course, issues = mainline_audit_annotations(audit_data, catalogue)
    assert issues == []
    courses_by_source = {course["source_id"]: course for course in catalogue["courses"]}
    route_map = {route["id"]: route for route in routes}
    cases = (("control-robotics", 73),)
    for route_id, course_id in cases:
        rendered = render_route_page(
            route_map[route_id],
            courses_by_source,
            "en",
            audits_by_course,
            researched_ids,
        )
        title = courses_by_source[course_id]["title"]["en"]
        course_line = next(
            line
            for line in rendered.splitlines()
            if f"[{title}]" in line and "**Use if needed**" in line
        )
        assert "**Use if needed**" in course_line
        assert "**Choose from these**" not in course_line
        assert "**Check material limits**" in course_line
        assert audits_by_course[course_id]["limitation_en"] in rendered

    photonics = render_route_page(
        route_map["photonics-mems"],
        courses_by_source,
        "en",
        audits_by_course,
        researched_ids,
    )
    silicon_title = courses_by_source[133]["title"]["en"]
    silicon_line = next(
        line
        for line in photonics.splitlines()
        if f"[{silicon_title}]" in line and "**Course in this path**" in line
    )
    assert "**Check material limits**" in silicon_line
    assert courses_by_source[133]["review_note"]["en"] in photonics


def test_power_route_renders_ordered_extension_and_complete_system_paths() -> None:
    root = Path(__file__).resolve().parents[1]
    catalogue = json.loads((root / "data" / "courses.json").read_text(encoding="utf-8"))
    routes = json.loads((root / "data" / "routes.json").read_text(encoding="utf-8"))["routes"]
    courses_by_source = {course["source_id"]: course for course in catalogue["courses"]}
    route = next(item for item in routes if item["id"] == "power-energy")

    rendered_en = render_route_page(route, courses_by_source, "en")
    assert (
        "**Optional ordered extension — Coursera Power Electronics 1→2→3 "
        "(take these in the listed order)**"
    ) in rendered_en
    extension_titles = [
        courses_by_source[course_id]["title"]["en"]
        for course_id in (115, 116, 117)
    ]
    extension_positions = [
        rendered_en.index(f"{index}. [{title}]")
        for index, title in enumerate(extension_titles, 1)
    ]
    assert extension_positions == sorted(extension_positions)
    assert rendered_en.count("**Complete path —") >= 4
    assert "**Complete path — Grid analysis (take these in the listed order)**" in rendered_en
    assert "**Complete path — Machine and drive (take these in the listed order)**" in rendered_en
    assert (
        "**Complete path — Photovoltaic conversion "
        "(take these in the listed order)**"
    ) in rendered_en
    assert (
        "**Complete path — Electrochemical storage "
        "(take these in the listed order)**"
    ) in rendered_en
    assert "**Stage elective**" not in rendered_en

    rendered_zh = render_route_page(route, courses_by_source, "zh")
    assert "**可选有序扩展 — Coursera Power Electronics 1→2→3（按列出顺序学习）**" in rendered_zh
    assert "**完整路线 — 电网分析（按列出顺序学习）**" in rendered_zh


def test_shared_route_guidance_appears_once_on_the_route_index(
    catalogue: dict, routes_data: dict
) -> None:
    courses_by_source = {
        course["source_id"]: course for course in catalogue["courses"]
    }

    rendered_index = render_route_index(
        routes_data["routes"],
        courses_by_source,
        "en",
    )
    rendered_page = render_route_page(
        routes_data["routes"][0],
        courses_by_source,
        "en",
    )

    assert "## Before using a route" in rendered_index
    assert "Operate mains, high voltage" in rendered_index
    assert "## Notes on sources and practice" not in rendered_page
    assert "Operate mains, high voltage" not in rendered_page
