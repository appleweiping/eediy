---
title: "Solar Energy Engineering: Photovoltaic Energy Conversion"
description: "Delft University of Technology's Solar Energy Engineering: Photovoltaic Energy Conversion builds a photovoltaic-conversion spine from videos, notes, practice, labs, and code, with a matching TU Delft open-course entry, public videos, and notes while edX audit and certificate access remain limited."
page_type: course
course_id: "course-122"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-29"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 74bc3d02002dec52 -->

# Delft University of Technology PV Energy Conversion: Solar Energy Engineering: Photovoltaic Energy Conversion

## Course Overview

- **University:** Delft University of Technology
- **Course code:** PV Energy Conversion
- **Official prerequisites:** No provider-published hard prerequisite verified; recheck the course page
- **EEDIY preparation:** Semiconductor Devices; Circuit Analysis; Engineering Mathematics
- **Access:** Open entry; some materials require registration or are limited
- **Material status:** 2026-07-29; public-material guide

### Course fit

TU Delft [Photovoltaic Energy Conversion](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion/) moves from irradiance, semiconductor physics, and the illuminated p-n junction to heterojunctions, light management, external quantum efficiency, the Shockley–Queisser limit, and third-generation concepts. The provider divides it into Modules 1–8 and lists a 121-hour study load. It explains a cell’s \(I\!-\!V\) curve and efficiency; module wiring, partial shading, MPPT, inverters, batteries, and grid integration belong to [Photovoltaic Systems](https://ocw.tudelft.nl/courses/solar-energy-photovoltaic-pv-systems/).

Before Module 2, try 4 checks: derive carrier concentration from density of states and Fermi level; state the units in drift, diffusion, and continuity; draw dark and illuminated junction band diagrams; and explain a generation profile from absorption coefficient and thickness. Review semiconductor physics if the first 2 fail, junction electrostatics for the 3rd, and basic optics for the 4th. This is a study placement test, not an official prerequisite.

### Access and version notes

OCW [Lectures](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion/?view=lectures) preserves videos for 8 modules, while [Readings](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion/?view=readings) lists only 4 entries: Module 1, 2, 6, and 8. Course material is marked CC BY-NC-SA 4.0, but embedded video, images, and external material retain their own notices.

The [official edX Assignments and course entry](https://www.edx.org/learn/solar-energy/delft-university-of-technology-solar-energy-photovoltaic-pv-energy-conversion) handles sessions, discussion, graded work, and certificates; anonymous pages do not establish what a current region and account can access. The official [audit explanation](https://edxsupport.zendesk.com/hc/en-us/articles/1500003964681-What-is-the-audit-track) says that audit access, when offered, is normally temporary, excludes graded assignments and certificates, and is not guaranteed for every course. The open route should therefore rely on OCW and independent checks, without claiming access to the edX grader.

### Add Recombination, Transport, and Losses to the Cell Model Week by Week

Modules 1–4 connect photon flux to drift-diffusion, generation/recombination, and the illuminated junction. Maintain a conservation sheet with consistent units for optical input, bulk/surface recombination, and terminal current. Module 5 introduces metal-semiconductor junctions and heterojunctions. Modules 6–7 treat refraction, dispersion, diffraction, scattering, and EQE; keep absorptance, collection probability, and internal/external quantum efficiency distinct. Module 8 closes a cell-level loss budget that identifies bandgap, radiative/non-radiative recombination, optical loss, series/shunt effects, and temperature.

For numerical practice, start with a dark diode and illuminated \(I\!-\!V\), then add recombination and optical loss before sweeping irradiance, temperature, series resistance, and thickness. Preserve each earlier model as a baseline. Recover the dark curve at 0 irradiance; inspect the limits as series resistance approaches 0 and shunt resistance increases; record units, grid sensitivity, and data provenance for spectral integration. Label parameters as synthetic when no public data is available.

### One loss budget connects the conversion losses

The exit package should contain derivations, a versioned notebook, raw tables, and an environment file, and should explain changes in short-circuit, open-circuit, maximum-power point, and EQE. The notebook is an independent exercise, not a TU Delft lab or official assignment.

The course is especially good for turning each physical loss into an explainable, falsifiable model.

Keep this route at low-energy computation. Cell fabrication involves chemicals, vacuum, high temperature, and cleanroom controls; modules and arrays add persistent DC, arcing, stored energy, and grid hazards. Move to PV Systems if the remaining questions concern inverter sizing, shading, or daily energy. Stay here for materials, junctions, passivation, light trapping, and efficiency limits.

## Course Resources

- [Course home](https://www.edx.org/learn/solar-energy/delft-university-of-technology-solar-energy-photovoltaic-pv-energy-conversion)
- [Alternate course entry](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion)
- [Notes · Course readings](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion?view=readings)
- [Videos · Video lectures](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion?view=lectures)

## Resource Summary

Every public entry point verified in this review is listed above. Use the feedback and corrections links below to submit a completion record, another resource, or a broken-link report.
