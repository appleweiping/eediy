#!/usr/bin/env python3
"""Run every locally available sync-FIFO verification path.

The runner never substitutes a source scan or a stored log for an installed
EDA tool. Missing tools are explicit skips by default and hard failures with
``--require-tools all``.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

EXAMPLE_DIR = Path(__file__).resolve().parent
BUILD_DIR = EXAMPLE_DIR / "build"
CHECK_NAMES = ("icarus", "verilator", "formal", "synthesis")
COMMAND_TIMEOUT_SECONDS = 600
VERSION_TIMEOUT_SECONDS = 30


class CheckFailure(RuntimeError):
    """Raised when a real tool run violates the expected result."""


@dataclass(frozen=True)
class Check:
    name: str
    executables: tuple[str, ...]
    run: Callable[[], None]


def _command_text(command: Sequence[os.PathLike[str] | str]) -> str:
    return " ".join(str(part) for part in command)


def _run(
    command: Sequence[os.PathLike[str] | str],
    *,
    expected_returncode: int | None = 0,
) -> subprocess.CompletedProcess[str]:
    printable = _command_text(command)
    print(f"RUN {printable}", flush=True)
    try:
        completed = subprocess.run(
            [str(part) for part in command],
            cwd=EXAMPLE_DIR,
            check=False,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise CheckFailure(
            f"command exceeded {COMMAND_TIMEOUT_SECONDS}s timeout: {printable}"
        ) from exc
    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.stderr:
        print(completed.stderr, end="" if completed.stderr.endswith("\n") else "\n")
    if (
        expected_returncode is not None
        and completed.returncode != expected_returncode
    ):
        raise CheckFailure(
            f"command returned {completed.returncode}, expected "
            f"{expected_returncode}: {printable}"
        )
    return completed


def _reset_directory(path: Path) -> None:
    resolved = path.resolve()
    build_root = BUILD_DIR.resolve()
    if resolved == build_root or build_root not in resolved.parents:
        raise CheckFailure(f"refusing to clear path outside build/: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True)


def _require_marker(
    completed: subprocess.CompletedProcess[str],
    marker: str,
    *,
    context: str,
) -> None:
    combined = completed.stdout + completed.stderr
    if marker not in combined:
        raise CheckFailure(f"{context} did not emit required marker {marker!r}")


def _require_expected_failure(
    completed: subprocess.CompletedProcess[str],
    *,
    marker: str,
    context: str,
) -> None:
    if completed.returncode == 0:
        raise CheckFailure(f"{context} unexpectedly returned success")
    _require_marker(completed, marker, context=context)


def _run_icarus() -> None:
    baseline_dir = BUILD_DIR / "icarus-baseline"
    fault_dir = BUILD_DIR / "icarus-fault"
    _reset_directory(baseline_dir)
    _reset_directory(fault_dir)

    baseline_binary = baseline_dir / "fifo.vvp"
    _run(
        (
            "iverilog",
            "-g2012",
            "-Wall",
            "-s",
            "fifo_tb",
            "-o",
            baseline_binary,
            "-c",
            "sim/rtl.f",
        )
    )
    baseline = _run(("vvp", baseline_binary))
    _require_marker(
        baseline,
        "SYNC_FIFO_SIM_PASS revision=baseline",
        context="Icarus baseline",
    )

    fault_binary = fault_dir / "fifo.vvp"
    _run(
        (
            "iverilog",
            "-g2012",
            "-Wall",
            "-DFAULT_READ_POINTER",
            "-s",
            "fifo_tb",
            "-o",
            fault_binary,
            "-c",
            "sim/rtl.f",
        )
    )
    fault = _run(("vvp", fault_binary), expected_returncode=None)
    _require_expected_failure(
        fault,
        marker="SYNC_FIFO_MISMATCH",
        context="Icarus read-pointer negative control",
    )


def _verilator_binary(directory: Path) -> Path:
    base = directory / "fifo_tb"
    windows_candidate = base.with_suffix(".exe")
    return windows_candidate if windows_candidate.exists() else base


def _run_verilator() -> None:
    baseline_dir = BUILD_DIR / "verilator-baseline"
    fault_dir = BUILD_DIR / "verilator-fault"
    _reset_directory(baseline_dir)
    _reset_directory(fault_dir)

    common = (
        "verilator",
        "--binary",
        "--timing",
        "--assert",
        "--top-module",
        "fifo_tb",
        "-Wall",
        "-f",
        "sim/rtl.f",
    )
    _run(
        (
            *common,
            "--Mdir",
            baseline_dir,
            "-o",
            "fifo_tb",
        )
    )
    baseline = _run((_verilator_binary(baseline_dir),))
    _require_marker(
        baseline,
        "SYNC_FIFO_SIM_PASS revision=baseline",
        context="Verilator baseline",
    )

    _run(
        (
            *common,
            "-DFAULT_READ_POINTER",
            "--Mdir",
            fault_dir,
            "-o",
            "fifo_tb",
        )
    )
    fault = _run((_verilator_binary(fault_dir),), expected_returncode=None)
    _require_expected_failure(
        fault,
        marker="SYNC_FIFO_MISMATCH",
        context="Verilator read-pointer negative control",
    )


def _assert_sby_pass(workdir: Path, context: str) -> None:
    status_path = workdir / "status"
    if not status_path.is_file():
        raise CheckFailure(f"{context} did not create {status_path}")
    status = status_path.read_text(encoding="utf-8").strip()
    status_fields = status.split()
    if not status_fields or status_fields[0] != "PASS":
        raise CheckFailure(f"{context} status was {status!r}, expected 'PASS'")


def _assert_sby_expected_assertion_failure(workdir: Path) -> Path:
    status_path = workdir / "status"
    if not status_path.is_file():
        raise CheckFailure(
            f"SymbiYosys fault did not create {status_path}"
        )
    status = status_path.read_text(encoding="utf-8").strip()
    status_fields = status.split()
    if not status_fields or status_fields[0] != "FAIL":
        raise CheckFailure(
            f"SymbiYosys fault status was {status!r}, expected 'FAIL'"
        )

    failure_summary = workdir / "FAIL"
    if not failure_summary.is_file() or failure_summary.stat().st_size == 0:
        raise CheckFailure(
            "SymbiYosys fault did not create a non-empty FAIL summary"
        )
    summary = failure_summary.read_text(encoding="utf-8")
    if "failed assertion" not in summary or "counterexample trace:" not in summary:
        raise CheckFailure(
            "SymbiYosys fault did not report an assertion counterexample"
        )

    traces = sorted(
        path
        for path in workdir.rglob("trace*.vcd")
        if path.is_file() and path.stat().st_size > 0
    )
    if not traces:
        raise CheckFailure(
            "SymbiYosys assertion failure did not generate a non-empty "
            "counterexample VCD"
        )
    return traces[0]


def _run_formal() -> None:
    bmc_dir = BUILD_DIR / "formal-baseline-bmc"
    cover_dir = BUILD_DIR / "formal-baseline-cover"
    fault_dir = BUILD_DIR / "formal-fault"
    for directory in (bmc_dir, cover_dir, fault_dir):
        _reset_directory(directory)
        directory.rmdir()

    _run(
        (
            "sby",
            "-f",
            "-d",
            bmc_dir,
            "formal/baseline.sby",
            "bmc",
        )
    )
    _assert_sby_pass(bmc_dir, "SymbiYosys baseline bounded safety check")

    _run(
        (
            "sby",
            "-f",
            "-d",
            cover_dir,
            "formal/baseline.sby",
            "cover",
        )
    )
    _assert_sby_pass(cover_dir, "SymbiYosys baseline cover")

    fault = _run(
        (
            "sby",
            "-f",
            "-d",
            fault_dir,
            "formal/fault-read-pointer.sby",
        ),
        expected_returncode=None,
    )
    if fault.returncode == 0:
        raise CheckFailure(
            "SymbiYosys read-pointer fault unexpectedly returned success"
        )
    trace = _assert_sby_expected_assertion_failure(fault_dir)
    print(f"COUNTEREXAMPLE {trace.relative_to(EXAMPLE_DIR)}")


def _run_synthesis() -> None:
    synthesis_dir = BUILD_DIR / "synth"
    _reset_directory(synthesis_dir)
    _run(("yosys", "-q", "-s", "synth/synth.ys"))
    for output in (
        synthesis_dir / "stat.txt",
        synthesis_dir / "sync_fifo.json",
    ):
        if not output.is_file() or output.stat().st_size == 0:
            raise CheckFailure(f"Yosys did not create non-empty {output}")


def _checks() -> dict[str, Check]:
    return {
        "icarus": Check("icarus", ("iverilog", "vvp"), _run_icarus),
        "verilator": Check("verilator", ("verilator",), _run_verilator),
        "formal": Check("formal", ("sby", "yosys", "yosys-smtbmc", "z3"), _run_formal),
        "synthesis": Check("synthesis", ("yosys",), _run_synthesis),
    }


def _print_versions(selected_checks: Sequence[Check]) -> None:
    version_commands: dict[str, tuple[str, ...]] = {
        "iverilog": ("iverilog", "-V"),
        "vvp": ("vvp", "-V"),
        "verilator": ("verilator", "--version"),
        "sby": ("sby", "--version"),
        "yosys": ("yosys", "-V"),
        "z3": ("z3", "--version"),
    }
    seen: set[str] = set()
    for check in selected_checks:
        for executable in check.executables:
            if executable in seen or shutil.which(executable) is None:
                continue
            seen.add(executable)
            if executable not in version_commands:
                print(
                    f"TOOL_PRESENT executable={executable} "
                    "version_source=yosys"
                )
                continue
            command = version_commands[executable]
            try:
                completed = subprocess.run(
                    command,
                    cwd=EXAMPLE_DIR,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=VERSION_TIMEOUT_SECONDS,
                )
            except subprocess.TimeoutExpired:
                print(
                    f"TOOL_VERSION executable={executable} "
                    f"returncode=timeout value=version command exceeded "
                    f"{VERSION_TIMEOUT_SECONDS}s"
                )
                continue
            first_line = (completed.stdout + completed.stderr).strip().splitlines()
            version = first_line[0] if first_line else "version command produced no text"
            print(
                f"TOOL_VERSION executable={executable} "
                f"returncode={completed.returncode} value={version}"
            )


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run installed simulation, formal, and synthesis checks."
    )
    parser.add_argument(
        "--only",
        action="append",
        choices=CHECK_NAMES,
        help="run only this check; repeat to select more than one",
    )
    parser.add_argument(
        "--require-tools",
        choices=("none", "all"),
        default="none",
        help="make a missing executable fail instead of skip",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    all_checks = _checks()
    selected_names = tuple(args.only) if args.only else CHECK_NAMES
    selected = [all_checks[name] for name in selected_names]
    _print_versions(selected)

    passed = 0
    skipped = 0
    failed = 0
    for check in selected:
        missing = [
            executable
            for executable in check.executables
            if shutil.which(executable) is None
        ]
        if missing:
            if args.require_tools == "all":
                failed += 1
                print(
                    f"CHECK_FAIL name={check.name} "
                    f"reason=missing_executables:{','.join(missing)}"
                )
            else:
                skipped += 1
                print(
                    f"CHECK_SKIP name={check.name} "
                    f"reason=missing_executables:{','.join(missing)}"
                )
            continue

        try:
            check.run()
        except (CheckFailure, OSError) as error:
            failed += 1
            print(f"CHECK_FAIL name={check.name} reason={error}")
        else:
            passed += 1
            print(f"CHECK_PASS name={check.name}")

    print(
        f"CHECK_SUMMARY passed={passed} skipped={skipped} failed={failed}"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
