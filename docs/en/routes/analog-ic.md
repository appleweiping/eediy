---
title: "Analog, Mixed-Signal, and Integrated Circuits"
description: "Complete an analog or mixed-signal design with specifications, corner simulation, noise/power tradeoffs, and layout checks."
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 27c5f4701740fac0 -->

# Analog, Mixed-Signal, and Integrated Circuits

[中文](../../routes/analog-ic.md) · [← Learning routes](index.md)

## Audience

Learners progressing from circuits and devices to transistor-level design, simulation, and layout

## Final outcome

Complete an analog or mixed-signal design with specifications, corner simulation, noise/power tradeoffs, and layout checks.

!!! warning "Mainline audit review in this route"
    - [Analog IC Design](../courses/analog-ic/036-108106105-noc26-ee66.md): The official 2026 twelve-week video syllabus is confirmed, but graded feedback and the certificate exam depend on enrollment, no open EDA project is supplied, and the resource manifest still contains only the older archive. Last audited: 2026-07-29.

## Stages

### Circuits and devices

**Selection rule:** Complete all 3 required courses and choose 1 of 2 elective options.

- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **Required**; MIT; Mainline; S
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **Required**; Cornell University; Mainline; S
- [Microelectronic Devices and Circuits](../courses/microelectronics/030-6-012.md) — **Elective option**; MIT; Alternative; A
- [Microelectronic Devices and Circuits](../courses/microelectronics/031-ee-105.md) — **Elective option**; University of California, Berkeley; Alternative; A
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **Required**; Cornell University; Mainline; A

**Stage exit criterion:** Extract MOS-device parameters from public or simulated I–V/C–V curves and use the same model to predict a bias circuit's DC, AC, and transient responses; normalized RMSE on held-out data must stay below 10%.

### Analog design

**Selection rule:** Complete all 1 required course and choose 2 of 3 elective options. The other course is an optional supplement and does not count toward the elective requirement.

- [Introductory Analog Electronics Laboratory](../courses/analog-electronics/026-6-101.md) — **Required**; MIT; Mainline; S
- [Solid-State Circuits](../courses/analog-electronics/032-6-301.md) — **Elective option**; MIT; Supplement; B
- [Analog Circuits](../courses/analog-electronics/034-108101094.md) — **Elective option**; IIT Bombay / NPTEL; Alternative; A
- [Integrated Circuits, MOSFETs, OP-Amps and Their Applications](../courses/analog-electronics/035-108108111.md) — **Elective option**; Indian Institute of Science / NPTEL; Alternative; A
- [Analog IC Design](../courses/analog-ic/036-108106105-noc26-ee66.md) — **Optional supplement**; IIT Madras / NPTEL; Mainline; A; **Audit review**

**Stage exit criterion:** Design an op-amp or low-noise front end and verify gain, bandwidth, phase margin, noise, slew rate, and power specifications individually; all PVT and load corners must pass, or any miss must be captured as a reproducible tradeoff.

### Integrated implementation

**Selection rule:** Complete all 2 required courses; use the other 1 option only to close a specific gap.

- [Analysis and Design of Digital Integrated Circuits](../courses/vlsi-ic/050-6-374.md) — **Required**; MIT; Mainline; A
- [VLSI Systems](../courses/vlsi-ic/051-ece-4740.md) — **Optional supplement**; Cornell University; Supplement; A
- [Micro/Nano Processing Technology](../courses/fabrication-mems/126-6-152j.md) — **Required**; MIT; Mainline; S

**Stage exit criterion:** Submit a layout and signoff package with explicit process assumptions, zero DRC and LVS errors, and a pre- versus post-layout comparison of key metrics; parasitic-driven changes must be quantified and every specification miss must have a layout-level remedy.

## Execution rules

- Follow each stage's selection rule: complete every required course and the stated number of electives; when complete path options are provided, choose one and finish every course in its listed order; use optional supplements only to close a specific gap.
- Produce at least one reproducible artifact per stage and include failed attempts in the retrospective.
- Work involving mains voltage, high voltage, RF exposure, lasers, chemicals, or fabrication equipment requires local-law compliance and qualified supervision.
