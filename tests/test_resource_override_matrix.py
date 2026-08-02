from __future__ import annotations

import json
from pathlib import Path

from scripts.course_data import validate_resource_manifest


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_RESOURCE_MATRIX = {
    (4, "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/resource-index/"): (
        "course",
        "index",
    ),
    (4, "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/final-exam/"): (
        "exams",
        "content",
    ),
    (26, "https://ocw.mit.edu/courses/6-101-introductory-analog-electronics-laboratory-spring-2007/pages/syllabus/"): (
        "course",
        "syllabus",
    ),
    (26, "https://ocw.mit.edu/courses/6-101-introductory-analog-electronics-laboratory-spring-2007/pages/projects/"): (
        "projects",
        "content",
    ),
    (41, "https://ocw.ece.cornell.edu/ece-2300-lectures-and-handouts/"): (
        "notes",
        "index",
    ),
    (57, "https://vanhunteradams.com/Pico/CourseMaterials/Policy.html"): (
        "course",
        "syllabus",
    ),
    (57, "https://vanhunteradams.com/Pico/Birds/Birdsong.html"): (
        "labs",
        "content",
    ),
    (57, "https://vanhunteradams.com/Pico/Galton/Galton.html"): (
        "labs",
        "content",
    ),
    (57, "https://vanhunteradams.com/Pico/Helicopter/Helicopter.html"): (
        "labs",
        "content",
    ),
    (57, "https://vanhunteradams.com/Pico/Helicopter/MotorCircuit.html"): (
        "labs",
        "content",
    ),
    (57, "https://vanhunteradams.com/Pico/CourseMaterials/Final_Project.html"): (
        "projects",
        "content",
    ),
    (64, "https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/curriculum/computer-engineering-embedded-systems/ecea-5316-theory-and-analysis"): (
        "course",
        "syllabus",
    ),
    (64, "https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/hardware-and-software-requirements"): (
        "course",
        "landing",
    ),
    (77, "https://hades.mech.northwestern.edu/index.php/Modern_Robotics"): (
        "textbook",
        "index",
    ),
    (77, "https://hades.mech.northwestern.edu/index.php/Coursera_Resources"): (
        "other",
        "index",
    ),
    (77, "https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_Modern_Robotics_Code_Library"): (
        "code",
        "content",
    ),
    (77, "https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_CoppeliaSim_Simulator"): (
        "simulator",
        "content",
    ),
    (98, "https://ocw.mit.edu/courses/6-011-introduction-to-communication-control-and-signal-processing-spring-2010/resources/mit6_011s10_notes/"): (
        "textbook",
        "content",
    ),
    (123, "https://ocw.mit.edu/courses/10-626-electrochemical-energy-systems-spring-2014/pages/calendar/"): (
        "course",
        "outline",
    ),
    (123, "https://ocw.mit.edu/courses/10-626-electrochemical-energy-systems-spring-2014/pages/lecture-notes/"): (
        "notes",
        "index",
    ),
    (127, "https://courseware.epfl.ch/courses/course-v1%3AEPFL%2Bmems%2B2023/about"): (
        "course",
        "landing",
    ),
    (127, "https://edu.epfl.ch/coursebook/en/mooc-micro-and-nanofabrication-mems-MICRO-621-A"): (
        "course",
        "syllabus",
    ),
    (127, "https://mediaspace.epfl.ch/channel/channelid/29004"): (
        "video",
        "index",
    ),
    (128, "https://onlinecourses.nptel.ac.in/noc26_ee04/preview"): (
        "course",
        "landing",
    ),
    (128, "https://archive.nptel.ac.in/content/syllabus_pdf/108104865.pdf"): (
        "course",
        "syllabus",
    ),
    (139, "https://archive.nptel.ac.in/content/syllabus_pdf/102106669.pdf"): (
        "course",
        "syllabus",
    ),
    (139, "https://physionet.org/content/mitdb/1.0.0/"): (
        "dataset",
        "content",
    ),
}

DISCLOSED_MIXED_OR_CROSS_LISTED_TITLES = {
    (77, "https://hades.mech.northwestern.edu/index.php/Modern_Robotics"): {
        "zh": "《Modern Robotics》教材主页与公开预印本入口",
        "en": "Modern Robotics textbook home and public-preprint link",
    },
    (77, "https://hades.mech.northwestern.edu/index.php/Coursera_Resources"): {
        "zh": "Modern Robotics 六门课程共享资源索引",
        "en": "Modern Robotics shared six-course resources index",
    },
    (
        127,
        "https://courseware.epfl.ch/courses/course-v1%3AEPFL%2Bmems%2B2023/about",
    ): {
        "zh": "EPFL MICRO-331 / MEMS 课程平台入口",
        "en": "EPFL MICRO-331 / MEMS courseware landing",
    },
}


def test_red_team_resource_matrix_is_complete_and_localized() -> None:
    payload = json.loads(
        (ROOT / "data" / "course_resource_overrides.json").read_text(
            encoding="utf-8"
        )
    )
    records = payload["resources"]
    by_key = {(record["course_id"], record["url"]): record for record in records}

    assert len(EXPECTED_RESOURCE_MATRIX) == 27
    assert len(by_key) == len(records)

    for key, (kind, artifact_scope) in EXPECTED_RESOURCE_MATRIX.items():
        record = by_key[key]
        assert record["kind"] == kind
        assert record["artifact_scope"] == artifact_scope
        assert record["access"] == "open"
        assert record["status"] == "available"
        assert record["last_verified"] == "2026-07-31"
        assert record["source_url"].startswith("https://")
        assert set(record["title"]) == {"zh", "en"}
        assert record["title"]["zh"].strip()
        assert record["title"]["en"].strip()

    for key, title in DISCLOSED_MIXED_OR_CROSS_LISTED_TITLES.items():
        assert by_key[key]["title"] == title


def test_resource_override_manifest_accepts_the_red_team_matrix() -> None:
    payload = json.loads(
        (ROOT / "data" / "course_resource_overrides.json").read_text(
            encoding="utf-8"
        )
    )
    valid, issues = validate_resource_manifest(
        payload,
        candidate_ids=set(range(1, 142)),
        source="data/course_resource_overrides.json",
    )

    assert issues == []
    assert len(valid) == len(payload["resources"])


def test_probability_course_resource_index_is_a_first_class_resource() -> None:
    payload = json.loads(
        (ROOT / "data" / "course_resource_overrides.json").read_text(
            encoding="utf-8"
        )
    )
    record = next(
        item
        for item in payload["resources"]
        if item["course_id"] == 7
        and item["url"].endswith("/pages/resource-index/")
    )

    assert record["kind"] == "course"
    assert record["artifact_scope"] == "index"
    assert "assignments" in record["title"]["en"]
    assert "作业" in record["title"]["zh"]
