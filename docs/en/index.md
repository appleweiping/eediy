---
title: EE Self-Learning Guide
description: Build a verifiable, reproducible, and safety-aware path through Electrical Engineering.
hide:
  - toc
---

<div class="ee-language" markdown>
[简体中文](../index.md)
</div>

<section class="ee-hero">
  <div class="ee-hero__copy">
    <p class="ee-kicker">EEDIY · Learn · Build · Measure</p>
    <h1>Learn electrical engineering as a working system</h1>
    <p class="ee-hero__lead">Start with mathematics, physics, and programming; move into circuits, signals, digital systems, control, electromagnetics, and energy. Every step connects to public resources, inspectable outcomes, and an explicit safety boundary.</p>
    <div class="ee-hero__actions">
      <a class="ee-button ee-button--primary" href="getting-started/">Build your first study plan</a>
      <a class="ee-button ee-button--secondary" href="roadmap/">Explore the global roadmap</a>
    </div>
  </div>
  <div class="ee-hero__visual">
    <img class="ee-hero__mark" src="../assets/images/eediy-mark.png" alt="EEDIY mark combining a circuit, waveform, and open book" width="1254" height="1254">
  </div>
</section>

<div class="ee-proof">
  <div class="ee-proof__item">
    <strong>Evidence first</strong>
    <span>Separate course marketing, genuinely open materials, and a completable feedback loop.</span>
  </div>
  <div class="ee-proof__item">
    <strong>Project driven</strong>
    <span>Completion means designing, measuring, reviewing, and recording—not merely watching.</span>
  </div>
  <div class="ee-proof__item">
    <strong>Safety gated</strong>
    <span>Simulation, bounded low-energy work, and supervised activities are labeled separately.</span>
  </div>
</div>

## Where are you now?

You do not need to read the entire site first. Choose the closest entry point, complete one small learning loop, and return to revise the route.

<div class="ee-card-grid">
  <article class="ee-card">
    <span class="ee-tag">0–3 months</span>
    <h3>Starting nearly from zero</h3>
    <p>Build algebra, trigonometry, single-variable calculus, basic mechanics and electromagnetism while learning to compute with Python. Your first artifact should be a measurement or simulation notebook with units, uncertainty, and plots.</p>
    <p><a href="getting-started/#the-four-week-launch">Run the four-week launch →</a></p>
  </article>
  <article class="ee-card">
    <span class="ee-tag">3–12 months</span>
    <h3>Comfortable with math and physics</h3>
    <p>Use linear circuits and signals as the spine. Put differential equations, complex numbers, and linear algebra into real problems while learning SPICE, instrument reasoning, and technical reporting.</p>
    <p><a href="roadmap/#shared-core">Enter the shared core →</a></p>
  </article>
  <article class="ee-card">
    <span class="ee-tag">Choose a direction</span>
    <h3>Basic circuits, no specialization yet</h3>
    <p>Complete one analog project, one digital or embedded project, and one signal or control project. Compare whether devices, systems, algorithms, or physical fields hold your attention.</p>
    <p><a href="roadmap/#direction-sampling">Explore directions →</a></p>
  </article>
  <article class="ee-card">
    <span class="ee-tag">Research / work</span>
    <h3>Foundations in place, evidence missing</h3>
    <p>Work backward from a research question or role. Fill the shortest prerequisite chain, then deliver a reproducible experiment, design review, test data, and failure analysis. Course count is not the target.</p>
    <p><a href="guides/projects/#project-evidence-package">Build an evidence package →</a></p>
  </article>
</div>

## Electrical engineering is not one straight line

Every direction shares mathematical, physical, computational, and measurement foundations, then develops a different depth axis. Build a common language first, choose one or two primary directions, and keep interface-level literacy in the rest.

