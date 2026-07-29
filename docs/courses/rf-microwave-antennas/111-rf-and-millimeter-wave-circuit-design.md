---
title: "RF and Millimeter-Wave Circuit Design"
description: "Eindhoven University of Technology 的《RF and Millimeter-Wave Circuit Design》以 Qucs-S 与 Octave 仿真构建射频毫米波电路实践主线；约七成内容可复现，硬件为可选项。"
page_type: course
course_id: "course-111"
editorial_status: "researched"
evidence_level: "R0"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 47cbd71dcad5385a -->

# RF and Millimeter-Wave Circuit Design

## 课程简介

- **所属大学：** Eindhoven University of Technology
- **课程编号：** RF and Millimeter-Wave Circuit Design
- **先修要求：** 建议先完成方向基础：电磁场与波；建议先完成方向基础：电路分析；建议先完成方向基础：通信系统
- **方向：** [射频、微波与天线](index.md)
- **路线角色：** 主线
- **公开材料：** 核心材料可访问
- **最近复核：** 2026-07-29

> **资料考察（R0）：** 正文于 2026-07-29 逐项核对课程官方材料，但还没有可核验的完整学习复盘，因此不冒充亲历。完成过课程的读者可以从页末提交复盘。

## 先把这门课看成五次 design review

Eindhoven University of Technology 在 Coursera 上的 **RF and millimeter-Wave Circuit Design** 不是器件名词速览。提供方 [course page](https://www.coursera.org/learn/rf-mmwave-circuit-design) 在 2026-07-29 显示 6 个 module、19 个 assignment，课程由 wireless system 开场，依次处理 amplifier、mixer、oscillator 与 synthesizer。Module 2–6 各有一个 peer-reviewed design lab：Wireless Tin Can Telephone system analysis、LNA/PA、up/down-conversion mixer、VCO，以及 frequency-divider/phase-detector synthesizer。把它读成五次 design review，比“看完 6 周视频”更接近课程的工程骨架。

同一页面说明全部 design lab 对证书是 optional，但推荐完成；约 70% 可用 simulation tools 做，另约 30% 需要电子实验室或购买现成器件。这个 70/30 是提供方对其 lab 构成的描述，不是 EEDIY 的安全建议，也不意味着任何家庭台架都合规。页面是持续更新的 Coursera offering，没有在公开营销页给出固定学期或 starter-file 版本；学习记录必须写审读日期和实际下载材料的版本。

## 三个入口题比“修过模拟电路”更可靠

第一题：给定载频、free-space Friis 传播模型、发射功率、天线增益、距离、接收带宽、290 K 参考噪声温度、noise figure 与目标 SNR，做一份完整 link budget，明确 dB/dBm、thermal noise、implementation margin 和 receiver sensitivity。第二题：从一个 2-port 的 S-parameter 写出 input/output reflection、transducer gain 与 stability 判断，再用 Smith chart 说明匹配点为什么不是“让所有反射都等于零”。第三题：对 mixer 或 oscillator 画 frequency plan，标 fundamental、image、LO leakage、主要 harmonic，并解释 phase noise 或 compression 怎样传到系统指标。

三题至少完成两题，且每个单位和 reference plane 清楚，才开始 Module 1。只会低频 small-signal gain、不会 S-parameter 和 noise cascade，应先补 microwave network；只会套 Friis path-loss、不会从 sensitivity 反推 block specification，也不宜跳进 PA/VCO lab。此门槛是 EEDIY placement diagnostic，不是 Coursera enrollment requirement。

## 19 个 assignment 与 5 个 lab 是两条并行证据链

Module 1 有 1 个 assignment，Module 2–5 各有 4 个，Module 6 有 2 个，合计 19 个；题目从 wireless-system introduction、path loss、sensitivity 与 selectivity，一路到 LNA matching、PA classes、mixer image/harmonics、oscillator phase noise 与 type-I/type-II PLL。每个 module 还提供 supporting material，若已合法取得，应先做 assessment 再看 solution video；solution 只用于定位 specification、equation、simulation setup 或 interpretation 中的第一处错误。

五个 peer-review lab 另成一条设计链。每次 review 都保存 specification table、assumption、schematic or block diagram、simulation configuration、pass/fail plot、corner/sensitivity check 与 open issue。每次评审还要保留至少一个被拒绝的候选方案，写明它在哪个指标、角落条件或稳定性检查中失败，以及哪项参数变化导致结论改变。同伴意见应逐条标为接受、拒绝或待验证，并指向对应曲线或计算；没有证据的“看起来更好”只能留在未决项。还要记录变更前后的指标表，防止最后一张原理图成为无法回放的调参偶然。若两个方案都通过名义点，则必须用温度、模型容差或负载扰动说明取舍，不能按图形美观决定。官方任务允许 simulation 与 implementation 两种层次，但硬件并非证书必要条件；EEDIY 默认只完成 simulation 部分。没有购买或没有 “Full Course, No Certificate” 权限时，不得从非官方镜像获取 locked assignment、supporting file 或 solution video。

## 工具版本必须跟着产物，而不是跟着课程标题

Module 1 明列 Qucs-S 与 Octave 入门，但公开页面没有 pin 具体 release。到 2026-07-29，官方 [Qucs-S repository](https://github.com/ra3xdh/qucs_s) 的最新 release 为 26.1.1；其 README 说明自 25.1.0 起只支持 Qt6。官方 [installation guide](https://qucs-s-help.readthedocs.io/en/latest/installation/installing-qucs-s.html) 还指出不同平台随包提供的 backend 不同：Windows 包含 ngspice 与 QucsatorRF，macOS 包只带 QucsatorRF，其他 backend 可能要另装。课程文件若在新版本报错，先记录原文件、backend、netlist 和报错，不要静默换 simulator 后继续比较数值。

GNU 官方 [download page](https://octave.org/download.html) 在同一审读日列出 Octave 11.3.0 为 stable release。它只是当前可复现环境的候选，不代表 TU/e 的 supporting files 原本以 11.3.0 验证。每个 lab 的 `environment.md` 应记录 OS、Qucs-S、backend、Octave、器件模型来源与 hash；升级前保存 baseline plot，升级后以 tolerance 比较，而不是凭图形大致相似。

## 五次 review 各自有一个不能含糊的判断

Wireless system review 要从 range、bandwidth、sensitivity、selectivity 和 distortion 推到 transceiver block specs，不能先挑器件再倒算需求。Amplifier review 要分别回答 LNA 的 noise/matching/stability 与 PA 的 gain/compression/efficiency，不把 small-signal S-parameter 当成大信号结论。Mixer review 要保留完整 frequency table，明确 wanted product、image、spur 与 filtering assumption。Oscillator review 要同时看 startup condition、amplitude limiting、tuning range、phase noise 和 buffer/load pulling。Synthesizer review 要解释 loop type、bandwidth、reference/divider noise 与 lock behavior。

若 Module 2 结束仍无法让 system budget 与 block specs 对账，退出到 link budget；若 Module 3 的 LNA 在 nominal gain 达标但 stability/noise 没有证据，不得进入 PA implementation；若到 Module 5 仍用单一 transient 波形宣称 phase-noise performance，应停下补 stochastic/frequency-domain interpretation。退出条件是为了阻止漂亮 plot 掩盖错误 metric。

## “可在家搭 transceiver”不是本页的实施许可

课程页面用 70% simulation、30% lab/components 描述 optional labs，也提到可以把 transceiver 做成实体。EEDIY 的默认范围仍是 simulation-only：不制作、驱动或连接 RF PA，不把 oscillator/mixer chain 接到 antenna，不向自由空间发射，不连接来历不明的 VNA、signal generator、bias tee、battery 或 mains-powered instrument。Tin Can Telephone lab 的名称也不改变这一边界。

若机构实验室批准实体部分，必须由 RF 合格人员监督，并在上电前完成 frequency authorization、exposure assessment、power budget、50 Ω termination、rated attenuator/cable/connector、DC current limit、ESD control、shielding/interlock 与 emergency shutdown review。不得带电换接高功率端口，不得直视或触碰开放 waveguide/aperture，不得把器件的绝对最大额定值当工作点。TU/e 关于 [remote RF laboratory](https://research.tue.nl/en/publications/rf-circuits-laboratory-for-remote-learning-and-massive-open-onlin/) 的论文说明远程实验是专门搭建的受控基础设施，并不等同于随意复制家庭台架。

## 没有平台权限时，只能做明确标注的补充项目

已获得课程权限者应优先完成官方 19 个 assignment 和可用的 5 个 peer-review lab，并保留 Coursera feedback；平台 grade、peer review 与 certificate 不能由本地脚本替代。Coursera FAQ 说明材料、assignment 与证书通常需要购买 certificate experience；符合条件者可能有 free trial，某些课程可能提供 Full Course, No Certificate，二者都不是保证。付费、登录和地区可用性应在开始前实际检查。

没有权限者可做一个 clean-room transceiver budget notebook：只根据公开教材公式自建 specification、block cascade、noise/linearity budget 和五个理想化 simulation block，不复制 locked prompt、supporting file 或 solution。它必须标为 EEDIY supplement，既不是官方 lab，也不能获得 Coursera grade。结课包应区分 official attempted、official inaccessible、EEDIY supplement 三栏，并附三道门槛题、19 项状态表、5 次 design review、环境锁定文件和安全范围。

本页为 R0 官方页面与工具文档审读，没有声称完成课程或实体实验。纠错请给出课程 ID 111、具体 module/assignment/lab、审读日期与提供方来源；不得提交付费材料、同伴私有作业、危险 RF 台架记录或未经许可的发射结果。

## 课程资源

<details markdown="1">
<summary>展开完整资源索引（1 项）</summary>

### 材料覆盖

| 类型 | 完整度 |
|---|---|
| 视频 | 完整 |
| 讲义 | 部分 |
| 练习 | 完整 |
| 实验 | 完整 |
| 考试 | 无公开材料 |
| 代码 | 完整 |

### 资源

| 资源 | 访问 | 状态 | 复核日期 |
|---|---|---|---|
| [课程主页](https://www.coursera.org/learn/rf-mmwave-circuit-design) | 注册后访问 | 官方页已列出 | 2026-07-28 |

> 链接在所列日期由官方来源页发现；可访问不等于可转载。地区、账号、第三方版权和后续改版仍可能改变实际可用性。

</details>
