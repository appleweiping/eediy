---
title: "Engineering Mathematics"
description: "Calculus, linear algebra, differential equations, complex variables, and numerical reasoning for modeling across EE."
page_type: track
track_id: "track-mathematics"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 907a4ea5d5b398c8 -->

# Engineering Mathematics

## Track position

Calculus, linear algebra, differential equations, complex variables, and numerical reasoning for modeling across EE.

## Recommended prerequisite tracks

- None

## Four foundation courses form a translation table, not four successive gates

The [official course page](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/) for [18.01SC](001-18-01sc.md) develops single-variable rates and accumulation. [18.02SC](002-18-02sc.md) carries them into multivariable geometry, vector fields, and integration. [18.03SC](003-18-03sc.md) expresses evolution through differential equations, while the [official course page](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/) for [18.06SC](004-18-06sc.md) supplies vector spaces, linear maps, least squares, and eigenmodes. EE repeatedly translates among a physical description, continuous equation, matrix, and plot; it does not use four isolated viewing lists. A first pass normally begins with 18.01SC and 18.02SC. 18.06SC can overlap once basic integration is secure, and 18.03SC need not wait for all multivariable material. Public problem sets and exams locate units that cannot yet be derived, sketched, or checked independently.

## The next engineering object determines where 18.02, 18.03, and 18.06 meet

Electromagnetics places gradients, divergence, and line or surface integrals from 18.02SC on a two- or three-dimensional potential. Signals and control place linear ODEs and Laplace transforms from 18.03SC beside eigenvalues and orthogonal projection from 18.06SC in one state equation. An order 2 RLC makes a useful paper check: derive its ODE and initial conditions, form the state matrix, obtain eigenmodes, and explain why underdamped, critical, and overdamped cases agree between the time trace and eigenvalue plane. For a two-dimensional electrostatic potential, sketch the integration domain, boundary orientation, and units before discretizing it. A basis change alters coordinates rather than the physical answer.

Each derivation receives an independent challenge from units, a limit, symmetry, a known special case, or a small numerical calculation. Symbolic software may simplify and a numerical library may solve, but one script should not manufacture both the reference and the quantity under test. Inability to state initial or boundary conditions indicates a modeling gap rather than a matrix-algorithm gap. An operator stored as an array but unexplained in terms of a basis means that the 18.06SC connection is still missing.

## 18.04, 18.065, and 6.055J address obstacles that have already appeared

[18.04](005-18-04.md) becomes useful when an AC circuit, frequency-domain method, or two-dimensional field needs residues, conformal maps, or harmonic functions. Its public package has no lecture video, and apart from an application it can become detached symbolic technique. [18.065](009-18-065.md) extends linear algebra toward data, signals, and optimization rather than replacing the spaces and maps of 18.06SC. Its public assignments have no solutions and the final-project package is incomplete, so hand-sized cases, an independent implementation, and known special cases provide checks. [6.055J](018-6-055j.md) teaches dimensions, scaling, and approximation and works best inside a device, thermal, or circuit problem. Read 18.04 for a two-dimensional potential, 18.065 for large matrices or data methods, and 6.055J whenever an order-of-magnitude decision appears.

## Give one EE model analytic, approximate, and numerical versions

Choose an object that will recur later: an RLC network, two-dimensional electrostatic potential, discrete state estimator, or heat-diffusion model. State physical assumptions and continuous equations, then produce a matrix representation, an analytic or semi-analytic prediction, and a rerunnable numerical implementation. Sweep at least three scales or parameter regions and compare conditioning, discretization error, and the valid range of the approximation. If complex variables or a matrix method are used, explain what they achieve over direct integration, time stepping, or scalar calculation and include a counterexample where the method is inappropriate.

A reader should be able to trace a plot back to its equation, basis, boundary conditions, parameters, and units. Preserve one parameter region where the analytic approximation begins to fail. Locate the cause through conditioning, discretization error, or a residual, then show whether changing basis, refining the grid, or returning to the continuous equation repairs it. That counterexample states when the mathematical representation is adequate and when it must change.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Single Variable Calculus](001-18-01sc.md) | MIT | Main course | Public-material guide | Partial or restricted |
| [Multivariable Calculus](002-18-02sc.md) | MIT | Main course | Public-material guide | Partial or restricted |
| [Differential Equations](003-18-03sc.md) | MIT | Main course | Public-material guide | Partial or restricted |
| [Linear Algebra](004-18-06sc.md) | MIT | Main course | Public-material guide | Partial or restricted |
| [Complex Variables with Applications](005-18-04.md) | MIT | Alternative | Public-material guide | Public assignments or labs |
| [Matrix Methods in Data Analysis, Signal Processing, and Machine Learning](009-18-065.md) | MIT | Alternative | Public-material guide | Partial or restricted |
| [The Art of Approximation in Science and Engineering](018-6-055j.md) | MIT | Supplement | Public-material guide | Public assignments or labs |
