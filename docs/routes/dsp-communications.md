---
title: "信号处理、通信与信息论"
description: "实现一个含同步、调制解调、信道编码和误码率测量的可复现实验链路。"
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 13b62bae6618e55e -->

# 信号处理、通信与信息论

[English](../en/routes/dsp-communications.md) · [← 学习路线](index.md)

## 适合人群

希望从傅里叶分析走到数字通信、无线和纠错码的学习者

## 最终验收

实现一个含同步、调制解调、信道编码和误码率测量的可复现实验链路。

## 阶段安排

### 信号与概率

**选课要求：** 完成全部 4 门必修；其余 1 门仅在需要补缺时选学。

- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **必修**; MIT; 主线; S
- [Probabilistic Systems Analysis and Applied Probability](../courses/probability-statistics/007-6-041sc.md) — **必修**; MIT; 主线; S
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **必修**; MIT; 主线; S
- [The Fourier Transform and Its Applications](../courses/signals-systems/097-ee-261.md) — **必修**; Stanford University; 主线; S
- [Introduction to Communication, Control, and Signal Processing](../courses/signals-systems/098-6-011.md) — **可选补充**; MIT; 补充; B

**阶段退出条件：** 在同一笔记本中解析并数值验证一个 LTI 系统的时域、频域和随机响应；Parseval 能量残差低于 1%，蒙特卡洛均值落入解析 95% 置信区间。

### DSP 实现

**选课要求：** 完成全部 1 门必修，并从 5 门选修候选中选择 1 门。

- [Digital Signal Processing](../courses/dsp/088-res-6-008.md) — **必修**; MIT; 主线; S
- [Discrete-Time Signal Processing](../courses/dsp/089-6-341.md) — **选修候选**; MIT; 替代; A
- [Digital Signal Processing 1: Basic Concepts and Algorithms](../courses/dsp/090-dsp-1.md) — **选修候选**; EPFL; 替代; A
- [Digital Signal Processing 2: Filtering](../courses/dsp/091-dsp-2.md) — **选修候选**; EPFL; 替代; A
- [Digital Signal Processing 3: Analog versus Digital](../courses/dsp/092-dsp-3.md) — **选修候选**; EPFL; 替代; A
- [Digital Signal Processing 4: Applications](../courses/dsp/093-dsp-4.md) — **选修候选**; EPFL; 替代; A

**阶段退出条件：** 实现一个滤波或频谱处理流水线，用合成与真实样本验证通带、阻带和混叠指标；同时报告浮点/定点信噪比、运行时间与内存占用的可重复对照。

### 通信与编码

**选课要求：** 完成全部 2 门必修，并从 2 门选修候选中选择 1 门。其余 1 门为可选补充，不计入本阶段选修数。

- [Introduction to EECS II: Digital Communication Systems](../courses/communications/099-6-02.md) — **必修**; MIT; 主线; S
- [Principles of Digital Communications I](../courses/communications/100-6-450.md) — **选修候选**; MIT; 主线; S
- [Principles of Digital Communication II](../courses/communications/101-6-451.md) — **可选补充**; MIT; 主线; S
- [Information Theory](../courses/information-theory-coding/102-ee-276.md) — **必修**; Stanford University; 主线; A
- [Wireless Communications](../courses/communications/105-ee-359.md) — **选修候选**; Stanford University; 替代; A

**阶段退出条件：** 搭建含同步、调制、信道与纠错的端到端链路，固定随机种子绘制至少 6 个 Eb/N0 点的 BER 曲线；给出理论或基线对照、置信区间及同步失效率。

## 执行规则

- 按每个阶段的选课要求完成全部必修与指定数量的选修；若提供完整路径选项，只选择一条并按序完成其中全部课程；可选补充只用于填补明确缺口。
- 阶段内至少完成一个可复现产物，并把失败记录纳入复盘。
- 涉及市电、高压、射频辐射、激光、化学品或加工设备时，必须遵守本地法规并由合格人员监督。
