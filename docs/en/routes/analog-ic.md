---
title: "Analog, Mixed-Signal, and Integrated Circuits"
description: "Use the public Berkeley EE 140/240A problems and lab specifications as the analog-IC spine, completing specifications, bias, noise, and only the PVT/load corners supported by the available models. The default exit is schematic-level. Add an independent layout study only after validating open EDA, a lawfully usable educational PDK, DRC/LVS, and extraction models; this route does not promise to reproduce Berkeley's campus Cadence flow or complete PEX."
page_type: route
route_id: "route-analog-ic"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: fb3fbf2319786712 -->

# Analog, Mixed-Signal, and Integrated Circuits

## Audience

Learners moving from device curves and small-signal circuits to transistor-level design, corner simulation, and layout

## What you should be able to do

Use the public Berkeley EE 140/240A problems and lab specifications as the analog-IC spine, completing specifications, bias, noise, and only the PVT/load corners supported by the available models. The default exit is schematic-level. Add an independent layout study only after validating open EDA, a lawfully usable educational PDK, DRC/LVS, and extraction models; this route does not promise to reproduce Berkeley's campus Cadence flow or complete PEX.

## Pass the EE 105 capability check before installing a PDK

Attempt an EE 105/6.012-level MOS bias and small-signal problem, then open Spring 2025 EE 140/240A HW1 and the public Lab 1. If gm, ro, poles, and feedback are not yet independent skills, repair the device bridge before installing a PDK.

Use EE 105, 6.002, and ECE 3150 to connect device curves, bias, and small-signal analysis. Read 6.012 or ECE 4070 only for a missing device-physics topic rather than repeating another survey.

## Make the schematic spine real first

- Use EE 140/240A as the transistor-level spine: work through the public material on bias, gain, frequency response, feedback, noise, and output swing, establishing an off-campus baseline with the LTspice scope of Lab 1.
- If an open toolchain and educational PDK are independently validated, take one frozen schematic through DRC/LVS. Compare pre- and post-parasitic behavior only when extraction rules and models actually exist, and scope every conclusion to the named PDK and tool versions.

## Layout is a separate claim, not a default bonus

- Do not end the analog route with MIT 6.374 or Cornell ECE 4740 digital-IC/VLSI labs; those belong to the digital-layout route.
- Without Berkeley server access, skip any claim of reproducing Labs 2–8 or the course project. Without a validated extraction model, omit PEX numbers instead of filling in a placeholder result.
- The default stop is schematic-level: the specification table, bias, AC/transient/noise analysis, and supported PVT/load sweeps rerun, with failed corners and tradeoffs retained.
- The independent layout branch ends only when DRC/LVS are clean under the stated rules. PEX is an optional next layer, not a gate to pretend to meet when public extraction evidence is absent.

## How to proceed

### From device curves to bias

**Why these courses:** 6.002 supplies circuit analysis and ECE 3150 supplies small-signal device work. EE 140/240A explicitly names EE 105 as its prerequisite, so EE 105 is the required bridge in this route. Existing equivalent competence may replace retaking the entire course only after an unaided diagnostic covering MOS bias, small-signal behavior, frequency response, and feedback; it cannot remove the capability check. Use 6.012 or ECE 4070 only for remaining device-derivation or semiconductor-physics gaps.

- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **Required**; MIT
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **Required**; Cornell University
- [Microelectronic Devices and Circuits](../courses/microelectronics/031-ee-105.md) — **Required**; University of California, Berkeley
- [Microelectronic Devices and Circuits](../courses/microelectronics/030-6-012.md) — **Use if needed**; MIT
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **Use if needed**; Cornell University

**Move on when:** Extract MOS parameters from public or simulated I–V/C–V curves, then use that same model to predict a bias circuit's DC, AC, and transient behavior. Before fitting, state the allowed error from data resolution, noise, or solver accuracy. Report normalized RMSE on held-out data and mark the bias regions where the model fails.

### EE 140/240A spine and an honest layout ceiling

**Why these courses:** The Spring 2025 EE 140/240A homework, partial solutions, exams, and Lab 1 form the spine. Labs 2–8 and the project depend on Cadence/Virtuoso, Berkeley servers, and a SKY130 environment that has not been validated as an off-campus reproduction package. Use NPTEL material for explanation, 6.152J only for process context, and 6.101 only with a real low-voltage bench. Layout is an independently validated study, not a course lab these public materials automatically provide.

- [Analog Integrated Circuits](../courses/analog-ic/141-ee-140-ee-240a.md) — **Required**; University of California, Berkeley
- [Analog Circuits](../courses/analog-electronics/034-108101094.md) — **Use if needed**; IIT Bombay / NPTEL
- [Integrated Circuits, MOSFETs, OP-Amps and Their Applications](../courses/analog-electronics/035-108108111.md) — **Use if needed**; Indian Institute of Science / NPTEL
- [Analog IC Design](../courses/analog-ic/036-108106105-noc26-ee66.md) — **Use if needed**; IIT Madras / NPTEL
- [Micro/Nano Processing Technology](../courses/fabrication-mems/126-6-152j.md) — **Use if needed**; MIT
- [Introductory Analog Electronics Laboratory](../courses/analog-electronics/026-6-101.md) — **Use if needed**; MIT

**Move on when:** First deliver a schematic-level design with repeatable gain, bandwidth, phase margin, noise, slew rate, power, and supported PVT/load corners, retaining every miss. If an independent layout is added, name the tool, educational PDK, and rule deck and obtain clean DRC/LVS. Report PEX only when extraction rules and models actually exist, and never call the result tapeout signoff.
