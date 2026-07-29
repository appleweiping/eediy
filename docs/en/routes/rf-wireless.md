---
title: "Electromagnetics, RF, Microwave, and Wireless"
description: "Complete an RF design or simulation with matching, link budget, antenna/channel models, and regulatory checks."
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 3a3de7081796fc19 -->

# Electromagnetics, RF, Microwave, and Wireless

## Audience

Learners progressing from fields and waves to RF circuits, antennas, receivers, and wireless links

## Final outcome

Complete an RF design or simulation with matching, link budget, antenna/channel models, and regulatory checks.

!!! warning "Mainline audit review in this route"
    - [Analysis and Design Principles of Microwave Antennas](../courses/rf-microwave-antennas/112-108105114.md): The official identity is Analysis and Design Principles of Microwave Antennas, not a general microwave-engineering course, and there is no open lab or code. The resource manifest still marks the superseded www-host fetch for review and needs a fresh evidence crawl. Last audited: 2026-07-29.

## Stages

### Fields and transmission lines

**Selection rule:** Complete all 4 required courses; use the other 1 option only to close a specific gap.

- [Multivariable Calculus](../courses/mathematics/002-18-02sc.md) — **Required**; MIT; Mainline; S
- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **Required**; MIT; Mainline; S
- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **Required**; MIT; Mainline; A
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **Required**; Cornell University; Mainline; S
- [Electromagnetics and Applications](../courses/electromagnetics/108-6-013.md) — **Optional supplement**; MIT; Mainline; S

**Stage exit criterion:** Build analytical and numerical models of a transmission line or waveguide and complete a convergence study at three or more mesh resolutions; propagation-constant deviation must stay below 3% and port power-balance residual below 5%.

### RF circuits and antennas

**Selection rule:** Complete all 1 required course and choose 1 of 2 elective options. The other course is an optional supplement and does not count toward the elective requirement.

- [Radio Frequency Systems](../courses/rf-microwave-antennas/110-ece-4880.md) — **Elective option**; Cornell University; Alternative; A
- [RF and Millimeter-Wave Circuit Design](../courses/rf-microwave-antennas/111-rf-and-millimeter-wave-circuit-design.md) — **Required**; Eindhoven University of Technology; Mainline; A
- [Analysis and Design Principles of Microwave Antennas](../courses/rf-microwave-antennas/112-108105114.md) — **Optional supplement**; IIT Kharagpur / NPTEL; Mainline; A; **Audit review**
- [Receivers, Antennas, and Signals](../courses/rf-microwave-antennas/113-6-661.md) — **Elective option**; MIT; Supplement; B

**Stage exit criterion:** Complete a matching-network, RF-front-end, or antenna design that achieves S11 below -10 dB across the declared band, or a justified equivalent target, and submit gain, noise, and stability budgets.

### Wireless systems

**Selection rule:** Complete all 1 required course and choose 1 of 3 elective options.

- [Principles of Digital Communications I](../courses/communications/100-6-450.md) — **Required**; MIT; Mainline; S
- [Principles of Wireless Communications](../courses/communications/104-6-452.md) — **Elective option**; MIT; Supplement; B
- [Wireless Communications](../courses/communications/105-ee-359.md) — **Elective option**; Stanford University; Alternative; A
- [Principles of Digital Communications](../courses/communications/106-108101113.md) — **Elective option**; IIT Bombay / NPTEL; Alternative; A

**Stage exit criterion:** Produce a reproducible link budget and channel simulation with fading and interference, plotting receiver sensitivity against BER or throughput; check frequency, bandwidth, transmit power, and duty cycle against a regulatory checklist for the target region.

## Execution rules

- Follow each stage's selection rule: complete every required course and the stated number of electives; when complete path options are provided, choose one and finish every course in its listed order; use optional supplements only to close a specific gap.
- Produce at least one reproducible artifact per stage and include failed attempts in the retrospective.
- Work involving mains voltage, high voltage, RF exposure, lasers, chemicals, or fabrication equipment requires local-law compliance and qualified supervision.
