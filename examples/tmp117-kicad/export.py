#!/usr/bin/env python3
"""Audit and export the TMP117 KiCad teaching project.

The runner is intentionally local-only: it writes ``build/`` and never
uploads, orders, or contacts a manufacturer.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
SCHEMATIC = ROOT / "tmp117.kicad_sch"
BOARD = ROOT / "tmp117.kicad_pcb"
COMMAND_TIMEOUT_SECONDS = 120
VERSION_TIMEOUT_SECONDS = 15

GERBER_JOB_FILE_FUNCTIONS = {
    "tmp117-F_Cu.gtl": "Copper,L1,Top",
    "tmp117-B_Cu.gbl": "Copper,L2,Bot",
    "tmp117-F_Paste.gtp": "SolderPaste,Top",
    "tmp117-B_Paste.gbp": "SolderPaste,Bot",
    "tmp117-F_Silkscreen.gto": "Legend,Top",
    "tmp117-B_Silkscreen.gbo": "Legend,Bot",
    "tmp117-F_Mask.gts": "SolderMask,Top",
    "tmp117-B_Mask.gbs": "SolderMask,Bot",
    "tmp117-Edge_Cuts.gm1": "Profile",
}
GERBER_X2_FILE_FUNCTIONS = {
    **GERBER_JOB_FILE_FUNCTIONS,
    "tmp117-F_Paste.gtp": "Paste,Top",
    "tmp117-B_Paste.gbp": "Paste,Bot",
    "tmp117-F_Mask.gts": "Soldermask,Top",
    "tmp117-B_Mask.gbs": "Soldermask,Bot",
    "tmp117-Edge_Cuts.gm1": "Profile,NP",
}

SOURCE_ONLY_OUTPUTS = {
    "manufacturing/bom.csv",
    "reports/pin-net-audit.json",
    "reports/source-inputs.json",
    "status.json",
}
KICAD_EXPORT_OUTPUTS = {
    *(f"manufacturing/gerbers/{name}" for name in GERBER_JOB_FILE_FUNCTIONS),
    "manufacturing/gerbers/tmp117-job.gbrjob",
    "manufacturing/gerbers/tmp117.drl",
    "manufacturing/gerbers/tmp117-drl_map.pdf",
    "manufacturing/positions.csv",
    "reports/assembly.pdf",
    "reports/netlist.xml",
    "reports/schematic.pdf",
}
KICAD_8_AUDIT_OUTPUTS = {
    "reports/erc.rpt",
    "reports/drc.rpt",
}

EXPECTED = {
    "C1": ("100nF", "EEDIY:C_0603_1608Metric", {"1": "3V3", "2": "GND"}),
    "J1": (
        "HOST_I2C",
        "EEDIY:PinHeader_1x06_P2.54mm",
        {"1": "3V3", "2": "GND", "3": "SDA", "4": "SCL", "5": "ALERT", "6": "ADD0"},
    ),
    "JP1": (
        "ADD0_SELECT",
        "EEDIY:SolderJumper_3_Open",
        {"1": "3V3", "2": "ADD0", "3": "GND"},
    ),
    "R1": ("4.7k SDA", "EEDIY:R_0603_1608Metric", {"1": "3V3", "2": "SDA"}),
    "R2": ("4.7k SCL", "EEDIY:R_0603_1608Metric", {"1": "3V3", "2": "SCL"}),
    "R3": ("4.7k ALERT", "EEDIY:R_0603_1608Metric", {"1": "3V3", "2": "ALERT"}),
    "U1": (
        "TMP117AIDRVR",
        "EEDIY:TMP117_WSON6_DRV0006B",
        {"1": "SCL", "2": "GND", "3": "ALERT", "4": "ADD0", "5": "3V3", "6": "SDA", "7": "GND"},
    ),
}

BOM_METADATA = {
    "C1": ("", "", "Select voltage rating, dielectric, and tolerance before assembly."),
    "J1": ("", "", "Connector family and mating-side geometry are intentionally unspecified."),
    "JP1": ("", "", "Copper solder selector; fit no purchased component."),
    "R1": ("", "", "Select resistance tolerance and voltage rating before assembly."),
    "R2": ("", "", "Select resistance tolerance and voltage rating before assembly."),
    "R3": ("", "", "Select resistance tolerance and voltage rating before assembly."),
    "U1": ("Texas Instruments", "TMP117AIDRVR", "DRV0006B WSON-6; independently verify package revision."),
}


class AuditError(RuntimeError):
    pass


def authoritative_input_paths() -> tuple[Path, ...]:
    """Return every file that can affect the reviewed KiCad design."""

    fixed = (
        ROOT / "tmp117.kicad_pro",
        SCHEMATIC,
        BOARD,
        ROOT / "sym-lib-table",
        ROOT / "fp-lib-table",
        ROOT / "library" / "EEDIY.kicad_sym",
    )
    footprint_dir = ROOT / "library" / "EEDIY.pretty"
    expected_footprints = {
        footprint_dir / f"{library_id.split(':', 1)[1]}.kicad_mod"
        for _, library_id, _ in EXPECTED.values()
    }
    footprints = tuple(sorted(expected_footprints | set(footprint_dir.glob("*.kicad_mod"))))
    return fixed + footprints


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_authoritative_inputs() -> dict[str, str]:
    paths = authoritative_input_paths()
    missing = [path.relative_to(ROOT).as_posix() for path in paths if not path.is_file()]
    if missing:
        raise AuditError("missing authoritative project source: " + ", ".join(missing))
    return {
        path.relative_to(ROOT).as_posix(): sha256_file(path)
        for path in paths
    }


def verify_authoritative_inputs_unchanged(before: dict[str, str]) -> None:
    after = hash_authoritative_inputs()
    if before == after:
        return

    changed = sorted(
        path
        for path in before.keys() | after.keys()
        if before.get(path) != after.get(path)
    )
    raise AuditError(
        "authoritative input mutation detected during export: " + ", ".join(changed)
    )


def balanced_blocks(text: str, prefix: str) -> list[str]:
    blocks: list[str] = []
    cursor = 0
    while True:
        start = text.find(prefix, cursor)
        if start < 0:
            return blocks
        depth = 0
        quoted = False
        escaped = False
        for index in range(start, len(text)):
            char = text[index]
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
                continue
            if char == '"':
                quoted = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    blocks.append(text[start : index + 1])
                    cursor = index + 1
                    break
        else:
            raise AuditError(f"unterminated S-expression starting with {prefix!r}")


def parse_board() -> dict[str, tuple[str, str, dict[str, str]]]:
    text = BOARD.read_text(encoding="utf-8")
    found: dict[str, tuple[str, str, dict[str, str]]] = {}
    for block in balanced_blocks(text, "(footprint "):
        footprint = re.match(r'\(footprint "([^"]+)"', block)
        reference = re.search(r'\(fp_text reference "([^"]+)"', block)
        value = re.search(r'\(fp_text value "([^"]*)"', block)
        if not (footprint and reference and value):
            raise AuditError("board footprint is missing reference, value, or library id")
        pads: dict[str, str] = {}
        for pad_block in balanced_blocks(block, "(pad "):
            number = re.match(r'\(pad "([^"]+)"', pad_block)
            net = re.search(r'\(net \d+ "([^"]+)"\)', pad_block)
            if not (number and net):
                raise AuditError(f"{reference.group(1)} has a pad without a numbered net")
            pads[number.group(1)] = net.group(1).lstrip("/")
        found[reference.group(1)] = (value.group(1), footprint.group(1), pads)
    return found


def source_audit() -> dict[str, object]:
    forbidden = list(ROOT.glob("*.sch")) + list(ROOT.glob("*.lib"))
    forbidden += list(ROOT.glob("~*.lck")) + list(ROOT.glob("*.kicad_prl"))
    if (ROOT / "rescue-backup").exists():
        forbidden.append(ROOT / "rescue-backup")
    if forbidden:
        raise AuditError("legacy or GUI-temporary files remain: " + ", ".join(p.name for p in forbidden))

    required = authoritative_input_paths()
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise AuditError("missing authoritative project source: " + ", ".join(missing))

    board_model = parse_board()
    if board_model != EXPECTED:
        raise AuditError(
            "board pin/net audit differs from the reviewed model:\n"
            + json.dumps({"expected": EXPECTED, "actual": board_model}, indent=2, sort_keys=True)
        )

    schematic_text = SCHEMATIC.read_text(encoding="utf-8")
    for reference, (value, footprint, _) in EXPECTED.items():
        for marker in (
            f'(property "Reference" "{reference}"',
            f'(property "Value" "{value}"',
            f'(property "Footprint" "{footprint}"',
        ):
            if marker not in schematic_text:
                raise AuditError(f"schematic is missing {marker}")

    wson = (ROOT / "library" / "EEDIY.pretty" / "TMP117_WSON6_DRV0006B.kicad_mod").read_text(encoding="utf-8")
    mechanical_markers = [
        'TI TMP117 DRV0006B WSON-6',
        '(pad "1" smd rect (at -0.975 -0.65) (size 0.45 0.3)',
        '(pad "6" smd roundrect (at 0.975 -0.65) (size 0.45 0.3)',
        '(pad "7" smd roundrect (at 0 0) (size 1 1.6)',
    ]
    if any(marker not in wson for marker in mechanical_markers):
        raise AuditError("WSON footprint no longer matches the reviewed DRV0006B land-pattern anchors")

    return {
        "components": len(EXPECTED),
        "nets": sorted({net for _, _, pads in EXPECTED.values() for net in pads.values()}),
        "pin_assignments": sum(len(pads) for _, _, pads in EXPECTED.values()),
        "status": "pass",
    }


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise AuditError(
            f"command exceeded {COMMAND_TIMEOUT_SECONDS}s timeout: {' '.join(command)}"
        ) from error
    if completed.returncode:
        raise AuditError(f"command failed with exit code {completed.returncode}: {' '.join(command)}")


def kicad_version(executable: str) -> tuple[str, int]:
    try:
        completed = subprocess.run(
            [executable, "--version"],
            capture_output=True,
            text=True,
            timeout=VERSION_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise AuditError(
            f"kicad-cli version probe exceeded {VERSION_TIMEOUT_SECONDS}s timeout"
        ) from error
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise AuditError(
            f"kicad-cli version probe failed with exit code {completed.returncode}: {detail}"
        )
    version = (completed.stdout or completed.stderr).strip()
    match = re.search(r"(\d+)\.", version)
    if not match:
        raise AuditError(f"could not parse kicad-cli version: {version!r}")
    return version, int(match.group(1))


def audit_xml_netlist(path: Path) -> None:
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as error:
        raise AuditError(f"KiCad schematic netlist is not valid XML: {error}") from error
    if root.tag != "export":
        raise AuditError(f"KiCad schematic netlist has unexpected root element: {root.tag!r}")
    component_elements = root.findall("./components/comp")
    components: dict[str, tuple[str, str]] = {}
    for component in component_elements:
        reference = component.attrib.get("ref", "")
        if not reference or reference in components:
            raise AuditError(
                f"KiCad schematic netlist contains a missing or duplicate component ref: {reference!r}"
            )
        components[reference] = (
            component.findtext("value", ""),
            component.findtext("footprint", ""),
        )
    expected_components = {ref: values[:2] for ref, values in EXPECTED.items()}
    if components != expected_components:
        raise AuditError("KiCad schematic netlist component audit failed")

    nodes: dict[str, dict[str, str]] = {ref: {} for ref in EXPECTED}
    seen_nodes: set[tuple[str, str]] = set()
    for net in root.findall("./nets/net"):
        if "name" not in net.attrib:
            raise AuditError("KiCad schematic netlist contains a net without a name")
        name = net.attrib["name"].lstrip("/")
        for node in net.findall("node"):
            reference = node.attrib.get("ref", "")
            pin = node.attrib.get("pin", "")
            if reference not in nodes or not pin:
                raise AuditError(
                    f"KiCad schematic netlist contains an unexpected node: {node.attrib!r}"
                )
            node_key = (reference, pin)
            if node_key in seen_nodes:
                raise AuditError(
                    f"KiCad schematic netlist repeats node {reference}.{pin}"
                )
            seen_nodes.add(node_key)
            nodes[reference][pin] = name
    expected_nodes = {ref: pads for ref, (_, _, pads) in EXPECTED.items()}
    if nodes != expected_nodes:
        raise AuditError("KiCad schematic pin/net audit failed")


def write_bom(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            ["reference", "quantity", "value", "footprint", "manufacturer", "manufacturer_part_number", "assembly_note"]
        )
        for reference in sorted(EXPECTED):
            value, footprint, _ = EXPECTED[reference]
            manufacturer, mpn, note = BOM_METADATA[reference]
            writer.writerow([reference, 1, value, footprint, manufacturer, mpn, note])


def expected_output_files(kicad_major: int | None) -> set[str]:
    expected = set(SOURCE_ONLY_OUTPUTS)
    if kicad_major is not None:
        expected.update(KICAD_EXPORT_OUTPUTS)
    if kicad_major is not None and kicad_major >= 8:
        expected.update(KICAD_8_AUDIT_OUTPUTS)
    return expected


def build_file_inventory() -> set[str]:
    return {
        path.relative_to(BUILD).as_posix()
        for path in BUILD.rglob("*")
        if path.is_file()
    }


def validate_output_allowlist(expected: set[str]) -> None:
    actual = build_file_inventory()
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing or unexpected:
        details = []
        if missing:
            details.append("missing=" + ", ".join(missing))
        if unexpected:
            details.append("unexpected=" + ", ".join(unexpected))
        raise AuditError("generated output contract failed: " + "; ".join(details))

    empty = sorted(
        relative
        for relative in expected
        if (BUILD / relative).stat().st_size == 0
    )
    if empty:
        raise AuditError("generated output is empty: " + ", ".join(empty))


def read_csv(path: Path, expected_header: list[str]) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != expected_header:
                raise AuditError(
                    f"{path.name} header differs from the reviewed schema: {reader.fieldnames!r}"
                )
            rows = list(reader)
    except (csv.Error, UnicodeError, OSError) as error:
        raise AuditError(f"{path.name} is not a valid UTF-8 CSV: {error}") from error
    return rows


def validate_bom(path: Path) -> None:
    header = [
        "reference",
        "quantity",
        "value",
        "footprint",
        "manufacturer",
        "manufacturer_part_number",
        "assembly_note",
    ]
    rows = read_csv(path, header)
    actual = {
        row["reference"]: (
            row["quantity"],
            row["value"],
            row["footprint"],
            row["manufacturer"],
            row["manufacturer_part_number"],
            row["assembly_note"],
        )
        for row in rows
    }
    expected = {
        reference: (
            "1",
            value,
            footprint,
            *BOM_METADATA[reference],
        )
        for reference, (value, footprint, _) in EXPECTED.items()
    }
    if len(rows) != len(actual) or actual != expected:
        raise AuditError("BOM rows differ from the reviewed component model")


def validate_positions(path: Path) -> None:
    header = ["Ref", "Val", "Package", "PosX", "PosY", "Rot", "Side"]
    rows = read_csv(path, header)
    actual_references = [row["Ref"] for row in rows]
    if len(actual_references) != len(set(actual_references)):
        raise AuditError("placement CSV contains duplicate component references")
    if set(actual_references) != set(EXPECTED):
        raise AuditError("placement CSV component set differs from the reviewed model")

    for row in rows:
        value, footprint, _ = EXPECTED[row["Ref"]]
        if row["Val"] != value or row["Package"] != footprint.split(":", 1)[1]:
            raise AuditError(f"placement CSV metadata differs for {row['Ref']}")
        if row["Side"] not in {"top", "bottom"}:
            raise AuditError(f"placement CSV has an invalid side for {row['Ref']}")
        try:
            numbers = [float(row[field]) for field in ("PosX", "PosY", "Rot")]
        except ValueError as error:
            raise AuditError(f"placement CSV has a non-numeric coordinate for {row['Ref']}") from error
        if not all(math.isfinite(number) for number in numbers):
            raise AuditError(f"placement CSV has a non-finite coordinate for {row['Ref']}")


def validate_pdf(path: Path) -> None:
    content = path.read_bytes()
    if len(content) < 512 or not content.startswith(b"%PDF-") or b"%%EOF" not in content[-1024:]:
        raise AuditError(f"{path.name} is not a structurally complete PDF")


def validate_gerbers(directory: Path) -> None:
    for name, file_function in GERBER_X2_FILE_FUNCTIONS.items():
        path = directory / name
        text = path.read_text(encoding="utf-8")
        if f"%TF.FileFunction,{file_function}*%" not in text or not text.rstrip().endswith("M02*"):
            raise AuditError(f"{name} is not a complete Gerber X2 {file_function} layer")

    job_path = directory / "tmp117-job.gbrjob"
    try:
        job = json.loads(job_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError, OSError) as error:
        raise AuditError(f"{job_path.name} is not valid JSON: {error}") from error
    attributes = job.get("FilesAttributes")
    if not isinstance(attributes, list):
        raise AuditError("Gerber job is missing FilesAttributes")
    generation_software = job.get("Header", {}).get("GenerationSoftware", {})
    if (
        not isinstance(generation_software, dict)
        or generation_software.get("Vendor") != "KiCad"
        or generation_software.get("Application") != "Pcbnew"
        or not generation_software.get("Version")
    ):
        raise AuditError("Gerber job has invalid generation-software metadata")
    if len(attributes) != len(GERBER_JOB_FILE_FUNCTIONS) or not all(
        isinstance(item, dict) for item in attributes
    ):
        raise AuditError("Gerber job layer entries are missing, duplicated, or malformed")
    actual_functions = {
        item.get("Path"): item.get("FileFunction")
        for item in attributes
    }
    if actual_functions != GERBER_JOB_FILE_FUNCTIONS:
        raise AuditError("Gerber job layer manifest differs from the required layer set")


def validate_drill(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    coordinate_count = len(re.findall(r"^X[-0-9.]+Y[-0-9.]+$", text, flags=re.MULTILINE))
    if (
        not text.startswith("M48")
        or "TF.FileFunction," not in text
        or not re.search(r"^T\d+C[0-9.]+$", text, flags=re.MULTILINE)
        or coordinate_count < 6
        or not text.rstrip().endswith("M30")
    ):
        raise AuditError("Excellon drill file is structurally incomplete")


def validate_zero_reports(reports: Path) -> None:
    erc = (reports / "erc.rpt").read_text(encoding="utf-8")
    if not re.search(r"\*\* ERC messages:\s+0\s+Errors\s+0\s+Warnings\s+0", erc):
        raise AuditError("ERC report does not record exactly zero errors and warnings")

    drc = (reports / "drc.rpt").read_text(encoding="utf-8")
    for marker in (
        "** Found 0 DRC violations **",
        "** Found 0 unconnected pads **",
        "** Found 0 Footprint errors **",
        "** End of Report **",
    ):
        if marker not in drc:
            raise AuditError(f"DRC report is missing the required zero-result marker: {marker}")


def validate_json_outputs(
    source_hashes: dict[str, str],
    status: dict[str, object],
) -> None:
    try:
        pin_audit = json.loads(
            (BUILD / "reports" / "pin-net-audit.json").read_text(encoding="utf-8")
        )
        provenance = json.loads(
            (BUILD / "reports" / "source-inputs.json").read_text(encoding="utf-8")
        )
        recorded_status = json.loads((BUILD / "status.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError, OSError) as error:
        raise AuditError(f"generated JSON report is not parseable: {error}") from error

    expected_pin_audit = {ref: pads for ref, (_, _, pads) in EXPECTED.items()}
    if pin_audit != expected_pin_audit:
        raise AuditError("pin/net JSON report differs from the reviewed model")

    if provenance != {
        "algorithm": "SHA-256",
        "files": source_hashes,
        "verified_unchanged": True,
    }:
        raise AuditError("source-input provenance report is incomplete or inconsistent")

    if recorded_status != status:
        raise AuditError("status JSON differs from the in-memory release status")


def validate_generated_outputs(
    expected: set[str],
    source_hashes: dict[str, str],
    status: dict[str, object],
    kicad_major: int | None,
) -> None:
    validate_output_allowlist(expected)
    validate_bom(BUILD / "manufacturing" / "bom.csv")
    validate_json_outputs(source_hashes, status)

    if kicad_major is None:
        return

    reports = BUILD / "reports"
    manufacturing = BUILD / "manufacturing"
    audit_xml_netlist(reports / "netlist.xml")
    validate_positions(manufacturing / "positions.csv")
    validate_gerbers(manufacturing / "gerbers")
    validate_drill(manufacturing / "gerbers" / "tmp117.drl")
    for path in (
        manufacturing / "gerbers" / "tmp117-drl_map.pdf",
        reports / "assembly.pdf",
        reports / "schematic.pdf",
    ):
        validate_pdf(path)
    if kicad_major >= 8:
        validate_zero_reports(reports)


def write_checksums(expected: set[str]) -> None:
    manifest = BUILD / "SHA256SUMS"
    lines = [
        f"{sha256_file(BUILD / relative)}  {relative}"
        for relative in sorted(expected)
    ]
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_checksums(expected: set[str]) -> None:
    manifest = BUILD / "SHA256SUMS"
    lines = manifest.read_text(encoding="utf-8").splitlines()
    if len(lines) != len(expected):
        raise AuditError("SHA256SUMS entry count differs from the output allowlist")

    parsed: dict[str, str] = {}
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\r\n]+)", line)
        if not match or match.group(2) in parsed:
            raise AuditError(f"SHA256SUMS contains an invalid or duplicate line: {line!r}")
        parsed[match.group(2)] = match.group(1)
    if set(parsed) != expected:
        raise AuditError("SHA256SUMS paths differ from the output allowlist")
    for relative, digest in parsed.items():
        if sha256_file(BUILD / relative) != digest:
            raise AuditError(f"SHA256SUMS digest mismatch: {relative}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-kicad",
        action="store_true",
        help="require KiCad 8+ so headless ERC and DRC are release-blocking",
    )
    args = parser.parse_args()

    audit = source_audit()
    source_hashes = hash_authoritative_inputs()
    resolved_build = BUILD.resolve()
    if resolved_build.parent != ROOT.resolve():
        raise AuditError(f"refusing to clean unexpected build path: {resolved_build}")
    if BUILD.exists():
        shutil.rmtree(BUILD)
    reports = BUILD / "reports"
    manufacturing = BUILD / "manufacturing"
    gerbers = manufacturing / "gerbers"
    gerbers.mkdir(parents=True)
    reports.mkdir(parents=True)

    cli = shutil.which("kicad-cli")
    major: int | None = None
    version: str | None = None
    erc_drc = "not_run"
    try:
        if not cli:
            if args.require_kicad:
                raise AuditError("kicad-cli 8 or newer is required but was not found")
        else:
            version, major = kicad_version(cli)
            if args.require_kicad and major < 8:
                raise AuditError(
                    f"--require-kicad needs KiCad 8+ for CLI ERC/DRC; found {version}. "
                    "KiCad 7 can parse and export this source but lacks those CLI subcommands."
                )

            xml_netlist = reports / "netlist.xml"
            run([cli, "sch", "export", "python-bom", "-o", str(xml_netlist), str(SCHEMATIC)])
            audit_xml_netlist(xml_netlist)
            run([cli, "sch", "export", "pdf", "-o", str(reports / "schematic.pdf"), str(SCHEMATIC)])

            if major >= 8:
                run([cli, "sch", "erc", "--exit-code-violations", "-o", str(reports / "erc.rpt"), str(SCHEMATIC)])
                run(
                    [
                        cli,
                        "pcb",
                        "drc",
                        "--exit-code-violations",
                        "--schematic-parity",
                        "-o",
                        str(reports / "drc.rpt"),
                        str(BOARD),
                    ]
                )
                erc_drc = "pass"
            else:
                erc_drc = "unavailable_in_kicad_7_cli"

            run(
                [
                    cli,
                    "pcb",
                    "export",
                    "gerbers",
                    "-l",
                    "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts",
                    "-o",
                    str(gerbers) + os.sep,
                    str(BOARD),
                ]
            )
            run(
                [
                    cli,
                    "pcb",
                    "export",
                    "drill",
                    "--generate-map",
                    "--map-format",
                    "pdf",
                    "-o",
                    str(gerbers) + os.sep,
                    str(BOARD),
                ]
            )
            run(
                [
                    cli,
                    "pcb",
                    "export",
                    "pos",
                    "--format",
                    "csv",
                    "--units",
                    "mm",
                    "--side",
                    "both",
                    "-o",
                    str(manufacturing / "positions.csv"),
                    str(BOARD),
                ]
            )
            run(
                [
                    cli,
                    "pcb",
                    "export",
                    "pdf",
                    "-l",
                    "F.Fab,F.Silkscreen,Edge.Cuts",
                    "-o",
                    str(reports / "assembly.pdf"),
                    str(BOARD),
                ]
            )

        write_bom(manufacturing / "bom.csv")
        (reports / "pin-net-audit.json").write_text(
            json.dumps(
                {ref: pads for ref, (_, _, pads) in EXPECTED.items()},
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    finally:
        verify_authoritative_inputs_unchanged(source_hashes)

    provenance = {
        "algorithm": "SHA-256",
        "files": source_hashes,
        "verified_unchanged": True,
    }
    (reports / "source-inputs.json").write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    manufacturing_scope = {
        "assembly_release": "hold",
        "paste_gerbers": (
            [
                "manufacturing/gerbers/tmp117-F_Paste.gtp",
                "manufacturing/gerbers/tmp117-B_Paste.gbp",
            ]
            if major is not None
            else []
        ),
        "profile": (
            "fabrication_and_assembly_review_outputs"
            if major is not None
            else "source_audit_only"
        ),
    }
    status: dict[str, object] = {
        "source_audit": audit,
        "source_provenance": "reports/source-inputs.json",
        "kicad_cli": version,
        "erc_drc": erc_drc,
        "manufacturing_scope": manufacturing_scope,
    }
    (BUILD / "status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    expected = expected_output_files(major)
    validate_generated_outputs(expected, source_hashes, status, major)
    write_checksums(expected)
    validate_checksums(expected)
    validate_output_allowlist(expected | {"SHA256SUMS"})

    print(f"PASS: audited source and wrote {BUILD}")
    print("HOLD: outputs were not uploaded, ordered, or released for fabrication.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AuditError, OSError, subprocess.SubprocessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
