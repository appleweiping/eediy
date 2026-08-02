"""One-command, offline rebuild and verification for the RC starter."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from analyze import analyze_directory
from generate_reference import generate_reference


KNOWN_OUTPUTS = (
    "analytic_step.csv",
    "analytic_ac.csv",
    "manifest.json",
    "summary.json",
    "ngspice.log",
    "ngspice_step.dat",
    "ngspice_ac.dat",
)


def _clear_known_outputs(output_dir: Path) -> None:
    """Remove only files this starter owns so stale solver data cannot survive."""

    for filename in KNOWN_OUTPUTS:
        path = output_dir / filename
        if path.is_file() or path.is_symlink():
            path.unlink()


def _lookup(payload: dict[str, Any], dotted_path: str) -> Any:
    value: Any = payload
    for component in dotted_path.split("."):
        value = value[component]
    return value


def verify_summary(summary: dict[str, Any], acceptance_path: Path) -> None:
    acceptance = json.loads(acceptance_path.read_text(encoding="utf-8"))
    for path, expected in acceptance["exact"].items():
        actual = _lookup(summary, path)
        if actual != expected:
            raise ValueError(f"{path}: expected {expected!r}, got {actual!r}")

    for check in acceptance["numeric"]:
        actual = float(_lookup(summary, check["path"]))
        expected = float(check["expected"])
        if "absolute_tolerance" in check:
            tolerance = float(check["absolute_tolerance"])
            passed = abs(actual - expected) <= tolerance
        else:
            tolerance = float(check["relative_tolerance"])
            passed = math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0)
        if not passed:
            raise ValueError(
                f"{check['path']}: expected {expected} within {tolerance}, got {actual}"
            )

    for check in acceptance["upper_bounds"]:
        actual = float(_lookup(summary, check["path"]))
        maximum = float(check["maximum"])
        if actual > maximum:
            raise ValueError(f"{check['path']}: expected <= {maximum}, got {actual}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate, analyze, and verify the offline RC low-pass starter."
    )
    script_dir = Path(__file__).resolve().parent
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=script_dir / "build",
        help="Disposable directory for generated data and summary.",
    )
    parser.add_argument(
        "--acceptance",
        type=Path,
        default=script_dir / "expected" / "acceptance.json",
        help="Predeclared numerical and provenance checks.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        _clear_known_outputs(args.output_dir)
        generate_reference(args.output_dir)
        summary_path = args.output_dir / "summary.json"
        summary = analyze_directory(args.output_dir, summary_path)
        verify_summary(summary, args.acceptance)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"verification=FAIL: {exc}")
        return 1

    print(f"data_kind={summary['data_kind']}")
    print(f"measurement_claim={str(summary['measurement_claim']).lower()}")
    print(f"trigger_time_s={summary['step']['trigger_time_s']:.9g}")
    print(
        "threshold_crossing_time_s="
        f"{summary['step']['threshold_crossing_time_s']:.9g}"
    )
    print(f"tau_63_2_s={summary['step']['tau_63_2_s']:.9g}")
    print(f"cutoff_hz={summary['ac']['cutoff_hz']:.9g}")
    print(f"phase_at_cutoff_deg={summary['ac']['phase_at_cutoff_deg']:.9g}")
    print(f"summary={summary_path.resolve()}")
    print("verification=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
