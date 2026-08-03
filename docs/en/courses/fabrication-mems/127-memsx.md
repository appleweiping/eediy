---
title: "Micro and Nanofabrication (MEMS)"
description: "EPFL's Micro and Nanofabrication (MEMS) offers an alternative MEMS fabrication path through videos and cleanroom demonstrations, which remain observational under a costly premium-access model."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: fc596abb1be4736c -->

# Micro and Nanofabrication (MEMS)

## Course Overview

- **Institution:** EPFL
- **Course code:** memsX
- **Track:** [Micro/Nanofabrication and MEMS](index.md)
- **Tier:** A
- **Role:** Alternative
- **Level:** Not standardized by provider (use prerequisites)
- **Last reviewed:** 2026-07-28

EPFL's Micro and Nanofabrication (MEMS) offers an alternative MEMS fabrication path through videos and cleanroom demonstrations, which remain observational under a costly premium-access model.

**Why choose this course**

Alternative course. A reliable option that can serve as a main course or strong alternative.

**Before you start**

- Recommended foundation: Semiconductor Devices
- Recommended foundation: Physics Foundations

**Verifiable learning outcomes**

- Explain the core models in Micro/Nanofabrication and MEMS, including their assumptions and limits
- Solve representative derivations and problems, checking units, limiting cases, or numerical results
- Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification

**Workload and pacing**

**10 weeks at 6 hours/week.** This maintainer planning estimate is derived from course role and the density of public practice and labs; it is not a provider workload promise. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.

**Safety level**

**Simulation only.** The default practice scope is software, computation, or simulation only; a lab label in the resource inventory does not authorize connecting physical equipment, and any hardware extension requires provider-scope verification and a new risk assessment.

## Course Resources

**Software, hardware, and cost**

**Software**

- Maintainer-suggested open-source/free verification path: KLayout, gdsfactory, Python 3, and Jupyter
- The resource inventory does not list public code coverage; the tools above are only a maintainer-suggested independent check, not a provider requirement

**Hardware**

- The resource inventory lists lab coverage, but this course's maintainer path explicitly limits it to computational or simulation work. It assumes only a general-purpose computer able to run the software above and retain results; do not purchase or connect institution-approved cleanroom, process tools, metrology, and personal protective equipment; do not substitute home purchases

**Cost note**

The current maintainer path uses computation and simulation only, with no dedicated hardware purchase, and prefers open-source/free tools. This is not a provider requirement; platform, commercial-software, or cloud-compute costs still vary by provider, region, and plan.

**Public resource coverage**

| Resource type | Completeness |
|---|---|
| Video | Complete |
| Notes | Partial |
| Practice | Partial |
| Labs | Partial |
| Exams | No public material |
| Code | No public material |

**Resources and access**

| Resource | Access | License | Status | Verified |
|---|---|---|---|---|
| [Course home](https://www.edx.org/learn/engineering/ecole-polytechnique-federale-de-lausanne-micro-and-nanofabrication-mems) | Free audit | edX Terms of Service | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice and Verification

**Practice loop**

**Micro and Nanofabrication (MEMS) · EPFL memsX: MEMS Process-Flow and Tolerance Digital Validation**

This is a maintainer-suggested self-study project for Micro and Nanofabrication (MEMS) · EPFL memsX, not an official course assignment. Propose a virtual MEMS or microfabricated structure and process flow for Micro/Nanofabrication and MEMS, then simulate geometry, residual stress, etch bias, and failure margin.

**Origin:** Maintainer-suggested project

**Deliverables**

- Device cross section, mask layers, materials, process sequence, design rules, and risk analysis
- Parameterized geometry or finite-element model and process-tolerance sweep sources
- Raw displacement, frequency, stress, thermal or fluid results and at least 100 tolerance samples
- A report defining process window, yield proxy, failure modes, and layout correction

**Verification**

- Keep the nominal key response within 10% of a simplified beam or membrane analytic model
- Cover minimum feature, maximum etch bias, material extremes, and contact or buckling boundaries
- After mesh refinement, keep the key metric change below 5% and report energy or force balance
- Inject residual stress or mask misalignment and locate the first design-rule or performance failure

**Reproducibility**

- Commit cross-section or mask, parametric geometry, solver, sweep, and post-processing sources
- Pin solver, material library, meshing rules, process parameters, and tolerance seeds
- Preserve raw field and geometry data, solver logs, and the generated report

**Safety boundary:** Simulation only — Use process planning and simulation only; do not use chemicals, vacuum, plasma, lithography, cleanroom equipment, or physical micromechanical structures.

**Risks, gaps, and boundaries**

The audit path is limited and premium access is about USD 249; cleanroom demonstrations are observational rather than reproducible home laboratories.

**Completion evidence**

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Design-review package with requirements and constraints, trade-offs, editable sources, applicable ERC/DRC/timing/stability checks, exports, and a reproduction test
- Simulation package with model or netlist, inputs, solver and version, parameter-sweep script, benchmark comparison, expected results, and one rerun command
