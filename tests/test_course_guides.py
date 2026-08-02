from __future__ import annotations

import json
from pathlib import Path

import scripts.course_guides as course_guides_module
from scripts.course_data import normalize_url
from scripts.course_guides import (
    _external_links,
    _learner_review_issues,
    _validate_body,
    load_course_guides,
)
from scripts.check_course_guides import (
    build_parser,
    corpus_style_issues,
    deep_coursework_issues,
    mainline_guide_coverage_issues,
    release_gate_issues,
    track_coverage_issues,
)
from scripts.generate_course_pages import build_expected_pages


ROOT = Path(__file__).resolve().parents[1]


def test_schema_exposes_the_three_reader_facing_editorial_states() -> None:
    schema = json.loads(
        (ROOT / "data" / "course-guide.schema.json").read_text(encoding="utf-8")
    )
    status = schema["$defs"]["guide"]["properties"]["editorial_status"]

    assert status["enum"] == ["catalogue", "researched", "learner-reviewed"]
    assert "not complete course substitutes" in status["description"]


def test_schema_allows_contextual_guides_to_omit_the_generic_resource_tail() -> None:
    schema = json.loads(
        (ROOT / "data" / "course-guide.schema.json").read_text(encoding="utf-8")
    )
    mode = schema["$defs"]["guide"]["properties"]["resource_index_mode"]

    assert mode["enum"] == ["structured", "inline-only"]
    assert mode["default"] == "structured"
    assert "archive caveats" in mode["description"]


def test_schema_models_attributed_reports_without_inventing_completion_dates() -> None:
    schema = json.loads(
        (ROOT / "data" / "course-guide.schema.json").read_text(encoding="utf-8")
    )
    learner_review = schema["$defs"]["learnerReview"]

    assert set(learner_review["required"]) == {
        "author",
        "url",
        "evidence_kind",
        "evidence_level",
        "relationship",
        "published_at",
        "completion_period",
        "coverage",
        "environment",
        "friction",
    }
    assert "completed_at" not in learner_review["properties"]
    assert learner_review["properties"]["evidence_kind"]["const"] == (
        "first-person-report"
    )
    assert learner_review["properties"]["evidence_level"]["enum"] == [
        "R2",
        "R3",
        "R4",
    ]
    assert learner_review["properties"]["relationship"]["enum"] == [
        "exact-offering",
        "same-course-other-run",
        "successor-course",
    ]
    for field in ("coverage", "environment", "friction"):
        assert learner_review["properties"][field]["$ref"] == (
            "#/$defs/bilingualText"
        )


def test_learner_review_semantics_require_a_report_and_matching_status() -> None:
    review = {
        "author": "Example Learner",
        "url": "https://example.edu/learner-account",
        "evidence_kind": "first-person-report",
        "evidence_level": "R3",
        "relationship": "same-course-other-run",
        "published_at": "2024-05-01",
        "completion_period": "Spring 2024",
        "coverage": {"zh": "完成全部实验。", "en": "Completed all laboratories."},
        "environment": {"zh": "使用 FPGA。", "en": "Used an FPGA."},
        "friction": {"zh": "调试时钟域。", "en": "Debugged clock domains."},
    }
    valid = {
        "editorial_status": "learner-reviewed",
        "evidence_level": "R3",
        "reviewed_at": "2026-07-31",
        "learner_reviews": [review],
    }

    assert _learner_review_issues(valid, source="fixture") == []

    empty = {**valid, "learner_reviews": []}
    assert {issue.code for issue in _learner_review_issues(empty, source="fixture")} == {
        "guide.review_missing"
    }

    wrong_status = {**valid, "editorial_status": "researched"}
    assert {
        issue.code
        for issue in _learner_review_issues(wrong_status, source="fixture")
    } == {"guide.review_state"}

    successor_review = {**review, "relationship": "successor-course"}
    successor_context = {
        **valid,
        "editorial_status": "researched",
        "evidence_level": "R0",
        "learner_reviews": [successor_review],
    }
    assert _learner_review_issues(successor_context, source="fixture") == []

    successor_as_learner_reviewed = {
        **successor_context,
        "editorial_status": "learner-reviewed",
        "evidence_level": "R3",
    }
    assert {
        issue.code
        for issue in _learner_review_issues(
            successor_as_learner_reviewed,
            source="fixture",
        )
    } == {"guide.review_missing"}

    missing_relationship = {key: value for key, value in review.items() if key != "relationship"}
    assert {
        issue.code
        for issue in _learner_review_issues(
            {**valid, "learner_reviews": [missing_relationship]},
            source="fixture",
        )
    } == {"guide.review_missing", "guide.review_shape", "guide.review_relationship"}

    invalid_relationship = {**review, "relationship": "similar-course"}
    assert {
        issue.code
        for issue in _learner_review_issues(
            {**valid, "learner_reviews": [invalid_relationship]},
            source="fixture",
        )
    } == {"guide.review_missing", "guide.review_relationship"}


