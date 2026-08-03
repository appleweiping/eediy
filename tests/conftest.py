from __future__ import annotations

import copy
from typing import Any

import pytest

from scripts.course_data import compile_catalogue


@pytest.fixture
def taxonomy_tracks() -> list[dict[str, Any]]:
    return [
        {
            "id": "mathematics",
            "group": "foundations",
            "order": 10,
            "title_zh": "工程数学",
            "title_en": "Engineering Mathematics",
            "summary_zh": "面向工程建模的数学基础。",
            "summary_en": "Mathematical foundations for engineering models.",
            "prerequisites": [],
        }
    ]


@pytest.fixture
def candidate() -> dict[str, Any]:
    return {
        "id": 1,
        "title": "Signals Through Calculus",
        "institution": "Example University",
        "code": "EE-101",
        "url": "https://example.edu/courses/ee-101/",
        "track": "mathematics",
        "role": "mainline",
        "tier": "S",
        "tier_note": "S",
        "resources": {
            "video": 2,
            "notes": 2,
            "practice": 2,
            "labs": 0,
            "exams": 1,
            "code": 1,
        },
        "risk": "No public laboratory is included.",
        "verified_at": "2026-07-28",
    }


@pytest.fixture
def catalogue(
    candidate: dict[str, Any], taxonomy_tracks: list[dict[str, Any]]
) -> dict[str, Any]:
    return compile_catalogue([candidate], taxonomy_tracks)


@pytest.fixture
def routes_data() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "routes": [
            {
                "id": "starter",
                "title_zh": "起步路线",
                "title_en": "Starter Route",
                "audience_zh": "希望建立基础的学习者",
                "audience_en": "Learners building a foundation",
                "outcome_zh": "完成一个可复现的基础成果。",
                "outcome_en": "Complete one reproducible foundational artifact.",
                "stages": [
                    {
                        "name_zh": "基础",
                        "name_en": "Foundation",
                        "course_ids": [1],
                        "required_course_ids": [1],
                        "elective_count": 0,
                        "exit_zh": "提交可复现的基础成果并通过五项自动检查。",
                        "exit_en": "Submit a reproducible foundation artifact that passes five automated checks.",
                    }
                ],
            }
        ],
    }
