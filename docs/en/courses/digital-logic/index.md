---
title: "Digital Logic and Computation Structures"
description: "Combinational and sequential logic, finite-state machines, processors, and memory from gates to complete computers."
page_type: track
track_id: "track-digital-logic"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 0d0c628814a128ac -->

# Digital Logic and Computation Structures

## Track position

Combinational and sequential logic, finite-state machines, processors, and memory from gates to complete computers.

## Recommended prerequisite tracks

- [Programming and Engineering Computing](../programming-tools/index.md)
- [Circuit Analysis](../circuits/index.md)

## Three spines answer “what is a digital system?” through different projects

[MIT 6.004](037-6-004.md) moves from combinational logic to processor organization. Its [official 2017 archive](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017) supplies 21 teaching units with videos, annotated slides, and worksheets; its syllabus names 7 labs, but the lab files are not in the public navigation. The [2009 official archive](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2009/) supplies 8 public labs, tutorial problems, and historical quizzes and exams under an older toolchain. Use the 2017 explanation and 2009 practice with the year shown on every artifact rather than describing them as one MIT offering. [ETH DDCA](038-ddca.md) keeps 2025 videos, notes, exercises, and code in one version; its [public lecture-video index](https://people.inf.ethz.ch/omutlu/lecture-videos.html) pairs naturally with SystemVerilog, Vivado, and Basys 3 synthesis. [Nand2Tetris I](039-nand2tetris-i.md) uses a self-contained HDL simulator and 6 cumulative projects to build from NAND to a computer. It has the lowest hardware barrier but does not teach FPGA timing constraints or board I/O.

Each route is complete in a different sense: 6.004 gives the processor panorama, DDCA gives a current HDL and FPGA environment, and Nand2Tetris emphasizes layered interfaces. Normally finish one project's sequence. [Cornell ECE 2300](041-ece-2300.md) publishes notes but no homework, laboratories, or exams; it can offer a second explanation for a difficult concept, not replace a project spine. Choose by the processor or FPGA work you are willing to complete rather than school name or video count.

The access boundary changes the portfolio: a complete public lab package can support the original prompt, while notes alone support only an explicitly independent module. Do not invent missing institutional assessment to make the routes appear symmetric.

## A one-page ISA, a testbench, and the first wrong cycle form the central exercise

[Programming and tools](../programming-tools/index.md) should support version control, scripts, bit operations, and command-line tests. [Circuit analysis](../circuits/index.md) supplies voltage logic, combinational delay, clocks, and stored state. Minimize a truth table and test every input, turn a prose specification into an FSM with explicit reset behavior, and write a self-checking testbench for a registered datapath covering normal, boundary, and illegal cases. Unclear setup, hold, clock-to-Q, or metastability calls for timing physics; clicking through every waveform in a GUI calls for test automation.

Then implement an ALU, registered state, controller or FSM, memory interface, and executable program from a one-page ISA. Put the reference model, edge-case table, and minimized counterexample beside the HDL. Trace one instruction through encoding, control, datapath values, clock boundaries, and visible result, then change one control bit and predict the first wrong cycle. The two 6.004 offerings cannot become a fictitious same-term grade. A DDCA project states Vivado, target part, board files, constraints, and warning policy; no Basys 3 means a pre-board result. The Nand2Tetris license asks learners to keep project solutions private, so a public portfolio shows self-written tests and non-solution explanation.

## The implementation report decides among architecture, verification, and FPGA work

Passing simulation does not establish synthesis timing, and a lit LED does not replace a reference model. Report utilization, critical path, clock period, cycle count, CPI, and memory behavior for the same design. With a board, map the bitstream to its source commit and demonstrate a deterministic input. Adding an instruction should touch defined decode, control, and datapath boundaries while existing tests reveal omissions.

Use one added instruction as the handoff test: its specification, state transition, reference result, first wrong cycle, synthesis timing, and source commit must agree. A mismatch before the architectural result is stable remains a digital-logic problem. Once that chain holds, pipeline/cache performance moves to [computer architecture](../computer-architecture/index.md), properties and coverage move to digital verification, and CDC, board interfaces, or constraints move to FPGA/SoC implementation. The selected branch inherits the same instruction and tests rather than replacing them with a new demonstration.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Computation Structures](037-6-004.md) | MIT | Main course | Public-material guide | Public assignments or labs |
| [Digital Design and Computer Architecture](038-ddca.md) | ETH Zurich | Alternative | Public-material guide | Public assignments or labs |
| [Build a Modern Computer from First Principles: From Nand to Tetris, Part I](039-nand2tetris-i.md) | Hebrew University of Jerusalem | Alternative | Public-material guide | Public assignments or labs |
| [Digital Logic and Computer Organization](041-ece-2300.md) | Cornell University | Supplement | Catalogue only; not a complete course substitute | No public practice found |
