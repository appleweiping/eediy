from __future__ import annotations

import copy
import json
from datetime import date
from pathlib import Path

import pytest

from scripts.course_data import (
    catalogue_statistics,
    compile_catalogue,
    load_taxonomy,
    normalize_url,
    validate_candidates,
    validate_resource_manifest,
)
from scripts.validate_courses import semantic_issues


def test_normalize_url_preserves_embedded_wayback_target_scheme() -> None:
    assert normalize_url(
        "https://web.archive.org/web/20241219154359/https://cs61c.org/fa24/"
    ) == (
        "https://web.archive.org/web/20241219154359/"
        "https://cs61c.org/fa24"
    )


def test_normalize_url_still_collapses_ordinary_duplicate_path_slashes() -> None:
    assert normalize_url("HTTPS://Example.EDU//course///week-1/") == (
        "https://example.edu/course/week-1"
    )


def test_normalize_url_treats_mit_ocw_www_alias_as_the_same_provider() -> None:
    assert normalize_url(
        "https://www.ocw.mit.edu/courses/2-71-optics-spring-2014/pages/syllabus/"
    ) == (
        "https://ocw.mit.edu/courses/2-71-optics-spring-2014/pages/syllabus"
    )


def test_schema_requires_a_nonempty_evidence_backed_catalogue() -> None:
    schema = json.loads(Path("data/course.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["courses"]["minItems"] == 1
    assert schema["properties"]["tracks"]["minItems"] == 1
    required = set(schema["$defs"]["course"]["required"])
    assert {
        "prerequisite_course_ids",
        "official_prerequisites",
        "recommended_background",
        "resources",
    } <= required
    assert {
        "study_plan",
        "tooling",
        "safety",
        "completion_evidence",
        "projects",
    }.isdisjoint(schema["$defs"]["course"]["properties"])
    resource_required = set(schema["$defs"]["resource"]["required"])
    assert {"last_verified", "access", "license", "status"} <= resource_required
    assert schema["$defs"]["resource"]["properties"]["artifact_scope"]["enum"] == [
        "content",
        "index",
        "outline",
        "landing",
        "syllabus",
    ]


def test_compile_is_deterministic_and_drops_unsupported_generated_fields(
    candidate: dict, taxonomy_tracks: list[dict]
) -> None:
    first = compile_catalogue([candidate], taxonomy_tracks)
    existing = copy.deepcopy(first)
    existing["courses"][0]["summary"]["zh"] = "人工审阅后的课程摘要。"
    existing["courses"][0]["resources"][0]["license"] = "Verified course-specific terms"
    existing["courses"][0]["level"] = "mixed"
    existing["courses"][0]["projects"] = [{"title": "generated filler"}]
    existing["courses"][0]["study_plan"] = {"estimated_weeks": 12}
    second = compile_catalogue([candidate], taxonomy_tracks, existing)
    course = second["courses"][0]
    assert course["summary"]["zh"] == "人工审阅后的课程摘要。"
    assert course["resources"][0]["license"] == "Verified course-specific terms"
    assert course["level"] == "unspecified"
    assert "projects" not in course
    assert "study_plan" not in course
    assert "tooling" not in course
    assert "safety" not in course
    assert "completion_evidence" not in course
    assert course["last_reviewed"] == candidate["verified_at"]
    assert second == compile_catalogue([candidate], taxonomy_tracks, second)


def test_compile_refreshes_explicit_candidate_level(
    candidate: dict, taxonomy_tracks: list[dict]
) -> None:
    candidate["level"] = "advanced"
    existing = compile_catalogue([candidate], taxonomy_tracks)
    existing["courses"][0]["level"] = "mixed"

    refreshed = compile_catalogue([candidate], taxonomy_tracks, existing)

    assert refreshed["courses"][0]["level"] == "advanced"


def test_compile_adds_explicit_course_sequence_prerequisites(
    candidate: dict, taxonomy_tracks: list[dict]
) -> None:
    first = copy.deepcopy(candidate)
    first["title"] = "Sequence Course One"
    second = copy.deepcopy(candidate)
    second.update(
        {
            "id": 2,
            "title": "Sequence Course Two",
            "code": "EE-102",
            "url": "https://example.edu/courses/ee-102/",
            "prerequisite_course_ids": [1],
        }
    )

    catalogue = compile_catalogue([first, second], taxonomy_tracks)
    course = catalogue["courses"][1]
    prerequisites = course["prerequisites"]

    assert any("Sequence Course One" in item for item in prerequisites["zh"])
    assert any(
        item.startswith("Complete Sequence Course One")
        for item in prerequisites["en"]
    )
    assert any("Sequence Course One" in item for item in prerequisites["en"])
    assert course["recommended_background"] == {"zh": [], "en": []}
    assert course["official_prerequisites"] == prerequisites


def test_recommended_background_does_not_create_a_hard_course_edge(
    candidate: dict, taxonomy_tracks: list[dict]
) -> None:
    candidate["recommended_background"] = {
        "zh": "直流电路分析或同等基础",
        "en": "DC circuit analysis or equivalent background",
    }

    course = compile_catalogue([candidate], taxonomy_tracks)["courses"][0]

    assert course["prerequisite_course_ids"] == []
    assert course["official_prerequisites"] == {"zh": [], "en": []}
    assert any(
        "直流电路分析或同等基础" in item
        for item in course["recommended_background"]["zh"]
    )
    assert any(
        "DC circuit analysis or equivalent background" in item
        for item in course["prerequisites"]["en"]
    )


def test_course_can_separate_track_background_without_dropping_hard_edge(
    candidate: dict, taxonomy_tracks: list[dict]
) -> None:
    physics_track = copy.deepcopy(taxonomy_tracks[0])
    physics_track.update(
        {
            "id": "physics",
            "order": 5,
            "title_zh": "物理基础",
            "title_en": "Physics Foundations",
        }
    )
    taxonomy_tracks[0]["prerequisites"] = ["physics"]
    prerequisite = copy.deepcopy(candidate)
    prerequisite.update(
        {
            "id": 2,
            "title": "Required Physics",
            "code": "PHYS-100",
            "url": "https://example.edu/courses/phys-100/",
            "track": "physics",
        }
    )
    candidate["inherit_track_prerequisites"] = False
    candidate["prerequisite_course_ids"] = [2]
    candidate["recommended_background"] = {
        "zh": "本站路线建议的数学背景",
        "en": "Mathematical background recommended by this route",
    }
    candidate["prerequisite_note"] = {
        "zh": "提供方列出的正式先修",
        "en": "The provider's formal prerequisite",
    }

    course = compile_catalogue(
        [candidate, prerequisite],
        [physics_track, *taxonomy_tracks],
    )["courses"][0]

    assert course["prerequisite_course_ids"] == [2]
    assert not any(
        "物理基础" in item or "Physics Foundations" in item
        for language in ("zh", "en")
        for item in course["prerequisites"][language]
    )
    assert any("本站路线建议的数学背景" in item for item in course["prerequisites"]["zh"])
    assert any("提供方列出的正式先修" in item for item in course["prerequisites"]["zh"])
    assert any("Required Physics" in item for item in course["prerequisites"]["en"])
    assert all(
        "本站路线建议的数学背景" not in item
        and "Mathematical background recommended by this route" not in item
        for language in ("zh", "en")
        for item in course["official_prerequisites"][language]
    )
    assert all(
        "提供方列出的正式先修" not in item
        and "The provider's formal prerequisite" not in item
        for language in ("zh", "en")
        for item in course["recommended_background"][language]
    )


def test_candidate_validation_rejects_partial_recommended_background(
    candidate: dict,
) -> None:
    candidate["recommended_background"] = {"en": "Basic calculus"}

    issues = validate_candidates(
        [candidate],
        taxonomy_ids={"mathematics"},
    )

    assert any(issue.code == "candidate.recommended_background" for issue in issues)


def test_candidate_validation_rejects_partial_prerequisite_note(
    candidate: dict,
) -> None:
    candidate["prerequisite_note"] = {"en": "Either EE 101 or EE 102"}

    issues = validate_candidates(
        [candidate],
        taxonomy_ids={"mathematics"},
    )

    assert any(issue.code == "candidate.prerequisite_note" for issue in issues)


def test_candidate_validation_rejects_non_boolean_track_prerequisite_control(
    candidate: dict,
) -> None:
    candidate["inherit_track_prerequisites"] = "false"

    issues = validate_candidates(
        [candidate],
        taxonomy_ids={"mathematics"},
    )

    assert any(
        issue.code == "candidate.inherit_track_prerequisites" for issue in issues
    )


def test_mit_271_keeps_official_prerequisites_separate_from_track_advice() -> None:
    candidates = json.loads(
        Path("data/course_candidates.json").read_text(encoding="utf-8")
    )
    taxonomy_value = json.loads(Path("data/tracks.json").read_text(encoding="utf-8"))
    taxonomy_tracks, taxonomy_issues = load_taxonomy(taxonomy_value)
    assert [issue for issue in taxonomy_issues if issue.severity == "error"] == []

    candidate = next(item for item in candidates if item["id"] == 134)
    course = compile_catalogue([candidate], taxonomy_tracks)["courses"][0]
    prerequisites = " ".join(
        course["prerequisites"]["zh"] + course["prerequisites"]["en"]
    )
    optics_track = next(
        track for track in taxonomy_tracks if track["id"] == "optics-photonics"
    )

    assert candidate["inherit_track_prerequisites"] is False
    assert "8.02" in prerequisites
    assert "18.03" in prerequisites
    assert "2.004" in prerequisites
    assert "semiconductor" not in prerequisites.lower()
    assert "semiconductor-devices" in optics_track["prerequisites"]


def test_explicit_provider_prerequisites_do_not_fall_back_to_track_advice() -> None:
    candidates = json.loads(
        Path("data/course_candidates.json").read_text(encoding="utf-8")
    )
    taxonomy_value = json.loads(Path("data/tracks.json").read_text(encoding="utf-8"))
    taxonomy_tracks, taxonomy_issues = load_taxonomy(taxonomy_value)
    assert [issue for issue in taxonomy_issues if issue.severity == "error"] == []

    catalogue = compile_catalogue(candidates, taxonomy_tracks)
    candidate_by_id = {candidate["id"]: candidate for candidate in candidates}
    course_by_id = {course["source_id"]: course for course in catalogue["courses"]}

    representative_ids = {1, 39, 42, 57, 71, 108, 126, 139}
    for course_id in representative_ids:
        candidate = candidate_by_id[course_id]
        course = course_by_id[course_id]
        note = candidate["prerequisite_note"]

        assert candidate["inherit_track_prerequisites"] is False
        assert note["zh"] in " ".join(course["official_prerequisites"]["zh"])
        assert note["en"] in " ".join(course["official_prerequisites"]["en"])
        assert course["recommended_background"] == {"zh": [], "en": []}

    assert candidate_by_id[2]["prerequisite_course_ids"] == [1]
    assert candidate_by_id[33]["prerequisite_course_ids"] == [32, 67]
    assert candidate_by_id[66]["prerequisite_course_ids"] == [63, 64, 65]
    assert candidate_by_id[89]["prerequisite_course_ids"] == [98]
    for alternative_or_permission_id in (20, 104, 120, 125, 140):
        assert candidate_by_id[alternative_or_permission_id].get(
            "prerequisite_course_ids", []
        ) == []


def test_every_provider_note_is_kept_out_of_eediy_route_advice() -> None:
    candidates = json.loads(
        Path("data/course_candidates.json").read_text(encoding="utf-8")
    )
    taxonomy_value = json.loads(Path("data/tracks.json").read_text(encoding="utf-8"))
    taxonomy_tracks, taxonomy_issues = load_taxonomy(taxonomy_value)
    assert [issue for issue in taxonomy_issues if issue.severity == "error"] == []

    catalogue = compile_catalogue(candidates, taxonomy_tracks)
    course_by_id = {course["source_id"]: course for course in catalogue["courses"]}
    provider_records = [
        candidate for candidate in candidates if "prerequisite_note" in candidate
    ]

    assert len(provider_records) >= 80
    for candidate in provider_records:
        course = course_by_id[candidate["id"]]
        note = candidate["prerequisite_note"]

        assert candidate["inherit_track_prerequisites"] is False
        assert note["zh"] in " ".join(course["official_prerequisites"]["zh"])
        assert note["en"] in " ".join(course["official_prerequisites"]["en"])
        assert note["zh"] not in " ".join(course["recommended_background"]["zh"])
        assert note["en"] not in " ".join(course["recommended_background"]["en"])


def test_canonical_prerequisite_sections_do_not_repeat_their_own_field_labels() -> None:
    candidates = json.loads(
        Path("data/course_candidates.json").read_text(encoding="utf-8")
    )
    taxonomy_value = json.loads(Path("data/tracks.json").read_text(encoding="utf-8"))
    taxonomy_tracks, taxonomy_issues = load_taxonomy(taxonomy_value)
    assert [issue for issue in taxonomy_issues if issue.severity == "error"] == []

    catalogue = compile_catalogue(candidates, taxonomy_tracks)
    redundant_prefixes = (
        "官方先修说明：",
        "Official prerequisite note:",
        "建议背景：",
        "Recommended background:",
        "建议先完成方向基础：",
        "Recommended foundation:",
    )
    for course in catalogue["courses"]:
        for field in ("official_prerequisites", "recommended_background"):
            for language in ("zh", "en"):
                assert not any(
                    item.startswith(redundant_prefixes)
                    for item in course[field][language]
                )


def test_recommended_sequences_and_equivalent_background_do_not_become_hard_edges() -> None:
    candidates = json.loads(
        Path("data/course_candidates.json").read_text(encoding="utf-8")
    )
    candidate_by_id = {candidate["id"]: candidate for candidate in candidates}

    for course_id in range(78, 83):
        candidate = candidate_by_id[course_id]
        assert candidate.get("prerequisite_course_ids", []) == []
        assert "highly recommended" in candidate["prerequisite_note"]["en"]
        assert candidate["recommended_background"]["en"]

    six_011 = candidate_by_id[98]
    assert six_011.get("prerequisite_course_ids", []) == []
    assert "or equivalents" in six_011["prerequisite_note"]["en"]
    assert "not themselves mandatory" in six_011["recommended_background"]["en"]


def test_provider_prerequisites_keep_eediy_preparation_in_a_separate_field() -> None:
    candidates = json.loads(
        Path("data/course_candidates.json").read_text(encoding="utf-8")
    )
    candidate_by_id = {candidate["id"]: candidate for candidate in candidates}

    for course_id in (4, 5, 21, 123, 128):
        candidate = candidate_by_id[course_id]
        official = candidate["prerequisite_note"]
        recommended = candidate["recommended_background"]

        assert "EEDIY" not in official["en"]
        assert "本站" not in official["zh"]
        assert "EEDIY" in recommended["en"]
        assert "本站" in recommended["zh"]


def test_current_cornell_roster_and_mit_equivalence_clauses_are_preserved() -> None:
    guide_manifest = json.loads(
        Path("data/course_guides.json").read_text(encoding="utf-8")
    )
    guide_by_id = {
        record["course_id"]: record for record in guide_manifest["guides"]
    }
    cornell_source = "https://classes.cornell.edu/browse/roster/FA26/class/ECE/3030"

    assert cornell_source in guide_by_id[107]["primary_sources"]
    assert guide_by_id[107]["reviewed_at"] == "2026-07-31"
    for language in ("zh", "en"):
        cornell_guide = Path(f"content/course-guides/107.{language}.md").read_text(
            encoding="utf-8"
        )
        mit_guide = Path(f"content/course-guides/108.{language}.md").read_text(
            encoding="utf-8"
        )
        assert cornell_source in cornell_guide
        assert (
            "or equivalent" in mit_guide
            if language == "en"
            else "或同等背景" in mit_guide
        )


@pytest.mark.parametrize(
    ("prerequisite_ids", "issue_code"),
    [
        ([1], "candidate.prerequisite_course_self"),
        ([999], "candidate.prerequisite_course_missing"),
        ([2, 2], "candidate.prerequisite_course_ids_duplicate"),
    ],
)
def test_candidate_validation_rejects_invalid_course_prerequisite_ids(
    candidate: dict,
    prerequisite_ids: list[int],
    issue_code: str,
) -> None:
    candidate["prerequisite_course_ids"] = prerequisite_ids

    issues = validate_candidates(
        [candidate],
        taxonomy_ids={"mathematics"},
    )

    assert any(issue.code == issue_code for issue in issues)


def test_candidate_validation_rejects_course_prerequisite_cycle(
    candidate: dict,
) -> None:
    first = copy.deepcopy(candidate)
    first["prerequisite_course_ids"] = [2]
    second = copy.deepcopy(candidate)
    second.update(
        {
            "id": 2,
            "code": "EE-102",
            "url": "https://example.edu/courses/ee-102/",
            "prerequisite_course_ids": [1],
        }
    )

    issues = validate_candidates(
        [first, second],
        taxonomy_ids={"mathematics"},
    )

    assert any(issue.code == "candidate.prerequisite_course_cycle" for issue in issues)


def test_manifest_refreshes_primary_and_old_available_cannot_mask_review_needed(
    candidate: dict, taxonomy_tracks: list[dict]
) -> None:
    candidate["alternate_urls"] = ["https://example.edu/courses/ee-101/archive"]
    existing = compile_catalogue([candidate], taxonomy_tracks)
    existing["courses"][0]["title"] = {
        "zh": "错误的旧课程身份",
        "en": "Incorrect old course identity",
    }
    existing["courses"][0]["course_code"] = "STALE-001"
    primary = existing["courses"][0]["resources"][0]
    primary["status"] = "available"
    primary["access"] = "open"
    primary["last_verified"] = "2025-01-01"
    primary["title"] = {"zh": "旧标题", "en": "Old title"}
    alternate = existing["courses"][0]["resources"][1]
    alternate["title"] = {"zh": "旧备用标题", "en": "Old alternate title"}
    manifest = [
        {
            "course_id": candidate["id"],
            "kind": "course",
            "title": "Current official overview",
            "url": candidate["url"] + "/",
            "access": "open-registration",
            "status": "review-needed",
            "last_verified": "2026-07-28",
            "artifact_scope": "landing",
        },
        {
            "course_id": candidate["id"],
            "kind": "course",
            "title": "Stale alternate crawl title",
            "url": candidate["alternate_urls"][0],
            "access": "open",
            "status": "archived",
            "last_verified": "2026-07-28",
        },
    ]

    refreshed = compile_catalogue(
        [candidate],
        taxonomy_tracks,
        existing,
        resource_records=manifest,
    )
    refreshed_primary = refreshed["courses"][0]["resources"][0]
    assert refreshed["courses"][0]["title"] == {
        "zh": candidate["title"],
        "en": candidate["title"],
    }
    assert refreshed["courses"][0]["course_code"] == candidate["code"]
    assert refreshed_primary["id"] == "primary"
    assert refreshed_primary["status"] == "review-needed"
    assert refreshed_primary["access"] == "open-registration"
    assert refreshed_primary["last_verified"] == "2026-07-28"
    assert refreshed_primary["artifact_scope"] == "landing"
    assert refreshed_primary["title"] == {
        "zh": "课程主页",
        "en": "Course home",
    }
    refreshed_alternate = refreshed["courses"][0]["resources"][1]
    assert refreshed_alternate["id"] == "alternate-1"
    assert refreshed_alternate["status"] == "archived"
    assert refreshed_alternate["title"] == {
        "zh": "备用课程入口",
        "en": "Alternate course entry",
    }
    assert refreshed == compile_catalogue(
        [candidate],
        taxonomy_tracks,
        refreshed,
        resource_records=manifest,
    )


def test_resource_manifest_rejects_unknown_artifact_scope() -> None:
    records = [
        {
            "course_id": 1,
            "kind": "assignments",
            "title": "Homework index",
            "url": "https://example.edu/homework",
            "access": "open",
            "status": "available",
            "last_verified": "2026-07-31",
            "artifact_scope": "link-list",
        }
    ]

    valid, issues = validate_resource_manifest(records, candidate_ids={1})

    assert valid == []
    assert [issue.code for issue in issues] == [
        "resource_manifest.artifact_scope"
    ]


@pytest.mark.parametrize("superseded_status", ["review-needed", "archived"])
def test_compile_drops_superseded_seed_after_primary_url_changes(
    candidate: dict,
    taxonomy_tracks: list[dict],
    superseded_status: str,
) -> None:
    old_url = candidate["url"]
    existing = compile_catalogue([candidate], taxonomy_tracks)
    candidate["url"] = "https://example.edu/courses/ee-101-current"
    manifest = [
        {
            "course_id": candidate["id"],
            "kind": "course",
            "title": "Superseded official overview",
            "url": old_url,
            "source_url": old_url,
            "access": "open",
            "status": superseded_status,
            "last_verified": "2026-07-28",
        }
    ]

    refreshed = compile_catalogue(
        [candidate],
        taxonomy_tracks,
        existing,
        resource_records=manifest,
    )

    assert [resource["url"] for resource in refreshed["courses"][0]["resources"]] == [
        candidate["url"]
    ]
    assert refreshed == compile_catalogue(
        [candidate],
        taxonomy_tracks,
        refreshed,
        resource_records=manifest,
    )


def test_compile_drops_stale_generated_resource_but_preserves_curated_resource(
    candidate: dict, taxonomy_tracks: list[dict]
) -> None:
    existing = compile_catalogue([candidate], taxonomy_tracks)
    generated_resource = {
        "id": "course-10dc8d8c83",
        "kind": "course",
        "title": {"zh": "失效占位资源", "en": "Stale placeholder"},
        "url": "https://example.edu/undefined.pdf",
        "access": "open",
        "license": "Provider-specific terms",
        "status": "archived",
        "last_verified": "2026-07-28",
        "note": {"zh": "旧生成记录。", "en": "Old generated record."},
    }
    curated_resource = {
        **generated_resource,
        "id": "maintainer-curated-simulator",
        "title": {"zh": "维护者核对资源", "en": "Maintainer-reviewed resource"},
        "url": "https://example.edu/simulator",
        "status": "available",
    }
    existing["courses"][0]["resources"].extend(
        [generated_resource, curated_resource]
    )

    refreshed = compile_catalogue([candidate], taxonomy_tracks, existing)
    urls = {resource["url"] for resource in refreshed["courses"][0]["resources"]}

    assert generated_resource["url"] not in urls
    assert curated_resource["url"] in urls


def test_compile_keeps_unavailable_supplement_in_evidence_only(
    candidate: dict, taxonomy_tracks: list[dict]
) -> None:
    dead_url = "https://example.edu/retired-video"
    manifest = [
        {
            "course_id": candidate["id"],
            "kind": "video",
            "title": "Retired video index",
            "url": dead_url,
            "source_url": candidate["url"],
            "access": "open",
            "status": "unavailable",
            "last_verified": "2026-07-28",
        }
    ]

    refreshed = compile_catalogue(
        [candidate],
        taxonomy_tracks,
        resource_records=manifest,
    )

    assert dead_url not in {
        resource["url"] for resource in refreshed["courses"][0]["resources"]
    }


def test_candidate_gate_rejects_bad_coverage_and_unknown_track(candidate: dict) -> None:
    candidate["resources"]["labs"] = 3
    candidate["track"] = "not-a-track"
    issues = validate_candidates(
        [candidate],
        taxonomy_ids={"mathematics"},
    )
    codes = {issue.code for issue in issues}
    assert "candidate.coverage_score" in codes
    assert "candidate.track" in codes


def test_semantic_gate_requires_resource_metadata(catalogue: dict) -> None:
    del catalogue["courses"][0]["resources"][0]["license"]
    issues = semantic_issues(
        catalogue,
        maximum_age_days=400,
        today=date(2026, 7, 29),
    )
    assert any(issue.code == "resource.metadata" for issue in issues)


def test_semantic_gate_rejects_zero_coverage_with_matching_published_resource(
    catalogue: dict,
) -> None:
    course = catalogue["courses"][0]
    course["resource_coverage"]["video"] = 0
    course["resources"][0]["kind"] = "video"
    issues = semantic_issues(
        catalogue,
        maximum_age_days=400,
        today=date(2026, 7, 29),
    )

    assert any(issue.code == "resource.coverage_kind_conflict" for issue in issues)


def test_semantic_gate_requires_machine_evidence_for_code_coverage_two(
    catalogue: dict,
) -> None:
    catalogue["courses"][0]["resource_coverage"]["code"] = 2
    issues = semantic_issues(
        catalogue,
        maximum_age_days=400,
        today=date(2026, 7, 29),
    )

    assert any(issue.code == "resource.code_coverage_evidence" for issue in issues)


def test_semantic_gate_rejects_video_misclassified_as_code(catalogue: dict) -> None:
    resource = catalogue["courses"][0]["resources"][0]
    resource["kind"] = "code"
    resource["url"] = "https://www.youtube.com/watch?v=verilog"
    issues = semantic_issues(
        catalogue,
        maximum_age_days=400,
        today=date(2026, 7, 29),
    )

    assert any(issue.code == "resource.kind_host_conflict" for issue in issues)


def test_semantic_gate_rejects_open_access_for_restricted_target(
    catalogue: dict,
) -> None:
    resource = catalogue["courses"][0]["resources"][0]
    resource["url"] = "https://example.edu/course/secure/lab.zip"
    resource["access"] = "open"
    issues = semantic_issues(
        catalogue,
        maximum_age_days=400,
        today=date(2026, 7, 29),
    )

    assert any(issue.code == "resource.access_wall" for issue in issues)


def test_semantic_gate_accepts_evidence_backed_catalogue(
    catalogue: dict,
) -> None:
    issues = semantic_issues(
        catalogue,
        maximum_age_days=400,
        today=date(2026, 7, 29),
    )
    errors = [issue for issue in issues if issue.severity == "error"]
    assert errors == []
    statistics = catalogue_statistics(catalogue)
    assert statistics["resource_metadata_percent"] == 100.0
