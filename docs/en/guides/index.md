---
title: Practice Guides
description: Start from the engineering problem in front of you and find a concrete path through simulation, measurement, toolchains, records, and reproduction.
page_type: guide
comments: true
---


# Practice Guides

Courses teach concepts. Projects often break at the seams between them: a build environment changes, a model disagrees with hardware, a probe changes the circuit, or the raw data can no longer be found. Choose the page that matches the problem in front of you.

## Start from the current problem

| Current problem | Open first | Evidence to keep |
| --- | --- | --- |
| The software, license, or replacement tool is unclear | [Tools and Environments](tools.md) | one real task, rejection criteria, and a small rerunnable test |
| A notebook runs only on one computer | [Python and Jupyter](python-jupyter.md) | a command-line entry point with units, dependencies, and a failing test |
| A C project fails after a machine or target change | [C and CMake](c-cmake.md) | host tests, a target build, and the actual compiler command |
| Code, reports, and data no longer identify the same revision | [Version Control](version-control.md) | a tagged baseline that rebuilds and an explained diff |
| A numerical result moves with step size, tolerance, or algorithm | [Numerical Computing](numerical-computing.md) | an analytic benchmark, refinement table, residual, and rebuild command |
| SPICE produced a trace, but the model is still uncertain | [SPICE Circuit Simulation](spice-simulation.md) | hand prediction, operating-point/AC/transient results, and model limits |
| Measurement disagrees with prediction | [Instrumentation and Measurement](instrumentation-measurement.md) | connections, probe settings, raw values, and uncertainty |
| Raw data, calibration, or processing steps cannot be traced | [Data and Laboratory Records](data-lab-notebooks.md) | an immutable raw layer, run identity, and processing chain |
| A clean machine cannot rebuild the result | [Reproducible Engineering](reproducibility.md) | an empty-directory command and explicit comparison rules |
| RTL succeeds only in one waveform or board demonstration | [HDL, Simulation, and FPGA](hdl-fpga.md) | self-checking tests, counterexamples, constraints, and timing/CDC conclusions |
| Firmware flashes, but startup or communication loss is opaque | [Embedded Toolchains](embedded-toolchains.md) | ELF/map evidence, logs, pin observations, and a recovery path |
| A circuit is moving into schematic, layout, or fabrication | [PCB and KiCad](pcb-kicad.md) | source project, rules, manufacturing package, and current-limited bring-up plan |
| The experiment may exceed the available facility | [Laboratory Safety](safety.md) | the hazard boundary, stop conditions, and qualified-facility requirement |
| A pile of sources has not produced an engineering decision | [Literature Research](literature-research.md) | a replayable query, evidence matrix, and unresolved test |
| A conclusion still depends on an oral explanation | [Technical Writing](technical-writing.md) | a short report tracing conditions, data, versions, and figures |
| Several tasks have become mutually dependent | [Project Practice](projects.md) | scope, non-goals, model, acceptance tests, and failed conditions |

A common laboratory chain is analytic prediction, simulation, measurement design, immutable raw data, and a rebuilt figure and conclusion. Software-only, FPGA, and literature projects take different paths; the current failure chooses the entry.

!!! danger "Choose the hardware boundary before the tool"
    Mains, high voltage, substantial stored energy, lasers, RF power, rotating machinery, vacuum, high temperature, and chemical processes require suitable facilities, equipment, and supervision. Without them, stop at analysis, simulation, public data, or a verified low-energy platform.

After a real task, use the feedback links below to submit an edition change, failure mode, or alternative route. Environment, input, and observed behavior help the next reader far more than “this tool did not work.”
