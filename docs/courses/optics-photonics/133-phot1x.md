---
title: "Silicon Photonics Design, Fabrication and Data Analysis"
description: "University of British Columbia 的《Silicon Photonics Design, Fabrication and Data Analysis》在注册课程内使用 KLayout、SiEPIC、gdsfactory、远程制造与测量设计材料；公开 edX 页没有固定 PDK 或工程包。"
page_type: course
course_id: "course-133"
editorial_status: "catalogue"
evidence_level: "R0"
reviewed_at: "2026-07-31"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: df38a8fe1d05942c -->

# University of British Columbia Phot1x: Silicon Photonics Design, Fabrication and Data Analysis

## 课程简介

- **所属大学：** University of British Columbia
- **课程编号：** Phot1x
- **官方先修：** Phot1x 提供方列出 introductory physics/optics，未将 integrated optics 列为先修
- **本站建议背景：** 本站未另设准备条件
- **访问条件：** 需付费访问
- **资料状态：** 2026-07-31；资料索引

### 当期课程、价格与先修

UBCx **Silicon Photonics Design, Fabrication and Data Analysis（Phot1x）** 适合愿意为当期 fabrication/data-return 权益付费的人。它是 instructor-paced 的
design–submit–fabricate–measure 课程。2026-07-29，[当前 edX 课程页及页内 FAQ](https://www.edx.org/learn/engineering/university-of-british-columbia-silicon-photonics-design-fabrication-and-data-ana)
列 active run `course-v1:UBCx+Phot1x+3T2026`：2026-09-15 开始、2026-12-08 结束、
2026-09-22 截止报名；标称 6 周、每周 3–25 小时。seat 是 `Professional Only`，当时
USD 495，没有列 audit。这些都是该次页面快照，不能当作长期有效的免费资源或默认必修。

购买资格、地区限制、税费、退款和最终价格只以真实账号的当前页面为准。技术上，学习者至少要能
说明 220 nm SOI waveguide 的 effective/group index、confinement 与 loss 如何进入 circuit
model，由 coupler 与 arm phase 推 MZI spectrum，并从 noisy trace 提取 FSR 与 residual；
官方只列 introductory physics/optics，页面没有把 integrated optics 写成先修。

### 设计、制造与返数

[SiEPIC 官方培训页](https://siepic.ca/trainings/online-training/) 与 edX 页面把核心描述为
MZI/component design、submission、fabrication 和 returned measurement data。first-time designer
以 grating coupler、splitter、waveguide 组成 MZI，advanced option 才扩到 resonator、Bragg、
photonic crystal、MMI、MDM 与 SWG/slot。公开页面仍没有 2026 module list、rubric、PDK revision、
GDS rule、review eligibility、tapeout 或 data-release date。

[2016-11-15 archived syllabus](https://s3.amazonaws.com/edx-course-phot1x-chrostowski/2016T3/UBCxPhot1x_Course%20Syllabus%20Schedule_2016_11b.pdf) 记录过 model、design PDF、draft layout、3 份 peer review、final layout、fabrication、practice/measurement data 与 report 的顺序；它属于 2016T3，4 周设计期、UTC deadline、70% pass line 和 whole-chip sharing 都不能当成 2026 政策。

当前页面还写明 220 nm SOI、60 nm minimum isolated feature、每人约
410 µm × 605 µm、可放超过 10 个 device；fabrication 由 University of Washington
Nanofabrication Facility 与 Applied Nanotools Inc. 执行，measurement 在 UBC。关键是
**one chip for the course**：课程默认不包含向每位参与者寄送个人芯片，只返回 measurement
data，参与者不会亲自操作 probe station。当前 FAQ 同时称参与者可在课程中或结束后另购个人
芯片；是否仍开放、价格、shipping 与其他条件都要按当期页面或官方支持答复复核。

### 付费前要确认的问题

从当前账号或官方支持确认：其一，PDK、solver 与 license 在什么日期和平台可用；其二，design
review、final GDS、DRC 与 tapeout 的资格和截止日；其三，版图未通过或错过 tapeout 时是否仍有
practice data、feedback、refund 或下一期迁移。把带日期的官方答复保存在购买记录旁即可。
这比展开平台法律条款更直接，也决定项目究竟能走到 model、layout、fabrication 还是 returned data。

### 工具版本要和提交版对得上

页面称包含 Lumerical Solutions、MATLAB、Luceda、Tidy3D，并使用 KLayout、SiEPIC-Tools、gdsfactory 与 Python，但未公开固定 release、PDK commit、layer map、rule deck、license duration 或 supported platform。第一次进入合法环境时，先记下 solver/tool version（工具版本）、Python lockfile、PDK hash、material model 与 wavelength grid（波长网格）；design freeze（设计冻结）后，让 netlist、GDS、DRC、corner/Monte Carlo 设置和 review PDF 都指向同一提交版。若中途升级 solver 或 compact model，先用旧设计重跑一个基准，再比较返数；否则很容易把工具漂移误判为制造偏差。

### 什么才算完成 Phot1x

正式学员按账号实际开放的 entitlement、PDK、submission、review、fabrication、data 与 certificate 往前走；如果版图没有通过 review，或最后没有返数，课程体验就停在对应阶段。公开替代可以做 PDK-free MZI model/layout、synthetic data、tolerance 和 simulation–measurement residual，但它与 Phot1x submission 或 tapeout 是两条不同路径。比较 simulation 与 measurement 时，先对齐 wavelength、normalization 和 reference port，再把 residual 分成 model、fabrication、measurement 与暂时无法解释的部分；这比只给一个拟合误差更能看出问题来自哪里。

remote learner 不会亲自执行 e-beam、wet chemistry、plasma、probe station 或 1550 nm laser/fiber 实验。真正能学到的是把 effective/group index 接到 spectrum、把 layout rule 接到 manufacturability，再从 raw data 重建 residual 与 uncertainty；能否经历完整 full cycle，则取决于这一期实际开放的账户权益和返数。

## 课程资源

本页已在正文中按版本与访问条件放置核心资料链接。为避免把前序课程、历史 syllabus 或受限材料脱离上下文误列为本课资源，这里不重复生成通用资源清单。

## 资源汇总

本页没有脱离上下文重复列出资源；正文中的链接及其版本说明构成本次核对的完整汇总。
