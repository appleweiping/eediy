---
title: "Electromagnetics, RF, Microwave, and Wireless"
description: "Complete an RF or wireless design that connects S-parameters, matching, gain and noise, and an antenna or channel model in one link budget, with rules checked for the target region."
page_type: route
route_id: "route-rf-wireless"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 167d91f19e232f3d -->

# Electromagnetics, RF, Microwave, and Wireless

## Audience

Learners moving from boundary conditions and transmission lines to matching networks, antennas, receivers, and a complete wireless link

## What you should be able to do

Complete an RF or wireless design that connects S-parameters, matching, gain and noise, and an antenna or channel model in one link budget, with rules checked for the target region.

## Calibrate the electromagnetic model first

Start on paper with one lossy transmission line: compute reflection coefficient, VSWR, and input impedance from the load and characteristic impedance, then check passivity. If port power and field boundaries do not connect, repair ECE 3030/6.013 material before drawing an antenna.

## One frequency plan, one RF chain

- Keep the field model, S-parameters, matching network, gain/noise budget, and channel on the same band, reference impedance, and power units, defining ports before simulation.
- Choose one executable RF-circuit/antenna material path. Prefer 6.661 for anonymous study; institutional or platform branches require opening the actual assignments, tools, and lab descriptions first.
- Insert the preceding device or antenna model into the detector and BER baseline, and record the target region, band, and date of the regulatory check.
- Skip a complete ECE 4880 reproduction when the missing first five lectures, paid text, Simulink, or lab conditions are unavailable. Skip the TU/e path until enrolled access to assignments and labs is verified.
- Default home study skips radiated testing and transmission. Simulation or a course page grants no spectrum, laboratory, or regulatory permission.

## Give the simulation route a real finish line

- S-parameters pass applicable passivity and reciprocity checks, matching and noise budgets rebuild from fixed inputs, and mesh or frequency-step convergence is recorded.
- The link exit requires no transmission: the antenna or channel model enters the BER or capacity result, with assumptions, regulatory bounds, and unmeasured quantities visible.

## How to proceed

### Single-variable calculus preparation

**Why these courses:** 18.02SC formally builds on 18.01, so begin with 18.01SC checks on differentiation, integration, series, and parametric curves. Equivalent preparation can be demonstrated with closed-book problems instead of repeating every lecture; failed topics are repaired before continuing.

- [Single Variable Calculus](../courses/mathematics/001-18-01sc.md) — **Required**; MIT

**Move on when:** Solve a fresh calculus set independently and integrate one dimensional field quantity into total charge, energy, or power. Analytical and numerical results must agree under a documented step-size convergence study.

### From boundary conditions to ports

**Why these courses:** Secure vector calculus, waves, and boundary conditions with 18.02SC, 18.03SC, and 8.02X before ECE 3030 turns them into engineering field problems. Add the relevant 6.013 material when transmission lines, waveguides, and energy flow still do not connect; skip it when equivalent derivations and problem practice are already secure.

- [Multivariable Calculus](../courses/mathematics/002-18-02sc.md) — **Required**; MIT
- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **Required**; MIT
- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **Required**; MIT
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **Required**; Cornell University
- [Electromagnetics and Applications](../courses/electromagnetics/108-6-013.md) — **Use if needed**; MIT

**Move on when:** Build analytical and numerical models of a transmission line or waveguide and refine the mesh until changes in propagation constant and port-power balance fall below a stated discretization error. Explain that error from solver order, the convergence trend, and the project specification, and retain the complete convergence table.

### RF circuits and antennas

**Why these courses:** There is no default course that works for everyone here. For anonymously accessible study, take MIT 6.661 and use its open draft plus 13 solved problem sets for receiver, antenna, and matching analysis. Choose Cornell ECE 4880 when system assignments and laboratory descriptions matter, but first account for the missing first 5 lectures, paid text, Simulink, and laboratory access. Choose the TU/e circuit path only after enrolling through Coursera and confirming access to its 19 assignments and 5 laboratories; the public overview alone is not a teachable course. Complete one path, using the NPTEL antenna course only for extra explanation. Physical measurements belong in a compliant RF laboratory under qualified supervision, and neither a course page nor simulation authorizes radiated testing.

**Complete path — Open theory path (MIT 6.661) (take these in the listed order)**

1. [Receivers, Antennas, and Signals](../courses/rf-microwave-antennas/113-6-661.md) — **Course in this path**; MIT

**Complete path — RF systems and laboratory path (Cornell ECE 4880) (take these in the listed order)**

1. [Radio Frequency Systems](../courses/rf-microwave-antennas/110-ece-4880.md) — **Course in this path**; Cornell University

**Complete path — Coursera circuit path (TU/e; enrollment required) (take these in the listed order)**

1. [RF and Millimeter-Wave Circuit Design](../courses/rf-microwave-antennas/111-rf-and-millimeter-wave-circuit-design.md) — **Course in this path**; Eindhoven University of Technology

- [Analysis and Design Principles of Microwave Antennas](../courses/rf-microwave-antennas/112-108105114.md) — **Use if needed**; IIT Kharagpur / NPTEL

**Move on when:** Complete one matching network, RF front end, or antenna design. Derive the S11 target from the link budget, allowed mismatch loss, and bandwidth; −10 dB is only a starting point when its mismatch loss is genuinely acceptable, not a substitute for system reasoning. Close the gain, noise, and stability budgets at the same time.

### Put the budget through a channel

**Why these courses:** Use 6.02 for the synchronization, coding, detection, and error-rate baseline; it does not silently assume the 6.011 sequence that this route has not guaranteed. Put the completed S-parameters, gain/noise budget, or antenna model directly at the link front end, then choose either EE 359 for wireless systems or the NPTEL lecture sequence according to access. The 6.450/6.452 graduate sequence requires separate 6.011 preparation and is not counted here.

- [Introduction to EECS II: Digital Communication Systems](../courses/communications/099-6-02.md) — **Required**; MIT
- [Wireless Communications](../courses/communications/105-ee-359.md) — **Choose 1**; Stanford University
- [Principles of Digital Communications](../courses/communications/106-108101113.md) — **Choose 1**; IIT Bombay / NPTEL

**Move on when:** Complete a reproducible link budget and a channel simulation with fading and interference, plotting receiver sensitivity against BER or throughput. Check frequency, bandwidth, transmit power, and duty cycle against current rules in the target region. Without a compliant test setting, remain in simulation and do not transmit.
