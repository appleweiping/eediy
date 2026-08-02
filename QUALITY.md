# EEDIY quality contract

This document defines release gates for the public learning navigator. It is a
contract, not a marketing checklist: a release is blocked when a required gate
fails, even if the site can still be built locally.

本文件定义公开学习导航的发布门禁。它是一份可执行的质量契约，而不是宣传清单：
任何必需门禁失败时，即使网站能够本地构建，也不能发布。

Course-guide depth, evidence levels, hard failures, and adversarial review are
defined in [EDITORIAL_QUALITY.md](EDITORIAL_QUALITY.md). A large generated
catalogue does not satisfy the researched-guide gate.

课程导读的深度、证据等级、硬失败与对抗审查以
[EDITORIAL_QUALITY.md](EDITORIAL_QUALITY.md) 为准。批量生成的资料目录不能计入
深度课程导读。

## 1. Catalogue coverage / 课程覆盖

- Every published course earns its place in a populated EE track and has a
  stable identifier, institution, primary official page, role, evidence tier,
  prerequisites, selection rationale, review caveats, resource-coverage
  vector, access state, and verification date.
  Provider-published prerequisites, corequisites, permissions, and explicit
  no-prerequisite statements are stored separately from EEDIY route advice;
  absence of verified provider evidence is never rewritten as “no hard
  prerequisite.”
- When a provider publishes study load, software or hardware requirements,
  costs, or safety constraints, the course record cites that evidence. EEDIY
  does not manufacture a generic workload, tool list, safety label, or learning
  exit merely to make every record look equally complete.
- Chinese and English catalogue records have one-to-one structural parity.
- Every populated track has a stated position in the prerequisite graph. Cycles,
  missing tracks, duplicate identifiers, and orphaned pages are release errors.
- Every populated track has a bilingual authored comparison guide that names
  concrete course choices, prerequisite gaps, access boundaries, and exit
  evidence; generated “master the core concepts” copy cannot satisfy this gate.
  Each language has at least three substantive H2 sections, at least two
  distinct links that resolve to real courses or prerequisite-track indexes,
  and a meaningful per-section translation counterpart. The validator rejects
  shallow sections, mismatched link targets, implausible bilingual length
  ratios, reused or lightly rewritten long paragraphs, and known catalogue
  boilerplate.
- Every `mainline` candidate has an independent audit record. Each populated
  track has exactly one explicit preferred entry, while unresolved identity,
  resource, access, tooling, licence, age, or safety evidence remains labelled
  `review` rather than being silently promoted.
- Release reports authored, deep (`researched` or `learner-reviewed`), and
  `catalogue` counts separately. Only deep guides may satisfy populated-track
  and independently audited mainline coverage; a catalogue-only record cannot
  be used as deep coverage.
- Learner-facing guide prose keeps evidence levels and maintenance workflow out
  of the narrative. It may not contain `R0`, desk-review, maintainer,
  correction-protocol, ledger, or dossier language; it may not end with a
  submission protocol, mention EEDIY more than twice, or sprawl beyond five
  H2 sections. A per-page density gate also caps generic archive, record,
  review, claim, artifact, unknown, final-report, and sign-off vocabulary at
  six Chinese matches or nine English matches. A guide may use two to five
  natural sections; short courses stay short, while unusually long pages must
  earn their length with course-specific work, access problems, or tooling.
- Corpus-level headings and endings must also read as independently edited
  pages. No more than 10% of guides may open with an H2 beginning `结论`, no
  more than 25% may contain an H2 beginning `用`, and no more than 20% may end
  in generic report/record/deliverable language. These limits are upper bounds,
  not quotas; a visibly templated individual page still fails.
- A course with no public assignment, laboratory, project, or exam cannot be
  promoted by inventing one. It may pass only as an explicit catalogue-only
  map that cites the official scope, states the missing public coursework and
  feedback, and labels every reconstructed exercise or project as independent
  rather than provider coursework. The release gate cross-checks deep status
  against structured `resource_coverage` and resource metadata. A coverage
  score of `1` means partial, version-mismatched, or access-restricted material;
  a provider landing page or syllabus may document that limited inventory. A
  score of `2` claims a usable material set, so every field scored `2` must
  have a matching, publicly reachable, `available` structured resource whose
  `artifact_scope` is substantive `content` (or is unset on a legacy record
  whose resource kind is itself substantive). An index, outline, landing page,
  syllabus, degraded or archived record, paid or institutional resource, or
  suggested project cannot substantiate a score of `2`.
