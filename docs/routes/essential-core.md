---
title: "精简核心路线"
description: "完成数理、电路、信号、数字、电磁、电子与一个可演示项目的最小闭环；总工期按各课程页的维护者规划估计汇总，并在每门课试学两周后校准。"
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 0cb187f02b3f6846 -->

# 精简核心路线

## 适合人群

时间有限、希望先建立完整 EE 骨架的学习者

## 最终验收

完成数理、电路、信号、数字、电磁、电子与一个可演示项目的最小闭环；总工期按各课程页的维护者规划估计汇总，并在每门课试学两周后校准。

## 阶段安排

### 数理与编程

**选课要求：** 完成全部 5 门必修，并完成该门选修候选。

- [Single Variable Calculus](../courses/mathematics/001-18-01sc.md) — **必修**; MIT; 主线; S
- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **必修**; MIT; 主线; S
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **必修**; MIT; 主线; S
- [Probabilistic Systems Analysis and Applied Probability](../courses/probability-statistics/007-6-041sc.md) — **选修候选**; MIT; 主线; S
- [Introduction to CS and Programming Using Python](../courses/programming-tools/015-6-100l.md) — **必修**; MIT; 主线; S
- [Practical Programming in C](../courses/programming-tools/016-6-087.md) — **必修**; MIT; 主线; A

**阶段退出条件：** 完成一套覆盖微积分、微分方程、线性代数与概率的校准题，正确率达到 80%；同时提交可从全新环境复现、含至少 5 个自动化检查的 Python/C 数值实验仓库。

### EE 核心

**选课要求：** 完成全部 5 门必修。

- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **必修**; MIT; 主线; S
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **必修**; MIT; 主线; S
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **必修**; MIT; 主线; S
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **必修**; Cornell University; 主线; S
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **必修**; Cornell University; 主线; S

**阶段退出条件：** 对同一系统给出电路、信号、数字逻辑、电磁场与晶体管五个视角的模型，提交手算—仿真对照表；关键量误差低于 10%，超限项须有量纲一致的原因分析。

### 工程收束

**选课要求：** 完成全部 2 门必修。

- [The Art and Science of PCB Design](../courses/pcb-eda/055-iap-pcb-2026.md) — **必修**; MIT; 主线; S
- [Digital Systems Design Using Microcontrollers](../courses/capstone-practice/057-ece-4760-ece-5730.md) — **必修**; Cornell University; 主线; S

**阶段退出条件：** 交付可演示的板级作品，仓库须含需求、原理图、PCB、BOM、固件、装配说明和连续测试记录；预先声明的 5 个端到端验收用例全部通过。

## 执行规则

- 按每个阶段的选课要求完成全部必修与指定数量的选修；若提供完整路径选项，只选择一条并按序完成其中全部课程；可选补充只用于填补明确缺口。
- 阶段内至少完成一个可复现产物，并把失败记录纳入复盘。
- 涉及市电、高压、射频辐射、激光、化学品或加工设备时，必须遵守本地法规并由合格人员监督。
