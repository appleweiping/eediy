---
title: Project Practice
description: Build an electrical-engineering project that can explain the path from specification and model to implementation and measurement.
page_type: guide
comments: true
---

# Project Practice

A board that powers up or RTL that reaches an FPGA has not necessarily answered an engineering question. The useful test is whether you can predict an outcome, implement the system, and explain where prediction and observation agree or fail. A tightly scoped low-voltage system with a precise question and trustworthy measurements is often more valuable than a feature-rich “capstone” whose behavior cannot be explained.

## Executable starting points in this repository

These 5 starters include source code and fault cases, and the release gate rebuilds them with real toolchains. Run the Python commands from the repository root and the 2 CMake workflows from their respective starter directories. They are independent EEDIY exercises, not official assignments from the mapped university courses.

| Starter | Command | What the run actually checks |
|---|---|---|
| [RC low-pass: analytical and ngspice](https://github.com/appleweiping/eediy/tree/main/examples/rc-lowpass) | `python examples/rc-lowpass/run.py` | Analytical step/frequency baselines, parameters, and generated-data checksums; the full release gate also runs the ngspice netlist and compares \(\tau\) and cutoff |
| [Fixed-capacity ring buffer](https://github.com/appleweiping/eediy/tree/main/examples/ring-buffer) | `cmake --workflow --preset host-sanitized` | Empty, full, wraparound, ADC/DMA-adapter, and fault cases with ASan/UBSan genuinely active |
| [Timeout-aware sensor sampler](https://github.com/appleweiping/eediy/tree/main/examples/sensor-sampler) | `cmake --workflow --preset host-sanitized` | Ordinary sampling, timeout, delayed interrupt, bus error, and cancellation paths with line-checkable output |
| [Synchronous FIFO simulation, formal, and synthesis](https://github.com/appleweiping/eediy/tree/main/examples/sync-fifo) | `python examples/sync-fifo/run_checks.py --require-tools all` | Icarus/Verilator simulation, a SymbiYosys counterexample, and Yosys synthesis; the fault implementation must fail |
| [TMP117 two-layer KiCad board](https://github.com/appleweiping/eediy/tree/main/examples/tmp117-kicad) | `python examples/tmp117-kicad/export.py --require-kicad` | ERC, DRC, pin parity, and manufacturing-file export; no fabricated-board measurement is included |

A skipped tool is not a passing result. The release environment uses the strict arguments in the table and fails when a dependency is missing. On a first read, begin with the “what this does not prove” section in each README, then adapt the starter into course work of your own.

## When an exercise is ready to become a project

Keep solving exercises while the input is fixed and there is one expected answer. Turn the work into a project when interfaces, tolerances, noise, timing, power, or cost create a real tradeoff. A useful starting question has conditions, for example: “With a 5 V supply and the specified sensor source impedance, can a front end map 10–40 °C into the ADC's usable range while meeting stated limits on in-band noise and settling time?”

That question establishes an input, environment, output, and conflict. “Build a smart thermometer” does not: networking, display, enclosure, and software can all hide whether the analog front end works. A first project should isolate one major uncertainty—model fidelity, implementation behavior, or measurement validity. Five unknown interfaces at once turn debugging into random component replacement.

## Write a specification that can fail

NASA's guidance on [writing a good requirement](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/) distinguishes a mandatory requirement from a statement of fact or an aspiration. The [Appendix D requirements-verification matrix](https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/) asks that each “shall” have a planned method such as analysis, inspection, demonstration, or test. A student project does not need aerospace paperwork, but both ideas scale down well.

Before implementation, state on one page:

- the operating envelope: input, supply, load, clock, temperature, or data distribution;
- measurable quantities such as gain error, bandwidth, noise, latency, throughput, power, and resource use, each with units and tolerances;
- explicit non-goals, such as no isolation, no mains connection, and no claim of production EMI compliance;
- the measurement method, including test point, instrument bandwidth and impedance, sampling, repetitions, and pass condition;
- failure behavior for saturation, oscillation, overflow, dropped samples, timing violations, or overheating.

“Good performance” and “stable operation” are not specifications. If a threshold is not yet known, mark it as an exploration variable and run a small experiment to find its scale. Do not write the target after the project around whichever result looks best.

## Make model, implementation, and measurement challenge one another

The first model only needs enough detail to support a choice. For an analog circuit, begin with operating point, gain, poles, and a noise budget. For digital logic, model state transitions, throughput, worst-case latency, and expected resources. For signal processing, state sampling, spectral, and error-propagation assumptions. Every parameter should point to a datasheet condition, hand calculation, course model, or measurement.

Implement the smallest version that exposes the dominant risk. Check bias, headroom, and one-stage response before attaching an ADC. Match RTL against a reference model and self-checking testbench before using an FPGA. Confirm sensor sign, sample period, and actuator limits before closing a control loop. Change one interpretable factor at a time and keep failed attempts; “three values changed and it worked” does not establish causality.

Measurement is not neutral observation. Tektronix's official [ABCs of Probes](https://www.tek.com/en/documents/whitepaper/abcs-probes-primer) treats source, probe, and oscilloscope as one measurement system and explains how input resistance, capacitance, bandwidth, and grounding can change a waveform. Record probe ratio, bandwidth limit, coupling, sample rate, load, and test point. If changing the probe changes the result, investigate loading before redesigning the circuit.

Compare prediction, simulation, and measurement explicitly. Attribute discrepancies to a missing model term, component spread, numerical setup, implementation defect, instrument limitation, or environment. NIST's [measurement-uncertainty guidance](https://www.nist.gov/pml/nist-technical-note-1297) separates statistically evaluated components from those estimated through specifications, calibration, or other information. At minimum, report repeatability, the source of instrument resolution and accuracy, and errors that remain unquantified.

## What a substantial small EE project looks like

Consider a low-voltage sensor front end. Specify sensor range and source impedance, then select protection, gain, filtering, and the ADC interface. Calculate headroom, noise, settling, and alias risk. Sweep supply, component tolerances, and load in SPICE. On a breadboard or PCB, measure DC transfer, frequency response, noise floor, and step response. The important outcome is not a polished Bode plot; it is knowing which region is limited by op-amp gain-bandwidth, which changes under probe or ADC loading, and which term dominates the error budget.

The same pattern applies elsewhere. A UART receiver needs baud-rate mismatch, metastability, and framing-error cases. A FIR accelerator should expose fixed-point quantization, throughput, latency, and resources. A simulated motor controller should separate the plant model, sensor noise, saturation, and sample delay. If a physical extension involves a motor, high-energy battery, mains supply, or another serious hazard, reduce it to an isolated low-energy simulation or bench setup and follow the [laboratory safety guide](safety.md). Risk does not make a project more authentic.

## How to know the project worked

Stop when the original question has been answered, not when no more features fit. A convincing result survives a new input inside the stated operating envelope, allows a major metric to be recomputed from raw data, and localizes a discrepancy to the model, implementation, or measurement layer. A final video, screenshot, or generated report alone cannot establish any of these.

Keep enough material for your future self to rerun the work: current specification and non-goals, versioned schematic or RTL and code, model and parameter sources, BOM or dependencies, raw data, plot commands, instrument settings, and failed conditions. End by answering two questions in plain language: “Which engineering judgment did the data support?” and “Outside which boundary does that conclusion stop applying?” If those answers are clear, the project has converted course knowledge into engineering judgment.
