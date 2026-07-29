from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from scripts.quality_common import Issue
from scripts.quality_report import _external_statistics, _markdown_report, _report_ok


def _write_report(
    path: Path,
    *,
    generated_at: str,
    ok: int = 2,
    review: int = 1,
    failed: int = 0,
    review_approved: int | None = None,
    review_unapproved: int | None = None,
    include_review_adjudication: bool = True,
) -> None:
    if review_approved is None:
        review_approved = review
    if review_unapproved is None:
        review_unapproved = review - review_approved
    results = []
    review_index = 0
    for index, outcome in enumerate(
        ["ok"] * ok + ["review"] * review + ["failed"] * failed
    ):
        result = {"url": f"https://example.com/{index}", "outcome": outcome}
        if outcome == "review" and include_review_adjudication:
            retained = review_index < review_approved
            result["review_adjudication"] = {
                "recorded": retained,
                "decision": "retain" if retained else None,
                "approved": retained,
            }
            review_index += 1
        results.append(result)
    summary = {
        "total": len(results),
        "ok": ok,
        "review": review,
        "failed": failed,
        "healthy_percent": round(ok * 100 / len(results), 2),
    }
    if include_review_adjudication:
        summary["review_approved"] = review_approved
        summary["review_unapproved"] = review_unapproved
    path.write_text(
        json.dumps(
            {
                "generated_at": generated_at,
                "summary": summary,
                "results": results,
            }
        ),
        encoding="utf-8",
    )


def test_external_report_is_optional_for_local_report(tmp_path: Path) -> None:
    statistics, issues = _external_statistics(tmp_path / "missing.json")

    assert statistics is None
    assert [(issue.severity, issue.code) for issue in issues] == [
        ("warning", "external.report_missing")
    ]


def test_external_report_can_be_explicitly_skipped(tmp_path: Path) -> None:
    statistics, issues = _external_statistics(
        tmp_path / "missing.json",
        skip_external=True,
    )

    assert statistics is None
    assert issues == []


def test_external_report_is_required_for_release(tmp_path: Path) -> None:
    statistics, issues = _external_statistics(
        tmp_path / "missing.json", require_external=True
    )

    assert statistics is None
    assert [(issue.severity, issue.code) for issue in issues] == [
        ("error", "external.report_missing")
    ]


def test_external_failures_are_a_quality_error(tmp_path: Path) -> None:
    report = tmp_path / "external.json"
    _write_report(
        report,
        generated_at=datetime.now(timezone.utc).isoformat(),
        failed=1,
    )

    statistics, issues = _external_statistics(report)

    assert statistics is not None
    assert statistics["failed"] == 1
    assert any(issue.code == "external.failed" and issue.severity == "error" for issue in issues)


def test_required_external_report_must_be_fresh(tmp_path: Path) -> None:
    report = tmp_path / "external.json"
    _write_report(
        report,
        generated_at=(datetime.now(timezone.utc) - timedelta(days=15)).isoformat(),
    )

    statistics, issues = _external_statistics(
        report,
        require_external=True,
        max_age_days=14,
    )

    assert statistics is not None
    assert statistics["generated_at"].endswith("+00:00")
    assert any(
        issue.code == "external.report_stale" and issue.severity == "error"
        for issue in issues
    )


def test_required_external_report_rejects_missing_review_adjudication(
    tmp_path: Path,
) -> None:
    report = tmp_path / "external.json"
    _write_report(
        report,
        generated_at=datetime.now(timezone.utc).isoformat(),
        include_review_adjudication=False,
    )

    statistics, issues = _external_statistics(report, require_external=True)

    assert statistics is not None
    assert any(
        issue.code == "external.review_adjudication_missing"
        and issue.severity == "error"
        for issue in issues
    )
    assert any(
        issue.code == "external.role_counts_required"
        and issue.severity == "error"
        for issue in issues
    )


def test_required_external_report_rejects_unapproved_reviews(
    tmp_path: Path,
) -> None:
    report = tmp_path / "external.json"
    _write_report(
        report,
        generated_at=datetime.now(timezone.utc).isoformat(),
        review_approved=0,
        review_unapproved=1,
    )

    statistics, issues = _external_statistics(report, require_external=True)

    assert statistics is not None
    assert statistics["review_unapproved"] == 1
    assert any(
        issue.code == "external.review_unapproved" and issue.severity == "error"
        for issue in issues
    )


