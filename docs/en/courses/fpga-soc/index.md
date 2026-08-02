---
title: "FPGA and System-on-Chip Design"
description: "RTL, verification, interfaces, and hardware/software co-design with synthesizable designs and board-level demonstrations."
page_type: track
track_id: "track-fpga-soc"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 2a4dc03b76f5bfcb -->

# FPGA and System-on-Chip Design

## Track position

RTL, verification, interfaces, and hardware/software co-design with synthesizable designs and board-level demonstrations.

## Recommended prerequisite tracks

- [Digital Logic and Computation Structures](../digital-logic/index.md)
- [Computer Architecture](../computer-architecture/index.md)

## 6.111 is the default public archive spine; ECE 5760 is a board-dependent current alternative

The [official MIT 6.111 lab archive](https://ocw.mit.edu/courses/6-111-introductory-digital-systems-laboratory-spring-2006/pages/labs/) publishes 4 Verilog lab assignments and a large final project for [6.111](042-6-111.md). Its boards and EDA flow date to 2006, but the public prompts, project reports, and contemporary implementation constraints form the default openly inspectable practice spine. The [Spring 2026 ECE 5760 home](https://people.ece.cornell.edu/land/courses/ece5760/) publishes the current lab index, C, Verilog, and MATLAB examples, and Quartus projects for [ECE 5760](052-ece-5760.md). It becomes the stronger current alternative only when a DE1-SoC or Cyclone V is available, the required Quartus flow is lawful, and board-specific projects can actually be run or carefully ported.

Choose between the two around boards, lawful licenses, and downloadable projects. 6.111 is valuable as a historical case of laboratories growing into systems. ECE 5760 emphasizes acceleration, processor interfaces, and current projects. Combining both into one timeless “FPGA course” would discard tool conditions and prompt context.

Also distinguish an assignment prompt, a complete downloadable project, and a project showcase. Each supports a different strength of reproduction, even when all three appear on an official course site.

## ECE 385 and EE 180 can only check scope

The [official UIUC ECE 385 page](https://ece.illinois.edu/academics/courses/ece385) publishes SystemVerilog, FPGA, and SoC scope and prerequisites for [ECE 385](043-ece-385.md), not the current assignments, starters, rubrics, feedback, or complete project package. Any RTL task supplied on the course page here is therefore an **independent project map**, not an ECE 385 laboratory. The [Winter 2026 Stanford EE 180 page](https://web.stanford.edu/class/ee180/) exposes topics, readings, and the release rhythm of Homework 1–3 and Lab 1–4 for [EE 180](045-ee-180.md), while assignment buttons, full handouts, starters, slides, Gradescope, and FPGA allocation require SUNet or Canvas.

ECE 385 is therefore catalogue-level scope, and EE 180 is a restricted syllabus index. They do not create third and fourth public lab sequences. Their pages can compare coverage and prerequisites, but a course title is not evidence of executable material, and missing public assessment should not be invented to increase the course count.

Catalogue pages answer what a course covers, and a restricted syllabus may show its assignment rhythm; neither provides an off-campus starter, hidden tests, or feedback. An independent exercise therefore needs its own prompt and acceptance criteria together with an explicit boundary from the institutional course.

## One ready/valid FIFO is enough for the first design check

[Digital logic](../digital-logic/index.md) should already provide synthesizable HDL, FSMs, reset, testbenches, and timing. [Computer architecture](../computer-architecture/index.md) should provide ISA or datapath, memory hierarchy, buses and peripherals, and performance counters. Implement a ready/valid FIFO or small memory-mapped peripheral whose interface, latency, and reset semantics are readable directly from the RTL and testbench.

Random traffic should reach different reset moments, sustained backpressure, boundary widths, and full-to-empty transitions. Occupancy equals accepted writes minus reads; after pointer wrap-around, full and empty cannot be inferred from matching low address bits alone. Assertions can bound occupancy, prevent writes while full and reads while empty, move pointers only on accepted transactions, and leave occupancy unchanged during simultaneous enqueue and dequeue. Utilization, the critical path, and unconstrained-path warnings reveal structural weaknesses earlier than one reassuring waveform.

Drive the same random inputs through a software reference queue and use the waveform to locate the first divergent cycle. That separates protocol errors, data errors, and omissions in the testbench while preserving the same oracle across simulators.

## Porting compares behavior rather than merely producing a new bitstream

The old FPGA environment of 6.111, Quartus 18.1 and DE1-SoC setting of ECE 5760, and legacy VHDL or TTL files associated with ECE 385 are distinct environments. Establish a small set of reference vectors, cycle-level assertions, and a software workload under the original tools, board, and IP, then run the same inputs on the new platform and compare clocks and resets, pinout, interfaces, latency, and throughput.

State simulator, synthesis or implementation release, device part, constraints, IP license, warning policy, and build command. A replaced PLL, memory controller, or vendor IP needs fresh measurements of latency, initialization completion, and reset recovery, especially for reset during a transaction. With no board, conclusions stop at simulation and implementation reports. Physical I/O follows the schematic and bank voltage, with power-off wiring, current limiting, and level translation.

When the original platform is unavailable, the baseline can come from a public testbench and cycle behavior stated explicitly in the prompt, with board-level properties left unverified. Upgrade tools in two steps: run unchanged RTL under the new tool before changing the design. Otherwise warning behavior, inference rules, and structural edits become one inseparable difference; an implementation with missing constraints or an undeclared clock has no timing meaning.

## A SoC project is organized around system boundaries that can be located

Build either a small processor with memory or a peripheral, or a streaming accelerator with a host interface. Before integration, define the address map, data width, clock domains, latency, interrupt or handshake behavior, and reset contract. Unit tests cover properties and boundaries, subsystem tests introduce backpressure, reset, and boundary addresses, and a system test runs a fixed software workload against a reference model. Compare clock frequency, cycle count, memory stalls, host-transfer time, and end-to-end latency together.

At each module boundary, preserve one failing input that can be replayed before full-system integration. Narrow a software-visible mismatch through address, transaction, and cycle, while timing-closure faults are traced through clock domains, constraints, and routing reports. Record the source commit, constraints, and software input that produced each bitstream.

Use the first irreducible mismatch in that trace as the syllabus selector. A mismatch in pipeline, cache, or software-workload semantics goes to architecture; a gap in properties, CDC, reset recovery, or coverage goes to digital verification; a correct computation limited by throughput or energy goes to accelerators or HLS; a fault at bank voltage, connector, or signal integrity returns to PCB and laboratory work. Reproduce the same mismatch at the new boundary before increasing the SoC's size.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Introductory Digital Systems Laboratory](042-6-111.md) | MIT | Main course | Public-material guide; successor-course report is contextual only | Public assignments or labs |
| [Hardware Acceleration via FPGA](052-ece-5760.md) | Cornell University | Alternative | Public-material guide | Public assignments or labs |
| [Digital Systems Laboratory](043-ece-385.md) | University of Illinois Urbana-Champaign | Alternative | Catalogue only; not a complete course substitute | No public practice found |
| [Digital Systems Architecture](045-ee-180.md) | Stanford University | Supplement | Catalogue only; not a complete course substitute | No public practice found |
