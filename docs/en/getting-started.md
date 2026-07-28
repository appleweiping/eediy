---
title: Getting Started
description: Turn EE self-study into an executable plan with a diagnostic, time budget, and four-week launch.
---

<div class="ee-language" markdown>
[简体中文](../getting-started.md)
</div>

# Getting Started

A reliable plan answers four questions at once: **Where do I begin? What do I do each week? What proves completion? When do I change course?** Spend one month building the learning system before optimizing the number of courses.

## The 30-minute starting diagnostic { #start-diagnostic }

This is not an entrance examination. Mark each row “independent,” “need references,” or “unfamiliar,” and retain one real sample of your work.

| Capability | Ten-minute task | Minimum state before the mainline |
| --- | --- | --- |
| Mathematics | Simplify a complex fraction, differentiate a simple function, and explain a dot product | Show steps and check dimensions; speed is irrelevant |
| Physics | Sketch forces or fields for a simple system and explain where energy enters and leaves | Distinguish state, rate of change, and conservation |
| Programming | Load one data column, compute a mean, and plot it; use pseudocode if needed | Run, modify, and save a short script |
| Circuits | Write KCL/KVL for a resistor divider and predict the effect of a load | Understand nodes, voltage, current, and reference ground |
| Measurement | Plan how to measure an unknown DC voltage: range, leads, units, and hazards | Check ratings before making a connection |

Repair only the gaps that block the current goal. If you want to study linear circuits but have not learned differential equations, begin with DC resistive networks and learn differential equations alongside RC/RL transients. You do not need to finish all mathematics first.

## Choose a weekly cadence

| Available time | Suggested allocation | Realistic semester evidence |
| --- | --- | --- |
| 5 hours | Theory 2h + problems 2h + records 1h | Core units from one foundation course + one simulation project |
| 10 hours | Theory 3h + problems 3h + project 3h + review 1h | One mainline course + two small data-backed projects |
| 15 hours | Theory 4h + problems 4h + project 5h + review 2h | Mainline plus necessary co-requisite + one complete stage artifact |

Do not count video runtime as learning time. Derivation- and laboratory-heavy courses often need one to three hours of practice, debugging, and documentation per hour of presented material. Measure your own ratio and adjust.

## The four-week launch

### Week 1: establish the workbench

- Choose one four-week question from the [global roadmap](roadmap.md), such as “explain and verify a first-order RC transient.”
- Select one unit from one mainline course; do not start three equivalent courses.
- Create a log with date, goal, actual time, blocker, and next action.
- Install the minimum software. Start with simulation or a bounded low-energy platform instead of buying a complete bench.

**Weekly evidence:** one-page objective, environment inventory, and first executable notebook.

### Week 2: create feedback

- Finish a problem set with solutions, tests, or a comparable reference.
- Classify each important error: concept, model, algebra, code, instrument, or units.
- Cross-check one result with two kinds of evidence, such as hand analysis and simulation or simulation and safe low-energy measurement.

**Weekly evidence:** at least five corrected problems and an error classification table.

### Week 3: build a micro-project

- Express the target as inputs, outputs, constraints, and acceptance tests.
- Predict first, then simulate; connect hardware only after the safety gate.
- Retain raw data, plot-generation code, key parameters, and versions.

**Weekly evidence:** a minimal project that someone else can reproduce from the instructions.

### Week 4: oral exam and route adjustment

- Without notes, explain the model, assumptions, main equations, and failure causes in ten minutes.
- Redo one random problem and change one parameter to test transfer.
- Decide the next state: continue the mainline, repair a prerequisite, use an alternative, or pause an ill-fitting direction.

**Weekly evidence:** a one-page retrospective and the next four-week milestone.

## How to read a course page

Read “risks and gaps” before opening the course links:

1. **Outcomes:** confirm that the course solves your current problem.
2. **Prerequisites:** schedule hard requirements; keep recommended background as an on-demand list.
3. **Resource matrix:** verify that practice, solutions, labs, and assessment are actually public.
4. **Tools and cost:** prepare software, component, regional-access, and accessibility alternatives.
5. **Completion standard:** turn course expectations into your own milestone evidence.
6. **Verification date:** spot-check links that are beyond a reasonable review interval.

!!! tip "Mainline, alternative, and supplement are not additive"
    Choose one mainline for a topic. Alternatives replace the teaching style or resource conditions; supplements repair a specific gap. Three parallel sets of lectures usually consume the time needed for practice.

## Build learning evidence

Keep one minimal evidence package per stage:

```text
stage-name/
├── README.md          # Question, conclusion, reproduction
├── notes/             # Your derivations and concept maps
├── exercises/         # Representative work and corrections
├── src/               # Simulation, code, configuration
├── data/raw/          # Immutable raw measurements
├── data/processed/    # Rebuildable results
└── report/            # Plots, uncertainty, limits, next step
```

The exact folders are optional. The essential questions are not: Which version produced the result? Which parameters were used? Is the raw data preserved? How does another person reproduce it? What failed?

## Cost and alternatives

- **Software first:** verify that open or no-cost tools can cover the objective before accepting license lock-in.
- **Borrow before buying:** use institutional, makerspace, or shared instruments and complete local training.
- **Buy by module:** purchase around the current milestone, not a hypothetical future laboratory.
- **Estimate total cost:** include probes, adapters, protection, consumables, shipping, and replacements.
- **Preserve a no-hardware route:** every costly lab should have a simulation, public-data, or remote-lab evidence alternative.

## Your launch checklist

Checkbox state is stored only in this browser and can be cleared at any time.

<div class="ee-checklist">
  <label><input type="checkbox" data-ee-check="diagnostic">I completed all five diagnostic areas and saved a real sample.</label>
  <label><input type="checkbox" data-ee-check="time-budget">I reserved realistic weekly blocks, including review time.</label>
  <label><input type="checkbox" data-ee-check="milestone">I wrote a four-week verifiable artifact, not “learn a field.”</label>
  <label><input type="checkbox" data-ee-check="main-course">I selected only one mainline and read its gaps and prerequisites.</label>
  <label><input type="checkbox" data-ee-check="safety">For physical work, I passed the safety gate and confirmed facilities and supervision.</label>
  <label><input type="checkbox" data-ee-check="evidence">I created a log and raw-data area and know how to record failure.</label>
  <div class="ee-checklist__footer">
    <span class="ee-check-progress" data-complete-label="Complete" data-of-label="of"></span>
    <button class="ee-reset-progress" type="button">Clear page progress</button>
  </div>
</div>

Next: open the [global roadmap](roadmap.md) and choose exactly one stage exit criterion.
