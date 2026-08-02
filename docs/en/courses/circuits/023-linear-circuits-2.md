---
title: "Linear Circuits 2: AC Analysis"
description: "Georgia Institute of Technology's Linear Circuits 2: AC Analysis follows DC analysis with AC circuit methods, combining videos, 45 assignments, and experiment demonstrations without a complete build loop."
page_type: course
course_id: "course-023"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 60ab7279e7a66f2c -->

# Georgia Institute of Technology: Linear Circuits 2: AC Analysis

## Course Overview

- **University:** Georgia Institute of Technology
- **Course code:** Linear Circuits 2
- **Official prerequisites:** No provider-published hard prerequisite verified; recheck the course page
- **EEDIY preparation:** Engineering Mathematics; Physics Foundations; DC circuit analysis or equivalent background; Course 1 is useful context but not an irreplaceable hard prerequisite
- **Access:** Registration required; scope varies by platform
- **Material status:** 2026-07-30; public-material guide

### This Course Starts with Phasors

Georgia Tech's official [Linear Circuits 2 course and assignments](https://www.coursera.org/learn/linear-circuits-ac-analysis)
has 5 modules centered on sinusoids and phasors, frequency response, filters,
complex power, and transformers. It does not rebuild KVL/KCL, node and mesh
methods, Thévenin/Norton equivalents, or first-order transients; the preceding
[Linear Circuits 1](https://www.coursera.org/learn/linear-circuits-dcanalysis)
covers those. Choose it only after that DC foundation. Test readiness with a series RLC circuit: move from time-domain
relations to impedances, solve the current phasor, translate it back into
amplitude and phase, and explain which element dominates as frequency changes.
If the complex arithmetic works but lead and lag do not make sense, review
complex geometry and stored-energy elements first.
Graded exercises on the official Coursera page depend on current login and
access permissions.

### Return Every Calculation to a Waveform

After deriving a phasor from \(v(t)\), translate it back to time. After drawing
Bode asymptotes from a transfer function, calculate several exact frequencies.
For AC power, state whether phasors are peak or RMS and keep W, var, and VA
distinct; maximum power transfer is not maximum efficiency. For a transformer,
set dot convention and reference directions before reflecting an impedance.

A filter design needs more than one cutoff. State passband, stopband,
source/load impedances, available component series, and tolerance. Then ask how
op-amp gain-bandwidth, slew rate, output swing, and probe loading move the
intended poles and zeros.

Before plotting, predict the low-frequency, high-frequency, and near-resonance
directions. If the exact curve violates those limits, inspect the phasor
convention, transfer-function normalization, and measurement loading before
changing axes to hide the discrepancy.

### Use a Sensor Filter to Check Phasors, Response, and Waveforms

The course demonstrates guitar filtering, RLC behavior, and sensors, but the
campus [ECE 3710 description](https://pe.gatech.edu/sites/default/files/agendas/ECE-3710-Circuits%20and%20Electronics.pdf)
and its myDAQ labs are not an open MOOC laboratory package. For independent
work, design a filter for a narrowband sensor: derive specifications from its
spectrum, obtain the transfer function, run a SPICE magnitude/phase sweep,
and measure several frequencies at low voltage. Without hardware, perform a
tolerance sweep and label it simulation. When you can predict scale, phase
direction, and frequency limits before using complex arithmetic, phasors have
become an engineering tool.

## Course Resources

- [Course home](https://www.coursera.org/learn/linear-circuits-ac-analysis)

## Resource Summary

Every public entry point verified in this review is listed above. Use the feedback and corrections links below to submit a completion record, another resource, or a broken-link report.
