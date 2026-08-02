from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_TOOLS = (
    "cmake",
    "gcc",
    "ninja",
    "ngspice",
    "iverilog",
    "verilator",
    "sby",
    "yosys",
    "z3",
    "kicad-cli",
)


@dataclass(frozen=True)
class Step:
    label: str
    arguments: tuple[str, ...]
    working_directory: Path
    timeout_seconds: int


def steps(python: str = sys.executable) -> tuple[Step, ...]:
    rc = REPO_ROOT / "examples" / "rc-lowpass"
    return (
        Step(
            "RC analytic reference",
            (python, "run.py"),
            rc,
            60,
        ),
        Step(
            "RC ngspice batch",
            ("ngspice", "-o", "build/ngspice.log", "rc_lowpass.cir"),
            rc,
            60,
        ),
        Step(
            "RC ngspice verification",
            (python, "verify_ngspice.py"),
            rc,
            60,
        ),
        Step(
            "ring buffer with ASan and UBSan",
            ("cmake", "--workflow", "--preset", "host-sanitized"),
            REPO_ROOT / "examples" / "ring-buffer",
            300,
        ),
        Step(
            "sensor sampler with ASan and UBSan",
            ("cmake", "--workflow", "--preset", "host-sanitized"),
            REPO_ROOT / "examples" / "sensor-sampler",
            300,
        ),
        Step(
            "synchronous FIFO simulation, formal, and synthesis",
            (python, "run_checks.py", "--require-tools", "all"),
            REPO_ROOT / "examples" / "sync-fifo",
            900,
        ),
        Step(
            "TMP117 KiCad ERC, DRC, parity, and export",
            (python, "export.py", "--require-kicad"),
            REPO_ROOT / "examples" / "tmp117-kicad",
            900,
        ),
    )


def missing_tools() -> list[str]:
    return [tool for tool in REQUIRED_TOOLS if shutil.which(tool) is None]


def run_steps(items: Sequence[Step]) -> int:
    missing = missing_tools()
    if missing:
        print(
            "Executable EE gate failed before execution; missing tool(s): "
            + ", ".join(missing),
            file=sys.stderr,
        )
        return 1

    for step in items:
        relative = step.working_directory.relative_to(REPO_ROOT).as_posix()
        rendered = shlex.join(step.arguments)
        print(f"\n== {step.label} ==")
        print(f"+ ({relative}) {rendered}")
        try:
            completed = subprocess.run(
                step.arguments,
                cwd=step.working_directory,
                check=False,
                timeout=step.timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            print(
                f"Executable EE gate failed: {step.label} exceeded "
                f"{step.timeout_seconds}s",
                file=sys.stderr,
            )
            return 1
        if completed.returncode:
            print(
                f"Executable EE gate failed: {step.label} "
                f"(exit {completed.returncode})",
                file=sys.stderr,
            )
            return 1

    print("\nAll executable EE starter gates passed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the release-blocking RC, sanitized C, FIFO, and KiCad "
            "starter toolchains."
        )
    )
    parser.add_argument(
        "--require-tools",
        choices=("all",),
        required=True,
        help="fail before execution unless every release tool is on PATH",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    return run_steps(steps())


if __name__ == "__main__":
    raise SystemExit(main())
