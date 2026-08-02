# EEDIY · EE 自学指南

EEDIY is a bilingual, evidence-oriented learning navigator for Electrical Engineering. It connects prerequisites, open course resources, reproducible projects, and laboratory safety into routes that a self-learner can actually execute.

EEDIY 是一个面向电子工程学习者的双语、证据导向型学习导航。它把先修关系、公开课程资源、可复现项目与实验安全组织成能够真正执行的学习路线。

## What this repository provides / 本仓库提供什么

- Chinese and English learning entrances with matching core guidance / 中英文同构的核心指南
- A staged global roadmap from foundations to specialization / 从基础到方向深化的分阶段全局路线
- Course records that distinguish mainline, alternatives, and supplements / 区分主线、替代与补充资源的课程档案
- Tool, safety, and project guides designed around reproducible evidence / 围绕可复现证据设计的工具、安全与项目指南
- Client-side bilingual search, responsive navigation, and light/dark themes / 双语本地搜索、响应式导航与浅深色主题

The catalog is a map, not a degree, credential, laboratory authorization, or guarantee of third-party availability. Always follow the rules of your institution, laboratory, equipment manufacturer, and jurisdiction.

课程目录是一张地图，不代表学位、资质、实验授权，也不保证第三方资源永久可用。请始终遵守所在机构、实验室、设备制造商与当地法规的要求。

## Information architecture / 信息架构

```text
docs/
├── index.md                     # 中文首页
├── getting-started.md           # 中文起步指南
├── roadmap.md                   # 中文全局路线
├── courses/                     # 生成的中文课程与方向页
├── guides/                      # 中文工具、安全、项目指南
├── en/                          # 英文镜像
└── assets/                      # 站点品牌资源、样式与渐进增强脚本
```

Course, track, and route pages are generated from reviewed structured records.
Do not hand-edit `data/courses.json` or the generated catalog pages; update the
appropriate authoritative layer and run the complete pipeline so both
languages remain aligned.

课程、方向与路线页由经过复核的结构化记录生成。请勿直接修改
`data/courses.json` 或生成的目录页面；应更新对应的权威数据层并运行完整管线，
以保持中英文一致。

## Authoritative data flow / 权威数据流

```text
data/course_candidates.json + data/tracks.json + data/course_resources.json
  候选课程 + 方向图 + 官方资源抓取证据
        ↓  compile_courses.py
compiled data/courses.json + data/course_editorial.json
  编译课程目录 + 双语编辑叠加层
        ↓  apply_course_editorial.py
canonical data/courses.json     canonical catalogue / 权威课程目录
        ↓
canonical data/courses.json + data/routes.json + data/mainline_audit.json
  + data/course_guides.json + content/course-guides + content/track-guides
  权威课程目录 + 路线语义 + 审计标注 + 单课/方向编辑导读
        ↓  generate_course_pages.py
docs/courses + docs/routes + docs/en/...
  generated bilingual Markdown / 生成的双语 Markdown
        ↓  sync_navigation.py + data/course_guides.json
mkdocs.yml curated bilingual navigation / 只直列深度导读的双语导航

data/mainline_audit.json ── validate_mainline_audit.py ──┐
other validators and tests / 其他验证器与测试 ────────────┴─ release gate / 发布门禁
```

Each layer has one responsibility. The compiler joins course candidates, the
track graph, and official-resource evidence into `data/courses.json`. Project
evidence stays attached to its cited course or a course-specific independent
exercise; bilingual editorial records are then applied as the only catalogue
overlay. Routes, researched-course fragments, authored track guides, and the
canonical course records drive the bilingual page generator.
The mainline material-scope record never changes canonical course data: it
supplies visible limitation notes to generated pages while its validator
remains an independent release check. Link reachability is evidence, not a
quality rating.

每层只承担一种权威职责：编译器把候选课程、方向图和官方资源证据合并为
`data/courses.json`；项目只保留课程原有证据或有明确课程语境的独立练习，双语编辑
记录作为唯一叠加层写入这份权威目录。
路线数据、研究型单课导读、人工方向导读与权威课程目录共同驱动双语页面生成。
主线材料范围记录不改写权威课程数据，只向生成页面提供可见的限制说明，同时其
验证器仍作为独立发布检查。链接可达性只是证据，不等于教学质量。

Run the maintenance pipeline in this order after changing authoritative data:

修改权威数据后，请严格按以下顺序运行维护管线：

```bash
python scripts/enrich_official_resources.py --validate-only
python scripts/compile_courses.py
python scripts/apply_course_editorial.py
python scripts/validate_courses.py
python scripts/validate_mainline_audit.py
python scripts/validate_routes.py
python scripts/generate_course_pages.py
python scripts/sync_navigation.py --write
python scripts/run_quality.py
```

Before a release, repeat the final command as
`python scripts/run_quality.py --external`; only that mode checks every
external target and its review evidence in the current run.

