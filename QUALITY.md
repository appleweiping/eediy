# EEDIY quality contract

This document defines release gates for the public learning navigator. It is a
contract, not a marketing checklist: a release is blocked when a required gate
fails, even if the site can still be built locally.

本文件定义公开学习导航的发布门禁。它是一份可执行的质量契约，而不是宣传清单：
任何必需门禁失败时，即使网站能够本地构建，也不能发布。

## 1. Catalogue coverage / 课程覆盖

- At least 125 reviewed courses across at least 24 populated EE tracks.
- Every course has a stable identifier, institution, primary official page,
  role, evidence tier, prerequisites, outcomes, selection rationale, review
  caveats, resource-coverage vector, access state, and verification date.
- Every course explicitly records study-load provenance, software and hardware
  needs, cost constraints, safety level, and completion evidence. A provider
  workload cites provider evidence; otherwise it is labelled as a maintainer
  estimate, states its basis, and requires a two-week learner calibration
  before long-term planning.
- Chinese and English catalogue records have one-to-one structural parity.
- Every populated track has a stated position in the prerequisite graph. Cycles,
  missing tracks, duplicate identifiers, and orphaned pages are release errors.
- Every `mainline` candidate has an independent audit record. Each of the 35
  tracks has exactly one explicit preferred entry, while unresolved identity,
  resource, access, tooling, licence, age, or safety evidence remains labelled
  `review` rather than being silently promoted.

## 2. Resource evidence / 资源证据

- Links are taken from official course, institution, instructor, or explicitly
  identified official repository pages. Guessed URLs are prohibited.
- Resource records distinguish course home, syllabus, notes, video,
  assignments, laboratories, projects, exams, code, datasets, and textbooks.
- Every resource records access conditions, licence or rights uncertainty,
  availability state, and the last verification date.
- A release must contain at least 550 unique, high-value course-resource links
  after normalization and de-duplication.
- Automated checks must reject insecure URLs, tracking links, malformed URLs,
  duplicate normalized URLs within a course, and missing metadata.
- External availability checks are evidence, not proof of teaching quality.
  Redirects, authentication walls, region limits, and intermittent failures are
  reported separately instead of being hidden.

## 3. Routes and practice / 路线与实践

- At least 10 goal-oriented routes must cover foundations, a specialization,
  and a verifiable final outcome.
- Route references resolve to real course records and collectively point to at
  least 100 unique courses.
- Every route states bilingual audience and expected outcome at route level.
  Every stage defines an ordered `course_ids` pool and an ordered
  `required_course_ids` subset; the required subset may be empty only when the
  stage supplies at least two complete `path_options`. It records an integer
  `elective_count`, uses `elective_course_ids` when only part of the remaining
  pool is counted, and provides specific bilingual `exit_zh` / `exit_en`
  criteria verifiable from learner artifacts. Courses outside the counted
  elective pool are optional. Path options are distinct complete alternatives
  and require `elective_count: 0`.
- At least 100 course records include an official or clearly labelled suggested
  project. Each project specifies deliverables, verification, reproducibility,
  and an appropriate safety boundary.
- High-energy electrical work, mains, large energy storage, RF power, lasers,
  rotating machinery, vacuum, high temperature, fabrication chemicals, and
  human-subject work are never presented as unsupervised home activities.

## 4. Learning support / 学习支持

- The site provides at least 16 substantive bilingual guides covering learning
  setup, route selection, reproducible projects, laboratory safety, software
  environments, version control, programming, numerical work, simulation,
  PCB/EDA, HDL/FPGA, embedded toolchains, instruments and measurement, data and
  laboratory notebooks, literature search, and technical communication.
- Guidance distinguishes conceptual learning, exercises, simulation, hardware
  implementation, and assessment evidence.
- Cost, bandwidth, accessibility, language, platform, and regional constraints
  are visible wherever they materially change a learner’s choice.

## 5. Build and data integrity / 构建与数据完整性

The following commands must succeed from a clean environment:

```text
python scripts/enrich_official_resources.py --validate-only
python scripts/compile_courses.py
python scripts/apply_project_templates.py
python scripts/apply_course_editorial.py
python scripts/validate_courses.py
python scripts/validate_mainline_audit.py
python scripts/validate_routes.py
python scripts/generate_course_pages.py
python scripts/run_quality.py
```

The final `run_quality.py` command is the release gate. It checks dependency
consistency, reruns upstream generation in drift-check mode, executes semantic
validators and unit tests, writes the quality report, and performs the
warning-free strict MkDocs build. It writes disposable, ignored artifacts to
`build/` and `site/` but does not rewrite authoritative source data.

最后的 `run_quality.py` 是发布门禁：它检查依赖一致性，以漂移检查模式重跑上游生成
步骤，执行语义验证与单元测试，生成质量报告，并完成无警告的 MkDocs 严格构建。
它会向被忽略的 `build/` 与 `site/` 写入可丢弃产物，但不会改写权威源数据。

Additional release checks must cover:

- JSON Schema validation and semantic validation;
- generated-page drift and bilingual page parity;
- fresh external-link evidence before the blocking consolidated report on
  default-branch releases;
- internal links, fragments, navigation targets, and orphaned Markdown files;
- forbidden private or unrelated provenance terms;
- deterministic generation with a clean working tree after regeneration;
- secret scanning, dependency review, and least-privilege workflow permissions.

The remote release path runs the blocking quality workflow first. GitHub Pages
is built from the exact tested commit only after that workflow succeeds; a
failed or cancelled quality run cannot publish.

远端发布路径会先运行阻断式质量工作流。只有质量工作流通过后，GitHub Pages 才会
从同一个已测试提交构建；失败或被取消的质量运行不能发布。

## 6. Interface and accessibility / 界面与无障碍

- Desktop and mobile layouts are visually reviewed at fixed viewports.
- Navigation drawer, search, language switching, theme switching, route links,
  course links, checklist persistence, and keyboard focus states are exercised.
- Pages preserve semantic heading order, descriptive link text, table keyboard
  access, visible focus, sufficient colour contrast, zoom resilience, reduced
  motion, and non-colour status cues.
- The production build does not require analytics, remote fonts, or client-side
  rendering for core reading and navigation.
- Browser console errors, broken assets, horizontal page overflow, and obscured
  focus are release blockers.

## 7. Review and publication / 复核与发布

- Editorial claims are traceable to primary evidence or clearly marked as
  maintainer judgement.
- A release report records exact counts, check outputs, known limitations, and
  the date of the external-link sample.
- The public repository must have a clean default branch, a green continuous
  integration run, an explicit code licence, an explicit content licence,
  contribution instructions, and a working deployed site.
- Publication is complete only after the remote repository, workflow run, and
  public site are independently opened and verified.
