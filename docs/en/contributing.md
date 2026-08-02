---
title: Contribution Guide
description: Maintain the EE learning navigator through traceable evidence, bilingual parity, and reproducible review.
---


# Contribute

Finding one error does not require learning the entire data pipeline, and adding a course should not begin by editing a generated page. Choose the path that matches the size of the change.

## Path one: make a quick correction

Use this path for a dead link, wrong prerequisite, translation mismatch, edition change, or safety concern:

- [Report a broken or restricted link](https://github.com/appleweiping/eediy/issues/new?template=broken-link.yml)
- [Submit a factual or safety correction](https://github.com/appleweiping/eediy/issues/new?template=content-error.yml)
- [Add learning experience or a course update](https://github.com/appleweiping/eediy/issues/new?template=course-feedback.yml)
- [Discuss the scope first](https://github.com/appleweiping/eediy/discussions)

The exact page, sentence to change, primary source, and verification date are enough to begin. A factual or safety correction can land before a complete page rewrite.

## Path two: add a course, project, or substantial revision

- [Propose a course](https://github.com/appleweiping/eediy/issues/new?template=course.yml)
- [Propose a project or laboratory exercise](https://github.com/appleweiping/eediy/issues/new?template=project.yml)
- [View or open a pull request](https://github.com/appleweiping/eediy/compare)
- [Read the repository contribution guide](https://github.com/appleweiping/eediy/blob/main/CONTRIBUTING.md)

Use an issue first to check for duplication and agree on track and scope. Open a pull request once the bilingual content and traceable evidence are ready.

## Edit the source that owns the claim

Course and route pages are generated. Do not edit `docs/courses/`, `docs/en/courses/`, `docs/routes/`, or `docs/en/routes/` directly.

| Change | Authoritative source |
| --- | --- |
| Course identity, institution, code, track, and prerequisites | [`data/course_candidates.json`](https://github.com/appleweiping/eediy/blob/main/data/course_candidates.json) |
| Official resources, access status, and verification record | [`data/course_resources.json`](https://github.com/appleweiping/eediy/blob/main/data/course_resources.json) |
| Course role and editorial judgment | [`data/course_editorial.json`](https://github.com/appleweiping/eediy/blob/main/data/course_editorial.json) |
| Guide state, source list, and bilingual fragment paths | [`data/course_guides.json`](https://github.com/appleweiping/eediy/blob/main/data/course_guides.json) |
| Course-guide prose | [`content/course-guides/`](https://github.com/appleweiping/eediy/tree/main/content/course-guides) |
| Track comparison prose | [`content/track-guides/`](https://github.com/appleweiping/eediy/tree/main/content/track-guides) |
| Route stages and dependencies | [`data/routes.json`](https://github.com/appleweiping/eediy/blob/main/data/routes.json) |

If ownership is unclear, follow the [complete data flow and generation order](https://github.com/appleweiping/eediy/blob/main/CONTRIBUTING.md#authoritative-data-flow--权威数据流).

## What makes a contribution reviewable

- Trace material facts to a primary course, institution, instructor, manufacturer, or standards page and record the verification date.
- Check notes, assignments, solutions, laboratories, code, and examinations separately; “resources complete” is not evidence.
- Disclose login, payment, region, license, specified hardware, and laboratory requirements.
- Keep facts, numbers, links, risks, and recommendations aligned across Chinese and English while allowing natural phrasing in each language.
- Describe something as learner experience only when completion scope, environment, actual effort, obstacles, and inspectable output are supplied.
- For electrical, laser, RF, battery, chemical, or mechanical hazards, use formal safety sources and never provide a way around interlocks, protection, or supervision.

## Admission policy: close one module instead of chasing catalogue counts

A track should first form one learnable loop: **one main course, one evidence-backed Chinese-language alternative where one genuinely exists, one problem or laboratory set, one official reference entry, and one task that verifies the learning result**. Record a missing part as a gap. Do not add duplicate or weakly evidenced material to satisfy a course, page, link, or project count.

Evaluate new sources in this order:

1. Complete open courses published by a university or instructor;
2. Official documentation from governments, standards bodies, and open-source projects;
3. Formal training and application material from semiconductor, EDA, and instrument vendors;
4. Learning sites with a named author and checkable exercises or automated feedback;
5. Community articles only for one specific gap, never as the source of a mainline fact.

Every proposed entry must say what it replaces or supplements, how much official material is actually open, which prerequisites and equipment it needs, and what evidence a learner will produce. Downgrade, archive, or remove an entry when its official source disappears, a more complete resource supersedes it, or only unverifiable promotional claims remain. Historical catalogue size is not a reason to keep it.

Do not upload paid solutions, restricted course files, PDKs, vendor-confidential material, credentials, personal data, or unlicensed images. Disclose a relevant financial or professional relationship in the change description. See [Licensing and Attribution](about/license.md) for third-party boundaries.

## Preview and check locally

```bash
python -m pip install --require-hashes -r requirements.lock
python -m mkdocs serve
python scripts/run_quality.py
```

Changes to authoritative course data also require the ordered generation pipeline in the [repository contribution guide](https://github.com/appleweiping/eediy/blob/main/CONTRIBUTING.md). Read both rendered languages before submission, and list the change, sources, remaining uncertainty, and checks run in the pull request.
