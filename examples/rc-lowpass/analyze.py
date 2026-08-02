"""Analyze the RC analytic reference using only the Python standard library."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65_536), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_manifest(input_dir: Path) -> dict[str, Any]:
    manifest_path = input_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing provenance manifest: {manifest_path}") from exc

    if manifest.get("data_kind") != "analytic_reference":
        raise ValueError("this analyzer expects data_kind=analytic_reference")
    if manifest.get("measurement_claim") is not False:
        raise ValueError("analytic reference must set measurement_claim=false")

    for filename in ("analytic_step.csv", "analytic_ac.csv"):
        path = input_dir / filename
        try:
            expected = manifest["files"][filename]["sha256"]
        except KeyError as exc:
            raise ValueError(f"manifest does not describe {filename}") from exc
        actual = _sha256(path)
        if actual != expected:
            raise ValueError(
                f"checksum mismatch for {filename}: expected {expected}, got {actual}"
            )
    return manifest


def _read_numeric_csv(path: Path, required_columns: tuple[str, ...]) -> list[dict[str, float]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(required_columns):
            raise ValueError(
                f"{path.name} columns must be {list(required_columns)}, "
                f"got {reader.fieldnames}"
            )
        rows: list[dict[str, float]] = []
        for line_number, row in enumerate(reader, start=2):
            try:
                parsed = {name: float(row[name]) for name in required_columns}
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"{path.name}:{line_number} contains a non-numeric value"
                ) from exc
            if not all(math.isfinite(value) for value in parsed.values()):
                raise ValueError(f"{path.name}:{line_number} contains a non-finite value")
            rows.append(parsed)
    if len(rows) < 3:
        raise ValueError(f"{path.name} needs at least three rows")
    return rows


def _linear_crossing(
    x0: float, y0: float, x1: float, y1: float, target: float
) -> float:
    if x1 <= x0:
        raise ValueError("interpolation coordinates must increase")
    if y1 == y0:
        raise ValueError("cannot interpolate across equal values")
    fraction = (target - y0) / (y1 - y0)
    if not 0.0 <= fraction <= 1.0:
        raise ValueError("target is not bracketed")
    return x0 + fraction * (x1 - x0)


def _analyze_step(rows: list[dict[str, float]]) -> dict[str, Any]:
    times = [row["time_s"] for row in rows]
    if any(current <= previous for previous, current in zip(times, times[1:])):
        raise ValueError("step time_s must be strictly increasing")

    triggers = [row["trigger"] for row in rows]
    if any(value not in (0.0, 1.0) for value in triggers):
        raise ValueError("trigger must contain only 0 or 1")
    try:
        trigger_index = triggers.index(1.0)
    except ValueError as exc:
        raise ValueError("step data has no trigger transition") from exc
    if trigger_index == 0 or any(value != 0.0 for value in triggers[:trigger_index]):
        raise ValueError("trigger needs a pre-trigger baseline")
    if any(value != 1.0 for value in triggers[trigger_index:]):
        raise ValueError("trigger must remain asserted after the transition")

    trigger_time_s = times[trigger_index]
    outputs = [row["output_v"] for row in rows]
    baseline_v = sum(outputs[:trigger_index]) / trigger_index
    tail_count = max(10, len(outputs) // 20)
    final_v = sum(outputs[-tail_count:]) / tail_count
    if final_v <= baseline_v:
        raise ValueError("this starter expects a rising step response")

    threshold_fraction = 1.0 - 1.0 / math.e
    threshold_v = baseline_v + threshold_fraction * (final_v - baseline_v)
    crossing_time_s: float | None = None
    for index in range(max(trigger_index, 1), len(rows)):
        previous_v = outputs[index - 1]
        current_v = outputs[index]
        if previous_v <= threshold_v <= current_v:
            crossing_time_s = _linear_crossing(
                times[index - 1],
                previous_v,
                times[index],
                current_v,
                threshold_v,
            )
            break
    if crossing_time_s is None:
        raise ValueError("output never crosses the 63.2% threshold")

    tau_s = crossing_time_s - trigger_time_s
    if tau_s <= 0.0:
        raise ValueError("estimated time constant must be positive")
    return {
        "method": "linear interpolation at 1-1/e of the observed final change",
        "trigger_time_s": trigger_time_s,
        "threshold_fraction": threshold_fraction,
        "threshold_v": threshold_v,
        "threshold_crossing_time_s": crossing_time_s,
        "tau_63_2_s": tau_s,
        "baseline_v": baseline_v,
        "observed_final_v": final_v,
        "delay_exclusion": "tau_63_2_s = threshold_crossing_time_s - trigger_time_s",
    }


def _interpolate_at_log_frequency(
    frequency_hz: list[float], values: list[float], target_frequency_hz: float
) -> float:
    for index in range(1, len(frequency_hz)):
        if frequency_hz[index] >= target_frequency_hz:
            x0 = math.log10(frequency_hz[index - 1])
            x1 = math.log10(frequency_hz[index])
            target_x = math.log10(target_frequency_hz)
            fraction = (target_x - x0) / (x1 - x0)
            return values[index - 1] + fraction * (
                values[index] - values[index - 1]
            )
    raise ValueError("target frequency lies outside AC sweep")


def _analyze_ac(rows: list[dict[str, float]]) -> dict[str, Any]:
    frequencies = [row["frequency_hz"] for row in rows]
    if frequencies[0] <= 0.0 or any(
        current <= previous for previous, current in zip(frequencies, frequencies[1:])
    ):
        raise ValueError("frequency_hz must be positive and strictly increasing")

    real_parts = [row["h_real"] for row in rows]
    imaginary_parts = [row["h_imag"] for row in rows]
    gains = [
        math.hypot(real, imaginary)
        for real, imaginary in zip(real_parts, imaginary_parts)
    ]
    phases_deg = [
        math.degrees(math.atan2(imaginary, real))
        for real, imaginary in zip(real_parts, imaginary_parts)
    ]
    if any(current > previous * (1.0 + 1.0e-10) for previous, current in zip(gains, gains[1:])):
        raise ValueError("this starter expects monotonic low-pass gain")

    low_frequency_gain = gains[0]
    target_gain = low_frequency_gain / math.sqrt(2.0)
    target_db = 20.0 * math.log10(target_gain / low_frequency_gain)

    cutoff_hz: float | None = None
    bracket_index: int | None = None
    normalized_gain_db = [
        20.0 * math.log10(gain / low_frequency_gain) for gain in gains
    ]
    for index in range(1, len(rows)):
        if normalized_gain_db[index] <= target_db:
            log_frequency = _linear_crossing(
                math.log10(frequencies[index - 1]),
                normalized_gain_db[index - 1],
                math.log10(frequencies[index]),
                normalized_gain_db[index],
                target_db,
            )
            cutoff_hz = 10.0**log_frequency
            bracket_index = index
            break
    if cutoff_hz is None or bracket_index is None:
        raise ValueError("AC sweep does not bracket the half-power cutoff")

    gain_at_cutoff = _interpolate_at_log_frequency(
        frequencies, gains, cutoff_hz
    )
    phase_at_cutoff_deg = _interpolate_at_log_frequency(
        frequencies, phases_deg, cutoff_hz
    )
    return {
        "criterion": "gain = first-frequency gain / sqrt(2) (-3.0103 dB)",
        "first_frequency_hz": frequencies[0],
        "low_frequency_gain_v_per_v": low_frequency_gain,
        "cutoff_hz": cutoff_hz,
        "gain_at_cutoff_v_per_v": gain_at_cutoff,
        "phase_at_cutoff_deg": phase_at_cutoff_deg,
    }


def analyze_directory(input_dir: Path, output_path: Path) -> dict[str, Any]:
    """Verify provenance, calculate step/AC metrics, and write a summary."""

    manifest = _load_manifest(input_dir)
    step_rows = _read_numeric_csv(
        input_dir / "analytic_step.csv",
        ("time_s", "input_v", "output_v", "trigger"),
    )
    ac_rows = _read_numeric_csv(
        input_dir / "analytic_ac.csv",
        ("frequency_hz", "h_real", "h_imag"),
    )
    step = _analyze_step(step_rows)
    ac = _analyze_ac(ac_rows)
    tau_from_ac_s = 1.0 / (2.0 * math.pi * ac["cutoff_hz"])
    relative_difference = abs(tau_from_ac_s - step["tau_63_2_s"]) / step[
        "tau_63_2_s"
    ]

    summary: dict[str, Any] = {
        "schema_version": 1,
        "data_kind": manifest["data_kind"],
        "measurement_claim": manifest["measurement_claim"],
        "step": step,
        "ac": ac,
        "cross_check": {
            "tau_from_ac_s": tau_from_ac_s,
            "relative_difference_between_step_and_ac": relative_difference,
            "relation": "tau = 1/(2*pi*fc)",
        },
        "limitations": manifest["limitations"],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(
            json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )
    return summary


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze checksum-verified analytic RC reference data."
    )
    script_dir = Path(__file__).resolve().parent
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=script_dir / "build",
        help="Directory containing manifest.json and analytic CSV files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=script_dir / "build" / "summary.json",
        help="Path for the deterministic JSON summary.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        summary = analyze_directory(args.input_dir, args.output)
    except (OSError, ValueError, KeyError) as exc:
        print(f"analysis=FAIL: {exc}")
        return 1
    print(f"data_kind={summary['data_kind']}")
    print(f"measurement_claim={str(summary['measurement_claim']).lower()}")
    print(f"tau_63_2_s={summary['step']['tau_63_2_s']:.9g}")
    print(f"cutoff_hz={summary['ac']['cutoff_hz']:.9g}")
    print(f"summary={args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
