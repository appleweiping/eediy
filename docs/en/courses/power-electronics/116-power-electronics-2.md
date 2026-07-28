---
title: "Converter Circuits"
description: "University of Colorado Boulder's Converter Circuits specializes in converter circuits after the introductory course, using videos, practice, simulation, and code under an explicit prerequisite and possible access fee."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 2769dabd9773043c -->

# Converter Circuits

[中文](../../../courses/power-electronics/116-power-electronics-2.md) · [← Power Electronics](index.md)

> University of Colorado Boulder's Converter Circuits specializes in converter circuits after the introductory course, using videos, practice, simulation, and code under an explicit prerequisite and possible access fee.

## Course position

| Attribute | Value |
|---|---|
| **Institution** | University of Colorado Boulder |
| **Course code** | Power Electronics 2 |
| **Track** | [Power Electronics](index.md) |
| **Tier** | A |
| **Role** | Alternative |
| **Level** | Not standardized by provider (use prerequisites) |
| **Last reviewed** | 2026-07-28 |

## Why choose this course

Alternative course. A reliable option that can serve as a main course or strong alternative.

## Before you start

- Recommended foundation: Circuit Analysis
- Recommended foundation: Control Systems
- Recommended foundation: Electronics Laboratory and Measurement
- Course-sequence requirement: complete [Introduction to Power Electronics](../power-electronics/115-power-electronics-1.md) (University of Colorado Boulder Power Electronics 1) first

## Verifiable learning outcomes

- Explain the core models in Power Electronics, including their assumptions and limits
- Solve representative derivations and problems, checking units, limiting cases, or numerical results
- Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification

## Workload and pacing

**11 weeks at 7 hours/week.** This maintainer planning estimate is derived from course role and the density of public practice and labs; it is not a provider workload promise. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.

## Software, hardware, and cost

### Software

- Maintainer-suggested open-source/free verification path: Qucs-S, ngspice, Python 3, Jupyter, and GNU Octave
- The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable

### Hardware

- The resource inventory lists lab coverage, but this course's maintainer path explicitly limits it to computational or simulation work. It assumes only a general-purpose computer able to run the software above and retain results; do not purchase or connect isolated/current-limited power, differential probes, electronic load, oscilloscope, and course-specified power stage in a compliant lab

### Cost note

The current maintainer path uses computation and simulation only, with no dedicated hardware purchase, and prefers open-source/free tools. This is not a provider requirement; platform, commercial-software, or cloud-compute costs still vary by provider, region, and plan.

## Safety level

**Simulation only.** The default practice scope is software, computation, or simulation only; a lab label in the resource inventory does not authorize connecting physical equipment, and any hardware extension requires provider-scope verification and a new risk assessment.

## Public resource coverage

| Resource type | Completeness |
|---|---|
| Video | Complete |
| Notes | Partial |
| Practice | Complete |
| Labs | Partial |
| Exams | No public material |
| Code | Partial |

## Resources and access

| Resource | Access | License | Status | Verified |
|---|---|---|---|---|
| [Course home](https://www.coursera.org/learn/converter-circuits) | Registration required | Coursera Terms of Use | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice loop

### Converter Circuits · University of Colorado Boulder Power Electronics 2: Converter Loss and Closed-Loop Protection Simulation

This is a maintainer-suggested self-study project for Converter Circuits · University of Colorado Boulder Power Electronics 2, not an official course assignment. Simulate a DC–DC converter for Power Electronics and quantify ripple, efficiency proxy, device stress, control stability, and overcurrent or open-load protection.

**Origin:** Maintainer-suggested project

**Deliverables**

- A specification of topology, input and output range, switching frequency, ratings, control, and protection
- Switching model, averaged model, controller, and fault-scenario sources
- Raw steady-state, startup, load-step, and fault waveforms with loss and stress data
- A report comparing analytic, averaged, and switching models and explaining worst stress and protection action

**Verification**

- Keep nominal steady-state output error below 2% and ripple within 15% of hand analysis
- Cover minimum and maximum input, no and full load, startup, and device-parameter extremes
- Cross-check input, output, and loss by power balance with normalized residual below 1%
- Inject a short-circuit proxy or load dump and show protection acts within the declared time without rating violations

**Reproducibility**

- Commit topology, models, controller, faults, calculations, and plotting sources
- Pin simulator, device models, time step, switching, and control parameters
- Preserve raw waveforms, power and stress tables, fault logs, and the generated report

**Safety boundary:** Simulation only — Use converter simulation only; do not build mains, high-voltage, high-current, magnetic-component, battery-powered, or power-switching hardware.

## Risks, gaps, and boundaries

This course assumes the introductory power-electronics course, and platform access may require payment.

## Completion evidence

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Design-review package with requirements and constraints, trade-offs, editable sources, applicable ERC/DRC/timing/stability checks, exports, and a reproduction test
- Simulation package with model or netlist, inputs, solver and version, parameter-sweep script, benchmark comparison, expected results, and one rerun command
- Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes
