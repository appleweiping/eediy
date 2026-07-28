---
title: "Power, Machines, Power Electronics, and Energy"
description: "Safely complete simulation, control, and design review for a converter, motor drive, photovoltaic, or storage system."
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: b95403269cacd799 -->

# Power, Machines, Power Electronics, and Energy

[中文](../../routes/power-energy.md) · [← Learning routes](index.md)

## Audience

Learners covering conversion, machines, grids, and energy storage systems

## Final outcome

Safely complete simulation, control, and design review for a converter, motor drive, photovoltaic, or storage system.

## Stages

### Circuits and electromagnetics

**Selection rule:** Complete all 2 required courses; use the other 1 option only to close a specific gap.

- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **Required**; MIT; Mainline; S
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **Required**; Cornell University; Mainline; S
- [Electromagnetics and Applications](../courses/electromagnetics/108-6-013.md) — **Optional supplement**; MIT; Mainline; S

**Stage exit criterion:** Build a coupled field-circuit model of an inductor, transformer, or machine magnetic circuit and reconcile flux, stored energy, and port power; steady-state key quantities must agree with hand calculations within 5%, and transient energy conservation must close.

### Conversion and control

**Selection rule:** Complete all 1 required course and complete the elective option. The other 2 courses are optional supplements and do not count toward the elective requirement.

- [Power Electronics](../courses/power-electronics/114-6-622.md) — **Required**; MIT; Mainline; S
- [Introduction to Power Electronics](../courses/power-electronics/115-power-electronics-1.md) — **Elective option**; University of Colorado Boulder; Alternative; A
- [Converter Circuits](../courses/power-electronics/116-power-electronics-2.md) — **Optional supplement**; University of Colorado Boulder; Alternative; A
- [Converter Control](../courses/power-electronics/117-power-electronics-3.md) — **Optional supplement**; University of Colorado Boulder; Alternative; A

**Stage exit criterion:** Implement one converter topology and its closed-loop control in simulation or on an energy-limited platform, verifying ripple, efficiency, stability margin, and device stress; preserve derating checks at every operating point and use isolation plus current limiting for hardware tests.

### Grid, machines, and energy

**Selection rule:** Complete all 2 required courses and choose 1 of 4 elective options.

- [Power System Analysis](../courses/power-systems-machines/118-117105140.md) — **Required**; IIT Kharagpur / NPTEL; Mainline; A
- [Seminar in Electric Power Systems](../courses/power-systems-machines/119-6-691.md) — **Elective option**; MIT; Alternative; A
- [Electric Machines](../courses/power-systems-machines/120-6-685.md) — **Required**; MIT; Mainline; S
- [Electrical Machines II](../courses/power-systems-machines/121-108105131.md) — **Elective option**; IIT Kharagpur / NPTEL; Alternative; A
- [Solar Energy Engineering: Photovoltaic Energy Conversion](../courses/energy-storage-pv/122-pv-energy-conversion.md) — **Elective option**; Delft University of Technology; Mainline; A
- [Electrochemical Energy Systems](../courses/energy-storage-pv/123-10-626.md) — **Elective option**; MIT; Alternative; A

**Stage exit criterion:** Construct one scenario combining a grid, machine, and selected energy technology with power-flow or energy-balance residual below 1%; then run an N-1, fault, or operating-point transition analysis and report constraint violations and recovery time.

## Execution rules

- Follow each stage's selection rule: complete every required course and the stated number of electives; when complete path options are provided, choose one and finish every course in its listed order; use optional supplements only to close a specific gap.
- Produce at least one reproducible artifact per stage and include failed attempts in the retrospective.
- Work involving mains voltage, high voltage, RF exposure, lasers, chemicals, or fabrication equipment requires local-law compliance and qualified supervision.
