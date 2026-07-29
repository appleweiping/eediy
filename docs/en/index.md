---
title: Foreword
description: Turn public electrical-engineering courses into learning routes that can be judged, executed, and corrected.
---

<p align="center">
  <img class="ee-home-mark" src="../assets/images/eediy-mark.png" alt="EEDIY mark combining a circuit, waveform, and open book" width="260" height="260">
</p>

# Foreword

Public electrical-engineering courses are not scarce. What is scarce is a careful answer after someone has inspected the syllabus, assignments, solutions, laboratories, tool versions, and access conditions: can an independent learner actually complete this course, where does the path break, and when should they switch?

A playable video is not a self-contained course. A downloadable lab handout does not give you a course account, campus instruments, a private repository, or a safe bench. An older edition may have the best archive but depend on obsolete software. A current edition may still run while keeping feedback behind a login or paid service. EEDIY is concerned with these unglamorous details because they determine whether learning continues.

This site deliberately follows the editorial model of [CSDIY](https://csdiy.wiki/). The useful lesson is not merely its navigation or colors. It is the decision to treat each real course as an article worth maintaining: explain its resources, work, projects, experience boundary, and community corrections. EEDIY applies that model to electrical engineering and adds hardware cost, measurement evidence, and laboratory safety.

## Why another guide is still needed

A catalogue answers “what exists.” Once learning begins, the questions become specific:

- Problems are public, but are solutions or a grader public too? Without feedback, how can a learner tell a modeling error from an algebra error?
- A lab says “use an oscilloscope,” but does it also require a proprietary teaching platform, campus EDA, a licence, or instructor sign-off?
- Which edition is on the page? Has the current course been renamed, split, moved to another platform, or turned into a paid service?
- Which claim can simulation test, and which measurement, safety, or fabrication problem cannot be replaced by a polished plot?
- What should remain at the end: a first attempt and correction log, waveforms, raw data, layout checks, or a reproducible project report?

Every researched guide should answer these questions in a course-specific way. Reusing one calendar, project template, and set of compliments under a different course name does not count.

## Say what is known, and what is not

EEDIY is currently an open editorial project, not one author’s complete memoir of studying EE. It will not imitate personal writing by inventing “I took this” or “I struggled here.” Pages distinguish three states:

| State | What it establishes | What it does not yet establish |
| --- | --- | --- |
| Catalogue | Course identity, official entry points, material scope, and obvious limits were checked | The assignments were not audited in depth, so the page is not a standalone recommendation |
| Researched | The syllabus, structure, work, labs, exams, and version were reviewed against primary sources | Without a learner record, it does not claim real workload or first-hand experience |
| Learner-reviewed | A traceable completion scope, artifacts, time record, and sticking points were reviewed | One learner’s experience still does not become a universal rule |

This boundary leaves some pages deliberately short. That is more honest than presenting generated prose as a mature recommendation. Course-page discussions and structured reports are how desk research can become real learning evidence.

## Where to begin

Do not read the whole site first. Choose the entry nearest to your current position, complete one small loop, then revise the route.

- Starting nearly from zero: take the [starting diagnostic](getting-started.md) and find the first break in algebra, trigonometry, calculus, physics, or computing.
- Comfortable with mathematics and physics: enter through [Mathematical Foundations](math-foundations.md) and the [Global Roadmap](roadmap.md), using circuits and signals as the shared spine.
- Familiar with basic circuits: open the [Course Catalogue](courses/index.md) and compare one theory course with one practice course that has a feedback path; do not choose by institution or tier alone.
- Working toward research or a role: trace the shortest prerequisite chain backward from a [Learning Route](routes/index.md), then specify reviewable artifacts with the [Project Practice Guide](guides/projects.md).

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

## The freedom and cost of self-study

The advantage of self-study is straightforward. A learner can pause, replay, choose another instructor’s explanation, and spend several days on a model that is genuinely unclear instead of being pulled along by a term schedule. Open courses also make it possible to compare how different institutions frame the same subject, which is especially valuable across device, system, and software boundaries.

The cost is equally direct. There may be no teaching assistant, peers, common bench, or hidden tests. Failing to notice an error is often more dangerous than being unable to start. EE adds a physical limit: some work requires expensive instruments, controlled fabrication, or trained supervision and cannot be supplied by persistence alone. These routes do not replace a university laboratory, instructor feedback, or formal qualification. They help distinguish what is publicly executable, what needs different evidence, and where a learner should stop.

## A course page should speak plainly

Look for six things on a course page:

1. Real lectures, units, assignments, labs, exams, or projects—not course marketing.
2. A comparison with nearby alternatives: what fits a first pass, repair work, or an advanced pass?
3. The actual boundary of solutions, graders, staff feedback, equipment, and software.
4. A diagnostic before starting and a precise prerequisite repair when it fails.
5. Concrete completion artifacts, with EEDIY supplements distinguished from official work.
6. Version, login, payment, licence, and safety limits, plus the latest review date.

A tier describes the **executability of the currently public edition for independent study**. It is not a ranking of institutions, instructors, or disciplines.

!!! danger "Read the safety guide before applying power"
    A lab appearing in course material does not make it suitable for a home setting. Mains electricity, energy-storage capacitors, high-power batteries, moving machinery, lasers, RF power, and high-temperature processes require facilities, training, and supervision matched to the risk. When the boundary is unclear, use simulation or a validated low-energy teaching platform. Read [Laboratory Safety](guides/safety.md) before starting.

## Discussion, correction, and real learning records

Each course page uses a stable course ID so its Chinese and English versions point to the same public record. Report broken links, edition changes, assignment structure, and first-hand sticking points, or share learning artifacts that do not contain answers. Factual corrections need primary evidence; experience reports need a completion scope. Credentials, private contact details, restricted answers, and unlicensed copies do not belong in comments.

Once verified, a correction should return to the article instead of remaining buried in a thread. See the [Contribution Guide](contributing.md) for the review process.

## Start today

- Have 30 minutes: complete the [starting diagnostic](getting-started.md#start-diagnostic) and repair only the first failed item.
- Already taking a course: use its page to identify whether the missing piece is work, feedback, tooling, or laboratory access.
- Have a project idea: write a [one-page specification](guides/projects.md#project-spec) before buying parts.
- Found an inaccurate claim: choose the closest report type at the bottom of the course page and attach evidence.
