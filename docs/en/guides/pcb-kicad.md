---
title: PCB and KiCad Workflow
description: Close the PCB design loop from requirements, schematic, and rules to fabrication output and controlled power-up.
---

<div class="ee-language" markdown>
[简体中文](../../guides/pcb-kicad.md)
</div>

# PCB and KiCad Workflow

PCB design is not arranging wires neatly. It jointly implements electrical, mechanical, manufacturing, test, and safety constraints. KiCad is a common open-source example; this workflow rests on tool-independent netlists, rules, review, and manufacturing evidence.

## Purpose and learning outcomes

- Build a constraint table from interface, power, and mechanical requirements.
- Create reviewable schematic hierarchy, net names, and test points.
- Set rules for clearance, width, return paths, thermal behavior, and assembly.
- Run electrical and design-rule checks and justify every waiver.
- Export a traceable BOM, fabrication package, and controlled power-up plan.

## Minimal environment

- A PCB EDA that exports netlists, fabrication files, and check reports.
- Data sheets and package-dimension sources.
- Version control plus PDF or 3D review paths.
- A low-voltage, current-limited practice board, or a design-only exercise.

Record the observed EDA, library, and plugin versions. Retain project-local symbols and footprints or rebuildable pinned references so global-library changes cannot silently alter the design.

## Learning sequence

1. **Requirements:** list supplies, interfaces, signal speed, mechanical boundary, environment, and acceptance method.
2. **Schematic:** group by function and label power, direction, intentionally unconnected pins, and critical calculations.
3. **Footprint audit:** compare pin numbers, polarity, dimensions, and pads against the data sheet.
4. **Placement and return:** place connectors, power, and critical devices first, then preserve continuous return paths.
5. **Rule checking:** run ERC and DRC; fix every warning or write an evidence-based waiver.
6. **Manufacturing and test:** produce BOM, placement, layers, assembly drawing, and staged power-up table.

## Verification task: low-voltage sensor interface

Design a low-voltage sensor interface powered by a current-limited bench supply:

1. Write requirements covering voltage, maximum current, connector orientation, and test points.
2. Complete the schematic and verify every device pin and absolute maximum rating.
3. Define separate network rules for power, analog signals, and digital interfaces.
4. Lay out decoupling, protection, and return paths; export an annotated review PDF.
5. Run ERC and DRC and produce a report with zero unexplained findings.
6. Export a fabrication bundle and power-up checklist; manufacturing is not required to finish the exercise.

Acceptance means another learner can inspect connectivity, footprints, rules, and test access from the evidence bundle alone.

## Common failures and diagnosis

- **The schematic is right but the board connects backward:** verify connector viewpoint, pin 1, polarity, and assembly side.
- **Pads do not fit the package:** compare the recommended land pattern and physical dimensions instead of guessing by name.
- **DRC passes through many waivers:** record each rationale; an unexplained waiver is unfinished work.
- **Digital works but analog noise is high:** inspect return path, decoupling, reference, measurement bandwidth, and coupling.
- **The fabricator rejects the order:** verify stack, drills, outline, minimum rules, and file units.
- **Power-up current is excessive:** disconnect immediately, then inspect rail resistance, polarity, shorts, and functional sections.

## Reproducible evidence

- Requirements and interface-control table.
- Schematic, PCB, project libraries, and pinned configuration.
- Footprint audit and data-sheet provenance.
- ERC/DRC reports and justified waivers.
- BOM with part numbers, ratings, and substitution strategy.
- Fabrication-output checksums and viewer images or PDFs.
- Test-point map, power-up steps, and acceptance record.

## Cost, licensing, and accessibility

A design-only exercise has no manufacturing cost. Before ordering, estimate board, parts, shipping, assembly, and rework and set a stop budget. Check licenses for EDA, libraries, device models, and manufacturing templates; third-party trademarks and restricted reference designs cannot be republished casually.

Do not communicate schematic and PCB meaning through color alone. Use net names, layer labels, line patterns, and annotations. Export high-contrast PDFs, a BOM table, and text reports for reviewers without the EDA or using assistive technology.

## Safety boundaries

- Keep a beginner board at safe low voltage and bounded current, with a conservative current limit before power-up.
- Mains, higher voltage, stored energy, power conversion, RF power, and medical interfaces are unsuitable unsupervised first boards.
- Clearance, thermal protection, fusing, and grounding cannot rely only on software defaults.
- Lithium charging, unknown supplies, and body connections require qualified design and supervision.
- Use sectional tests and a setup that can disconnect power immediately on first power-up.

## Completion checklist

- [ ] Requirements, interfaces, mechanics, and acceptance conditions are explicit.
- [ ] Every symbol-to-footprint pin mapping is verified.
- [ ] Critical net rules and return paths have been reviewed.
- [ ] ERC and DRC contain no unexplained finding.
- [ ] BOM, fabrication output, and checksums are complete.
- [ ] PDF and text exports allow review without the original tool.
- [ ] Power-up steps include current limiting, stop conditions, and measurement points.
- [ ] Licensing, budget, and substitution risks are recorded.

Next, plan board validation with [Instrumentation and Measurement](instrumentation-measurement.md), or revisit [SPICE Circuit Simulation](spice-simulation.md) for effects not yet modeled.
