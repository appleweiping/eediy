# TMP117 KiCad source project

This is a reviewable, routed KiCad source project for the
[EEDIY PCB workflow](../../docs/en/guides/pcb-kicad.md). It is a 3.3 V
teaching board, not a released reference design or a fabrication order.

The authoritative inputs are `tmp117.kicad_pro`, `tmp117.kicad_sch`,
`tmp117.kicad_pcb`, and the project-local libraries under `library/`.
No global symbol or footprint library is required to parse them.

## Circuit boundary

| Item | Reviewed connection |
| --- | --- |
| TMP117 DRV pin 1 | SCL |
| pin 2 | GND |
| pin 3 | ALERT |
| pin 4 | ADD0 |
| pin 5 | 3V3 |
| pin 6 | SDA |
| exposed pad 7 | GND |
| J1 pins 1–6 | 3V3, GND, SDA, SCL, ALERT, ADD0 |

R1, R2, and R3 are 4.7 kΩ pull-ups for SDA, SCL, and ALERT. C1 is
100 nF from 3V3 to GND. JP1 is open by default: bridge 1–2 for ADD0=3V3
or 2–3 for ADD0=GND, never both. The selected pull-up value still needs a
bus-capacitance, rise-time, and sink-current check for the actual host.

The WSON footprint records the dimensions in the
[TI TMP117 data sheet](https://www.ti.com/lit/ds/symlink/tmp117.pdf):
2.0 mm × 2.0 mm nominal body, 0.45 mm × 0.30 mm perimeter lands,
0.65 mm pitch, and 1.95 mm row spacing. Pad 7 is a project-added
1.0 mm × 1.6 mm GND land based on the exposed-pad package dimensions.
TI's example land pattern shows the six perimeter lands, and the accuracy
table identifies an unsoldered thermal pad condition. Therefore pad 7,
paste coverage, thermal response, and assembly yield are explicit manual
review boundaries—not validated performance claims.

## One-command audit and export

With KiCad 8 or newer on `PATH`, run from the repository root:

```bash
python examples/tmp117-kicad/export.py --require-kicad
```

The command deletes and recreates only `examples/tmp117-kicad/build/`.
It blocks on ERC, DRC, schematic/PCB parity, exact pin/net mapping, and the
reviewed footprint anchors; then it writes:

- ERC/DRC reports, schematic PDF, and an assembly PDF;
- copper/mask/silkscreen/edge and top/bottom paste Gerbers, Excellon
  drill/map, placement CSV, and deterministic BOM;
- a machine-readable pin/net audit, run status, and `SHA256SUMS`.

The paste layers and placement file make this an
**assembly-review output set**, not an assembly-ready release: several BOM
rows intentionally have no selected manufacturer part number, and every run
records `assembly_release: hold` in `build/status.json`. The source-input
SHA-256 manifest proves that KiCad did not rewrite the reviewed project while
exporting it.

KiCad 7.0.11 can parse and export this project, but its `kicad-cli` has no
`sch erc` or `pcb drc` subcommands. During development, the same sources
were opened in KiCad 7.0.11 and the GUI reported 0 ERC messages and
0 DRC violations, with 0 unconnected pads and 0 footprint errors. A strict
headless release run intentionally requires KiCad 8+ so ERC/DRC cannot be
silently skipped. Running the script without `--require-kicad` permits a
KiCad 7 export or a source-only audit and records that limitation in
`build/status.json`.

## Hold points

Do not upload or order the generated files without an independent review of:

1. the current TI package revision and every pad number;
2. the actual connector family, mating-side pin view, and enclosure;
3. fabricator clearance, solder-mask, paste, drill, and stack-up rules;
4. Gerber/drill alignment in a separate viewer and placement rotation;
5. the ADD0 bridge choice and effective I²C/ALERT pull-up resistance.

This board makes no claim about thermal accuracy, EMC, production yield,
medical/body-connected use, or regulatory compliance. The runner performs
no network upload, ordering, or manufacturing action.
