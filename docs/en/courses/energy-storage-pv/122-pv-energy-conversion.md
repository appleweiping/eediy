---
title: "Solar Energy Engineering: Photovoltaic Energy Conversion"
description: "Delft University of Technology's Solar Energy Engineering: Photovoltaic Energy Conversion builds a photovoltaic-conversion spine from videos, notes, practice, labs, and code, with a matching TU Delft open-course entry, public videos, and notes while edX audit and certificate access remain limited."
page_type: course
course_id: "course-122"
editorial_status: "researched"
evidence_level: "R0"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 33400200bbec95bc -->

# Solar Energy Engineering: Photovoltaic Energy Conversion

## Course Overview

- **University:** Delft University of Technology
- **Course code:** PV Energy Conversion
- **Prerequisites:** Recommended foundation: Semiconductor Devices; Recommended foundation: Circuit Analysis; Recommended foundation: Engineering Mathematics
- **Track:** [Energy Storage and Photovoltaics](index.md)
- **Path role:** Mainline
- **Public materials:** Core materials available
- **Last reviewed:** 2026-07-29

> **Desk-researched (R0):** The official course materials were checked item by item on 2026-07-29, but no traceable full-course report has been accepted. This guide therefore makes no first-hand claims; completers can submit a report below.

## Separate the Solar Cell, PV Module, and PV System First

TU Delft's open [Photovoltaic Energy Conversion page](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion/)
is organized around the solar cell. It moves from irradiance and the
photovoltaic effect through semiconductor physics, generation and
recombination, the illuminated p-n junction, heterojunctions, light
management, external quantum efficiency, the Shockley–Queisser limit,
additional losses, and third-generation concepts. The provider divides the
material into Modules 1–8 and publishes a 121-hour study load. That is a
provider description of course scale, not an EEDIY promise about every
learner's time.

