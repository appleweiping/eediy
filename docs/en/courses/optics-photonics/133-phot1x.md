---
title: "Silicon Photonics Design, Fabrication and Data Analysis"
description: "University of British Columbia's Silicon Photonics Design, Fabrication and Data Analysis forms a rare full silicon-photonics loop across a KLayout, SiEPIC, gdsfactory, remote-fabrication, and measurement toolchain, with timing, licensing, and regional conditions requiring recheck."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 0b9a880d9ba84c58 -->

# Silicon Photonics Design, Fabrication and Data Analysis

## Course Overview

- **Institution:** University of British Columbia
- **Course code:** Phot1x
- **Track:** [Optics, Optoelectronics, and Photonics](index.md)
- **Tier:** A
- **Role:** Mainline
- **Level:** Not standardized by provider (use prerequisites)
- **Last reviewed:** 2026-07-28

University of British Columbia's Silicon Photonics Design, Fabrication and Data Analysis forms a rare full silicon-photonics loop across a KLayout, SiEPIC, gdsfactory, remote-fabrication, and measurement toolchain, with timing, licensing, and regional conditions requiring recheck.

!!! warning "Mainline audit review"
    This mainline course still requires manual review: The course is instructor-paced, and commercial-tool licenses, regional registration, tapeout dates, and payment terms can change; learners receive measurement data rather than a mailed chip, so every run needs manual recheck. Last audited: 2026-07-29.

**Why choose this course**

Mainline course. A reliable option that can serve as a main course or strong alternative.

**Before you start**

- Recommended foundation: Electromagnetic Fields and Waves
- Recommended foundation: Semiconductor Devices
- Recommended foundation: Physics Foundations

**Verifiable learning outcomes**

- Explain the core models in Optics, Optoelectronics, and Photonics, including their assumptions and limits
- Solve representative derivations and problems, checking units, limiting cases, or numerical results
- Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification

**Workload and pacing**

**13 weeks at 11 hours/week.** This maintainer planning estimate is derived from course role and the density of public practice and labs; it is not a provider workload promise. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.

**Safety level**

**Simulation only.** The default practice scope is software, computation, or simulation only; a lab label in the resource inventory does not authorize connecting physical equipment, and any hardware extension requires provider-scope verification and a new risk assessment.

## Course Resources

**Software, hardware, and cost**

**Software**

- Maintainer-suggested open-source/free verification path: MEEP, MPB, Python 3, Jupyter, and ParaView
- The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable

**Hardware**

- The resource inventory lists lab coverage, but this course's maintainer path explicitly limits it to computational or simulation work. It assumes only a general-purpose computer able to run the software above and retain results; do not purchase or connect course-specified sources, optics, detectors, beam containment, and laser safety controls in a compliant optics lab

**Cost note**

The current maintainer path uses computation and simulation only, with no dedicated hardware purchase, and prefers open-source/free tools. This is not a provider requirement; platform, commercial-software, or cloud-compute costs still vary by provider, region, and plan.

**Public resource coverage**

| Resource type | Completeness |
|---|---|
| Video | Complete |
| Notes | Complete |
| Practice | Complete |
| Labs | Complete |
| Exams | Partial |
| Code | Complete |

**Resources and access**

| Resource | Access | License | Status | Verified |
|---|---|---|---|---|
| [Course home](https://www.edx.org/learn/engineering/university-of-british-columbia-silicon-photonics-design-fabrication-and-data-ana) | Free audit | edX Terms of Service | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice and Verification

**Practice loop**

**Silicon Photonics Design, Fabrication and Data Analysis · University of British Columbia Phot1x: Waveguide or Imaging-System Parameter Sweep**

This is a maintainer-suggested self-study project for Silicon Photonics Design, Fabrication and Data Analysis · University of British Columbia Phot1x, not an official course assignment. Simulate a waveguide, resonator, or imaging system for Optics, Optoelectronics, and Photonics and validate mode, loss, or image quality using analytic limits, mesh convergence, and manufacturing tolerances.

**Origin:** Maintainer-suggested project

**Deliverables**

- A specification of wavelength, materials, geometry, polarization, boundaries, and target metrics
- Executable optical or electromagnetic model, parameter sweeps, and post-processing sources
- Raw fields, modes or point-spread functions, transmission or loss, and tolerance data
- A report comparing analytic and numeric results and explaining cutoff, dispersion, or aberration failure

**Verification**

- Keep effective index, focal length, or diffraction scale within 3% of an analytic simple baseline
- Cover near-cutoff, band-edge, material-extreme, and polarization-switch boundaries
- Keep the key metric change below 3% after mesh refinement or a second propagation method
- Inject ±5% geometry variation and report mode loss, resonance shift, or image degradation

**Reproducibility**

- Commit geometry, material, solver, sweep, and plotting sources
- Pin solver, wavelength grid, material-data version, and convergence parameters
- Preserve raw fields or images, solver logs, material provenance, and the generated report

**Safety boundary:** Simulation only — Use optical or photonic simulation only; do not use lasers, intense sources, high-voltage drivers, bare fiber ends, or unsupervised optical experiments.

**Risks, gaps, and boundaries**

KLayout, SiEPIC, gdsfactory, remote fabrication, and measurement form a rare full loop, but tapeout dates, tool licenses, regional access, and the fact that chips are not mailed must be rechecked.

**Completion evidence**

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Theory dossier with explicit assumptions, notation, derivation, units, and boundary conditions, checked by at least one independent method
- Simulation package with model or netlist, inputs, solver and version, parameter-sweep script, benchmark comparison, expected results, and one rerun command
- Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes
