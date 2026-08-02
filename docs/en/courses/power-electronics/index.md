---
title: "Power Electronics"
description: "Converter topologies, magnetics, modulation, and feedback; high-voltage or high-power work defaults to simulation or supervision."
page_type: track
track_id: "track-power-electronics"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 12b0e0c2bfdcfca9 -->

# Power Electronics

## Track position

Converter topologies, magnetics, modulation, and feedback; high-voltage or high-power work defaults to simulation or supervision.

## Recommended prerequisite tracks

- [Circuit Analysis](../circuits/index.md)
- [Control Systems](../control-systems/index.md)
- [Electronics Laboratory and Measurement](../electronics-laboratory/index.md)

## 6.622 is one complete design narrative; Coursera is a three-stage sequence

The [official OCW page](https://ocw.mit.edu/courses/6-622-power-electronics-spring-2023/) for [MIT 6.622](114-6-622.md) joins switching conversion, magnetics, semiconductor loss, modeling, and feedback control. Public video, handwritten notes, problems, examinations, and a design project support a complete pass. Coursera divides the dependency chain. The [official page](https://www.coursera.org/learn/power-electronics) for [Introduction to Power Electronics](115-power-electronics-1.md) establishes switching states and steady-state quantities through simulation. [Converter Circuits](116-power-electronics-2.md) adds isolated and non-isolated topologies, and [Converter Control](117-power-electronics-3.md) reaches small-signal models and loop design. Their order is substantive.

These are alternative routes, not four mandatory courses. Choose 6.622 for demanding paper work and one continuous design story, or the Coursera sequence for shorter modules and frequent simulation feedback. After 6.622, one LTspice or control exercise may calibrate tool use. Completing only the first Coursera course should be described as steady-state conversion; it does not yet cover magnetics, device stress, or closed-loop boundaries. Keep each week’s topology, magnetics, loss, and control work tied to one converter specification so the units converge on a design.

## One buck converter answers different questions in three models

Draw current paths for both ideal buck states and use inductor volt-second and capacitor charge balance from [circuit analysis](../circuits/index.md) to derive conversion, ripple, and the CCM/DCM boundary. Analytic expressions answer steady-state ratio, stress, and order of magnitude. An averaged model around an operating point supplies control-to-output poles and zeros for crossover and phase-margin work in [control systems](../control-systems/index.md). A switched model reveals ripple, dead time, parasitics, and startup. Their trends agree in overlapping regions, although their pointwise waveforms need not.

State device models, temperature, step size, startup conditions, steady-state window, and disturbance time, comparing nominal and at least two corners. Calculate inductor slope, output ripple, and duty on paper before simulation so disagreement can be assigned to signs, parameters, or solver settings. Inspect separate windows at switching-period, control-bandwidth, and line/load-transient scales so ripple is not mistaken for control oscillation or startup for steady state. If a step produces duty limiting, magnetic saturation, or oscillation, explain it along both energy and control paths.

## Bench traces add evidence only on an isolated low-voltage platform

Current limiting, isolation, differential measurement, and emergency disconnect from [electronics laboratory](../electronics-laboratory/index.md) belong in the schematic. Physical extension remains isolated, current-bounded, and low voltage. Do not connect mains, improvise unknown high-energy transformer tests, or place an ordinary grounded probe across a high-side switch. Check semiconductor voltage, current, safe operating area (SOA), and junction temperature; magnetic saturation and temperature rise; PCB spacing; and energy after shutdown. Public 6.622 design material does not provide an outside high-power facility, and Coursera grading or feedback may require paid access.

When the required bench is unavailable, finish at simulation level and name untested thermal, EMI, and physical-parasitic behavior. A low-voltage build states current limit, isolation, probe connection, startup current, and stop condition. State the measurement bandwidth, probe error, and steady-state interval used for input and output power; one attractive switching trace does not establish safety or efficiency.

## Let line and load steps decide between two topologies

Define input range, output and load, ripple, efficiency, transient response, switching frequency, size proxy, and allowable temperature rise. Compare at least two candidates among buck, boost, flyback, or another bounded topology through switching states, CCM/DCM range, device stress, magnetic values, and loss models, then explain the selection. The controller analysis includes crossover, phase margin, actuator saturation, and line or load transients. Across three operating corners, identify the first named constraint to be violated.

The project contains analytic derivations, averaged and switched sources, model versions, corner sweeps, and raw traces. A run outside specification should trace to inductor saturation, duty limit, loop dynamics, or a thermal assumption and cause a concrete revision. Compare both topologies under the same input range, load step, device temperature, and loss definitions. The conclusion states which corner reaches which constraint first, which model gave advance evidence, and which questions still require hardware.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Power Electronics](114-6-622.md) | MIT | Main course | Public-material guide | Public assignments or labs |
| [Introduction to Power Electronics](115-power-electronics-1.md) | University of Colorado Boulder | Alternative | Public-material guide | Partial or restricted |
| [Converter Circuits](116-power-electronics-2.md) | University of Colorado Boulder | Alternative | Public-material guide | Partial or restricted |
| [Converter Control](117-power-electronics-3.md) | University of Colorado Boulder | Alternative | Public-material guide | Partial or restricted |
