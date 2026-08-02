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
    ) == []


def test_route_set_must_be_non_empty(catalogue: dict, routes_data: dict) -> None:
    routes_data["routes"] = []

    issues = route_issues(routes_data, catalogue)

    assert {issue.code for issue in issues} == {"routes.count", "routes.coverage"}


def test_route_rejects_missing_course(catalogue: dict, routes_data: dict) -> None:
    routes_data["routes"][0]["stages"][0]["course_ids"] = [999]
    issues = route_issues(
        routes_data,
        catalogue,
    )
    assert any(issue.code == "routes.course_missing" for issue in issues)


def test_route_rejects_required_course_outside_stage(
    catalogue: dict, routes_data: dict
) -> None:
    routes_data["routes"][0]["stages"][0]["required_course_ids"] = [999]
    issues = route_issues(
        routes_data,
        catalogue,
    )
    assert any(issue.code == "routes.stage_required_subset" for issue in issues)


def test_route_rejects_impossible_elective_count(
    catalogue: dict, routes_data: dict
) -> None:
    routes_data["routes"][0]["stages"][0]["elective_count"] = 1
    issues = route_issues(
        routes_data,
        catalogue,
    )
    assert any(issue.code == "routes.stage_elective_count" for issue in issues)


def test_route_accepts_ordered_complete_path_options(
    catalogue: dict, routes_data: dict
) -> None:
    _add_complete_paths(catalogue, routes_data)
    assert route_issues(
        routes_data,
        catalogue,
    ) == []


def test_route_rejects_path_course_outside_stage(
    catalogue: dict, routes_data: dict
) -> None:
    stage = _add_complete_paths(catalogue, routes_data)
    stage["path_options"][0]["course_ids"] = [1, 999]
    issues = route_issues(
        routes_data,
        catalogue,
    )
    assert any(issue.code == "routes.stage_path_subset" for issue in issues)


def test_route_rejects_path_order_drift(catalogue: dict, routes_data: dict) -> None:
    stage = _add_complete_paths(catalogue, routes_data)
    stage["path_options"][0]["course_ids"] = [2, 1]
    issues = route_issues(
        routes_data,
        catalogue,
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
            "selection_zh": "先完成后续课，再提交阶段产物。",
            "selection_en": "Complete the later course before submitting the stage artifact.",
            "exit_zh": "提交后续阶段成果。",
            "exit_en": "Submit the later-stage artifact.",
        }
    )
    issues = route_issues(
        routes_data,
        catalogue,
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
    ) == []
    stage.pop("elective_course_ids")
    issues = route_issues(
        routes_data,
        catalogue,
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
    )
    codes = {issue.code for issue in issues}
    assert "routes.stage_path_translation" in codes
    assert "routes.stage_path_label_duplicate" in codes


def test_route_requires_bilingual_path_specific_stop_criteria(
    catalogue: dict, routes_data: dict
) -> None:
    stage = _add_complete_paths(catalogue, routes_data)
    stage["path_options"][0]["stop_when_zh"] = "完成硬件分支的独立检查。"

    issues = route_issues(
        routes_data,
        catalogue,
    )
    assert any(
        issue.code == "routes.stage_path_stop_translation" for issue in issues
    )


def test_route_accepts_one_ordered_optional_extension(
    catalogue: dict, routes_data: dict
) -> None:
    base_course = catalogue["courses"][0]
    base_course["prerequisite_course_ids"] = []
    for source_id, prerequisites in ((2, []), (3, [2]), (4, [2, 3])):
        course = deepcopy(base_course)
        course["source_id"] = source_id
        course["prerequisite_course_ids"] = prerequisites
        course["role"] = "alternative"
        catalogue["courses"].append(course)
    stage = routes_data["routes"][0]["stages"][0]
    stage.update(
        {
            "course_ids": [1, 2, 3, 4],
            "required_course_ids": [1],
            "extension_paths": [
                {
                    "id": "ordered-extension",
                    "label_zh": "按序扩展",
                    "label_en": "Ordered extension",
                    "course_ids": [2, 3, 4],
                }
            ],
            "elective_count": 0,
        }
    )

    assert route_issues(
        routes_data,
        catalogue,
    ) == []


