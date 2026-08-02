from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "tmp117-kicad"


def load_exporter():
    spec = importlib.util.spec_from_file_location("tmp117_export", EXAMPLE / "export.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_source_and_pin_net_audit_is_exact():
    exporter = load_exporter()
    result = exporter.source_audit()
    assert result == {
        "components": 7,
        "nets": ["3V3", "ADD0", "ALERT", "GND", "SCL", "SDA"],
        "pin_assignments": 24,
        "status": "pass",
    }
    assert exporter.EXPECTED["U1"][2] == {
        "1": "SCL",
        "2": "GND",
        "3": "ALERT",
        "4": "ADD0",
        "5": "3V3",
        "6": "SDA",
        "7": "GND",
    }


def test_authoritative_sha256_provenance_covers_every_kicad_input():
    exporter = load_exporter()
    relative_paths = {
        path.relative_to(EXAMPLE).as_posix()
        for path in exporter.authoritative_input_paths()
    }
    assert relative_paths == {
        "fp-lib-table",
        "library/EEDIY.kicad_sym",
        "library/EEDIY.pretty/C_0603_1608Metric.kicad_mod",
        "library/EEDIY.pretty/PinHeader_1x06_P2.54mm.kicad_mod",
        "library/EEDIY.pretty/R_0603_1608Metric.kicad_mod",
        "library/EEDIY.pretty/SolderJumper_3_Open.kicad_mod",
        "library/EEDIY.pretty/TMP117_WSON6_DRV0006B.kicad_mod",
        "sym-lib-table",
        "tmp117.kicad_pcb",
        "tmp117.kicad_pro",
        "tmp117.kicad_sch",
    }
    hashes = exporter.hash_authoritative_inputs()
    assert set(hashes) == relative_paths
    assert all(len(digest) == 64 for digest in hashes.values())
    assert all(set(digest) <= set("0123456789abcdef") for digest in hashes.values())


def test_authoritative_input_mutation_is_release_blocking(monkeypatch):
    exporter = load_exporter()
    before = {"tmp117.kicad_pcb": "0" * 64}
    monkeypatch.setattr(
        exporter,
        "hash_authoritative_inputs",
        lambda: {"tmp117.kicad_pcb": "1" * 64},
    )
    with pytest.raises(exporter.AuditError, match="input mutation.*tmp117.kicad_pcb"):
        exporter.verify_authoritative_inputs_unchanged(before)


def test_project_is_modern_and_self_contained():
    assert not list(EXAMPLE.glob("*.sch"))
    assert not list(EXAMPLE.glob("*.lib"))
    assert not list(EXAMPLE.glob("~*.lck"))
    assert not list(EXAMPLE.glob("*.kicad_prl"))
    assert not (EXAMPLE / "rescue-backup").exists()
    assert "${KIPRJMOD}/library/EEDIY.kicad_sym" in (EXAMPLE / "sym-lib-table").read_text(encoding="utf-8")
    assert "${KIPRJMOD}/library/EEDIY.pretty" in (EXAMPLE / "fp-lib-table").read_text(encoding="utf-8")
    json.loads((EXAMPLE / "tmp117.kicad_pro").read_text(encoding="utf-8"))


def test_wson_source_records_reviewed_dimensions_and_boundary():
    footprint = (
        EXAMPLE / "library" / "EEDIY.pretty" / "TMP117_WSON6_DRV0006B.kicad_mod"
    ).read_text(encoding="utf-8")
    for marker in (
        "TI TMP117 DRV0006B WSON-6",
        '(pad "1" smd rect (at -0.975 -0.65) (size 0.45 0.3)',
        '(pad "6" smd roundrect (at 0.975 -0.65) (size 0.45 0.3)',
        '(pad "7" smd roundrect (at 0 0) (size 1 1.6)',
        "requires independent",
    ):
        assert marker in footprint

    readme = (EXAMPLE / "README.md").read_text(encoding="utf-8")
    for boundary in (
        "not a released reference design",
        "unsoldered thermal pad condition",
        "thermal accuracy",
        "no network upload",
    ):
        assert boundary in readme


def test_runner_is_local_only_and_strict_when_requested(tmp_path):
    exporter = load_exporter()
    first = tmp_path / "bom-a.csv"
    second = tmp_path / "bom-b.csv"
    exporter.write_bom(first)
    exporter.write_bom(second)
    assert first.read_bytes() == second.read_bytes()
    text = (EXAMPLE / "export.py").read_text(encoding="utf-8")
    assert "--require-kicad" in text
    assert "--exit-code-violations" in text
    assert "--schematic-parity" in text
    assert "F.Cu,B.Cu,F.Paste,B.Paste" in text
    assert text.index("validate_generated_outputs(expected") < text.index(
        "write_checksums(expected)"
    )
    assert "HOLD: outputs were not uploaded, ordered, or released" in text


def test_subprocesses_have_bounded_timeouts(monkeypatch):
    exporter = load_exporter()
    calls = []

    def complete(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, stdout="8.0.9\n", stderr="")

    monkeypatch.setattr(exporter.subprocess, "run", complete)
    exporter.run(["kicad-cli", "pcb", "drc"])
    assert calls[-1][1]["timeout"] == exporter.COMMAND_TIMEOUT_SECONDS
    assert calls[-1][1]["cwd"] == exporter.ROOT

    assert exporter.kicad_version("kicad-cli") == ("8.0.9", 8)
    assert calls[-1][1]["timeout"] == exporter.VERSION_TIMEOUT_SECONDS

    def time_out(command, **kwargs):
        raise subprocess.TimeoutExpired(command, kwargs["timeout"])

    monkeypatch.setattr(exporter.subprocess, "run", time_out)
    with pytest.raises(exporter.AuditError, match="exceeded 120s timeout"):
        exporter.run(["kicad-cli", "pcb", "drc"])


def test_output_contract_rejects_missing_empty_and_unexpected_files(tmp_path, monkeypatch):
    exporter = load_exporter()
    monkeypatch.setattr(exporter, "BUILD", tmp_path)
    expected = {"one.txt", "nested/two.txt"}

    (tmp_path / "one.txt").write_text("one", encoding="utf-8")
    with pytest.raises(exporter.AuditError, match="missing=nested/two.txt"):
        exporter.validate_output_allowlist(expected)

    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "two.txt").write_bytes(b"")
    with pytest.raises(exporter.AuditError, match="output is empty"):
        exporter.validate_output_allowlist(expected)

    (tmp_path / "nested" / "two.txt").write_text("two", encoding="utf-8")
    (tmp_path / "extra.txt").write_text("extra", encoding="utf-8")
    with pytest.raises(exporter.AuditError, match="unexpected=extra.txt"):
        exporter.validate_output_allowlist(expected)


