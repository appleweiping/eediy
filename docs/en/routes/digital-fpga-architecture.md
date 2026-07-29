---
title: "Digital Systems, FPGA, and Architecture"
description: "Implement and verify a pipelined processor or custom accelerator and run software on an FPGA or reproducible simulator."
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: c45834519c480e59 -->

# Digital Systems, FPGA, and Architecture

## Audience

Hardware learners who want the full path from RTL to processors and SoCs

## Final outcome

Implement and verify a pipelined processor or custom accelerator and run software on an FPGA or reproducible simulator.

## Stages

### Logic to computer

**Selection rule:** Complete all 1 required course and choose 1 of 2 elective options.

- [Computation Structures](../courses/digital-logic/037-6-004.md) — **Required**; MIT; Mainline; S
- [Build a Modern Computer from First Principles: From Nand to Tetris, Part I](../courses/digital-logic/039-nand2tetris-i.md) — **Elective option**; Hebrew University of Jerusalem; Alternative; S
- [Build a Modern Computer from First Principles: From Nand to Tetris, Part II](../courses/computer-architecture/040-nand2tetris-ii.md) — **Elective option**; Hebrew University of Jerusalem; Alternative; S

**Stage exit criterion:** Build a datapath and controller with a minimal instruction set from Boolean logic, then differentially verify at least 1,000 randomized instruction sequences against a reference interpreter; final waveforms must contain no unexplained X or Z states.

### RTL and board implementation

**Selection rule:** Complete all 1 required course and choose 1 of 3 elective options.

- [Introductory Digital Systems Laboratory](../courses/fpga-soc/042-6-111.md) — **Required**; MIT; Mainline; A
- [Digital Systems Laboratory](../courses/fpga-soc/043-ece-385.md) — **Elective option**; University of Illinois Urbana-Champaign; Alternative; A
- [Digital Design and Integrated Circuits](../courses/vlsi-ic/044-eecs-151.md) — **Elective option**; University of California, Berkeley; Alternative; B
- [Digital Systems Architecture](../courses/fpga-soc/045-ee-180.md) — **Elective option**; Stanford University; Supplement; A

**Stage exit criterion:** Deploy an RTL module with a clock-domain crossing to an FPGA and complete lint, constraint, and static-timing checks; worst slack at the target clock must be nonnegative and board outputs must match simulation golden vectors item by item.

### Architecture and SoC

**Selection rule:** Complete all 2 required courses and choose 1 of 3 elective options.

- [Computer Architecture](../courses/computer-architecture/046-ece-4750.md) — **Required**; Cornell University; Mainline; A
- [Computer System Architecture](../courses/computer-architecture/047-6-823.md) — **Elective option**; MIT; Alternative; A
- [Great Ideas in Computer Architecture](../courses/computer-architecture/048-cs-61c.md) — **Elective option**; University of California, Berkeley; Alternative; A
- [Advanced Microcontroller Design and System-on-Chip](../courses/fpga-soc/052-ece-5760.md) — **Elective option**; Cornell University; Alternative; A
- [Secure Hardware Design](../courses/hardware-security/053-6-5950.md) — **Required**; MIT; Mainline; A

**Stage exit criterion:** Implement a pipelined processor or custom accelerator, run at least three benchmarks with zero deviation from software reference outputs, report throughput, area, and a power proxy, and complete one threat review covering assets and trust boundaries.

## Execution rules

- Follow each stage's selection rule: complete every required course and the stated number of electives; when complete path options are provided, choose one and finish every course in its listed order; use optional supplements only to close a specific gap.
- Produce at least one reproducible artifact per stage and include failed attempts in the retrospective.
- Work involving mains voltage, high voltage, RF exposure, lasers, chemicals, or fabrication equipment requires local-law compliance and qualified supervision.
