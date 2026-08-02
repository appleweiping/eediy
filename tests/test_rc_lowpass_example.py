from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = REPO_ROOT / "examples" / "rc-lowpass"


def _run_starter(output_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(EXAMPLE_DIR / "run.py"),
            "--output-dir",
            str(output_dir),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_offline_rebuild_recovers_tau_and_cutoff_without_counting_delay(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "result"
    completed = _run_starter(output_dir)

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "measurement_claim=false" in completed.stdout
    assert "verification=PASS" in completed.stdout

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["data_kind"] == "analytic_reference"
    assert summary["measurement_claim"] is False

    step = summary["step"]
    assert abs(step["trigger_time_s"] - 0.002) <= 1e-12
    assert abs(step["threshold_crossing_time_s"] - 0.003) <= 2e-7
    assert abs(step["tau_63_2_s"] - 0.001) <= 2e-7
    assert abs(
        step["threshold_crossing_time_s"]
        - step["trigger_time_s"]
        - step["tau_63_2_s"]
    ) <= 1e-15
    assert step["threshold_crossing_time_s"] > 2.5 * step["tau_63_2_s"]

    ac = summary["ac"]
    assert abs(ac["cutoff_hz"] - 159.15494309189535) / 159.15494309189535 < 0.001
    assert abs(ac["phase_at_cutoff_deg"] + 45.0) < 0.2
    assert (
        summary["cross_check"]["relative_difference_between_step_and_ac"] < 0.002
    )


def test_analytic_reference_is_byte_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first_run = _run_starter(first)
    second_run = _run_starter(second)

    assert first_run.returncode == 0, first_run.stdout + first_run.stderr
    assert second_run.returncode == 0, second_run.stdout + second_run.stderr
    for filename in (
        "analytic_step.csv",
        "analytic_ac.csv",
        "manifest.json",
        "summary.json",
    ):
        assert _digest(first / filename) == _digest(second / filename)


def test_analysis_rejects_a_tampered_reference_file(tmp_path: Path) -> None:
    output_dir = tmp_path / "tampered"
    completed = _run_starter(output_dir)
    assert completed.returncode == 0, completed.stdout + completed.stderr

    step_path = output_dir / "analytic_step.csv"
    step_path.write_text(
        step_path.read_text(encoding="utf-8").replace(
            "0.003,1,0.632120558829,1",
            "0.003,1,0.9,1",
            1,
        ),
        encoding="utf-8",
    )
    analysis = subprocess.run(
        [
            sys.executable,
            str(EXAMPLE_DIR / "analyze.py"),
            "--input-dir",
            str(output_dir),
            "--output",
            str(output_dir / "tampered-summary.json"),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert analysis.returncode != 0
    assert "checksum mismatch for analytic_step.csv" in analysis.stdout
    assert not (output_dir / "tampered-summary.json").exists()


def test_rebuild_removes_stale_ngspice_outputs(tmp_path: Path) -> None:
    output_dir = tmp_path / "stale"
    output_dir.mkdir()
    stale_step = output_dir / "ngspice_step.dat"
    stale_ac = output_dir / "ngspice_ac.dat"
    stale_log = output_dir / "ngspice.log"
    stale_step.write_text("not current simulation data\n", encoding="utf-8")
    stale_ac.write_text("not current simulation data\n", encoding="utf-8")
    stale_log.write_text("old solver run\n", encoding="utf-8")

    completed = _run_starter(output_dir)

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert not stale_step.exists()
    assert not stale_ac.exists()
    assert not stale_log.exists()


def test_ngspice_output_verifier_checks_numeric_files(tmp_path: Path) -> None:
    build_dir = tmp_path / "ngspice"
    build_dir.mkdir()
    (build_dir / "ngspice.log").write_text(
        "ngspice integration fixture: t0 t63 tau63 f3db\n",
        encoding="utf-8",
    )
    (build_dir / "ngspice_step.dat").write_text(
        "\n".join(
            (
                "time v(in) v(out)",
                "0 0 0",
                "0.002 0 0",
                "0.0020001 1 0.000099995",
                "0.003 1 0.6321205588",
                "0.014 1 0.9999938558",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    (build_dir / "ngspice_ac.dat").write_text(
        "\n".join(
            (
                "frequency real(h) imag(h)",
                "1 0.9999605231 -0.0062829373",
                "100 0.7169568003 -0.4504772434",
                "159.1549431 0.5 -0.5",
                "1000 0.024704523 -0.1552230961",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(EXAMPLE_DIR / "verify_ngspice.py"),
            "--build-dir",
            str(build_dir),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "ngspice_verification=PASS" in completed.stdout


def test_ngspice_output_verifier_rejects_solver_errors(tmp_path: Path) -> None:
    build_dir = tmp_path / "ngspice-error"
    build_dir.mkdir()
    (build_dir / "ngspice.log").write_text(
        "Error: singular matrix\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(EXAMPLE_DIR / "verify_ngspice.py"),
            "--build-dir",
            str(build_dir),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "ngspice_verification=FAIL" in completed.stdout


def test_ngspice_output_verifier_rejects_named_measurement_failure(
    tmp_path: Path,
) -> None:
    build_dir = tmp_path / "ngspice-measurement-error"
    build_dir.mkdir()
    (build_dir / "ngspice.log").write_text(
        "meas t63 failed!: out of interval\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(EXAMPLE_DIR / "verify_ngspice.py"),
            "--build-dir",
            str(build_dir),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "ngspice_verification=FAIL" in completed.stdout


def test_ngspice_output_verifier_rejects_an_empty_log(tmp_path: Path) -> None:
    build_dir = tmp_path / "ngspice-empty-log"
    build_dir.mkdir()
    (build_dir / "ngspice.log").write_text("", encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(EXAMPLE_DIR / "verify_ngspice.py"),
            "--build-dir",
            str(build_dir),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "ngspice log is empty" in completed.stdout


def test_ngspice_output_verifier_rejects_wrong_vector_names(
    tmp_path: Path,
) -> None:
    build_dir = tmp_path / "ngspice-wrong-header"
    build_dir.mkdir()
    (build_dir / "ngspice.log").write_text(
        "solver completed: t0 t63 tau63 f3db\n",
        encoding="utf-8",
    )
    (build_dir / "ngspice_step.dat").write_text(
        "\n".join(
            (
                "seconds input output",
                "0 0 0",
                "0.002 0 0",
                "0.003 1 0.6321205588",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(EXAMPLE_DIR / "verify_ngspice.py"),
            "--build-dir",
            str(build_dir),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "header must be time v(in) v(out)" in completed.stdout


def test_ngspice_output_verifier_rejects_one_percent_model_drift(
    tmp_path: Path,
) -> None:
    build_dir = tmp_path / "ngspice-model-drift"
    build_dir.mkdir()
    (build_dir / "ngspice.log").write_text(
        "solver completed: t0 t63 tau63 f3db\n",
        encoding="utf-8",
    )
    (build_dir / "ngspice_step.dat").write_text(
        "\n".join(
            (
                "time v(in) v(out)",
                "0 0 0",
                "0.002 0 0",
                "0.0020001 1 0",
                "0.002990099 1 0.6321205588",
                "0.014 1 0.999999",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    (build_dir / "ngspice_ac.dat").write_text(
        "\n".join(
            (
                "frequency real(h) imag(h)",
                "1 0.9999605231 -0.0062829373",
                "100 0.7169568003 -0.4504772434",
                "159.1549431 0.5 -0.5",
                "1000 0.024704523 -0.1552230961",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(EXAMPLE_DIR / "verify_ngspice.py"),
            "--build-dir",
            str(build_dir),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "tau mismatch" in completed.stdout


def test_ngspice_output_verifier_rejects_a_shifted_trigger(
    tmp_path: Path,
) -> None:
    build_dir = tmp_path / "ngspice-shifted-trigger"
    build_dir.mkdir()
    (build_dir / "ngspice.log").write_text(
        "solver completed: t0 t63 tau63 f3db\n",
        encoding="utf-8",
    )
    (build_dir / "ngspice_step.dat").write_text(
        "\n".join(
            (
                "time v(in) v(out)",
                "0 0 0",
                "0.003 0 0",
                "0.0030001 1 0",
                "0.004 1 0.6321205588",
                "0.014 1 0.999999",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(EXAMPLE_DIR / "verify_ngspice.py"),
            "--build-dir",
            str(build_dir),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "trigger mismatch" in completed.stdout


def _active_netlist_lines(netlist: str) -> list[str]:
    lines: list[str] = []
    for raw_line in netlist.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("*"):
            continue
        active = stripped.split(";", 1)[0].strip()
        if active:
            lines.append(active)
    return lines


def _assert_rc_deck_semantics(netlist: str) -> None:
    lines = _active_netlist_lines(netlist)
    folded = [" ".join(line.casefold().split()) for line in lines]
    assert folded.count(".control") == 1
    assert folded.count(".endc") == 1
    assert folded.index(".control") < folded.index(".endc")

    params: dict[str, str] = {}
    for line in lines:
        match = re.fullmatch(
            r"\.param\s+([A-Za-z][A-Za-z0-9_]*)\s*=\s*(\S+)",
            line,
            flags=re.IGNORECASE,
        )
        if match:
            name, value = match.groups()
            assert name.upper() not in params
            params[name.upper()] = value
    assert params == {"RVAL": "1k", "CVAL": "1u", "TDELAY": "2m"}

    assert any(
        re.fullmatch(
            r"VSTEP\s+in\s+0\s+DC\s+0\s+AC\s+1\s+"
            r"PULSE\(0\s+1\s+\{TDELAY\}\s+100n\s+100n\s+20m\s+40m\)",
            line,
            flags=re.IGNORECASE,
        )
        for line in lines
    )
    assert any(
        re.fullmatch(r"R1\s+in\s+out\s+\{RVAL\}", line, flags=re.IGNORECASE)
        for line in lines
    )
    assert any(
        re.fullmatch(r"C1\s+out\s+0\s+\{CVAL\}", line, flags=re.IGNORECASE)
        for line in lines
    )

    control_start = folded.index(".control")
    control_end = folded.index(".endc")
    outside_control = folded[:control_start] + folded[control_end + 1 :]
    assert outside_control == [
        ".param rval=1k",
        ".param cval=1u",
        ".param tdelay=2m",
        "vstep in 0 dc 0 ac 1 pulse(0 1 {tdelay} 100n 100n 20m 40m)",
        "r1 in out {rval}",
        "c1 out 0 {cval}",
        ".end",
    ]

    control = folded[control_start + 1 : control_end]
    expected_control = [
        "set noaskquit",
        "set wr_singlescale",
        "set wr_vecnames",
        "option numdgt=15",
        "op",
        "print v(in) v(out)",
        "tran 2u 14m",
        "meas tran t0 when v(in)=0.5 rise=1",
        "meas tran t63 when v(out)=0.6321205588285577 rise=1",
        "let tau63 = t63 - t0",
        "print t0 t63 tau63",
        "wrdata build/ngspice_step.dat v(in) v(out)",
        "ac dec 40 1 100k",
        "let h = v(out)/v(in)",
        "meas ac f3db when vdb(out)=-3.010299956639812 fall=1",
        "print f3db",
        "wrdata build/ngspice_ac.dat real(h) imag(h)",
        "quit",
    ]
    assert control == expected_control


@pytest.mark.parametrize(
    "mutation",
    [
        lambda text: text.replace("R1 in out {RVAL}", "* R1 in out {RVAL}"),
        lambda text: text.replace("C1 out 0 {CVAL}", "C1 wrong 0 {CVAL}"),
        lambda text: text.replace("tran 2u 14m", "* tran 2u 14m"),
        lambda text: text.replace(".endc", "* .endc"),
        lambda text: text.replace("let tau63 = t63 - t0", "let tau63 = t63"),
        lambda text: text.replace(
            "set wr_singlescale",
            "* set wr_singlescale",
        ),
        lambda text: text.replace(
            "C1 out 0 {CVAL}",
            "C1 out 0 {CVAL}\nRLOAD out 0 100k",
        ),
        lambda text: text.replace(
            "op\n",
            "op\nalter R1 1.01k\n",
        ),
    ],
)
def test_ngspice_deck_semantic_check_rejects_mutations(mutation) -> None:
    netlist = (EXAMPLE_DIR / "rc_lowpass.cir").read_text(encoding="utf-8")
    with pytest.raises(AssertionError):
        _assert_rc_deck_semantics(mutation(netlist))


def test_ngspice_deck_and_guides_keep_the_example_connected() -> None:
    netlist = (EXAMPLE_DIR / "rc_lowpass.cir").read_text(encoding="utf-8")
    _assert_rc_deck_semantics(netlist)

    guide_paths = (
        "docs/guides/python-jupyter.md",
        "docs/en/guides/python-jupyter.md",
        "docs/guides/data-lab-notebooks.md",
        "docs/en/guides/data-lab-notebooks.md",
        "docs/guides/spice-simulation.md",
        "docs/en/guides/spice-simulation.md",
        "docs/guides/reproducibility.md",
        "docs/en/guides/reproducibility.md",
    )
    for relative_path in guide_paths:
        guide = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        assert "examples/rc-lowpass" in guide