def test_bom_and_placement_csvs_are_structurally_validated(tmp_path):
    exporter = load_exporter()
    bom = tmp_path / "bom.csv"
    exporter.write_bom(bom)
    exporter.validate_bom(bom)

    positions = tmp_path / "positions.csv"
    with positions.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["Ref", "Val", "Package", "PosX", "PosY", "Rot", "Side"])
        for reference, (value, footprint, _) in exporter.EXPECTED.items():
            writer.writerow([reference, value, footprint.split(":", 1)[1], 1.0, 2.0, 0.0, "top"])
    exporter.validate_positions(positions)

    text = positions.read_text(encoding="utf-8").replace(",top\n", ",sideways\n", 1)
    positions.write_text(text, encoding="utf-8")
    with pytest.raises(exporter.AuditError, match="invalid side"):
        exporter.validate_positions(positions)


def test_release_output_allowlist_includes_paste_and_auditable_reports():
    exporter = load_exporter()
    expected = exporter.expected_output_files(8)
    assert {
        "manufacturing/gerbers/tmp117-F_Paste.gtp",
        "manufacturing/gerbers/tmp117-B_Paste.gbp",
        "manufacturing/gerbers/tmp117-job.gbrjob",
        "manufacturing/gerbers/tmp117.drl",
        "manufacturing/positions.csv",
        "manufacturing/bom.csv",
        "reports/netlist.xml",
        "reports/erc.rpt",
        "reports/drc.rpt",
        "reports/source-inputs.json",
        "reports/schematic.pdf",
        "reports/assembly.pdf",
        "status.json",
    } <= expected
    assert "SHA256SUMS" not in expected

    readme = (EXAMPLE / "README.md").read_text(encoding="utf-8")
    assert "top/bottom paste Gerbers" in readme
    assert "assembly-review output set" in readme
    assert "`assembly_release: hold`" in readme


def test_checksum_manifest_is_exact_and_detects_tampering(tmp_path, monkeypatch):
    exporter = load_exporter()
    monkeypatch.setattr(exporter, "BUILD", tmp_path)
    expected = {"a.txt", "nested/b.txt"}
    (tmp_path / "a.txt").write_text("alpha", encoding="utf-8")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "b.txt").write_text("beta", encoding="utf-8")

    exporter.write_checksums(expected)
    exporter.validate_checksums(expected)
    lines = (tmp_path / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    assert [line.split("  ", 1)[1] for line in lines] == sorted(expected)

    (tmp_path / "a.txt").write_text("tampered", encoding="utf-8")
    with pytest.raises(exporter.AuditError, match="digest mismatch: a.txt"):
        exporter.validate_checksums(expected)


def test_bilingual_guides_link_the_executable_starter():
    starter = "https://github.com/appleweiping/eediy/tree/main/examples/tmp117-kicad"
    command = "python examples/tmp117-kicad/export.py --require-kicad"
    for guide in (
        ROOT / "docs" / "guides" / "pcb-kicad.md",
        ROOT / "docs" / "en" / "guides" / "pcb-kicad.md",
    ):
        text = guide.read_text(encoding="utf-8")
        assert starter in text
        assert command in text
