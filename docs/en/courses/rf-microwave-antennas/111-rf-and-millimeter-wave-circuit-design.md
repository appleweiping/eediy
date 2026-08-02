---
title: "RF and Millimeter-Wave Circuit Design"
description: "Eindhoven University of Technology's RF and Millimeter-Wave Circuit Design uses Qucs-S and Octave inside Coursera for simulation-first RF study; the public page exposes no fixed course project bundle."
page_type: course
course_id: "course-111"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-29"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 6d2757f6d9b6834d -->

# Eindhoven University of Technology: RF and Millimeter-Wave Circuit Design

## Course Overview

- **University:** Eindhoven University of Technology
- **Course code:** RF and Millimeter-Wave Circuit Design
- **Official prerequisites:** No provider-published hard prerequisite verified; recheck the course page
- **EEDIY preparation:** Electromagnetic Fields and Waves; Circuit Analysis; Communication Systems
- **Access:** Registration required; scope varies by platform
- **Material status:** 2026-07-29; public-material guide

### Treat the course as 5 linked RF design passes

TU/e's [RF and millimeter-Wave Circuit Design](https://www.coursera.org/learn/rf-mmwave-circuit-design)
page listed on 2026-07-29 6 modules, 19 assignments, and 5 peer-assessed design
labs: system, LNA/PA, mixer, VCO, and synthesizer. The provider describes about
70% as simulation and 30% as requiring a laboratory/components. It fits
learners who know link budgets, S-parameters, noise cascades, and frequency
planning and want to trace block specifications into circuit tradeoffs.
Revisit microwave networks and RF systems first if low-frequency small-signal
gain remains the main tool.

### Each pass isolates a different RF failure

The system pass derives block specifications from range, bandwidth,
sensitivity, and selectivity. Amplifier work separates LNA
noise/matching/stability from PA compression/efficiency. Mixer work preserves
wanted, image, and spur frequencies. VCO work covers startup, tuning, phase
noise, and load pulling. Synthesizer work explains loop type/bandwidth,
reference/divider noise, and locking. For every block, compare its
specification, schematic or model, pass/fail plot, corner/sensitivity result,
and rejected candidate. Nominal gain cannot stand in for stability or the
system budget.

### Tool versions change the simulated answer

The course introduces Qucs-S and Octave without pinning a public release. The
[Qucs-S repository](https://github.com/ra3xdh/qucs_s) and
[installation guide](https://qucs-s-help.readthedocs.io/en/latest/installation/installing-qucs-s.html)
show that OS/backend combinations vary; the
[Octave download](https://octave.org/download.html) represents only a current
environment option. Write the OS, Qucs-S, backend, Octave, device model, and
hash beside each circuit model. When changing simulators, rerun the same
netlist and baseline, then explain parser, model, or convergence differences
before comparing outputs.

### Default to a Simulation-Only System Loop

The 70/30 description is not a home-RF safety conclusion. Without an approved
institutional laboratory, do not connect a PA, antenna, uncharacterized
VNA/source, or transmit into free space. TU/e's
[remote RF laboratory](https://research.tue.nl/en/publications/rf-circuits-laboratory-for-remote-learning-and-massive-open-onlin/)
is purpose-built controlled infrastructure, not permission for a home bench.

With platform access, the 19 assignments, 5 peer assessments, and peer
feedback form the original course route. Without access, locked prompts,
supporting files, and solutions are outside the available material, so build
an independent clean-room model instead. Make idealized LNA, mixer, VCO, and
divider/phase-detector blocks share one transceiver link budget. At each pass,
push system requirements into the current block and return any excess noise,
linearity, or locking demand to the budget.

Judge one transceiver at the end: do the same frequency plan, impedance, and
power assumptions survive all five blocks? If extra LNA gain costs still more
in mixer compression, VCO phase noise, or synthesizer lock time, withdraw that
local optimum. RF design is the work of making five individually attractive
curves describe the same machine.

## Course Resources

- [Course home](https://www.coursera.org/learn/rf-mmwave-circuit-design)

## Resource Summary

Every public entry point verified in this review is listed above. Use the feedback and corrections links below to submit a completion record, another resource, or a broken-link report.
