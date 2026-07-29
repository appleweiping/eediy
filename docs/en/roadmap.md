---
title: Global Roadmap
description: Organize EE learning around a shared core, direction sampling, and depth tracks instead of course accumulation.
---

<div class="ee-language" markdown>
[简体中文](../roadmap.md)
</div>

# Global Roadmap

This is a **dependency graph**, not a universal syllabus. Time ranges assume roughly ten hours per week. Use the exit checks to skip material you already command, and extend the calendar if you have less time. Maintain one mainline and at most one parallel prerequisite at any moment.

## Route overview

1. **Stage 0 · Engineering language (months 0–3)**
   Review algebra, trigonometry, complex numbers, single-variable calculus,
   units, and order-of-magnitude reasoning. Build basic mechanics and
   electromagnetism, Python or an equivalent computational tool, Git, and
   reproducible-note habits at the same time.
2. **Stage 1 · Shared core (months 3–12)**
   Study linear algebra, differential equations, probability, circuits,
   signals and systems, and digital logic. Begin using instruments, simulation,
   and programming, with low-energy experiments only.
3. **Stage 2 · Explore directions (months 12–18)**
   Use three small projects to compare continuous devices, digital/embedded
   systems, and signals, control, or fields. The point is not project size; it
   is learning which kinds of failure you are willing to investigate.
4. **Stage 3 · Depth track (months 18–30)**
   Choose one or two adjacent directions, complete advanced study and
   toolchain practice, and deliver at least one system project with a
   documented design review.
5. **Stage 4 · Integration and transfer (ongoing)**
   Put specifications, models, implementation, verification, cost, safety,
   and communication into one body of engineering evidence, then transfer the
   method to a new device, platform, or problem.

## Stage 0: engineering language (months 0–3)

### Content

- Mathematics: functions, equations, trigonometry, complex numbers, derivatives, integrals, and vector intuition.
- Physics: force, energy, fields, potential, current, and basic waves.
- Computing: scripts, arrays, plots, numerical error, and version control.
- Engineering habits: units, significant figures, order-of-magnitude estimates, sources, and assumptions.

### Exit check

Skip this stage if you can independently:

1. express a sinusoid with phasors or complex numbers and convert rectangular/polar forms;
2. explain steady state, a time constant, and an initial condition in a first-order dynamic equation;
3. write a script that loads data, plots with units, and identifies numerical error sources;
4. estimate the scale of a simple system and catch an obviously unreasonable answer.

## Stage 1: shared core (months 3–12) { #shared-core }

The shared core does not mean equal depth in every subject. It creates interoperable concepts and tools.

| Module | Essential command | Minimum practice |
| --- | --- | --- |
| Mathematics and probability | Linear systems, eigenvalues, convolution, random variables, estimation intuition | Use a numerical experiment to check an analytic result |
| Circuits and electronics | KCL/KVL, equivalents, frequency response, diode/transistor, op-amp | Simulate and measure a filter or amplifier |
| Signals and systems | LTI, Fourier/Laplace, sampling, noise | Extract a spectrum from real data and discuss aliasing |
| Digital logic | Combinational/sequential logic, state machines, clock and metastability awareness | Verify a state machine with a testbench |
| Programming and computation | C or another low-level language, Python, debugging, automation | Rebuild plots from code and pass minimal tests |
| Measurement and safety | Instrument input, grounding, uncertainty, ratings, de-energized checks | Write a prediction–measurement–difference report |

### Exit check

- Build a linear model from physical assumptions and identify when it fails.
- Put theory, simulation, and measurement on one plot with units.
- Read a basic schematic, data sheet, and timing diagram.
- Deliver a small tested, versioned, reproducible program or HDL module.
- Stop when an experimental risk is unclear instead of “trying the connection.”

## Stage 2: explore directions (months 12–18) { #direction-sampling }

Keep each trial project to four to six weeks. Compare working styles rather than chasing advanced difficulty:

1. **Continuous world:** sensor front end, audio filter, or bounded low-voltage supply analysis. Notice whether devices, noise, and instrument detail engage you.
2. **Discrete systems:** FPGA state machine, microcontroller data acquisition, or a simple real-time protocol. Notice whether timing, interfaces, and debugging engage you.
3. **Models and algorithms:** filtering, a communication link, closed-loop control, or an electromagnetic simulation. Notice whether mathematical models and system behavior engage you.