def test_track_coverage_requires_one_deep_guide_per_populated_track() -> None:
    catalogue = {
        "courses": [
            {"source_id": 1, "track": "circuits"},
            {"source_id": 2, "track": "signals"},
        ]
    }

    issues, statistics = track_coverage_issues(
        catalogue,
        {1: {"editorial_status": "researched"}},
    )

    assert statistics == {"tracks_populated": 2, "tracks_deep_covered": 1}
    assert [issue.code for issue in issues] == ["guide.track_coverage"]
    assert issues[0].context == "signals"


def test_mainline_coverage_requires_a_deep_guide_for_every_audited_course() -> None:
    audit = {"audits": [{"course_id": 1}, {"course_id": 2}]}

    issues, statistics = mainline_guide_coverage_issues(
        audit,
        {1: {"editorial_status": "researched"}},
    )

    assert statistics == {
        "mainlines_audited": 2,
        "mainlines_deep_covered": 1,
    }
    assert [issue.code for issue in issues] == ["guide.mainline_coverage"]
    assert issues[0].context == "002"


def test_release_gate_defaults_to_structural_coverage_without_a_count_quota() -> None:
    args = build_parser().parse_args([])

    assert not hasattr(args, "minimum_authored_guides")
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
        {1: {"editorial_status": "researched"}},
        mainline_audit=mainline_audit,
    )

    assert statistics == {
        "authored_guides": 1,
        "deep_guides": 1,
        "catalogue_guides": 0,
        "tracks_populated": 2,
        "tracks_deep_covered": 1,
        "mainlines_audited": 2,
        "mainlines_deep_covered": 1,
    }
    assert {issue.code for issue in issues} == {
        "guide.track_coverage",
        "guide.mainline_coverage",
    }


def test_catalogue_record_counts_as_authored_but_not_as_deep_coverage() -> None:
    catalogue = {
        "courses": [
            {
                "source_id": 1,
                "track": "circuits",
                "resource_coverage": {
                    "practice": 0,
                    "labs": 0,
                    "exams": 0,
                },
            },
        ]
    }
    mainline_audit = {"audits": [{"course_id": 1}]}

    issues, statistics = release_gate_issues(
        catalogue,
        {1: {"editorial_status": "catalogue"}},
        mainline_audit=mainline_audit,
    )

    assert statistics == {
        "authored_guides": 1,
        "deep_guides": 0,
        "catalogue_guides": 1,
        "tracks_populated": 1,
        "tracks_deep_covered": 0,
        "mainlines_audited": 1,
        "mainlines_deep_covered": 0,
    }
    assert {issue.code for issue in issues} == {
        "guide.track_coverage",
        "guide.mainline_coverage",
    }


def test_deep_status_requires_structured_public_coursework() -> None:
    catalogue = {
        "courses": [
            {
                "source_id": 41,
                "track": "digital-logic",
                "resource_coverage": {
                    "video": 0,
                    "notes": 2,
                    "practice": 0,
                    "labs": 0,
                    "exams": 0,
                    "code": 0,
                },
                "projects": [
                    {
                        "origin": "suggested",
                        "title": {"en": "Independent RTL project"},
                    }
                ],
            }
        ]
    }
    guides = {41: {"editorial_status": "researched"}}

    issues = deep_coursework_issues(catalogue, guides)
    release_issues, _ = release_gate_issues(
        catalogue,
        guides,
        require_track_coverage=False,
        require_mainline_coverage=False,
    )

    assert [issue.code for issue in issues] == [
        "guide.deep_without_public_coursework"
    ]
    assert issues[0].context == "041"
    assert "guide.deep_without_public_coursework" in {
        issue.code for issue in release_issues
    }


