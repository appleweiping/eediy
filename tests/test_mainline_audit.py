from __future__ import annotations

import copy
from datetime import date

from scripts.validate_mainline_audit import mainline_audit_issues


def sample_inputs() -> tuple[dict, list[dict], dict, dict]:
    candidates = [
        {
            "id": index,
            "title": f"Course {index}",
            "institution": "Example University",
            "code": f"EE {index}",
            "url": f"https://example.edu/courses/{index}",
            "track": f"track-{index}",
            "role": "mainline",
            "tier": "A",
            "tier_note": "A",
            "resources": {
                "video": 1,
                "notes": 1,
                "practice": 1,
                "labs": 0,
                "exams": 0,
                "code": 0,
            },
            "risk": "No public laboratory.",
            "verified_at": "2026-07-28",
        }
        for index in range(1, 36)
    ]
    tracks = {"tracks": [{"id": f"track-{index}"} for index in range(1, 36)]}
    resources = {
        "resources": [
            {
                "course_id": index,
                "kind": "course",
                "url": f"https://example.edu/courses/{index}",
            }
            for index in range(1, 36)
        ]
    }
    audits = [
        {
            "track": f"track-{index}",
            "course_id": index,
            "status": "pass",
            "preferred": True,
            "official_url": f"https://example.edu/courses/{index}/",
            "checks": {
                "identity": "pass",
                "resources": "pass",
                "mainline_fit": "pass",
                "limitations": "pass",
            },
            "limitation_zh": "没有公开实验。",
            "limitation_en": "No public laboratory.",
            "rationale_zh": "身份和资源与候选记录一致。",
            "rationale_en": "Identity and resources agree with the candidate record.",
            "verified_at": "2026-07-29",
        }
        for index in range(1, 36)
    ]
    audit_data = {
        "summary": {
            "track_count": 35,
            "mainline_count": 35,
            "preferred_count": 35,
            "pass_count": 35,
            "review_count": 0,
        },
        "audits": audits,
    }
    return audit_data, candidates, tracks, resources


def test_mainline_audit_accepts_exact_coverage() -> None:
    audit_data, candidates, tracks, resources = sample_inputs()
    assert (
        mainline_audit_issues(
            audit_data,
            candidates,
            tracks,
            resources,
            today=date(2026, 7, 29),
        )
        == []
    )


def test_mainline_audit_rejects_missing_mainline_and_preferred() -> None:
    audit_data, candidates, tracks, resources = sample_inputs()
    audit_data["audits"].pop()
    audit_data["summary"]["mainline_count"] -= 1
    audit_data["summary"]["preferred_count"] -= 1
    audit_data["summary"]["pass_count"] -= 1
    issues = mainline_audit_issues(
        audit_data,
        candidates,
        tracks,
        resources,
        today=date(2026, 7, 29),
    )
    codes = {issue.code for issue in issues}
    assert "mainline_audit.missing" in codes
    assert "mainline_audit.preferred_count" in codes


def test_mainline_audit_rejects_inconsistent_review_status() -> None:
    audit_data, candidates, tracks, resources = sample_inputs()
    broken = copy.deepcopy(audit_data)
    broken["audits"][0]["checks"]["resources"] = "review"
    issues = mainline_audit_issues(
        broken,
        candidates,
        tracks,
        resources,
        today=date(2026, 7, 29),
    )
    assert any(
        issue.code == "mainline_audit.status_inconsistent" for issue in issues
    )


def test_mainline_audit_rejects_non_candidate_official_url() -> None:
    audit_data, candidates, tracks, resources = sample_inputs()
    audit_data["audits"][0]["official_url"] = "https://unrelated.example/course"
    issues = mainline_audit_issues(
        audit_data,
        candidates,
        tracks,
        resources,
        today=date(2026, 7, 29),
    )
    assert any(issue.code == "mainline_audit.official_url" for issue in issues)
