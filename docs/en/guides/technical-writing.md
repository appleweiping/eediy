---
title: Technical Writing and Design Review
description: Create verifiable, maintainable EE documents from requirements, evidence, figures, and decision records.
---

<div class="ee-language" markdown>
[简体中文](../../guides/technical-writing.md)
</div>

# Technical Writing and Design Review

Engineering documentation helps a reader decide, reproduce an experiment, or operate a system safely. Decorative terminology cannot replace clear requirements, evidence, and limits. Identify the reader’s action first, then choose a report, design note, or procedure structure.

## Purpose and learning outcomes

- Write requirements as testable statements with units, tolerance, and verification method.
- Separate observation, calculation, inference, decision, and action item.
- Make figures, tables, equations, and citations independently understandable and traceable.
- Record alternatives, tradeoffs, risks, and stop conditions.
- Use peer review to find ambiguity and irreproducible steps.

## Minimal environment

- A text format that supports headings, links, code, and figure references.
- Version control plus spelling and link checks.
- One completed safe, low-risk experiment or design.
- A path to PDF or static web output while the source remains reviewable text.

Record build-tool and template versions. Fonts and layout are not core evidence; published output must retain selectable text, navigable headings, and image alternatives.

## Learning sequence

1. **Reader and action:** state who reads, what they decide, their background, and success criteria.
2. **Conclusion first:** give the conclusion and applicability before method and evidence.
3. **Requirements:** include object, condition, threshold, unit, and verification method in each.
4. **Evidence structure:** place figures near interpretation, name object and conditions, and cite primary sources.
5. **Decision record:** list alternatives, tradeoffs, risks, assumptions, and the reason for the choice.
6. **Executable review:** ask a reviewer to reproduce one step and record every blockage.

## Verification task: one-page design review

Choose a completed small-signal filter or digital module:

1. Write one problem statement, three testable requirements, and one non-goal.
2. Support the conclusion with one unit-labeled plot and one compact result table.
3. Link raw data, generation command, and design revision.
4. Compare two alternatives and state choice, cost, and residual risk.
5. Name one test that would overturn the current conclusion.
6. Ask another learner to execute verification from the document alone and fix one ambiguity.

Acceptance requires a reader to find input, run command, expected result, and failure response without oral context.

## Common failures and diagnosis

- **The opening gives background but no conclusion:** put the decision, scope, and key number first.
- **A requirement says “good performance”:** add metric, condition, threshold, unit, and verification.
- **A figure is meaningless outside the paragraph:** add a descriptive caption, legend, data source, and textual conclusion.
- **Precision looks stronger than evidence:** limit significant digits by measurement or model uncertainty.
- **Steps skip what is “obvious”:** have an unfamiliar reader execute them and record every hidden assumption.
- **Documentation drifts from implementation:** generate parameters and figures from one authoritative source and check them in CI.

## Reproducible evidence

- Document source, build command, and published artifact.
- Reader, purpose, scope, and term definitions.
- Traceability from requirements to tests.
- Figure data ID, script, parameters, and revision.
- Stable citation identifiers and access dates.
- Alternatives, decision, risks, and open questions.
- Review comments, dispositions, and change record.

## Cost, licensing, and accessibility

A text workflow can use free tools. Check licenses for templates, fonts, icons, images, and cited material; permission to cite is not permission to copy full text. Offer an open format or web page so readers do not need paid editing software.

Use semantic headings, meaningful link text, sufficient contrast, and image alternatives. Do not express relationships only by color, location, or “see above.” Define equation variables, avoid overly wide tables, and accompany video demonstrations with written steps.

## Safety boundaries

- Procedures must state ratings, prechecks, stop conditions, and fail-safe state.
- Do not publish secrets, personal data, controlled hardware details, or uncoordinated vulnerabilities.
- Documentation does not replace institutional training, manufacturer manuals, or qualified supervision.
- A qualified reviewer must check higher-energy procedures.
- When evidence is missing, write “not verified” rather than filling the gap with certainty.

## Completion checklist

- [ ] Reader, action, scope, and non-goals are explicit.
- [ ] Every requirement has condition, threshold, unit, and verification.
- [ ] The conclusion and key limits are visible at the beginning.
- [ ] Figures are traceable, accessible, and explained in text.
- [ ] Facts, inference, decisions, and actions are separated.
- [ ] An unfamiliar reader has exercised the build and reproduction steps.
- [ ] Licensing, privacy, and safety reviews are complete.
- [ ] Review comments and dispositions remain in version history.

Next, prevent document drift with [Reproducible Engineering](reproducibility.md), or strengthen evidence through [Literature Search](literature-research.md).