def test_scores_below_two_do_not_claim_a_usable_material_set() -> None:
    catalogue = {
        "courses": [
            {
                "source_id": 1,
                "resource_coverage": {
                    "video": 0,
                    "notes": 0,
                    "practice": 1,
                    "labs": 0,
                    "exams": 0,
                    "code": 0,
                },
                "resources": [
                    {
                        "kind": "assignments",
                        "access": "open",
                        "status": "available",
                        "artifact_scope": "content",
                    }
                ],
            },
            {
                "source_id": 2,
                "resource_coverage": {
                    "video": 0,
                    "notes": 0,
                    "practice": 0,
                    "labs": 0,
                    "exams": 0,
                    "code": 0,
                },
                "projects": [{"origin": "suggested"}],
            },
        ]
    }
    guides = {
        1: {"editorial_status": "researched"},
        2: {"editorial_status": "learner-reviewed"},
    }

    issues = deep_coursework_issues(catalogue, guides)

    assert issues == []


def test_partial_coverage_may_be_documented_by_non_content_records() -> None:
    catalogue = {
        "courses": [
            {
                "source_id": 94,
                "resource_coverage": {
                    "video": 0,
                    "notes": 0,
                    "practice": 1,
                    "labs": 0,
                    "exams": 0,
                    "code": 0,
                },
                "resources": [
                    {
                        "kind": "assignments",
                        "access": "open",
                        "status": "available",
                        "artifact_scope": "index",
                    }
                ],
            },
            {
                "source_id": 95,
                "resource_coverage": {
                    "video": 0,
                    "notes": 1,
                    "practice": 1,
                    "labs": 1,
                    "exams": 0,
                    "code": 0,
                },
                "resources": [
                    {
                        "kind": "labs",
                        "access": "open",
                        "status": "available",
                        "artifact_scope": "outline",
                    },
                    {
                        "kind": "labs",
                        "access": "institutional",
                        "status": "available",
                        "artifact_scope": "content",
                    },
                ],
            },
            {
                "source_id": 133,
                "resource_coverage": {
                    "video": 0,
                    "notes": 0,
                    "practice": 1,
                    "labs": 0,
                    "exams": 0,
                    "code": 0,
                },
                "resources": [
                    {
                        "kind": "course",
                        "access": "paid",
                        "status": "available",
                        "artifact_scope": "landing",
                    }
                ],
            },
        ]
    }
    guides = {
        course_id: {"editorial_status": "researched"}
        for course_id in (94, 95, 133)
    }

    issues = deep_coursework_issues(catalogue, guides)

    assert issues == []


def test_every_score_two_field_needs_matching_available_substantive_content() -> None:
    catalogue = {
        "courses": [
            {
                "source_id": 112,
                "resource_coverage": {
                    "video": 2,
                    "notes": 2,
                    "practice": 2,
                    "labs": 0,
                    "exams": 0,
                    "code": 2,
                },
                "resources": [
                    {
                        "kind": "course",
                        "access": "open",
                        "status": "available",
                        "artifact_scope": "landing",
                    },
                    {
                        "kind": "video",
                        "access": "open",
                        "status": "available",
                        "artifact_scope": "content",
                    },
                    {
                        "kind": "notes",
                        "access": "open",
                        "status": "degraded",
                        "artifact_scope": "content",
                    },
                    {
                        "kind": "assignments",
                        "access": "open",
                        "status": "available",
                        "artifact_scope": "index",
                    },
                    {
                        "kind": "code",
                        "access": "open",
                        "status": "available",
                    },
                ],
            }
        ]
    }

    issues = deep_coursework_issues(
        catalogue,
        {112: {"editorial_status": "researched"}},
    )

    assert [issue.code for issue in issues] == [
        "guide.deep_without_public_coursework"
    ]
    assert issues[0].context == "112"
    assert issues[0].message.endswith("Unsupported fields: notes, practice")


def test_corpus_gate_rejects_uniform_audit_dossiers() -> None:
    body = (
        "## 课程定位\n\n"
        + "EEDIY 先核对公开材料。这不是完整课程，学习者必须记录证据。"
        + "本段持续复述同一种流程与限制。" * 45
        + "\n\n## 作业\n\n"
        + "[课程](https://example.edu/course) "
        + "[作业](https://example.edu/work) "
        + "[考试](https://example.edu/exam)\n\n"
        + "## 完成\n\n保留一份结果。"
    )
    guide_ids = range(1, 5)
    guides = {
        course_id: {"bodies": {"zh": body, "en": "placeholder"}}
        for course_id in guide_ids
    }
    catalogue = {"courses": []}

    issues, statistics = corpus_style_issues(catalogue, guides)
    codes = {issue.code for issue in issues}

    assert {
        "guide.corpus_length_rhythm",
        "guide.corpus_heading_rhythm",
        "guide.corpus_domain_diversity",
        "guide.corpus_template_vocabulary",
    } <= codes
    assert statistics["guide_h2_mode_share"] == 1.0
    assert statistics["guide_median_unique_domains"] == 1.0


