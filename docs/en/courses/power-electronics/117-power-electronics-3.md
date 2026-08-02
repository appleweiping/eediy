---
title: "Converter Control"
description: "University of Colorado Boulder's Converter Control advances the power-electronics sequence into converter control through videos, practice, simulation, and code, requiring prior converter and feedback-control knowledge."
page_type: course
course_id: "course-117"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 9d1e1387de7d4ebd -->

# University of Colorado Boulder Power Electronics 3: Converter Control

## Course Overview

- **University:** University of Colorado Boulder
- **Course code:** Power Electronics 3
- **Official prerequisites:** CU Boulder Converter Control is the third course in the sequence; its official page names Introduction to Power Electronics and Converter Circuits as preceding courses
- **EEDIY preparation:** No additional EEDIY preparation requirement
- **Access:** Registration required; scope varies by platform
- **Material status:** 2026-07-30; public-material guide

### Course fit and prerequisites

The University of Colorado Boulder [Converter Control](https://www.coursera.org/learn/converter-control) course is the third step in its power-electronics sequence. Its official page lists 4 modules and 5 graded assignments, with a reference pace of 2 weeks at 10 hours per week, and names [Introduction to Power Electronics](https://www.coursera.org/learn/power-electronics) and [Converter Circuits](https://www.coursera.org/learn/converter-circuits) as preceding courses. Before starting, derive a CCM buck averaged model and linearize it about an operating point. If a transfer function must be copied from a table, review state space, the Laplace transform, and Bode plots first.

### From Power-Stage Modeling to Closed-Loop Verification

Chapter 7 on the official course page covers averaging, perturbation and linearization, the canonical model, the PWM switch, and state-space averaging. Keep the operating point, input and output definitions, and neglected terms beside every model. A transfer function named `Gvd` need not remain valid after the load or conduction mode changes.

Chapter 8 first develops Bode-plot construction, then converter transfer functions and graphical impedance construction. Sketch DC gain, pole and zero slope changes, and phase direction before using software to refine the corners. Distinguish control-to-output, line-to-output, and output impedance; command following alone is insufficient. Chapter 9 turns to stability, phase margin, closed-loop Q, regulator or op-amp compensation, and a point-of-load regulator. Specify crossover, steady-state error, and disturbance rejection before placing compensator poles and zeros. That order is more reliable than starting with a familiar Type-II or Type-III circuit.

### A Complete Case Study Beats Disconnected Bode Plots

Take a buck or boost already checked in the preceding course and preserve its full chain: operating point, averaged model, small-signal model, analytic poles and zeros, numerical Bode plot, compensation targets, loop gain, closed-loop response, and line and load steps. Compare at least 3 representations—the analytic transfer function, an averaged time-domain model, and a switched model—and check agreement below `fs/20`. Then vary input voltage and load while recording crossover, phase margin, duty limits, saturation, and recovery. Build a separate model if the converter enters DCM instead of extrapolating the CCM result.

This course is easily reduced to “tuning phase margin” while the underlying plant remains uncalibrated. Cross-check analytic DC gain against the steady-state time-domain disturbance response, and verify whether an ESR zero or right-half-plane zero moves with topology, load, and operating point. If the averaged model follows switching waveforms only over a limited band, put that validity boundary in the figure caption instead of hiding it in code.

The prompts, feedback, and retry rules for the 5 assignments depend on Coursera login access. The [Power Electronics specialization](https://www.coursera.org/specializations/power-electronics) confirms sequence but does not promise anonymous access to graded material. The continuous case study is learner-built and does not replace training in digital-control firmware, sampling delay, PWM quantization, current-mode control, EMI, layout, or physical loop measurement. The useful result is the ability to identify the operating point and approximations behind every Bode plot, not merely to produce a stable-looking curve.

## Course Resources

- [Course home](https://www.coursera.org/learn/converter-control)

## Resource Summary

Every public entry point verified in this review is listed above. Use the feedback and corrections links below to submit a completion record, another resource, or a broken-link report.
