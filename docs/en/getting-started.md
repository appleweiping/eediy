---
title: How to Use This Guide
description: Choose a first course from your actual background, time, and laboratory access—and begin the work.
page_type: guide
comments: true
---


# How to Use This Guide

You do not need, and cannot reasonably expect, to finish every course in the navigation. This is not another degree plan. It is an annotated resource map: what a public course actually releases, what it assumes, whether assignments have feedback, what a lab requires, and what remains impossible to confirm from the public pages.

Do not begin with the question “Which specialization is hottest?” Before opening a course, write down the problem immediately in front of you: “I can solve DC networks but do not understand an RC response,” “I write C but have never read a datasheet,” or “I want to find out whether chip design genuinely interests me.” A precise problem makes it much easier to tell whether a course is helping.

## Locate your actual starting point

### You have just entered university or are early in an EE degree

Do not rush to route around your degree and assemble a supposedly stronger parallel curriculum. Calculus, linear algebra, physics, and basic circuits recur everywhere. Public courses work best as sources of better explanations, problems, and laboratories—not as a second full timetable.

If the shape of EE is still unclear, sample the system view in [MIT 6.01SC](courses/ee-introduction/019-6-01sc.md), then repair what the current semester needs through [mathematics foundations](math-foundations.md), [physics](courses/physics/index.md), and [circuits](courses/circuits/index.md). Reserve at least as much time for problems, simulation, or laboratory work as for watching instruction. A long playback history mostly proves familiarity.

### You are arriving from software, computer science, or another engineering field

Programming is a real advantage, but it does not replace circuits, continuous-time models, or physical scale. A common mistake is to make a development board blink and infer that power, interfaces, and measurement are understood.

Try three small questions. Derive the output of a loaded divider. Explain a first-order time constant. Explain how an oscilloscope's protective-earth connection can create a short circuit. If the first two fail, begin with [MIT 6.002](courses/circuits/021-6-002.md) and [mathematics foundations](math-foundations.md). If the third is unclear, read [Instrumentation and Measurement](guides/instrumentation-measurement.md) and [Laboratory Safety](guides/safety.md), and keep work in simulation or on a qualified low-energy teaching platform for now.

### You know the common core and are choosing a direction

Do not “systematically study” three tracks at once. Pick the closest candidate from the [learning routes](routes/index.md), inspect the assignments and projects in two or three representative courses, and only then commit.

Course titles matter less than the failures you are willing to investigate: bias and noise in analog work, timing and CDC on an FPGA, concurrency and peripherals in embedded systems, stochastic models in communications, modeling error in control, or boundary conditions in fields and waves. The kind of error you willingly chase to ground often predicts fit better than the lecture you enjoyed most.

### Your time or laboratory access is limited

Choose one main course from the [essential core](routes/essential-core.md). A lack of hardware does not prevent substantial work in mathematics, circuit analysis, SPICE, signal processing, HDL verification, control simulation, or public-data research. It does require the report to state which parasitic, noise, thermal, quantization, and manufacturing effects remain unmeasured.

Borrow, buy, or enter a laboratory when a defined task needs the instrument or board. Buying a bench first usually produces a bench full of components without a question.

## A five-minute prerequisite diagnostic

Do not treat “I took that class” as a prerequisite check. Use one small task with a checkable result. Attempt only the first column without looking up an answer. If it fails, repair the linked foundation; if it passes, continue toward the course closest to your goal.

| Attempt | Evidence that the foundation is usable | Repair first |
| --- | --- | --- |
| Write the node equation for a loaded divider and predict what happens as the load resistance falls | Equation, units, and limiting direction agree | [Mathematical foundations](math-foundations.md) and [circuits](courses/circuits/index.md) |
| Predict the initial value, final value, and time constant of an RC step from its first-order differential equation | You can sketch the qualitative waveform before simulation | [Differential equations](courses/mathematics/003-18-03sc.md) and [MIT 6.002](courses/circuits/021-6-002.md) |
| Explain where a sinusoid above Nyquist appears after sampling | The sampling, source, and alias frequencies have an explicit relationship | [Signals and systems](courses/signals-systems/index.md) |
| Draw a state diagram for “toggle an LED after button debouncing” and list edge cases | States, transitions, clock, and reset conditions are explicit | [Digital logic](courses/digital-logic/index.md) |
| Explain how to connect a meter for current and when an oscilloscope protective-earth lead can create a short | Stop conditions, ratings, and current limiting come before wiring | [Instrumentation and Measurement](guides/instrumentation-measurement.md) and [Laboratory Safety](guides/safety.md) |

This is not an exam, and no learner needs all five at the start. It prevents course titles, playback history, or familiarity with one tool from masquerading as a usable prerequisite.

## Choosing the first course

These are common first moves, not a rigid sequence:

