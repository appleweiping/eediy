from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts.quality_report import _external_statistics


def _write_report(
    path: Path,
    *,
    generated_at: str,
    ok: int = 2,
    review: int = 1,
    failed: int = 0,
) -> None:
    results = [
        {"url": f"https://example.com/{index}", "outcome": outcome}
        for index, outcome in enumerate(
            ["ok"] * ok + ["review"] * review + ["failed"] * failed
        )
    ]
    path.write_text(
        json.dumps(
            {
                "generated_at": generated_at,
                "summary": {
                    "total": len(results),
                    "ok": ok,
                    "review": review,
                    "failed": failed,
                    "healthy_percent": round(ok * 100 / len(results), 2),
                },
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
