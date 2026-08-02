## EE 140/240A sends the same specifications through problems, labs, and a project

Analog IC design begins at transistor level. Berkeley's [official course catalogue](https://www2.eecs.berkeley.edu/Courses/ELENG140/) names EE 105 as the prerequisite for EE 140/240A, so MOS I–V behavior, \(g_m\), \(r_o\), body effect, single-stage small-signal models, and the feedback, frequency-response, noise, and stability ideas of [analog electronics](../analog-electronics/index.md) need to be usable. [Berkeley EE 140/240A](141-ee-140-ee-240a.md) publishes 21 lecture PDFs, 10 homeworks, 8 labs, and a mixed-signal final project spanning biasing, single stages, differential pairs, feedback, noise, op amps, oscillators, and data converters. Its value lies in specifications returning in derivations, testbenches, and design choices.

[NPTEL Analog IC Design](036-108106105-noc26-ee66.md) supplies 12 weeks on MOS small signal, current mirrors, differential stages, frequency response, feedback, and fully differential common-mode feedback (CMFB). It is useful when a Berkeley note moves too quickly, but it has no open layout-verification chain. Following the Berkeley problem sequence and consulting the matching NPTEL week at a conceptual bottleneck is more efficient than taking both courses in series.

The prerequisite is more than remembering a few small-signal formulas. Given gain, swing, load, and power targets, a learner should be able to say which requirement is controlled mainly by bias current, device size, output resistance, or the compensation network. Otherwise the later laboratories become an undirected parameter search.

## Public LTspice, bench measurement, and campus Cadence are three different conditions

The first layer is the LTspice subset that public files can reconstruct. The opening portion of [Lab 1](https://people.eecs.berkeley.edu/~pister/140sp23/labs/lab1.pdf) uses hand analysis and LTspice. Old [Lab 3 Part 1](https://people.eecs.berkeley.edu/~pister/140sp23/labs/lab3_1.pdf) has a direct [`BJTopamp.asc`](https://people.eecs.berkeley.edu/~pister/140sp23/labs/BJTopamp.asc) download, enough to rerun operating-point and sweep work for its BJT op amp. The second layer is breadboarding, oscilloscope readings, slew or compensation measurements, and GSI initials. Opening the `.asc` file does not complete those residential portions.

The third layer is the Spring 2025 campus IC flow. [Lab 2](https://people.eecs.berkeley.edu/~pister/140sp25/labs/lab2.pdf), Labs 4–8, and the [design project](https://people.eecs.berkeley.edu/~pister/140sp25/labs/project.pdf) depend on a campus Virtuoso server, the SKY130 PDK, libraries, DRC, LVS, PEX, and instructor setup. An independent port using ngspice, Xschem, KLayout, or another lawful toolchain can be worthwhile when that infrastructure is unavailable, but its documentation needs the model deck, device mapping, corners, tool versions, and the simulation, bench, or campus conditions that were not reproduced.

Keep these layers separate in directory names and figure captions as well. Results from a public netlist, breadboard readings, and campus layout verification answer different questions and should not appear in one performance table without provenance. Textbook access, model access, and server access also need separate statements; buying a book does not provide the process files.

## Every performance claim must match its layer

Schematic simulation supports pre-layout claims about gain, stability, noise, and power. Simulated slew or noise is not a bench result, absence of a mismatch model rules out a statistical-yield claim, and schematic GBW is not a post-layout result without extracted parasitics. NPTEL enrollment, graded assignments, and certificate exams can change between runs; public videos alone confer no formal grade.

A differential pair with specified supply, load, gain, and bandwidth makes a useful check. Estimate its bias, headroom, output swing, and dominant pole, and draw the separate jobs of the differential path and common-mode feedback. If transistor-level nodes can still be explained only through ideal-op-amp rules, multistage compensation is premature. Convergence warnings, missing models, startup behavior, and extreme operating regions also limit the claim; a simulator exiting cleanly does not cover them automatically.

Every row in the result table should trace back to a measurement definition. The loop break used for phase margin, the integration band used for noise, and whether power includes bias branches can all change the reported number. Two apparently better results are not directly comparable when those definitions differ.

## One small amplifier can display the real tradeoffs

Choose a two-stage op amp, OTA, or fully differential gain stage. State DC gain, gain-bandwidth product (GBW), phase margin, slew rate, output swing, input-referred noise, power, load, and an area proxy before sizing bias and compensation. Give each performance item its own testbench, followed by operating-point, AC, transient, noise, PVT, load-step, and startup or saturation cases. A sizing attempt in which higher bandwidth harms phase margin, swing, or power often explains the design better than the final nominal plot.

Add schematic, layout, DRC/LVS, and post-layout comparison only with a dependable and authorized open-PDK flow; stopping explicitly at pre-layout is valid. The more important test is whether a change in load or bias current leads, through current, transconductance, poles, and compensation capacitance, to a prediction about bandwidth, stability, swing, and power.

When specifications conflict, return to current paths and node capacitances instead of adding more sweep dimensions. One clear derivation of a tradeoff is usually closer to design work than dozens of unexplained sizing combinations.

## Layout, data converters, and RF change different parts of the problem

Once biasing, loop stability, and PVT behavior are explainable, the route can split. Layout is appropriate when parasitics, matching, floorplanning, and physical verification dominate. Mixed-signal or data-converter work begins when comparators, sampling, clocks, and digital calibration become central. RFIC begins when device \(f_T\), matching networks, noise figure, and distributed effects control the design.

One op amp does not establish all three branches. At the end of the spine, identify whether headroom, noise, stability, speed, power, or area limits the design first, then state which model or tool layer the next course will change. That answer is more useful than treating “completed a layout” as a universal finish line.

If the remaining problem cannot yet be separated into device modeling, the feedback network, or physical implementation, stay with the small amplifier. A branch course will not supply the missing causal explanation automatically.
