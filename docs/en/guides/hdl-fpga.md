---
title: HDL, Simulation, and FPGA
description: Close the digital-hardware learning loop with synthesizable RTL, self-checking tests, and timing evidence.
---

<div class="ee-language" markdown>
[简体中文](../../guides/hdl-fpga.md)
</div>

# HDL, Simulation, and FPGA

An HDL describes concurrent hardware structure, not sequential software. An FPGA tool is an implementation vehicle. Prove function in vendor-neutral simulation first, then use synthesis, constraints, and timing analysis to show that an implementation meets its objective.

## Purpose and learning outcomes

- Distinguish combinational logic, sequential logic, and simulation-only constructs.
- Write self-checking tests instead of relying only on waveform inspection.
- Handle reset, clock-domain crossing, metastability, and parameter boundaries.
- Read synthesis resources, latch warnings, and static-timing reports.
- Preserve verification evidence that does not require a physical board.

## Minimal environment

- An HDL compiler or simulator and a waveform viewer.
- A scriptable test entry point.
- A supported HDL subset and explicit clock objective.
- An optional FPGA board and vendor implementation tool; the core exercise does not require either.

Record the observed language standard, simulator, synthesizer, and device target versions. A sequence of vendor GUI clicks is not a design specification.

## Learning sequence

1. **Combinational logic:** implement an encoder or ALU, assign every path, and avoid accidental latches.
2. **Sequential logic:** update state on one clock edge and define synchronous or asynchronous reset semantics.
3. **Self-checking tests:** let stimuli, a reference model, and assertions decide pass or failure.
4. **State machines:** separate transition and output logic and test illegal-state recovery.
5. **Timed interfaces:** learn handshakes, pipelines, and structured clock-domain crossings.
6. **Implementation:** add pin and clock constraints, implement the design, and inspect the worst path.

## Verification task: parameterized FIFO with handshake

Implement a small synchronous FIFO:

1. Specify depth, width, full/empty semantics, and simultaneous read/write behavior.
2. Cover minimum depth and non-power-of-two boundaries, or document an explicit restriction.
3. Build a reference queue and generate legal randomized operations.
4. Assert overflow, underflow, ordering, and reset properties.
5. Introduce a pointer error and confirm the test fails.
6. Synthesize two parameter configurations, compare resources, and inspect timing constraints.

Acceptance requires replayable tests with fixed seeds, zero accidental latch or undriven-signal findings, and evidence of worst timing margin or zero unconstrained paths.

## Common failures and diagnosis

- **Simulation passes but synthesis differs:** inspect nonsynthesizable constructs, incomplete assignment, initialization, and races.
- **Waveforms contain unknown values:** trace unreset registers, multiple drivers, out-of-range indices, and open inputs.
- **Hardware fails intermittently:** inspect metastability, clock crossings, constraints, and external-input synchronization.
- **Timing “passes” with unconstrained paths:** add clocks, I/O delays, and documented exception rationale.
- **Behavior fails after reset release:** analyze cross-domain reset and synchronized deassertion, not merely longer reset.
- **Random tests differ every run:** retain the seed and the minimized failing sequence.

## Reproducible evidence

- RTL source, parameters, and interface timing description.
- Testbench, reference model, assertions, and fixed seeds.
- Batch simulation command and pass/fail summary.
- Key waveforms only as diagnostic supplements.
- Resource report, warning disposition, and timing summary.
- Constraint file, device or board target, and tool versions.
- Known clock-domain, reset, and hardware dependencies.

## Cost, licensing, and accessibility

Functional verification can use free simulators and portable RTL. Vendor tools and boards are needed only for implementation; check no-cost limits, device support, download size, and licenses. Do not publish restricted IP cores or encrypted netlists.

Provide textual test summaries; do not communicate state only through waveform colors. Group and name waveform signals semantically and describe the failing cycle in text. Learners without a board can meet the same functional objective through simulation and implementation reports.

## Safety boundaries

- Before using a board, verify I/O voltage, pins, direction, pull resistors, and clock source.
- Do not connect unverified logic directly to a motor, power stage, laser, or RF transmitter.
- Outputs need a safe default during reset, configuration, and clock loss.
- Passing timing does not establish external electrical safety.
- For high-speed interfaces, stay within board ratings and use suitable measurement methods.

## Completion checklist

- [ ] Combinational and sequential boundaries are explicit.
- [ ] The testbench decides results automatically and replays fixed seeds.
- [ ] Boundaries, reset, full/empty, and fault paths are tested.
- [ ] No latch, multiple-driver, or undriven warning remains unexplained.
- [ ] Constraints are complete with no unexplained unconstrained path.
- [ ] Resource and timing reports are retained per target configuration.
- [ ] Tools, target device, licensing, and limits are recorded.
- [ ] Board-level outputs have a safe default state.

Next, study hardware/software integration with [Embedded Toolchains](embedded-toolchains.md), or automate HDL regression with [Reproducible Engineering](reproducibility.md).