def test_route_rejects_unordered_or_prerequisite_leaking_extension(
    catalogue: dict, routes_data: dict
) -> None:
    base_course = catalogue["courses"][0]
    base_course["prerequisite_course_ids"] = []
    for source_id, prerequisites in ((2, []), (3, [2]), (4, [3])):
        course = deepcopy(base_course)
        course["source_id"] = source_id
        course["prerequisite_course_ids"] = prerequisites
        catalogue["courses"].append(course)
    stage = routes_data["routes"][0]["stages"][0]
    stage.update(
        {
            "course_ids": [1, 2, 3, 4],
            "required_course_ids": [1],
            "extension_paths": [
                {
                    "id": "broken-extension",
                    "label_zh": "错误扩展",
                    "label_en": "Broken extension",
                    "course_ids": [4, 3, 2],
                }
            ],
            "elective_count": 0,
        }
    )

    issues = route_issues(
        routes_data,
        catalogue,
    )
    codes = {issue.code for issue in issues}
    assert "routes.stage_extension_order" in codes
    assert "routes.stage_extension_prerequisite" in codes


def test_route_rejects_a_cloned_guidance_rhythm(
    catalogue: dict, routes_data: dict
) -> None:
    clone = deepcopy(routes_data["routes"][0])
    clone["id"] = "starter-clone"
    clone["title_zh"] = "另一条路线"
    clone["title_en"] = "Another route"
    clone["stages"][0]["exit_zh"] = "另一份可复现出口。"
    clone["stages"][0]["exit_en"] = "A different reproducible exit."
    routes_data["routes"].append(clone)

    issues = route_issues(
        routes_data,
        catalogue,
    )
    assert any(
        issue.code == "routes.guidance_structure_duplicate" for issue in issues
    )


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


def test_essential_core_does_not_promise_a_hidden_aggregate_duration() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    route = next(item for item in routes if item["id"] == "essential-core")

    assert "最短主线的完整出口" in route["outcome_zh"]
    assert "complete exit for this shortest route" in route["outcome_en"]
    guidance_zh = " ".join(
        item
        for section in route["guidance_sections"]
        for item in section["items_zh"]
    )
    guidance_en = " ".join(
        item
        for section in route["guidance_sections"]
        for item in section["items_en"]
    )
    assert "simulation-only 完成" in guidance_zh
    assert "complete, simulation-only" in guidance_en
    assert "各课程页的维护者规划估计" not in route["outcome_zh"]
    assert "maintainer planning estimates on each course page" not in route["outcome_en"]


def test_production_routes_do_not_speak_as_the_site_or_a_reviewer() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    text = routes_path.read_text(encoding="utf-8")

    for phrase in (
        "本站",
        "EEDIY makes",
        "按本站",
        "this guide",
        "reviewer",
        "复核者",
    ):
        assert phrase not in text


def test_route_rejects_missing_or_unpaired_guidance_sections(
    catalogue: dict, routes_data: dict
) -> None:
    route = routes_data["routes"][0]
    route["guidance_sections"][0]["items_zh"] = []
    route["guidance_sections"][1]["items_en"].append("A second unmatched item.")

    issues = route_issues(
        routes_data,
        catalogue,
    )
    codes = {issue.code for issue in issues}
    assert "routes.guidance_section_translation" in codes
    assert "routes.guidance_section_parity" in codes


def test_production_routes_have_bilingual_route_specific_guidance_rhythms() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]

    signatures = []
    for route in routes:
        sections = route["guidance_sections"]
        assert 2 <= len(sections) <= 6
        assert len({section["id"] for section in sections}) == len(sections)
        for section in sections:
            assert section["style"] in {"prose", "list"}
            assert len(section["items_zh"]) == len(section["items_en"]) >= 1
            assert section["title_zh"].strip()
            assert section["title_en"].strip()
        signatures.append(
            (
                len(sections),
                tuple(
                    (section["style"], len(section["items_en"]))
                    for section in sections
                ),
            )
        )

    # A route's reading rhythm is editorial data, not a global 3-do/2-skip/2-stop
    # template with renamed headings.
    assert len(signatures) == len(set(signatures)) == len(routes)
    assert {len(route["guidance_sections"]) for route in routes} == {3, 4}
    for language in ("zh", "en"):
        titles = [
            section[f"title_{language}"]
            for route in routes
            for section in route["guidance_sections"]
        ]
        assert len(titles) == len(set(titles))


