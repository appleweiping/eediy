from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping

from scripts.apply_project_templates import (
    HIGH_RISK_TRACKS,
    LOW_ENERGY_TRACKS,
    apply_project_templates,
    validate_project_templates,
)
from scripts.quality_common import load_json, stable_json


def _inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    catalogue = load_json(Path("data/courses.json"))
    templates = load_json(Path("data/project_templates.json"))
    taxonomy = load_json(Path("data/tracks.json"))
    return catalogue, templates, taxonomy


def test_templates_cover_all_tracks_with_unique_track_specific_content() -> None:
    _, templates, taxonomy = _inputs()
    issues = validate_project_templates(templates, taxonomy)
    assert [issue for issue in issues if issue.severity == "error"] == []

    expected_tracks = {track["id"] for track in taxonomy["tracks"]}
    template_tracks = [template["track"] for template in templates["templates"]]
    assert len(template_tracks) == 35
    assert len(set(template_tracks)) == 35
    assert set(template_tracks) == expected_tracks

    # A shared evidence structure is intentional, but the actual engineering
    # system, metrics, and failure study must remain track-specific.
    fingerprints = {
        (
            template["title"]["en"],
            template["brief"]["en"],
            tuple(template["verification"]["en"]),
        )
        for template in templates["templates"]
    }
    assert len(fingerprints) == len(template_tracks)


def test_every_template_has_bilingual_execution_and_evidence_depth() -> None:
    _, templates, _ = _inputs()
    for template in templates["templates"]:
        for field in ("title", "brief", "safety_note"):
            assert set(template[field]) == {"zh", "en"}
            assert all(template[field][language].strip() for language in ("zh", "en"))
        for field, minimum in (
            ("deliverables", 4),
            ("verification", 4),
            ("reproducibility", 3),
        ):
            assert set(template[field]) == {"zh", "en"}
            assert len(template[field]["zh"]) == len(template[field]["en"])
            assert len(template[field]["zh"]) >= minimum
        english_evidence = " ".join(
            item
            for field in ("deliverables", "verification", "reproducibility")
            for item in template[field]["en"]
        ).casefold()
        assert "source" in english_evidence
        assert "raw" in english_evidence
        assert "report" in english_evidence
        assert any(
            token in english_evidence
            for token in ("pin ", "pinned", "version", "environment")
        )


def test_application_is_deterministic_contextual_and_non_mutating() -> None:
    catalogue, templates, taxonomy = _inputs()
    original = copy.deepcopy(catalogue)
    first, first_issues = apply_project_templates(catalogue, templates, taxonomy)
    assert [issue for issue in first_issues if issue.severity == "error"] == []
    assert first is not None
    assert catalogue == original

    second, second_issues = apply_project_templates(first, templates, taxonomy)
    assert [issue for issue in second_issues if issue.severity == "error"] == []
    assert second is not None
    assert stable_json(first) == stable_json(second)

    track_titles = {
        track["id"]: {"zh": track["title_zh"], "en": track["title_en"]}
        for track in taxonomy["tracks"]
    }
    assert len(first["courses"]) == len(original["courses"])
    rendered_fingerprints: set[tuple[str, tuple[str, ...]]] = set()
    for course in first["courses"]:
        assert len(course["projects"]) == 1
        project = course["projects"][0]
        assert project["origin"] == "suggested"
        for language in ("zh", "en"):
            course_title = course["title"][language]
            assert course_title in project["title"][language]
            assert course_title in project["brief"][language]
            assert track_titles[course["track"]][language] in project["brief"][language]
        assert "不是课程官方作业" in project["brief"]["zh"]
        assert "not an official course assignment" in project["brief"]["en"].casefold()
        rendered_fingerprints.add(
            (project["brief"]["en"], tuple(project["verification"]["en"]))
        )
    assert len(rendered_fingerprints) == len(first["courses"])


def test_project_safety_policy_is_explicit_and_conservative() -> None:
    catalogue, templates, taxonomy = _inputs()
    result, issues = apply_project_templates(catalogue, templates, taxonomy)
    assert [issue for issue in issues if issue.severity == "error"] == []
    assert result is not None

    projects_by_track: dict[str, list[Mapping[str, Any]]] = {}
    for course in result["courses"]:
        projects_by_track.setdefault(course["track"], []).extend(course["projects"])

    for track in HIGH_RISK_TRACKS:
        assert {
            project["safety_level"] for project in projects_by_track[track]
        } <= {"simulation-only", "supervised"}
    for track in LOW_ENERGY_TRACKS:
        for project in projects_by_track[track]:
            assert project["safety_level"] == "low-energy"
            assert all(
                token in project["safety_note"]["zh"] for token in ("限流", "额定值", "断电")
            )
            english = project["safety_note"]["en"].casefold()
            assert "current-limit" in english
            assert "rating" in english
            assert "power removed" in english

    for project in projects_by_track["biomedical"]:
        combined = " ".join(project["safety_note"].values()).casefold()
        assert all(
            token in combined
            for token in ("公开", "合成", "public", "synthetic", "人体", "human")
        )
        assert project["safety_level"] == "simulation-only"


def test_validation_rejects_generic_duplicate_and_unsafe_high_risk_template() -> None:
    _, templates, taxonomy = _inputs()
    broken = copy.deepcopy(templates)
    by_track = {template["track"]: template for template in broken["templates"]}
    by_track["power-electronics"]["safety_level"] = "low-energy"
    by_track["probability-statistics"]["brief"] = copy.deepcopy(
        by_track["mathematics"]["brief"]
    )
    issues = validate_project_templates(broken, taxonomy)
    codes = {issue.code for issue in issues}
    assert "project_template.high_risk" in codes
    assert "project_template.generic_duplicate" in codes