def test_corpus_gate_rejects_repeated_heading_and_protocol_endings() -> None:
    body = (
        "## 结论：适合做第一门课\n\n"
        "课程的具体取舍、公开材料和难点在这里说明。\n\n"
        "## 用一个项目收尾\n\n"
        "[课程](https://example.edu/course) "
        "[作业](https://example.edu/work) "
        "[考试](https://example.edu/exam)\n\n"
        "结课时必须交付报告、冻结证据包并通过验收。"
    )
    guides = {
        course_id: {"bodies": {"zh": body, "en": "placeholder"}}
        for course_id in range(1, 142)
    }
    catalogue = {
        "courses": [
            {"source_id": course_id, "role": "mainline"}
            for course_id in range(1, 142)
        ]
    }

    issues, statistics = corpus_style_issues(catalogue, guides)
    codes = {issue.code for issue in issues}

    assert "guide.corpus_heading_template" in codes
    assert "guide.corpus_protocol_endings" in codes
    assert "guide.corpus_governance_endings" in codes
    assert "guide.corpus_normative_endings" in codes
    assert statistics["guide_heading_pattern_page_shares"] == {
        "first H2 starts with 结论": 1.0,
        "an H2 starts with 用": 1.0,
    }
    assert statistics["guide_protocol_ending_share"] == 1.0
    assert statistics["guide_governance_ending_share"] == 1.0
    assert statistics["guide_normative_ending_share"] == 1.0


def test_production_course_guides_are_bilingual_and_evidence_bounded() -> None:
    catalogue = json.loads((ROOT / "data" / "courses.json").read_text(encoding="utf-8"))
    guides, issues = load_course_guides(ROOT / "data" / "course_guides.json", catalogue)

    assert issues == []
    assert 7 in guides
    assert guides[7]["editorial_status"] == "researched"
    assert guides[7]["evidence_level"] == "R0"
    assert guides[7]["learner_reviews"] == []
    assert set(guides[7]["bodies"]) == {"zh", "en"}
    assert guides[41]["editorial_status"] == "catalogue"
    for course_id, status, evidence_level, relationship, author, completion_period, published_at, url in (
        (
            21,
            "learner-reviewed",
            "R3",
            "same-course-other-run",
            "Steven J. Frank",
            "March–June 2012",
            "2012-07-13",
            "https://spectrum.ieee.org/review-mitxs-online-circuit-design-and-analysis-course",
        ),
        (
            42,
            "researched",
            "R0",
            "successor-course",
            "Andi Q. ’25",
            "Fall 2023",
            "2023-12-21",
            "https://mitadmissions.org/blogs/entry/6-2050-field-programmable-gate-awesomeness/",
        ),
    ):
        guide = guides[course_id]
        assert guide["editorial_status"] == status
        assert guide["evidence_level"] == evidence_level
        assert guide["reviewed_at"] == "2026-07-31"
        assert len(guide["learner_reviews"]) == 1
        report = guide["learner_reviews"][0]
        assert report["author"] == author
        assert report["completion_period"] == completion_period
        assert report["published_at"] == published_at
        assert report["url"] == url
        assert report["evidence_kind"] == "first-person-report"
        assert report["evidence_level"] == "R3"
        assert report["relationship"] == relationship
        assert "completed_at" not in report


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
    assert statistics["authored_guides"] == len(catalogue["courses"])
    assert (
        statistics["deep_guides"] + statistics["catalogue_guides"]
        == statistics["authored_guides"]
    )
    populated_tracks = {course["track"] for course in catalogue["courses"]}
    assert (
        statistics["tracks_deep_covered"]
        == statistics["tracks_populated"]
        == len(populated_tracks)
    )
    audited_mainlines = sum(
        course.get("role") == "mainline" for course in catalogue["courses"]
    )
    assert (
        statistics["mainlines_deep_covered"]
        == statistics["mainlines_audited"]
        == audited_mainlines
    )


