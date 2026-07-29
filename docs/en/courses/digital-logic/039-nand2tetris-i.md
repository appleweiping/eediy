---
title: "Build a Modern Computer from First Principles: From Nand to Tetris, Part I"
description: "Hebrew University of Jerusalem's Build a Modern Computer from First Principles: From Nand to Tetris, Part I teaches digital logic through a self-contained HDL simulator and staged projects, subject to changing platform access terms."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 9ee2c95aacb3aa0a -->

# Build a Modern Computer from First Principles: From Nand to Tetris, Part I

## Course Overview

- **Institution:** Hebrew University of Jerusalem
- **Course code:** Nand2Tetris I
- **Track:** [Digital Logic and Computation Structures](index.md)
- **Tier:** S
- **Role:** Alternative
- **Level:** Not standardized by provider (use prerequisites)
- **Last reviewed:** 2026-07-28

Hebrew University of Jerusalem's Build a Modern Computer from First Principles: From Nand to Tetris, Part I teaches digital logic through a self-contained HDL simulator and staged projects, subject to changing platform access terms.

**Why choose this course**

Alternative course. A particularly complete and well-structured option for this track. Review note: S content / A access

**Before you start**

- Recommended foundation: Programming and Engineering Computing
- Recommended foundation: Circuit Analysis

**Verifiable learning outcomes**

- Explain the core models in Digital Logic and Computation Structures, including their assumptions and limits
- Solve representative derivations and problems, checking units, limiting cases, or numerical results
- Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification

**Workload and pacing**

**11 weeks at 9 hours/week.** This maintainer planning estimate is derived from course role and the density of public practice and labs; it is not a provider workload promise. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.

**Safety level**

**Simulation only.** The default practice scope is software, computation, or simulation only; a lab label in the resource inventory does not authorize connecting physical equipment, and any hardware extension requires provider-scope verification and a new risk assessment.

## Course Resources

**Software, hardware, and cost**

**Software**

- Maintainer-suggested open-source/free verification path: Logisim Evolution, Icarus Verilog or Verilator, and GTKWave
- The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable

**Hardware**

- The resource inventory lists lab coverage, but this course's maintainer path explicitly limits it to computational or simulation work. It assumes only a general-purpose computer able to run the software above and retain results; do not purchase or connect a logic training board, USB programmer, and logic analyzer explicitly specified by the course

**Cost note**

The current maintainer path uses computation and simulation only, with no dedicated hardware purchase, and prefers open-source/free tools. This is not a provider requirement; platform, commercial-software, or cloud-compute costs still vary by provider, region, and plan.

**Public resource coverage**

| Resource type | Completeness |
|---|---|
| Video | Complete |
| Notes | Partial |
| Practice | Complete |
| Labs | Complete |
| Exams | No public material |
| Code | Complete |

**Resources and access**

| Resource | Access | License | Status | Verified |
|---|---|---|---|---|
| [Course home](https://www.coursera.org/learn/build-a-computer) | Registration required | Coursera Terms of Use | Listed by official page | 2026-07-28 |
| [Build a Modern Computer from First Principles: Nand to Tetris Part II (project-centered course)](https://www.coursera.org/learn/nand2tetris2) | Registration required | Coursera Terms of Use | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice and Verification

**Practice loop**

**Build a Modern Computer from First Principles: From Nand to Tetris, Part I · Hebrew University of Jerusalem Nand2Tetris I: Streaming Digital Unit with Formal Checks**

This is a maintainer-suggested self-study project for Build a Modern Computer from First Principles: From Nand to Tetris, Part I · Hebrew University of Jerusalem Nand2Tetris I, not an official course assignment. Implement a parameterized, handshaked streaming unit for Digital Logic and Computation Structures and verify function, timing protocol, and reset boundaries with RTL simulation, assertions, and randomized testing.

**Origin:** Maintainer-suggested project

**Deliverables**

- Interface timing diagrams, width and overflow policy, state machine, and latency specification
- Synthesizable RTL, reference model, testbench, and protocol-assertion sources
- Seeds, raw logs, coverage, and waveforms for at least 10,000 randomized transactions
- A verification report listing throughput, latency, coverage holes, and one corrected counterexample

**Verification**

- Match a software reference bit-for-bit for 10,000 randomized transactions with zero assertion failures
- Cover minimum and maximum operands, sustained backpressure, interrupted reset, and counter wraparound
- Exhaust all 8-bit configurations or run equivalence or formal properties for wider configurations
- Inject one off-by-one or handshake defect and show that the suite reproduces and localizes it reliably

**Reproducibility**

- Commit RTL, reference model, assertions, tests, and waveform-viewing instructions
- Pin simulator and synthesis versions, seeds, parameters, and a one-command regression entry point
- Preserve raw regression logs, coverage-database summaries, and the generated report

**Safety boundary:** Simulation only — Use RTL simulation and synthesis reports only by default; do not load a design with unaudited clocks, resets, or interfaces into physical systems.

**Risks, gaps, and boundaries**

The HDL simulator and projects are self-contained, but Coursera trial, payment, and full-course access terms can change.

**Completion evidence**

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Design-review package with requirements and constraints, trade-offs, editable sources, applicable ERC/DRC/timing/stability checks, exports, and a reproduction test
- Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes
- Simulation package with model or netlist, inputs, solver and version, parameter-sweep script, benchmark comparison, expected results, and one rerun command
