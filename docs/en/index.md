---
title: Foreword
description: A systematic course map, learning roadmap, and project-practice guide for electrical engineering.
---

<p align="center">
  <img class="ee-home-mark" src="../assets/images/eediy-mark.png" alt="EEDIY mark combining a circuit, waveform, and open book" width="260" height="260">
</p>

# Foreword

Welcome to **EEDIY**, a systematic self-learning guide for electrical engineering. It begins with mathematics, physics, and programming, then moves into circuits, signals, digital systems, control, electromagnetics, energy, semiconductors, and related fields. Public courses are connected to exercises, experiments, and projects whose results can be inspected.

Electrical engineering is dense, and its branches depend on one another. The hard part is rarely finding a video. It is deciding whether the prerequisites are sound, the public materials are complete, the work produces feedback, and the experiment fits the available equipment and safety conditions. This guide therefore focuses on four things:

- **Course coverage:** organize public courses by discipline and distinguish mainline, alternative, and supplementary resources.
- **Route planning:** connect courses through prerequisites and milestone evidence instead of presenting an unstructured list.
- **Project practice:** require inspectable design, calculation, simulation, measurement, or review evidence at each stage.
- **Ongoing verification:** record open materials, access constraints, hardware needs, risk boundaries, and review dates.

## Where to begin

You do not need to read the whole site first. Choose the closest entry point, complete one small loop, and return to revise your route.

- Starting nearly from zero: complete the [starting diagnostic](getting-started.md), then repair algebra, trigonometry, calculus, basic physics, and computing foundations.
- Comfortable with mathematics and physics: enter through [Mathematical Foundations](math-foundations.md) and the [Global Roadmap](roadmap.md), using circuits and signals as the shared spine.
- Familiar with basic circuits: browse the [Course Catalog](courses/index.md), complete one analog, one digital or embedded, and one signal or control project, then choose a depth area.
- Working toward research or a role: trace the shortest prerequisite chain backward from a [Learning Route](routes/index.md), then organize evidence with the [Project Practice Guide](guides/projects.md).

## Electrical engineering is not one straight line

The branches share mathematical, physical, computational, and measurement foundations, then develop along different depth axes. Build a common language first, choose one or two primary directions, and retain interface-level literacy in the rest.

| Direction | Central question | Typical completion evidence |
| --- | --- | --- |
| Circuits and analog electronics | How do we trade noise, bandwidth, power, and nonlinearity? | Amplifier, filter, supply, and measurement report |
| Digital systems and FPGA | How does a behavioral specification become timing-correct hardware? | HDL module, verification bench, and timing report |
| Embedded and real-time systems | How do hardware and software cooperate under resource and timing limits? | Driver, data logger, and hardware-in-the-loop test |
| Signals, communications, and information theory | How do we recover information from incomplete, noisy observations? | DSP pipeline, link budget, and error-rate experiment |
| Control and robotics | How can a dynamic system remain stable, observable, and goal-directed? | Identification, controller, and closed-loop test |
| Electromagnetics, RF, and photonics | How do fields and waves propagate through structures, media, and frequency? | Field simulation, antenna, or passive-network analysis |
| Power and energy | How can energy be converted, transmitted, and managed safely and efficiently? | Converter simulation, thermal analysis, and protection plan |
| Semiconductors and integrated systems | How do materials and devices become manufacturable, verifiable systems? | Device model, layout checks, and PVT analysis |

[See the complete prerequisite and branch map](roadmap.md)

## How to judge whether a course is worth the effort

Every course page should answer these questions:

1. **What will I be able to do?** Outcomes must be explainable, calculable, designable, implementable, or measurable.
2. **What are the real prerequisites?** Separate hard requirements, knowledge that can be repaired in parallel, and optional background.
3. **What is actually public?** Check videos, notes, problems, solutions, labs, code, and exams separately.
4. **Where does feedback come from?** If solutions or autograding are absent, plan peer review, simulation, or measurement.
5. **What are the costs and constraints?** Surface paywalls, regional restrictions, old software, specialist hardware, and accessibility issues.
6. **When was it last verified?** External links and access policies change; stale information must be clearly marked.

A tier describes the **executability of the currently public edition for independent study**. It is not a ranking of institutions, instructors, or disciplines.

## A sustainable learning loop

1. **Define the evidence:** write what you will explain, calculate, design, or measure before choosing a course.
2. **Acquire the minimum theory:** build a model from notes, lectures, and derivations, including its assumptions and range of validity.
3. **Practice and implement:** attempt the work independently, then compare against solutions, simulation, or test data and classify errors.
4. **Measure and review:** retain raw data, versions, units, uncertainty, and failed attempts, then decide whether to continue, repair a prerequisite, or change route.

!!! danger "Read the safety guide before applying power"
    A lab appearing in course material does not make it suitable for a home setting. Mains electricity, energy-storage capacitors, high-power batteries, moving machinery, lasers, RF power, and high-temperature processes require facilities, training, and supervision matched to the risk. When the boundary is unclear, use simulation or a validated low-energy teaching platform. Read [Laboratory Safety](guides/safety.md) before starting.

## Start today

- Have 30 minutes: complete the [starting diagnostic](getting-started.md#start-diagnostic).
- Have one hour: select a four-week milestone from the [Global Roadmap](roadmap.md).
- Already taking a class: use its course page to find missing feedback or project work.
- Have a project idea: write a [one-page specification](guides/projects.md#project-spec) before buying parts.
- Found stale information: submit an evidence-backed correction through the [Contribution Guide](contributing.md).
