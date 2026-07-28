---
title: "Solar Energy Engineering: Photovoltaic Energy Conversion"
description: "Delft University of Technology's Solar Energy Engineering: Photovoltaic Energy Conversion builds a photovoltaic-conversion spine from videos, notes, practice, labs, and code, with a matching TU Delft open-course entry, public videos, and notes while edX audit and certificate access remain limited."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 4bbbe1e3e647cba8 -->

# Solar Energy Engineering: Photovoltaic Energy Conversion

[中文](../../../courses/energy-storage-pv/122-pv-energy-conversion.md) · [← Energy Storage and Photovoltaics](index.md)

> Delft University of Technology's Solar Energy Engineering: Photovoltaic Energy Conversion builds a photovoltaic-conversion spine from videos, notes, practice, labs, and code, with a matching TU Delft open-course entry, public videos, and notes while edX audit and certificate access remain limited.

## Course position

| Attribute | Value |
|---|---|
| **Institution** | Delft University of Technology |
| **Course code** | PV Energy Conversion |
| **Track** | [Energy Storage and Photovoltaics](index.md) |
| **Tier** | A |
| **Role** | Mainline |
| **Level** | Advanced |
| **Last reviewed** | 2026-07-28 |

## Why choose this course

Mainline course. A reliable option that can serve as a main course or strong alternative.

## Before you start

- Recommended foundation: Semiconductor Devices
- Recommended foundation: Circuit Analysis
- Recommended foundation: Engineering Mathematics

## Verifiable learning outcomes

- Explain the core models in Energy Storage and Photovoltaics, including their assumptions and limits
- Solve representative derivations and problems, checking units, limiting cases, or numerical results
- Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification

## Workload and pacing

**12 weeks at 10.5 hours/week.** The provider publishes 12 weeks at 10–11 hours per week; the midpoint is shown above for planning. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.

## Software, hardware, and cost

### Software

- Maintainer-suggested open-source/free verification path: pvlib-python, PyBaMM, Python 3, Jupyter, and pandas
- The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable

### Hardware

- The resource inventory lists lab coverage, but this course's maintainer path explicitly limits it to computational or simulation work. It assumes only a general-purpose computer able to run the software above and retain results; do not purchase or connect course-specified protected low-voltage PV/battery training modules, temperature/current sensors, electronic load, and protective enclosure

### Cost note

The current maintainer path uses computation and simulation only, with no dedicated hardware purchase, and prefers open-source/free tools. This is not a provider requirement; platform, commercial-software, or cloud-compute costs still vary by provider, region, and plan.

## Safety level

**Simulation only.** The default practice scope is software, computation, or simulation only; a lab label in the resource inventory does not authorize connecting physical equipment, and any hardware extension requires provider-scope verification and a new risk assessment.

## Public resource coverage

| Resource type | Completeness |
|---|---|
| Video | Complete |
| Notes | Complete |
| Practice | Partial |
| Labs | Partial |
| Exams | No public material |
| Code | Partial |

## Resources and access

| Resource | Access | License | Status | Verified |
|---|---|---|---|---|
| [Course home](https://www.edx.org/learn/solar-energy/delft-university-of-technology-solar-energy-photovoltaic-pv-energy-conversion) | Free audit | edX Terms of Service | Listed by official page | 2026-07-28 |
| [Alternate course entry](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion) | Open access | Provider-specific terms; verify before reuse | Listed by official page | 2026-07-28 |
| [Course readings](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion?view=readings) | Open access | Provider-specific terms; verify before reuse | Listed by official page | 2026-07-28 |
| [Video lectures](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion?view=lectures) | Open access | Provider-specific terms; verify before reuse | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice loop

### Solar Energy Engineering: Photovoltaic Energy Conversion · Delft University of Technology PV Energy Conversion: Battery or PV Energy-Management Digital Twin

This is a maintainer-suggested self-study project for Solar Energy Engineering: Photovoltaic Energy Conversion · Delft University of Technology PV Energy Conversion, not an official course assignment. Build a battery or PV digital twin from public or synthetic data for Energy Storage and Photovoltaics and evaluate state estimation, energy scheduling, temperature or irradiance changes, and safety constraints.

**Origin:** Maintainer-suggested project

**Deliverables**

- Equivalent model, states and parameters, power and temperature bounds, scheduling objective, and data provenance
- Model calibration, state estimation, scheduling, constraint checking, and scenario-simulation sources
- Raw public or synthetic curves, fit residuals, state-of-charge or power trajectories, and constraint logs
- A report comparing baseline and improved strategies and analyzing aging, shading, or thermal-drift failure

**Verification**

- Keep normalized voltage or power RMSE below 5% on held-out data or declare a noise-based threshold
- Cover empty and full state boundaries, temperature extremes, power steps, and sensor bias
- Cross-check state of charge or cumulative generation by energy integration with normalized residual below 2%
- Inject capacity fade or partial shading and show that constraint checks prevent an out-of-bounds schedule

**Reproducibility**

- Commit model, calibration, estimation, scheduling, scenario, and plotting sources
- Pin data version, units, solver, parameters, random seeds, and environment
- Preserve raw public or synthetic data, provenance and license, checksums, and the generated report

**Safety boundary:** Simulation only — Use public or synthetic data and simulation only; do not charge, discharge, or open real cells or connect PV arrays, mains, high voltage, or laser sources.

## Risks, gaps, and boundaries

The edX audit path is limited and certificate pricing can change; the companion open materials use a CC BY-NC-SA license.

## Completion evidence

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Theory dossier with explicit assumptions, notation, derivation, units, and boundary conditions, checked by at least one independent method
- Simulation package with model or netlist, inputs, solver and version, parameter-sweep script, benchmark comparison, expected results, and one rerun command
- Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes
