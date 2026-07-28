---
title: SPICE Circuit Simulation
description: Build reviewable circuit evidence from hand-calculated benchmarks through tolerance and corner analysis.
---

<div class="ee-language" markdown>
[简体中文](../../guides/spice-simulation.md)
</div>

# SPICE Circuit Simulation

SPICE describes a family of circuit solvers and netlist conventions, not one interface. Learn topology, models, analysis types, initial conditions, and convergence rather than menu sequences. Start with ideal components, establish a benchmark, and add nonideal models incrementally.

## Purpose and learning outcomes

- Predict a DC operating point, pole, or transient direction before simulation.
- Select the appropriate DC, AC, transient, noise, or parameter analysis.
- Trace device-model provenance, range, and licensing.
- Explain convergence errors instead of blindly loosening tolerances.
- Test design margin with tolerance, temperature, and fault sweeps.

## Minimal environment

- A SPICE-compatible solver that reads text netlists or exports them.
- A text editor and plot/data-export capability.
- Basic R, L, C, and controlled-source models.
- A practice project disconnected from real higher-energy hardware.

Record the observed solver, model-library, and critical-option versions. Do not assume identically named device models are equivalent across distributions.

## Learning sequence

1. **Operating point:** check node voltages and power in a divider and simple bias circuit.
2. **Small signal:** predict cutoff frequency, magnitude, and phase for a first-order network.
3. **Transient:** use finite source rise time, explicit initial conditions, and a long enough observation window.
4. **Parameterize:** centralize component values and run a unit-labeled single-variable sweep.
5. **Audit models:** add device models and record source, temperature range, and omitted effects.
6. **Test robustness:** run tolerance, corner, or Monte Carlo analysis and retain random settings.

## Verification task: two-stage amplifier evidence

Choose a safe small-signal two-stage amplifier or active filter:

1. Estimate DC bias, target gain, and major poles by hand.
2. Simulate the operating point and inspect device power and region of operation.
3. Run AC analysis and extract gain, bandwidth, and phase features.
4. Run a transient with finite rise time and inspect clipping and settling.
5. Sweep critical component tolerances and report the worst case, not only typical.
6. Introduce one connection fault and show that an acceptance check detects it.

Acceptance requires hand analysis and simulation to agree within a declared tolerance, plus an explanation of parasitic, thermal, or layout effects that remain unmodeled.

## Common failures and diagnosis

- **Singular matrix or floating node:** find a DC path and reference for every node.
- **The time step collapses:** inspect ideal switches, discontinuous sources, stiff models, and unrealistic parasitics.
- **AC output is zero:** confirm that the source has a small-signal amplitude.
- **Transient and AC disagree:** check bias, linearization, input amplitude, and initial conditions.
- **A model is missing:** inspect include paths, model name, case, and distribution rights.
- **Only loose tolerances converge:** simplify and isolate the device first; do not treat a numerical symptom as a solution.

## Reproducible evidence

- Schematic source and exported text netlist.
- Solver and model provenance, license, and checksum.
- Parameters, temperature, analysis directives, and initial conditions.
- Hand predictions and numerical acceptance tolerances.
- Parseable raw output and unit-labeled plots.
- Tolerance or corner settings and a failure case.
- One noninteractive batch command.

## Cost, licensing, and accessibility

Free solvers are sufficient for fundamentals. Vendor tools may support a specific model, but retain a standard netlist or readable export. A model license may forbid redistribution; publish its retrieval location and integrity information instead.

Do not upload only waveform screenshots. Provide CSV, measurement-statement results, and textual conclusions; distinguish traces with line styles and labels. A slower device may use fewer sweep points while retaining worst-case logic.

## Safety boundaries

- Models commonly omit some failure, thermal, package, and layout effects.
- Simulated ground differs from real protective earth, isolation, and return paths.
- Do not connect mains, stored energy, high-power RF, or laser loads based on simulation alone.
- An absolute maximum rating is not a recommended operating point.
- Higher-energy designs require a qualified facility, trained supervision, and independent protection.

## Completion checklist

- [ ] Every analysis begins with an order-of-magnitude prediction.
- [ ] DC, AC, and transient settings match the question.
- [ ] Model source, version, license, and range are recorded.
- [ ] Scripts or measurement statements extract key results.
- [ ] At least one tolerance or corner analysis is complete.
- [ ] An intentional fault triggers an acceptance failure.
- [ ] Batch execution rebuilds all results from source.
- [ ] Unmodeled effects and safety limits are explicit.

Next, turn simulation assumptions into layout constraints with [PCB and KiCad Workflow](pcb-kicad.md), or study convergence through [Numerical Computing](numerical-computing.md).
