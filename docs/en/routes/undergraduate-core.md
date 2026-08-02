---
title: "Undergraduate EE Core"
description: "Move from mathematics, physics, and programming through circuits, signals, digital systems, fields, devices, laboratory work, and a two-area final design. The route can expose gaps in an undergraduate foundation, but it grants no degree, credit, or accreditation."
page_type: route
route_id: "route-undergraduate-core"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 27e446ecb4c0d43d -->

# Undergraduate EE Core

## Audience

Learners rebuilding the breadth and depth of an undergraduate EE education, including laboratory work and an integrated design

## What you should be able to do

Move from mathematics, physics, and programming through circuits, signals, digital systems, fields, devices, laboratory work, and a two-area final design. The route can expose gaps in an undergraduate foundation, but it grants no degree, credit, or accreditation.

## Place yourself before copying a syllabus

Sample one problem each from calculus, linear algebra, electromagnetism, circuit transients, and probability, then write one small Python model. Record anything you cannot solve or can solve only by copying as a gap. That gap list, not institutional prestige, determines the order.

## Keep one spine at each layer

- Keep one object through every stage, such as a second-order RLC network or a motor-converter pair. Derivations, code, field models, and experiments should update the same parameters instead of becoming unrelated course exercise sets.
- Attempt the end-of-stage task first and study only the units that failed. During laboratory work, retain calibration, uncertainty, ratings, and failed runs, labeling simulation, public data, and measurement separately.
- Join exactly two final areas that share a real interface, and define its quantities, units, update rate, allowed error, and shutdown conditions before implementation.

## Defer specialization until the core can challenge it

- Skip any course whose stage task you can already pass on new parameters, and do not take two alternatives for the same gap.
- When equipment, a license, or an institutional starter is unavailable, skip the physical reproduction and use a bounded simulation or public dataset instead of hiding the gap behind a future promise.

## Use a cross-layer artifact for the undergraduate exit

- Each of the five stages has a reviewable artifact, parameters and failures trace forward, and both interface scenarios in the final design pass the tolerances written before testing.
- If the goal is one specialization, move to its focused route after the relevant stage. Do not add courses for a feeling of undergraduate completeness, and never present route completion as a degree or credential.

## How to proceed

### Secure single-variable calculus first

**Why these courses:** 18.01SC is the common starting point for 18.02SC and the later probability course. Begin with its diagnostic problems. If limits, derivatives, integrals, and series are already secure, complete only the failed units, but keep a closed-book retest with changed parameters rather than treating prior enrollment as evidence.

- [Single Variable Calculus](../courses/mathematics/001-18-01sc.md) — **Required**; MIT

**Move on when:** Solve a fresh set of limit, derivative, definite-integral, and series problems without consulting solutions, then carry one dimensional physical quantity from model through analytical result to numerical plot with consistent domains and units.

### Multivariable calculus, physics, and programming

**Why these courses:** Carry forward the single-variable foundation, then use problems from 18.02SC, 18.06SC, and 8.01SC/8.02X to find gaps in multivariable calculus, linear algebra, mechanics, and electromagnetism, revisiting only the weak units. Let 6.100L supply Python modeling and 6.087 supply C and memory work on the same physical case. Reproduce an experiment only with the safe equipment required by the course; otherwise use public data or simulation and state the data origin plainly in the README.

- [Multivariable Calculus](../courses/mathematics/002-18-02sc.md) — **Required**; MIT
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **Required**; MIT
- [Classical Mechanics](../courses/physics/010-8-01sc.md) — **Required**; MIT
- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **Required**; MIT
- [Introduction to CS and Programming Using Python](../courses/programming-tools/015-6-100l.md) — **Required**; MIT
- [Practical Programming in C](../courses/programming-tools/016-6-087.md) — **Required**; MIT

**Move on when:** Any error in calculus, linear algebra, mechanics, or electromagnetism that would obstruct later work must be studied and retested with changed parameters. Then complete acquisition or public-data import, unit checks, and fitting for one mechanics or electromagnetics case. A second machine must reproduce every plot from the README alone, and simulation or replay must never be described as measurement.

### Circuits and dynamic systems

