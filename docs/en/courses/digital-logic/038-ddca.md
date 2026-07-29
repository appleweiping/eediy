---
title: "Digital Design and Computer Architecture"
description: "ETH Zurich's Digital Design and Computer Architecture connects digital design and computer architecture through complete 2025 videos, notes, exercises, and code, while its separately hosted materials need manual access checks."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: a1cc439a03febb02 -->

# Digital Design and Computer Architecture

## Course Overview

- **Institution:** ETH Zurich
- **Course code:** DDCA
- **Track:** [Digital Logic and Computation Structures](index.md)
- **Tier:** S
- **Role:** Alternative
- **Level:** Not standardized by provider (use prerequisites)
- **Last reviewed:** 2026-07-28

ETH Zurich's Digital Design and Computer Architecture connects digital design and computer architecture through complete 2025 videos, notes, exercises, and code, while its separately hosted materials need manual access checks.

**Why choose this course**

Alternative course. A particularly complete and well-structured option for this track. Review note: S/A

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

**Low energy.** Keep work isolated, current-limited, and low energy; verify ratings, grounding, short-circuit risk, and emergency shutdown before power-up.

## Course Resources

**Software, hardware, and cost**

**Software**

- Maintainer-suggested open-source/free verification path: Logisim Evolution, Icarus Verilog or Verilator, and GTKWave
- The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable

**Hardware**

- The resource inventory lists lab coverage; prefer borrowing or sharing the following equipment: a logic training board, USB programmer, and logic analyzer explicitly specified by the course. Verify ratings, authorization, and safety conditions only after the provider lab manual explicitly calls for them

**Cost note**

The suggested software stack is available open source or free; this is not a provider requirement or bill of materials. The actual boards, components, fabrication, and instruments—and their costs—depend on the provider lab manual, region, and local availability; prefer simulation, borrowing, or sharing before purchase.

**Public resource coverage**

| Resource type | Completeness |
|---|---|
| Video | Complete |
| Notes | Complete |
| Practice | Complete |
| Labs | Partial |
| Exams | Partial |
| Code | Complete |

**Resources and access**

| Resource | Access | License | Status | Verified |
|---|---|---|---|---|
| [Course home](https://people.inf.ethz.ch/omutlu/lecture-videos.html) | Open access | Provider-specific terms; verify before reuse | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice and Verification

**Practice loop**

**Digital Design and Computer Architecture · ETH Zurich DDCA: Streaming Digital Unit with Formal Checks**

This is a maintainer-suggested self-study project for Digital Design and Computer Architecture · ETH Zurich DDCA, not an official course assignment. Implement a parameterized, handshaked streaming unit for Digital Logic and Computation Structures and verify function, timing protocol, and reset boundaries with RTL simulation, assertions, and randomized testing.

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

The official landing page links complete 2025 videos and materials; the Safari-hosted material server needs a manual robots and download-health check.

**Completion evidence**

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Design-review package with requirements and constraints, trade-offs, editable sources, applicable ERC/DRC/timing/stability checks, exports, and a reproduction test
- Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes
- Simulation package with model or netlist, inputs, solver and version, parameter-sweep script, benchmark comparison, expected results, and one rerun command
- Experiment package with schematic/setup, calibration record, raw data, uncertainty, safety checks, failed runs, and steps to rebuild plots from raw data
