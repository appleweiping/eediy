from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_quality_report_is_a_blocking_gate_with_external_evidence() -> None:
    workflow = (ROOT / ".github" / "workflows" / "quality.yml").read_text(
        encoding="utf-8"
    )

    assert "continue-on-error: true" not in workflow
    assert "--skip-external --warnings-as-errors" in workflow
    assert "--require-external --warnings-as-errors" in workflow
    assert "--cache-ttl-hours 0" in workflow
    assert workflow.index("Check external resources with the bounded cache") < workflow.index(
        "Build consolidated report"
    )
    assert "build/external-links.json" in workflow


def test_pages_deploys_only_after_a_successful_main_quality_run() -> None:
    workflow = (ROOT / ".github" / "workflows" / "deploy.yml").read_text(
        encoding="utf-8"
    )
    trigger = workflow.split("permissions:", maxsplit=1)[0]

    assert "workflow_run:" in trigger
    assert "workflow_dispatch:" not in trigger
    assert "github.event.workflow_run.conclusion == 'success'" in workflow
    assert "github.event.workflow_run.head_branch == 'main'" in workflow
    assert "ref: ${{ github.event.workflow_run.head_sha }}" in workflow
    assert "enablement: true" in workflow
