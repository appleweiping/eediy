from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from scripts.validate_routes import route_issues


def _add_complete_paths(catalogue: dict, routes_data: dict) -> dict:
    base_course = catalogue["courses"][0]
    base_course["prerequisite_course_ids"] = []
    for source_id in (2, 3, 4):
        course = deepcopy(base_course)
        course["source_id"] = source_id
        course["prerequisite_course_ids"] = (
            [1] if source_id == 2 else [3] if source_id == 4 else []
        )
        catalogue["courses"].append(course)
    stage = routes_data["routes"][0]["stages"][0]
    stage.update(
        {
            "course_ids": [1, 2, 3, 4],
            "required_course_ids": [],
            "path_options": [
                {
                    "id": "short-path",
                    "label_zh": "短路径",
                    "label_en": "Short path",
                    "course_ids": [1, 2],
                },
                {
                    "id": "long-path",
                    "label_zh": "长路径",
                    "label_en": "Long path",
                    "course_ids": [3, 4],
                },
            ],
            "elective_count": 0,
        }
    )
    return stage


def test_route_references_canonical_source_ids(catalogue: dict, routes_data: dict) -> None:
    assert route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    ) == []


def test_route_rejects_missing_course(catalogue: dict, routes_data: dict) -> None:
    routes_data["routes"][0]["stages"][0]["course_ids"] = [999]
    issues = route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    assert any(issue.code == "routes.course_missing" for issue in issues)


def test_route_rejects_required_course_outside_stage(
    catalogue: dict, routes_data: dict
) -> None:
    routes_data["routes"][0]["stages"][0]["required_course_ids"] = [999]
    issues = route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    assert any(issue.code == "routes.stage_required_subset" for issue in issues)


def test_route_rejects_impossible_elective_count(
    catalogue: dict, routes_data: dict
) -> None:
    routes_data["routes"][0]["stages"][0]["elective_count"] = 1
    issues = route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    assert any(issue.code == "routes.stage_elective_count" for issue in issues)


def test_route_accepts_ordered_complete_path_options(
    catalogue: dict, routes_data: dict
) -> None:
    _add_complete_paths(catalogue, routes_data)
    assert route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    ) == []


def test_route_rejects_path_course_outside_stage(
    catalogue: dict, routes_data: dict
) -> None:
    stage = _add_complete_paths(catalogue, routes_data)
    stage["path_options"][0]["course_ids"] = [1, 999]
    issues = route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    assert any(issue.code == "routes.stage_path_subset" for issue in issues)


def test_route_rejects_path_order_drift(catalogue: dict, routes_data: dict) -> None:
    stage = _add_complete_paths(catalogue, routes_data)
    stage["path_options"][0]["course_ids"] = [2, 1]
    issues = route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    assert any(issue.code == "routes.stage_path_order" for issue in issues)


def test_route_rejects_course_repeated_within_or_across_paths(
    catalogue: dict, routes_data: dict
) -> None:
    stage = _add_complete_paths(catalogue, routes_data)
    stage["path_options"][0]["course_ids"] = [1, 1]
    stage["path_options"][1]["course_ids"] = [1, 3, 4]
    issues = route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    codes = {issue.code for issue in issues}
    assert "routes.stage_path_duplicate" in codes
    assert "routes.stage_path_course_duplicate" in codes


def test_route_rejects_path_elective_count_conflict(
    catalogue: dict, routes_data: dict
) -> None:
    stage = _add_complete_paths(catalogue, routes_data)
    stage["elective_count"] = 1
    issues = route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    assert any(issue.code == "routes.stage_path_elective_conflict" for issue in issues)


def test_route_rejects_path_prerequisite_outside_same_path_or_prior_stage(
    catalogue: dict, routes_data: dict
) -> None:
    stage = _add_complete_paths(catalogue, routes_data)
    course_four = next(
        course for course in catalogue["courses"] if course["source_id"] == 4
    )
    course_four["prerequisite_course_ids"] = [1]
    issues = route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    assert any(issue.code == "routes.stage_path_prerequisite" for issue in issues)
    assert stage["path_options"][1]["course_ids"] == [3, 4]


def test_route_requires_required_prerequisite_to_be_guaranteed_by_all_prior_choices(
    catalogue: dict, routes_data: dict
) -> None:
    _add_complete_paths(catalogue, routes_data)
    course_five = deepcopy(catalogue["courses"][0])
    course_five["source_id"] = 5
    course_five["prerequisite_course_ids"] = [1]
    catalogue["courses"].append(course_five)
    routes_data["routes"][0]["stages"].append(
        {
            "name_zh": "后续阶段",
            "name_en": "Later stage",
            "course_ids": [5],
            "required_course_ids": [5],
            "elective_count": 0,
            "exit_zh": "提交后续阶段成果。",
            "exit_en": "Submit the later-stage artifact.",
        }
    )
    issues = route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    assert any(issue.code == "routes.stage_required_prerequisite" for issue in issues)


