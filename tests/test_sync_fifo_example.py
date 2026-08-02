from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = REPO_ROOT / "examples" / "sync-fifo"
RUNNER = EXAMPLE_DIR / "run_checks.py"

RUNNER_SPEC = importlib.util.spec_from_file_location(
    "eediy_sync_fifo_run_checks",
    RUNNER,
)
assert RUNNER_SPEC is not None and RUNNER_SPEC.loader is not None
FIFO_RUNNER = importlib.util.module_from_spec(RUNNER_SPEC)
sys.modules[RUNNER_SPEC.name] = FIFO_RUNNER
RUNNER_SPEC.loader.exec_module(FIFO_RUNNER)


def _run_check(name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--only",
            name,
            "--require-tools",
            "all",
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _has_all(*executables: str) -> bool:
    return all(shutil.which(executable) is not None for executable in executables)


def test_sync_fifo_example_has_complete_source_sets() -> None:
    required = (
        "README.md",
        "Makefile",
        "run_checks.py",
        "build-metadata.json",
        "rtl/sync_fifo.sv",
        "tb/fifo_tb.sv",
        "sim/rtl.f",
        "formal/sync_fifo_formal.sv",
        "formal/baseline.sby",
        "formal/fault-read-pointer.sby",
        "synth/synth.ys",
        "constraints/sync_fifo.sdc",
    )
    for relative in required:
        path = EXAMPLE_DIR / relative
        assert path.is_file(), relative
        assert path.stat().st_size > 0, relative

    source_list = (EXAMPLE_DIR / "sim" / "rtl.f").read_text(encoding="utf-8")
    assert source_list.splitlines() == [
        "rtl/sync_fifo.sv",
        "tb/fifo_tb.sv",
    ]


def test_rtl_contract_and_fault_injection_are_explicit() -> None:
    rtl = (EXAMPLE_DIR / "rtl" / "sync_fifo.sv").read_text(encoding="utf-8")
    assert re.search(r"module\s+sync_fifo\b", rtl)
    assert "parameter bit FAULT_READ_POINTER = 1'b0" in rtl
    assert "assign out_valid = (count != 0);" in rtl
    assert "assign out_data = memory[read_pointer];" in rtl
    assert "assign occupancy = count;" in rtl
    assert re.search(
        r"assign\s+in_ready\s*=\s*"
        r"\(count\s*<\s*COUNT_WIDTH'\(DEPTH\)\)\s*\|\|\s*"
        r"\(out_valid\s*&&\s*out_ready\);",
        rtl,
    )
    assert "assign push = in_valid && in_ready;" in rtl
    assert "assign pop = out_valid && out_ready;" in rtl
    assert "if ((DEPTH < 2) || ((DEPTH & (DEPTH - 1)) != 0))" in rtl

    fault_branch = re.search(
        r"if \(FAULT_READ_POINTER\) begin(?P<fault>.*?)"
        r"end else begin(?P<baseline>.*?)end",
        rtl,
        flags=re.DOTALL,
    )
    assert fault_branch is not None
    assert "read_pointer <= read_pointer;" in fault_branch.group("fault")
    assert "read_pointer <= read_pointer + 1'b1;" in fault_branch.group(
        "baseline"
    )
    assert "FAULT_READ_POINTER" not in rtl.split("module sync_fifo", 1)[0]


def test_testbench_is_self_checking_and_exercises_boundaries() -> None:
    testbench = (EXAMPLE_DIR / "tb" / "fifo_tb.sv").read_text(encoding="utf-8")
    for required in (
        "reference_queue",
        "check_visible_state",
        "SYNC_FIFO_SIM_PASS revision=baseline",
        "SYNC_FIFO_MISMATCH",
        "FAULT_READ_POINTER",
        "apply_reset();",
        "step(1'b1, 8'hee, 1'b0);",
        "step(1'b1, 8'h31, 1'b1);",
        "reference_head = (reference_head + 1) % DEPTH;",
        "reference_tail = (reference_tail + 1) % DEPTH;",
    ):
        assert required in testbench

    assert testbench.count("sync_fifo #(") == 1
    assert ".FAULT_READ_POINTER(INJECT_READ_POINTER_FAULT)" in testbench
    assert "$fatal" in testbench
    assert "SYNC_FIFO_NEGATIVE_CONTROL_UNEXPECTED_PASS" in testbench


def test_formal_configs_record_bounded_scope_and_real_negative_control() -> None:
    baseline = (EXAMPLE_DIR / "formal" / "baseline.sby").read_text(
        encoding="utf-8"
    )
    fault = (EXAMPLE_DIR / "formal" / "fault-read-pointer.sby").read_text(
        encoding="utf-8"
    )
    harness = (EXAMPLE_DIR / "formal" / "sync_fifo_formal.sv").read_text(
        encoding="utf-8"
    )

    assert "[tasks]\nbmc\ncover" in baseline
    assert "bmc: mode bmc" in baseline
    assert "bmc: depth 12" in baseline
    assert "cover: mode cover" in baseline
    assert "cover: depth 8" in baseline
    assert "smtbmc z3" in baseline
    assert "multiclock on" not in baseline
    assert "sync_fifo.sv rtl/sync_fifo.sv" in baseline
    assert "sync_fifo_formal.sv formal/sync_fifo_formal.sv" in baseline

    assert "mode bmc" in fault
    assert "depth 8" in fault
    assert "expect pass" in fault
    assert "-D FAULT_READ_POINTER" in fault
    assert "smtbmc z3" in fault
    assert "sync_fifo.sv rtl/sync_fifo.sv" in fault
    assert "sync_fifo_formal.sv formal/sync_fifo_formal.sv" in fault

    for property_text in (
        "assert (occupancy == reference_count);",
        "assert (occupancy <= COUNT_WIDTH'(DEPTH));",
        "assert (out_data == reference_head_data);",
        "cover (occupancy == COUNT_WIDTH'(DEPTH));",
        "cover (out_valid && out_ready && in_valid && in_ready);",
        "cover (!out_valid && out_ready);",
    ):
        assert property_text in harness
    assert "localparam int unsigned DATA_WIDTH = 2;" in harness
    assert "localparam int unsigned DEPTH = 2;" in harness


def test_formal_negative_control_requires_assertion_failure_and_trace(
    tmp_path: Path,
) -> None:
    workdir = tmp_path / "formal-fault"
    engine = workdir / "engine_0"
    engine.mkdir(parents=True)
    (workdir / "status").write_text("FAIL 2 0\n", encoding="utf-8")
    (workdir / "FAIL").write_text(
        "engine_0 returned FAIL\n"
        "counterexample trace: engine_0/trace.vcd\n"
        "failed assertion sync_fifo_formal.$assert$example\n",
        encoding="utf-8",
    )
    trace = engine / "trace.vcd"
    trace.write_text("$date\n$end\n", encoding="utf-8")

    assert FIFO_RUNNER._assert_sby_expected_assertion_failure(workdir) == trace


@pytest.mark.parametrize(
    ("status", "summary", "trace"),
    [
        ("ERROR 1 0\n", "failed assertion\ncounterexample trace: x\n", "$end\n"),
        ("FAIL 2 0\n", "engine crashed\n", "$end\n"),
        ("FAIL 2 0\n", "failed assertion\ncounterexample trace: x\n", ""),
    ],
)
def test_formal_negative_control_rejects_tool_errors_or_empty_witnesses(
    tmp_path: Path,
    status: str,
    summary: str,
    trace: str,
) -> None:
    workdir = tmp_path / "formal-fault"
    engine = workdir / "engine_0"
    engine.mkdir(parents=True)
    (workdir / "status").write_text(status, encoding="utf-8")
    (workdir / "FAIL").write_text(summary, encoding="utf-8")
    (engine / "trace.vcd").write_text(trace, encoding="utf-8")

    with pytest.raises(FIFO_RUNNER.CheckFailure):
        FIFO_RUNNER._assert_sby_expected_assertion_failure(workdir)


def test_metadata_and_constraints_do_not_claim_implementation_evidence() -> None:
    metadata = json.loads(
        (EXAMPLE_DIR / "build-metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["parameters"] == {"DATA_WIDTH": 8, "DEPTH": 4}
    assert metadata["formal_scope"]["baseline"]["mode"] == "bmc"
    assert metadata["formal_scope"]["baseline"]["depth"] == 12
    assert metadata["formal_scope"]["baseline"]["parameters"] == {
        "DATA_WIDTH": 2,
        "DEPTH": 2,
    }
    assert "not an unbounded proof" in metadata["formal_scope"]["baseline"][
        "claim_limit"
    ]
    assert metadata["formal_scope"]["fault_read_pointer"][
        "expected_result"
    ].startswith("FAIL")
    assert metadata["constraints"]["target_device"] is None
    assert metadata["constraints"]["board_pinout"] is None

    constraints = (EXAMPLE_DIR / "constraints" / "sync_fifo.sdc").read_text(
        encoding="utf-8"
    )
    assert "create_clock -name clk -period 10.000" in constraints
    assert "set_clock_uncertainty 0.200" in constraints
    assert "set_input_delay" in constraints
    assert "set_output_delay" in constraints
    assert "set_false_path" not in constraints

    synthesis = (EXAMPLE_DIR / "synth" / "synth.ys").read_text(
        encoding="utf-8"
    )
    for command in (
        "read_verilog -sv -D SYNTHESIS",
        "hierarchy -check -top sync_fifo",
        "synth -top sync_fifo",
        "check -assert",
        "write_json build/synth/sync_fifo.json",
    ):
        assert command in synthesis


def test_runner_reports_missing_tools_as_skips(tmp_path: Path) -> None:
    environment = os.environ.copy()
    environment["PATH"] = str(tmp_path)
    completed = subprocess.run(
        [sys.executable, str(RUNNER)],
        cwd=REPO_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    for check_name in ("icarus", "verilator", "formal", "synthesis"):
        assert f"CHECK_SKIP name={check_name}" in completed.stdout
    assert "CHECK_SUMMARY passed=0 skipped=4 failed=0" in completed.stdout


def test_guides_link_the_executable_fifo_starter() -> None:
    starter_url = (
        "https://github.com/appleweiping/eediy/tree/main/examples/sync-fifo"
    )
    command = "python examples/sync-fifo/run_checks.py"
    for relative in (
        "docs/guides/hdl-fpga.md",
        "docs/en/guides/hdl-fpga.md",
    ):
        guide = (REPO_ROOT / relative).read_text(encoding="utf-8")
        assert starter_url in guide
        assert command in guide


@pytest.mark.skipif(
    not _has_all("iverilog", "vvp"),
    reason="Icarus and vvp are not installed; source checks still run",
)
def test_installed_icarus_runs_baseline_and_rejects_fault() -> None:
    completed = _run_check("icarus")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "SYNC_FIFO_SIM_PASS revision=baseline" in completed.stdout
    assert "SYNC_FIFO_MISMATCH" in completed.stdout
    assert "CHECK_PASS name=icarus" in completed.stdout


@pytest.mark.skipif(
    not _has_all("verilator"),
    reason="Verilator is not installed; source checks still run",
)
def test_installed_verilator_runs_baseline_and_rejects_fault() -> None:
    completed = _run_check("verilator")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "SYNC_FIFO_SIM_PASS revision=baseline" in completed.stdout
    assert "SYNC_FIFO_MISMATCH" in completed.stdout
    assert "CHECK_PASS name=verilator" in completed.stdout


@pytest.mark.skipif(
    not _has_all("sby", "yosys", "yosys-smtbmc", "z3"),
    reason="SymbiYosys toolchain is not installed; source checks still run",
)
def test_installed_formal_tools_pass_baseline_and_find_counterexample() -> None:
    completed = _run_check("formal")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "COUNTEREXAMPLE" in completed.stdout
    assert "CHECK_PASS name=formal" in completed.stdout


@pytest.mark.skipif(
    not _has_all("yosys"),
    reason="Yosys is not installed; source checks still run",
)
def test_installed_yosys_synthesizes_the_fifo() -> None:
    completed = _run_check("synthesis")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "CHECK_PASS name=synthesis" in completed.stdout
