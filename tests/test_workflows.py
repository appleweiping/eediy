from __future__ import annotations

from pathlib import Path

from scripts.run_quality import commands


ROOT = Path(__file__).resolve().parents[1]


def test_quality_report_is_a_blocking_gate_with_external_evidence() -> None:
    workflow = (ROOT / ".github" / "workflows" / "quality.yml").read_text(
        encoding="utf-8"
    )

    assert "continue-on-error: true" not in workflow
    assert "--skip-external --warnings-as-errors" not in workflow
    assert "--require-external --warnings-as-errors" in workflow
    assert "--cache-ttl-hours 0" in workflow
    assert workflow.index("Check every external resource with fresh network evidence") < workflow.index(
        "Build consolidated report"
    )
    assert "build/external-links.json" in workflow
    assert (
        "python scripts/check_course_guides.py "
        "--require-track-coverage --require-mainline-coverage"
    ) in workflow
    assert "apply_project_templates.py" not in workflow
    assert "check_giscus.py" not in workflow
    assert "full_external_check" not in workflow
    assert "actions/cache@" not in workflow
    shared_runner = "python scripts/run_executable_examples.py --require-tools all"
    assert workflow.count(shared_runner) == 1
    assert "runs-on: ubuntu-24.04" in workflow
    assert "ppa:kicad/kicad-8.0-releases" in workflow
    assert "8.0.9-0~ubuntu24.04.1" in workflow
    assert 'test "$(kicad-cli version)" = "8.0.9"' in workflow
    toolchain_step = workflow.split("- name: Install executable EE toolchains", 1)[
        1
    ].split("- name: Install pinned SymbiYosys", 1)[0]
    assert "libngspice0" in toolchain_step
    assert "libngspice-kicad 2>/dev/null" in toolchain_step
    assert "--force-overwrite" not in workflow
    assert "fea6e467d067b3ea84b6b5ac08cd48beb59f0d42" in workflow
    assert 'test "$(git -C "$RUNNER_TEMP/sby" rev-parse HEAD)" = "$SBY_COMMIT"' in workflow
    assert workflow.count("--cache-ttl-hours 0") == 1
    external_step = workflow.split(
        "- name: Check every external resource with fresh network evidence", 1
    )[1].split("- name: Build consolidated report", 1)[0]
    assert "if:" not in external_step
    assert workflow.index("Install pinned SymbiYosys") < workflow.index(
        "Execute all release-blocking EE starter toolchains"
    )
    assert workflow.index("Install executable EE toolchains") < workflow.index(
        "Execute all release-blocking EE starter toolchains"
    )


def test_pages_deploys_only_after_a_successful_main_quality_run() -> None:
    workflow = (ROOT / ".github" / "workflows" / "quality.yml").read_text(
        encoding="utf-8"
    )
    assert not (ROOT / ".github" / "workflows" / "deploy.yml").exists()
    assert "Upload the tested Pages artifact" in workflow
    assert workflow.index("Build documentation with warnings as errors") < workflow.index(
        "Upload the tested Pages artifact"
    )
    assert "name: Publish the tested Pages artifact" in workflow
    assert "needs: quality" in workflow
    assert "github.event_name == 'push' && github.ref == 'refs/heads/main'" in workflow
    assert "ref: main" in workflow
    assert 'test "$(git rev-parse HEAD)" = "$GITHUB_SHA"' in workflow
    deploy_job = workflow.split("\n  deploy:\n", 1)[1]
    assert "python -m mkdocs" not in deploy_job
    assert "actions/deploy-pages@cd2ce8fcbc39b97be8ca5fce6e763baed58fa128" in deploy_job


def test_dependency_review_uses_the_fixed_release_runner_image() -> None:
    workflow = (
        ROOT / ".github" / "workflows" / "dependency-review.yml"
    ).read_text(encoding="utf-8")

    assert "runs-on: ubuntu-24.04" in workflow
    assert "ubuntu-latest" not in workflow


def test_local_release_runner_requires_fresh_external_evidence() -> None:
    release_commands = {
        command.label: command.arguments
        for command in commands(include_external=True, include_build=True)
    }
    external = release_commands["external links"]
    report = release_commands["quality report"]

    assert external[-2:] == ("--cache-ttl-hours", "0")
    assert release_commands["executable EE starters"][-3:] == (
        "scripts/run_executable_examples.py",
        "--require-tools",
        "all",
    )
    assert "--require-external" in report
    assert "--skip-external" not in report
    assert "--warnings-as-errors" in report
    assert "suggested project drift" not in release_commands
    assert "--minimum-authored-guides" not in release_commands[
        "authored course records and deep-guide coverage"
    ]


def test_local_offline_runner_declares_external_check_omitted() -> None:
    offline_commands = {
        command.label: command.arguments
        for command in commands(include_external=False, include_build=False)
    }
    report = offline_commands["quality report"]

    assert "--skip-external" in report
    assert "--require-external" not in report
    assert "--warnings-as-errors" in report
    assert "executable EE starters" not in offline_commands
