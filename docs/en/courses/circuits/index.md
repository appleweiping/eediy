---
title: "Circuit Analysis"
description: "DC, AC, dynamic circuits, network theorems, and frequency-domain methods shared by electronics, control, power, and instrumentation."
page_type: track
track_id: "track-circuits"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 3c8aad5d7d85f06f -->

# Circuit Analysis

## Track position

DC, AC, dynamic circuits, network theorems, and frequency-domain methods shared by electronics, control, power, and instrumentation.

## Recommended prerequisite tracks

- [Engineering Mathematics](../mathematics/index.md)
- [Physics Foundations](../physics/index.md)

## 6.002 is one demanding spine; Linear Circuits 1–2 is a two-part alternative

[MIT 6.002](021-6-002.md) places nodal analysis, dynamic networks, small-signal electronics, problems, laboratories, and exams in one course. Its [official 2007 archive](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007) is unusually complete, but laboratories and teaching pages from different offerings cannot become a fictitious single term. [Linear Circuits 1](022-linear-circuits-1.md) and [Linear Circuits 2](023-linear-circuits-2.md) divide DC and transients from AC. The [official first-course page](https://www.coursera.org/learn/linear-circuits-dcanalysis) is platform-hosted, so feedback, price, and open access may change; both parts together form the alternative spine.

The public prelabs and experiments in [Cornell ECE 2100](028-ece-2100.md) can add bench work to either route, but missing continuous notes, solutions, and same-term exams prevent it from carrying the theory alone. Choose 6.002 or the Georgia Tech pair, then attach one matching Cornell experiment. Taking all four mostly repeats node equations rather than improving judgment about probes, ground references, and component tolerance.

## Carry one network through paper, netlist, and measurement

This subject uses small linear systems, complex polar form, and first-order initial-value problems from [engineering mathematics](../mathematics/index.md), together with charge, energy, signed power, and the passive sign convention from [physics foundations](../physics/index.md). Choose a low-voltage network containing resistance, energy storage, and a controlled source or op amp. With consistent node names and reference directions, derive the DC operating point, transient endpoints and time constant, AC transfer function, and power balance.

Before running a netlist, state the expected sign and the \(t=0^+\), \(t\to\infty\), \(\omega\to0\), and \(\omega\to\infty\) limits. Use ngspice, LTspice, or Qucs-S next, followed by safe measurements of the DC point and frequency response when equipment exists. KCL or KVL residuals, parameter sweeps, and a probe-loading estimate distinguish equation signs, models, component spread, and instrument error. Unclosed algebra points back to mathematics; contradictory voltage, current, and power directions point back to physics. Software does not select nodes, initial conditions, or units.

When no oscilloscope or source is available, stop at simulation or prelab. Physical work uses isolated, current-limited, low-voltage power and states probes, ground reference, ranges, and tolerances. Similar-looking simulated and measured curves are comparable only under aligned stimulus, load, bandwidth, and uncertainty.

## Read both archive gaps and the next branch from that network

The 2007 6.002 teaching page and older laboratories do not map item for item, and Lecture 24 is incomplete. Linear Circuits demonstrations do not provide a portable BOM, complete instrument settings, or raw data. ECE 2100 omits residential guidance and the full feedback process. State the offering, simulator release, model source, and unexecuted bench portions instead of presenting several archives as one “complete” course.

Finish with an unseen timed synthesis problem, then rebuild its principal curves from a short explanation and a discrepancy table covering frequency, load, and uncertainty. Use the first phenomenon that the table cannot explain to choose the continuation: transistor operating point, feedback, or noise goes to [analog electronics](../analog-electronics/index.md); discrete time, spectra, or filtering goes to signals and systems; transmission-line, boundary-field, or radiation behavior goes to electromagnetics. Carry the solved network and its conservation, initial-condition, impedance, and frequency-response checks into that next subject rather than starting with a disconnected example.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Circuits and Electronics](021-6-002.md) | MIT | Main course | Learner-reviewed (another run of the same course) | Public assignments or labs |
| [Linear Circuits 1: DC Analysis](022-linear-circuits-1.md) | Georgia Institute of Technology | Alternative | Public-material guide | Partial or restricted |
| [Linear Circuits 2: AC Analysis](023-linear-circuits-2.md) | Georgia Institute of Technology | Alternative | Public-material guide | Partial or restricted |
| [Introduction to Circuits for Electrical and Computer Engineers](028-ece-2100.md) | Cornell University | Supplement | Public-material guide | Partial or restricted |