def test_external_review_summary_must_match_result_adjudications(
    tmp_path: Path,
) -> None:
    report = tmp_path / "external.json"
    _write_report(
        report,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
    payload = json.loads(report.read_text(encoding="utf-8"))
    payload["results"][2]["review_adjudication"] = {
        "recorded": False,
        "decision": None,
        "approved": False,
    }
    report.write_text(json.dumps(payload), encoding="utf-8")

    statistics, issues = _external_statistics(report, require_external=True)

    assert statistics is not None
    assert any(
        issue.code == "external.review_adjudication_results"
        and issue.severity == "error"
        for issue in issues
    )


def test_markdown_report_displays_review_adjudication_counts() -> None:
    report = _markdown_report(
        {
            "ok": True,
            "generated_at": "2026-07-30T00:00:00+00:00",
            "catalogue": {
                "courses": 141,
                "tracks_used": 35,
                "resource_metadata_percent": 100.0,
                "unique_high_value_resources": 1531,
                "courses_with_projects": 141,
                "courses_by_tier": {},
                "courses_by_role": {},
            },
            "execution": {
                "workload_explicit": 141,
                "workload_explicit_percent": 100.0,
                "tooling_complete": 141,
                "tooling_complete_percent": 100.0,
                "safety_complete": 141,
                "safety_complete_percent": 100.0,
                "completion_evidence_complete": 141,
                "completion_evidence_complete_percent": 100.0,
                "safety_levels": {},
                "resource_statuses": {},
            },
            "editorial": {
                "guides_checked": 62,
                "guides_total": 62,
                "errors": 0,
                "warnings": 0,
            },
            "course_guides": {
                "minimum_guides": 60,
                "tracks_covered": 35,
                "tracks_populated": 35,
                "mainlines_covered": 60,
                "mainlines_audited": 60,
            },
            "mainline_audit": {
                "tracks": 35,
                "mainlines": 60,
                "preferred": 35,
                "pass": 60,
                "review": 0,
            },
            "routes": {"catalogue_coverage_percent": 100.0},
            "docs": {
                "researched_course_guides": 62,
                "translation": {
                    "pair_coverage_percent": 100.0,
                    "substantive_guide_pairs": 62,
                },
                "navigation": {"reachability_percent": 100.0},
                "generated_expected": 380,
                "links": {
                    "markdown_files": 400,
                    "links_internal": 6040,
                    "unique_external_urls": 1880,
                },
            },
            "external": {
                "ok": 1842,
                "review": 38,
                "review_approved": 38,
                "review_unapproved": 0,
                "failed": 0,
                "healthy_percent": 97.98,
                "generated_at": "2026-07-30T00:00:00+00:00",
                "report_age_hours": 1,
            },
            "issues": [],
        }
    )

    assert "- Manual review approved: 38" in report
    assert "- Manual review unapproved: 0" in report


def test_report_verdict_respects_warnings_as_errors() -> None:
    issues = [Issue("warning", "example.warning", "needs review")]

    assert _report_ok(issues, warnings_as_errors=False)
    assert not _report_ok(issues, warnings_as_errors=True)


def _write_role_aware_external_report(
    path: Path,
    *,
    evidence_outcome: str = "review",
    evidence_status: int | None = 403,
    evidence_reason: str = "client access policy",
) -> None:
    target_url = "https://example.edu/course"
    evidence_url = "https://example.edu/index"
    reviewed_at = datetime.now(timezone.utc).date().isoformat()
    evidence_reason_code = (
        "http_403"
        if evidence_status == 403
        else "http_missing"
        if evidence_status in {404, 410}
        else "network_error"
    )
    results = [
        {
            "url": target_url,
            "outcome": "review",
            "http_status": 403,
            "reason": "client access policy",
            "reason_code": "http_403",
            "link_roles": ["target"],
            "review_adjudication": {
                "recorded": True,
                "decision": "retain",
                "approved": True,
                "reviewer": "independent review",
                "reviewed_at": reviewed_at,
                "automation_reason": "HTTP 403",
                "method": "Confirmed on the official index.",
                "allowed_reason_codes": ["http_403"],
                "evidence": [evidence_url],
            },
        },
        {
            "url": evidence_url,
            "outcome": evidence_outcome,
            "http_status": evidence_status,
            "reason": evidence_reason,
            "reason_code": evidence_reason_code,
            "link_roles": ["evidence"],
            "evidence_attestation": {
                "recorded": True,
                "manually_verified": True,
                "reviewer": "independent review",
                "reviewed_at": reviewed_at,
            },
        },
    ]
    outcome_counts = {
        outcome: sum(result["outcome"] == outcome for result in results)
        for outcome in ("ok", "review", "failed")
    }
    evidence_counts = {
        outcome: int(evidence_outcome == outcome)
        for outcome in ("ok", "review", "failed")
    }
    path.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "summary": {
                    "total": 2,
                    **outcome_counts,
                    "target_total": 1,
                    "target_ok": 0,
                    "target_review": 1,
                    "target_failed": 0,
                    "evidence_total": 1,
                    **{
                        f"evidence_{outcome}": count
                        for outcome, count in evidence_counts.items()
                    },
                    "evidence_only": 1,
                    "review_approved": 1,
                    "review_unapproved": 0,
                    "healthy_percent": round(outcome_counts["ok"] * 50, 2),
                },
                "results": results,
            }
        ),
        encoding="utf-8",
    )


def test_role_aware_external_report_keeps_attested_403_evidence_separate(
    tmp_path: Path,
) -> None:
    report = tmp_path / "external.json"
    _write_role_aware_external_report(report)

    statistics, issues = _external_statistics(report, require_external=True)

    assert statistics is not None
    assert statistics["target_review"] == 1
    assert statistics["review_approved"] == 1
    assert statistics["evidence_review"] == 1
    assert not [issue for issue in issues if issue.severity == "error"]


def test_role_aware_external_report_rejects_non_policy_evidence_review(
    tmp_path: Path,
) -> None:
    report = tmp_path / "external.json"
    _write_role_aware_external_report(
        report,
        evidence_status=None,
        evidence_reason="TLS handshake failed",
    )

    _statistics, issues = _external_statistics(report, require_external=True)

    assert any(
        issue.code == "external.evidence_review_unapproved"
        and issue.severity == "error"
        for issue in issues
    )


@pytest.mark.parametrize("status", [404, 410])
def test_role_aware_external_report_rejects_missing_evidence(
    tmp_path: Path,
    status: int,
) -> None:
    report = tmp_path / "external.json"
    _write_role_aware_external_report(
        report,
        evidence_outcome="failed",
        evidence_status=status,
        evidence_reason="resource is missing",
    )

    _statistics, issues = _external_statistics(report, require_external=True)

    assert any(
        issue.code == "external.failed" and issue.severity == "error"
        for issue in issues
    )


def test_role_aware_external_report_rejects_inconsistent_role_counts(
    tmp_path: Path,
) -> None:
    report = tmp_path / "external.json"
    _write_role_aware_external_report(report)
    payload = json.loads(report.read_text(encoding="utf-8"))
    payload["summary"]["evidence_review"] = 0
    payload["summary"]["evidence_ok"] = 1
    report.write_text(json.dumps(payload), encoding="utf-8")

    _statistics, issues = _external_statistics(report, require_external=True)

    assert any(issue.code == "external.role_count_results" for issue in issues)


