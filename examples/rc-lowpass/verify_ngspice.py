"""Verify ngspice output for the RC starter without third-party packages."""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path


EXPECTED_TAU_S = 1.0e-3
EXPECTED_TRIGGER_TIME_S = 2.0e-3
EXPECTED_CUTOFF_HZ = 1.0 / (2.0 * math.pi * EXPECTED_TAU_S)
RELATIVE_MODEL_TOLERANCE = 0.005
ABSOLUTE_TAU_TOLERANCE_S = 2.0e-6


def _read_wrdata(
    path: Path,
    *,
    expected_header: tuple[str, str, str],
) -> list[tuple[float, float, float]]:
    rows: list[tuple[float, float, float]] = []
    header_seen = False
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        parts = raw_line.split()
        if not parts:
            continue
        try:
            values = tuple(float(part) for part in parts)
        except ValueError:
            normalized_header = tuple(part.casefold() for part in parts)
            if rows or header_seen or normalized_header != expected_header:
                raise ValueError(
                    f"{path.name}:{line_number} header must be "
                    + " ".join(expected_header)
                )
            header_seen = True
            continue
        if not header_seen:
            raise ValueError(f"{path.name} is missing its vector-name header")
        if len(values) != 3:
            raise ValueError(
                f"{path.name}:{line_number} needs scale plus two vectors, "
                f"got {len(values)} columns"
            )
        if not all(math.isfinite(value) for value in values):
            raise ValueError(f"{path.name}:{line_number} contains non-finite data")
        rows.append((values[0], values[1], values[2]))
    if len(rows) < 3:
        raise ValueError(f"{path.name} needs at least three numeric rows")
    if any(current[0] <= previous[0] for previous, current in zip(rows, rows[1:])):
        raise ValueError(f"{path.name} scale must be strictly increasing")
    return rows


def _crossing(
    rows: list[tuple[float, float, float]],
    *,
    column: int,
    target: float,
) -> float:
    for previous, current in zip(rows, rows[1:]):
        y0 = previous[column]
        y1 = current[column]
        if y0 <= target <= y1 and y1 != y0:
            fraction = (target - y0) / (y1 - y0)
            return previous[0] + fraction * (current[0] - previous[0])
    raise ValueError(f"column {column} does not cross {target}")


def verify_outputs(build_dir: Path) -> dict[str, float]:
    log_path = build_dir / "ngspice.log"
    log = log_path.read_text(encoding="utf-8", errors="replace")
    lowered_log = log.casefold()
    if (
        re.search(
            r"\bmeas(?:ure(?:ment)?)?\b[^\r\n]*\bfailed\b",
            lowered_log,
        )
        or "error:" in lowered_log
    ):
        raise ValueError("ngspice log reports a failed measurement or error")
    if not lowered_log.strip():
        raise ValueError("ngspice log is empty")
    missing_measurements = [
        name for name in ("t0", "t63", "tau63", "f3db") if name not in lowered_log
    ]
    if missing_measurements:
        raise ValueError(
            "ngspice log is missing printed measurement(s): "
            + ", ".join(missing_measurements)
        )

    step_rows = _read_wrdata(
        build_dir / "ngspice_step.dat",
        expected_header=("time", "v(in)", "v(out)"),
    )
    t0 = _crossing(step_rows, column=1, target=0.5)
    if not math.isclose(
        t0,
        EXPECTED_TRIGGER_TIME_S,
        rel_tol=RELATIVE_MODEL_TOLERANCE,
        abs_tol=ABSOLUTE_TAU_TOLERANCE_S,
    ):
        raise ValueError(
            f"trigger mismatch: expected {EXPECTED_TRIGGER_TIME_S}, got {t0}"
        )
    t63 = _crossing(
        step_rows,
        column=2,
        target=1.0 - 1.0 / math.e,
    )
    tau_s = t63 - t0
    if not math.isclose(
        tau_s,
        EXPECTED_TAU_S,
        rel_tol=RELATIVE_MODEL_TOLERANCE,
        abs_tol=ABSOLUTE_TAU_TOLERANCE_S,
    ):
        raise ValueError(f"tau mismatch: expected {EXPECTED_TAU_S}, got {tau_s}")

    ac_rows = _read_wrdata(
        build_dir / "ngspice_ac.dat",
        expected_header=("frequency", "real(h)", "imag(h)"),
    )
    gains = [math.hypot(real, imaginary) for _frequency, real, imaginary in ac_rows]
    target_gain = gains[0] / math.sqrt(2.0)
    cutoff_hz: float | None = None
    for index in range(1, len(ac_rows)):
        if gains[index] <= target_gain:
            f0, f1 = ac_rows[index - 1][0], ac_rows[index][0]
            g0_db = 20.0 * math.log10(gains[index - 1] / gains[0])
            g1_db = 20.0 * math.log10(gains[index] / gains[0])
            target_db = 20.0 * math.log10(target_gain / gains[0])
            fraction = (target_db - g0_db) / (g1_db - g0_db)
            cutoff_hz = 10.0 ** (
                math.log10(f0) + fraction * (math.log10(f1) - math.log10(f0))
            )
            break
    if cutoff_hz is None:
        raise ValueError("AC data does not bracket the half-power cutoff")
    if not math.isclose(
        cutoff_hz,
        EXPECTED_CUTOFF_HZ,
        rel_tol=RELATIVE_MODEL_TOLERANCE,
    ):
        raise ValueError(
            f"cutoff mismatch: expected {EXPECTED_CUTOFF_HZ}, got {cutoff_hz}"
        )

    return {
        "trigger_time_s": t0,
        "threshold_crossing_time_s": t63,
        "tau_63_2_s": tau_s,
        "cutoff_hz": cutoff_hz,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--build-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "build",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        summary = verify_outputs(args.build_dir)
    except (OSError, ValueError) as exc:
        print(f"ngspice_verification=FAIL: {exc}")
        return 1
    for key, value in summary.items():
        print(f"{key}={value:.12g}")
    print("ngspice_verification=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
