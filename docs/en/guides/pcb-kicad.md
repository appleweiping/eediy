---
title: PCB and KiCad Workflow
description: Follow one low-voltage sensor board from device documentation and schematic capture through fabrication output and first power.
page_type: guide
comments: true
---

# PCB and KiCad Workflow

This page follows one 3.3 V TMP117 temperature-sensor board through the whole
workflow. It contains the sensor, I²C pull-ups, address selection, decoupling,
ALERT, and a host connector. That is small enough to understand but still
exposes connector-view, package-numbering, return-path, thermal-placement,
and missing-layer errors. ERC and DRC help with only part of that list.

| Stage | What to check | If it fails |
| --- | --- | --- |
| Device and package | Data-sheet pin/package comparison and fixed KiCad/library versions | Hold the schematic |
| Schematic | Interface table, explained ERC results, symbol-to-pad review | Hold placement |
| Layout | Fabrication rules, return/thermal/assembly review, layer-by-layer DRC | Hold production export |
| Manufacturing files | Independently viewed Gerber, drill, BOM, placement data, and checksums | Hold the order |
| First power | Unpowered inspection, current-limit plan, staged measurement record | Disconnect on an anomaly and return to fault isolation |

The exercise can end after checking the manufacturing files without ordering
a board. Physical bring-up is restricted to a safe, current-bounded
low-voltage supply; the table does not cover higher-energy or regulated
hardware.

## Fix the version, libraries, and physical package

As of July 2026, KiCad's official stable release is [10.0.5](https://www.kicad.org/blog/2026/07/KiCad-10.0.5-Release/). Record the full version actually used, not merely “KiCad 10”; patch releases, global libraries, and plugins can change an export. Commit the `.kicad_pro`, `.kicad_sch`, `.kicad_pcb`, and any project-specific symbols and footprints. Prefer `${KIPRJMOD}` paths to project-local `.kicad_sym` and `.pretty` libraries. The day an order is prepared is a poor time to migrate the file format.

