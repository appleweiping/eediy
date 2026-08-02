---
title: "数字 VLSI 与芯片设计"
description: "CMOS 逻辑、时序、功耗、物理设计与验证，区分开源流程和受限商业 EDA。"
page_type: track
track_id: "track-vlsi-ic"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: eabf2a5f2b27653a -->

# 数字 VLSI 与芯片设计

## 方向定位

CMOS 逻辑、时序、功耗、物理设计与验证，区分开源流程和受限商业 EDA。

## 建议先修方向

- [微电子学](../microelectronics/index.md)
- [数字逻辑与计算结构](../digital-logic/index.md)

## 6.374 的公开档案能独立承担数字 IC 主轴

[MIT 6.374](050-6-374.md)的[官方 OCW 页面](https://ocw.mit.edu/courses/6-374-analysis-and-design-of-digital-integrated-circuits-fall-2003/)以讲义、题目、考试和 design material，把 transistor switching、delay、power、combinational/sequential block 与 physical design 连成一条可自学主线。它来自 2003 年：process、SPICE、standard cell 与 layout flow 的概念仍可复用，具体数值和工具必须标记年代。第一次学习可以沿课程次序完成 inverter/device delay、logic sizing、timing/power、memory 与 layout 题，再把 design task 迁移到开放 teaching library；不能把现代工具跑通后反称原课程实验已经复现。

学习记录可以让同一个 inverter chain 贯穿前半课程：手算 logical effort 或 RC trend，用 SPICE/library 查 delay 与 transition，再在 larger block 的 critical path 中寻找同类负载效应。课程题给出的是方法与历史工艺语境，迁移后的数值由新 library/corner 决定；两组结果并列比强行对齐更有信息。

## EECS 151、6.884 与 ECE 4740 各自只补一个缺口

[Berkeley EECS 151](044-eecs-151.md)的[官方 catalog](https://www2.eecs.berkeley.edu/Courses/EECS151/)适合作为现代 curriculum 与 assessment 范围参照；公开 catalog 与 HKN solved exam 可用，但当前和历史 teaching site 都转向 CalNet，不能视作 open lab。[MIT 6.884](049-6-884.md)的[官方 OCW 归档](https://ocw.mit.edu/courses/6-884-complex-digital-systems-spring-2005/)补 complex digital system，原作业受 commercial EDA 与旧 cell assumption 限制。[Cornell ECE 4740](051-ece-4740.md)的[官方 OCW 页面](https://ocw.ece.cornell.edu/ece-4740-course-details/)公开 VLSI systems 材料和 lab，但 archive 列 Lab 1–5，课程说明又写 four extensive labs；两种官方表述应并列，不能擅自抹平。

完成 6.374 后，按项目需要从 modern scope、system complexity 或 lab intent 中取一个补充。四套 synthesis/layout flow 从头叠加只会重复工具步骤；login-protected starter、answer 与 staff repository 也不应从镜像绕取。

补充材料应回答明确问题：EECS 151 用于核对现代课程覆盖和 exam style，6.884 用于观察复杂系统 decomposition，ECE 4740 用于理解公开 lab prompt 与 system workflow。选择时注明采用的年份、公开入口和未获得的 grader/tool access。这样 historical archive、catalog reference 与 hands-on prompt 各自保有身份，不会拼成一门并不存在的“联合课程”。

## 一条 ready/valid datapath 要在 RTL、cell timing 与 physical path 中对齐

[微电子学](../microelectronics/index.md)中的 MOS operating region、parasitic capacitance、inverter transfer 与 sizing effect，以及[数字逻辑](../digital-logic/index.md)中的 combinational/sequential logic、FSM、pipeline、clock 与 reset，在一个 single-clock ready/valid datapath 上相遇。先写 cycle-level contract 与 self-checking testbench，覆盖 backpressure、reset、overflow、latency 和 continuous traffic，再估算 critical logic depth、fanout 与 register boundary。

cycle contract 应明确 input 在 `valid && ready` 时被接收、output 在 backpressure 期间保持不变，以及 reset 前后 outstanding transaction 怎样处理。scoreboard 用 transaction identifier 对齐 reference result 与 output cycle，assertion 检查 protocol stability 和 no-drop/no-duplicate。定点 arithmetic 还需把 sign extension、rounding 和 saturation 写入 reference model，避免 protocol 正确却数值定义漂移。

synthesis 后检查 inferred cell、buffer、memory/multiplier mapping 与 combinational loop；place-and-route 后检查 wire delay、congestion、clock tree、slew 与 capacitance。同一个 input vector 应能从 port cycle 追到 synthesized register boundary 和最慢 physical path，即使 hierarchy name 被工具改写也要建立映射。waveform 目测不能替代 assertion，引用 cell delay 也不能替代 load、drive 与 parasitic trend。

三层对齐可由一张 path table 完成：RTL expression 对应 synthesized cell arc，cell arc 再对应 placed instance、net 与 physical coordinate。若 critical path 在综合后换成另一条逻辑，应解释 mapping 或 optimization；若布线后 wire delay 主导，则要从 congestion、fanout 或 placement 查原因。功能向量和 timing path 使用同一 pipeline stage，才能避免“功能测试一条路径、STA 讨论另一条路径”。

## 开放 EDA 产生教学实现，不会自动产生 foundry signoff

Verilator/GTKWave 可做 regression，Yosys 做 synthesis，OpenROAD/OpenSTA 做 implementation/timing，KLayout 检查 geometry。每次运行注明 tool release、Liberty/LEF/PDK source、corner、constraint、seed 与 license，并把 simulation、synthesis 与 physical source 分开。它们与课程中的 VCS、Design Compiler、Innovus、Vivado、PYNQ 或 legacy cell environment 不同；迁移结果只能说明完成了功能相近的练习。

没有 authorized PDK 和完整 design rule 时，只报告 educational library 上的 area、timing、routing 与 geometry。manufacturable、tape-out ready、foundry signoff 和 silicon validation 都需要当前流程未提供的证据。课程公开材料也缺 packaging、完整 IR-drop/EM condition 与 post-silicon data；由 activity 和 library 估计的数值应称 power proxy，并说明缺少的 parasitic、process 与 workload information。

开放 flow 中的每个输入也要可追溯：Liberty 决定 cell timing/power，LEF 决定 abstract geometry，technology LEF 与 routing rule 决定布线约束，SDC 决定 clock 与 I/O assumption。混用不同来源或不兼容 corner 会产生外观完整却物理含义不一致的结果。DRC clean 仅表示所加载规则没有报错，无法替代缺失的 foundry deck 与 signoff extraction。

## 一条 MAC pipeline 要一直推到第一次 negative slack

实现带 ready/valid 的 fixed-point multiply-accumulate core，定义 bit width、rounding/saturation、reset、latency 与 target throughput。用 reference model、directed corner 与 random vector 核对 arithmetic，再比较一、二、三段 pipeline。每个版本运行 netlist equivalence、synthesis、place-and-route 与 STA，在 3 个 clock constraint 下列出 cell area、utilization、wire length、worst slack 与 power proxy，同时区分 clock frequency 和 effective data throughput。

第一次 negative slack 是核心诊断材料：由 report 找 startpoint、endpoint、logic/wire delay 与 transition violation，回到 RTL 判断应重构 logic、增加 pipeline、降低 fanout 还是调整 physical constraint。手算 logic depth 与 load trend 用于检查 STA 方向，不替代 library data。项目应包含 RTL、assertion/test、reference vector、script、constraint、library information、timing/congestion/geometry output 与该负裕量版本。layout screenshot 只有与 functional equivalence、corner 和 constraint variation 对应时，才能成为可工作的设计论证。

三种 pipeline depth 的比较还要对齐有效 transaction：额外 register 会增加 latency，却可能提高 clock frequency；backpressure 和 bubble 又会降低实际 throughput。分别报告 nominal cycle latency、maximum accepted rate 和给定 traffic trace 的 delivered rate，面积/功耗代理才有相同工作量基准。修复负裕量后重跑 equivalence 与 protocol regression，确认 timing optimization 没有改变 rounding、reset 或 ready/valid 行为。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Analysis and Design of Digital Integrated Circuits](050-6-374.md) | MIT | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Digital Design and Integrated Circuits](044-eecs-151.md) | University of California, Berkeley | 可替代 | 公开材料导读 | 未核到公开练习 |
| [VLSI Systems](051-ece-4740.md) | Cornell University | 补充材料 | 公开材料导读 | 部分开放或受限 |
| [Complex Digital Systems](049-6-884.md) | MIT | 补充材料 | 公开材料导读 | 部分开放或受限 |