| Direction | Central question | Shared prerequisite anchors | Typical evidence |
| --- | --- | --- | --- |
| Circuits and analog electronics | How do we trade noise, bandwidth, power, and nonlinearity? | Circuits, differential equations, devices | Amplifier, filter, supply, and measurement report |
| Digital systems and FPGA | How does a behavioral specification become timing-correct hardware? | Logic, C/scripting, architecture basics | HDL module, verification bench, timing report |
| Embedded and real-time systems | How do hardware and software cooperate under resource and timing limits? | Digital systems, C, interfaces, instruments | Driver, data logger, hardware-in-the-loop test |
| Signals and communications | How do we recover information from incomplete, noisy observations? | Linear algebra, probability, signals | DSP pipeline, link budget, error-rate experiment |
| Control and robotics | How can a dynamic system remain stable, observable, and goal-directed? | Differential equations, linear algebra, programming | Identification, controller, closed-loop test |
| Electromagnetics, RF, and photonics | How do fields and waves propagate through structures, media, and frequency? | Multivariable calculus, electromagnetism, complex numbers | Field simulation, antenna or passive-network analysis |
| Power and energy | How can energy be converted, transmitted, and managed safely and efficiently? | Circuits, electromagnetism, control | Converter simulation, thermal analysis, protection plan |
| Semiconductors and integrated systems | How do materials and devices become manufacturable, verifiable systems? | Quantum/solid-state basics, devices, circuits | Device model, layout checks, PVT analysis |

[See the complete prerequisite and branch map](roadmap.md){ .ee-button .ee-button--secondary }

## What should a course record answer?

A course page is not a bag of links. Before starting, it should let you answer six questions:

1. **What will I be able to do?** Outcomes must be observable, not a restatement of the title.
2. **What are the real prerequisites?** Separate hard requirements, co-learning, and optional background.
3. **What is actually public?** Check videos, notes, problems, solutions, labs, code, and exams separately.
4. **Where does feedback come from?** If solutions or autograding are absent, plan peer review, simulation, or measurement.
5. **What are the costs and constraints?** Surface paywalls, regions, old software, specialist hardware, and accessibility.
6. **When was it verified?** External links and access policies change; stale information must be marked.

### Resource roles and evidence tiers

| Label | Meaning | How to use it |
| --- | --- | --- |
| Mainline | Resources and practice form a complete learning spine | Follow in order and retain milestone evidence |
| Alternative | Similar outcomes with a different style, cost, or resource structure | Choose one based on language, pace, tools, and background |
| Supplement | Exceptional for one concept, lab, or perspective | Use on demand; do not replace the main feedback loop |
| S | Highly complete for independent study; critical public materials verified | Suitable as a stage backbone |
| A | Strong teaching with a small number of explicit gaps | Read the gap note and plan a compensating activity |
| B | Valuable but missing a complete teaching or feedback spine | Use only alongside an established mainline |

A tier describes the **executability of the currently public edition for self-study**. It is not a ranking of institutions, instructors, or disciplines.

## A sustainable learning loop

<div class="ee-route">
  <div class="ee-route__stage">
    <div>
      <h3>Define the evidence</h3>
      <p>Write what you will explain, calculate, design, or measure before choosing a course. Do not infer the goal from playlist length.</p>
    </div>
  </div>
  <div class="ee-route__stage">
    <div>
      <h3>Acquire the minimum theory</h3>
      <p>Use notes, lectures, and derivations to build a model. Mastery includes assumptions and the range in which the model applies.</p>
    </div>
  </div>
  <div class="ee-route__stage">
    <div>
      <h3>Practice and implement</h3>
      <p>Attempt work independently, then compare with solutions, simulation, or test data. Classify errors as conceptual, modeling, computation, tooling, or experimental.</p>
    </div>
  </div>
  <div class="ee-route__stage">
    <div>
      <h3>Measure and review</h3>
      <p>Keep raw data, versions, units, uncertainty, and failed attempts. Use a one-page review to continue, repair a prerequisite, or change route.</p>
    </div>
  </div>
</div>

!!! danger "Read the safety guide before applying power"
    A lab appearing in course material does not make it suitable for a home setting. Mains electricity, energy-storage capacitors, high-power batteries, moving machinery, lasers, RF power, and high-temperature processes require facilities, training, and supervision matched to the risk. When the boundary is unclear, use simulation or a validated low-energy teaching platform. Read [Laboratory Safety](guides/safety.md) first.

## Start today

- Have 30 minutes: complete the [starting diagnostic](getting-started.md#start-diagnostic).
- Have one hour: select a four-week milestone from the [global roadmap](roadmap.md).
- Already taking a class: use the course-record fields to find its missing feedback or project loop.
- Have a project idea: write a [one-page specification](guides/projects.md#project-spec) before buying parts.
- Found stale information: submit an evidence-backed correction through the [contribution guide](contributing.md).