def test_digital_route_keeps_hardware_and_software_acceptance_separate() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    route = next(item for item in routes if item["id"] == "digital-fpga-architecture")
    first_stage = route["stages"][0]

    assert first_stage["elective_count"] == 0
    assert [option["course_ids"] for option in first_stage["path_options"]] == [
        [39],
        [40],
    ]
    hardware, software = first_stage["path_options"]
    assert "CPU、内存与 Hack 计算机" in hardware["stop_when_zh"]
    assert "chips, CPU, memory, and Hack computer" in hardware["stop_when_en"]
    assert "assembler、VM translator、Jack compiler" in software["stop_when_zh"]
    assert "assembler, VM translator, Jack compiler" in software["stop_when_en"]
    assert "不声称实现了门电路、RTL 或 FPGA" in software["stop_when_zh"]
    assert "makes no gate-level, RTL, or FPGA claim" in software["stop_when_en"]


def test_analog_route_uses_ee140_and_does_not_jump_to_digital_ic() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    route = next(item for item in routes if item["id"] == "analog-ic")
    course_ids = {
        course_id
        for stage in route["stages"]
        for course_id in stage["course_ids"]
    }

    assert 141 in course_ids
    assert 50 not in course_ids
    assert 51 not in course_ids
    assert "schematic-level" in route["outcome_zh"]
    assert "schematic-level" in route["outcome_en"]
    assert "不承诺复现 Berkeley" in route["outcome_zh"]
    assert "does not promise to reproduce Berkeley" in route["outcome_en"]


def test_production_stage_selection_notes_are_authored_and_nonrepetitive() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    stages = [stage for route in routes for stage in route["stages"]]
    zh_notes = [stage["selection_zh"] for stage in stages]
    en_notes = [stage["selection_en"] for stage in stages]

    assert stages
    assert len(stages) == len(set(zh_notes)) == len(set(en_notes))
    assert all(len(note) >= 55 for note in zh_notes)
    assert all(len(note.split()) >= 24 for note in en_notes)
    boilerplate = (
        "使用全部",
        "核心课程取材",
        "Use all ",
        "Use the core course",
        "as source material",
    )
    assert not any(fragment in note for note in zh_notes + en_notes for fragment in boilerplate)


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
    cases = (("control-robotics", "Feedback and optimal control", [67], [69, 72], 1),)
    for route_id, stage_name, required_ids, elective_ids, elective_count in cases:
        stage = next(
            item
            for item in route_map[route_id]["stages"]
            if item["name_en"] == stage_name
        )
        assert stage["required_course_ids"] == required_ids
        assert stage["elective_course_ids"] == elective_ids
        assert stage["elective_count"] == elective_count


def test_power_route_has_mutually_exclusive_complete_system_exits() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    route = next(item for item in routes if item["id"] == "power-energy")
    converter = next(
        stage for stage in route["stages"] if stage["name_en"] == "Converter and closed loop"
    )
    system = next(
        stage
        for stage in route["stages"]
        if stage["name_en"] == "Connect to a grid, machine, or energy system"
    )

    assert converter["required_course_ids"] == [114]
    assert converter["elective_count"] == 0
    assert [path["course_ids"] for path in converter["extension_paths"]] == [
        [115, 116, 117]
    ]
    assert "1→2→3" in converter["extension_paths"][0]["label_en"]

    assert system["required_course_ids"] == []
    assert system["elective_count"] == 0
    assert system["course_ids"] == [118, 120, 122, 123]
    assert [option["id"] for option in system["path_options"]] == [
        "grid-analysis",
        "electric-machine",
        "photovoltaic-conversion",
        "electrochemical-storage",
    ]
    assert [option["course_ids"] for option in system["path_options"]] == [
        [118],
        [120],
        [122],
        [123],
    ]
    assert "mutually exclusive complete exits" in system["selection_en"]
    assert "unchosen branches are not completion requirements" in system["exit_en"]


