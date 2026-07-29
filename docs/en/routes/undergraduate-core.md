---
title: "Undergraduate Core Audit"
description: "Covers mathematics, natural science, engineering core, laboratory practice, and capstone-style design for completeness auditing without claiming accreditation."
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: f3d8a61cc1345ada -->

# Undergraduate Core Audit

## Audience

Learners auditing a full undergraduate-level EE core

## Final outcome

Covers mathematics, natural science, engineering core, laboratory practice, and capstone-style design for completeness auditing without claiming accreditation.

## Stages

### Stage 0: diagnostics and tools

**Selection rule:** Complete all 6 required courses.

- [Single Variable Calculus](../courses/mathematics/001-18-01sc.md) — **Required**; MIT; Mainline; S
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **Required**; MIT; Mainline; S
- [Classical Mechanics](../courses/physics/010-8-01sc.md) — **Required**; MIT; Mainline; S
- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **Required**; MIT; Mainline; A
- [Introduction to CS and Programming Using Python](../courses/programming-tools/015-6-100l.md) — **Required**; MIT; Mainline; S
- [Practical Programming in C](../courses/programming-tools/016-6-087.md) — **Required**; MIT; Mainline; A

**Stage exit criterion:** Earn at least 80% on a timed diagnostic and reproduce the acquisition, unit checks, and fitting workflow for one mechanics or electromagnetics experiment in a single repository; every plot must rebuild on another machine using only the README.

### Stage 1: circuits and dynamics

**Selection rule:** Complete all 3 required courses; use the other 1 option only to close a specific gap.

- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **Required**; MIT; Mainline; S
- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **Required**; MIT; Mainline; S
- [Introduction to Electronics, Signals, and Measurement](../courses/electronics-laboratory/024-6-071j.md) — **Optional supplement**; MIT; Mainline; A
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **Required**; MIT; Mainline; S

**Stage exit criterion:** Derive state-space and frequency-domain models for a second-order circuit from its differential equation, then measure or simulate its step and swept-frequency responses; dominant pole, DC gain, and bandwidth must each agree with prediction within 5%.

### Stage 2: probability, digital, and fields

**Selection rule:** Complete all 4 required courses.

- [Probabilistic Systems Analysis and Applied Probability](../courses/probability-statistics/007-6-041sc.md) — **Required**; MIT; Mainline; S
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **Required**; MIT; Mainline; S
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **Required**; Cornell University; Mainline; S
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **Required**; Cornell University; Mainline; S

**Stage exit criterion:** Implement a digital module driven by stochastic inputs with at least 1,000 reproducible test vectors and submit an electromagnetic model of its interconnect; logic mismatches must be zero and simulated power-balance residual must stay below 5%.

### Stage 3: laboratory and fabrication

**Selection rule:** Complete all 3 required courses.

- [Introductory Analog Electronics Laboratory](../courses/analog-electronics/026-6-101.md) — **Required**; MIT; Mainline; S
- [The Art and Science of PCB Design](../courses/pcb-eda/055-iap-pcb-2026.md) — **Required**; MIT; Mainline; S
- [Digital Systems Design Using Microcontrollers](../courses/capstone-practice/057-ece-4760-ece-5730.md) — **Required**; Cornell University; Mainline; S

**Stage exit criterion:** Fabricate and commission a PCB containing an analog front end and digital control, preserving traceable calibration data, a test matrix of at least ten operating points, rework history, and hardware photographs; every requirement must map to test evidence.

### Stage 4: concentration choices

**Selection rule:** Complete all 1 required course and choose 2 of 5 elective options.

- [Digital Signal Processing](../courses/dsp/088-res-6-008.md) — **Required**; MIT; Mainline; S
- [Principles of Digital Communications I](../courses/communications/100-6-450.md) — **Elective option**; MIT; Mainline; S
- [Introduction to Linear Dynamical Systems (2008 Archive)](../courses/control-systems/068-ee-263.md) — **Elective option**; Stanford University; Mainline; S
- [Power Electronics](../courses/power-electronics/114-6-622.md) — **Elective option**; MIT; Mainline; S
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **Elective option**; Cornell University; Mainline; A
- [Introduction to Photonics](../courses/optics-photonics/132-108106135.md) — **Elective option**; IIT Madras / NPTEL; Mainline; A

**Stage exit criterion:** Integrate the signal-processing spine with two selected concentrations in one design review, defining at least two subsystem metrics per concentration and validating them with simulation, measurement, or public data; the final report must include interface risks and one failed iteration.

## Execution rules

- Follow each stage's selection rule: complete every required course and the stated number of electives; when complete path options are provided, choose one and finish every course in its listed order; use optional supplements only to close a specific gap.
- Produce at least one reproducible artifact per stage and include failed attempts in the retrospective.
- Work involving mains voltage, high voltage, RF exposure, lasers, chemicals, or fabrication equipment requires local-law compliance and qualified supervision.
