---
title: "Micro/Nanofabrication and MEMS"
description: "Deposition, lithography, etching, process integration, and MEMS design using process plans and simulation when cleanrooms are unavailable."
page_type: track
track_id: "track-fabrication-mems"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: f41efc617c1e8045 -->

# Micro/Nanofabrication and MEMS

## Track position

Deposition, lithography, etching, process integration, and MEMS design using process plans and simulation when cleanrooms are unavailable.

## Recommended prerequisite tracks

- [Semiconductor Devices](../semiconductor-devices/index.md)
- [Physics Foundations](../physics/index.md)

## 6.152J supplies the process backbone; 6.777J begins MEMS design

[MIT 6.152J](126-6-152j.md) provides the process backbone through oxidation, diffusion, implantation, deposition, lithography, etching, and integration constraints. Its [official assignment page](https://ocw.mit.edu/courses/6-152j-micro-nano-processing-technology-fall-2005/pages/assignments/) lists only Problem Sets 1–8, all with solutions. The separate [exam page](https://ocw.mit.edu/courses/6-152j-micro-nano-processing-technology-fall-2005/pages/exams/) includes a public take-home exam plus quiz questions or solutions from several terms. Do not invent PS9–10 or merge that exam inventory with another course's design problem. [MIT 6.777J](129-6-777j.md) is the course that combines mechanics, electronics, and fabrication in MEMS device design. Its [syllabus](https://ocw.mit.edu/courses/6-777j-design-and-fabrication-of-microelectromechanical-devices-spring-2007/pages/syllabus/) requires seven homeworks, a take-home design problem, and a team final project, while the [public assignment page](https://ocw.mit.edu/courses/6-777j-design-and-fabrication-of-microelectromechanical-devices-spring-2007/pages/assignments/) contains PS1–7, no PS5 solution, and no take-home design prompt. [EPFL memsX](127-memsx.md) is useful for observing CVD, PVD, lithography, wet and dry etching, and metrology, not for operator qualification. The [NPTEL processing overview](128-108104865.md) gives a fast 12-week panorama. For IC cross-section literacy, 6.152J plus selected memsX or NPTEL material is enough. Add 6.777J only when a membrane, cantilever, or resonator becomes the design object.

## Consecutive cross-sections are the real unit of study

Connect junctions, MOS capacitors and MOSFETs, doping, and carrier behavior from [semiconductor devices](../semiconductor-devices/index.md) with diffusion, thermal processes, mechanics, and scaling from [physics](../physics/index.md). Choose a planar diode or cantilever, draw the starting wafer, and then draw 3 to 5 consecutive cross-sections. At every step name the material added, removed, or doped; temperature range; critical dimension; interface; observable; and effect on the final electrical or mechanical quantity. If dose, concentration, film thickness, sheet resistance, and stress units are confused, repair units and device physics first. A polished final shape is not enough when release, mask alignment, and thermal budget cannot explain how it was reached or whether 6.777J is yet appropriate. Fabrication literacy is about sequence and compatibility, not a vocabulary list of tools.

## Simulation and layout tools stop at the cleanroom door

KLayout, gdsfactory, and Python or Jupyter can produce masks, sequential cross-sections, parameter sweeps, and tolerance studies. They are excellent for finding incompatible material order, an unreleased structure, or an unmeasurable step on paper. Public course packages do not provide facility admission, tool qualification, approved recipes, an official wafer traveler, contamination rules, raw metrology data, or waste procedures. Advanced memsX access may also be paid, and NPTEL has no physical experimental loop. Vacuum, high temperature, plasma, implantation, specialty gases, photoresist chemistry, and wet etchants belong in controlled facilities under trained supervision; a video must never be reverse-engineered into a home recipe. Label each numerical value as course-derived, current primary-source data, or a teaching assumption, and do not fill missing pages from unauthorized slide mirrors.

## One virtual flow should answer one device question

Choose a measurable objective for a MEMS membrane, cantilever, interdigitated capacitor, or simplified CMOS or diode structure. Produce its mask list, consecutive cross-sections, thermal budget, contamination compatibility, critical dimensions, and the quantities to be measured at 2 points in the flow. Run a sensitivity or Monte Carlo study on lithography bias, etch bias, film stress, oxide thickness, or implant dose, connecting the variation to resonance, capacitance, sheet resistance, or threshold. Put one accepted and one rejected process branch side by side and mark the first step at which material order, release, thermal budget, or metrology makes them differ. If that step changes junction, threshold, or yield, hand the same cross-sections to process integration; if it changes a structural mode, transduction, or control interface, hand them to MEMS design. Without institutional facilities, both conclusions remain tests of internal consistency under stated assumptions, not claims of operating a tool.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Micro/Nano Processing Technology](126-6-152j.md) | MIT | Main course | Public-material guide | Partial or restricted |
| [Design and Fabrication of Microelectromechanical Devices](129-6-777j.md) | MIT | Main course | Public-material guide | Partial or restricted |
| [Micro and Nanofabrication (MEMS)](127-memsx.md) | EPFL | Alternative | Public-material guide | Partial or restricted |
| [Basic Overview of Semiconductor Device Processing and IC Fabrication](128-108104865.md) | IIT Kanpur / NPTEL | Supplement | Public-material guide | Partial or restricted |
