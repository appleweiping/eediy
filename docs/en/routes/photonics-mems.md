---
title: "Optoelectronics, Photonics, and MEMS"
description: "Complete a photonic or optoelectronic-MEMS design with mode and device simulation, virtual process constraints, layout, and a system performance budget. This is not the shortest route for a purely MEMS goal."
page_type: route
route_id: "route-photonics-mems"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 1a749ed6ae1f8677 -->

# Optoelectronics, Photonics, and MEMS

## Audience

Learners moving from waves, materials, and modes into optoelectronic devices, with moving structures available as a MEMS branch

## What you should be able to do

Complete a photonic or optoelectronic-MEMS design with mode and device simulation, virtual process constraints, layout, and a system performance budget. This is not the shortest route for a purely MEMS goal.

## Solve a mode problem before opening the device menu

Solve one slab-waveguide or Fabry–Pérot mode problem, stating refractive indices, wavelength, boundary conditions, and normalization. If waves, electromagnetic boundaries, or bands are still memorized rather than derived, repair the shared physics. A pure MEMS goal should use the fabrication route instead.

## Make the solver earn trust

- Cross-check modal effective index with an analytic result or second solver, and converge mesh, boundary distance, and material parameters while retaining normalization and power definitions.

## Choose one device mechanism and one system exit

- Choose only the mechanism-appropriate branch among ECE 5330, ECE 5310, and 6.777J, carrying virtual process dimensions and tolerances into device corner sweeps.
- At system level, choose one path—2.71, 3.46, or UBC Silicon Photonics only with complete access—and retain real device loss and dimensional sensitivity in the link budget.
- Skip 8.04 with existing quantum competence, but not the check on bands, density of states, emission, and absorption. Do not take every device branch.
- Skip UBC laboratory claims without its PDK, solver, fabrication, and measurement-data workflow. A product page or restricted lab is not completion.

## Finish with a performance budget, not a lab claim

- Mode and device results converge against mesh, boundary, and critical dimensions; virtual-process corners rerun with one command; unbuilt and unmeasured items are explicit.
- The system budget uses those device results rather than ideal catalog values and identifies the dominant material, dimension, or coupling assumption. No cleanroom or laser measurement is required.

!!! warning "Check these course materials before starting"
    - [Silicon Photonics Design, Fabrication and Data Analysis](../courses/optics-photonics/133-phot1x.md): KLayout, SiEPIC, gdsfactory, remote fabrication, and measurement form a rare enrolled-course loop, but the public edX page does not expose a fixed official PDK, layout, solver, or measurement-data package. The included course flow does not mail each participant a personal chip; the current FAQ says a personal chip may be purchased separately during or after the course, so tapeout dates, tool licenses, regional access, purchase availability, price, shipping, and other terms must be rechecked. Last checked: 2026-07-31.

## How to proceed

### Physics shared by photonic devices

**Why these courses:** The shared physics comes from 8.02X, 8.03SC, ECE 3030, and ECE 4070: electromagnetics, waves, engineering fields, and the material-device connection. ECE 5330, used next, explicitly expects quantum mechanics. If band structure, density of states, emission, and absorption cannot yet be explained, study the relevant 8.04 units or supply equivalent preparation. Existing knowledge can replace 8.04, but it cannot remove the quantum requirement.

- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **Required**; MIT
- [Physics III: Vibrations and Waves](../courses/physics/012-8-03sc.md) — **Required**; MIT
- [Quantum Physics I](../courses/physics/013-8-04.md) — **Use if needed**; MIT
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **Required**; Cornell University
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **Required**; Cornell University

**Move on when:** Solve every relevant mode of a waveguide or resonator in the declared band and check it with a second numerical method. Refine the mesh until eigenfrequency and normalized field energy stabilize, with allowed error set jointly by the discretization trend and device specification.

### From modes to device and process

**Why these courses:** Keep using the existing mode solver, field normalization, material parameters, and convergence results, turning them into device requirements and automated simulation tests. Use 6.152J to understand virtual process constraints and ECE 5330 for semiconductor optoelectronic devices; the former grants no home-fabrication permission. Choose 6.777J for moving structures, micromachining, and electromechanical coupling, or ECE 5310 for quantum states and noise in emission or detection. Cleanrooms, lasers, chemicals, and fabrication equipment remain limited to compliant facilities with qualified supervision.

- [Micro/Nano Processing Technology](../courses/fabrication-mems/126-6-152j.md) — **Required**; MIT
- [Design and Fabrication of Microelectromechanical Devices](../courses/fabrication-mems/129-6-777j.md) — **Choose 1**; MIT
- [Quantum Optics for Photonics](../courses/optics-photonics/130-ece-5310.md) — **Choose 1**; Cornell University
- [Semiconductor Optoelectronics](../courses/optics-photonics/131-ece-5330.md) — **Required**; Cornell University

**Move on when:** Design an optoelectronic, waveguide, or MEMS device tied to a specific process. From its process rules and failure analysis, identify every dimensional or material variable that can push performance out of specification and sweep its sensitivity and corners. Report acceptable tolerances and worst-corner performance, with the layout passing the adopted rule checks.

### Photonic systems

**Why these courses:** NPTEL Introduction to Photonics supplies only the shared system vocabulary, after which exactly one of three courses is chosen: UBC Silicon Photonics with a complete PDK and data workflow, MIT 2.71 for free-space imaging and Fourier optics, or MIT 3.46 for materials, waveguides, and device implementation. Every branch retains the preceding device model, process corners, and dimensional sensitivities rather than substituting ideal catalog values.

- [Introduction to Photonics](../courses/optics-photonics/132-108106135.md) — **Required**; IIT Madras / NPTEL

**Complete path — UBC Silicon Photonics (take these in the listed order)**

1. [Silicon Photonics Design, Fabrication and Data Analysis](../courses/optics-photonics/133-phot1x.md) — **Course in this path**; University of British Columbia; **Check material limits**

**This branch is done when:** Take this branch only when its PDK, layout or solver, fabrication, and measurement-data workflow are accessible; deliver a repeatable layout-to-device-to-link budget plus an explicit list of fabrication or measurement evidence not obtained.

**Complete path — MIT 2.71 free-space and Fourier optics (take these in the listed order)**

1. [Optics](../courses/optics-photonics/134-2-71.md) — **Course in this path**; MIT

**This branch is done when:** Complete a free-space imaging or Fourier-optics system budget and tolerance sweep, stopping explicitly at analysis and simulation when no complete public laboratory package is available.

**Complete path — MIT 3.46 photonic materials and devices (take these in the listed order)**

1. [Photonic Materials and Devices](../courses/optics-photonics/135-3-46.md) — **Course in this path**; MIT

**This branch is done when:** Carry material dispersion and loss into a waveguide or device implementation and complete the link budget over dimensional and material corners; do not claim restricted fabrication or measurement.

**Move on when:** Complete an on-chip or free-space optical link budget and check insertion loss, bandwidth, crosstalk, and energy per bit. Run a reproducible Monte Carlo analysis over dimensional and material variations, increasing the sample count as needed to reach the desired confidence-interval width near the target yield. Report the seed, specification yield, and confidence interval together.
