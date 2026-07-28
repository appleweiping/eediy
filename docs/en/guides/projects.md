---
title: Project Practice
description: Build verifiable EE projects through specification, modeling, implementation, measurement, and review.
---

<div class="ee-language" markdown>
[简体中文](../../guides/projects.md)
</div>

# Project Practice

A project is valuable when it forces explainable engineering judgment, not when it contains many parts. An excellent first project may be small, but it must include prediction, implementation, measurement, and a difference analysis.

## The project loop

<div class="ee-route">
  <div class="ee-route__stage">
    <div>
      <h3>Problem and acceptance</h3>
      <p>Define the user, input, output, constraints, tests, and non-goals. Replace “build a filter” with measurable passband, cutoff, load, and error requirements.</p>
    </div>
  </div>
  <div class="ee-route__stage">
    <div>
      <h3>Model and budgets</h3>
      <p>Build the simplest useful model. Record parameter sources, dimensions, tolerance, noise, power, cost, and safety budgets, then predict the critical curves.</p>
    </div>
  </div>
  <div class="ee-route__stage">
    <div>
      <h3>Simulation and design review</h3>
      <p>Cover nominal and boundary conditions and examine failure modes. Review specification, schematic, and test plan before purchasing, fabrication, or energization.</p>
    </div>
  </div>
  <div class="ee-route__stage">
    <div>
      <h3>Implementation and staged verification</h3>
      <p>Begin with the smallest module and energy. Change one variable at a time. Automate software/HDL tests; perform passive and de-energized checks on hardware first.</p>
    </div>
  </div>
  <div class="ee-route__stage">
    <div>
      <h3>Measurement and retrospective</h3>
      <p>Keep raw data and align prediction, simulation, and measurement. Explain differences, limitations, and the next revision without deleting the failed path.</p>
    </div>
  </div>
</div>

## The one-page project specification { #project-spec }

Before creating a repository or buying parts, answer:

| Field | Required content |
| --- | --- |
| Problem | Who needs which result, and in what context? |
| Input/output | Signals, energy, format, range, units, and references |
| Acceptance test | Repeatable procedure, pass threshold, and measurement uncertainty |
| Constraints | Cost, time, power, size, tools, license, and availability |
| Safety boundary | Maximum energy, prohibited state, supervision, and stop conditions |
| Assumptions | Environment, load, model, parts, sampling, and user behavior |
| Non-goals | What this revision intentionally does not solve |
| Milestones | Each milestone can be verified and demonstrated independently |

If the acceptance test is impossible to write, the problem is still too broad or its terms are undefined.

## Project ladder: software to hardware

Every project starts with a safety assessment. These examples increase in conceptual complexity; they do not authorize a particular voltage, power, or setting.

| Level | Example | Core capability | Minimum acceptance |
| --- | --- | --- | --- |
| 0 | Measurement-data cleaning and uncertainty plot | Units, statistics, scripting, reproducible plots | Rebuild the result from raw data in one path |
| 0 | RC/RLC transient and frequency simulation | Differential equations, phasors, model boundary | Hand, numerical, and SPICE results agree within a budget |
| 0 | HDL state machine and self-checking bench | Timing, states, assertions, fault cases | Automatic results for valid and invalid inputs |
| 1 | Bounded low-energy sensor readout | Data sheet, ADC, calibration, noise | Error and repeatability against a known reference |
| 1 | Low-energy active filter/amplifier | Op-amp, bandwidth, load, stability | Measured response aligned with prediction and discrepancy explained |
| 1 | Microcontroller data logger | Driver, timestamp, buffering, file format | Long-duration test quantifies or eliminates dropped samples |
| 1 | FPGA serial interface or small processing unit | Protocol, domain awareness, synthesis, timing | Self-checking tests plus resource/timing report |
| 0–1 | Digital filter and real-time implementation | Sampling, quantization, compute budget | Comparable offline baseline and real-time output |
| 0–1 | Identification and closed-loop control | Model, stability, saturation, delay | Simulation first; bounded plant validation stays inside limits |
| 0 | Receive-only communication-link analysis | Link budget, noise, modulation, statistics | Predicted and public/self-captured error metrics agree |
| 0 | Electromagnetic or thermal parameter sweep | Boundary conditions, mesh, convergence | Mesh independence and analytic/benchmark comparison |
| 2+ | High energy, RF transmit, laser, or process work | Formal assessment and specialist facility | Defined only in an authorized laboratory plan |

