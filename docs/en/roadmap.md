---
title: One Possible EE Study Plan
description: A course map from the common core into circuits, chips, embedded systems, signals, control, fields, energy, and instrumentation.
page_type: guide
comments: true
---


# One Possible EE Study Plan

Electrical engineering is not a one-way road from “basic” to “advanced.” Analog circuits, digital systems, communications, control, electromagnetics, power, and devices share part of a mathematical and physical language, then diverge quickly. Any one branch can fill an entire graduate education.

This plan describes relationships among courses, not a semester schedule everyone should copy. Prerequisites and public resources on course pages come from provider material; the choices in the route are EEDIY editorial judgments. New readers should begin with [How to Use This Guide](getting-started.md): choose one mainline for a topic, do not treat alternatives as extra requirements, and never describe simulation as measurement when laboratory access is missing.

## Learn tools until they stop obstructing the work

An EE student does not need to become a software engineer first, but code, versioning, and records recur in almost every track. Develop these abilities inside the first computational or laboratory course that needs them:

- use [Python and Jupyter](guides/python-jupyter.md) to read data, plot figures with units, and regenerate results from raw inputs;
- use [Git](guides/version-control.md) to preserve reversible versions of code, netlists, reports, and hardware;
- learn [C and CMake](guides/c-cmake.md) when native compilation becomes necessary, not as a large environment prepared for hypothetical future work;
- use [SPICE](guides/spice-simulation.md) alongside circuits, with a hand baseline or limiting-case check for every simulation;
- read [Instrumentation and Measurement](guides/instrumentation-measurement.md) and [Laboratory Safety](guides/safety.md) before first contact with instruments.

For a broad first look at EE, [MIT 6.01SC](courses/ee-introduction/019-6-01sc.md) places software, signals, probability, state machines, and robotics in one introduction. It does not replace later specialist courses, but it can reveal which kind of problem deserves more of your patience.

## The common core: languages that the branches keep borrowing

### Interleave mathematics and physics with engineering

Calculus, linear algebra, differential equations, and probability all matter. That does not mean spending two closed years “finishing mathematics” before touching EE. A more useful interleaving is:

1. establish single- and multivariable calculus through [MIT 18.01SC](courses/mathematics/001-18-01sc.md) and [18.02SC](courses/mathematics/002-18-02sc.md);
2. take [MIT 18.06SC](courses/mathematics/004-18-06sc.md) alongside networks and linear systems;
3. enter [MIT 18.03SC](courses/mathematics/003-18-03sc.md) when RC/RLC circuits, mechanical analogies, and state evolution appear;
4. complete [MIT 6.041SC](courses/probability-statistics/007-6-041sc.md), or another probability mainline suited to your background, before noise, random signals, or communications depends on it.

[EE Mathematics Foundations](math-foundations.md) explains the choices in detail. In physics, mechanics trains modeling and energy reasoning, while electromagnetism feeds circuits, fields, devices, and machines directly. The [physics track](courses/physics/index.md) includes entries such as MIT 8.01SC, 8.02x, and 8.03SC. Do not reduce physics to symbolic manipulation; retain free-body diagrams, field geometry, boundaries, and dimensional explanations.

### Circuits, signals, and digital logic form the first professional core

- **Circuits:** [MIT 6.002](courses/circuits/021-6-002.md) is a complete mainline. After nodal analysis and equivalent circuits, do not skip dynamic elements, frequency response, and device models. They return in analog design, control, communications, power, and instrumentation.
- **Signals and systems:** [MIT 6.003](courses/signals-systems/083-6-003.md) places LTI systems, convolution, transforms, sampling, and feedback in one language. It is a prerequisite for DSP, communications, and control, and valuable to anyone processing sensor data.
- **Digital logic:** use [Nand2Tetris I](courses/digital-logic/039-nand2tetris-i.md) to see abstraction layers connect, or compare [MIT 6.004](courses/digital-logic/037-6-004.md) with alternatives in the track for a more conventional undergraduate EE route through logic, state machines, and processors.
- **Programming:** if scripts or C still block assignments, repair them through [Programming and Engineering Tools](courses/programming-tools/index.md). The goal is to read, modify, and test course code—not to finish an unrelated software stack first.