def test_release_report_rejects_legacy_format_even_with_retain_decision(
    tmp_path: Path,
) -> None:
    report = tmp_path / "external.json"
    _write_report(
        report,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    _statistics, issues = _external_statistics(report, require_external=True)

    assert any(
        issue.code == "external.role_counts_required"
        and issue.severity == "error"
        for issue in issues
    )


def test_role_aware_report_rejects_one_line_retain_adjudication(
    tmp_path: Path,
) -> None:
    report = tmp_path / "external.json"
    _write_role_aware_external_report(report)
    payload = json.loads(report.read_text(encoding="utf-8"))
    payload["results"][0]["review_adjudication"] = {"decision": "retain"}
    report.write_text(json.dumps(payload), encoding="utf-8")

    _statistics, issues = _external_statistics(report, require_external=True)

    assert any(
        issue.code == "external.review_adjudication_invalid"
        and issue.severity == "error"
        for issue in issues
    )


def test_role_aware_report_applies_evidence_policy_to_overlap(
    tmp_path: Path,
) -> None:
    report = tmp_path / "external.json"
    _write_role_aware_external_report(report)
    payload = json.loads(report.read_text(encoding="utf-8"))
    target = payload["results"][0]
    evidence = payload["results"][1]
    target["link_roles"] = ["target", "evidence"]
    target["outcome"] = "review"
    target["http_status"] = None
    target["reason"] = "SSLError: certificate chain unavailable"
    target["reason_code"] = "tls_error"
    target["review_adjudication"]["allowed_reason_codes"] = ["tls_error"]
    target["review_adjudication"]["evidence"] = [target["url"]]
    target["evidence_attestation"] = evidence["evidence_attestation"]
    evidence["outcome"] = "ok"
    evidence["http_status"] = 200
    evidence["reason"] = "successful response"
    evidence["reason_code"] = "http_ok"
    summary = payload["summary"]
    summary.update(
        {
            "ok": 1,
            "review": 1,
            "target_total": 1,
            "target_ok": 0,
            "target_review": 1,
            "target_failed": 0,
            "evidence_total": 2,
            "evidence_ok": 1,
            "evidence_review": 1,
            "evidence_failed": 0,
            "evidence_only": 1,
            "healthy_percent": 50.0,
        }
    )
    report.write_text(json.dumps(payload), encoding="utf-8")

    _statistics, issues = _external_statistics(report, require_external=True)

    assert any(
        issue.code == "external.evidence_review_unapproved"
        and issue.severity == "error"
        for issue in issues
    )


def test_role_aware_report_rejects_robots_word_spoof(
    tmp_path: Path,
) -> None:
    report = tmp_path / "external.json"
    _write_role_aware_external_report(
        report,
        evidence_status=None,
        evidence_reason="DNS resolution failed for robots.invalid",
    )
    payload = json.loads(report.read_text(encoding="utf-8"))
    payload["results"][1]["reason_code"] = "robots_denied"
    report.write_text(json.dumps(payload), encoding="utf-8")

    _statistics, issues = _external_statistics(report, require_external=True)

    assert any(
        issue.code == "external.evidence_review_unapproved"
        and issue.severity == "error"
        for issue in issues
    )


def test_role_aware_report_requires_checked_adjudication_evidence(
    tmp_path: Path,
) -> None:
    report = tmp_path / "external.json"
    _write_role_aware_external_report(report)
    payload = json.loads(report.read_text(encoding="utf-8"))
    payload["results"][0]["review_adjudication"]["evidence"] = [
        "https://example.edu/not-checked"
    ]
    report.write_text(json.dumps(payload), encoding="utf-8")

    _statistics, issues = _external_statistics(report, require_external=True)

    assert any(
        issue.code == "external.review_evidence_missing"
        and issue.severity == "error"
        for issue in issues
    )


@pytest.mark.parametrize("max_age", [float("nan"), float("inf"), -1])
def test_external_report_rejects_invalid_max_age(
    tmp_path: Path,
    max_age: float,
) -> None:
    report = tmp_path / "external.json"
    _write_role_aware_external_report(report)

    statistics, issues = _external_statistics(
        report,
        require_external=True,
        max_age_days=max_age,
    )

    assert statistics is None
    assert [(issue.severity, issue.code) for issue in issues] == [
        ("error", "external.max_age")
    ]


@pytest.mark.parametrize(
    ("status", "reason_code"),
    [(403, "http_403"), (404, "http_missing"), (500, "http_server_error")],
)
def test_role_aware_report_rejects_forged_healthy_http_result(
    tmp_path: Path,
    status: int,
    reason_code: str,
) -> None:
    report = tmp_path / "external.json"
    _write_role_aware_external_report(report)
    payload = json.loads(report.read_text(encoding="utf-8"))
    target = payload["results"][0]
    target["outcome"] = "ok"
    target["http_status"] = status
    target["reason"] = "forged healthy result"
    target["reason_code"] = reason_code
    target.pop("review_adjudication")
    summary = payload["summary"]
    summary.update(
        {
            "ok": 1,
            "review": 1,
            "target_ok": 1,
            "target_review": 0,
            "review_approved": 0,
            "review_unapproved": 0,
            "healthy_percent": 50.0,
        }
    )
    report.write_text(json.dumps(payload), encoding="utf-8")

    _statistics, issues = _external_statistics(report, require_external=True)

    assert any(
        issue.code == "external.result_inconsistent"
        and issue.severity == "error"
        for issue in issues
    )
