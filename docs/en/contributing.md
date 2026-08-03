---
title: Contribution Guide
description: Maintain the EE learning navigator through traceable evidence, bilingual parity, and reproducible review.
---

<div class="ee-language" markdown>
[简体中文](../contributing.md)
</div>

# Contribution Guide

EEDIY welcomes course recommendations, link reviews, route improvements, translations, project reproductions, safety corrections, and accessibility work. Quality depends less on the size of a contribution than on making every fact traceable and every judgment explainable.

## Useful contributions

- Add a course with genuine publicly accessible learning value.
- Correct a link, access status, prerequisite, hardware need, price, or license.
- Verify problems, solutions, labs, code, and assessment evidence.
- Report actual completion time, blockers, and alternatives after taking a course.
- Improve a route dependency or stage exit criterion.
- Contribute a reproducible project, test data, or failure retrospective.
- Restore Chinese/English parity and accessibility.
- Report a safety-boundary or attribution problem.

Pure rankings, promotional copy, unsupported “best course” claims, unauthorized copies of restricted material, and link-only pages are not suitable course records.

## Evidence priority

Prefer:

1. the official course or institutional page, syllabus, and public repository;
2. original material published by the instructor or laboratory;
3. official software, component, and instrument documentation;
4. reproducible learner evidence as a supplement to official facts;
5. aggregators, forums, and playlists only as leads to primary sources.

External pages change. Every important resource field needs a **last verified date**. Do not infer current availability from a search snippet, cached title, or old screenshot.

## Minimum course fields

| Field | Requirement |
| --- | --- |
| Title, institution, code | Match the official page; explain when no code exists |
| Official entry | Prefer a stable course page over a reposted playlist |
| Track and role | One primary track; mainline, alternative, or supplement |
| Learning outcomes | Three to six observable capabilities, not copied marketing |
| Prerequisites | Separate hard, recommended, and co-learning prerequisites |
| Resource matrix | Verify video, notes, problems, solutions, labs, code, and exams separately |
| Completion path | Order, critical work, and a substitute feedback mechanism |
| Time and cost | Cite traceable provider workload evidence, or label a maintainer estimate, state its basis, and require two-week calibration; also disclose paywall, region, software, and hardware |
| Risk and aging | Old tools, missing materials, unsafe labs, irreproducible steps |
| Verification and evidence | YYYY-MM-DD plus primary links supporting the facts |

Evidence tier must match the record:

- **S:** a public teaching–practice–feedback–assessment/project loop that can support independent study;
- **A:** strong teaching with a small number of explicit, compensable gaps;
- **B:** valuable components without a complete mainline spine;
- when evidence is insufficient, mark the item for review instead of assigning a high tier.

## Contribution workflow

1. **Search first:** confirm that the course, issue, or correction is not duplicated.
2. **Limit scope:** one change solves one clear problem; discuss a large route redesign first.
3. **Collect evidence:** open each resource and check login, payment, region, and specialist hardware.
4. **Update canonical data:** never hand-edit generated course or route pages.
5. **Maintain both languages:** facts, numbers, risks, and links match; phrasing may be natural.
6. **Validate locally:** run generation, the strict build, and quality checks; read the rendered page.
7. **Explain the judgment:** list the change, evidence, uncertainty, and verification beyond screenshots.
8. **Respond to review:** resolve disagreement with new evidence; preserve “review needed” when unknown.

## Bilingual parity

Translation is not word substitution. These must remain semantically identical:

- course identity, links, and verification dates;
- prerequisites and completion standards;
- open/closed status and missing resources;
- tier, role, and rationale;
- safety, cost, regional, and license constraints.

You may localize:

- sentence structure, terminology explanations, and reader-facing examples;
- common Chinese names while preserving the official title on first use;
- time-unit presentation and reading order.

When a fact changes in one language, update the other in the same contribution. If a reliable translation is unavailable, mark it and request language review instead of leaving a silent stale fact.

## Writing and attribution

- Lead with the conclusion, then evidence and limits.
- Separate official claims, contributor verification, and evidence-based judgment.
- Name the missing item; “resources incomplete” is too vague.
- Workload may use only one of two provenances: provider data with traceable evidence, or an explicitly labelled maintainer estimate.
- A maintainer estimate must state its basis and assumptions and require learners to calibrate for two weeks before long-term planning; “unknown” is not a substitute for this record.
- Summarize in your own words and link the source; do not copy course descriptions or books at length.
- Do not upload paid solutions, restricted slides, secrets, personal data, or unlicensed images.
- Give images meaningful alternatives; distinguish plots with more than color; use proper table headers.

## Additional gate for safety content

Safety changes receive priority review. For specific electrical, laser, RF, battery, chemical, mechanical, or first-aid statements:

- prefer regulators, standards bodies, manufacturers, or formal laboratory procedures;
- do not present one jurisdiction’s threshold as a universal safe line;
- do not enable unqualified readers to bypass interlocks, protection, or supervision;
- raise the risk class and recommend simulation or a qualified facility when uncertain;
- state that educational guidance is not work authorization.

## Change-description template

```markdown
## Change
- Added/corrected:
- Chinese and English pages affected:

## Evidence
- Official entry:
- Practice/lab/assessment:
- Access, cost, and license:
- Verified date:

## Judgment and uncertainty
- Role/tier rationale:
- Workload provenance (provider evidence, or maintainer estimate + basis + two-week calibration):
- Known gaps:
- Needs further review:

## Validation
- [ ] Data generation succeeded
- [ ] Strict site build passed
- [ ] Chinese and English facts match
- [ ] Internal links and critical external links checked
- [ ] Safety and content license reviewed
```

## Reviewer checklist

- [ ] The record solves a navigation problem rather than inflating the count.
- [ ] Every material fact traces to a primary source.
- [ ] Mainline/alternative/supplement role fits the route.
- [ ] Tier reflects the self-study loop, not institutional reputation.
- [ ] Missing resources, old tools, cost, and hardware are disclosed.
- [ ] Workload has traceable provider evidence, or is a labelled maintainer estimate with its basis and a two-week calibration requirement.
- [ ] Numbers, risks, links, and dates agree across languages.
- [ ] Projects and labs stay inside the supervision boundary.
- [ ] Third-party material is linked or used within its license.
- [ ] Automated checks pass and human reading finds no navigation dead end.

## Conflicts and corrections

Disclose if you teach the course, work for the platform, created the material, sell relevant equipment, or have another economic interest. A relationship does not automatically disqualify a resource, but readers must be able to judge it.

Factual errors, safety risks, and license concerns may receive a minimal correction before a complete rewrite. Provide the exact page, current statement, evidence, proposed remedy, and urgency. Maintainers should record the disagreement and resolution rationale.

See [Licensing and Attribution](about/license.md) for reuse and third-party boundaries.
