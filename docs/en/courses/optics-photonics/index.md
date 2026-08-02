---
title: "Optics, Optoelectronics, and Photonics"
description: "Geometric and wave optics, optoelectronic devices, integrated photonics, and quantum optics with reproducible simulation."
page_type: track
track_id: "track-optics-photonics"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 3c742c304258afad -->

# Optics, Optoelectronics, and Photonics

## Track position

Geometric and wave optics, optoelectronic devices, integrated photonics, and quantum optics with reproducible simulation.

## Recommended prerequisite tracks

- [Electromagnetic Fields and Waves](../electromagnetics/index.md)
- [Semiconductor Devices](../semiconductor-devices/index.md)
- [Physics Foundations](../physics/index.md)

## 2.71 and NPTEL build classical optics through derivations and demonstrations

[MIT 2.71](134-2-71.md) uses 10 note sets, six problem sets, and several examinations for geometrical optics, wave optics, diffraction, and imaging. Solutions cover Sets 1–4 but not 5–6, and there is no complete video or physical-laboratory sequence. [NPTEL Introduction to Photonics](132-108106135.md) offers 34 topics, four tutorials, and ten laboratory demonstrations, with broader device phenomena but no public assignment answers. Choose 2.71 for an equation-and-exam backbone or NPTEL for a phenomenon-first route, then borrow only the complementary derivations or demonstrations. Both routes should end with a scaled ray diagram and a diffraction calculation whose normalization can be checked.

The classical base should eventually handle apertures, Fourier planes, sampling, and waveguide boundaries. For a slab waveguide, derive the mode condition and predict mode count, cutoff, effective index, and confinement as geometry changes. Use a solver for numerical comparison and a power integral for normalization. For imaging, predict resolution and aliasing from aperture and detector sampling instead of tuning until an image looks sharp.

## ECE 5330 asks how carriers become optical power

[Cornell ECE 5330](131-ece-5330.md) follows semiconductor optoelectronics into LEDs, lasers, detectors, and modulators. Its [official OCW page](https://ocw.ece.cornell.edu/courses/ece-5330-semiconductor-optoelectronics/) publishes notes and partial assignment feedback, making it the first sustainable public device branch. Modes, polarization, and Poynting flow from [electromagnetics](../electromagnetics/index.md) meet bands, carrier statistics, junctions, recombination, and noise from [semiconductor devices](../semiconductor-devices/index.md). Density of states, occupation, spontaneous and stimulated emission, and recombination must remain distinct as they enter responsivity, gain, threshold, or modulation bandwidth.

Later assignments depend on the unavailable `ece533solver`. MEEP, MPB, Python or Jupyter, gdsfactory, and ParaView can implement open equivalents, but they remain independent work with mesh, boundaries, dispersion, normalization, solver release, and convergence stated. For an LED or detector, place the carrier-rate equation, optical power, and terminal current in one dimensional table; for a laser, add threshold gain, cavity loss, and confinement factor. Open software restores computation, not the private tool or grading feedback.

## ECE 5310 is a separate graduate quantum branch

[Cornell ECE 5310](130-ece-5310.md) uses density matrices, operators, and open systems for quantum optics. Its [official archive](https://ocw.ece.cornell.edu/courses/ece-5310-quantum-optics-for-photonics/) contains notes, homework, and partial exam feedback; it has no video, and the final has no solution. It is not a compulsory endpoint of ordinary optics. Before choosing it, quantum mechanics, basis changes, operators, density matrices, and simple time evolution from [physics](../physics/index.md) should be usable independently. A classical interference formula cannot stand in for quantum-state evolution.

ECE 5310 becomes appropriate when photon statistics, coherence, open-system dynamics, or measurement back-action is the active question. Waveguide cutoff, detector responsivity, and laser threshold are better pursued in the classical or semiconductor branch. As an entry check, solve one two-level system from the same initial state by a matrix equation and numerical integration, then test trace, positivity, and the long-time limit.

## Phot1x is a per-run purchase of an engineering loop, not a permanent public mainline

[UBC Phot1x](133-phot1x.md) must be evaluated as a high-cost, per-run catalogue. Its current [official edX page](https://www.edx.org/learn/engineering/university-of-british-columbia-silicon-photonics-design-fabrication-and-data-ana) requires a fresh check of price, cohort, region, fabrication window, and actual access to PDK, solver, layouts, and measurement data at enrollment. The FAQ says the cohort shares one fabrication, UBC performs the measurements, and participants receive data; no physical chip is mailed by default. A separately purchased personal chip may add fabrication, shipping, and tax. Treat it as a paid cohort only when the live run, budget, region, and visible in-account material all work; an old syllabus and surrounding tools are not a current Phot1x package.

[MIT 3.46](135-3-46.md) enters only when material selection limits device performance, and its paid text and unsolved design work form another access boundary. Lasers, fiber ends, biased detectors, and invisible sources require a compliant laboratory, enclosure, interlocks, and training. A lecture demonstration is not a home bench experiment, so simulation is the default unless the real facility, instruments, and procedures exist.

## Make one device pass mode, material, and measurement budgets

Choose a waveguide, ring resonator, photodetector, LED or laser, or simple imaging system. Fix wavelength, material, geometry, ports, loss, bandwidth, noise, and fabrication tolerance. Cross-check the central result by two independent methods, such as analytic slab modes against a mode solver, a transfer matrix against frequency-domain simulation, or responsivity and noise calculations against a datasheet. Sweep a critical dimension, refractive index, loss, or temperature and identify convergence and the first specification boundary.

Place source power, coupling and connector loss, polarization mismatch, detector floor and bandwidth, averaging time, and expected observable in one measurement budget so a missing signal can be assigned to the device or measurement chain. Without fabrication and instrument data, the conclusion is model-level compliance under stated assumptions; field plots do not replace energy conservation, mesh convergence, or tolerance analysis. End with a parameter table, a convergence plot, and the first tolerance corner to cross specification so the remaining margin can be assigned to device physics, measurement budget, or meshing.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Optics](134-2-71.md) | MIT | Main course | Public-material guide | Public assignments or labs |
| [Semiconductor Optoelectronics](131-ece-5330.md) | Cornell University | Main course | Public-material guide | Partial or restricted |
| [Introduction to Photonics](132-108106135.md) | IIT Madras / NPTEL | Main course | Public-material guide | Partial or restricted |
| [Quantum Optics for Photonics](130-ece-5310.md) | Cornell University | Alternative | Public-material guide | Public assignments or labs |
| [Silicon Photonics Design, Fabrication and Data Analysis](133-phot1x.md) | University of British Columbia | Alternative | Catalogue only; not a complete course substitute | Public assignments or labs |
| [Photonic Materials and Devices](135-3-46.md) | MIT | Supplement | Public-material guide | Partial or restricted |