def test_course_112_landing_page_cannot_substantiate_score_two() -> None:
    catalogue = json.loads((ROOT / "data" / "courses.json").read_text(encoding="utf-8"))
    course = next(
        item for item in catalogue["courses"] if item["source_id"] == 112
    )
    guide_manifest = json.loads(
        (ROOT / "data" / "course_guides.json").read_text(encoding="utf-8")
    )
    guide = next(
        item for item in guide_manifest["guides"] if item["course_id"] == 112
    )

    assert guide["editorial_status"] == "researched"
    assert course["resource_coverage"] == {
        "video": 1,
        "notes": 1,
        "practice": 1,
        "labs": 0,
        "exams": 0,
        "code": 0,
    }
    assert {
        (
            resource["kind"],
            resource["status"],
            resource.get("artifact_scope"),
        )
        for resource in course["resources"]
    } == {("course", "available", "landing")}
    assert deep_coursework_issues(
        {"courses": [course]},
        {112: guide},
    ) == []

    inflated = json.loads(json.dumps(course))
    inflated["resource_coverage"]["video"] = 2
    issues = deep_coursework_issues(
        {"courses": [inflated]},
        {112: guide},
    )

    assert [issue.context for issue in issues] == ["112"]
    assert issues[0].message.endswith("Unsupported fields: video")


def test_access_sensitive_course_fixtures_stay_consistent_across_sources() -> None:
    candidates = json.loads(
        (ROOT / "data" / "course_candidates.json").read_text(encoding="utf-8")
    )
    guide_manifest = json.loads(
        (ROOT / "data" / "course_guides.json").read_text(encoding="utf-8")
    )["guides"]
    resource_manifest = json.loads(
        (ROOT / "data" / "course_resource_overrides.json").read_text(
            encoding="utf-8"
        )
    )["resources"]
    editorial = json.loads(
        (ROOT / "data" / "course_editorial.json").read_text(encoding="utf-8")
    )

    candidate_by_id = {record["id"]: record for record in candidates}
    guide_by_id = {record["course_id"]: record for record in guide_manifest}
    resources_by_id = {
        course_id: [
            record
            for record in resource_manifest
            if record["course_id"] == course_id
        ]
        for course_id in (94, 95, 133, 137, 141)
    }
    editorial_records = (
        editorial["courses"] if isinstance(editorial, dict) else editorial
    )
    editorial_by_id = {
        record.get("course_id", record.get("source_id")): record
        for record in editorial_records
    }

    assert candidate_by_id[77]["workload"] == {
        "weeks": 2,
        "hours_per_week": {"min": 10, "max": 10},
    }
    guide_077_zh = (ROOT / guide_by_id[77]["files"]["zh"]).read_text(
        encoding="utf-8"
    )
    guide_077_en = (ROOT / guide_by_id[77]["files"]["en"]).read_text(
        encoding="utf-8"
    )
    assert "5 个模块" in guide_077_zh and "21 项作业" in guide_077_zh
    assert "5 modules" in guide_077_en and "21 assignments" in guide_077_en

    for course_id in (94, 95):
        assert candidate_by_id[course_id]["role"] == "alternative"
        assert guide_by_id[course_id]["editorial_status"] == "catalogue"
        assert set(candidate_by_id[course_id]["resources"].values()) == {0}
        assert resources_by_id[course_id]
        assert {
            resource["artifact_scope"] for resource in resources_by_id[course_id]
        } <= {"index", "outline", "landing", "syllabus"}
    assert [
        resource["kind"]
        for resource in resources_by_id[94]
        if resource["artifact_scope"] == "index"
    ] == ["other"]

    course_133 = candidate_by_id[133]
    assert course_133["role"] == "alternative"
    assert guide_by_id[133]["editorial_status"] == "catalogue"
    assert "does not mail each participant a personal chip" in course_133["risk"]
    assert "may be purchased separately" in course_133["risk"]
    assert [
        (
            resource["access"],
            resource["status"],
            resource["artifact_scope"],
            resource["last_verified"],
        )
        for resource in resources_by_id[133]
    ] == [("paid", "available", "landing", "2026-07-31")]
    assert "may be purchased separately" in editorial_by_id[133]["review_note"]["en"]
    assert "另行购买个人芯片" in editorial_by_id[133]["review_note"]["zh"]

    downloads_url = "https://nptel.ac.in/api/downloads/108106193"
    assert downloads_url in guide_by_id[137]["primary_sources"]
    assert [
        (
            resource["kind"],
            resource["access"],
            resource["status"],
            resource["artifact_scope"],
        )
        for resource in resources_by_id[137]
        if resource["url"] == downloads_url
    ] == [("video", "open", "available", "content")]

    bjtopamp_url = (
        "https://people.eecs.berkeley.edu/~pister/140sp23/labs/BJTopamp.asc"
    )
    assert candidate_by_id[141]["resources"]["code"] == 1
    assert bjtopamp_url in guide_by_id[141]["primary_sources"]
    assert [
        (
            resource["kind"],
            resource["access"],
            resource["status"],
            resource["artifact_scope"],
        )
        for resource in resources_by_id[141]
        if resource["url"] == bjtopamp_url
    ] == [("code", "open", "available", "content")]


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
    assert "## 课程简介" in zh
    assert "**资料状态：** 2026-07-29；公开材料导读" in zh
    assert "**资料状态：** 2026-07-29；公开材料导读\n\n" in zh
    assert "暂无完整学习复盘" not in zh
    assert "**说明：** 我们逐项核对了公开材料" not in zh
    assert "25 讲" in zh and "11 份 problem set" in zh
    assert "## Course Overview" in en
    assert (
        "**Material status:** 2026-07-29; public-material guide"
    ) in en
    assert (
        "**Material status:** 2026-07-29; public-material guide\n\n"
    ) in en
    assert "no complete learner report yet" not in en
    assert "**Note:** We checked the public course materials one by one" not in en
    assert "### 正文引用的官方材料" not in zh
    assert "### Official material cited above" not in en
    assert "25 lectures" in en and "11 problem sets" in en
    for language, rendered in (("zh", zh), ("en", en)):
        first_authored_heading = next(
            line[3:]
            for line in (
                ROOT / "content" / "course-guides" / f"007.{language}.md"
            ).read_text(encoding="utf-8").splitlines()
            if line.startswith("## ")
        )
        assert f"### {first_authored_heading}" in rendered
    assert '## 课程资源' in zh and '<details markdown="1">' in zh
    assert '## Course Resources' in en and '<details markdown="1">' in en
    assert "### 材料覆盖" not in zh and "可用材料集合" not in zh
    assert "### Material coverage" not in en and "Usable material set" not in en
    assert "### 资源" not in zh and "### Resource" not in en
    assert "**资源**" in zh and "**Resource**" in en
    assert "11 周，每周 9 小时" not in zh
    assert "11 weeks at 9 hours/week" not in en
    assert "95% coverage" not in en
    for rendered, resource_heading in (
        (zh, "## 课程资源"),
        (en, "## Course Resources"),
    ):
        visible = rendered.split("-->\n", 1)[1]
        narrative, resources = visible.split(resource_heading, 1)
        narrative_urls = [
            normalize_url(url) for url in _external_links(narrative)
        ]
        resource_urls = [
            normalize_url(url) for url in _external_links(resources)
        ]
        assert len(narrative_urls) == len(set(narrative_urls))
        assert len(resource_urls) == len(set(resource_urls))

        # The compact resource list may deliberately repeat a few decisive
        # links from the authored narrative for scan-first readers. Repetition
        # must stay at that section boundary rather than becoming a link wall.
        repeated = set(narrative_urls) & set(resource_urls)
        assert 1 <= len(repeated) <= 5
        all_urls = narrative_urls + resource_urls
        assert len(all_urls) - len(set(all_urls)) == len(repeated)


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


def test_learner_prose_rejects_internal_review_language_and_protocol_ending(
    tmp_path: Path,
) -> None:
    zh_body = (
        "## 课程位置\n\n"
        + "这门课围绕一个具体模型展开。" * 120
        + "\n\n## 材料用法\n\n"
        + "[课程](https://example.edu/course) "
        + "[作业](https://example.edu/work) "
        + "[考试](https://example.edu/exam)\n\n"
        + "## 结束建议\n\n"
        + "本页按 R0 桌面审读整理；纠错请附课程 ID。"
    )
    en_body = (
        "## Course position\n\n"
        + "This course develops one concrete model. " * 120
        + "\n\n## Using the material\n\n"
        + "[Course](https://example.edu/course) "
        + "[Work](https://example.edu/work) "
        + "[Exam](https://example.edu/exam)\n\n"
        + "## Closing advice\n\n"
        + "This is an R0 maintainer review; corrections should include the course ID."
    )

    zh_issues = _validate_body(
        zh_body,
        language="zh",
        path=tmp_path / "guide.zh.md",
        evidence_level="R0",
    )
    en_issues = _validate_body(
        en_body,
        language="en",
        path=tmp_path / "guide.en.md",
        evidence_level="R0",
    )

    assert {issue.code for issue in zh_issues} >= {
        "guide.internal_review_language",
        "guide.protocol_ending",
    }
    assert {issue.code for issue in en_issues} >= {
        "guide.internal_review_language",
        "guide.protocol_ending",
    }


