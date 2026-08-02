---
title: "Digital VLSI and Chip Design"
description: "CMOS logic, timing, power, physical design, and verification with explicit open-source versus restricted EDA paths."
page_type: track
track_id: "track-vlsi-ic"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: eabf2a5f2b27653a -->

# Digital VLSI and Chip Design

## Track position

CMOS logic, timing, power, physical design, and verification with explicit open-source versus restricted EDA paths.

## Recommended prerequisite tracks

- [Microelectronics](../microelectronics/index.md)
- [Digital Logic and Computation Structures](../digital-logic/index.md)

## The public 6.374 archive can carry the digital-IC spine by itself

[MIT 6.374](050-6-374.md) uses notes, problems, exams, and design material on its [official OCW page](https://ocw.mit.edu/courses/6-374-analysis-and-design-of-digital-integrated-circuits-fall-2003/) to connect transistor switching, delay, power, logic blocks, memory, and physical design. Its 2003 process, SPICE, standard-cell, and layout concepts remain useful, while numbers and tools need historical labels. Follow inverter delay, sizing, timing/power, memory, and layout, then port the design task to an open teaching library; a modern tool does not reproduce the original lab.

Carry one inverter chain from hand logical-effort/RC trends into SPICE/library delay, then locate the same loading effect on a block critical path. Compare historical and migrated library/corner results instead of forcing a match.

## EECS 151, 6.884, and ECE 4740 each fill only one named gap

[Berkeley EECS 151](044-eecs-151.md) provides modern scope through its [official catalog](https://www2.eecs.berkeley.edu/Courses/EECS151/) and public HKN solved exams, but teaching sites redirect to CalNet rather than an open lab. [MIT 6.884](049-6-884.md) adds complex systems through its [OCW archive](https://ocw.mit.edu/courses/6-884-complex-digital-systems-spring-2005/), with commercial EDA and old-cell constraints. [Cornell ECE 4740](051-ece-4740.md) publishes VLSI systems material and labs on its [official page](https://ocw.ece.cornell.edu/ece-4740-course-details/); the archive lists Labs 1–5 while the overview says four extensive labs, so retain both statements.

After 6.374, select one supplement for modern scope, system complexity, or laboratory intent. Repeating four synthesis and layout flows mainly repeats tool steps. Login-protected starters, answers, and staff repositories should not be retrieved through mirrors.

Name the supplement’s job: EECS 151 checks scope/exam style, 6.884 complex-system decomposition, and ECE 4740 public lab intent/workflow. Record year, public entry, and missing grader/tool access so archive, catalog reference, and prompt do not become an invented combined course.

## Make one ready-valid datapath align across RTL, cell timing, and the physical path

MOS regions, parasitic capacitance, inverter transfer, and sizing from [microelectronics](../microelectronics/index.md) meet logic, FSM, pipelines, clocks, and reset from [digital logic](../digital-logic/index.md) in a single-clock ready-valid datapath. Write a cycle contract and self-checking testbench for backpressure, reset, overflow, latency, and continuous traffic; estimate logic depth, fanout, and register boundaries.

The contract accepts input on `valid && ready`, holds output stable under backpressure, and defines outstanding transactions across reset. A transaction identifier scoreboard aligns reference results with output cycles; assertions check stability, no drops, and no duplicates. The fixed-point model defines sign extension, rounding, and saturation.

After synthesis, inspect cells, buffers, memory/multiplier mapping, and combinational loops; after routing, inspect wire delay, congestion, clock tree, slew, and capacitance. Trace one input vector from port cycles through register boundaries to the slowest physical path despite renamed hierarchy. Waveforms do not replace assertions, and quoted cell delay does not replace load/drive/parasitic trends.

A path table maps an RTL expression to a synthesized cell arc and then to placed instance, net, and coordinate. Explain a post-synthesis path change through mapping/optimization and a post-route wire-dominated path through congestion, fanout, or placement, using the same pipeline stage for functional vectors and STA.

## Open EDA produces an educational implementation, not automatic foundry signoff

Use Verilator/GTKWave for regression, Yosys for synthesis, OpenROAD/OpenSTA for implementation/timing, and KLayout for geometry. State releases, Liberty/LEF/PDK sources, corners, constraints, seeds, and licenses; separate simulation, synthesis, and physical sources. These differ from course VCS, Design Compiler, Innovus, Vivado, PYNQ, or legacy-cell environments, so a port proves only functionally similar work.

Without an authorized PDK and complete rules, report area, timing, routing, and geometry on a teaching library. Manufacturability, tape-out readiness, signoff, and silicon validation need absent evidence. Course material also lacks packaging, complete IR-drop/EM context, and post-silicon data. Activity/library estimates are power proxies with missing parasitic, process, and workload information stated.

Trace every input: Liberty defines cell timing/power, LEF abstract geometry, technology LEF and routing rules interconnect constraints, and SDC clock/I/O assumptions. Mixed sources or incompatible corners can look complete while lacking physical meaning. DRC clean means only that the loaded rules passed; it is not a missing foundry deck or signoff extraction.

## Push one MAC pipeline to its first negative slack

Implement a fixed-point ready-valid multiply-accumulate core with defined width, rounding/saturation, reset, latency, and throughput. Check arithmetic with a reference model, corner cases, and random vectors; compare one-, two-, and three-stage pipelines. For each, run equivalence, synthesis, place-and-route, and STA at 3 clock constraints. Report area, utilization, wire length, worst slack, and power proxy, separating clock frequency from data throughput.

Use the first negative-slack result as the diagnostic. Trace startpoint, endpoint, logic/wire delay, and transition violation to RTL; then restructure logic, add a stage, reduce fanout, or revise a physical constraint. Hand estimates check STA direction, not library data. Include RTL, assertions/tests, vectors, scripts, constraints, library information, timing/congestion/geometry output, and the failing version. A layout screenshot without equivalence, corners, and constraint variation does not establish a working design.

Compare pipeline depths on accepted transactions: registers add latency, faster clocks raise nominal capacity, and bubbles/backpressure reduce delivered throughput. Report cycle latency, maximum accepted rate, and delivered rate for one trace. After fixing slack, rerun equivalence and protocol regression to protect rounding, reset, and ready-valid behavior.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Analysis and Design of Digital Integrated Circuits](050-6-374.md) | MIT | Main course | Public-material guide | Public assignments or labs |
| [Digital Design and Integrated Circuits](044-eecs-151.md) | University of California, Berkeley | Alternative | Public-material guide | No public practice found |
| [VLSI Systems](051-ece-4740.md) | Cornell University | Supplement | Public-material guide | Partial or restricted |
| [Complex Digital Systems](049-6-884.md) | MIT | Supplement | Public-material guide | Partial or restricted |
