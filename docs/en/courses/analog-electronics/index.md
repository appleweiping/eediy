---
title: "Analog Electronics"
description: "Diodes, transistors, op-amps, feedback, filters, and analog system design with real nonidealities."
page_type: track
track_id: "track-analog-electronics"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: f37a443c955ce63f -->

# Analog Electronics

## Track position

Diodes, transistors, op-amps, feedback, filters, and analog system design with real nonidealities.

## Recommended prerequisite tracks

- [Circuit Analysis](../circuits/index.md)
- [Electronics Laboratory and Measurement](../electronics-laboratory/index.md)

## The six laboratories and seven-week project are the spine of 6.101

[MIT 6.101](026-6-101.md) treats analog electronics as a design course rather than a catalogue of devices. Its [official course page](https://ocw.mit.edu/courses/6-101-introductory-analog-electronics-laboratory-spring-2007) organizes six laboratories around diodes, transistors, op amps, feedback, frequency response, and instruments, then devotes seven weeks to one project. The prompts and much of the teaching material are public, but some readings are paid and the BOM, parts, and bench assumptions date to 2007. Choosing 6.101 means rebuilding its questions with justified modern substitutions, not shopping from the old part numbers.

For a learner with limited bench access, the [official NPTEL Analog Circuits page](https://nptel.ac.in/courses/108101094) gives [Analog Circuits](034-108101094.md) a continuous lecture-and-problem rhythm. [Integrated Circuits, MOSFETs, Op-Amps and Their Applications](035-108108111.md) moves from process and devices to op-amp applications. Either can supply a second explanation for a difficult 6.101 chapter, but neither reproduces the six-lab and seven-week-project feedback chain. One project spine plus one explanatory source is normally enough.

For an off-campus learner, confirm access to instruments, parts, and the original prompts before treating a course number as sequencing evidence.

## An operating-point check says more than a stack of Bode plots

Use the same common-source or common-emitter stage to connect [circuit analysis](../circuits/index.md) with [electronics laboratory](../electronics-laboratory/index.md). Determine the device region from bias, then derive \(g_m\), \(r_o\), midband gain, input and output resistance, headroom, and a dominant pole. Draw the supply, current limit, probe ground, and signal-source connection beside the schematic. After a SPICE sweep, measure the DC point, linear swing, and frequency response, separating model error, part spread, and probe loading in the discrepancy.

If ideal-op-amp rules are the only available model, investigate finite gain-bandwidth product (GBW), slew rate, offset, output range, and capacitive load in a few small experiments. The important question is whether device region, output current, swing, or a pole can be identified as the first limitation before power-up or simulation. Physical work stays isolated, low voltage, and current limited; when instruments are unavailable, describe the result as simulation-only.

## The public 6.301 material is 25 recitation sets, not a seamless next course

After a single-stage amplifier in 6.101 is routine, select multistage and feedback work from [MIT 6.301](032-6-301.md). Its syllabus requires 6.012 and assumes 6.003 material including Bode plots, Laplace transforms, transfer functions, and complex impedance. The surviving public recitations are numbered 1–26 with 17 missing; the archive also has 9 unsolved assignments, Lab 1, Lab 2, a Design Problem, and historical exams, but no continuous primary-note or video sequence. It is therefore a strong advanced topic library rather than an automatic second spine. Consult [6.331](033-6-331.md) for a named advanced circuit question; a higher course number alone is not a reason to take the whole archive.

A 6.301 feedback or compensation problem can be attached to the same circuit used for the 6.101 project. The operating point, load, and frequency specification then receive paper, simulation, and bench scrutiny without repeating another device survey. A modern part substitution needs a comparison of pinout, supply, dissipation, bandwidth, stable load, and model provenance. State simulator version, temperature, and model corner instead of calling two parts equivalent because their descriptions sound similar.

## One low-frequency front end is enough to expose the boundary

A low-frequency sensor front end or two-stage amplifier makes a credible closing design. State source impedance, signal range, supply, load, gain, bandwidth, noise, offset, swing, and power. Compare two topologies through the same bias and error budgets, followed by operating-point, AC, transient, load, and temperature studies. Add raw measurements only with a safe bench; otherwise stop at schematic simulation.

Close the design by moving exactly one load, supply, or temperature condition beyond the specification and identify the first violated constraint. If the explanation still reduces to a bias error, feedback sign, or probe connection, repair the same front end before changing subjects. If the remaining uncertainty is PVT, mismatch, parasitics, area, or on-chip power, carry the specification table and schematic into [analog integrated circuits](../analog-ic/index.md). With no authorized PDK, that handoff remains schematic or pre-layout and says nothing about fabricated-silicon performance.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Introductory Analog Electronics Laboratory](026-6-101.md) | MIT | Main course | Public-material guide | Public assignments or labs |
| [Analog Circuits](034-108101094.md) | IIT Bombay / NPTEL | Alternative | Public-material guide | Partial or restricted |
| [Integrated Circuits, MOSFETs, OP-Amps and Their Applications](035-108108111.md) | Indian Institute of Science / NPTEL | Alternative | Public-material guide | Partial or restricted |
| [Solid-State Circuits](032-6-301.md) | MIT | Supplement | Public-material guide | Public assignments or labs |
| [Advanced Circuit Techniques](033-6-331.md) | MIT | Supplement | Public-material guide | Public assignments or labs |
