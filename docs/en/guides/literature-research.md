---
title: Literature Search and Evidence Evaluation
description: Build a reviewable EE research process from question decomposition, source tiers, and an evidence matrix.
---

<div class="ee-language" markdown>
[简体中文](../../guides/literature-research.md)
</div>

# Literature Search and Evidence Evaluation

Research is not collecting the most links. It finds enough evidence to support or overturn an engineering decision. Course pages, textbooks, standards, data sheets, papers, application notes, and forum answers serve different roles; source count cannot replace source quality.

## Purpose and learning outcomes

- Turn a broad topic into searchable, decidable questions.
- Distinguish primary research, standards or data sheets, reviews, teaching material, and experience reports.
- Retain stable bibliographic data, version, page location, and access date.
- Compare methods, conditions, results, and limits in an evidence matrix.
- Check conflicts of interest, retractions, outdated standards, and irreproducible experiments.

## Minimal environment

- A search entry point with phrase, Boolean, and site filters.
- A reference-management method that exports an open bibliographic format.
- A plain-text search log and evidence matrix.
- Institutional library or lawful open-access paths; paid access is not required for the core task.

Do not bypass access controls or upload unlicensed full text to a public repository. Tools and indexes change, so record the actual database and search date.

## Learning sequence

1. **Define the question:** state object, input, output, conditions, comparison, and decision threshold.
2. **Build vocabulary:** list synonyms, abbreviations, historical terms, standard numbers, and exclusions.
3. **Tier sources:** use textbooks or reviews to learn vocabulary, then return to standards, data sheets, and primary papers.
4. **Trace backward and forward:** inspect references and later citations for corrections, replications, and counterexamples.
5. **Extract evidence:** record test conditions, sample, metric, error, limitations, and funding.
6. **Apply a stop rule:** stop when new sources no longer change the conclusion or the important gap is explicit.

## Verification task: compare two filter implementations

Choose a low-risk question such as the FIR versus IIR tradeoff at a given sample rate and resource limit:

1. Define a decision question covering performance, resources, stability, and delay.
2. Build search terms and exclusions in two languages where useful.
3. Collect at least one teaching benchmark, one primary or authoritative source, and one implementation source.
4. Normalize conditions in an evidence matrix; do not directly compare differently defined metrics.
5. Find at least one result that argues against the initial preference.
6. Write a one-page conclusion separating facts, inference, untested assumptions, and the next experiment.

Acceptance requires every important judgment to point to a specific section, table, figure, or dataset rather than only a landing-page link.

## Common failures and diagnosis

- **Results are too broad:** add device, topology, metric, condition, or standard number.
- **Only search snippets were read:** open the source and verify that context and limits were not omitted.
- **The citation chain is circular:** trace back to the original measurement or specification and identify repeated summaries.
- **Only confirming evidence appears:** search explicitly for counterexamples, negative results, and boundaries.
- **Incompatible metrics are compared:** normalize definitions, units, bandwidth, and test environment.
- **A link dies:** retain DOI, report number, version, author, title, and lawful archive information.

## Reproducible evidence

- Research question, inclusion/exclusion criteria, and stop rule.
- Databases, query strings, filters, and search dates.
- Deduplicated bibliography with stable identifiers.
- Screening log and reasons for exclusion.
- Evidence matrix with conditions, metrics, results, and limits.
- Retraction or correction, standard-version, and data-sheet-revision checks.
- A synthesis that separates facts, inference, and open questions.

## Cost, licensing, and accessibility

Prefer lawful open access, author archives, libraries, and accessible standards paths. Mark sources requiring payment or institutional login and seek an open alternative with the same learning objective. Citation does not grant redistribution rights.

Keep text notes that work with screen readers rather than placing conclusions only in scans. Record chapter, page, or timestamp for long material. For low bandwidth, share the bibliography and summary matrix before full documents.

## Safety boundaries

- Do not execute code, firmware, or scripts attached to an unknown source without isolated review.
- A forum post is not an authority for mains, high voltage, medical, or battery safety.
- Typical data-sheet values do not replace worst-case rating review.
- Follow applicable rules for export-controlled, private, or vulnerability-related material.
- Never fabricate access, replication, or peer-review status.

## Completion checklist

- [ ] Question, metrics, conditions, and decision threshold are explicit.
- [ ] Queries, databases, dates, and filters are retained.
- [ ] Sources cover teaching, authoritative or primary, and implementation tiers.
- [ ] At least one counterexample or negative result was sought deliberately.
- [ ] Important conclusions point to specific evidence.
- [ ] Standards, revisions, retractions, and licensing are checked.
- [ ] Facts, inference, assumptions, and gaps are separated.
- [ ] Bibliography and evidence matrix are exportable and reviewable.

Next, create a design review with [Technical Writing](technical-writing.md), or turn evidence into a testable hypothesis through [Project Practice](projects.md).
