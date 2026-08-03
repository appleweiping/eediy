---
title: Tools and Environments
description: Choose EE software and laboratory tools by learning objective, reproducibility, cost, and risk.
---

<div class="ee-language" markdown>
[简体中文](../../guides/tools.md)
</div>

# Tools and Environments

A tool exists to test a model; it is not the learning objective. Ask what you need to observe, how precise the result must be, and how another person can reproduce it before choosing software, instruments, or hardware. A small, stable toolchain usually beats constant platform switching.

## Five selection criteria

1. **Objective coverage:** can it support the current input, analysis, implementation, and verification?
2. **Reproducibility:** can you save text configuration, versions, parameters, and scripts—not just screenshots?
3. **Availability:** are its license, operating system, region, hardware, and network requirements sustainable?
4. **Transfer:** do the concepts carry to other tools, or are you learning one interface?
5. **Risk fit:** do ratings, isolation, protection, and user training match the experimental energy?

## Minimal software stack

These are not the only valid tools, and you should not install all of them. Choose one primary tool per row. When a course requires commercial software, preserve an accessible alternative path.

| Task | Practical starting point | Alternatives | Evidence to retain |
| --- | --- | --- | --- |
| Numerical work and data | [Python](https://www.python.org/) + [Jupyter](https://jupyter.org/) | [GNU Octave](https://octave.org/) | Environment file, scripts, raw data, plots with units |
| Circuit simulation | [ngspice](https://ngspice.sourceforge.io/) or course-supported SPICE | Qucs-S, vendor simulator | Netlist/schematic, model source, tolerance sweep |
| PCB design | [KiCad](https://www.kicad.org/) | Course or laboratory EDA | Schematic, layout, rules, BOM, fabrication outputs |
| HDL simulation | [Icarus Verilog](https://steveicarus.github.io/iverilog/) or [Verilator](https://www.veripool.org/verilator/) | FPGA vendor suite | Source, testbench, waveforms, coverage/timing summary |
| Waveform inspection | [GTKWave](https://gtkwave.github.io/gtkwave/) | Simulator viewer | Replayable waveform and trigger conditions |
| Embedded builds | Compiler + debugger + scripted build | PlatformIO, vendor SDK, RTOS toolchain | Locked dependencies, flashing method, serial/logic logs |
| Versioning and review | [Git](https://git-scm.com/) | Institution-compatible hosting | Small commits, tags, issues, review decisions |
| Reports and plots | Markdown + script-generated figures | LaTeX, notebooks | Report rebuilt from source data |

!!! note "Commercial does not automatically mean better"
    Industry tools can matter for a role or chip flow, but foundational concepts and files should remain transferable. Record versions, license limits, and an alternative so the artifact is not trapped on one machine.

## A reproducible software environment

Put the environment contract in the project rather than in memory:

```text
project/
├── README.md             # Objective, install, run, verify
├── environment.yml      # Or requirements/lockfile
├── Makefile              # Or an equivalent repeatable task entry
├── src/
├── tests/
├── simulations/
├── data/
└── docs/
```

Record at least:

- operating system, tool, and critical plugin versions;
- installation source and license requirements;
- one clean-environment build path;
- random seeds, model files, and data provenance;
- the command that creates plots and reports;
- known platform differences and failure modes.

For binary project formats, also export reviewable PDFs, netlists, BOMs, test reports, or textual intermediate forms. Exports do not replace source files, but they let reviewers without the same license participate.

## Classify a workbench by energy

<div class="ee-card-grid ee-card-grid--three">
  <article class="ee-card">
    <span class="ee-tag">Level 0</span>
    <h3>Software only</h3>
    <p>Hand analysis, computation, circuit/field/control simulation, public data, and HDL testbenches. Appropriate at every stage and the first step before physical work.</p>
  </article>
  <article class="ee-card">
    <span class="ee-tag">Level 1</span>
    <h3>Bounded low energy</h3>
    <p>Protected teaching supplies, low-energy components, conservative current limits, and complete rating checks. Short circuits, heat, polarity, grounding, and tool hazards still matter.</p>
  </article>
  <article class="ee-card">
    <span class="ee-tag">Level 2+</span>
    <h3>Qualified facility and supervision</h3>
    <p>Mains, higher voltage/current, stored-energy systems, lasers, RF power, moving machinery, vacuum, high temperature, or chemical processes. Use only approved facilities and trained supervision.</p>
  </article>
</div>

Voltage is not the only risk variable. Current capability, stored energy, arcs, frequency, grounding, temperature, motion, and chemical exposure can change the hazard class. Read [Laboratory Safety](safety.md) before starting.

## What a Level 1 bench needs to accomplish

Models and prices vary by region and project, so treat this as a functional list:

- **Protected source:** current limiting and output ratings matched to the project; start at a conservative limit.
- **Digital multimeter:** category and range fit the use; probes, fuses, and jacks are intact.
- **Observation:** select an oscilloscope, logic analyzer, or software instrument by objective; understand input range and ground first.
- **Connection and protection:** insulated leads, appropriate fusing/limiting, eye protection, stable surface, lighting, and ventilation.
- **Traceable components:** retain part number, data sheet, and source; unknown batteries and power supplies do not enter the bench.

!!! warning "An oscilloscope ground clip is not an arbitrary reference"
    Many bench oscilloscope grounds connect to protective earth. A wrong connection can short a circuit, damage equipment, or injure someone. If you do not understand the supply and isolation topology, do not probe mains or floating high-energy systems. Use simulation, a properly rated differential setup, or a supervised facility.

## Files, units, and names

- Preserve column names, units, sample rate, timestamp, and instrument settings in data.
- Include object, condition, and sequence in names; avoid `final-final-2`.
- Use consistent SI units and prefixes; every plot axis needs a unit.
- Define parameters in one authoritative file and derive simulation, code, and reports from it.
- Append to raw data; make cleaning and processing rerunnable.
- Never publish secrets, personal data, paid materials, or controlled device files.

## Learn a tool in this order

1. Verify installation and version with a minimal example.
2. Reproduce a reference result from the course.
3. Change one parameter and predict the effect.
4. Introduce one deliberate fault and learn the logs and diagnostics.
5. Automate the repeated path.
6. Export evidence another learner can inspect.

When switching tools, map concepts—nodes, netlists, constraints, testbenches, debug interfaces, coordinates, and units—instead of copying button sequences.

## Accessibility and low-bandwidth paths

- Prefer text notes, captions/transcripts, and downloadable files.
- Distinguish plots with line style, symbols, and direct labels in addition to color.
- Describe the conclusion and key data in image alternatives; “figure below” is insufficient.
- A large video should not be the only route; provide chapter, exercise, and timestamp mappings.
- Cloud tools need a local or export path so a network interruption does not erase core work.
- Keyboard operation, sufficient contrast, and scalable text are tool-selection requirements.

Next: turn the environment into a testable micro-project with the [Project Practice](projects.md) guide.
