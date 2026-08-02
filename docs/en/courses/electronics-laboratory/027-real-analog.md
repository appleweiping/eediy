---
title: "Real Analog Courses"
description: "Digilent's Real Analog Courses builds a practical analog-circuit sequence from notes, exercises, and instrument-based labs, with strong reproducibility constrained by required Analog Discovery hardware."
page_type: course
course_id: "course-027"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-29"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: ea7c865d24be1d3a -->

# Digilent: Real Analog Courses

## Course Overview

- **University:** Digilent
- **Course code:** Real Analog
- **Official prerequisites:** No provider-published hard prerequisite verified; recheck the course page
- **EEDIY preparation:** Circuit Analysis
- **Access:** Open without registration
- **Material status:** 2026-07-29; public-material guide

### Real Analog turns calculation into measurement

Digilent's [Real Analog](https://digilent.com/shop/coursework-learning-resources/) places 12 chapters of Circuits 1 theory and Analog Discovery experiments on one path. Chapters 1–5 move from voltage, current, power, and KCL/KVL to network theorems and op-amps. Chapters 6–9 add storage, first- and second-order systems, and state variables. Chapters 10–12 cover sinusoidal steady state, frequency response, filtering, and power. It suits learners with basic algebra who cannot yet explain instrument loading, grounding, or measurement discrepancy. The material was written mainly for AD2. Digilent says its concepts are compatible with AD3, not that every old button, range, and wiring diagram has been updated.

### Chapter 1 Teaches Measurement; Chapter 9 Teaches State Models

[Chapter 1](https://digilent.com/reference/_media/learn/courses/real-analog-chapter-1/real-analog-chapter-1.pdf) combines exposition, exercises, worksheets, and 9 experiments. Beginning with breadboards, sources and meters, and V–I regression, place prediction and measurement side by side with the AD model, WaveForms version, reference ground, ranges, raw data, and residuals. Its table of contents names Exercise and Homework Solutions, but the current PDF contains no solution section. A broken contents entry is not an answer chain.

[Chapter 9](https://digilent.com/reference/_media/learn/courses/real-analog-chapter-9/real-analog-chapter-9.pdf) uses A, b, c, and d matrices and two experiments to express an RLC in state form. Compare the hand-derived model, initial conditions, simulated and measured curves, overlay residual, and state trajectory in one view. A wrong initial point points first to state definitions and probe reference; an incorrect envelope points to coil resistance and tolerance. Calling every discrepancy “noise” discards the diagnostic lesson.

### Instrument versions determine whether automation is interpretable

[WaveForms](https://digilent.com/shop/waveforms/) is free to use and has a hardware-free demo mode. Demo mode teaches the interface but does not generate circuit data. Marius Greuel's [DwfPy](https://github.com/mariusgreuel/dwfpy) is a useful unofficial companion: an MIT-licensed, documented, CI-tested Python binding for WaveForms devices, with oscilloscope, generator, logic, supply, and acquisition examples. It is not a Digilent course requirement. Use it to automate repeated sweeps and export raw arrays beside their parameter settings, never to skip manual verification of probes, ranges, and ground.

Begin automation with a known resistor and an internal loopback. Have the script emit device enumeration, channel configuration, sample rate, trigger conditions, and raw arrays, then compare them with a one-shot GUI reading. Each sweep point also needs its settle time and clipping decision. A final Bode plot alone cannot separate an instrument setting, a script-unit error, and a circuit discrepancy.

The AD2 ground shares the USB host reference and must not be assumed galvanically isolated. Restrict physical reconstruction to low-voltage, current-limited circuits disconnected from mains and other hazardous sources. Power down before rewiring and discharge capacitors. Without a trustworthy DMM, current-limited source, and known ground path, stop at analysis and SPICE rather than labeling a demo-mode screen as measurement.

### Three Experiments Expose Model Failure

Select one static, one dynamic, and one frequency-domain experiment. Use V–I fitting to expose input loading and residuals; use the Chapter 9 RLC to expose state and initial conditions; then place hand-derived Bode values, point measurements, and a Network Analyzer sweep for one filter on the same axes. Put the schematic, bill of materials, software version, wiring, raw data, and script together, then use one failed waveform to show what the correction actually changed.

Real Analog is more portable than the old NI bench, but simulation still does not replace measurement. The lasting skill is explaining how an instrument changes a circuit, how residual structure separates a model error from a wiring error, and why a curve without range and version metadata cannot support that diagnosis.

## Course Resources

- [Course home](https://digilent.com/shop/coursework-learning-resources)

## Resource Summary

Every public entry point verified in this review is listed above. Use the feedback and corrections links below to submit a completion record, another resource, or a broken-link report.
