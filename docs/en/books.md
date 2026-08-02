---
title: Recommended EE Books
description: A curated shelf for electrical engineering, with intended level, practical use, and legitimate access routes.
page_type: guide
comments: true
last_reviewed: 2026-08-02
---


# Recommended EE Books

This is not a shelf to buy in one pass. Circuits, fields, devices, signals, and control demand different kinds of intuition, and one book rarely teaches theory, design, and laboratory work equally well. Each recommendation below says what the resource does especially well, when it becomes useful, and where to obtain it legitimately. Full-text links point only to material released by the author, publisher, or institution; commercial books link to their official pages rather than unofficial copies.

Do not start five books in parallel. Pick one primary text, pair it with a [public course](courses/index.md) that has exercises or laboratories, and consult a second book only for a named problem. A derivation should eventually meet a calculation, simulation, or measurement; otherwise, recognition can easily masquerade as understanding.

## Circuit foundations and the electronics bench

- **[Lessons in Electric Circuits / All About Circuits](https://www.allaboutcircuits.com/textbook/)** (open online text)
  The collection runs from DC and AC through semiconductors, digital circuits, instrumentation, and safety. It is searchable and rich in worked explanations, which makes it a good first repair manual for terminology or a concept to check before a build. Its mathematical depth is limited; after nodal analysis, transients, and frequency response, move to a full circuit-analysis course.

- **[The Art of Electronics, 3rd ed.](https://www.book2look.com/book/9780521809269)** (Cambridge publisher preview; print edition is paid)
  This book is interested in what real components do when connected. Device choice, noise, precision circuits, interfaces, and practical failure modes are its strengths. It is not the gentlest first circuit-theory text: learn linear circuits first, then use it by topic while designing or debugging rather than trying to memorize it cover to cover.

- **[Learning the Art of Electronics, 2nd ed.](https://www.cambridge.org/core/books/learning-the-art-of-electronics/9B9FA2FE6B1802BD4627B1F9825E8F0A)** (publisher page; paid)
  Choose the companion laboratory book when the missing ingredient is experimental practice. The new edition spans analog work, FPGA exercises, and an ARM microcontroller. Check the required instruments, parts, and safety conditions before starting; a laboratory sequence cannot be reduced to a paper exercise when the necessary bench is unavailable.

- **[Foundations of Analog and Digital Electronic Circuits](https://shop.elsevier.com/books/foundations-of-analog-and-digital-electronic-circuits/agarwal/978-0-08-050681-4)** (publisher page; paid, with some official companion material open)
  Agarwal and Lang move from the circuit abstraction, resistive networks, and network theorems through MOSFETs, small-signal models, transients, sinusoidal steady state, and operational amplifiers. The result is a complete undergraduate circuit-analysis spine and the text used by MIT 6.002. Its special strength is a shared abstraction language for analog and digital work. A learner seeking many traditional network-theorem exercises or three-phase circuits still needs the corresponding course. Pair each chapter with the 6.002 problems rather than reading concepts alone.

## Instruments, probing, and measurement uncertainty

- **[XYZs of Oscilloscopes Primer](https://www.tek.com/en/documents/primer/xyzs-oscilloscopes-primer)** (open manufacturer primer)
  Waveforms, oscilloscope architectures, bandwidth, sampling, triggering, and basic measurements are introduced for a first encounter with the instrument. This is a Tektronix primer, not an independent metrology text; product-selection claims and features must be checked against the manual for the instrument actually used. After reading, you should be able to distinguish bandwidth from rise time and sample rate from record length, then choose a vertical range and timebase in advance for a known low-voltage signal.

- **[ABCs of Probes Primer](https://www.tek.com/en/documents/whitepaper/abcs-probes-primer)** (open manufacturer probing guide)
  A probe is not a transparent wire. This guide places input resistance, tip capacitance, bandwidth, rise time, ground-lead inductance, differential and current probes, and safety ratings in one measurement chain. Read it beside a low-voltage, isolated RC or pulse source with known parameters: predict loading first, then compare ground lengths or attenuation settings. High-voltage, floating, or power measurements still require the proper equipment category, ratings, and qualified supervision.

- **[JCGM 100:2008 — Guide to the Expression of Uncertainty in Measurement](https://www.bipm.org/en/committees/jc/jcgm/publications)** (official open BIPM/JCGM guide)
  The GUM is not an instrument manual. It is the long-lived reference for asking what a reported measurement actually supports: defining the measurand, identifying inputs, treating standard uncertainties and correlation, combining uncertainty, and reporting the result. A first pass can skip the deeper appendices. Build an uncertainty model for one voltage or cutoff-frequency measurement and distinguish resolution, accuracy, repeatability, and calibration information. Do not replace the actual instrument manual or reduce the method to adding every error bound.

## Mathematics, probability, and optimization

- **[Introduction to Applied Linear Algebra: Vectors, Matrices, and Least Squares](https://stanford.edu/~boyd/vmls/)** (authorized open full text)
  Linear algebra is organized around least squares, fitting, and engineering applications, with videos, extra exercises, and Python/Julia companions. It is a strong way to learn what matrices accomplish before signals, control, or estimation. A proof-heavy course is still needed later for deeper spectral theory.

- **[Introduction to Probability, Statistics, and Random Processes](https://www.probabilitycourse.com/)** (open full text)
  Undergraduate probability, statistics, random processes, and random signals share one notation, supported by short videos, calculators, and a Python simulation chapter. It makes a coherent runway into communications, noise, and estimation. Do not jump from elementary counting straight to random processes; conditional probability and multivariate random variables are load-bearing prerequisites.

- **[Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/)** (authorized open full text)
  This belongs after multivariable calculus and linear algebra, when control, signal recovery, communication resource allocation, or circuit optimization creates a real need. Study convex sets, convex functions, duality, and KKT conditions, then reproduce one small application. It is neither a zero-background math introduction nor a catalogue of solvers to invoke blindly.

## Signals, DSP, and feedback

- **[Signals and Systems, 2nd ed.](https://www.pearson.com/en-gb/subject-catalog/p/signals-and-systems-pearson-new-international-edition/P200000005151)** (publisher page; paid)
  Oppenheim, Willsky, and Nawab develop continuous- and discrete-time systems in parallel, from LTI models, convolution, and Fourier representations through sampling, Laplace and Z transforms, and feedback. It is a standard undergraduate spine for the shared language needed by communications, control, and DSP, with more mathematical demand than the DSP Guide below. Do not memorize transform tables in isolation: represent each system in time, frequency, and pole-zero form, then use problems to check causality, stability, and the region of convergence.

- **[The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/)** (author-released full text)
  Sampling, convolution, spectra, digital filters, and the FFT are explained with abundant figures and engineering language. Use it to build intuition or locate a technique quickly during a project. The book deliberately lowers the mathematical barrier; communications, estimation, or research-level DSP still requires rigorous work with complex exponentials, the DTFT, the Z-transform, and random signals.

- **[Feedback Systems: An Introduction for Scientists and Engineers, 2nd ed.](https://fbswiki.org/wiki/index.php/Feedback_Systems:_An_Introduction_for_Scientists_and_Engineers)** (publisher-authorized open full text)
  Åström and Murray connect modeling, time response, frequency-domain design, robustness, and system architecture. The site also carries chapter PDFs, examples, FAQs, errata, and Python figure sources. Complete one low-order model–analysis–controller–simulation loop before the robustness chapters; applying a memorized PID recipe is not yet feedback design.

## Digital logic and computer architecture

- **[The Elements of Computing Systems / Nand2Tetris](https://www.nand2tetris.org/)** (book paid; courses, software, and projects open)
  A continuous project chain starts with NAND, HDL, and a CPU, then climbs to an assembler, compiler, and operating system. Its special value is showing how abstraction layers meet. It does not go deeply into FPGA timing closure, clock-domain crossings, bus protocols, or physical implementation; after the hardware half, continue with a [digital logic](courses/digital-logic/index.md) or [FPGA/SoC](courses/fpga-soc/index.md) course.

- **[Digital Design and Computer Architecture: RISC-V Edition](https://shop.elsevier.com/books/digital-design-and-computer-architecture-risc-v-edition/harris/978-0-12-820064-3)** (publisher page; paid, some companion resources open)
  Combinational and sequential logic, SystemVerilog/VHDL, the RISC-V ISA, single-cycle, multicycle, and pipelined processors, and memory hierarchy sit on one path. It suits a reader who can already program and wants to move from RTL to a processor. The companion site includes HDL, labs, and slides; run the simulations and inspect waveforms instead of treating the code as illustrations.

## Embedded systems

- **[Making Embedded Systems, 2nd ed.](https://www.oreilly.com/library/view/making-embedded-systems/9781098151539/)** (publisher page; paid or subscription)
  The focus is not one board's register map but architecture, state machines, interrupts, concurrency, error handling, debugging, and power under resource constraints. It works best after you can write C and bring up a board. Refactor a small polling project into something observable and testable while reading; collecting pattern names alone misses the point.

## Semiconductor devices and integrated circuits

- **[Fundamentals of Microelectronics, 3rd ed.](https://bcs.wiley.com/he-bcs/Books?action=index&bcsId=12028&itemId=1119694396)** (official publisher companion site; text paid)
  Razavi moves from semiconductor foundations, diodes, and bipolar and MOS devices into single-stage and differential amplifiers, frequency response, feedback, oscillators, and power amplifiers. It supplies the undergraduate bridge between knowing devices and analyzing complete microelectronic circuits. The official companion site lists equations, figures, laboratories, videos, and selected problem resources by chapter; access must still be checked item by item. Do not start it in parallel with the advanced CMOS-design text below. First close the analysis loop here with problems and SPICE checks.

- **[Modern Semiconductor Devices for Integrated Circuits](https://www.chu.berkeley.edu/modern-semiconductor-devices-for-integrated-circuits-chenming-calvin-hu-2010/)** (author page; chapters open)
  Chenming Hu gives a compact path through junctions, the MOS capacitor, MOSFETs, scaling, and device limits. It is a good entrance to microelectronics after basic electromagnetics and solid-state physics. Do not only memorize band diagrams: connect each device equation and operating region to an observable I–V or C–V curve.

- **[Design of Analog CMOS Integrated Circuits, 2nd ed.](https://www.mheducation.com/highered/product/design-of-analog-cmos-integrated-circuits-razavi.html)** (publisher page; paid)
  Razavi moves from MOS intuition through single-stage amplifiers, differential pairs, mirrors, frequency response, noise, feedback, op-amps, and PLLs. It is a primary analog-IC text after introductory microelectronic circuits. Give every chapter a working SPICE testbench and check bias, swing, gain-bandwidth, and process corners; equations alone do not create design judgment.

- **[CMOS VLSI Design: A Circuits and Systems Perspective, 4th ed.](https://www.pearson.com/en-us/subject-catalog/p/cmos-vlsi-design-a-circuits-and-systems-perspective/P200000003427/9780137981076)** (publisher page; paid)
  CMOS gates lead into delay, power, interconnect, datapaths, memory arrays, and systems on chip. It is a good second step in digital VLSI, but not a replacement for HDL and synthesis work. Pair logical effort, delay estimates, or power models with results from an actual synthesis or layout flow.

## Communications and information theory

- **[Fundamentals of Wireless Communication](https://web.stanford.edu/~dntse/wireless_book.html)** (publisher-permitted author version)
  Tse and Viswanath use channels, detection, capacity, multiuser communication, and MIMO to connect probability, information theory, and system design. This is a graduate-level wireless text, not a first communications course. Stabilize random variables, linear systems, baseband representation, and AWGN detection before fading and MIMO.

- **[Information Theory, Inference, and Learning Algorithms](https://www.inference.org.uk/mackay/itila/)** (author-released full text)
  MacKay places coding, Bayesian inference, and learning algorithms in one unusually broad and lively frame. It is useful once probability is secure and the connection among information, inference, and coding is the question. For a standard communications route, follow entropy, typicality, channel capacity, and coding theorems first; the neural-network and statistical-physics branches can wait.

## Electromagnetics, microwave engineering, and photonics

- **[Electromagnetic Field Theory: A Problem-Solving Approach](https://ocw.mit.edu/courses/res-6-002-electromagnetic-field-theory-a-problem-solving-approach-spring-2008/pages/textbook-contents/)** (MIT OpenCourseWare full text)
  Vector analysis, electrostatics, boundary-value problems, induction, waves, transmission lines, waveguides, and radiation appear in one sequence, with problems and selected answers on the same page. It rewards a willingness to solve boundary conditions. Drawing the geometry, normals, and material regions correctly matters more than memorizing Maxwell's equations in isolation.

- **[Microwave Engineering, 4th ed.](https://bcs.wiley.com/he-bcs/Books?action=index&bcsId=6874&itemId=0470631554)** (publisher companion page; text paid)
  Pozar is a classic bridge from fields to microwave networks, matching, couplers, filters, and active circuits. Transmission lines, complex power, and S-parameters should already be familiar. Smith-chart and matching exercises belong beside calculation or simulation, not as copied graphical rituals.

- **[RP Photonics Encyclopedia](https://www.rp-photonics.com/encyclopedia.html)** (open online reference)
  Lasers, fibers, nonlinear optics, optical communication, optoelectronic devices, and measurement are covered with definitions and further literature. This is a continuously maintained, expert-authored encyclopedia rather than a week-by-week course. Use it to answer a precise question, then return to a systematic text or paper for the full derivation.

## Power electronics, machines, and power systems

- **[Fundamentals of Power Electronics, 3rd ed.](https://link.springer.com/book/10.1007/978-3-030-43881-4)** (publisher page; paid)
  Intended for senior undergraduate and early graduate study, it develops converter steady state, switching devices, magnetics, control, and design tradeoffs. Verify volt-second and ampere-second balance and a small-signal model in simulation or on an isolated low-voltage platform. A topology analysis in a book is not authorization to work on mains or high-energy storage.

- **[Electric Machines and Drives: A First Course](https://bcs.wiley.com/he-bcs/Books?action=contents&bcsId=7010&itemId=1118074815)** (publisher companion page; text paid)
  Electromechanical conversion, magnetic circuits, DC and AC machines, space vectors, and drive control form the first machine-and-drive path. It fits after three-phase circuits and introductory control. Use a bounded simulation or teaching rig to connect torque-speed curves, losses, and controller limits to the equations.

- **[Electric Power Systems: A First Course](https://bcs.wiley.com/he-bcs/Books?action=index&bcsId=7091&itemId=1118074793)** (publisher companion page; text paid)
  This is an entry to the system view: three-phase networks, transformers, transmission, power flow, faults, and stability. It does not compete with power electronics—the former explains grid power and constraints, while the latter explains converters. Any mains, grid-connected, or high-voltage work belongs in a qualified laboratory under supervision.

## Robotics and mechatronic systems

- **[Modern Robotics: Mechanics, Planning, and Control](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)** (author site with an open preprint, videos, exercises, and code)
  Rigid-body motion, kinematics, dynamics, trajectories, planning, control, grasping, and mobile robots share a consistent notation, with Python, MATLAB, and Mathematica code. It is a systematic entrance after linear algebra, calculus, and basic mechanics. A physical robot still demands motor drives, sensors, real-time software, and a safe-stop design in parallel.

## Turning one recommendation into a study plan

With no chosen direction, begin with **All About Circuits plus one circuit course**. For digital hardware, use **Nand2Tetris → Digital Design and Computer Architecture**. For signals or control, establish differential equations, LTI systems, and linear algebra through **18.03/6.003 plus 18.06**, then move to DSP Guide or Feedback Systems. Add probability when the work reaches noise, estimation, random inputs, or communications. For chips, stabilize **circuits plus devices** before splitting toward Razavi or Weste/Harris.

Then make one small commitment: name the chapters, associated problems, and one verification task. For example: “Read Chapter 2 of Feedback Systems, reproduce two first-order models, plot one closed-loop response, and explain its steady-state error.” After one representative chapter–problem–verification loop, if you can repeat the prose but cannot independently build a model or reproduce the result, narrow the scope, repair the prerequisites, or move to a course with feedback instead of adding another book.

Editions, prices, regional availability, and companion resources change. Check the author or publisher page before buying. If a link dies, an edition changes, or a better legitimate access route appears, leave a comment below or propose a correction through the [contribution guide](contributing.md).