def test_learner_prose_rejects_section_sprawl_and_brand_overuse(
    tmp_path: Path,
) -> None:
    sections = "\n\n".join(
        f"## Section {index}\n\n"
        + ("A concrete course-specific explanation. " * 35)
        for index in range(1, 9)
    )
    body = (
        sections
        + "\n\n[Course](https://example.edu/course) "
        + "[Work](https://example.edu/work) "
        + "[Exam](https://example.edu/exam)\n\n"
        + "EEDIY proposes one exercise. EEDIY labels it independently. "
        + "EEDIY keeps the result separate."
    )

    issues = _validate_body(
        body,
        language="en",
        path=tmp_path / "guide.en.md",
        evidence_level="R0",
    )

    assert {issue.code for issue in issues} >= {
        "guide.section_sprawl",
        "guide.brand_overuse",
    }


def test_learner_prose_rejects_dense_acceptance_protocol_vocabulary(
    tmp_path: Path,
) -> None:
    zh_body = (
        "## 课程位置\n\n"
        + "这门课围绕一个具体模型展开，并比较两种解法的适用范围。" * 20
        + "\n\n## 怎么学习\n\n"
        + "[课程](https://example.edu/course) "
        + "[作业](https://example.edu/work) "
        + "[考试](https://example.edu/exam)\n\n"
        + "记录参数，保留日志，复核输出；记录版本，保留截图，复核结论，再记录最终报告。"
    )
    en_body = (
        "## Course position\n\n"
        + "This course develops a concrete model and compares two solution methods. " * 20
        + "\n\n## How to study\n\n"
        + "[Course](https://example.edu/course) "
        + "[Work](https://example.edu/work) "
        + "[Exam](https://example.edu/exam)\n\n"
        + "Record parameters, preserve logs, review output, record versions, preserve "
        + "screenshots, review conclusions, archive an artifact, mark an unknown, "
        + "request sign-off, and write a final report."
    )

    zh_issues = _validate_body(
        zh_body,
        language="zh",
        path=tmp_path / "protocol.zh.md",
        evidence_level="R0",
    )
    en_issues = _validate_body(
        en_body,
        language="en",
        path=tmp_path / "protocol.en.md",
        evidence_level="R0",
    )

    assert "guide.protocol_tone_density" in {issue.code for issue in zh_issues}
    assert "guide.protocol_tone_density" in {issue.code for issue in en_issues}


def test_course_guide_rejects_both_thin_copy_and_exhaustive_dossiers(
    tmp_path: Path,
) -> None:
    links = (
        "[Course](https://example.edu/course) "
        "[Work](https://example.edu/work) "
        "[Exam](https://example.edu/exam)"
    )
    thin = (
        "## Course judgment\n\nA useful course.\n\n"
        f"## Work\n\n{links}\n"
    )
    sprawling = (
        "## Course judgment\n\n"
        + ("This sentence inventories every week instead of making a choice. " * 105)
        + "\n\n## Work\n\n"
        + links
        + "\n"
    )

    thin_issues = _validate_body(
        thin,
        language="en",
        path=tmp_path / "thin.en.md",
        evidence_level="R0",
    )
    sprawling_issues = _validate_body(
        sprawling,
        language="en",
        path=tmp_path / "sprawling.en.md",
        evidence_level="R0",
    )

    assert "guide.depth" in {issue.code for issue in thin_issues}
    assert "guide.sprawl" in {issue.code for issue in sprawling_issues}


def test_course_guide_must_begin_with_the_overview_h2(tmp_path: Path) -> None:
    body = (
        "A paragraph before the section heading would be silently folded into "
        "the wrong generated section.\n\n"
        "## Course judgment\n\n"
        + "This course makes one concrete, evidence-backed choice. " * 120
        + "\n\n## Work\n\n"
        "[Course](https://example.edu/course) "
        "[Work](https://example.edu/work) "
        "[Exam](https://example.edu/exam)\n"
    )

    issues = _validate_body(
        body,
        language="en",
        path=tmp_path / "bad-opening.en.md",
        evidence_level="R0",
    )

    assert "guide.opening_h2" in {issue.code for issue in issues}


