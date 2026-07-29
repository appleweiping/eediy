from __future__ import annotations

import copy
import json
import re
from pathlib import Path

from scripts.apply_course_editorial import apply_editorial, main, validate_editorial
from scripts.course_data import compile_catalogue, load_taxonomy


def _load_inputs() -> tuple[list[dict], list[dict], dict]:
    candidates = json.loads(
        Path("data/course_candidates.json").read_text(encoding="utf-8")
    )
    editorial = json.loads(
        Path("data/course_editorial.json").read_text(encoding="utf-8")
    )
    catalogue = json.loads(Path("data/courses.json").read_text(encoding="utf-8"))
    return candidates, editorial, catalogue


def test_editorial_has_exact_unique_bilingual_coverage() -> None:
    candidates, editorial, _ = _load_inputs()
    assert validate_editorial(editorial, candidates) == []
    assert [entry["source_id"] for entry in editorial] == [
        candidate["id"] for candidate in candidates
    ]
    assert len({entry["summary"]["zh"] for entry in editorial}) == len(candidates)
    assert len({entry["summary"]["en"] for entry in editorial}) == len(candidates)
    assert all(
        re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", entry["review_note"]["zh"])
        for entry in editorial
    )


def test_editorial_gate_rejects_missing_duplicate_and_untranslated_notes() -> None:
    candidates, editorial, _ = _load_inputs()
    broken = copy.deepcopy(editorial)
    broken.pop()
    broken[1]["source_id"] = broken[0]["source_id"]
    broken[2]["review_note"]["zh"] = broken[2]["review_note"]["en"]
    codes = {issue.code for issue in validate_editorial(broken, candidates)}
    assert "editorial.duplicate_id" in codes
    assert "editorial.coverage_missing" in codes
    assert "editorial.coverage_count" in codes
    assert "editorial.identical_translation" in codes
    assert "editorial.review_note_chinese" in codes


def test_apply_is_deterministic_and_compile_preserves_editorial() -> None:
    candidates, editorial, catalogue = _load_inputs()
    applied, issues = apply_editorial(catalogue, editorial, candidates)
    assert issues == []
    assert applied is not None
    applied_again, second_issues = apply_editorial(applied, editorial, candidates)
    assert second_issues == []
    assert applied_again == applied

    taxonomy_value = json.loads(Path("data/tracks.json").read_text(encoding="utf-8"))
    taxonomy_tracks, taxonomy_issues = load_taxonomy(taxonomy_value)
    assert [issue for issue in taxonomy_issues if issue.severity == "error"] == []
    recompiled = compile_catalogue(candidates, taxonomy_tracks, applied)
    by_id = {course["source_id"]: course for course in recompiled["courses"]}
    for entry in editorial:
        course = by_id[entry["source_id"]]
        assert course["summary"] == entry["summary"]
        assert course["review_note"] == entry["review_note"]


def test_command_writes_then_checks_the_same_result(tmp_path: Path) -> None:
    candidates, editorial, catalogue = _load_inputs()
    catalogue_path = tmp_path / "courses.json"
    candidates_path = tmp_path / "candidates.json"
    editorial_path = tmp_path / "editorial.json"
    output_path = tmp_path / "edited.json"
    for path, value in (
        (catalogue_path, catalogue),
        (candidates_path, candidates),
        (editorial_path, editorial),
    ):
        path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    arguments = [
        "--catalogue",
        str(catalogue_path),
        "--candidates",
        str(candidates_path),
        "--editorial",
        str(editorial_path),
        "--output",
        str(output_path),
    ]
    assert main(arguments) == 0
    assert main([*arguments, "--check"]) == 0


def test_researched_inventory_corrections_survive_the_authoritative_pipeline() -> None:
    _, _, catalogue = _load_inputs()
    courses = {course["source_id"]: course for course in catalogue["courses"]}

    cs107e = courses[58]
    assert cs107e["resource_coverage"]["video"] == 0
    assert "lectures are not recorded" in cs107e["summary"]["en"]
    assert "lecture 不录制" in cs107e["summary"]["zh"]

    res_6008 = courses[88]
    assert "solution packets for Lessons 2–20" in res_6008["summary"]["en"]
    assert "nineteen solved problem sets" not in res_6008["summary"]["en"].lower()
    assert "后 19 课对应的解答包" in res_6008["summary"]["zh"]

    ece3030 = courses[107]
    assert "thirty-six handout groups" in ece3030["summary"]["en"].lower()
    assert "36 组讲义" in ece3030["summary"]["zh"]
