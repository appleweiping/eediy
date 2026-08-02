---
title: "Electromagnetic Fields and Waves"
description: "Maxwell equations, boundaries, transmission lines, waveguides, and radiation for RF, photonics, and high-speed interconnects."
page_type: track
track_id: "track-electromagnetics"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: a685b08729cc4c1f -->

# Electromagnetic Fields and Waves

## Track position

Maxwell equations, boundaries, transmission lines, waveguides, and radiation for RF, photonics, and high-speed interconnects.

## Recommended prerequisite tracks

- [Engineering Mathematics](../mathematics/index.md)
- [Physics Foundations](../physics/index.md)

## ECE 3030 corrects boundaries through problems; 6.013 organizes equations through systems

The [official Cornell ECE 3030 archive](https://ocw.ece.cornell.edu/courses/ece-3030-electromagnetic-fields-and-waves-2) gives [ECE 3030](107-ece-3030.md) 36 handout groups, 12 solved homework sets, and 4 solved exams. The current Cornell catalogue lists PHYS 2213, MATH 2930, and ECE 2100 as prerequisites; the public teaching archive itself is the Fall 2007 version, so current catalogue requirements and archived materials should not be presented as one offering. It suits a learner who can rebuild derivations from text and wants many paper problems to correct boundary-condition errors. The [official MIT 6.013 page](https://ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009) uses an open text, examples, demonstrations, and exams to connect electrostatics, magnetics, waves, transmission, and applications. Its syllabus expects 18.01/18.02, 8.01/8.02, 6.002, and 6.00, with Fourier methods used in the course. [6.013](108-6-013.md) more readily shows field equations entering devices and systems, but it also lacks a complete lecture-video sequence.

Either course can be the first spine; choose by reading style and application interest rather than repeating the same Maxwell foundation. [MIT 6.630](109-6-630.md) contributes a simulation video, MATLAB files, problems, and exams, while its reading and teaching indexes are partial. It is best used after the spine for numerical fields or a named topic.

## Move from flux and boundaries to a numerical model with an analytic limit

[Engineering mathematics](../mathematics/index.md) should supply multivariable calculus, vector analysis, ODEs, complex phasors, and boundary-value language. [Physics foundations](../physics/index.md) should supply electrostatics, magnetic induction, material response, and energy. For a simple vector field, calculate grad, div, and curl and draw direction, area element, normal, and flux. Then solve a symmetric problem through both Coulomb and Gauss reasoning and carry one \(e^{j\omega t}\) convention through phase, Poynting power, and material loss.

Choose a coaxial or microstrip line, rectangular waveguide, dielectric interface, or electrostatic sensor and define geometry, materials, source, boundaries, and requested quantities. Derive one soluble limit, then run a parameter sweep and mesh-refinement study. Compare field continuity, Poynting power, stored energy, reflection, or propagation constant and apply an independent conservation or reciprocity check. Coordinate substitution with no geometry calls for vector work; a memorized boundary unsupported by Maxwell equations and constitutive relations calls for physics.

Whenever the coordinate system changes, draw the differential lengths, surface element, and normal before choosing the integration range from symmetry. At a material interface, write tangential and normal conditions separately and state whether free charge or surface current is present. Those steps expose missing scale factors, reversed normals, and material parameters before a solver can hide them.

ECE 3030 is a 2007 text release, a 6.013 demonstration is not a reproducible RF laboratory, and the MATLAB interface in 6.630 is dated. A port to Python, Julia, or current MATLAB states equations, grid, boundaries, solver tolerance, and convergence. Every field map needs its mesh, domain truncation, material parameters, and an energy or flux residual. Attractive colors do not replace an analytic limit and mesh convergence.

When analytic and numerical results disagree, inspect units, source normalization, phase convention, and the location of the artificial boundary before changing the mesh or solver. Numerical differences become interpretable only after those physical conditions match.

## The path by which energy leaves the model chooses the next branch

Energy propagating along a transmission line or waveguide points toward microwaves. Radiation, far field, matching, and arrays point toward antennas and RF. Material dispersion, device geometry, and modes point toward photonics or devices. A target of baseband, channels, and coding connects the field and RF front end to [communication systems](../communications/index.md). The reason for moving should name the approximation that has begun to break in the current model.

The default project scope is analysis and simulation. Low-power transmission-line, waveguide, or antenna hardware requires fresh checks of regulation, instruments, and risk. Independent work excludes mains, high voltage, strong RF radiation, and unknown microwave sources. Cite material constants and frequency ranges and identify perfect-conductor (PEC), lossless-medium, far-field, and infinite-boundary assumptions. The final explanation should say where energy enters, is stored or dissipated, and leaves, while separating Maxwell-equation conclusions from numerical approximations.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Electromagnetic Fields and Waves](107-ece-3030.md) | Cornell University | Main course | Public-material guide | Public assignments or labs |
| [Electromagnetics and Applications](108-6-013.md) | MIT | Main course | Public-material guide | Public assignments or labs |
| [Electromagnetics](109-6-630.md) | MIT | Supplement | Public-material guide | Partial or restricted |
