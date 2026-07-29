---
title: "Silicon Photonics Design, Fabrication and Data Analysis"
description: "University of British Columbia 的《Silicon Photonics Design, Fabrication and Data Analysis》以 KLayout、SiEPIC、gdsfactory、远程制造和测量工具链形成罕见的硅光全流程；实践价值极高，但时点、许可与地区条件需复核。"
page_type: course
course_id: "course-133"
editorial_status: "researched"
evidence_level: "R0"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 8b80ce8119b27aea -->

# Silicon Photonics Design, Fabrication and Data Analysis

## 课程简介

- **所属大学：** University of British Columbia
- **课程编号：** Phot1x
- **先修要求：** 建议先完成方向基础：电磁场与波；建议先完成方向基础：半导体器件；建议先完成方向基础：物理基础
- **方向：** [光学、光电与光子学](index.md)
- **路线角色：** 主线
- **公开材料：** 核心材料可访问
- **最近复核：** 2026-07-29

> **资料考察（R0）：** 正文于 2026-07-29 逐项核对课程官方材料，但还没有可核验的完整学习复盘，因此不冒充亲历。完成过课程的读者可以从页末提交复盘。

!!! warning "主线审计复核中"
    课程按期开放，商业工具许可、地区注册、流片日期和付费条件会变化；只返回测量数据，不邮寄芯片，必须在每次开课前人工复核。 最近审计：2026-07-29。

## 先记准 2026 run，再做任何计划