| What you can do now | Open first | Why this is a useful start |
| --- | --- | --- |
| High-school mathematics is comfortable; university EE is new | [MIT 6.01SC](courses/ee-introduction/019-6-01sc.md) | See systems, signals, software, and hardware meet before deciding what to repair |
| Calculus or linear algebra is in progress; circuits are almost new | [MIT 6.002](courses/circuits/021-6-002.md) | Networks, dynamic components, and device models expose mathematical gaps quickly |
| Basic circuits are comfortable; filters and spectra are not | [MIT 6.003](courses/signals-systems/083-6-003.md) | Build the shared language of LTI systems, convolution, and transforms |
| You can program and want to approach digital hardware | [Nand2Tetris I](courses/digital-logic/039-nand2tetris-i.md) | Projects move from gates to a processor without an FPGA toolchain at the entrance |
| You want an MCU or sensor project | [Embedded Systems track](courses/embedded-systems/index.md) | Compare board, debugger, and laboratory dependencies before choosing the main line |
| The undergraduate core is already in place | [Track routes](routes/index.md) | Enter adjacent advanced courses by prerequisite and project evidence |

When two courses look equally plausible, open their first substantial assignments. Prefer the one whose assignment, feedback, or reference results you can actually obtain. A beautiful homepage and a complete video playlist do not replace a practice loop.

## What matters on a course page

Read the editorial course judgment before the resource inventory. Several details are easy to miss:

- **Mainline, alternative, and supplement describe relationships, not prestige.** Usually choose one mainline for a topic. An alternative changes style or access conditions; a supplement repairs a specific gap.
- **“Prerequisites and preparation” is not one blended list.** An “EEDIY recommended foundation” is an editorial route judgment. An “official prerequisite note” or “course-sequence requirement” records a provider condition; neither substitutes for the other.
- **Start with the course's own work.** Provider assignments, laboratories, and projects are linked directly. Any independent-study exercise added to fill a gap is labeled separately and never represented as an official requirement.
- **A rich resource inventory may still be a bad fit.** Prerequisites, language, region, licensing, hardware, and feedback determine whether the course can be completed.
- **The feedback links can supply experience missing from the article.** Learners can submit edition changes, environment failures, and actual workload. Each link carries the page, language, and stable ID so maintainers can verify the report.

For a factual error or dead link, use the matching GitHub report link at the bottom. For a complete learning report, consult the [contribution guide](contributing.md). A correction with a date and primary source is usually more helpful than “great course.”

## What it means to begin

Before designing a six-month plan, complete one small feedback loop:

1. Open the syllabus and the first substantial assignment; verify access, language, and tool conditions.
2. Name one question this unit should answer and any prerequisite gap already visible.
3. Complete a task that an answer, test, simulation, or measurement can correct.
4. Keep the original attempt and the reason for each correction, not only the polished result.
5. Decide whether to continue, repair a prerequisite, or change course, and record the reason in two or three sentences.

For an RC step problem, the evidence can be small: calculate the time constant, run one parameter sweep, plot a figure with units, and explain agreement or disagreement with the prediction. For HDL, it can be a self-checking test plus the failing waveform. Make this small loop work before expanding it into a course plan.

Use the [practice guides](guides/index.md) when code, environments, data, or reports need structure. Their tool lists are menus for a problem, not instructions to install everything.

## Hardware and laboratory boundaries

A passing simulation shows that a model is internally consistent under the chosen conditions. It does not establish that hardware will be safe or correct. Learn first connections in an environment with stated ratings, protection, and local supervision. Mains, high voltage, substantial stored energy, lasers, rotating machinery, vacuum systems, chemicals, and high-temperature processes are not “follow an online tutorial and see” activities.

When a course page marks the proposed work as simulation-only, do not extend it to physical equipment on your own. A course with official laboratories still remains subject to institutional, manufacturer, and laboratory safety rules. If the boundary is unclear, stop and use an isolated low-voltage platform, public data, or simulation. [Laboratory Safety](guides/safety.md) gives more specific stop conditions.

## Six things to do now

The state below stays only in this browser.

<div class="ee-checklist">
  <label><input type="checkbox" data-ee-check="question">I wrote down one EE problem I genuinely need to solve now.</label>
  <label><input type="checkbox" data-ee-check="starting-point">I chose an entry from my background, not from course prestige.</label>
  <label><input type="checkbox" data-ee-check="first-assignment">I verified that the first assignment, its feedback, and the required tools are accessible.</label>
  <label><input type="checkbox" data-ee-check="one-mainline">There is only one mainline course for this topic.</label>
  <label><input type="checkbox" data-ee-check="safe-scope">For hardware work, I know the ratings, supervision conditions, and stop boundaries.</label>
  <label><input type="checkbox" data-ee-check="first-evidence">I completed and saved one small task that can be corrected.</label>
  <div class="ee-checklist__footer">
    <span class="ee-check-progress" data-complete-label="complete" data-of-label="/"></span>
    <button class="ee-reset-progress" type="button">Clear this page</button>
  </div>
</div>

After the first five, close this guide and do the first problem. Return to check the sixth.
