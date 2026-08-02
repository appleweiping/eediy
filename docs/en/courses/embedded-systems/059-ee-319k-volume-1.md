---
title: "Embedded Systems: Shape the World"
description: "The University of Texas at Austin's Embedded Systems: Shape the World provides an embedded-systems introduction through an open text, chapter-embedded videos, and activities created for EE 319K; the dead aggregate video index is excluded, the edX run is archived, and learners should prefer the MSPM0 edition while preserving their own lab records."
page_type: course
course_id: "course-059"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-29"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 229b025703f494a1 -->

# The University of Texas at Austin EE 319K / Volume 1: Embedded Systems: Shape the World

## Course Overview

- **University:** The University of Texas at Austin
- **Course code:** EE 319K / Volume 1
- **Official prerequisites:** UT Austin EE 319K requires EE 306, ECE 306, or BME 306 with a grade of at least C-
- **EEDIY preparation:** No additional EEDIY preparation requirement
- **Access:** Open without registration
- **Material status:** 2026-07-29; public-material guide

### Course fit

UT Austin EE319K’s [2022 Volume 1](https://users.ece.utexas.edu/~valvano/Volume1/IntroToEmbSys/) targets the TM4C123/Cortex-M4 in 10 chapters. The [Spring 2026 syllabus](https://users.ece.utexas.edu/~valvano/mspm0/EE319KSp26.html) instead uses the LP-MSPM0G3507/Cortex-M0+, current CCS, and a 9-chapter e-book. The conceptual order transfers; register addresses, startup code, project files, and pinouts do not. Put `LP-MSPM0G3507 / Spring 2026` at the top of the repository and treat the old book only as conceptual support.

The prerequisite is EE306, ECE306, or BME306 with at least C-. If you cannot yet read simple assembly, draw a finite-state machine, and explain voltage, current, and binary representation, repair those gaps before buying the kit.

### Labs and projects

[Labs](https://users.ece.utexas.edu/~valvano/mspm0/labs.html) progresses through Lab 1–9: the first 5 are individual and the final 4 are paired. Lab 1 establishes the toolchain and assembly, Lab 2 handles switches and LEDs, Lab 3 uses C and debug dumps, Lab 4 implements a traffic-light FSM, and Lab 5 builds a piano with a 5-bit DAC. The sequence then covers LCD/fixed-point output, real-time ADC position, serial FIFO data acquisition, and a game.

Do more than record successful videos. For each lab, preserve source, wiring, input conditions, a logic trace or dump, a failure boundary, and its fix. Lab 4 should be reconstructible from a transition table; Lab 7 should retain the ADC calibration curve; Lab 8 should show FIFO sample loss at peak input; Lab 9 should explain how frame timing, input, and sound share the budget.

### Access and version notes

[Downloads](https://users.ece.utexas.edu/~valvano/mspm0/downloads.htm) supplies software and partial starters, while [Exams](https://users.ece.utexas.edu/~valvano/mspm0/exams.htm) can test assembly, FSMs, I/O, and timing. Canvas quizzes, in-person checkoffs, the full grader, and unpublished solutions remain unavailable. Attempt the work before looking for answers, then use waveforms, boundary inputs, and a second implementation to locate mistakes; searching for answers is not a substitute for grader or TA feedback.

[ValvanoWare](https://github.com/kk4ead/ValvanoWare) is kk4ead's public
subset of Jonathan Valvano's material, retaining BSD-compatible licenses and
TM4C123 traffic-light, ADC, FIFO, and SysTick examples. It is useful only for
checking interfaces from the 2022 Volume 1 board, not as a 2026 MSPM0 starter.
Compare an FSM table or FIFO contract, but rewrite register code for the
current device.

Compared with Stanford CS107E, this course is the better first systematic encounter with MCU I/O, instruments, and real-time loops. CS107E goes deeper into runtimes, linkers, allocators, and an interrupt-driven library. They can follow one another, but different ISAs and boards should never be combined into one project.

### Keep One Failure from FSM, Calibration, and Real-Time I/O

Use the [TI LP-MSPM0G3507 guide](https://www.ti.com/lit/ug/slau873d/slau873d.pdf) for hardware connections. Default J101 exposes GND, 5 V, 3V3, UART, and SWD; it does not imply safety isolation. Wire only with power removed, use current limiting, calculate the speaker drive and LED resistors from the current schematic, and exclude mains, lithium charging, and unknown external supplies.

Choose one real failure from the Lab 4 FSM, Lab 7 sensor calibration, and Lab
8/9 real-time integration. Then build a small system that connects input,
state, output, and timing to raw data. Explaining the version, waveform, and
one performance tradeoff reveals whether MCU I/O, instruments, and the
real-time loop actually connect; “running 9 labs” does not.

## Course Resources

- [Course home](https://users.ece.utexas.edu/~valvano/Volume1/IntroToEmbSys)
- [Alternate course entry](https://users.ece.utexas.edu/~valvano/mspm0/ebook)
- [Notes · Assembly reference](https://users.ece.utexas.edu/~valvano/Volume1/IntroToEmbSys/AssemblyReference.htm)

## Resource Summary

<details markdown="1">
<summary>Show more official resources (1 item)</summary>

**Resource**

| Resource | Access | Status | Verified |
|---|---|---|---|
| [TM4C123 Hardware Reference Material](https://users.ece.utexas.edu/~valvano/Volume1/IntroToEmbSys/Appendix.htm) | Open access | Listed by official page | 2026-07-28 |

> These remaining entries retain access status and review dates. Rights stay with the original providers, and actual access may change with account, region, or course redesign.

</details>