Use the DRV (WSON-6) option in the [TI TMP117 data sheet](https://www.ti.com/lit/ds/symlink/tmp117.pdf) for this exercise. Before trusting a library name, extract a small device table from the source:

| Item | What must come from the data sheet |
| --- | --- |
| Pins | Numbers for SCL, GND, ALERT, ADD0, V+, and SDA; ALERT and SDA are open-drain nodes |
| Supply | Recommended operation and absolute maximum ratings are different; this board uses 3.3 V |
| Package | Top/bottom view, pad numbering, exposed-pad treatment, solder-mask and paste guidance |
| Application | Decoupling, pull-ups, ADD0 wiring, and the intended thermal path around the sensor |

In the footprint editor, highlight every pad in turn and compare it with the mechanical drawing. Then print a 1:1 plot or use the assembler's package preview to check physical dimensions. The question is whether the real part can be mounted in the correct orientation onto the intended nets. An attractive 3D model does not answer it.

## Make the interface table and schematic cross-check each other

The [KiCad 10 Schematic Editor manual](https://docs.kicad.org/10.0/en/eeschema/eeschema.html) describes ERC, no-connect flags, power symbols, and project libraries. Before drawing, write an interface table for every host-connector pin: direction, logic voltage, board-side versus mating-side view, location of pull-ups, and an accessible test point. For this board, the schematic should make the following questions answerable:

- When the host is absent, do SDA, SCL, and ALERT have defined states? If the host also provides pull-ups, does their parallel value still satisfy sink-current and rise-time requirements?
- Which address follows from the ADD0 connection? The configuration should be visible in a note and on silkscreen, not hidden in copper.
- Is connector pin 1 shown from the mating face or the solder face, and does the symbol numbering agree with the physical drawing?
- Which pins are intentionally unused? A no-connect flag records intent; it should not be used to silence an ERC result that has not been understood.
- Where does 3.3 V originate, what range and maximum current are expected, and can each test point be contacted without touching its neighbour?

`PWR_FLAG` tells ERC that a net is driven. It neither creates a supply nor proves its polarity. Resolve each ERC message at the circuit level: a missing driver usually calls for a wiring or power-model fix; a genuine symbol-model limitation deserves a short note beside the exception. After capture, compare symbol pin numbers with footprint pad numbers once more as a separate pass.

## Review placement for return current, heat, and assembly

The [KiCad 10 PCB Editor manual](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html) covers outlines, net classes, clearances, zones, and DRC. Actual board rules must also come from the intended fabricator's stack-up, minimum trace and space, drill size, solder-mask bridge, and edge requirements. KiCad defaults are not a fabrication capability statement.

Lay out this board in the following order:

1. Lock the outline, mounting holes, and connector. Check plug housing, finger access, pin-1 marking, and overhang at the board edge.
2. Put the TMP117 where it represents the temperature of interest. For ambient measurement, keep regulators, LEDs, and large heat-carrying copper away. For PCB-temperature measurement, design that thermal coupling deliberately.
3. Place the bypass capacitor near V+ and GND so the supply-current loop is short and legible. Plan a continuous reference plane before routing SDA, SCL, and ALERT; do not send them across a split in that reference.
4. Create only the net classes justified by current and fabrication limits. A low-speed I²C link does not acquire controlled-impedance requirements merely to make the design look sophisticated, but long stubs, missing connector return paths, and needless coupling still matter.
5. Provide labelled 3V3, GND, SDA, SCL, and ALERT test points. Check probe landing area, fixture access, and rework clearance in the actual component geometry.

DRC can find formal spacing, unrouted-net, and hole-to-copper violations. It cannot recognize a reversed connector viewpoint, sensor self-heating, a detoured return current, or a test point that no probe can reach. Inspect copper, solder mask, silkscreen, outline, and drilling layer by layer in 2D, then use 3D for component orientation and mechanical interference. The two views answer different questions.

## Reopen the manufacturing files outside KiCad

The [KiCad 10 command-line manual](https://docs.kicad.org/10.0/en/cli/cli.html) documents automatable ERC, DRC, and export commands. The following is suitable for a project script or CI job; substitute the project filenames:

The repository's [executable TMP117 KiCad starter](https://github.com/appleweiping/eediy/tree/main/examples/tmp117-kicad) includes modern project sources, project-local symbol and footprint libraries, a routed two-layer PCB, an exact pin audit, and a manufacturing-file exporter. With KiCad 8 or newer, one command rebuilds `build/` and returns nonzero for any ERC, DRC, or schematic-to-PCB parity failure:

```bash
python examples/tmp117-kicad/export.py --require-kicad
```

The example performs no ordering action. The exposed pad, actual connector, effective pull-up value, thermal response, and fabricator rules remain explicit manual-review boundaries.

```bash
kicad-cli sch erc --exit-code-violations -o build/erc.rpt sensor-node.kicad_sch
kicad-cli pcb drc --exit-code-violations --schematic-parity --refill-zones -o build/drc.rpt sensor-node.kicad_pcb
kicad-cli pcb export gerbers -o build/gerbers sensor-node.kicad_pcb
kicad-cli pcb export drill -o build/gerbers --generate-map --generate-report sensor-node.kicad_pcb
```

`--exit-code-violations` turns rule findings into a nonzero exit status. `--schematic-parity` compares board and schematic, while `--refill-zones` prevents DRC from operating on stale pours. Automation makes an action repeatable; it does not explain an excluded finding. Keep exclusions local and scarce, with the applicable data-sheet or fabricator rule beside each one.

Open the resulting Gerbers, Excellon drill data, BOM, placement file, and assembly drawing in an independent viewer. Confirm that the outline occurs once, copper and mask are not mirrored, plated and non-plated holes are distinguished, drills are centred on pads, and silkscreen does not cover exposed pads. Record the complete KiCad version, export commands, and package checksums. After a net changes, those details reveal whether the manufacturing data was actually regenerated.

## Begin first power-up with an unpowered inspection

Do not attach the host as soon as boards arrive. Compare the assembly with its drawing and inspect orientation, solder bridges, missing or wrong parts, and connector pin 1. With power removed, measure rail-to-ground resistance and compare the result with the circuit's expected behaviour. There is no universal resistance above which every board is safe, but a near short or a large difference between nominally identical boards must be located first.

Apply only 3.3 V and ground initially. Set the supply limit above the expected idle current but well below a fault current that could damage traces or parts. Watch for constant-current operation, a collapsed board voltage, and local heating; disconnect immediately for unexpected current, odour, smoke, or a polarity error. Never use an ohmmeter on a powered board, and do not use a fingertip as a temperature instrument.

Only after the rail is stable should the host be connected. Check idle logic levels, the I²C address, register reads and writes, and ALERT behaviour in that order. If a bus line is held low, remove the host to divide the fault between board and host, then inspect bridges, pull-up voltage, device orientation, and pin multiplexing. The useful output is the source project and local libraries, the device pin comparison, ERC/DRC reports, independently viewed fabrication data, voltage/current notes from first power, and the localization trail for every anomaly.

This exercise is confined to safe low voltage and bounded current. Mains, higher voltage, lithium charging, stored energy, power conversion, RF power, and body-connected circuits introduce insulation, thermal, protection, and regulatory problems and are unsuitable unsupervised first boards. Clearance, fusing, and grounding defaults in an editor are not substitutes for that engineering.

The project record should state any remaining deviations and why ordering or
power-up is still on hold—not merely show a screenshot that says DRC passed.
Design board-level observations with [Instrumentation,
Measurement, and Uncertainty](instrumentation-measurement.md). If the expected
supply or analog behaviour remains unclear, [SPICE Circuit
Simulation](spice-simulation.md) should first produce an inspectable operating
point and response prediction; physical power-up waits in the meantime.
