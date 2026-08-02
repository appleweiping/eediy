---
title: "Semiconductors, Micro/Nanofabrication, and VLSI"
description: "Complete a digital chip design whose device parameters, process assumptions, RTL, timing and power constraints, verification, and layout all use the same stated premises."
page_type: route
route_id: "route-semiconductor-vlsi"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 60f1ab2f0fdd42e8 -->

# Semiconductors, Micro/Nanofabrication, and VLSI

## Audience

Learners who want semiconductor devices, microfabrication, digital IC design, and physical implementation to form one connected workflow

## What you should be able to do

Complete a digital chip design whose device parameters, process assumptions, RTL, timing and power constraints, verification, and layout all use the same stated premises.

## Choose a device question or a layout question first

Choose one CMOS inverter and state its device model, VDD, temperature, load, and process assumptions, then estimate switching point and delay from its I–V behavior. If those premises cannot be fixed, remain at the device model instead of sending RTL directly to layout.

## Carry one tested device model forward

- Derive one versioned parameter set from bands, device curves, and the compact model, carrying critical dimensions, tolerances, and process rules into gate delay and power estimates.
- Keep microfabrication to virtual flow and case analysis. Choose one of MEMS, systematic microfabrication, or an IC production overview rather than rewriting cleanroom material as a home lab.

## Respect tool, PDK, and public-material boundaries

- Choose one digital implementation path whose public conditions you can meet. Freeze RTL, tests, timing/power constraints, educational PDK, and tool versions, retaining every difference introduced when migrating an old flow.
- Use quantum foundations, 6.012, and 6.701 only for the actual gap rather than as three surveys. Do not take 6.884, 6.374, and ECE 4740 for the same digital-layout problem.

## Stop before tapeout language begins

- Skip signoff claims when an authorized PDK, commercial EDA, or supporting files are unavailable. A public educational flow is not foundry signoff.
- Device parameters, process assumptions, RTL regression, synthesis/timing/power, and layout checks trace to one version, and every model substitution triggers the relevant regression.
- Layout completes DRC/LVS and available parasitic analysis only for the stated educational rules. Without fabrication and silicon measurement, stop at the educational flow and make no tapeout claim.

## How to proceed

### Waves and quantum preparation

**Why these courses:** 8.04 formally follows 8.03, so use 8.03SC first for waves, complex amplitudes, boundary conditions, and Fourier representations. Equivalent preparation can be demonstrated with course problems; otherwise complete the units that affect quantum and device models.

- [Physics III: Vibrations and Waves](../courses/physics/012-8-03sc.md) — **Required**; MIT

**Move on when:** Derive and numerically recompute one boundary-value wave eigenproblem. Eigenvalues and normalization error must converge under mesh refinement, with the connection to the later quantum energy-level model explained.

### From bands to a compact model

**Why these courses:** ECE 3150 and 6.012 connect device physics to circuit models, ECE 4070 supplies semiconductor physics, and 6.004 supplies the logic-design background needed by the later digital VLSI path. Add one course for the actual gap: 8.04 for quantum foundations or 6.701 for nanoscale transport; they are not interchangeable device surveys.

- [Quantum Physics I](../courses/physics/013-8-04.md) — **Choose 1**; MIT
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **Required**; Cornell University
- [Microelectronic Devices and Circuits](../courses/microelectronics/030-6-012.md) — **Required**; MIT
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **Required**; MIT
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **Required**; Cornell University
- [Introduction to Nanoelectronics](../courses/semiconductor-devices/125-6-701.md) — **Choose 1**; MIT

**Move on when:** Derive device I–V/C–V behavior from band and transport assumptions, then extract compact-model parameters from public or simulated data. Before fitting, state the allowed error from data resolution, noise, or solver accuracy. Report normalized RMSE over a held-out bias interval and mark where the model begins to fail.

### Turn the device into a process flow

**Why these courses:** Translate the compact model, bias range, and device assumptions into critical dimensions, process targets, and tolerances. Use 6.152J for the common microfabrication foundation, then choose 6.777J only for a genuinely MEMS device, memsX for a systematic fabrication sequence, or NPTEL for an IC production-line overview. Independent study remains simulation and case analysis, not permission to create a home cleanroom. Chemicals, vacuum, high temperature, and fabrication equipment belong only in compliant facilities under qualified supervision.

- [Micro/Nano Processing Technology](../courses/fabrication-mems/126-6-152j.md) — **Required**; MIT
- [Micro and Nanofabrication (MEMS)](../courses/fabrication-mems/127-memsx.md) — **Choose 1**; EPFL
- [Basic Overview of Semiconductor Device Processing and IC Fabrication](../courses/fabrication-mems/128-108104865.md) — **Choose 1**; IIT Kanpur / NPTEL
- [Design and Fabrication of Microelectromechanical Devices](../courses/fabrication-mems/129-6-777j.md) — **Choose 1**; MIT

**Move on when:** Draw the mask layers, device cross sections, and step-by-step process flow, and state a sourced tolerance for every critical dimension that affects performance or yield. Use design-rule checks and an FMEA to identify dominant failure mechanisms, and quantify the yield sensitivity to at least one process variable.

### From transistors to digital layout

**Why these courses:** Each of these three paths has a real limitation, so open the materials and tools before choosing. For anonymous self-study, prefer 6.884: its notes, laboratories, and code are public, but the old standard-cell assumptions and commercial EDA flow must be translated to versioned modern tools. Choose 6.374 only with lawful access to the text or historical material; its public archive lacks video and a complete lecture-note sequence, and the proprietary 2003 flow is a historical case rather than a current recipe. Choose ECE 4740 only when commercial EDA, all 5 public laboratories, and supporting files are available, noting that solutions and the final project are absent. EECS 151 is useful for the current curriculum and public exams, but a teaching site behind CalNet is not an executable path. Whichever path is chosen, retain the device parameters, process rules, masks, and tolerances from earlier work; without an authorized PDK, limit every conclusion to the named educational process.

**Complete path — Public archive path (MIT 6.884) (take these in the listed order)**

1. [Complex Digital Systems](../courses/vlsi-ic/049-6-884.md) — **Course in this path**; MIT

**Complete path — Archived transistor-design path (MIT 6.374) (take these in the listed order)**

1. [Analysis and Design of Digital Integrated Circuits](../courses/vlsi-ic/050-6-374.md) — **Course in this path**; MIT

**Complete path — Commercial-tool laboratory path (Cornell ECE 4740) (take these in the listed order)**

1. [VLSI Systems](../courses/vlsi-ic/051-ece-4740.md) — **Course in this path**; Cornell University

- [Digital Design and Integrated Circuits](../courses/vlsi-ic/044-eecs-151.md) — **Use if needed**; University of California, Berkeley

**Move on when:** Complete the specification, RTL, verification, and implementation of a synthesizable digital block. Regression must show zero mismatches, timing must close under the target constraints, and the results must include area, a power estimate, and one design tradeoff genuinely driven by the specification.
