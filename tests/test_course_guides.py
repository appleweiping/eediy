from __future__ import annotations

import json
from pathlib import Path

from scripts.course_guides import _validate_body, load_course_guides
from scripts.check_course_guides import (
    MINIMUM_RESEARCHED_GUIDES,
    build_parser,
    mainline_guide_coverage_issues,
    release_gate_issues,
    track_coverage_issues,
)
from scripts.generate_course_pages import build_expected_pages


ROOT = Path(__file__).resolve().parents[1]


def test_track_coverage_requires_one_researched_guide_per_populated_track() -> None:
    catalogue = {
        "courses": [
            {"source_id": 1, "track": "circuits"},
            {"source_id": 2, "track": "signals"},
        ]
    }

    issues, statistics = track_coverage_issues(catalogue, {1: {}})

    assert statistics == {"tracks_populated": 2, "tracks_covered": 1}
    assert [issue.code for issue in issues] == ["guide.track_coverage"]
    assert issues[0].context == "signals"


def test_mainline_coverage_requires_a_guide_for_every_audited_course() -> None:
    audit = {"audits": [{"course_id": 1}, {"course_id": 2}]}

    issues, statistics = mainline_guide_coverage_issues(audit, {1: {}})

    assert statistics == {"mainlines_audited": 2, "mainlines_covered": 1}
    assert [issue.code for issue in issues] == ["guide.mainline_coverage"]
    assert issues[0].context == "002"


def test_release_gate_defaults_to_60_guides_and_full_coverage() -> None:
    args = build_parser().parse_args([])

    assert args.minimum_guides == MINIMUM_RESEARCHED_GUIDES == 60
    assert args.require_track_coverage is True
    assert args.require_mainline_coverage is True

    catalogue = {
        "courses": [
            {"source_id": 1, "track": "circuits"},
            {"source_id": 2, "track": "signals"},
        ]
    }
    mainline_audit = {"audits": [{"course_id": 1}, {"course_id": 2}]}
    issues, statistics = release_gate_issues(
        catalogue,
        {1: {}},
        mainline_audit=mainline_audit,
    )

    assert statistics == {
        "guides": 1,
        "minimum_guides": 60,
        "tracks_populated": 2,
        "tracks_covered": 1,
        "mainlines_audited": 2,
        "mainlines_covered": 1,
    }
    assert {issue.code for issue in issues} == {
        "guide.minimum_count",
        "guide.track_coverage",
        "guide.mainline_coverage",
    }


def test_production_course_guides_are_bilingual_and_evidence_bounded() -> None:
    catalogue = json.loads((ROOT / "data" / "courses.json").read_text(encoding="utf-8"))
    guides, issues = load_course_guides(ROOT / "data" / "course_guides.json", catalogue)

    assert issues == []
    assert 7 in guides
    assert guides[7]["editorial_status"] == "researched"
    assert guides[7]["evidence_level"] == "R0"
    assert guides[7]["learner_reviews"] == []
    assert set(guides[7]["bodies"]) == {"zh", "en"}


def test_production_course_guides_pass_the_release_gate() -> None:
    catalogue = json.loads((ROOT / "data" / "courses.json").read_text(encoding="utf-8"))
    mainline_audit = json.loads(
        (ROOT / "data" / "mainline_audit.json").read_text(encoding="utf-8")
    )
    guides, load_issues = load_course_guides(
        ROOT / "data" / "course_guides.json",
        catalogue,
    )
    release_issues, statistics = release_gate_issues(
        catalogue,
        guides,
        mainline_audit=mainline_audit,
    )

    assert load_issues == []
    assert release_issues == []
    assert statistics["guides"] >= 60
    assert statistics["tracks_covered"] == statistics["tracks_populated"] == 35
    assert statistics["mainlines_covered"] == statistics["mainlines_audited"] == 60


def test_researched_guide_replaces_catalogue_copy_but_keeps_resource_index() -> None:
    catalogue = json.loads((ROOT / "data" / "courses.json").read_text(encoding="utf-8"))
    routes = json.loads((ROOT / "data" / "routes.json").read_text(encoding="utf-8"))
    guides, issues = load_course_guides(ROOT / "data" / "course_guides.json", catalogue)
    assert issues == []

    docs_root = ROOT / "build" / "guide-render-test"
    pages = build_expected_pages(
        catalogue,
        routes,
        docs_root,
        course_guides=guides,
    )
    zh = pages[
        docs_root
        / "courses"
        / "probability-statistics"
        / "007-6-041sc.md"
    ]
    en = pages[
        docs_root
        / "en"
        / "courses"
        / "probability-statistics"
        / "007-6-041sc.md"
    ]

    assert 'editorial_status: "researched"' in zh
    assert "## 课程简介" in zh and "**资料考察（R0）：**" in zh
    assert "25 讲" in zh and "11 份 problem set" in zh
    assert "## Course Overview" in en and "**Desk-researched (R0):**" in en
    assert "25 lectures" in en and "eleven problem sets" in en
    assert '## 课程资源' in zh and '<details markdown="1">' in zh
    assert '## Course Resources' in en and '<details markdown="1">' in en
    assert "11 周，每周 9 小时" not in zh
    assert "11 weeks at 9 hours/week" not in en
    assert "95% coverage" not in en


def test_r0_fragment_rejects_first_hand_claims(tmp_path: Path) -> None:
    body = (
        "## Course position\n\n"
        + "I completed this course and recommend it. " * 80
        + "\n\n## Assignments\n\n"
        + "[Course](https://example.edu/course) "
        + "[Work](https://example.edu/work) "
        + "[Exam](https://example.edu/exam)"
        + "\n\n## Limits\n\n"
        + "A specific limitation. " * 80
    )
    path = tmp_path / "guide.en.md"
    path.write_text(body, encoding="utf-8")

    issues = _validate_body(
        body,
        language="en",
        path=path,
        evidence_level="R0",
    )

    assert any(issue.code == "guide.unsourced_first_hand" for issue in issues)


def test_r0_fragment_allows_explicit_editorial_recommendation(tmp_path: Path) -> None:
    body = (
        "## Course position\n\n"
        + "Based on the published syllabus, I recommend this route for a first pass. " * 80
        + "\n\n## Assignments\n\n"
        + "[Course](https://example.edu/course) "
        + "[Work](https://example.edu/work) "
        + "[Exam](https://example.edu/exam)"
        + "\n\n## Limits\n\n"
        + "The recommendation is editorial judgment, not a completion claim. " * 80
    )
    path = tmp_path / "guide.en.md"

    issues = _validate_body(
        body,
        language="en",
        path=path,
        evidence_level="R0",
    )

    assert not any(issue.code == "guide.unsourced_first_hand" for issue in issues)
