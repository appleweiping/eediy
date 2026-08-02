---
title: Numerical Computing and Model Credibility
description: Use an RLC model to practice scaling, tolerances, convergence, and independent comparison—and separate solver success from a credible result.
page_type: guide
comments: true
---


# Numerical Computing and Model Credibility

A solver returning `success` means that it completed according to its own rules. It has not shown that the differential equations are correct, the units agree, or the fastest dynamics are resolved. It certainly has not shown that the model represents the circuit on the bench. Credible numerical work separates model error, discretization error, floating-point effects, parameter uncertainty, and physical discrepancy.

A series RLC step response is enough to expose all of them. With the state \(x=[i,\ v_C]\), write
\[
\frac{di}{dt}=\frac{v_s-Ri-v_C}{L},\qquad
\frac{dv_C}{dt}=\frac{i}{C}.
\]
The initial slope, steady state, poles, and direction of energy flow can be checked by hand. The same model can also be made stiff, badly scaled, or under-sampled on purpose. Make this small calculation trustworthy before transferring the habits to a field solver, controller, or device model.

## Before execution, state the physical facts that may not be violated

Give every quantity an SI unit and a plausible scale, and state initial conditions, stimulus, sign convention, and boundaries. For a DC step from zero state, inductor current cannot jump instantaneously. At long-time steady state, capacitor current should approach zero. In a passive circuit with \(R>0\), stored energy cannot grow forever without supplied power. Derive the poles from \(L\), \(C\), and \(R\) and decide whether the response should be overdamped, critical, or oscillatory. A smooth curve that violates one of these facts is not ready for tolerance tuning.

Reduce the engineering question to a few scalars: peak current, overshoot, 2% settling time, and perhaps
\[
\Delta E = E(t)-E(0)-\int_0^t\!\bigl(v_s i-Ri^2\bigr)\,dt.
\]
Such quantities reveal errors more reliably than comparing plot pixels and can become tests. If parameters come from measurements, preserve their source and uncertainty. NIST [Technical Note 1297](https://www.nist.gov/pml/nist-technical-note-1297) describes evaluation, combination, and reporting of measurement uncertainty. It addresses how well the inputs are known; it does not estimate the discretization error of an algorithm.

## Make one solver disagree with itself on purpose

Run the same parameters through a sequence of stricter configurations instead of changing one step size and declaring the curves “close enough.” The SciPy [`solve_ivp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html) documentation distinguishes `t_eval`, which selects stored output times, from `rtol`, `atol`, and `max_step`, which affect integration. A denser plot is not necessarily a more accurate integration. Begin with a suitable default, tighten tolerances in stages, and limit the maximum step so the fastest expected time scale can be represented.

At each level, record function evaluations, peak value, settling time, and energy residual. Plot the change in each target quantity relative to the strictest run rather than only overlaying waveforms. Then use at least one independent comparison: analytical poles, a frequency-domain transfer function, or an integrator with different numerical properties. The `solve_ivp` documentation recommends explicit Runge–Kutta methods for non-stiff problems and implicit methods such as Radau or BDF for stiff ones. Agreement across method families says more than an extremely small tolerance in one method.

A convergence study should record spatial-grid and time-step refinement separately, while asking the same central question: does a target quantity approach a stable asymptotic trend as the discretization is refined? Do not apply Richardson extrapolation mechanically to every solver. Discontinuities, missed events, or runs outside the asymptotic range can produce a meaningless apparent order. For the RLC exercise, an effective refinement study has several levels pointing toward the same limit while independent physical checks improve as well.

## If refinement still wanders, classify the failure

Tighter tolerances producing noisier answers do not automatically mean “the computer lacks precision.” Check units and state scales first. If one state is near \(10^{-9}\) and another near \(10^3\), one absolute tolerance has very different meanings for them. Check stiffness and discontinuous inputs next, including whether an event or switch transition can be crossed inside one large step. Only then examine rounding and cancellation. Python's official [floating-point explanation](https://docs.python.org/3/tutorial/floatingpoint.html) shows why most decimal fractions have no exact binary floating-point representation, but that fact is not a universal excuse for numerical discrepancies.

For a sensitive linear solve or parameter fit, inspect singular values and conditioning. NumPy [`linalg.cond`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.cond.html) computes a matrix condition number under a selected norm. A large value warns that input perturbations may be amplified; it does not automatically declare the physical model wrong. Rescale variables, avoid an unnecessary explicit inverse, ask whether parameters are identifiable, and use synthetic data to test recovery of a known answer.

Different failures call for different next steps:

- **Model error:** every discretization setting converges to the same wrong physical trend.
- **Discretization error:** the target quantity moves systematically with mesh or step refinement.
- **Rounding or conditioning:** scaling, precision, or algorithm choice changes the answer substantially.
- **Input uncertainty:** the algorithm has converged, but the permitted parameter range changes the engineering decision.

The classification matters because it tells you whether to change the equations, change the algorithm, measure a parameter, or narrow the claim.

## The final comparison must leave this program

For the RLC model, compare dynamics with hand-derived poles and DC limits, then with a frequency-domain result from another tool or a safe low-voltage measurement. When measured and computed curves disagree, do not immediately call the gap “simulation error.” Probe loading, source impedance, parasitics, component tolerance, and instrument bandwidth may all be physical quantities missing from the model. Add them one at a time and see which one actually explains the discrepancy.

Retain equations, units, parameter sources, solver and version, tolerances, the refinement table, independent benchmark, residual definition, and one rebuild command. Reported digits should be limited jointly by numerical convergence and input uncertainty. If a model will influence operating boundaries for power supplies, motors, RF transmission, or medical equipment, computation may propose tests; it cannot replace ratings, fault protection, qualified personnel, or supervised validation.

Once the RLC result rebuilds in a clean environment and deliberate changes to units, step size, or damping cause intelligible failures, move to [SPICE Circuit Simulation](spice-simulation.md) for device models or connect measurements through [Data and Laboratory Records](data-lab-notebooks.md).
