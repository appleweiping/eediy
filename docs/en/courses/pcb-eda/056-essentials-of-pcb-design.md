---
title: "Essentials of PCB Design"
description: "Worcester Polytechnic Institute's Essentials of PCB Design supplements PCB practice with slides, starter files, KiCad materials, and GitHub resources, while recordings are restricted and fabrication is self-funded."
page_type: course
course_id: "course-056"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 4df78a52c41da7fe -->

# Worcester Polytechnic Institute: Essentials of PCB Design

## Course Overview

- **University:** Worcester Polytechnic Institute
- **Course code:** Essentials of PCB Design
- **Official prerequisites:** No provider-published hard prerequisite verified; recheck the course page
- **EEDIY preparation:** Circuit Analysis; Electronics Laboratory and Measurement
- **Access:** Open without registration
- **Material status:** 2026-07-30; public-material guide

### A Strong First Complete PCB

WPI’s [Essentials of PCB Design](https://pcb.wpi.edu/) is a short practicum created in 2024: after 4 evening lectures, students spend about 2 weeks turning a supplied schematic into an Arduino-compatible MCU board that can drive up to 30 RGB LEDs. It teaches a complete pass from schematic and footprints to fabrication files and bring-up. Choose a specialist course instead for high-speed design, RF, EMC, or production reliability.

You should already read power, ground, and digital interfaces, consult a datasheet, and check for shorts with a multimeter. KiCad experience is optional. If MCU power, decoupling, and connector pinouts are still opaque, study basic circuits first.

### Course materials

WPI’s official course project materials live in the [course repository](https://github.com/ieee-wpi/pcb), organized into `slides`, `datasheets`, `starter_board`, `sample_board`, and `code`. Read the [4 lecture decks](https://github.com/ieee-wpi/pcb/tree/main/slides), then copy the [starter board](https://github.com/ieee-wpi/pcb/tree/main/starter_board). Use the [sample board](https://github.com/ieee-wpi/pcb/tree/main/sample_board) to inspect functional placement, power paths, connector orientation, and silkscreen—not to trace its routing. The companion [code](https://github.com/ieee-wpi/pcb/tree/main/code) establishes intended behavior, but symbols, footprints, and physical pins still need line-by-line verification.

### Review the Design at 3 Milestones

The schematic review resolves every ERC warning and lists voltage domains,
peak current, programming access, test points, and sources for critical parts.
Milestone 2 checks the outline, holes, connectors, MCU, decoupling, and
high-current paths. Milestone 3 checks routing and DRC, including
copper-to-edge clearance, return paths, silkscreen over pads, and fabricator
limits.

Record the major [KiCad](https://www.kicad.org/) version. Generate Gerbers,
drill files, BOM, position files, and the assembly drawing as a single export set,
then inspect those exports in an independent viewer. Arrange peer review; if
working alone, review again on a later day.

### Bring-up Matters Beyond DRC

After assembly, inspect orientation and solder bridges, then measure power-to-ground resistance. Use a current-limited supply for first power, verify rails before attaching the programmer, and test the MCU, LEDs, and added peripheral in stages. Record each failure’s probe point, expected value, measured value, and repair. If the board was never fabricated, call the result a fabrication package—not validated hardware.

The public repository does not include WPI office hours, free fabrication, assembly help, or account-gated recordings. Sources, rules, ERC/DRC dispositions, manufacturing files, BOM, bring-up checklist, and photos should remain consistent throughout; if the board was not made, stop explicitly at the fabrication package. Limit the first board to a low-voltage, low-speed peripheral. High-speed USB, switch-mode power, RF, lithium charging, and mains interfaces belong in later study.

## Course Resources

- [Course home](https://pcb.wpi.edu/)
- [Code · WPI PCB course source, starter board, and sample board](https://github.com/ieee-wpi/pcb)

## Resource Summary

Every public entry point verified in this review is listed above. Use the feedback and corrections links below to submit a completion record, another resource, or a broken-link report.