Use the same [project evidence package](guides/projects.md#project-evidence-package) for each, then compare:

- Which kind of failure do you investigate voluntarily?
- Which abstractions energize you, and which details create sustained friction?
- What hardware, mentors, laboratories, or datasets can you realistically access?
- What evidence does the target research area or role require—not which course names?

## Stage 3: direction depth (months 18–30)

### Circuits, devices, and integrated systems

`Microelectronic devices → analog/digital ICs → feedback and noise → layout/process constraints → chip- or board-level validation`

Strengthen semiconductor physics, nonlinear circuits, small-signal models, statistical variation, thermal behavior, and reliability. Evidence should include corner conditions, an error budget, and design tradeoffs—not only a nominal simulation screenshot.

### Digital systems, FPGA, and architecture

`Logic design → HDL and verification → computer organization → FPGA toolchain → interface/accelerator/processor`

Strengthen synchronous design, clock-domain crossing, memory hierarchy, protocols, verification coverage, and timing closure. Evidence should include a self-checking bench, resource/timing reports, and fault cases.

### Embedded, PCB, and real-time systems

`C and debugging → MCU peripherals → buses and drivers → RTOS/real-time analysis → PCB and system validation`

Strengthen data-sheet reading, interrupts and concurrency, power, EMC awareness, board integrity, and manufacturability. Preserve interface contracts, logic-analyzer traces, and hardware revisions.

### Signals, DSP, and communications

`Signals and systems → probability/random processes → DSP → detection/estimation → communication systems`

Strengthen sampling, spectral analysis, filters, noise models, link budgets, and statistical validation. Report datasets, baselines, confidence or error distributions—not only attractive waveforms.

### Control, robotics, and autonomous systems

`Dynamic modeling → linear control → state space → estimation → nonlinear/optimal/robotic systems`

Strengthen controllability/observability, stability, identification, and actuator/sensor limits. Validate in simulation and on bounded low-energy plants before considering large-motion or high-energy platforms.

### Electromagnetics, RF, and photonics

`Electromagnetic fields → transmission lines/waveguides → microwave networks or optics → antennas/photonic devices → measurement and calibration`

Strengthen multivariable calculus, boundary conditions, complex fields, scattering parameters, and numerical field methods. RF power, lasers, or high voltage require qualified facilities and supervision.

### Power, energy, and machines

`Circuits and electromagnetism → machines/transformers → power electronics → control and grids → protection/thermal/reliability`

Strengthen switched systems, magnetics, thermal design, insulation, fault energy, and protection. Start with simulation and isolated low-energy teaching hardware. Mains electricity is not an introductory material.

### Semiconductor manufacturing, microsystems, and instrumentation

`Materials/devices → process and statistics → sensing/microsystems → measurement chain → reliability and calibration`

Strengthen solid-state physics, chemistry/materials, clean processes, statistical process control, and metrology. Fabrication, vacuum, high temperature, chemicals, or radiation equipment require an authorized laboratory.

## Stage 4: integration project

An integration project should expose all of these interfaces:

- **Need:** user, context, measurable acceptance criteria, and explicit non-goals;
- **Model:** assumptions, parameter sources, sensitivity, and failure range;
- **Implementation:** schematic/code/HDL/mechanical or process files with versions;
- **Verification:** baselines, test matrix, raw data, error, and uncertainty;
- **Engineering constraints:** cost, power, size, maintainability, license, and supply risk;
- **Safety:** hazard identification, energy boundary, stop conditions, and supervision;
- **Communication:** one-page summary, full report, reproduction guide, and design-review record.

## Adjusting the route

### For research

Add derivation, paper reproduction, and uncertainty analysis early. Track a narrow question deeply and treat “could not reproduce” as a valid result. Do not substitute a stack of surveys for research-method training.

### For employment

Extract repeated capabilities from five to ten real role descriptions and build a requirement-to-evidence matrix. Prioritize toolchains, debugging, testing, and collaboration records without skipping theory that limits long-term judgment.

### While enrolled in an EE program

Use this roadmap as an interface layer. Add public explanations, answer feedback, and projects to institutional courses; bring laboratory access, safety training, and peer review to self-study. Do not sacrifice depth in current courses merely to move faster on the map.

### With software only

You can complete substantial work in models, simulation, public data, HDL verification, and control algorithms. Mark hardware results “awaiting validation,” list parasitics, noise, quantization, thermal, and manufacturing effects that simulation omitted, and close the loop later.

Next: choose one mainline matching your stage in the [course catalog](courses/index.md), not the largest number of courses.
