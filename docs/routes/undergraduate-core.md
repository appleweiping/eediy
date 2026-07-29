---
title: "本科核心审计路线"
description: "覆盖 ABET 风格完整性检查所需的数学、自然科学、工程核心、实验和综合设计，但不宣称任何认证。"
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: f3d8a61cc1345ada -->

# 本科核心审计路线

## 适合人群

希望按本科培养深度系统补齐基础的学习者

## 最终验收

覆盖 ABET 风格完整性检查所需的数学、自然科学、工程核心、实验和综合设计，但不宣称任何认证。

## 阶段安排

### 阶段 0：诊断与工具

**选课要求：** 完成全部 6 门必修。

- [Single Variable Calculus](../courses/mathematics/001-18-01sc.md) — **必修**; MIT; 主线; S
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **必修**; MIT; 主线; S
- [Classical Mechanics](../courses/physics/010-8-01sc.md) — **必修**; MIT; 主线; S
- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **必修**; MIT; 主线; A
- [Introduction to CS and Programming Using Python](../courses/programming-tools/015-6-100l.md) — **必修**; MIT; 主线; S
- [Practical Programming in C](../courses/programming-tools/016-6-087.md) — **必修**; MIT; 主线; A

**阶段退出条件：** 在限时诊断中取得 80% 以上，并用同一仓库复现一个力学或电磁实验的数据采集、单位检查与拟合流程；换一台机器后仅凭 README 可重建全部图表。

### 阶段 1：电路与动态系统

**选课要求：** 完成全部 3 门必修；其余 1 门仅在需要补缺时选学。

- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **必修**; MIT; 主线; S
- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **必修**; MIT; 主线; S
- [Introduction to Electronics, Signals, and Measurement](../courses/electronics-laboratory/024-6-071j.md) — **可选补充**; MIT; 主线; A
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **必修**; MIT; 主线; S

**阶段退出条件：** 从微分方程推导一个二阶电路的状态与频域模型，测量或仿真其阶跃和扫频响应；主极点、稳态增益和带宽与预测值偏差均不超过 5%。

### 阶段 2：概率、数字与场

**选课要求：** 完成全部 4 门必修。

- [Probabilistic Systems Analysis and Applied Probability](../courses/probability-statistics/007-6-041sc.md) — **必修**; MIT; 主线; S
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **必修**; MIT; 主线; S
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **必修**; Cornell University; 主线; S
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **必修**; Cornell University; 主线; S

**阶段退出条件：** 实现一个受随机输入驱动的数字模块并完成不少于 1000 组可复现测试向量，同时提交其互连场模型；逻辑失配为零，场仿真的功率平衡残差低于 5%。

### 阶段 3：实验和制造

**选课要求：** 完成全部 3 门必修。

- [Introductory Analog Electronics Laboratory](../courses/analog-electronics/026-6-101.md) — **必修**; MIT; 主线; S
- [The Art and Science of PCB Design](../courses/pcb-eda/055-iap-pcb-2026.md) — **必修**; MIT; 主线; S
- [Digital Systems Design Using Microcontrollers](../courses/capstone-practice/057-ece-4760-ece-5730.md) — **必修**; Cornell University; 主线; S

**阶段退出条件：** 制造并调通一块含模拟前端与数字控制的 PCB，保留可追溯的校准数据、至少 10 个工作点的测试矩阵、返修记录和实物照片；所有需求都映射到测试证据。

### 阶段 4：专项选择

**选课要求：** 完成全部 1 门必修，并从 5 门选修候选中选择 2 门。

- [Digital Signal Processing](../courses/dsp/088-res-6-008.md) — **必修**; MIT; 主线; S
- [Principles of Digital Communications I](../courses/communications/100-6-450.md) — **选修候选**; MIT; 主线; S
- [Introduction to Linear Dynamical Systems (2008 Archive)](../courses/control-systems/068-ee-263.md) — **选修候选**; Stanford University; 主线; S
- [Power Electronics](../courses/power-electronics/114-6-622.md) — **选修候选**; MIT; 主线; S
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **选修候选**; Cornell University; 主线; A
- [Introduction to Photonics](../courses/optics-photonics/132-108106135.md) — **选修候选**; IIT Madras / NPTEL; 主线; A

**阶段退出条件：** 把信号处理主干与所选两个专项整合为一份综合设计评审，分别定义不少于 2 个子系统指标，并用仿真、测量或公开数据验证；最终报告须包含接口风险与一次失败迭代。

## 执行规则

- 按每个阶段的选课要求完成全部必修与指定数量的选修；若提供完整路径选项，只选择一条并按序完成其中全部课程；可选补充只用于填补明确缺口。
- 阶段内至少完成一个可复现产物，并把失败记录纳入复盘。
- 涉及市电、高压、射频辐射、激光、化学品或加工设备时，必须遵守本地法规并由合格人员监督。
