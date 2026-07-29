---
title: "Build a Modern Computer from First Principles: From Nand to Tetris, Part II"
description: "Hebrew University of Jerusalem's Build a Modern Computer from First Principles: From Nand to Tetris, Part II uses six self-contained projects to implement a virtual machine, compiler, and operating system, requiring introductory programming, Python or Java setup, and potentially paid platform access."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: bd0510d3c730b3f2 -->

# Build a Modern Computer from First Principles: From Nand to Tetris, Part II

## Course Overview

- **Institution:** Hebrew University of Jerusalem
- **Course code:** Nand2Tetris II
- **Track:** [Computer Architecture](index.md)
- **Tier:** S
- **Role:** Alternative
- **Level:** Not standardized by provider (use prerequisites)
- **Last reviewed:** 2026-07-28

Hebrew University of Jerusalem's Build a Modern Computer from First Principles: From Nand to Tetris, Part II uses six self-contained projects to implement a virtual machine, compiler, and operating system, requiring introductory programming, Python or Java setup, and potentially paid platform access.

**Why choose this course**

Alternative course. A particularly complete and well-structured option for this track. Review note: S content / A access

**Before you start**

- Recommended foundation: Digital Logic and Computation Structures
- Recommended foundation: Programming and Engineering Computing
- Recommended background: Introductory programming; Part I is a useful companion, but the provider describes Part II as self-contained

**Verifiable learning outcomes**

- Explain the core models in Computer Architecture, including their assumptions and limits
- Solve representative derivations and problems, checking units, limiting cases, or numerical results
- Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification

**Workload and pacing**

**11 weeks at 9 hours/week.** This maintainer planning estimate is derived from course role and the density of public practice and labs; it is not a provider workload promise. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.

**Safety level**

**Simulation only.** The default practice scope is software, computation, or simulation only; a lab label in the resource inventory does not authorize connecting physical equipment, and any hardware extension requires provider-scope verification and a new risk assessment.

## Course Resources

**Software, hardware, and cost**

**Software**

- Maintainer-suggested open-source/free verification path: a RISC-V GNU or LLVM toolchain, QEMU, Verilator, and GTKWave
- The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable

**Hardware**

- The resource inventory lists lab coverage; the maintainer path treats it as computational/simulation work unless the provider lab manual explicitly says otherwise. It assumes only a general-purpose computer for simulation and cross-compilation; use a specified RISC-V or FPGA board only when the course explicitly calls for it. If the provider lists different equipment or compute requirements, follow its course page

**Cost note**

The suggested software stack is available open source or free; this is maintainer planning, not a provider requirement. If the provider specifies commercial licenses, cloud compute, storage, or institutional resources, costs vary by plan, region, and institution, so no fixed price is asserted here.

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
| [Course home](https://www.coursera.org/learn/nand2tetris2) | Registration required | Coursera Terms of Use | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice and Verification

**Practice loop**

**Build a Modern Computer from First Principles: From Nand to Tetris, Part II · Hebrew University of Jerusalem Nand2Tetris II: Microarchitecture Performance and Correctness Audit**

This is a maintainer-suggested self-study project for Build a Modern Computer from First Principles: From Nand to Tetris, Part II · Hebrew University of Jerusalem Nand2Tetris II, not an official course assignment. Implement an instruction-level simulator or pipeline model for Computer Architecture and reproducibly audit functional correctness, CPI, cache behavior, and hazard handling.

**Origin:** Maintainer-suggested project

**Deliverables**

- A specification of ISA subset, pipeline or cache parameters, exceptions, and counter semantics
- Simulator or RTL model, reference executor, and source files for at least 20 microbenchmarks
- Raw instruction traces, performance counters, cache-hit data, and runtimes
- A report explaining performance bottlenecks, correctness counterexamples, and design tradeoffs

**Verification**

- Match architectural state instruction-by-instruction against the reference executor on every microbenchmark
- Cover empty programs, all-mispredicted branches, dependency chains, cache thrashing, and address boundaries
- Hand-calculate instruction count and ideal CPI for at least 5 short programs and cross-check counters
- Disable forwarding or change cache-line size and quantify CPI or miss-rate changes, explaining anomalies

**Reproducibility**

- Commit model, microbenchmark, reference, test, and trace-analysis sources
- Pin compiler, simulator, parameters, benchmark inputs, and build commands
- Preserve raw traces, counters, and report-generation logs with checksums

**Safety boundary:** Simulation only — Use local simulators and self-authored tests only; do not execute unknown binaries, real malicious payloads, or unisolated privileged code.

**Risks, gaps, and boundaries**

Six substantial projects require Python or Java setup, and Coursera access terms can change.

**Completion evidence**

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Design-review package with requirements and constraints, trade-offs, editable sources, applicable ERC/DRC/timing/stability checks, exports, and a reproduction test
- Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes
- Simulation package with model or netlist, inputs, solver and version, parameter-sweep script, benchmark comparison, expected results, and one rerun command