发布前必须将最后一条命令改为 `python scripts/run_quality.py --external`；
只有该模式会在当次运行中检查全部外部目标及其复核证据。

## Local preview / 本地预览

Python 3.12 is recommended.

```bash
python -m venv .venv
python -m pip install --require-hashes -r requirements.lock
python -m mkdocs serve
```

The local address is printed by MkDocs after startup. Before proposing a
change, run the complete maintenance pipeline above. Its final
`run_quality.py` step performs the offline dependency, generated-data,
test, report, and strict-build checks. It explicitly omits the network
resource sweep; use `--external` for a release. MkDocs creates disposable output
in `site/`; source content remains under `docs/`.

MkDocs 启动后会打印本地访问地址。提交修改前，请运行上方完整维护管线；最后的
`run_quality.py` 会执行离线的依赖一致性、生成数据漂移、测试、
报告与严格构建检查，但明确跳过全站网络资源扫描；发布时必须使用 `--external`。
MkDocs 的可丢弃产物位于 `site/`，源内容始终位于 `docs/`。

## Community feedback / 社区反馈

Every course, track, route, and reader guide uses one stable ID across Chinese
and English. These pages expose direct GitHub Issue forms for factual
corrections and broken-link reports; course pages also accept learner reports.
Every link carries the stable page ID, canonical URL, reported URL, and language
so maintainers can reproduce the context without a third-party comment embed.

每份课程、方向、路线和读者指南都以同一个稳定 ID 连接中英文版本，并提供事实纠错、
失效链接的 GitHub Issue 表单；课程页还接受学习复盘。每个入口都会携带稳定页面 ID、
规范 URL、实际报告 URL 与语言，维护者无需依赖第三方评论嵌入即可复现上下文。

## Contribution standard / 贡献标准

A course recommendation must state prerequisites, learning outcomes, resource completeness, assessment evidence, tooling or hardware needs, access constraints, safety concerns, and the last verification date. “Good course” is not enough: another learner should be able to decide whether the course fits and know how to finish it.

课程推荐必须说明先修要求、学习产出、资源完整度、考核证据、工具或硬件需求、访问限制、安全风险与最近核验日期。“这是一门好课”并不足够：另一位学习者应能据此判断是否适合，并知道如何完成。

Use a provider-backed workload only when its traceable provider source is
recorded. Otherwise, label the value as an estimate, state its basis, and ask
the learner to time a representative unit before long-term planning. Route-level
audience and outcome fields are separate from stage selection: each stage
defines its course pool, ordered required courses and any complete path
options, the counted elective pool and count where applicable, and specific
bilingual, verifiable exit criteria. A stage must have required courses or path
options; a path-options stage has no counted electives.

只有在记录了可追溯的提供方来源时，才把工作量写作提供方数据；否则须明确标注
为估算、说明依据，并请学习者先记录一个代表性单元的真实投入再制定长期计划。路线层的
受众与目标和阶段选择规则相互独立：每个阶段定义课程池、有序必修课或完整路径
选项、适用时的计数选修池与数量，以及具体、双语、可验证的退出条件。阶段必须
包含必修课或路径选项；使用路径选项的阶段不再设置计数选修。

Read the site’s contribution guide before opening a change. Keep factual claims traceable to primary course pages whenever possible, disclose conflicts of interest, and update both language versions together.

## Template lineage / 模板来源

EEDIY deliberately follows the information architecture and MkDocs Material
reading patterns of [CSDIY](https://github.com/PKUFlyingPig/cs-self-learning):
topic navigation, focused course articles, search, bilingual pages, theme
switching, and page-level feedback belong to the same product family. EEDIY
adds EE-specific routes, evidence records, laboratory-safety boundaries,
resource audits, and reproducible-project review gates. It does not present
that shared template lineage as an original visual invention.

EEDIY 有意沿用
[CSDIY](https://github.com/PKUFlyingPig/cs-self-learning)
的内容架构与 MkDocs Material 阅读方式：按主题导航、聚焦单课的文章、搜索、双语页面、
主题切换和页面讨论属于同一套产品范式。在此基础上，EEDIY 增加 EE 专属路线、证据记录、
实验安全边界、资源审计与可复现项目门禁，不再把这层模板继承包装成原创视觉发明。

## License / 许可

Source code and site configuration are available under the [MIT License](LICENSE). Original editorial content is available under [CC BY 4.0](CONTENT_LICENSE.md). The CSDIY template lineage and other reused components are credited in [Third-Party Notices](THIRD_PARTY_NOTICES.md). Linked courses, books, videos, software, trademarks, and other third-party materials remain under their respective owners’ terms.

源代码与站点配置采用 [MIT License](LICENSE)；原创编辑内容采用 [CC BY 4.0](CONTENT_LICENSE.md)。CSDIY 模板来源及其他复用组件列在[第三方声明](THIRD_PARTY_NOTICES.md)中。链接到的课程、书籍、视频、软件、商标及其他第三方材料仍受各自权利人的条款约束。