The common core need not be completed to identical depth in every course. It should at least leave you able to derive a low-order model from assumptions; compare hand analysis, simulation, and measurement; read a basic schematic, datasheet, and timing diagram; and preserve a small project that another person can rerun.

## What to keep when time is limited

People already working, changing fields late, or repairing an undergraduate foundation can begin with the six blocks below. They are not “EE in a hurry”; they are interfaces that become difficult to avoid later.

| Block | Suggested mainline | Evidence before moving on |
| --- | --- | --- |
| Engineering mathematics | choose the needed 18.01/18.02/18.06/18.03 material from [mathematics foundations](math-foundations.md) | formulate a circuit or dynamic-system equation and check its scale |
| Circuits | [MIT 6.002](courses/circuits/021-6-002.md) | analyze a network containing a dynamic element or device model |
| Signals | [MIT 6.003](courses/signals-systems/083-6-003.md) | explain convolution, frequency response, sampling, and stability |
| Digital systems | [Nand2Tetris I](courses/digital-logic/039-nand2tetris-i.md) or [MIT 6.004](courses/digital-logic/037-6-004.md) | verify combinational and sequential modules and a small processor structure with tests |
| Computing and records | only the current task's part of the [practice guides](guides/index.md) | code, data, environment, and conclusions can be rerun |
| One track project | choose from the [track routes](routes/index.md) | specifications, model, implementation, verification, and limitations are all present |

Skip a block when an existing project already proves it. Do not delete physics or mathematics merely because time is limited when neither is in place.

## Where the route branches

The summaries below identify a first mainline and a common misconception. Each linked track and route page gives fuller course combinations, alternatives, and project evidence.

### Analog electronics and integrated circuits

A common sequence is:

`6.002 circuits → 6.101 analog laboratory → microelectronic devices → analog IC`

[MIT 6.101](courses/analog-electronics/026-6-101.md) turns amplification, feedback, noise, and instrumentation into physical laboratory work. Without comparable equipment, read the course page's access gap rather than substituting a few ideal SPICE plots for the laboratory. Move through [Microelectronics](courses/microelectronics/index.md) into the [Analog IC route](routes/analog-ic.md) when transistor internals and chip design become the goal. The work continually trades approximation, swing, noise, mismatch, and process corners.

### Digital systems, FPGA, and architecture

A common sequence is:

`digital logic → computer organization → HDL verification → FPGA/SoC or architecture`

[UC Berkeley CS61C](courses/computer-architecture/048-cs-61c.md) connects C, assembly, processors, and memory hierarchy. [MIT 6.111](courses/fpga-soc/042-6-111.md) turns toward larger digital designs and FPGA projects. Demonstrations can hide the missing part: verification. A design that occasionally works on a board still needs self-checking tests, constraints, timing reports, CDC handling, and a reproducible build.

### Embedded systems, PCB design, and real-time work

Between writing C and engineering an embedded system lie datasheets, startup and linking, debuggers, interrupts, buses, concurrency, power, and board behavior. [UT Austin EE 319K](courses/embedded-systems/059-ee-319k-volume-1.md) is the gentler first MCU entry; choose [Stanford CS107E](courses/embedded-systems/058-cs-107e.md) when you are ready to descend through reset, boot, linker, and register layers. They use different boards, so verify that the required hardware can still be obtained.

Enter [KiCad and PCB Design](guides/pcb-kicad.md) when a real board becomes necessary, and [Real-Time and Cyber-Physical Systems](courses/real-time-cps/index.md) when deadlines become part of correctness. Arduino library calls are not a measure of depth; an explained bus timeout, stack overflow, or supply droop is more revealing.

### Signal processing, communications, and information theory

A common sequence is:

`6.003 signals and systems → 6.041SC probability → DSP → detection/estimation or communications`

[MIT RES.6-008](courses/dsp/088-res-6-008.md) is the first systematic DSP spine. Move to [MIT 6.341](courses/dsp/089-6-341.md) after discrete systems are familiar and a longer graduate project is desirable. [MIT 6.450](courses/communications/100-6-450.md) draws heavily on probability when entering digital communication. A clean filtered waveform alone is not enough: retain sampling conditions, data provenance, baselines, noise assumptions, and an error distribution.

