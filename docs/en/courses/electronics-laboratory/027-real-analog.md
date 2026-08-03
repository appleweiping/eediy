---
title: "Real Analog Courses"
description: "Digilent's Real Analog Courses builds a practical analog-circuit sequence from notes, exercises, and instrument-based labs, with strong reproducibility constrained by required Analog Discovery hardware."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: ad70cead9a08b3fe -->

# Real Analog Courses

## Course Overview

- **Institution:** Digilent
- **Course code:** Real Analog
- **Track:** [Electronics Laboratory and Measurement](index.md)
- **Tier:** A
- **Role:** Mainline
- **Level:** Not standardized by provider (use prerequisites)
- **Last reviewed:** 2026-07-28

Digilent's Real Analog Courses builds a practical analog-circuit sequence from notes, exercises, and instrument-based labs, with strong reproducibility constrained by required Analog Discovery hardware.

**Why choose this course**

Mainline course. A reliable option that can serve as a main course or strong alternative.

**Before you start**

- Recommended foundation: Circuit Analysis

**Verifiable learning outcomes**

- Explain the core models in Electronics Laboratory and Measurement, including their assumptions and limits
- Solve representative derivations and problems, checking units, limiting cases, or numerical results
- Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification

**Workload and pacing**

**13 weeks at 11 hours/week.** This maintainer planning estimate is derived from course role and the density of public practice and labs; it is not a provider workload promise. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.

**Safety level**

**Low energy.** Keep work isolated, current-limited, and low energy; verify ratings, grounding, short-circuit risk, and emergency shutdown before power-up.

## Course Resources

**Software, hardware, and cost**

**Software**

- Maintainer-suggested open-source/free verification path: ngspice, sigrok/PulseView, Python 3, and Jupyter
- The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable

**Hardware**

- The resource inventory lists lab coverage; prefer borrowing or sharing the following equipment: a current-limited bench supply, digital multimeter, oscilloscope, function generator, breadboard, and logic analyzer. Verify ratings, authorization, and safety conditions only after the provider lab manual explicitly calls for them

**Cost note**

The suggested software stack is available open source or free; this is not a provider requirement or bill of materials. The actual boards, components, fabrication, and instruments—and their costs—depend on the provider lab manual, region, and local availability; prefer simulation, borrowing, or sharing before purchase.

**Public resource coverage**

| Resource type | Completeness |
|---|---|
| Video | Partial |
| Notes | Complete |
| Practice | Complete |
| Labs | Complete |
| Exams | No public material |
| Code | Partial |

**Resources and access**

| Resource | Access | License | Status | Verified |
|---|---|---|---|---|
| [Course home](https://digilent.com/shop/coursework-learning-resources) | Open access | Provider-specific terms; verify before reuse | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice and Verification

**Practice loop**

**Real Analog Courses · Digilent Real Analog: Measurement-Chain Calibration and Uncertainty Ledger**

This is a maintainer-suggested self-study project for Real Analog Courses · Digilent Real Analog, not an official course assignment. Build a low-voltage source–device–instrument chain for Electronics Laboratory and Measurement and document calibration, repeatability, uncertainty, and wiring-error diagnosis.

**Origin:** Maintainer-suggested project

**Deliverables**

- A wiring diagram, instrument ratings, range choices, safety checklist, and calibration procedure
- An automated or semi-automated acquisition script and a data format with units and timestamps
- Raw data from at least 30 repeated measurements, environmental records, and an uncertainty budget
- A lab report separating random and systematic error and reviewing one deliberately introduced wiring fault

**Verification**

- After calibration, keep mean reference error below 2% of the declared full scale
- Check linearity at low, middle, and high ranges and report fit residuals and confidence intervals
- Cross-check at least ten points with a second instrument or simulation and keep differences inside combined uncertainty
- Inject a probe-factor, ground, or range error and show that the checklist catches it before power-up or in the first reading

**Reproducibility**

- Commit wiring diagrams, acquisition and analysis sources, calibration evidence, a BOM, and a README
- Record instrument model and firmware, probe settings, acquisition parameters, and software environment
- Store raw data read-only with checksums and rebuild tables and the report by script

**Safety boundary:** Low energy — Measure only isolated, current-limited circuits at or below 12 V; verify instrument input ratings and wire with power removed. Never attach an oscilloscope ground clip to mains-side circuitry.

**Risks, gaps, and boundaries**

Requires an Analog Discovery 2 or 3, creating a hardware-cost and regional-availability constraint.

**Completion evidence**

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Design-review package with requirements and constraints, trade-offs, editable sources, applicable ERC/DRC/timing/stability checks, exports, and a reproduction test
- Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes
- Experiment package with schematic/setup, calibration record, raw data, uncertainty, safety checks, failed runs, and steps to rebuild plots from raw data
