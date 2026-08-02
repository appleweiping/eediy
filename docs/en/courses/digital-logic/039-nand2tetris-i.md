---
title: "Build a Modern Computer from First Principles: From Nand to Tetris, Part I"
description: "Hebrew University of Jerusalem's Build a Modern Computer from First Principles: From Nand to Tetris, Part I teaches digital logic through a self-contained HDL simulator and staged projects, subject to changing platform access terms."
page_type: course
course_id: "course-039"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 5e189dc7e03afcaf -->

# Hebrew University of Jerusalem Nand2Tetris I: Build a Modern Computer from First Principles: From Nand to Tetris, Part I

## Course Overview

- **University:** Hebrew University of Jerusalem
- **Course code:** Nand2Tetris I
- **Official prerequisites:** The official Nand2Tetris site states that Part I requires no prior knowledge
- **EEDIY preparation:** No additional EEDIY preparation requirement
- **Access:** Open entry; some materials require registration or are limited
- **Material status:** 2026-07-30; public-material guide

### Labs and projects

Nand2Tetris Part I is cumulative rather than organized around lectures and
exams. Projects 1–6 on the official
[course page](https://www.nand2tetris.org/course) build logic gates, an
adder/ALU, registers and RAM, Hack assembly programs, a CPU/computer, and an
assembler. The official [home](https://www.nand2tetris.org/) supplies
lectures, specifications, and tools and states that no prior knowledge is
required. Projects 4 and 6 do involve programming and files; a complete
beginner should first learn variables, loops, functions, and command-line
basics.
Choose it if you want to construct a machine interface by interface; a short
HDL course is more direct when syntax is the only goal.

### Use Only Interfaces Already Built

[Project 1](https://www.nand2tetris.org/project01) demonstrates the common
contract: an `.hdl` interface, `.tst` script, and `.cmp` output. Do not call a
future-project chip or host-language library. Keep a truth or state table,
design sketch, official test transcript, added edge tests, and bug log for
each project. Hand-trace registers, memory, and jumps in Project 4; draw the
datapath and control truth table before Project 5; and preserve the tokenizer,
two-pass symbol table, and malformed-input tests for the Project 6 assembler.

The official [software](https://www.nand2tetris.org/software) includes a
browser IDE and legacy Java desktop tools. Choose one path for all 6 projects
and export source regularly. Switching tools halfway can make formatting or
time-step behavior look like a design defect.

### Trace One Instruction from NAND without Notes

At the end, choose one Hack C-instruction and write its assembler encoding,
control bits, ALU function, destination and jump behavior, CPU datapath, and
register/memory timing. Flip one control bit, predict the machine behavior,
and then verify it in the emulator. This demonstrates accumulated abstraction
better than 6 separately green projects.

The official [license](https://www.nand2tetris.org/license) asks learners not
to publish project solutions. Keep HDL and assembler source private; a public
portfolio can discuss design decisions, testing, and non-solution
demonstrations. A physical FPGA is not a Part I requirement. Continue to Part
II's VM, compiler, and OS only after the assembler reliably produces machine
code for the Project 5 computer.

Run one dependency audit from the lowest gate through the CPU: every chip may
refer only to components already completed. For each sequential component,
state the current-cycle input, the state-update boundary, and what becomes
visible next cycle. If one fault looks different in a chip test and a computer
test, use the smallest test script to pin down the first divergence instead of
repeatedly changing wiring by guesswork.
That check should include bit widths, reset state, and the boundary between
combinational output and registered state. After every repair, rerun the older
chip tests as well as the computer test; otherwise a passing upper layer can
hide a lower-level interface that has quietly changed.

## Course Resources

- [Code · Nand2Tetris projects and software suite](https://www.nand2tetris.org/software)
- [Course home](https://www.coursera.org/learn/build-a-computer)

## Resource Summary

Every public entry point verified in this review is listed above. Use the feedback and corrections links below to submit a completion record, another resource, or a broken-link report.
