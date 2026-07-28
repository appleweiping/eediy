# Contributing to EEDIY / 参与 EEDIY

Thank you for helping make electrical-engineering self-study more executable.
Contributions are welcome for courses, routes, projects, accessibility,
translations, tooling, and corrections.

感谢你帮助电子工程学习者获得更可执行的自学路线。课程、路线、项目、无障碍、
翻译、工具链与事实纠错方面的贡献都很重要。

## Before changing content / 修改内容之前

Read the full [editorial contribution guide](docs/contributing.md). In
particular:

- prefer official course or institution pages as factual evidence;
- separate verified facts from maintainer judgement;
- describe access, licence uncertainty, hardware, cost, and safety constraints;
- update Chinese and English fields together;
- never commit credentials, restricted course files, personal data, or copied
  paid material.

请先阅读完整的[编辑贡献指南](docs/contributing.md)。事实应优先引用课程或机构官方
页面；核验事实与编辑判断必须分开；访问、许可、硬件、成本与安全约束不能隐藏；
中英文内容要同步更新；不得提交凭证、受限课程文件、个人数据或复制的付费材料。

## Development setup / 开发环境

```bash
python -m venv .venv
python -m pip install --require-hashes -r requirements.lock
python -m mkdocs serve
```

`requirements.txt` 与 `requirements-dev.txt` 是直接依赖输入；CI 与发布使用带哈希的
`requirements.lock`。修改依赖后，用 Python 3.12 目标重新生成锁文件：

```bash
uv pip compile requirements.txt requirements-dev.txt --python-version 3.12 --generate-hashes --output-file requirements.lock
```

## Authoritative data flow / 权威数据流

```text
course_candidates + tracks + course_resources
课程候选 + 方向图 + 官方资源抓取证据
  → compile_courses.py
  → compiled courses.json + project_templates
  → apply_project_templates.py
  → project-enriched courses.json + course_editorial
  → apply_course_editorial.py
  → canonical courses.json + routes + mainline_audit review annotations
  → generate_course_pages.py
  → generated bilingual Markdown / 生成的双语 Markdown

mainline_audit → validate_mainline_audit.py ─┐
other validators and tests / 其他验证器与测试 ┴→ release gate / 发布门禁
```

The compiler joins `data/course_candidates.json`, `data/tracks.json`, and
`data/course_resources.json`. Project and editorial records are subsequent
overlays on `data/courses.json`; canonical courses and `data/routes.json` feed
the page generator. `data/mainline_audit.json` does not alter canonical course
data: it supplies visible review annotations to generated pages and remains an
independent release gate. Edit the layer that owns the claim. Do not hand-edit
`data/courses.json` or generated pages under `docs/courses/`,
`docs/en/courses/`, `docs/routes/`, or `docs/en/routes/`.

编译器合并 `data/course_candidates.json`、`data/tracks.json` 与
`data/course_resources.json`；项目和编辑记录随后叠加到 `data/courses.json`。
权威课程目录与 `data/routes.json` 共同驱动页面生成。
`data/mainline_audit.json` 不改写权威课程数据，只向生成页面提供可见复核标注，
同时仍是独立发布门禁。请修改对事实负责的权威层；不得手改 `data/courses.json`，
也不得手改 `docs/courses/`、
`docs/en/courses/`、`docs/routes/` 或 `docs/en/routes/` 下的生成页面。

After changing authoritative data, run the complete maintenance pipeline in
exactly this order:

修改权威数据后，请严格按以下顺序运行完整维护管线：

```bash
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

`run_quality.py` is the final release gate. It checks upstream source drift and
dependency consistency, runs unit tests and the quality report, and performs a
strict site build. It writes disposable, ignored artifacts under `build/` and
`site/`; it does not rewrite authoritative source data. Do not delete generated
data to bypass drift checks.

`run_quality.py` 是最终发布门禁：它检查上游源码漂移与依赖一致性，运行单元测试、
生成质量报告并严格构建站点。它会在被忽略的 `build/` 与 `site/` 中写入可丢弃
产物，但不会改写权威源数据。不得通过删除生成数据来绕过漂移检查。

## Required verification / 必需验证

When changing URLs or resource metadata, also run:

```bash
python scripts/run_quality.py --external
```

The quality contract in [QUALITY.md](QUALITY.md) defines release thresholds.
A smaller change does not have to solve every open editorial gap, but it must
not weaken an existing gate or make the reported coverage less truthful.

[QUALITY.md](QUALITY.md) 定义发布阈值。单个贡献不必解决所有编辑缺口，但不能削弱
已有门禁，也不能让覆盖报告变得不真实。

## Course and route semantics / 课程与路线语义

A course contribution must record prerequisites, outcomes, role and tier,
resource coverage, access and licence conditions, verification date, completion
evidence, tooling, hardware, cost, and safety. Record provider workload only
with a traceable provider source. Otherwise label it as a maintainer estimate,
explain the basis, and tell learners to calibrate it for two weeks before
committing to a long-term schedule.

课程贡献必须记录先修、产出、角色与分层、资源覆盖、访问和许可条件、核验日期、
完成证据、工具、硬件、成本与安全信息。只有在提供方来源可追溯时，才记录为提供方
工作量；否则须明确标注为维护者估算、解释依据，并提示学习者先进行两周校准，再
承诺长期进度。

Every route defines bilingual audience and outcome fields. Each stage defines
an ordered `course_ids` pool, ordered `required_course_ids`, and any complete
`path_options`; at least one required course or a path-option group must be
present. It also records `elective_count`, an explicit counted
`elective_course_ids` pool when needed, and specific bilingual `exit_zh` /
`exit_en` criteria verifiable from learner artifacts. Courses outside the
counted elective pool remain optional. Path options are complete alternatives
and require `elective_count: 0`.

每条路线定义双语受众与目标。每个阶段定义有序 `course_ids` 课程池，并提供有序
`required_course_ids` 与可能存在的完整 `path_options` 路径选项；阶段必须至少包含
一门必修课或一组路径选项。同时记录 `elective_count`、需要时显式列出的计数选修池
`elective_course_ids`，以及能通过学习产物核验的双语 `exit_zh` / `exit_en` 条件。
计数选修池之外的课程保持可选；路径选项是完整替代，并要求 `elective_count: 0`。

## Change description / 变更说明

Explain:

1. what learner problem the change solves;
2. which primary evidence was checked and on what date;
3. what judgement or uncertainty remains;
4. which commands were run;
5. whether content, routes, generated pages, screenshots, or external links
   changed.

请说明学习者问题、核验日期与一手证据、仍存在的判断或不确定性、实际执行的检查，
以及内容、路线、生成页面、截图或外链是否发生变化。
