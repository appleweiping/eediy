---
title: Practice Guides
description: Turn electrical-engineering course knowledge into executable, verifiable, and reproducible capability.
---

<div class="ee-language" markdown>
[简体中文](../../guides/index.md)
</div>

# Practice Guides

These guides answer what to do after learning the theory. Every page includes a minimal environment, learning sequence, verification task, diagnosis, evidence, cost and licensing, accessibility, and safety stop boundaries. Choose the page that serves the current project; do not install every tool at once.

## How to use the guides

1. Read [Laboratory Safety](safety.md) and classify the work as software-only, bounded low energy, or supervised-only.
2. Use [Tools and Environments](tools.md) to select a minimal toolchain without letting tool count replace the objective.
3. Choose one topic below and write predictions, acceptance criteria, and stop conditions first.
4. Complete its verification task and retain evidence another person can review.
5. Combine micro-tasks into a portfolio project through [Project Practice](projects.md).
6. Rebuild from a clean environment with [Reproducible Engineering](reproducibility.md); a failed rebuild is not complete.

## Engineering foundations

- [Version Control and Engineering Collaboration](version-control.md): atomic commits, branch experiments, tags, and sensitive-data boundaries.
- [Python, Jupyter, and Engineering Computation](python-jupyter.md): units, data, tests, and stateless reruns.
- [C, Build Systems, and Hardware-Adjacent Programming](c-cmake.md): representation, memory, layering, and host tests.
- [Numerical Computing and Model Verification](numerical-computing.md): scaling, convergence, sensitivity, and independent benchmarks.
- [Reproducible Engineering and Automated Verification](reproducibility.md): pinned environments, one entry point, and evidence manifests.

## Circuits, hardware, and digital systems

- [SPICE Circuit Simulation](spice-simulation.md): operating point, AC/transient, models, and tolerance analysis.
- [PCB and KiCad Workflow](pcb-kicad.md): requirements, footprints, rules, fabrication output, and controlled power-up.
- [HDL, Simulation, and FPGA](hdl-fpga.md): self-checking tests, synthesis, constraints, and timing evidence.
- [Embedded Toolchains and Board-Level Debugging](embedded-toolchains.md): recoverable flashing, peripheral layers, and fault paths.
- [Instrumentation, Measurement, and Uncertainty](instrumentation-measurement.md): range, bandwidth, probes, calibration, and uncertainty.

## Research, records, and communication

- [Data and Laboratory Records](data-lab-notebooks.md): run identity, immutable raw data, metadata, and processing traceability.
- [Literature Search and Evidence Evaluation](literature-research.md): question decomposition, source tiers, counterevidence, and evidence matrices.
- [Technical Writing and Design Review](technical-writing.md): requirements, conclusions, figures, decisions, and peer reproduction.

## Cross-cutting guides

- [Tools and Environments](tools.md): software, instruments, files, units, and low-bandwidth alternatives.
- [Laboratory Safety](safety.md): risk levels, stop conditions, supervision boundaries, and incident response.
- [Project Practice](projects.md): objectives, scope, milestones, acceptance, and portfolio evidence.

## Three suggested practice chains

### Software and signal analysis

[Python/Jupyter](python-jupyter.md) → [Numerical Verification](numerical-computing.md) → [Data Records](data-lab-notebooks.md) → [Technical Writing](technical-writing.md) → [Reproducible Engineering](reproducibility.md)

This chain fits signal processing, control, communications, and public-data projects. Final evidence should include raw data, tested scripts, unit-labeled figures, and a clean rebuild log.

### Circuits and PCB

[SPICE](spice-simulation.md) → [PCB](pcb-kicad.md) → [Instrumentation](instrumentation-measurement.md) → [Data Records](data-lab-notebooks.md) → [Project Practice](projects.md)

Keep beginner work software-only or bounded low energy. Higher energy, stored energy, lasers, RF power, or body connection must move to a qualified facility with supervision.

### Digital hardware and embedded systems

[C and Builds](c-cmake.md) → [HDL/FPGA](hdl-fpga.md) or [Embedded Toolchains](embedded-toolchains.md) → [Version Control](version-control.md) → [Reproducible Engineering](reproducibility.md)

Treat host tests, automated simulation, recoverable flashing, board logs, and timing reports as one evidence chain rather than showing only a final demonstration video.

## Definition of done

Completing a guide means submitting a reviewable result, not merely reading the page. At minimum retain a prior prediction, explicit acceptance, fault injection or boundary test, raw inputs, automation, interpretation, safety review, and an evidence bundle another learner can replay.