## The project evidence package { #project-evidence-package }

A reviewer who has never met the author should be able to determine what was done, why it is credible, and how to reproduce it.

```text
project/
├── README.md              # Summary, demonstration, reproduction
├── SPEC.md                # Requirements, non-goals, acceptance matrix
├── SAFETY.md              # Hazards, controls, stop conditions
├── design/                # Derivations, schematics, constraints, reviews
├── src/                   # Software, firmware, or HDL
├── simulation/            # Models, netlists, parameter sweeps
├── tests/                 # Automated tests and hardware protocols
├── data/raw/              # Append-only source measurements
├── data/processed/        # Rebuildable products
├── bom/                   # Parts, substitutes, cost, licenses
└── report/                # Conclusion, error, failure, next revision
```

### The README first view

- one-sentence problem and result, not a slogan;
- one key result plot with units and direct labels;
- status: concept, simulation, prototype, verified, or stopped;
- a three-to-five-step reproduction path;
- safety boundaries and prohibited uses;
- the most important limitation and failure.

## Design-review gates

### Gate 0: the problem is valid

- Acceptance metrics are measurable.
- Scope fits time and budget.
- Work does not depend on unavailable equipment or restricted material.
- A software-only or bounded low-energy first milestone exists.

### Gate 1: implementation is credible

- Model, interfaces, part ratings, and error budgets are consistent.
- Critical parts have data sheets and obtainable substitutes.
- Test points, debug interfaces, and observability are designed.
- Risk controls begin with elimination, energy limitation, and engineered protection.

### Gate 2: execution or energization is allowed

- Simulation or automated tests pass.
- Schematic, wiring, polarity, shorts, and mechanical boundaries are reviewed.
- Instrument and supply settings are recorded.
- Stop conditions are explicit and required supervisors are present.

### Gate 3: completion can be claimed

- Every acceptance result traces to raw data.
- Failed tests and deviations remain visible.
- The report separates measured, inferred, and assumed statements.
- A reproduction from locked versions produces an equivalent result.

## Evaluation rubric

<div class="ee-rubric">

| Dimension | 0: missing | 1: preliminary | 2: reliable | 3: engineering-grade |
| --- | --- | --- | --- | --- |
| Problem | Title only | Goal without thresholds | Measurable metrics and non-goals | Metrics connect to a real context and tradeoffs |
| Model | No prediction | Unchecked formula/simulation | Assumptions, units, benchmark | Sensitivity, boundary, and failure models |
| Implementation | Does not run | Works only for author | Versions, build, interfaces clear | Modular, testable, maintainable |
| Verification | Demo only | A few successful cases | Test matrix and raw data | Uncertainty, fault injection, repeatability |
| Safety | Not addressed | Generic warning | Project-specific hazards and controls | Controls verified; residual risk recorded |
| Communication | Screenshots only | Describes what was built | Reproducible report and figures | Reviews, tradeoffs, and next revision clear |

</div>

The score exposes weak interfaces; it is not a leaderboard. A safety score of zero blocks physical execution.

## Failure log

```text
Observed:
Expected:
Minimal reproduction:
Ruled out:
Root-cause evidence:
Fix:
Regression test:
Still unknown:
```

Do not stop at “bad contact,” “library bug,” or “wrong parameter.” Separate observation from interpretation. If the cause is uncertain, mark it unknown and preserve the minimal failing case.

## Team projects

- Give every interface an owner and a reviewer.
- Express specifications, data formats, pins, timing, and safety responsibilities as contracts.
- Run automated checks before merging and record the hardware revision.
- End meetings with decisions, evidence, objections, and open validation items.
- Attribute actual contributions and cite external code, models, and data under their licenses.

Choose the minimum stack from [Tools and Environments](tools.md) and pass [Laboratory Safety](safety.md) before any physical step.
