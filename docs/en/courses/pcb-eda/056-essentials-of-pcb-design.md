---
title: "Essentials of PCB Design"
description: "Worcester Polytechnic Institute's Essentials of PCB Design supplements PCB practice with slides, starter files, KiCad materials, and GitHub resources, while recordings are restricted and fabrication is self-funded."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 9ec70be24d4488e1 -->

# Essentials of PCB Design

## Course Overview

- **Institution:** Worcester Polytechnic Institute
- **Course code:** Essentials of PCB Design
- **Track:** [PCB, EDA, and Hardware Verification](index.md)
- **Tier:** B
- **Role:** Supplement
- **Level:** Not standardized by provider (use prerequisites)
- **Last reviewed:** 2026-07-28

Worcester Polytechnic Institute's Essentials of PCB Design supplements PCB practice with slides, starter files, KiCad materials, and GitHub resources, while recordings are restricted and fabrication is self-funded.

**Why choose this course**

Supplement course. Useful for specific topics and best paired with a more complete mainline resource.

**Before you start**

- Recommended foundation: Circuit Analysis
- Recommended foundation: Electronics Laboratory and Measurement

**Verifiable learning outcomes**

- Explain the core models in PCB, EDA, and Hardware Verification, including their assumptions and limits
- Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification

**Workload and pacing**

**7 weeks at 6 hours/week.** This maintainer planning estimate is derived from course role and the density of public practice and labs; it is not a provider workload promise. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.

**Safety level**

**Low energy.** Keep work isolated, current-limited, and low energy; verify ratings, grounding, short-circuit risk, and emergency shutdown before power-up.

## Course Resources

**Software, hardware, and cost**

**Software**

- Maintainer-suggested open-source/free verification path: KiCad (schematic, PCB, and ngspice), gerbv, and Git
- The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable

**Hardware**

- The resource inventory lists lab coverage; prefer borrowing or sharing the following equipment: course-specified components, prototype PCB, current-limited supply, digital multimeter, and oscilloscope only after design checks pass. Verify ratings, authorization, and safety conditions only after the provider lab manual explicitly calls for them

**Cost note**

The suggested software stack is available open source or free; this is not a provider requirement or bill of materials. The actual boards, components, fabrication, and instruments—and their costs—depend on the provider lab manual, region, and local availability; prefer simulation, borrowing, or sharing before purchase.

**Public resource coverage**

| Resource type | Completeness |
|---|---|
| Video | No public material |
| Notes | Partial |
| Practice | No public material |
| Labs | Complete |
| Exams | No public material |
| Code | Complete |

**Resources and access**

| Resource | Access | License | Status | Verified |
|---|---|---|---|---|
| [Course home](https://pcb.wpi.edu/) | Open access | Provider-specific terms; verify before reuse | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice and Verification

**Practice loop**

**Essentials of PCB Design · Worcester Polytechnic Institute Essentials of PCB Design: Manufacturable Low-Voltage Test Board Review**

This is a maintainer-suggested self-study project for Essentials of PCB Design · Worcester Polytechnic Institute Essentials of PCB Design, not an official course assignment. Design a passive or small-signal test board at or below 5 V for PCB, EDA, and Hardware Verification, completing rule checks, BOM, manufacturing outputs, testability, and an optional current-limited bring-up plan.

**Origin:** Maintainer-suggested project

**Deliverables**

- Requirements, interfaces and ratings, power tree, risks, schematic, and design-review checklist
- PCB sources, footprint or 3D checks, DRC and ERC configuration, and versioned libraries
- Gerber, drill, position, BOM, and other manufacturing outputs with raw check reports
- A testability and bring-up report with test points, expected readings, budget, and failure review

**Verification**

- Have 0 unexplained ERC or DRC errors and traceable checks for every interface, supply, and component rating
- Cover reversed connector, do-not-populate, short, open, and probe-access boundaries
- Cross-check layers, drills, and connectivity with an independent Gerber viewer and netlist comparison
- Deliberately remove a decoupler or test point or change a footprint and show the review checklist catches the regression

**Reproducibility**

- Commit schematic, PCB, libraries, BOM, manufacturing, and review sources
- Pin EDA version, design rules, library commit hashes, and generation commands
- Preserve raw ERC, DRC, manufacturing checks, optional bring-up data, and the generated report

**Safety boundary:** Low energy — If fabricated, limit operation to isolated, current-limited supplies at or below 5 V; verify component and connector ratings, solder and wire with power removed, and current-limit first power-up. No mains, battery packs, high current, or hot loads.

**Risks, gaps, and boundaries**

Slides, starter files, KiCad materials, and GitHub resources are public; recordings require a WPI account and fabrication is self-funded.

**Completion evidence**

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Design-review package with requirements and constraints, trade-offs, editable sources, applicable ERC/DRC/timing/stability checks, exports, and a reproduction test
- Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes
- Experiment package with schematic/setup, calibration record, raw data, uncertainty, safety checks, failed runs, and steps to rebuild plots from raw data
