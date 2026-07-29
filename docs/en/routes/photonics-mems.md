---
title: "Optoelectronics, Photonics, and MEMS"
description: "Complete a photonic or MEMS design with mode/device simulation, process constraints, layout, and performance budget."
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 3209ba8462e4a8ed -->

# Optoelectronics, Photonics, and MEMS

## Audience

Learners moving from electromagnetics and quantum foundations to optoelectronic devices, integrated photonics, and MEMS

## Final outcome

Complete a photonic or MEMS design with mode/device simulation, process constraints, layout, and performance budget.

!!! warning "Mainline audit review in this route"
    - [Silicon Photonics Design, Fabrication and Data Analysis](../courses/optics-photonics/133-phot1x.md): The course is instructor-paced, and commercial-tool licenses, regional registration, tapeout dates, and payment terms can change; learners receive measurement data rather than a mailed chip, so every run needs manual recheck. Last audited: 2026-07-29.

## Stages

### Physics and fields

**Selection rule:** Complete all 4 required courses; use the other 1 option only to close a specific gap.

- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **Required**; MIT; Mainline; A
- [Physics III: Vibrations and Waves](../courses/physics/012-8-03sc.md) — **Required**; MIT; Mainline; S
- [Quantum Physics I](../courses/physics/013-8-04.md) — **Optional supplement**; MIT; Alternative; A
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **Required**; Cornell University; Mainline; S
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **Required**; Cornell University; Mainline; A

**Stage exit criterion:** Solve the modes of a waveguide or resonator and cross-check them with an independent numerical method; the first three eigenfrequencies must agree with an analytical or converged reference within 2%, and normalized field-energy error must stay below 1%.

### Devices and fabrication

**Selection rule:** Complete all 2 required courses and choose 1 of 2 elective options.

- [Micro/Nano Processing Technology](../courses/fabrication-mems/126-6-152j.md) — **Required**; MIT; Mainline; S
- [Design and Fabrication of Microelectromechanical Devices](../courses/fabrication-mems/129-6-777j.md) — **Elective option**; MIT; Mainline; A
- [Quantum Optics for Photonics](../courses/optics-photonics/130-ece-5310.md) — **Elective option**; Cornell University; Alternative; A
- [Semiconductor Optoelectronics](../courses/optics-photonics/131-ece-5330.md) — **Required**; Cornell University; Mainline; A

**Stage exit criterion:** Design an optoelectronic, waveguide, or MEMS device tied to a manufacturable process and sweep at least three critical dimensions; report sensitivity, tolerance window, and worst-corner performance, with layout passing the adopted rule checks.

### Photonic systems

**Selection rule:** Complete all 1 required course and choose 1 of 2 elective options. The other course is an optional supplement and does not count toward the elective requirement.

- [Introduction to Photonics](../courses/optics-photonics/132-108106135.md) — **Required**; IIT Madras / NPTEL; Mainline; A
- [Silicon Photonics Design, Fabrication and Data Analysis](../courses/optics-photonics/133-phot1x.md) — **Optional supplement**; University of British Columbia; Mainline; A; **Audit review**
- [Optics](../courses/optics-photonics/134-2-71.md) — **Elective option**; MIT; Mainline; S
- [Photonic Materials and Devices](../courses/optics-photonics/135-3-46.md) — **Elective option**; MIT; Supplement; B

**Stage exit criterion:** Complete an on-chip or free-space optical link budget and verify insertion loss, bandwidth, crosstalk, and energy per bit; run at least 200 Monte Carlo trials over dimensional and material variations and report specification yield.

## Execution rules

- Follow each stage's selection rule: complete every required course and the stated number of electives; when complete path options are provided, choose one and finish every course in its listed order; use optional supplements only to close a specific gap.
- Produce at least one reproducible artifact per stage and include failed attempts in the retrospective.
- Work involving mains voltage, high voltage, RF exposure, lasers, chemicals, or fabrication equipment requires local-law compliance and qualified supervision.
