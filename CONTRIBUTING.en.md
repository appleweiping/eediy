# Contributing to EEDIY

Thank you for helping learners find electrical-engineering resources that are executable, verifiable, and safe. We judge contributions by whether a course is accessible, completable, reproducible, and honestly bounded—not by link count.

[中文贡献指南](CONTRIBUTING.md)

## Before you start

Small prose, translation, and link fixes may go directly to a pull request. Open an issue before adding courses, changing routes, revising safety levels, or changing resource status. Include the evidence and affected scope so investigations are not duplicated.

Contributors must:

- submit only text, code, and media they are entitled to contribute;
- cite official course pages or other primary sources rather than search summaries;
- maintain both Chinese and English pages;
- avoid publishing course solutions, restricted notes, personal data, credentials, or material that cannot be redistributed;
- set conservative, executable boundaries for physical work.

## Data flow

The authoritative layers flow in this order:

```text
course_candidates + tracks + course_resources
  → compile_courses.py
  → compiled courses.json + course_editorial
  → apply_course_editorial.py
  → canonical courses.json + routes + mainline_audit review annotations
  → generate_course_pages.py
  → generated bilingual Markdown

mainline_audit → validate_mainline_audit.py ─┐
other validators and tests ──────────────────┴→ release gate
```

Edit the layer that owns the claim. Candidate data owns identity, track and
role, the resource-coverage matrix, risk, and optional provider-backed `level`
and `workload`. Resource data owns crawler evidence and verification metadata;
reachability is evidence, not a teaching-quality rating. Editorial records own
the bilingual summary and review note. The mainline audit owns
preferred-course decisions and unresolved review states; it does not alter
canonical course data, but supplies visible review annotations to generated
pages and remains an independent release gate. Tracks and routes own
prerequisite structure and stage semantics.

Do not hand-edit `data/courses.json` or generated pages under `docs/courses/`,
`docs/en/courses/`, `docs/routes/`, or `docs/en/routes/`. After changing
authoritative data, run the complete pipeline in exactly this order:

```bash
python scripts/enrich_official_resources.py --validate-only
python scripts/compile_courses.py
python scripts/apply_course_editorial.py
python scripts/validate_courses.py
python scripts/validate_mainline_audit.py
python scripts/validate_routes.py
python scripts/generate_course_pages.py
python scripts/run_quality.py
```

`run_quality.py` is the final release gate. It checks upstream source drift and
dependency consistency, runs unit tests and the quality report, and performs a
strict site build. It writes disposable, ignored artifacts under `build/` and
`site/` without rewriting authoritative source data. Do not delete generated
data to bypass drift checks.

## Adding or changing a course

Every course needs:

1. An official course page, institution, course code, and canonical track.
2. A role and tier with selection rationale and known gaps.
3. Public-availability scores for video, notes, practice, labs, exams, and code.
4. `last_verified`, `access`, `license`, and `status` for every resource.
5. Prerequisites, verifiable outcomes, and completion evidence.
6. A workload value backed by a traceable provider source; otherwise, an explicitly labelled maintainer estimate with its basis and a required two-week calibration before long-term planning.
7. Software, hardware, and cost notes. Unknown cost must not be described as free.
8. A safety level and bilingual note. Work involving mains, high voltage, stored energy, RF, lasers, chemicals, fabrication equipment, or human subjects requires a compliant facility and qualified supervision.

Every route defines a bilingual audience and expected outcome. Every route stage needs:

1. An ordered `course_ids` pool and ordered `required_course_ids` subset. The required subset may be empty only when the stage supplies at least two complete `path_options`.
2. An integer `elective_count`; use `elective_course_ids` when only part of the remaining pool counts. Courses outside that counted pool are optional.
3. Distinct complete path alternatives with `elective_count: 0`, when paths are used.
4. Specific bilingual `exit_zh` and `exit_en` criteria verifiable from learner artifacts.

Electives are choices, not hidden mandatory workload.

Resource status means:

- `available`: the material worked under its recorded access condition at the latest review;
- `degraded`: useful material remains, but an important component or function is missing;
- `archived`: a read-only snapshot whose timing or platform information may be dated;
- `unavailable`: the material has been confirmed inaccessible;
- `review-needed`: access policy, rate limits, or another condition prevented a reliable manual conclusion.

HTTP 403, robots restrictions, and login walls require manual review and are never counted as healthy responses.

## Translation

Every Chinese page needs a matching page under `docs/en/`, and every English page needs a Chinese counterpart. Both versions must carry the same facts, risks, exit criteria, and link status. Natural localization is preferred over word-for-word translation. Official course titles, standards, and tool names may remain in their original language.

When changing heading structure, code blocks, tables, or links, update the counterpart in the same pull request. Run:

```bash
python scripts/check_translations.py
python scripts/check_markdown_links.py
python scripts/check_navigation.py
```

## External-link review

The regular local gate validates internal links. To perform network checks, run:

```bash
python scripts/check_external_links.py
```

Results remain separated into healthy, manual review, and failed. If a network environment causes systematic policy denials, `--allow-review` keeps those items visible without making them healthy; genuine failures still fail the command. Never hide a problem by loosening status or removing evidence.

## Local quality gate

Python 3.12 is recommended:

```bash
python -m pip install --require-hashes -r requirements.lock
python scripts/run_quality.py
```

`requirements.txt` and `requirements-dev.txt` are the direct-dependency inputs;
CI and releases install the hash-locked `requirements.lock`. After changing a
dependency, regenerate it for Python 3.12:

```bash
uv pip compile requirements.txt requirements-dev.txt --python-version 3.12 --generate-hashes --output-file requirements.lock
```

The release gate requires:

- evidence-backed courses and an audited preferred mainline for every populated track; catalogue size is not a release criterion;
- complete resource metadata;
- valid route references and stages with required/elective semantics and bilingual verifiable exits;
- 100% Chinese/English page pairing;
- navigation reachability and valid internal links and anchors;
- no unfinished markers, restricted comparison names, or credential patterns;
- no generated-file drift;
- a warning-free strict MkDocs build.

## Pull request expectations

- Keep one clear concern per pull request; split bulk course work by track or route.
- List review dates, primary evidence, affected pages, and local check results.
- Do not mix formatting-only work with semantic changes to tiers, routes, or safety.
- Reviewers may request reproduction records, screenshots, response headers, or archived license evidence, but never personal accounts or restricted content.
- By merging, you agree that the repository license applies to your contribution and that third-party material retains its own license.
