---
title: "数字系统、FPGA 与体系结构"
description: "实现并验证一个流水线处理器或自定义加速器，并在 FPGA 或可复现仿真环境中运行软件。"
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: c45834519c480e59 -->

# 数字系统、FPGA 与体系结构

## 适合人群

希望理解从 RTL 到处理器和 SoC 的硬件学习者

## 最终验收

实现并验证一个流水线处理器或自定义加速器，并在 FPGA 或可复现仿真环境中运行软件。

## 阶段安排

### 逻辑到计算机

**选课要求：** 完成全部 1 门必修，并从 2 门选修候选中选择 1 门。

- [Computation Structures](../courses/digital-logic/037-6-004.md) — **必修**; MIT; 主线; S
- [Build a Modern Computer from First Principles: From Nand to Tetris, Part I](../courses/digital-logic/039-nand2tetris-i.md) — **选修候选**; Hebrew University of Jerusalem; 替代; S
- [Build a Modern Computer from First Principles: From Nand to Tetris, Part II](../courses/computer-architecture/040-nand2tetris-ii.md) — **选修候选**; Hebrew University of Jerusalem; 替代; S

**阶段退出条件：** 从布尔逻辑实现带最小指令集的数据通路与控制器，并用参考解释器差分验证不少于 1000 条随机指令序列；最终波形中不得出现未解释的 X/Z 状态。

### RTL 与板级实现

**选课要求：** 完成全部 1 门必修，并从 3 门选修候选中选择 1 门。

- [Introductory Digital Systems Laboratory](../courses/fpga-soc/042-6-111.md) — **必修**; MIT; 主线; A
- [Digital Systems Laboratory](../courses/fpga-soc/043-ece-385.md) — **选修候选**; University of Illinois Urbana-Champaign; 替代; A
- [Digital Design and Integrated Circuits](../courses/vlsi-ic/044-eecs-151.md) — **选修候选**; University of California, Berkeley; 替代; B
- [Digital Systems Architecture](../courses/fpga-soc/045-ee-180.md) — **选修候选**; Stanford University; 补充; A

**阶段退出条件：** 将一个含跨时钟域接口的 RTL 模块部署到 FPGA，完成 lint、约束与静态时序检查；目标时钟下最差裕量非负，板上输出与仿真黄金向量逐项一致。

### 架构与 SoC

**选课要求：** 完成全部 2 门必修，并从 3 门选修候选中选择 1 门。

- [Computer Architecture](../courses/computer-architecture/046-ece-4750.md) — **必修**; Cornell University; 主线; A
- [Computer System Architecture](../courses/computer-architecture/047-6-823.md) — **选修候选**; MIT; 替代; A
- [Great Ideas in Computer Architecture](../courses/computer-architecture/048-cs-61c.md) — **选修候选**; University of California, Berkeley; 替代; A
- [Advanced Microcontroller Design and System-on-Chip](../courses/fpga-soc/052-ece-5760.md) — **选修候选**; Cornell University; 替代; A
- [Secure Hardware Design](../courses/hardware-security/053-6-5950.md) — **必修**; MIT; 主线; A

**阶段退出条件：** 实现流水线处理器或自定义加速器，运行至少 3 个基准并与软件参考结果零差异；报告吞吐量、面积和功耗代理值，并针对资产与信任边界完成一次威胁检查。

## 执行规则

- 按每个阶段的选课要求完成全部必修与指定数量的选修；若提供完整路径选项，只选择一条并按序完成其中全部课程；可选补充只用于填补明确缺口。
- 阶段内至少完成一个可复现产物，并把失败记录纳入复盘。
- 涉及市电、高压、射频辐射、激光、化学品或加工设备时，必须遵守本地法规并由合格人员监督。