def test_route_excludes_dependency_leak_from_explicit_elective_pool(
    catalogue: dict, routes_data: dict
) -> None:
    base_course = catalogue["courses"][0]
    base_course["prerequisite_course_ids"] = []
    dependent = deepcopy(base_course)
    dependent["source_id"] = 2
    dependent["prerequisite_course_ids"] = [1]
    independent = deepcopy(base_course)
    independent["source_id"] = 3
    independent["prerequisite_course_ids"] = []
    catalogue["courses"].extend([dependent, independent])
    stage = routes_data["routes"][0]["stages"][0]
    stage.update(
        {
            "course_ids": [1, 2, 3],
            "required_course_ids": [1],
            "elective_course_ids": [3],
            "elective_count": 1,
        }
    )
    assert route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    ) == []
    stage.pop("elective_course_ids")
    issues = route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    assert any(issue.code == "routes.stage_elective_prerequisite" for issue in issues)


def test_route_requires_unique_bilingual_path_labels(
    catalogue: dict, routes_data: dict
) -> None:
    stage = _add_complete_paths(catalogue, routes_data)
    stage["path_options"][0]["label_zh"] = " "
    stage["path_options"][1]["label_en"] = "Short path"
    issues = route_issues(
        routes_data,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    codes = {issue.code for issue in issues}
    assert "routes.stage_path_translation" in codes
    assert "routes.stage_path_label_duplicate" in codes


def test_control_robotics_declares_two_complete_production_paths() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    route = next(item for item in routes if item["id"] == "control-robotics")
    stage = next(item for item in route["stages"] if item["name_en"] == "Robotic systems")
    assert stage["required_course_ids"] == []
    assert stage["elective_count"] == 0
    assert [option["course_ids"] for option in stage["path_options"]] == [
        [74, 75],
        [77, 78, 79, 80, 81, 82],
    ]


def test_instrumentation_route_keeps_access_dependent_practice_optional() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    route = next(
        item for item in routes if item["id"] == "instrumentation-biomedical"
    )
    measurement = next(
        item
        for item in route["stages"]
        if item["name_en"] == "Circuits and measurement"
    )
    sensors = next(
        item
        for item in route["stages"]
        if item["name_en"] == "Sensors and interfaces"
    )

    assert measurement["required_course_ids"] == [21, 24, 83]
    assert sensors["course_ids"] == [136, 138, 137]
    assert sensors["required_course_ids"] == [136]
    assert sensors["elective_count"] == 0
    assert "do not claim a physical experiment" in sensors["exit_en"]


def test_review_mainlines_are_not_hard_required_in_production_routes() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    route_map = {route["id"]: route for route in routes}
    cases = (
        ("analog-ic", "Analog design", [26], [32, 34, 35], 2),
        ("control-robotics", "Feedback and optimal control", [67], [69, 72], 1),
        ("rf-wireless", "RF circuits and antennas", [111], [110, 113], 1),
        ("photonics-mems", "Photonic systems", [132], [134, 135], 1),
    )
    for route_id, stage_name, required_ids, elective_ids, elective_count in cases:
        stage = next(
            item
            for item in route_map[route_id]["stages"]
            if item["name_en"] == stage_name
        )
        assert stage["required_course_ids"] == required_ids
        assert stage["elective_course_ids"] == elective_ids
        assert stage["elective_count"] == elective_count


def test_modern_robotics_chain_is_valid_only_inside_complete_path() -> None:
    root = Path(__file__).resolve().parents[1]
    catalogue = json.loads((root / "data" / "courses.json").read_text(encoding="utf-8"))
    routes = json.loads((root / "data" / "routes.json").read_text(encoding="utf-8"))
    by_id = {course["source_id"]: course for course in catalogue["courses"]}
    for course_id in range(77, 83):
        by_id[course_id]["prerequisite_course_ids"] = list(range(77, course_id))

    control = next(route for route in routes["routes"] if route["id"] == "control-robotics")
    scoped_routes = {"routes": [deepcopy(control)]}
    issues = route_issues(
        scoped_routes,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    assert not any(issue.code == "routes.stage_path_prerequisite" for issue in issues)

    robotic_stage = scoped_routes["routes"][0]["stages"][-1]
    robotic_stage.pop("path_options")
    robotic_stage["required_course_ids"] = [74, 75]
    robotic_stage["elective_count"] = 1
    flat_issues = route_issues(
        scoped_routes,
        catalogue,
        minimum_routes=1,
        minimum_unique_courses=1,
    )
    assert any(issue.code == "routes.stage_elective_prerequisite" for issue in flat_issues)