UBCx **Silicon Photonics Design, Fabrication and Data Analysis（Phot1x）** 不是随到随学的视频库，而是一门按教师节奏推进、贯穿设计、提交、制造、测量和数据分析的课程。官方 [edX course page](https://www.edx.org/learn/engineering/university-of-british-columbia-silicon-photonics-design-fabrication-and-data-ana) 在 2026-07-29 列出的 active run 为 `course-v1:UBCx+Phot1x+3T2026`：2026-09-15 开始，2026-12-08 结束，报名截至 2026-09-22；页面写 6 周、每周 3–25 小时。日历跨度大于 6 周，说明“6 周内容”不能拿来推算 tapeout 与返数日期。

这个 run 的 seat 是 `Professional Only`，复核时标价 USD 495；课程级结构化信息和 edX 通用页虽会出现 “Partially Free” 或 audit 语言，但当前 run 没有列出 audit seat。不要假设免费账户能进入 graded design submission、商业工具许可、fabrication 或 measurement data。税费、币种、退款、financial aid、单位采购与最终结算条件都要在自己的账号和地区确认，以上金额只是带日期的基准。

active-run 元数据同时标记 `hasOfacRestrictions`，课程 FAQ 指出 Iran、Cuba 与 Ukraine 的 Crimea region 无法注册。制裁与平台合规范围会变，旧名单不能替代结算时针对具体账户的资格核验；注册前必须用实际居住地和账户验证 eligibility，不得用 VPN、代购账号或虚假所在地绕过限制。

## 三道入场检查要在付款前做完

第一题：给定 220 nm SOI strip waveguide 的折射率与几何，说明 mode solver 输出的 effective index、group index、confinement 与 propagation loss 分别怎样进入 circuit model；不要求精确仿真，但要写清边界和色散假设。第二题：由两个 coupler 和两臂相位差推出理想 Mach–Zehnder interferometer 的 power transfer，解释 FSR、extinction ratio、imbalance 与 fabrication bias 如何改变 spectrum。第三题：用 Python 读取一组带 baseline 与噪声的合成 transmission data，保留原始数组，提取峰间距（如 FSR）或 autocorrelation 周期，并给出 residual 与不确定度。

至少完成前两题中的一题和第三题，才适合付款。官方先修是 introductory physics and optics，例如本科 optics 或 electromagnetics；不要求 integrated optics 背景，microwave/RF 只是加分项，MATLAB/Python 一类基础编程会有帮助。如果连波导传播常数与 circuit phase 的接口都说不清，先补电磁波导；如果脚本只输出一张平滑图而没有单位、原始数据和 residual，先补数值分析。这是 EEDIY 的付款前准备度检查，不是 UBCx admission test。

## “全流程”是一组待核合同，不是营销页上的可复现实验

课程页说 first-time designer 以带 grating coupler、splitter 与 waveguide 的 Mach–Zehnder interferometer 为主，advanced designer 可做 directional coupler、ring/racetrack/disk resonator、Bragg grating、photonic crystal、MMI、polarization/MDM 或 SWG/slot waveguide。提供方还说会用 100 keV electron-beam lithography 制造提交的设计，在自动 optical probe station 测量，并把数据交给学员分析。这些陈述确认了课程意图，却没有公开 2026 module checklist、assignment count、rubric、PDK revision、GDS acceptance rule、design-review 资格、最终 layout 截止日或 measurement-data release date。要把三层承诺分开：机构具备制造与测量能力，不等于每份版图都会被接受；某份版图被合并制造，不等于其每个测试结构都会返回有效 trace；收到数据，也不等于数据已经包含足够的 reference、metrology 与许可来支持可复现结论。

因此付款前要拿到五个答案。其一，账户是否真的能加入 `3T2026`，而不是只看到 landing page；其二，USD 495 包含哪些 graded access、certificate、software entitlement、fabrication 与 data delivery；其三，commercial license 的操作系统、硬件、license server、开始/失效日与地区限制；其四，draft review、final GDS、DRC waiver、IP/export-control 表格与迟交政策；其五，设计若未通过 review 或错过 tapeout，是否仍有 practice dataset、feedback、退款或下一批次迁移。任何一项只得到宣传语，都应先保留付款决定。

## 2016 syllabus 只能借工作流，不能借日期和分数

一份仍可访问、日期为 2016-11-15 的 [archived syllabus](https://s3.amazonaws.com/edx-course-phot1x-chrostowski/2016T3/UBCxPhot1x_Course%20Syllabus%20Schedule_2016_11b.pdf) 给出过非常具体的闭环：mode solving 与 compact circuit model、design PDF、draft layout、对 3 份同伴设计的 review、final layout、fabrication、practice data、本人设计的 measurement data、final report。它还能解释为什么本课不是“看完讲座后做个 GDS”：模型、manufacturability、design-for-test、peer review 和 data/model residual 本来就是同一条证据链。

但该文件属于 2016T3，写的是 4 周设计、当年的 UTC deadline、当年的评分比例和 70% pass line；这些都不能移植到 2026。它还说整片合并后的 design file 会与 group 分享。当前公开页没有确认 2026 是否仍采用相同分享方式，所以这条只能当 confidentiality red flag，不能写成现行政策。当前 dashboard、courseware、announcement 与 course-specific terms 必须覆盖历史 PDF。

## 先理解“一片共享芯片”，再谈我的器件

当前课程页给出的 fabrication boundary 是 220 nm silicon-on-insulator、60 nm minimum isolated feature，每位参与者约有 410 µm × 605 µm 面积，页面称可容纳大于 10 个器件。fabrication 由 University of Washington Nanofabrication Facility 与 Applied Nanotools Inc. 执行，measurement 在 UBC 完成。这里的关键措辞是 **one chip for the course**：参与者的版图被汇总制造和自动测量，不是每个人收到一片独立封装器件。

页面明确回答“不邮寄实体芯片”，只向 course participants 提供 measurement data；想要自己的芯片需要在课程中或之后另行购买。因而“fabricated”不能写成“我持有并测过芯片”，拿到数据也不能写成“我操作过 probe station”。还应向当前 run 核对 design acceptance、数据字段、wavelength grid、reference/loopback、normalization、missing trace、SEM/metrology、许可与发布时间。公共页面没有列出 2026 tapeout date；只能把它记为动态、账户内截止条件，绝不能沿用 2016 日期。

## 工具许可和 PDK 必须进入复现清单

课程页说 run 包含 Lumerical Solutions、MATLAB、Luceda 与 Tidy3D 的商业工具许可，并使用 KLayout、SiEPIC-Tools、gdsfactory 与 Python。公共 landing page 没有固定 release、PDK commit、layer map、foundry rule deck、license feature、license duration 或支持平台。课程“包含许可”也不表示永久、可转让、可在公司项目使用，或免费旁听者可获得；只有当前账号中的 entitlement 与第三方 EULA 能回答这些问题。

第一次打开合法环境就保存 OS、CPU/GPU、tool and solver version、license expiry、Python lockfile、KLayout/SiEPIC/gdsfactory version、PDK hash、layer map、DRC rules、material model 与 wavelength grid。design freeze 时再保存 netlist/GDS checksum、parameter source、corner/Monte Carlo settings、DRC report 与 rendered review PDF。商业求解器输出要带可导出的中性数据和解析/open-source sanity check，使没有相同 license 的审稿人仍能检查趋势；但不得绕过 license、复制受限 PDK 或公开 foundry rule deck。

若因地区、费用或硬件无法加入，EEDIY fallback 可以只做一个开源 MZI model/layout 与 synthetic measurement analysis：固定 PDK-free geometry、用解析 transfer function 和第二实现交叉检查、注入 linewidth/etch bias、输出 residual 与 tolerance report。它是 EEDIY supplement，不是 Phot1x submission、fabrication、UBC measurement data、grade 或 certificate，也不能用来宣称完成 full design–fabricate–test cycle。

## 版图是用户内容，也可能是受控或保密内容

edX 的 [Terms of Service](https://www.edx.org/edx-terms-service) 说明用户保留所提交 User Content 的权利，同时向 edX 与相关成员授予广泛的托管、展示、复制、格式修改和分发许可；course-specific terms 还可能追加条件。再结合 2016 syllabus 曾出现的 whole-chip file sharing，最安全的默认值是 clean-room educational design。不要上传 employer IP、未公开论文版图、第三方 NDA PDK、export-controlled structure、个人数据或无法授予平台所需权利的代码。

远程学习者默认不接触制造或测量硬件。不得自行复刻 electron-beam lithography、cleanroom wet chemistry、plasma etch、high-temperature process 或 automated probe station，也不得购买 telecom laser 后把“测自己的芯片”变成家庭实验。1550 nm 光不可见仍可伤眼，裸光纤会产生锐利碎屑。若另购芯片，任何 laser/fiber/probe-station 工作都必须进入机构批准的 laser laboratory，由机构指定的合格激光安全负责人完成 classification、enclosure/interlock、wavelength-specific eyewear、beam stop、功率计、fiber-sharps 和去能量程序；本页不授权实体测量。

## 结课有两条路线，不能混写

活动 run 路线的结课包应包括报名与付费/地区快照、许可与 PDK 清单、entry diagnostics、design specification、model and corner evidence、draft/final submission receipt、DRC/design-review 状态、提供方按实际形式返回的 measurement data（交付文件须原样保存）、处理脚本、simulation–measurement residual、uncertainty 与 final report。若版图未被接受、没有返数或未通过课程，就按事实写出，certificate 也只以 edX/UBCx 实际签发为准。

公开路线只能交 EEDIY fallback：MZI model、layout source、synthetic dataset、测试和差异报告，并明确列出未获得的 commercial entitlements、current PDK、design review、tapeout、fabrication、measurement data、grader 与 certificate。无论哪条路线，退出标准都是能够从 effective/group index 推到 circuit spectrum，从 layout rule 推到 manufacturability，并用 residual 和 uncertainty 解释 model–data mismatch。本页为 R0 官方材料桌面审读；课程仍处于 mainline `review`，每个新 run 都必须重新核开课、价格、地区、许可和 tapeout。

## 课程资源

<details markdown="1">
<summary>展开完整资源索引（1 项）</summary>

### 材料覆盖

| 类型 | 完整度 |
|---|---|
| 视频 | 完整 |
| 讲义 | 完整 |
| 练习 | 完整 |
| 实验 | 完整 |
| 考试 | 部分 |
| 代码 | 完整 |

### 资源

| 资源 | 访问 | 状态 | 复核日期 |
|---|---|---|---|
| [课程主页](https://www.edx.org/learn/engineering/university-of-british-columbia-silicon-photonics-design-fabrication-and-data-ana) | 可免费旁听 | 官方页已列出 | 2026-07-28 |

> 链接在所列日期由官方来源页发现；可访问不等于可转载。地区、账号、第三方版权和后续改版仍可能改变实际可用性。

</details>
