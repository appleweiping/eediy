---
title: "Digital Systems, FPGA, and Architecture"
description: "Implement a pipelined processor or custom accelerator, verify it against a reference model and regression suite, and run software on an FPGA or a reproducible simulation for a fixed device."
page_type: route
route_id: "route-digital-fpga-architecture"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 8e7c7b9a0a16b583 -->

# Digital Systems, FPGA, and Architecture

## Audience

Hardware learners moving from gates and RTL to FPGAs, pipelined processors, accelerators, and SoCs

## What you should be able to do

Implement a pipelined processor or custom accelerator, verify it against a reference model and regression suite, and run software on an FPGA or a reproducible simulation for a fixed device.

## Separate the hardware and software exits

Choose the exit before starting. Take Nand2Tetris I to build the Hack computer from gates. Take Part II only when an equivalent datapath already exists and the goal is the assembler, VM, and compiler. A Part II software stack is not evidence of completed FPGA or RTL work.

## Finish exactly one Nand2Tetris branch

- Take exactly one Nand2Tetris branch and use its own tests: chips, CPU, memory, and the complete computer for the hardware branch; assembler, VM translator, Jack compiler, and OS modules for the software branch.
- Do not sample both Nand2Tetris I and II, and do not publish solution code the provider asks learners to keep private. A portfolio may explain tests and results.

## Earn the FPGA claim with RTL, constraints, and regression

- Before the FPGA stage, have synthesizable RTL, a self-checking testbench, a fixed device part, and timing constraints. If you have only Part II artifacts, first build an independent RTL module; compiler tests cannot be repurposed as hardware acceptance.
- Carry one reference interpreter and workload into the architecture stage, reporting control-flow, memory, and compute bottlenecks separately. Without the board, retain synthesis and static-timing results for a named device.
- Skip branches whose target board, EDA license, or complete starter is unavailable; a course overview or screenshot does not replace synthesis, timing, and regression.

## Keep separate endpoints for software and hardware

- The Part II branch may stop when the software toolchain passes its provider tests, but the result is a completed software stack only. Continuing to FPGA still requires separate synthesizable RTL and hardware tests.
- The hardware route ends when reference outputs match exactly, no X or Z remains unexplained, timing closes for a fixed device, and performance results rerun. Add a board claim only after a real deployment.

!!! warning "Check these course materials before starting"
    - [Digital Systems Laboratory](../courses/fpga-soc/043-ece-385.md): The current department page, catalogue, and Course Explorer expose no assignments, starter files, rubrics, staff feedback, or complete project package. Any reconstructed RTL or FPGA exercise must remain an independent project rather than being presented as official ECE 385 laboratory work. Last checked: 2026-07-30.
    - [Digital Systems Architecture](../courses/fpga-soc/045-ee-180.md): The public Winter 2026 page exposes the topic and reading schedule plus the names and release dates of Homework 1–3 and Lab 1–4. Complete handouts, starters, slides, solutions, Gradescope, FPGA allocation, and feedback require SUNet or Canvas access, so this is a restricted syllabus index rather than an independently executable course. Last checked: 2026-07-31.

## How to proceed

### From gates to a working computer

**Why these courses:** Let 6.004 establish the digital abstractions and processor boundary. Choose Nand2Tetris I when building a computer from gates for the first time; choose Part II only when an equivalent datapath is already secure and the goal has shifted to the assembler, VM, and compiler. Follow one path rather than sampling both. Keep implementation repositories private as the provider requests; a public portfolio may explain tests but must not publish solution code.

- [Computation Structures](../courses/digital-logic/037-6-004.md) — **Required**; MIT

**Complete path — Nand2Tetris I hardware computer (take these in the listed order)**

1. [Build a Modern Computer from First Principles: From Nand to Tetris, Part I](../courses/digital-logic/039-nand2tetris-i.md) — **Course in this path**; Hebrew University of Jerusalem

**This branch is done when:** The HDL chips, CPU, memory, and Hack computer pass their respective tests and the final system runs the target machine code. This artifact can feed the later RTL/FPGA stage.

**Complete path — Nand2Tetris II software toolchain (take these in the listed order)**

1. [Build a Modern Computer from First Principles: From Nand to Tetris, Part II](../courses/computer-architecture/040-nand2tetris-ii.md) — **Course in this path**; Hebrew University of Jerusalem

**This branch is done when:** The assembler, VM translator, Jack compiler, and implemented OS modules pass their own tests. This accepts a software stack only and makes no gate-level, RTL, or FPGA claim.

**Move on when:** Use the separate stop condition attached to the chosen branch. Only the hardware branch or a separately completed equivalent RTL artifact proceeds directly to FPGA; the software branch may end here or add hardware before continuing.

### RTL on an FPGA

**Why these courses:** Treat the 6.111 FPGA project structure as the working frame and preferably keep the existing datapath, reference interpreter, and randomized instruction tests; a different RTL block should still use the same self-checking harness. Practical access determines the branch: ECE 385 with the Illinois environment, EECS 151 for ASIC synthesis, or EE 180 for architecture-centered RTL. Check the board, EDA license, and assignment access first, and switch paths when one is unavailable.

- [Introductory Digital Systems Laboratory](../courses/fpga-soc/042-6-111.md) — **Required**; MIT
- [Digital Systems Laboratory](../courses/fpga-soc/043-ece-385.md) — **Choose 1**; University of Illinois Urbana-Champaign; **Check material limits**
- [Digital Design and Integrated Circuits](../courses/vlsi-ic/044-eecs-151.md) — **Choose 1**; University of California, Berkeley
- [Digital Systems Architecture](../courses/fpga-soc/045-ee-180.md) — **Choose 1**; Stanford University; **Check material limits**

**Move on when:** An RTL module with a clock-domain crossing must pass self-checking simulation, lint, constraints, synthesis, and static timing with nonnegative worst slack at the target clock. Deploy only on a matching board and compare each board output with golden vectors. Without the board, label the work pre-board, report implementation for a fixed device part, and make no hardware claim.

### Pipelines, accelerators, and SoCs

**Why these courses:** ECE 4750 covers pipelines and performance measurement; 6.5950 adds assets, attack surfaces, and trust boundaries. Continue directly from the existing RTL, constraints, regression, and software workload. The ECE 4750 team repository, server, and some starters are private, so build repeatable tests around the public material without claiming a Cornell lab or autograder result. Choose one remaining gap: 6.823, CS 61C, or ECE 5760 only with DE1-SoC and Quartus access.

- [Computer Architecture](../courses/computer-architecture/046-ece-4750.md) — **Required**; Cornell University
- [Computer System Architecture](../courses/computer-architecture/047-6-823.md) — **Choose 1**; MIT
- [Great Ideas in Computer Architecture](../courses/computer-architecture/048-cs-61c.md) — **Choose 1**; University of California, Berkeley
- [Hardware Acceleration via FPGA](../courses/fpga-soc/052-ece-5760.md) — **Choose 1**; Cornell University
- [Secure Hardware Design](../courses/hardware-security/053-6-5950.md) — **Required**; MIT

**Move on when:** Implement a pipelined processor or custom accelerator with benchmarks that separately expose control-flow, memory, and compute bottlenecks, while matching software reference outputs exactly. Report throughput, area, and a power estimate for each workload class, then explain threats and mitigations against the stated assets, entry points, and trust boundaries.