### Control, robotics, and autonomous systems

Learn to obtain a model from the physical plant before selecting a controller. [MIT 6.302](courses/control-systems/067-6-302.md) is an entry to classical feedback; the [Control and Robotics route](routes/control-robotics.md) continues into state space, estimation, optimal control, or robotics.

The dangerous control-project illusion is “stable in simulation, therefore safe in hardware.” Actuator saturation, delay, friction, sensor failure, and mechanical stops all violate models. Validate first in simulation and on low-energy teaching hardware, with an emergency stop and explicit fault states.

### Electromagnetics, RF, and photonics

Multivariable calculus, electromagnetism, and complex fields form the common entrance. Compare [Cornell ECE 3030](courses/electromagnetics/107-ece-3030.md) with [MIT 6.013](courses/electromagnetics/108-6-013.md), then branch through [RF, Microwave, and Antennas](routes/rf-wireless.md) or [Photonics and Microsystems](routes/photonics-mems.md).

This branch cannot be learned as algebra around formulas. Geometry, material regions, boundary conditions, modes, and calibration must be explicit. Physical work involving RF power, lasers, vacuum, or fabrication equipment requires a qualified facility.

### Semiconductor devices, VLSI, and fabrication

[MIT 6.012](courses/microelectronics/030-6-012.md) connects semiconductor physics and device models to circuits. [MIT 6.152J](courses/fabrication-mems/126-6-152j.md) continues into processing. The [Semiconductor and VLSI route](routes/semiconductor-vlsi.md) then separates digital VLSI, analog IC, devices, and fabrication.

Device curves, SPICE models, layouts, and process data live at different abstraction levels and cannot stand in for one another. Without cleanroom access, chemicals, and process supervision, fabrication practice remains in public data, design-rule work, and authorized remote or teaching flows.

### Power electronics, machines, and power systems

This branch simultaneously calls on circuits, electromagnetics, control, thermal reasoning, and protection. [MIT 6.622](courses/power-electronics/114-6-622.md) is an entry to converter theory; machines, power systems, and energy courses are separated in the [Power and Energy route](routes/power-energy.md).

Mains, high voltage, and large batteries are not introductory self-study materials. Without a laboratory, supervision, isolation, protection, and a discharge procedure, use simulation or low-energy teaching hardware and name the switching parasitics, thermal behavior, and fault energy that the model omits.

### Instrumentation, sensors, and biomedical systems

This route starts from circuits, signals, probability, and measurement together. Connect sensor excitation, front end, sampling, calibration, and uncertainty into one measurement chain, then follow the [Instrumentation and Biomedical route](routes/instrumentation-biomedical.md). A biomedical-signal project that only plots data but omits electrode or sensor conditions, filter delay, statistical bias, and ethical boundaries cannot support strong conclusions.

## Adapting the route for school, employment, or research

### While enrolled in EE

Use public courses as alternate explanations and sources of feedback for local classes. Institutional laboratories, safety training, instructor access, and peers are resources that online courses struggle to replace. When content overlaps, a stronger public assignment or project may be worthwhile, but check academic-integrity rules and local requirements first.

### Preparing for employment

Extract recurring capabilities from several real job descriptions, then return to courses and projects for evidence. An FPGA position requires more than Verilog syntax, just as embedded work requires more than one MCU. Debugging, testing, interfaces, versioning, and written design judgments often reveal project depth. Do not chase tool names by skipping circuits, signals, or architecture.

### Preparing for research

Practice reading papers, reconstructing derivations, reproducing results, and reporting negative findings early. Courses provide the language and classic models; research questions rarely include answer keys. One narrow, careful investigation is closer to research than simultaneous “introductions” to several fashionable areas.

## Customizing the map

Start from one problem. Open three candidate pages in the [course catalogue](courses/index.md) and compare their first assignments, public feedback, prerequisites, and laboratory conditions. After choosing one mainline, use the [learning routes](routes/index.md) to understand adjacent courses.

When the route changes, retain the exercises, code, and measurements already completed. Record why: missing material, mismatched prerequisites, unavailable equipment, or a teaching style that truly does not fit. That note will help you later and, when submitted through the course-report link, can help the next reader too.