**Why these courses:** Make 18.03SC, 6.002, and 6.003 explain the same second-order network: begin with its differential equation, connect it to circuit parameters, and use system representations to relate step and frequency response. Reuse the modeling, unit checks, and fitting code from the first part. Add 6.071J only when instrumentation, error analysis, or measurement chains remain weak; it does not replace the three foundations.

- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **Required**; MIT
- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **Required**; MIT
- [Introduction to Electronics, Signals, and Measurement](../courses/electronics-laboratory/024-6-071j.md) — **Use if needed**; MIT
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **Required**; MIT

**Move on when:** Derive state-space and frequency-domain models for a second-order circuit, then measure or simulate its step and swept-frequency responses. Before tuning, state allowed errors for the dominant pole, DC gain, and bandwidth from component tolerance, instrument uncertainty, or numerical accuracy, and verify them on data not used for fitting.

### Probability, digital systems, and fields

**Why these courses:** Random inputs come from 6.041SC, the digital implementation from 6.004, interconnect fields from ECE 3030, and transistor limits from ECE 3150; prior FPGA work does not replace probability or electromagnetics. Turn the previous second-order system's stimulus and reference response into randomized digital tests, then carry the same interface into the field and device models.

- [Probabilistic Systems Analysis and Applied Probability](../courses/probability-statistics/007-6-041sc.md) — **Required**; MIT
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **Required**; MIT
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **Required**; Cornell University
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **Required**; Cornell University

**Move on when:** Directed tests for the digital module must cover every state transition, interface boundary, and invalid input. Preserve random seeds and coverage progression, with zero mismatches against the reference model. Refine the interconnect mesh until propagation quantities converge, and keep port-power imbalance within the solver's stated numerical error.

### Laboratory, PCB, and system integration

**Why these courses:** Put the analog network, digital module, and randomized regression on one board. Use 6.101 for analog debugging, the MIT PCB workshop for fabrication preparation, and ECE 4760/5730 for system integration. Before starting, confirm substitute parts for dated components, an isolated current-limited supply, an oscilloscope or DMM, the target MCU, and a fabrication budget. Missing access means stopping at pre-board; prior experience still does not remove calibration, rework, or requirements-to-test mapping.

- [Introductory Analog Electronics Laboratory](../courses/analog-electronics/026-6-101.md) — **Required**; MIT
- [The Art and Science of PCB Design](../courses/pcb-eda/055-iap-pcb-2026.md) — **Required**; MIT
- [Digital Systems Design Using Microcontrollers](../courses/capstone-practice/057-ece-4760-ece-5730.md) — **Required**; Cornell University

**Move on when:** Fabricate and commission a PCB with an analog front end and digital control under isolated, current-limited, low-voltage conditions. Test the endpoints, nominal point, critical corners, and protection boundaries of its operating range. Keep rating checks, stop conditions, raw calibration data, rework history, and photographs, and map every requirement to a test. Connect neither mains, people, nor unknown supplies.

### An integrated design across two areas

**Why these courses:** RES.6-008 supplies the shared signal-processing foundation. The communications option uses 6.02, which does not assume the 6.011 sequence, rather than jumping directly into graduate digital communications. Choose two areas—communications, linear dynamics, power electronics, semiconductor devices, or photonics—that genuinely meet inside one system. Define each subsystem's performance and interface requirements before choosing chapters, and use the board tests or pre-board interface from the preceding work as their common input rather than starting two prestige-driven projects.

- [Digital Signal Processing](../courses/dsp/088-res-6-008.md) — **Required**; MIT
- [Introduction to EECS II: Digital Communication Systems](../courses/communications/099-6-02.md) — **Choose 2**; MIT
- [Introduction to Linear Dynamical Systems (2008 Archive)](../courses/control-systems/068-ee-263.md) — **Choose 2**; Stanford University
- [Power Electronics](../courses/power-electronics/114-6-622.md) — **Choose 2**; MIT
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **Choose 2**; Cornell University
- [Introduction to Photonics](../courses/optics-photonics/132-108106135.md) — **Choose 2**; IIT Madras / NPTEL

**Move on when:** The final design must connect signal processing and both chosen areas into one system, with performance and interface metrics derived from system requirements and checked by simulation or public data by default. High voltage or current, RF, lasers, chemicals, and fabrication equipment require a compliant facility and qualified supervision. State which conclusions come from simulation, public data, or measurement, and retain one failure that genuinely changed the design.