The course answers why a cell has a particular \(I\!-\!V\) curve and
efficiency. It does not fully teach module wiring, partial shading, MPPT,
inverters, batteries, grid integration, or plant economics. TU Delft's
separate [Photovoltaic Systems course](https://ocw.tudelft.nl/courses/solar-energy-photovoltaic-pv-systems/)
explicitly moves from cells to modules and then to residential or
utility-scale systems. A system-integration learner can use this course to
build the cell model and then move to the systems course. “Energy Conversion”
in the title is not evidence that the downstream system layer is already
covered.

Before Module 2, try 4 actions: explain carrier concentration from density of
states and Fermi level; write the units in drift, diffusion, and continuity;
draw dark and illuminated p-n-junction band diagrams; and explain from
absorption coefficient and thickness why photogeneration varies with depth.
Review semiconductor physics when the first 2 fail, junction electrostatics
when the 3rd fails, and basic optics when the 4th fails. This placement
exercise is an EEDIY recommendation, not a TU Delft prerequisite threshold.

## Split the Open-Material and edX-Feedback Routes on Day One

TU Delft OCW's [Lectures index](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion/?view=lectures)
preserves public videos across 8 paginated modules. Its
[Readings index](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion/?view=readings)
lists only 4 reading entries, for Modules 1, 2, 6, and 8. “Readings are
present” must not become “every module has a complete open textbook chapter.”
The course page and its material state a CC BY-NC-SA 4.0 license, while
embedded videos, images, and external material still require their own rights
check. The license permits compliant reuse and adaptation; it does not
automatically relicense every third-party item.

The official [edX assignments and grader access entry](https://www.edx.org/learn/solar-energy/delft-university-of-technology-solar-energy-photovoltaic-pv-energy-conversion)
handles registration, sessions, discussion, graded work, and the certificate
route. Its anonymous content changes with region, session, and login state.
This review could not derive a durable assignment or exam inventory from the
anonymous HTML, so it does not claim that OCW exposes the edX grader. edX's
official [audit explanation](https://edxsupport.zendesk.com/hc/en-us/articles/1500003964681-What-is-the-audit-track)
says that an audit, when offered, is temporary, generally excludes graded
assignments, and earns no certificate; an audit is not guaranteed for every
course. At enrollment, record the actual session, expiry, and visible items
instead of publishing one price that will quickly become false.

There are therefore 2 honest completion routes. The open route uses OCW
videos, the 4 readings, and learner-built checks. It has stable entries and a
clear license, but no public graded-feedback loop. Use the edX route only when
an account actually displays an enrollable session, and record exactly which
problems, discussions, or certificate features it provides. A feature once
offered in a paid track is not evidence that every region and session offers
it now.

## Upgrade the Same Cell Model Three Times

### From a Carrier Account to the Illuminated p-n Junction

Modules 1–4 connect irradiance, photon flux, and the photovoltaic effect to
equilibrium and non-equilibrium semiconductors, drift-diffusion, generation
and recombination, and the illuminated p-n junction. Do not consume these as
an uninterrupted video playlist. Maintain one conservation sheet that states
the units and signs of optical input, volumetric generation, bulk and surface
recombination, and terminal current. Redraw the minority-carrier profile after
adding each recombination mechanism, and verify that the dark and
zero-generation limits reduce to known cases.

### From Interfaces and Optical Paths to External Quantum Efficiency

Module 5 covers metal-semiconductor junctions and heterojunctions; Modules
6–7 cover refraction, dispersion, diffraction, scattering, and external
quantum efficiency. The common failure here is not integration arithmetic but
treating internal quantum efficiency, external quantum efficiency,
absorptance, and collection probability as the same quantity. Put wavelength,
depth, absorption, and collection on one diagram, then state which term loses
reflection, parasitic absorption, or recombination. One efficiency number
cannot show whether the model conserves anything.

### Let Module 8 Close the Cell Budget and Delay the System Layer

Module 8 treats the Shockley–Queisser limit, additional losses, loss
reduction, and third-generation cell concepts. Its output should be a
cell-level loss budget in which bandgap, radiative and non-radiative
recombination, optical loss, series and shunt effects, and operating
temperature remain visible. Module mismatch, bypass diodes, converters, and
grid interaction belong to the later PV Systems course. If they appear in
this notebook, label them as an EEDIY extension rather than an official Module
8 assignment.

## Make Simulation Produce Falsifiable Evidence without a Public Grader

EEDIY recommends a simulation-only notebook; it is not a TU Delft lab,
assignment, or capstone. Implement a dark diode and illuminated \(I\!-\!V\)
curve, add one recombination mechanism and one optical loss, then sweep
irradiance, temperature, series resistance, and thickness. Preserve the
previous model as a baseline after every added mechanism instead of jumping
straight to an opaque “real solar-cell model.”

Verification must go beyond a plausible-looking curve. Report how
short-circuit, open-circuit, and maximum-power points are solved. Recover the
dark curve at 0 irradiance. Check the limits as series resistance approaches
0 and shunt resistance increases. State wavelength-to-energy conversion and
units in every spectral integral, and change the integration grid to show
that a conclusion is not a step-size accident. When using external optical
constants or EQE data, preserve the raw file, source, license, cleaning
script, and checksum. Use parameters explicitly marked synthetic when no
public dataset is available; do not present them as measurements.

A completion directory can follow the official OCW modules: concept map,
model-upgrade derivations, simulation sources, raw tables, environment lock,
and loss-budget report. An edX learner may append graded work actually visible
through the official entry and a session record; the open route cannot claim
them. Useful feedback reports a region, session, or expiry change without
copying restricted questions, or identifies a failed OCW item.

## End Practice at Low-Energy Computation, Not an Energized Array

The course does not require an outside learner to fabricate a cell, wire a
module, or connect a battery, inverter, or grid. The EEDIY route is
computation and simulation only. Semiconductor processing introduces
chemicals, vacuum, high temperature, and cleanroom controls; modules and
arrays introduce persistent DC voltage, fault arcs, stored energy, and
grid-connection hazards. Rooftops, outdoor arrays, energized DC cable,
battery packs, and mains-connected inverters belong in compliant facilities
or engineering sites with appropriate protection, procedures, and expert
supervision, not a home reproduction.

If the remaining question after a cell loss budget is how to size an inverter,
manage shading, or estimate daily energy, stop this course and move to PV
Systems instead of attaching system parameters to a cell model. Stay here for
materials, junctions, passivation, light trapping, and efficiency limits.
That exit criterion shows the track choice better than watching every public
module, without confusing open content with an open physical laboratory.

## Course Resources

<details markdown="1">
<summary>Expand the complete resource index (4 items)</summary>

### Material coverage

| Type | Completeness |
|---|---|
| Video | Complete |
| Notes | Complete |
| Practice | Partial |
| Labs | Partial |
| Exams | No public material |
| Code | Partial |

### Resource

| Resource | Access | Status | Verified |
|---|---|---|---|
| [Course home](https://www.edx.org/learn/solar-energy/delft-university-of-technology-solar-energy-photovoltaic-pv-energy-conversion) | Free audit | Listed by official page | 2026-07-28 |
| [Alternate course entry](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion) | Open access | Listed by official page | 2026-07-28 |
| [Course readings](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion?view=readings) | Open access | Listed by official page | 2026-07-28 |
| [Video lectures](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion?view=lectures) | Open access | Listed by official page | 2026-07-28 |

> Links were discovered from official sources on the recorded date. Access does not grant redistribution rights, and region, account, third-party rights, or later redesigns may change availability.

</details>
