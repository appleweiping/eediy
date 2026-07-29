---
title: "RF and Millimeter-Wave Circuit Design"
description: "Eindhoven University of Technology's RF and Millimeter-Wave Circuit Design builds a simulation-first RF and millimeter-wave circuit path in Qucs-S and Octave, with about seventy percent reproducible and hardware optional."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: a3092536c79591ce -->

# RF and Millimeter-Wave Circuit Design

## Course Overview

- **Institution:** Eindhoven University of Technology
- **Course code:** RF and Millimeter-Wave Circuit Design
- **Track:** [RF, Microwave, and Antennas](index.md)
- **Tier:** A
- **Role:** Mainline
- **Level:** Not standardized by provider (use prerequisites)
- **Last reviewed:** 2026-07-28

Eindhoven University of Technology's RF and Millimeter-Wave Circuit Design builds a simulation-first RF and millimeter-wave circuit path in Qucs-S and Octave, with about seventy percent reproducible and hardware optional.

**Why choose this course**

Mainline course. A reliable option that can serve as a main course or strong alternative. Review note: A+

**Before you start**

- Recommended foundation: Electromagnetic Fields and Waves
- Recommended foundation: Circuit Analysis
- Recommended foundation: Communication Systems

**Verifiable learning outcomes**

- Explain the core models in RF, Microwave, and Antennas, including their assumptions and limits
- Solve representative derivations and problems, checking units, limiting cases, or numerical results
- Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification

**Workload and pacing**

**13 weeks at 11 hours/week.** This maintainer planning estimate is derived from course role and the density of public practice and labs; it is not a provider workload promise. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.

**Safety level**

**Simulation only.** The default practice scope is software, computation, or simulation only; a lab label in the resource inventory does not authorize connecting physical equipment, and any hardware extension requires provider-scope verification and a new risk assessment.

## Course Resources

**Software, hardware, and cost**

**Software**

- Maintainer-suggested open-source/free verification path: openEMS, scikit-rf, GNU Octave or Python 3, and KiCad
- The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable

**Hardware**

- The resource inventory lists lab coverage, but this course's maintainer path explicitly limits it to computational or simulation work. It assumes only a general-purpose computer able to run the software above and retain results; do not purchase or connect a vector network analyzer, calibration kit, shielded interconnects, attenuators, and course-specified fixture/antenna in a compliant lab

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
| [Course home](https://www.coursera.org/learn/rf-mmwave-circuit-design) | Registration required | Coursera Terms of Use | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice and Verification

**Practice loop**

**RF and Millimeter-Wave Circuit Design · Eindhoven University of Technology RF and Millimeter-Wave Circuit Design: Passive RF Network and Antenna-Matching Simulation**

This is a maintainer-suggested self-study project for RF and Millimeter-Wave Circuit Design · Eindhoven University of Technology RF and Millimeter-Wave Circuit Design, not an official course assignment. Design a passive matching network, transmission line, or antenna model for RF, Microwave, and Antennas and audit S-parameters, passivity or stability, and manufacturing tolerance.

**Origin:** Maintainer-suggested project

**Deliverables**

- A specification of band, port impedance, geometry or materials, matching, and regulatory boundary
- Circuit or full-wave models, mesh and port settings, and parameter-sweep sources
- Raw S-parameters, Smith-chart data, efficiency or gain or loss, and tolerance Monte Carlo results
- A report comparing analytic, circuit, and field solutions and explaining resonance drift and mismatch failure

**Verification**

- Meet the predeclared return-loss or insertion-loss target over the nominal band and pass a passivity check
- Cover the DC or low-frequency limit, center frequency, band edges, and material-parameter extremes
- Cross-check at least five frequency points against transmission-line or matching equations within 5%
- Inject ±10% geometry or permittivity variation and report resonance shift and worst mismatch

**Reproducibility**

- Commit geometry, circuit, mesh, sweep, and post-processing sources
- Pin solver, material models, ports, meshing rules, and convergence tolerances
- Preserve raw Touchstone or field data, solver logs, and the generated report

**Safety boundary:** Simulation only — Use passive RF or antenna simulation only; do not transmit or connect power amplifiers, microwave sources, or unknown antennas, and do not violate local spectrum rules.

**Risks, gaps, and boundaries**

About seventy percent of the course uses reproducible Qucs-S and Octave simulations, but Coursera access may require payment and hardware is optional.

**Completion evidence**

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Theory dossier with explicit assumptions, notation, derivation, units, and boundary conditions, checked by at least one independent method
- Simulation package with model or netlist, inputs, solver and version, parameter-sweep script, benchmark comparison, expected results, and one rerun command
- Design-review package with requirements and constraints, trade-offs, editable sources, applicable ERC/DRC/timing/stability checks, exports, and a reproduction test
- Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes
