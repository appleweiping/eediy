---
title: HDL, Simulation, and FPGA
description: Build a portable RTL workflow with two simulators, a self-checking FIFO, passing formal results, a counterexample from a deliberately broken revision, and complete timing constraints.
page_type: guide
comments: true
---

# HDL, Simulation, and FPGA

This page follows one synchronous FIFO through two revisions. The
self-checking tests and stated formal properties should pass on `baseline`.
The `fault/read-pointer` revision deliberately corrupts the read-pointer
update so the tests and properties have a real error to catch. After finding
a minimal failing seed or counterexample, the repaired `baseline` runs the
same checks again. The counterexample belongs to the broken revision, not to
the deliverable design.

The repository's [synchronous FIFO verification starter](https://github.com/appleweiping/eediy/tree/main/examples/sync-fifo) implements the chain below. From the repository root, run `python examples/sync-fifo/run_checks.py`: installed Icarus, Verilator, SymbiYosys/Z3, and Yosys paths execute for real, while an unavailable tool is reported as `CHECK_SKIP`. A release machine uses the same command with `--require-tools all` so absence is a failure. Baseline and read-pointer-fault builds share one testbench and formal reference model; the fault must exit nonzero and SBY must generate a counterexample. No prefabricated PASS log is committed.

| Revision | Expected evidence | Unacceptable substitute |
| --- | --- | --- |
| `baseline` | Self-checking PASS in two simulators; formal PASS with assumptions, mode, and depth recorded | A waveform screenshot or “simulation looks right” |
| `fault/read-pointer` | Automated failure with cycle and seed; a saved formal counterexample | A verbal diagnosis after manual waveform inspection |
| Repair commit | The same failing input becomes PASS while the rest of the regression stays green | Deleting the trigger or weakening the property |

The FIFO then moves through simulation, formal verification, synthesis,
CDC/timing, and hardware checks. Each step answers a different question; a
generated bitstream cannot replace the earlier verification.

## Run the same interface in Icarus and Verilator

The [Icarus Verilog getting-started guide](https://steveicarus.github.io/iverilog/usage/getting_started.html) separates compilation with `iverilog` from execution with `vvp` and explains why a `-c` file list and `-s` top module matter in a multi-file design. Pin the language standard, top, and source order. For example, let a script run `iverilog -g2012 -s fifo_tb -o build/fifo.vvp -c rtl.f` and then execute the compiled output with `vvp build/fifo.vvp`; do not depend on incidental shell-glob order or allow several uninstantiated modules to become roots.

The [official Verilator overview](https://verilator.org/guide/latest/overview.html) describes compilation of Verilog or SystemVerilog into a C++ or SystemC model rather than a traditional event simulator. Use lint to address width, signedness, unreachable code, latch, and multiple-driver findings, then run the same vectors and reference model under Verilator and Icarus. When they disagree, reduce the design to the shortest source list and first divergent cycle, then inspect language extensions, unknown initialization, races, delay constructs, and simulator-specific behavior. Do not use separate `ifdef` paths merely to appease each tool.

A scoreboard or assertion must decide the result; a waveform only explains a failure. Preserve every random seed and minimize the input sequence after finding a bug. CI output should name testcase, cycle, expected and actual values, and the failing signal so diagnosis does not require a GUI.

## Break one revision to prove that the tests can fail

Implement a synchronous ready/valid FIFO and define depth, width, full and empty behavior, simultaneous read and write, output after reset, and treatment of illegal requests. A reference queue should cover empty-to-write-to-read, full boundaries, wraparound, sustained backpressure, and inserted reset. If non-power-of-two depth is unsupported, reject it during elaboration rather than silently overflowing a pointer. Damage the read pointer or count only in a separate fault revision and confirm that the tests fail. Preserve the counterexample, return to the correct revision, and make the same test and property PASS. An always-green suite without a negative control says little.

The [SymbiYosys FIFO quickstart](https://yosyshq.readthedocs.io/projects/sby/en/stable/quickstart.html) connects count, pointer difference, overflow and underflow properties, and generated counterexample traces. Write safety assertions for occupancy bounds, count changes after accepted reads and writes, ordering, and reset state, then add covers showing that empty, full, and simultaneous operations are reachable. A bounded proof covers only its configured time depth, while an unbounded proof still depends on environment assumptions. Preserve solver, mode, depth, and assumptions with the result rather than turning a PASS screenshot into a claim about every parameter.

## Use synthesis to identify the resulting hardware

The [Yosys documentation](https://yosyshq.readthedocs.io/projects/yosys/en/latest/) describes a synthesis framework, not another simulator. Pin a script that performs `read_verilog -sv`, `hierarchy -top`, process lowering, optimization, `check`, and target-specific synthesis. Inspect latch, combinational-loop, undriven or multiply driven, memory-inference, cell-count, and hierarchy results instead of stopping at a successful exit code. Synthesize two FIFO depths and explain why storage becomes registers, distributed RAM, or block RAM and whether inferred structure changes read latency.

Separate portable RTL from vendor primitives. Keep control and data protocols generic and place PLLs, block-RAM modes, SERDES, and debug cores behind thin wrappers. Simulation models, synthesis sources, and constraints need explicit file sets. For a netlist or bitstream, record tool version, device part, parameters, constraint hash, and source commit. If an open synthesizer rejects a SystemVerilog construct, decide whether this is a language-support gap or a genuine proprietary dependency; do not hide functional changes under a “compatibility” rewrite.

## CDC structure and timing constraints are separate problems

Design CDC before constraining it. A single-bit level may use a clearly identified synchronizer, but this only reduces the probability that metastability propagates and does not ensure that a narrow pulse is observed. A pulse or command needs a toggle or handshake. A multi-bit payload needs stable data plus handshake or a proven asynchronous FIFO, not an independent two-flop chain on every bit. Reset may assert asynchronously, but deassert it synchronously within each clock domain and test missing clocks, different release order, and reset crossings.

Then constrain primary and generated clocks, input and output delays, and real timing exceptions. [AMD's 2026.1 UG903](https://docs.amd.com/r/en-US/ug903-vivado-using-constraints/All-Constraints) joins clocks, I/O, asynchronous clock groups, CDC synchronizers, and constraint coverage in one flow; another vendor still needs the same completeness of description. `set_false_path` may describe an asynchronous relation already protected by correct CDC structure. It cannot make a bad crossing safe. Account for every unconstrained path, setup and hold, recovery and removal, clock uncertainty, and worst slack in the implementation report. “Timing passed” is meaningless while unexplained paths remain unconstrained.

## First hardware should test only the physical interface

For first hardware, use only protected onboard LEDs, buttons, or a loopback. Check the schematic, bank voltage, pin direction, pull resistors, clock source, and configuration-time state, and connect peripherals with power removed. Unverified RTL must not drive a motor, power stage, laser, or RF transmitter. Outputs need safe values during configuration, reset, clock loss, and loss of lock. Tie every bitstream to its source commit, constraints, device part, and fixed demonstration input.

The project record should contain RTL, an interface timing diagram, commands
for both simulators, a self-checking testbench, fixed seeds, formal PASS
results from the correct revision, and the counterexample plus patch or commit
from the deliberately broken revision. Add the Yosys script, vendor
constraints, resource, timing, and CDC summaries, and an optional board trace.
Without a board, the work can legitimately end at a post-implementation
report. Hardware adds observations of I/O and the physical clock; it does not
invent a missing property or constraint. [Embedded
Toolchains](embedded-toolchains.md) extends the evidence chain when a
processor and firmware join the system; [Reproducible
Engineering](reproducibility.md) keeps this regression stable across
machines.
