"""Generate deterministic analytic reference data for an ideal RC low-pass.

This module does not read an instrument and does not invoke a circuit solver.
Every sample is calculated from the equations stated in README.md.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
from pathlib import Path
from typing import Any

RESISTANCE_OHM = 1_000.0
CAPACITANCE_F = 1.0e-6
INPUT_STEP_V = 1.0
TRIGGER_TIME_S = 2.0e-3
STEP_INTERVAL_S = 10.0e-6
STEP_STOP_S = 14.0e-3
AC_START_HZ = 1.0
AC_STOP_HZ = 100_000.0
AC_POINTS_PER_DECADE = 20


def _format_number(value: float) -> str:
    return format(value, ".12g")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65_536), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_step_csv(path: Path) -> int:
    sample_count = round(STEP_STOP_S / STEP_INTERVAL_S) + 1
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("time_s", "input_v", "output_v", "trigger"))
        for index in range(sample_count):
            time_s = index * STEP_INTERVAL_S
            triggered = time_s >= TRIGGER_TIME_S
            input_v = INPUT_STEP_V if triggered else 0.0
            elapsed_s = time_s - TRIGGER_TIME_S
            output_v = (
                INPUT_STEP_V
                * (1.0 - math.exp(-elapsed_s / (RESISTANCE_OHM * CAPACITANCE_F)))
                if triggered
                else 0.0
            )
            writer.writerow(
                (
                    _format_number(time_s),
                    _format_number(input_v),
                    _format_number(output_v),
                    "1" if triggered else "0",
                )
            )
    return sample_count


def _ac_frequencies() -> list[float]:
    decades = math.log10(AC_STOP_HZ / AC_START_HZ)
    regular_count = round(decades * AC_POINTS_PER_DECADE)
    frequencies = {
        AC_START_HZ * 10.0 ** (index / AC_POINTS_PER_DECADE)
        for index in range(regular_count + 1)
    }
    frequencies.add(1.0 / (2.0 * math.pi * RESISTANCE_OHM * CAPACITANCE_F))
    return sorted(frequencies)


def _write_ac_csv(path: Path) -> int:
    frequencies = _ac_frequencies()
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("frequency_hz", "h_real", "h_imag"))
        for frequency_hz in frequencies:
            normalized_frequency = (
                2.0 * math.pi * frequency_hz * RESISTANCE_OHM * CAPACITANCE_F
            )
            denominator = 1.0 + normalized_frequency**2
            writer.writerow(
                (
                    _format_number(frequency_hz),
                    _format_number(1.0 / denominator),
                    _format_number(-normalized_frequency / denominator),
                )
            )
    return len(frequencies)


def generate_reference(output_dir: Path) -> dict[str, Any]:
    """Write deterministic CSV files and their provenance manifest."""

    output_dir.mkdir(parents=True, exist_ok=True)
    step_path = output_dir / "analytic_step.csv"
    ac_path = output_dir / "analytic_ac.csv"

    step_samples = _write_step_csv(step_path)
    ac_samples = _write_ac_csv(ac_path)

    manifest: dict[str, Any] = {
        "schema_version": 1,
        "data_kind": "analytic_reference",
        "measurement_claim": False,
        "randomness": "none",
        "generator": {
            "file": "generate_reference.py",
            "sha256": _sha256(Path(__file__).resolve()),
            "python_version": platform.python_version(),
            "model": "ideal first-order RC low-pass",
            "equations": {
                "step": "vout=0 before t0; vout=Vin*(1-exp(-(t-t0)/(R*C))) at and after t0",
                "transfer": "H(jw)=1/(1+j*w*R*C)",
            },
        },
        "parameters": {
            "resistance_ohm": RESISTANCE_OHM,
            "capacitance_f": CAPACITANCE_F,
            "input_step_v": INPUT_STEP_V,
            "trigger_time_s": TRIGGER_TIME_S,
        },
        "sampling": {
            "step_interval_s": STEP_INTERVAL_S,
            "step_stop_s": STEP_STOP_S,
            "ac_start_hz": AC_START_HZ,
            "ac_stop_hz": AC_STOP_HZ,
            "ac_points_per_decade": AC_POINTS_PER_DECADE,
        },
        "files": {
            step_path.name: {
                "columns": {
                    "time_s": "s",
                    "input_v": "V",
                    "output_v": "V",
                    "trigger": "0 before t0, 1 at and after t0",
                },
                "rows": step_samples,
                "sha256": _sha256(step_path),
            },
            ac_path.name: {
                "columns": {
                    "frequency_hz": "Hz",
                    "h_real": "V/V",
                    "h_imag": "V/V",
                },
                "rows": ac_samples,
                "sha256": _sha256(ac_path),
            },
        },
        "limitations": [
            "Ideal linear resistor and capacitor only.",
            "No component tolerance, parasitic, source impedance, load, noise, or instrument model.",
            "Equation-generated values are neither ngspice output nor laboratory measurement.",
        ],
    }
    manifest_path = output_dir / "manifest.json"
    with manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )
    return manifest


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate deterministic analytic RC low-pass reference data."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "build",
        help="Directory for generated CSV files and manifest.json.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    manifest = generate_reference(args.output_dir)
    print(f"data_kind={manifest['data_kind']}")
    print(f"measurement_claim={str(manifest['measurement_claim']).lower()}")
    print(f"output_dir={args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
