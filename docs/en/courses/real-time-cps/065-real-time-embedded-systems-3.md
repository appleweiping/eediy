---
title: "Real-Time Mission-Critical Systems Design"
description: "University of Colorado Boulder's Real-Time Mission-Critical Systems Design advances real-time study into mission-critical design through videos, practice, labs, and code, with specified hardware and paid access as barriers."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: d6b668b8cd279521 -->

# Real-Time Mission-Critical Systems Design

[中文](../../../courses/real-time-cps/065-real-time-embedded-systems-3.md) · [← Real-Time and Cyber-Physical Systems](index.md)

> University of Colorado Boulder's Real-Time Mission-Critical Systems Design advances real-time study into mission-critical design through videos, practice, labs, and code, with specified hardware and paid access as barriers.

## Course position

| Attribute | Value |
|---|---|
| **Institution** | University of Colorado Boulder |
| **Course code** | Real-Time Embedded Systems 3 |
| **Track** | [Real-Time and Cyber-Physical Systems](index.md) |
| **Tier** | A |
| **Role** | Alternative |
| **Level** | Not standardized by provider (use prerequisites) |
| **Last reviewed** | 2026-07-28 |

## Why choose this course

Alternative course. A reliable option that can serve as a main course or strong alternative.

## Before you start

- Recommended foundation: Embedded Systems
- Recommended foundation: Signals and Systems

## Verifiable learning outcomes

- Explain the core models in Real-Time and Cyber-Physical Systems, including their assumptions and limits
- Solve representative derivations and problems, checking units, limiting cases, or numerical results
- Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification

## Workload and pacing

**11 weeks at 9 hours/week.** This maintainer planning estimate is derived from course role and the density of public practice and labs; it is not a provider workload promise. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.

## Software, hardware, and cost

### Software

- Maintainer-suggested open-source/free verification path: Zephyr or FreeRTOS source, GCC or LLVM, CMake, GDB, and Renode or QEMU
- The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable

### Hardware

- The resource inventory lists lab coverage; prefer borrowing or sharing the following equipment: a course-supported real-time control board, USB debugger, logic analyzer, and low-voltage sensors/actuators. Verify ratings, authorization, and safety conditions only after the provider lab manual explicitly calls for them

### Cost note

The suggested software stack is available open source or free; this is not a provider requirement or bill of materials. The actual boards, components, fabrication, and instruments—and their costs—depend on the provider lab manual, region, and local availability; prefer simulation, borrowing, or sharing before purchase.

## Safety level

**Low energy.** Keep work isolated, current-limited, and low energy; verify ratings, grounding, short-circuit risk, and emergency shutdown before power-up.

## Public resource coverage

| Resource type | Completeness |
|---|---|
| Video | Complete |
| Notes | Partial |
| Practice | Complete |
| Labs | Complete |
| Exams | Partial |
| Code | Complete |

## Resources and access

| Resource | Access | License | Status | Verified |
|---|---|---|---|---|
| [Course home](https://www.coursera.org/learn/real-time-mission-critical-systems-design) | Registration required | Coursera Terms of Use | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice loop

### Real-Time Mission-Critical Systems Design · University of Colorado Boulder Real-Time Embedded Systems 3: Real-Time Closed-Loop Deadline Stress Test

This is a maintainer-suggested self-study project for Real-Time Mission-Critical Systems Design · University of Colorado Boulder Real-Time Embedded Systems 3, not an official course assignment. Build a discrete-event scheduler and simulated plant for Real-Time and Cyber-Physical Systems, quantifying how jitter, missed deadlines, and sensor loss affect closed-loop safety margin.

**Origin:** Maintainer-suggested project

**Deliverables**

- A task set with period, deadline, and WCET assumptions, scheduling policy, and plant model
- An executable scheduler, closed-loop simulation, fault injector, and monitoring assertions
- Raw response-time, jitter, miss, and state trajectories across multiple loads
- A report defining the schedulability boundary, control degradation, and safe degraded state

**Verification**

- Produce zero deadline misses at nominal load and keep analytic response-time bound within 10% of the simulated worst case
- Cover zero load, near-100% utilization, burst blocking, and clock-drift boundaries
- Cross-check schedulability with a second analysis or exhaustive enumeration over a short hyperperiod
- Increase WCET until the first miss and report miss rate and closed-loop error growth

**Reproducibility**

- Commit scheduler, plant, fault scenarios, assertions, and analysis sources
- Pin event ordering, random seeds, time units, solver, and dependency versions
- Preserve raw event and state logs and automatically generated timelines and report

**Safety boundary:** Simulation only — Inject deadlines and faults only into a simulated plant; do not connect unvalidated scheduling or degradation logic to real machinery, vehicles, medical, or power systems.

## Risks, gaps, and boundaries

ECC, flash, redundancy, and FMEA exercises use specified hardware, and platform access may require payment.

## Completion evidence

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Design-review package with requirements and constraints, trade-offs, editable sources, applicable ERC/DRC/timing/stability checks, exports, and a reproduction test
- Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes
- Experiment package with schematic/setup, calibration record, raw data, uncertainty, safety checks, failed runs, and steps to rebuild plots from raw data