def test_english_course_guide_rejects_singular_label_before_numeric_range(
    tmp_path: Path,
) -> None:
    body = (
        "## Course structure\n\n"
        + "Week 1–4 develops the circuit model. " * 30
        + "\n\n## Assignments\n\n"
        + "[Course](https://example.edu/course) "
        + "[Work](https://example.edu/work) "
        + "[Exam](https://example.edu/exam)\n\n"
        + "The assignments connect analysis to measurement. " * 30
    )

    issues = _validate_body(
        body,
        language="en",
        path=tmp_path / "singular-range.en.md",
        evidence_level="R0",
    )

    assert "guide.range_label_agreement" in {issue.code for issue in issues}


def test_course_guide_rejects_repeated_narrative_destination(
    tmp_path: Path,
) -> None:
    body = (
        "## Course judgment\n\n"
        + "This course is a useful first choice for a concrete circuit model. " * 12
        + "\n\n## Work\n\n"
        + "[Course](https://example.edu/course) "
        + "[Same course](https://example.edu/course/) "
        + "[Exam](https://example.edu/exam)\n\n"
        + "The official assignment and exam define the learning exit. " * 8
    )

    issues = _validate_body(
        body,
        language="en",
        path=tmp_path / "duplicate-link.en.md",
        evidence_level="R0",
    )

    assert "guide.duplicate_link" in {issue.code for issue in issues}


def test_course_guide_loader_rejects_reused_long_paragraph(
    tmp_path: Path,
    monkeypatch,
) -> None:
    guide_root = tmp_path / "content" / "course-guides"
    guide_root.mkdir(parents=True)
    monkeypatch.setattr(
        course_guides_module,
        "repo_path",
        lambda value: (
            Path(value)
            if Path(value).is_absolute()
            else tmp_path / Path(value)
        ),
    )
    repeated_zh = (
        "这段正文逐项比较课程版本、公开作业、反馈边界和实际学习顺序，"
        "并说明哪些结论来自提供方页面、哪些练习只是自学补充。"
    ) * 10
    repeated_en = (
        "This paragraph compares the course version, public assignments, feedback "
        "boundaries, and an actual study sequence while separating provider facts "
        "from independent-study supplements. "
    ) * 10
    distinct = {
        "001": ("第一门课的收束建议。", "Closing advice for the first course. "),
        "002": ("第二门课的收束建议。", "Closing advice for the second course. "),
    }
    records = []
    for course_id, (zh_tail, en_tail) in distinct.items():
        for language, paragraph, tail in (
            ("zh", repeated_zh, zh_tail),
            ("en", repeated_en, en_tail),
        ):
            body = (
                f"## 位置\n\n{paragraph}\n\n"
                "## 材料\n\n"
                "[课程](https://example.edu/course) "
                "[作业](https://example.edu/work) "
                "[考试](https://example.edu/exam)\n\n"
                f"## 收束\n\n{tail * 120}\n"
                if language == "zh"
                else (
                    f"## Position\n\n{paragraph}\n\n"
                    "## Material\n\n"
                    "[Course](https://example.edu/course) "
                    "[Work](https://example.edu/work) "
                    "[Exam](https://example.edu/exam)\n\n"
                    f"## Closing\n\n{tail * 120}\n"
                )
            )
            (guide_root / f"{course_id}.{language}.md").write_text(
                body,
                encoding="utf-8",
            )
        records.append(
            {
                "course_id": int(course_id),
                "editorial_status": "researched",
                "evidence_level": "R0",
                "reviewed_at": "2026-07-30",
                "files": {
                    "zh": f"content/course-guides/{course_id}.zh.md",
                    "en": f"content/course-guides/{course_id}.en.md",
                },
                "primary_sources": [
                    "https://example.edu/course",
                    "https://example.edu/work",
                ],
                "learner_reviews": [],
            }
        )
    manifest = tmp_path / "course-guides.json"
    manifest.write_text(
        json.dumps({"schema_version": 1, "guides": records}, ensure_ascii=False),
        encoding="utf-8",
    )
    schema = json.loads((ROOT / "data" / "course-guide.schema.json").read_text(encoding="utf-8"))
    schema_path = tmp_path / "course-guide.schema.json"
    schema_path.write_text(json.dumps(schema), encoding="utf-8")
    catalogue = {
        "courses": [
            {"source_id": 1},
            {"source_id": 2},
        ]
    }

    _, issues = load_course_guides(manifest, catalogue, schema_path)

    duplicated = [issue for issue in issues if issue.code == "guide.duplicate_paragraph"]
    assert len(duplicated) == 2
    assert {Path(issue.path).name for issue in duplicated} == {
        "002.zh.md",
        "002.en.md",
    }