- Course-guide bodies contain 320–1,400 Chinese CJK characters and 180–900
  English words. Corpus rhythm is also a release gate: Chinese median 400–850,
  p90 at most 1,200, length coefficient of variation at least 0.20, and no
  single H2 count on more than 70% of pages. These bounds reject both stubs and
  a new uniformly padded template.
- The opening paragraph makes a course decision immediately. Imagined-grader
  phrases such as “I will check,” repeated `先—再—最后` workflows, defensive
  negations, and command-heavy prose are release errors. Across the corpus,
  no more than 25% of Chinese guides may use workflow `先`, defensive
  `不是/不等于/而不是`, or command-heavy `必须/不要/应当` phrasing. Uniform
  entry-diagnostic language is capped at 12%, completion-package language at
  10%, audit-protocol language at 15%, site self-reference at 10%, and an
  imagined independent reviewer at 5%. English entry/exit-gate,
  completion-package, imagined-reviewer, and EEDIY-supplement phrasing is
  capped at 15%. These are corpus tripwires, not targets: a page still fails
  when the wording is visibly procedural even if the aggregate remains below
  the cap.

## 2. Resource evidence / 资源证据

- Links are taken from official course, institution, instructor, or explicitly
  identified official repository pages. Guessed URLs are prohibited.
- Resource records distinguish course home, syllabus, notes, video,
  assignments, laboratories, projects, exams, code, datasets, and textbooks.
- Every resource records access conditions, licence or rights uncertainty,
  availability state, and the last verification date.
- Resource counts are reported after normalization and de-duplication, but a
  link quota cannot substitute for relevance, provenance, or usable teaching
  material.
- Automated checks must reject insecure URLs, tracking links, malformed URLs,
  duplicate normalized URLs within a course, and missing metadata.
- External availability checks are evidence, not proof of teaching quality.
  Redirects, authentication walls, region limits, and intermittent failures are
  reported separately instead of being hidden.
- A release-time automated `review` result must be adjudicated against a
  primary official index, rendered primary page, or repository API. The exact
  targets, evidence, method, and retain/replace/remove decision are recorded in
  `data/external_link_reviews.json`; an unrecorded review result cannot be
  silently counted as healthy.
- The manual-review ledger names its reviewer, uses a strict non-future ISO
  review date no more than 14 days old by default, and records a concrete
  automation reason, method, and at least one unique canonical HTTPS evidence
  URL for every group. Its optional summary must equal the target-level decision
  counts exactly.
- Evidence URLs are checked in the same release run as content targets. A
  missing evidence URL (`404`/`410`) blocks release. A current manually verified
  evidence-only URL blocked by `robots.txt` or HTTP `403` may remain a warning
  under `--allow-review`, but it is reported separately and never counts as a
  retained content target.
- Every release-time network result must come from that exact run:
  `from_cache` must be `false`, `checked_at` must be a timezone-aware timestamp
  inside the permitted freshness window, and it cannot be later than the
  report's `generated_at`. A cached or undated result blocks release even when
  its last HTTP status was healthy.

## 3. Routes and practice / 路线与实践

- The route set must be non-empty and must cover foundations, specialization
  choices, and verifiable outcomes without duplicating routes to inflate a
  count.
- Every route reference resolves to a real course record. Coverage is reported
  for maintenance, not enforced as a catalogue-percentage quota.
- Every route states bilingual audience and expected outcome at route level.
  Every stage defines an ordered `course_ids` pool and an ordered
  `required_course_ids` subset; the required subset may be empty only when the
  stage supplies at least two complete `path_options`. It records an integer
  `elective_count`, uses `elective_course_ids` when only part of the remaining
  pool is counted, and provides specific bilingual `exit_zh` / `exit_en`
  criteria verifiable from learner artifacts. Courses outside the counted
  elective pool are optional. Path options are distinct complete alternatives
  and require `elective_count: 0`.
- Projects are included only when they come from a cited course or are authored
  as a genuinely course-specific independent exercise. A generic project
  template applied across the catalogue is not acceptable evidence of practice.
- High-energy electrical work, mains, large energy storage, RF power, lasers,
  rotating machinery, vacuum, high temperature, fabrication chemicals, and
  human-subject work are never presented as unsupervised home activities.

## 4. Learning support / 学习支持

- Learning support covers the setup, route-selection, safety, software,
  measurement, documentation, and communication needs that the maintained
  routes actually require. New guides are added for a demonstrated learner
  need, not to reach a page-count target.
