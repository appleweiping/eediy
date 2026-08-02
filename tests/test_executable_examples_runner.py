from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import scripts.run_executable_examples as runner


def test_release_runner_declares_every_strict_toolchain_in_order() -> None:
    steps = runner.steps("python")

    assert [step.label for step in steps] == [
        "RC analytic reference",
        "RC ngspice batch",
        "RC ngspice verification",
        "ring buffer with ASan and UBSan",
        "sensor sampler with ASan and UBSan",
        "synchronous FIFO simulation, formal, and synthesis",
        "TMP117 KiCad ERC, DRC, parity, and export",
    ]
    assert steps[1].arguments == (
        "ngspice",
        "-o",
        "build/ngspice.log",
        "rc_lowpass.cir",
    )
    assert steps[3].arguments == (
        "cmake",
        "--workflow",
        "--preset",
        "host-sanitized",
    )
    assert steps[4].arguments == steps[3].arguments
    assert steps[5].arguments[-2:] == ("--require-tools", "all")
    assert steps[6].arguments[-1] == "--require-kicad"
    assert all(step.working_directory.is_dir() for step in steps)
    assert [step.timeout_seconds for step in steps] == [
        60,
        60,
        60,
        300,
        300,
        900,
        900,
    ]


def test_release_runner_fails_before_execution_when_any_tool_is_missing(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        runner,
        "missing_tools",
        lambda: ["ngspice", "kicad-cli"],
    )

    def unexpected_run(*_args, **_kwargs):
        raise AssertionError("no starter may run after a failed tool preflight")

    monkeypatch.setattr(runner.subprocess, "run", unexpected_run)
    assert runner.run_steps(runner.steps("python")) == 1


@dataclass
class Completed:
    returncode: int


def test_release_runner_executes_each_declared_step_with_its_own_directory(
    monkeypatch,
) -> None:
    declared = runner.steps("python")
    calls: list[tuple[tuple[str, ...], Path]] = []
    monkeypatch.setattr(runner, "missing_tools", lambda: [])

    def record(arguments, *, cwd, check, timeout):
        assert check is False
        assert timeout > 0
        calls.append((tuple(arguments), cwd))
        return Completed(0)

    monkeypatch.setattr(runner.subprocess, "run", record)
    assert runner.run_steps(declared) == 0
    assert calls == [
        (step.arguments, step.working_directory)
        for step in declared
    ]


def test_release_runner_stops_at_the_first_failed_toolchain(monkeypatch) -> None:
    declared = runner.steps("python")
    calls: list[tuple[str, ...]] = []
    monkeypatch.setattr(runner, "missing_tools", lambda: [])

    def fail_second(arguments, *, cwd, check, timeout):
        del cwd, check, timeout
        calls.append(tuple(arguments))
        return Completed(7 if len(calls) == 2 else 0)

    monkeypatch.setattr(runner.subprocess, "run", fail_second)
    assert runner.run_steps(declared) == 1
    assert calls == [declared[0].arguments, declared[1].arguments]


def test_release_runner_fails_closed_on_a_step_timeout(monkeypatch) -> None:
    declared = runner.steps("python")
    monkeypatch.setattr(runner, "missing_tools", lambda: [])

    def time_out(arguments, *, cwd, check, timeout):
        del cwd, check
        raise runner.subprocess.TimeoutExpired(arguments, timeout)

    monkeypatch.setattr(runner.subprocess, "run", time_out)

    assert runner.run_steps(declared) == 1
