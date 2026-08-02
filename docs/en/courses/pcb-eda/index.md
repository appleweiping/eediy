---
title: "PCB, EDA, and Hardware Verification"
description: "Schematics, layout, fabrication outputs, BOMs, debugging, and reviews that turn simulations into manufacturable hardware."
page_type: track
track_id: "track-pcb-eda"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 352f461aea0f7ebe -->

# PCB, EDA, and Hardware Verification

## Track position

Schematics, layout, fabrication outputs, BOMs, debugging, and reviews that turn simulations into manufacturable hardware.

## Recommended prerequisite tracks

- [Circuit Analysis](../circuits/index.md)
- [Electronics Laboratory and Measurement](../electronics-laboratory/index.md)

## Eight MIT laboratories are enough to produce a first board

[MIT IAP PCB 2026](055-iap-pcb-2026.md) organizes its [official course site](https://pcb.mit.edu/) around 8 KiCad and Altium laboratories, progressing through schematic capture, layout, review, manufacturing output, and bring-up. Notes, source, and the course flow are openly licensed, although Panopto access, fabrication, and BOM cost still require a current check. [WPI Essentials of PCB Design](056-essentials-of-pcb-design.md) publishes slides, starter and sample boards, and KiCad or GitHub material on its [official site](https://pcb.wpi.edu/); recordings require a WPI account. A first board can follow the complete MIT laboratory rhythm and use the WPI sample only to compare directory, library, and submission organization. Learners interested solely in schematic reading or manufacturing review may stop after digital review rather than order hardware for ceremonial completion.

## Schematic, layout, and manufacturing package receive different reviews

The schematic review begins with an interface table. For every connection on a low-voltage sensor or MCU board, state supply and current, logic levels, connector pins, source and load, bandwidth, and test point. Separate absolute maxima, recommended operation, and footprint data from each datasheet. This applies power, return paths, interface impedance, filtering, and decoupling from [circuit analysis](../circuits/index.md): calculate worst-case rail current, draw the return path of fast or pulsed currents, and explain the time scales addressed by pull-ups, bulk capacitance, and local bypass. Passing ERC in an MIT lab means no configured connection rule fired; it does not prove that the interface choice is sound.

The layout review examines placement, decoupling loops, return paths, connectors and ESD, power copper, test points, and assembly orientation. Name the source and license of self-authored and third-party symbols, footprints, and 3D models, and compare pin numbering, courtyard, paste, mask, and land pattern with the datasheet. The manufacturing review concerns Gerber, drill, and placement files that machines actually consume. Stack-up, minimum trace and space, drills, copper weight, controlled impedance, and panel rules belong to a particular quotation. Open every export in an independent viewer and inspect board outline, holes, solder mask, and polarity layer by layer; an editor screenshot is not production input. The WPI sample board is a second file-organization example for checking that library paths and fabrication notes travel with the project.

## Bring-up starts at the current-limited supply, not the firmware demo

The project directory includes requirements, a block diagram, interface and power budgets, editable schematic and PCB, ERC and DRC output, rule sources, BOM and alternates, Gerbers, drill and placement files, and a fabrication README. State the KiCad, ngspice, gerbv, and Git versions. BOM choices account for regional stock, alternates, EOL, and assembly orientation. If a recording or proprietary Altium step is inaccessible, name the functionally equivalent KiCad operation rather than calling the migrated procedure the original lab.

Physical work proceeds only on an isolated, current-bounded low-voltage board. Apply unpowered continuity, short, polarity, and probe-connection checks from [electronics laboratory](../electronics-laboratory/index.md), then energize one rail at a time. Examine quiescent current and critical nodes before functional tests and controlled open or short cases. Batteries, motors, relays, and external energy ports need additional protection. Keep the first failed check in the bring-up log and connect it to a schematic node, layout location, manufacturing file, or assembly orientation, followed by the result after revision. The fabricator input and bench evidence then close on one concrete rework.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [The Art and Science of PCB Design](055-iap-pcb-2026.md) | MIT | Main course | Public-material guide | Partial or restricted |
| [Essentials of PCB Design](056-essentials-of-pcb-design.md) | Worcester Polytechnic Institute | Supplement | Public-material guide | Public assignments or labs |
