---
title: "嵌入式与智能硬件"
description: "完成一个含传感、实时控制、通信、原理图/PCB、测试记录和演示视频的嵌入式系统。"
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 43d04b1b154b370e -->

# 嵌入式与智能硬件

## 适合人群

希望从数字逻辑走到 MCU、实时系统、PCB 和完整硬件作品的学习者

## 最终验收

完成一个含传感、实时控制、通信、原理图/PCB、测试记录和演示视频的嵌入式系统。

## 阶段安排

### 底层基础

**选课要求：** 完成全部 4 门必修；其余 1 门仅在需要补缺时选学。

- [Introduction to CS and Programming Using Python](../courses/programming-tools/015-6-100l.md) — **必修**; MIT; 主线; S
- [Practical Programming in C](../courses/programming-tools/016-6-087.md) — **必修**; MIT; 主线; A
- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **必修**; MIT; 主线; S
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **必修**; MIT; 主线; S
- [Digital Design and Computer Architecture](../courses/digital-logic/038-ddca.md) — **可选补充**; ETH Zurich; 替代; S

**阶段退出条件：** 用 C 实现一个带寄存器级外设模型的驱动，并建立主机端参考模型；至少 200 个边界与随机测试全部通过，逻辑分析仪或时序仿真证明建立/保持裕量满足数据手册。

### 裸机与实时

**选课要求：** 完成全部 1 门必修，并从 2 门选修候选中选择 1 门。其余 1 门为可选补充，不计入本阶段选修数。

- [Computer Systems from the Ground Up](../courses/embedded-systems/058-cs-107e.md) — **必修**; Stanford University; 主线; S
- [Embedded Systems: Shape the World](../courses/embedded-systems/059-ee-319k-volume-1.md) — **选修候选**; The University of Texas at Austin; 主线; S
- [Real-Time Embedded Systems Concepts and Practices](../courses/real-time-cps/063-real-time-embedded-systems-1.md) — **选修候选**; University of Colorado Boulder; 替代; A
- [Real-Time Embedded Systems Theory and Analysis](../courses/real-time-cps/064-real-time-embedded-systems-2.md) — **可选补充**; University of Colorado Boulder; 替代; A

**阶段退出条件：** 实现含中断、定时任务与故障恢复的裸机或 RTOS 原型，报告最坏执行时间、CPU 占用与 1000 个周期的抖动分布；所有截止期满足预先声明的预算。

### 系统项目

**选课要求：** 完成全部 2 门必修，并完成该门选修候选。其余 1 门为可选补充，不计入本阶段选修数。

- [The Art and Science of PCB Design](../courses/pcb-eda/055-iap-pcb-2026.md) — **必修**; MIT; 主线; S
- [Digital Systems Design Using Microcontrollers](../courses/capstone-practice/057-ece-4760-ece-5730.md) — **必修**; Cornell University; 主线; S
- [Real-Time Mission-Critical Systems Design](../courses/real-time-cps/065-real-time-embedded-systems-3.md) — **选修候选**; University of Colorado Boulder; 替代; A
- [Real-Time Project for Embedded Systems](../courses/real-time-cps/066-real-time-embedded-systems-4.md) — **可选补充**; University of Colorado Boulder; 替代; A

**阶段退出条件：** 完成含传感、通信、自制 PCB 与固件更新路径的智能硬件，给出功耗预算和失效注入记录；不少于 20 个自动化系统测试通过，并提供连续 30 分钟运行日志。

## 执行规则

- 按每个阶段的选课要求完成全部必修与指定数量的选修；若提供完整路径选项，只选择一条并按序完成其中全部课程；可选补充只用于填补明确缺口。
- 阶段内至少完成一个可复现产物，并把失败记录纳入复盘。
- 涉及市电、高压、射频辐射、激光、化学品或加工设备时，必须遵守本地法规并由合格人员监督。