def test_analog_route_makes_ee105_a_real_bridge() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    route = next(item for item in routes if item["id"] == "analog-ic")
    bridge = next(
        stage for stage in route["stages"] if stage["name_en"] == "From device curves to bias"
    )

    assert bridge["required_course_ids"] == [21, 29, 31]
    assert bridge["elective_count"] == 0
    assert "elective_course_ids" not in bridge
    assert "EE 105 is the required bridge" in bridge["selection_en"]
    assert "equivalent competence may replace retaking the entire course" in bridge[
        "selection_en"
    ]


def test_photonics_system_stage_enforces_the_three_way_choice_it_describes() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    route = next(item for item in routes if item["id"] == "photonics-mems")
    system = next(
        stage for stage in route["stages"] if stage["name_en"] == "Photonic systems"
    )

    assert system["required_course_ids"] == [132]
    assert system["elective_count"] == 0
    assert "elective_course_ids" not in system
    assert [option["course_ids"] for option in system["path_options"]] == [
        [133],
        [134],
        [135],
    ]
    assert "exactly one of three courses is chosen" in system["selection_en"]


def test_essential_core_probability_changes_the_rc_artifact() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    route = next(item for item in routes if item["id"] == "essential-core")
    guidance = " ".join(
        item
        for section in route["guidance_sections"]
        for item in section["items_en"]
    )
    final_exit = route["stages"][-1]["exit_en"]

    assert "first unaided failure is the stop point" in guidance
    assert "no preset problem count" in guidance
    assert "Solve 12" not in guidance
    assert "model R and C as independent random variables" in guidance
    assert "E[RC]" in guidance
    assert "Var(RC)" in guidance
    assert "5th/50th/95th percentiles" in guidance
    assert "seeded Monte Carlo" in final_exit
    assert "delta-method" in guidance


def test_access_limited_rf_and_vlsi_courses_are_complete_path_choices() -> None:
    routes_path = Path(__file__).resolve().parents[1] / "data" / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8"))["routes"]
    route_map = {route["id"]: route for route in routes}

    rf_stage = next(
        stage
        for stage in route_map["rf-wireless"]["stages"]
        if stage["name_en"] == "RF circuits and antennas"
    )
    assert rf_stage["required_course_ids"] == []
    assert rf_stage["elective_count"] == 0
    assert [option["course_ids"] for option in rf_stage["path_options"]] == [
        [113],
        [110],
        [111],
    ]
    assert 112 not in {
        course_id
        for option in rf_stage["path_options"]
        for course_id in option["course_ids"]
    }

    analog_design = next(
        stage
        for stage in route_map["analog-ic"]["stages"]
        if stage["name_en"] == "EE 140/240A spine and an honest layout ceiling"
    )
    assert analog_design["required_course_ids"] == [141]
    assert analog_design["elective_count"] == 0
    assert 50 not in analog_design["course_ids"]
    assert 51 not in analog_design["course_ids"]
    assert 126 in analog_design["course_ids"]

    semiconductor_layout = next(
        stage
        for stage in route_map["semiconductor-vlsi"]["stages"]
        if stage["name_en"] == "From transistors to digital layout"
    )
    assert semiconductor_layout["required_course_ids"] == []
    assert semiconductor_layout["elective_count"] == 0
    assert [option["course_ids"] for option in semiconductor_layout["path_options"]] == [
        [49],
        [50],
        [51],
    ]
    assert 44 not in {
        course_id
        for option in semiconductor_layout["path_options"]
        for course_id in option["course_ids"]
    }


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
    )
    assert not any(issue.code == "routes.stage_path_prerequisite" for issue in issues)

    robotic_stage = scoped_routes["routes"][0]["stages"][-1]
    robotic_stage.pop("path_options")
    robotic_stage["required_course_ids"] = [74, 75]
    robotic_stage["elective_count"] = 1
    flat_issues = route_issues(
        scoped_routes,
        catalogue,
    )
    assert any(issue.code == "routes.stage_elective_prerequisite" for issue in flat_issues)
