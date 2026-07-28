from __future__ import annotations

import copy
import json
from datetime import date
from pathlib import Path

import pytest

from scripts.course_data import (
    TRACK_TOOLING,
    catalogue_statistics,
    compile_catalogue,
    validate_candidates,
)
from scripts.validate_courses import semantic_issues


def test_schema_encodes_release_thresholds() -> None:
    schema = json.loads(Path("data/course.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["courses"]["minItems"] == 125
    assert schema["properties"]["tracks"]["minItems"] == 24
    required = set(schema["$defs"]["course"]["required"])
    assert {
        "study_plan",
        "tooling",
        "safety",
        "prerequisite_course_ids",
        "completion_evidence",
        "resources",
    } <= required
    resource_required = set(schema["$defs"]["resource"]["required"])
    assert {"last_verified", "access", "license", "status"} <= resource_required


def test_compile_is_deterministic_and_preserves_manual_enrichment(
    candidate: dict, taxonomy_tracks: list[dict]
) -> None:
    first = compile_catalogue([candidate], taxonomy_tracks)
    existing = copy.deepcopy(first)
    existing["courses"][0]["summary"]["zh"] = "人工审阅后的课程摘要。"
    existing["courses"][0]["resources"][0]["license"] = "Verified course-specific terms"
    existing["courses"][0]["level"] = "mixed"
    existing["courses"][0]["projects"] = [
        {
            "title": {"zh": "验证项目", "en": "Verification project"},
            "brief": {"zh": "构建并验证。", "en": "Build and verify."},
            "origin": "suggested",
            "deliverables": {"zh": ["报告"], "en": ["Report"]},
            "verification": {"zh": ["自动检查"], "en": ["Automated check"]},
            "reproducibility": {
                "zh": ["固定版本并提供运行步骤"],
                "en": ["Pin versions and provide run steps"],
            },
            "safety_level": "simulation-only",
            "safety_note": {
                "zh": "仅使用仿真，不连接实体电源。",
                "en": "Use simulation only; do not connect physical power.",
            },
        }
    ]
    second = compile_catalogue([candidate], taxonomy_tracks, existing)
    course = second["courses"][0]
    assert course["summary"]["zh"] == "人工审阅后的课程摘要。"
    assert course["resources"][0]["license"] == "Verified course-specific terms"
    assert course["projects"][0]["title"]["en"] == "Verification project"
    assert course["level"] == "unspecified"
    assert course["study_plan"]["estimated_weeks"] > 0
    assert course["study_plan"]["hours_per_week"] > 0
    assert "not a provider workload promise" in course["study_plan"]["note"]["en"]
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


def test_provider_workload_with_fixed_weekly_hours_uses_singular_value(
    candidate: dict, taxonomy_tracks: list[dict]
) -> None:
    candidate["workload"] = {
        "weeks": 2,
        "hours_per_week": {"min": 10, "max": 10},
    }

    course = compile_catalogue([candidate], taxonomy_tracks)["courses"][0]
    note = course["study_plan"]["note"]

    assert course["study_plan"]["hours_per_week"] == 10
    assert "10–10" not in note["zh"]
    assert "10–10" not in note["en"]
    assert "每周 10 小时" in note["zh"]
    assert "10 hours per week" in note["en"]


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
    prerequisites = catalogue["courses"][1]["prerequisites"]

    assert any("Sequence Course One" in item for item in prerequisites["zh"])
    assert any("Course-sequence requirement" in item for item in prerequisites["en"])
    assert any("Sequence Course One" in item for item in prerequisites["en"])


def test_recommended_background_does_not_create_a_hard_course_edge(
    candidate: dict, taxonomy_tracks: list[dict]
) -> None:
    candidate["recommended_background"] = {
        "zh": "直流电路分析或同等基础",
        "en": "DC circuit analysis or equivalent background",
    }

    course = compile_catalogue([candidate], taxonomy_tracks)["courses"][0]

    assert course["prerequisite_course_ids"] == []
    assert any("直流电路分析或同等基础" in item for item in course["prerequisites"]["zh"])
    assert any(
        "DC circuit analysis or equivalent background" in item
        for item in course["prerequisites"]["en"]
    )


def test_candidate_validation_rejects_partial_recommended_background(
    candidate: dict,
) -> None:
    candidate["recommended_background"] = {"en": "Basic calculus"}

    issues = validate_candidates(
        [candidate],
        minimum_courses=1,
        minimum_tracks=1,
        taxonomy_ids={"mathematics"},
    )

    assert any(issue.code == "candidate.recommended_background" for issue in issues)


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
        minimum_courses=1,
        minimum_tracks=1,
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
        minimum_courses=1,
        minimum_tracks=1,
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


def test_compile_drops_superseded_failed_seed_after_primary_url_changes(
    candidate: dict, taxonomy_tracks: list[dict]
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
            "status": "review-needed",
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


def _compile_for_track(
    candidate: dict,
    track_id: str,
    *,
    labs: int,
    code: int,
) -> dict:
    track_candidate = copy.deepcopy(candidate)
    track_candidate["track"] = track_id
    track_candidate["resources"]["labs"] = labs
    track_candidate["resources"]["code"] = code
    track = {
        "id": track_id,
        "group": "test-group",
        "order": 1,
        "title_zh": track_id,
        "title_en": track_id,
        "summary_zh": f"{track_id} 测试方向。",
        "summary_en": f"Test track for {track_id}.",
        "prerequisites": [],
    }
    return compile_catalogue([track_candidate], [track])["courses"][0]


def test_tooling_profiles_cover_every_canonical_track() -> None:
    taxonomy = json.loads(Path("data/tracks.json").read_text(encoding="utf-8"))
    track_ids = {track["id"] for track in taxonomy["tracks"]}

    assert len(track_ids) == 35
    assert set(TRACK_TOOLING) == track_ids
    assert {
        mode
        for profile in TRACK_TOOLING.values()
        for mode in profile["evidence"]
    } <= {"theory", "simulation", "code", "experiment", "design"}


@pytest.mark.parametrize(
    ("track_id", "labs", "code", "software_token", "hardware_token"),
    [
        ("mathematics", 0, 0, "sympy", "no dedicated physical hardware"),
        ("circuits", 2, 0, "ngspice", "oscilloscope"),
        ("analog-ic", 0, 0, "xschem", "no tape-out"),
        ("fpga-soc", 2, 2, "yosys", "fpga development board"),
        ("embedded-systems", 2, 2, "openocd", "microcontroller development board"),
        ("control-systems", 1, 1, "python-control", "real-time controller"),
        ("robotics", 2, 2, "ros 2", "robot platform"),
        ("power-systems-machines", 1, 1, "pandapower", "three-phase"),
        ("energy-storage-pv", 1, 1, "pvlib-python", "pv/battery"),
        ("communications", 1, 1, "gnu radio", "software-defined radio"),
        ("rf-microwave-antennas", 2, 1, "scikit-rf", "vector network analyzer"),
    ],
)
def test_typical_tracks_get_specific_honest_tooling(
    candidate: dict,
    track_id: str,
    labs: int,
    code: int,
    software_token: str,
    hardware_token: str,
) -> None:
    course = _compile_for_track(candidate, track_id, labs=labs, code=code)
    software = "\n".join(course["tooling"]["software"]["en"]).lower()
    hardware = "\n".join(course["tooling"]["hardware"]["en"]).lower()
    cost_note = course["tooling"]["cost_note"]["en"].lower()

    assert software_token in software
    assert hardware_token in hardware
    assert "maintainer-suggested" in software
    assert "not a provider" in cost_note
    assert "requirement" in cost_note
    assert "provider" in cost_note
    assert "region" in cost_note


def test_typical_track_tooling_is_not_one_reused_template(candidate: dict) -> None:
    cases = [
        ("mathematics", 0, 0),
        ("circuits", 2, 0),
        ("analog-ic", 0, 0),
        ("fpga-soc", 2, 2),
        ("embedded-systems", 2, 2),
        ("control-systems", 1, 1),
        ("robotics", 2, 2),
        ("power-systems-machines", 1, 1),
        ("energy-storage-pv", 1, 1),
        ("communications", 1, 1),
        ("rf-microwave-antennas", 2, 1),
    ]
    suggested_paths = {
        _compile_for_track(candidate, track_id, labs=labs, code=code)["tooling"][
            "software"
        ]["en"][0]
        for track_id, labs, code in cases
    }

    assert len(suggested_paths) == len(cases)


def test_resource_coverage_controls_hardware_and_evidence(candidate: dict) -> None:
    simulation_only = _compile_for_track(
        candidate, "circuits", labs=0, code=0
    )
    practical = _compile_for_track(candidate, "circuits", labs=2, code=1)
    no_lab_hardware = simulation_only["tooling"]["hardware"]["en"][0]
    lab_hardware = practical["tooling"]["hardware"]["en"][0]
    simulation_evidence = "\n".join(
        simulation_only["completion_evidence"]["en"]
    )
    practical_evidence = "\n".join(practical["completion_evidence"]["en"])

    assert "does not list public lab coverage" in no_lab_hardware
    assert "do not purchase" in no_lab_hardware
    assert "lists lab coverage" in lab_hardware
    assert "borrowing or sharing" in lab_hardware
    assert "Experiment package" not in simulation_evidence
    assert "Code repository" not in simulation_evidence
    assert "Experiment package" in practical_evidence
    assert "Code repository" in practical_evidence


def test_compute_labs_remain_simulation_only(candidate: dict) -> None:
    course = _compile_for_track(
        candidate, "programming-tools", labs=2, code=2
    )
    hardware = "\n".join(course["tooling"]["hardware"]["en"]).lower()
    evidence = "\n".join(course["completion_evidence"]["en"])

    assert course["safety"]["level"] == "simulation-only"
    assert "computational/simulation work" in hardware
    assert "Experiment package" not in evidence
    assert "Simulation package" in evidence
    assert "Code repository" in evidence


def test_explicit_simulation_modality_overrides_robotics_lab_score(
    candidate: dict,
) -> None:
    candidate["practice_modality"] = "simulation-only"
    course = _compile_for_track(candidate, "robotics", labs=2, code=2)
    hardware = "\n".join(course["tooling"]["hardware"]["en"]).lower()
    evidence = "\n".join(course["completion_evidence"]["en"])

    assert course["safety"]["level"] == "simulation-only"
    assert "do not purchase or connect" in hardware
    assert "robot platform" in hardware
    assert "Experiment package" not in evidence
    assert "Simulation package" in evidence


def test_biomedical_hardware_guidance_is_safe_and_grammatical(candidate: dict) -> None:
    simulation_only = _compile_for_track(candidate, "biomedical", labs=0, code=1)
    practical = _compile_for_track(candidate, "biomedical", labs=2, code=1)

    simulation_zh = simulation_only["tooling"]["hardware"]["zh"][0]
    simulation_en = simulation_only["tooling"]["hardware"]["en"][0]
    practical_zh = practical["tooling"]["hardware"]["zh"][0]
    practical_en = practical["tooling"]["hardware"]["en"][0]

    assert "不采购优先使用" not in simulation_zh
    assert "do not purchase prefer" not in simulation_en
    assert "借用或共享优先使用" not in practical_zh
    assert "borrowed equipment: prefer" not in practical_en
    assert "去标识公开数据或信号模拟器" in simulation_zh
    assert "de-identified public data or a signal simulator" in simulation_en
    assert "伦理与安全审查" in practical_zh
    assert "ethics and safety review" in practical_en


def test_completion_evidence_distinguishes_five_reproducible_artifact_types(
    candidate: dict,
) -> None:
    theory_course = _compile_for_track(
        candidate, "mathematics", labs=0, code=0
    )
    design_course = _compile_for_track(
        candidate, "fpga-soc", labs=2, code=2
    )
    evidence = "\n".join(
        theory_course["completion_evidence"]["en"]
        + design_course["completion_evidence"]["en"]
    )

    assert "Theory dossier" in evidence
    assert "Simulation package" in evidence
    assert "Code repository" in evidence
    assert "Experiment package" in evidence
    assert "Design-review package" in evidence
    assert "rerun command" in evidence
    assert "raw data" in evidence
    assert "editable sources" in evidence


def test_candidate_gate_rejects_bad_coverage_and_unknown_track(candidate: dict) -> None:
    candidate["resources"]["labs"] = 3
    candidate["track"] = "not-a-track"
    issues = validate_candidates(
        [candidate],
        minimum_courses=1,
        minimum_tracks=1,
        taxonomy_ids={"mathematics"},
    )
    codes = {issue.code for issue in issues}
    assert "candidate.coverage_score" in codes
    assert "candidate.track" in codes


def test_candidate_gate_rejects_unknown_practice_modality(candidate: dict) -> None:
    candidate["practice_modality"] = "wet-lab"

    issues = validate_candidates(
        [candidate],
        minimum_courses=1,
        minimum_tracks=1,
        taxonomy_ids={"mathematics"},
    )

    assert any(issue.code == "candidate.practice_modality" for issue in issues)


def test_semantic_gate_requires_resource_metadata(catalogue: dict) -> None:
    del catalogue["courses"][0]["resources"][0]["license"]
    issues = semantic_issues(
        catalogue,
        minimum_courses=1,
        minimum_used_tracks=1,
        minimum_unique_resources=1,
        minimum_project_courses=0,
        maximum_age_days=400,
        today=date(2026, 7, 29),
    )
    assert any(issue.code == "resource.metadata" for issue in issues)


def test_semantic_gate_accepts_maintainer_workload_with_provenance(
    catalogue: dict,
) -> None:
    issues = semantic_issues(
        catalogue,
        minimum_courses=1,
        minimum_used_tracks=1,
        minimum_unique_resources=1,
        minimum_project_courses=0,
        maximum_age_days=400,
        today=date(2026, 7, 29),
    )
    errors = [issue for issue in issues if issue.severity == "error"]
    assert errors == []
    statistics = catalogue_statistics(catalogue)
    assert statistics["resource_metadata_percent"] == 100.0


def test_semantic_gate_rejects_unexplained_workload(catalogue: dict) -> None:
    catalogue["courses"][0]["study_plan"]["note"] = {
        "zh": "请自行安排。",
        "en": "Choose a schedule.",
    }
    issues = semantic_issues(
        catalogue,
        minimum_courses=1,
        minimum_used_tracks=1,
        minimum_unique_resources=1,
        minimum_project_courses=0,
        today=date(2026, 7, 29),
    )
    assert any(issue.code == "course.workload_provenance_missing" for issue in issues)
    assert any(issue.code == "course.workload_calibration_missing" for issue in issues)
