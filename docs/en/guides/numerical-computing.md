---
title: Numerical Computing and Model Verification
description: Decide whether an EE numerical result is trustworthy with scaling, convergence checks, and independent benchmarks.
---

<div class="ee-language" markdown>
[简体中文](../../guides/numerical-computing.md)
</div>

# Numerical Computing and Model Verification

A numerical tool can produce an attractive result without deciding whether the model applies. Reliable computation must answer what the equations represent, how large discretization error is, whether parameters are identifiable, and whether an independent method confirms the result.

## Purpose and learning outcomes

- Check a model with dimensions, order of magnitude, and limiting cases before solving.
- Recognize conditioning, discretization error, roundoff, and stopping criteria.
- Use mesh or step convergence to show that a result is not a plotting-resolution artifact.
- Compare against analysis, a hand-solvable case, and an independent numerical method.
- Report uncertainty instead of unsupported significant digits.

## Minimal environment

- Any numerical environment with arrays, linear algebra, and plotting.
- Plain-text scripts, parameter files, and a test entry point.
- One small problem that can be solved by hand.
- An optional notebook for explanation, but not as the only execution path.

Record observed tool versions, solver options, and relevant hardware differences. Defaults can vary by implementation, so set critical tolerances explicitly and justify them.

## Learning sequence

1. **Scale the problem:** list variable units, select reference scales, and identify dimensionless groups.
2. **Build a benchmark:** solve an analytical or hand-checkable small instance first.
3. **Separate errors:** distinguish model, data, discretization, and floating-point error.
4. **Run convergence:** reduce time step, frequency spacing, or spatial mesh and track a target quantity.
5. **Test sensitivity:** perturb parameters and initial conditions to see whether the conclusion is robust.
6. **Cross-check independently:** use another algorithm, conservation law, or limiting case.

## Verification task: integrate an RLC state model

Build a state-space model of a damped RLC system:

1. Derive the initial slope, steady value, and expected oscillation or decay regime.
2. Integrate the same excitation with at least three time steps.
3. Record peak value, steady value, and energy residual.
4. Plot target-quantity error relative to the finest step.
5. Vary one component within a tolerance range and compute local sensitivity.
6. Cross-check the dynamics with a frequency-domain result or analytical poles.

Acceptance requires convergence of the target quantity, the correct conservation or dissipation direction, and a statement of how sensitive the conclusion is to tolerance.

## Common failures and diagnosis

- **The matrix solves but results jump:** inspect conditioning, variable scales, and near-linear dependence.
- **A smaller step diverges:** check algorithm stability, stiffness, units, and implementation.
- **A smooth curve is physically wrong:** verify signs, initial values, boundary conditions, and power direction.
- **Only “solver succeeded” is reported:** define a residual and acceptance quantity tied to the physical question.
- **Too many significant digits:** limit precision by input uncertainty and convergence error.
- **A random sweep cannot be replayed:** fix the seed and retain distributions and ranges.

## Reproducible evidence

- Equations, assumptions, units, and reference scales.
- Parameter provenance, ranges, and uncertainty.
- Solver, tolerances, step sizes, and stopping criteria.
- Benchmark results compared with analysis or hand calculation.
- Convergence table, sensitivity plot, and residual definition.
- One command that generates all results.
- Failure cases and domain of validity.

## Cost, licensing, and accessibility

Free numerical environments are sufficient. A commercial platform may support course compatibility, but export scripts, parameters, and standard-format results. Record solver and data licenses and do not redistribute restricted models.

Use line styles, markers, and direct labels in addition to color. Provide key values in a table and state conclusions in text. A low-performance device may use a smaller mesh but should still demonstrate a three-point convergence trend.

## Safety boundaries

- A passing simulation does not establish hardware safety; ratings, faults, and protection need independent review.
- Do not use an unvalidated extrapolation to set higher-energy operating limits.
- Separate numerical instability from physical instability through step studies and independent methods.
- Medical, power, RF-transmission, or actuator-control conclusions need qualified review.
- Never conceal nonconvergence, nonphysical negative values, or violated conservation.

## Completion checklist

- [ ] Equations, units, assumptions, and boundary conditions are recorded.
- [ ] At least one benchmark has an independent answer.
- [ ] A convergence study uses three or more steps or meshes.
- [ ] Residuals and stopping criteria relate to the physical objective.
- [ ] Parameter sensitivity and input uncertainty are assessed.
- [ ] Plots, tables, and prose state a consistent conclusion.
- [ ] One command rebuilds the result.
- [ ] Domain of validity and safety limits are explicit.

Next, practice device models with [SPICE Circuit Simulation](spice-simulation.md), or compare against measurements with [Data and Laboratory Records](data-lab-notebooks.md).