- Guidance distinguishes conceptual learning, exercises, simulation, hardware
  implementation, and assessment evidence.
- Cost, bandwidth, accessibility, language, platform, and regional constraints
  are visible wherever they materially change a learner’s choice.

## 5. Build and data integrity / 构建与数据完整性

The following commands must succeed from a clean environment:

```text
python scripts/enrich_official_resources.py --validate-only
python scripts/compile_courses.py
python scripts/apply_course_editorial.py
python scripts/validate_courses.py
python scripts/validate_mainline_audit.py
python scripts/validate_routes.py
python scripts/check_course_guides.py --require-track-coverage --require-mainline-coverage
python scripts/check_editorial_quality.py
python scripts/generate_course_pages.py
python scripts/run_executable_examples.py --require-tools all
python scripts/run_quality.py --external
```

Four executable starter families are additional blocking gates rather than
download-only examples:

- the RC low-pass starter must agree across an analytic reference and a real
  ngspice batch run;
- the C ring buffer and sensor sampler must pass warning-as-error,
  AddressSanitizer/UndefinedBehaviorSanitizer, boundary, timeout, and deliberate
  fault checks;
- the synchronous FIFO must pass Icarus and Verilator simulation, SymbiYosys/Z3
  proofs and counterexample detection, and Yosys synthesis;
- the TMP117 KiCad project must pass source pin/net audit, headless ERC, DRC
  with schematic parity, and a fresh Gerber/drill/placement/BOM export under
  the pinned KiCad 8.0.9 release.

这四类 starter 不是“可下载即合格”的示例，而是额外的阻断式执行门禁：RC
必须同时通过解析参考与真实 ngspice 批处理；两项 C 工程必须通过
warning-as-error、ASan/UBSan、边界、超时和故障注入；同步 FIFO 必须通过两套
仿真器、形式证明/反例检测与综合；TMP117 KiCad 工程必须在固定的 KiCad
8.0.9 环境中重新完成引脚/网络审计、无界面 ERC、带原理图一致性检查的 DRC，
并导出新的 Gerber、钻孔、坐标与 BOM。任何一项缺工具、跳过或只留下预制
PASS 日志，都不能发布。

The final `run_quality.py --external` command is the release gate. It checks
dependency consistency, reruns upstream generation in drift-check mode,
executes semantic validators and unit tests, performs a current network check
of every external target and its review evidence, writes a warning-free
blocking quality report, and performs the strict MkDocs build. Running
`run_quality.py` without `--external` is an explicitly offline development
check; it cannot qualify a release. Both modes write disposable, ignored
artifacts to `build/` and `site/` but do not rewrite authoritative source data.

最后的 `run_quality.py --external` 是发布门禁：它检查依赖一致性，以漂移检查模式
重跑上游生成步骤，执行语义验证与单元测试，对全部外部目标及其复核证据做当次网络检查，
生成零警告的阻断式质量报告，
并完成 MkDocs 严格构建。不带 `--external` 的 `run_quality.py` 只是明确跳过网络检查
的离线开发门禁，不能用于发布。两种模式都会向被忽略的 `build/` 与 `site/` 写入
可丢弃产物，但不会改写权威源数据。

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
- Feedback actions must remain directly visible without client-side rendering.
  Their GitHub Issue prefill must preserve the stable page ID, canonical URL,
  reported URL, and language, and request verifiable evidence for corrections.

## 7. Review and publication / 复核与发布

- Editorial claims are traceable to primary evidence or clearly marked as
  maintainer judgement.
- Every course page declares `catalogue`, `researched`, or `learner-reviewed`.
  The authored-record gate counts all three states, while only the latter two
  count as deep guides for track and mainline coverage. Learner-reviewed status
  requires traceable R2–R4 evidence.
- The primary sidebar lists only `researched` or `learner-reviewed` course
  articles. `catalogue` records remain reachable through track indexes and
  search, but cannot borrow the visual prominence of an editorial guide.
- Researched guides pass the editorial hard-failure checks, the per-page
  content rubric, narrative-link limits, bilingual fact-parity checks, and the
  cross-page swap test. The calibrated guide corpus has no unresolved
  editorial warnings at release time.
- A release report records exact counts, check outputs, known limitations, and
  the date of the external-link sample.
- The public repository must have a clean default branch, a green continuous
  integration run, an explicit code licence, an explicit content licence,
  contribution instructions, and a working deployed site.
- Publication is complete only after the remote repository, workflow run, and
  public site are independently opened and verified.
