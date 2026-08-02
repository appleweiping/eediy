---
title: "数字信号处理"
description: "离散变换、滤波器、谱估计、多率系统与实现，以代码、数据和误差指标闭环。"
page_type: track
track_id: "track-dsp"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 77f3112bcd49a2cf -->

# 数字信号处理

## 方向定位

离散变换、滤波器、谱估计、多率系统与实现，以代码、数据和误差指标闭环。

## 建议先修方向

- [信号与系统](../signals-systems/index.md)
- [概率、统计与随机过程](../probability-statistics/index.md)
- [编程与工程计算](../programming-tools/index.md)

## RES.6-008 与 6.341 是两种历史型理论主线

[MIT RES.6-008](088-res-6-008.md)的[官方档案](https://ocw.mit.edu/courses/res-6-008-digital-signal-processing-spring-2011)整理了 20 课视频/讲义，以及 Lecture 2–20 的 19 份 solution packet，适合系统学习离散表示、z-transform、DFT、filter 和算法实现。录像源自 1987 年，核心教材更早；数学与算法仍有效，执行环境缺少现代 coding baseline。[MIT 6.341](089-6-341.md)用 11 份题、2 个 project 和 3 套考试增加研究生推导、设计与报告，适合已经具备基础 DSP 的学习者。

6.341 的 Athena/MATLAB project 需要迁移，但原题要求的 phase comparison、operation count 和报告结构值得保留。新 Python 或 Julia 实现应与旧题面分开注明，不能把更新库接口写成原课成果。第一次学习通常以 RES.6-008 为理论主线；已有离散系统基础且愿意完成长 project 时，再直接进入 6.341。

## EPFL 四门短课按问题选，不按编号重修

[DSP 1](090-dsp-1.md)、[DSP 2](091-dsp-2.md)、[DSP 3](092-dsp-3.md)分别覆盖基本表示、滤波与模拟/数字接口；[DSP 4](093-dsp-4.md)进入应用。当前 [DSP 4 官方页](https://www.coursera.org/learn/dsp4)列出 3 个模块、2 次计分 assignment 和 4 个未计分 lab；页面所列计分作业数量为 2。旧公开 repository 与当前平台 labs 并非逐项对应，旧 NumEx 也不能当成当前 graded work；平台完整访问可能收费。

[Illinois ECE 310](094-ece-310.md)可作为文字型课程地图，[ECE 311](095-ece-311.md)只公开实验范围：截至 2026-07-30，ECE 310 的 homework/exam 文件匿名请求返回 HTTP 401，ECE 311 的 Lab 1–7/final ZIP 也受限，walkthrough 进入 Illinois SSO。[Berkeley EE 123](096-ee-123.md)把 DSP 推到无线项目，但已确认可直接下载的机器包只覆盖 HW11。课程名出现在网页上，并未自动带来完整作业、starter 和反馈。

因此这些页面更适合判断主题覆盖和所需工具，不能用自拟 notebook 补齐受限文件后声称完成原课实验。公开范围变化时，也应以当次实际取得的材料为准。

## 一条信号要同时解释表示、滤波和数值误差

[信号与系统](../signals-systems/index.md)提供 convolution、LTI、sampling、Fourier/z-transform 与 pole-zero，[概率与统计](../probability-statistics/index.md)提供 random process、expectation、correlation 和 noise，[编程与工程工具](../programming-tools/index.md)负责可复现环境、测试与原始数据。选择一段有来源的 audio、sensor 或 baseband data，写清 sample rate、record length、unit 和 raw checksum。

手算一个短 convolution 与 DFT，说明 Hz、rad/sample、FFT normalization；再分别改变 sample rate、window 和 record length，预测 aliasing、resolution 与 leakage。随后以明确的 passband、stopband、transition width、delay、complexity 和允许失真比较 FIR/IIR，并在一个可手算序列上对照 SciPy reference 与自写实现。padding、dtype、filter state、coefficient quantization 或 unstable pole 造成的异常，应能定位到具体样本和处理级，而非只剩一张“更平滑”的图。

时域、频域与极点—零点图应解释同一个现象。例如瞬态振铃需要同时对应冲激响应长度、频域过渡带和极点位置；如果三种表示给出互相矛盾的故事，优先核对归一化和边界处理。指标表还应包含 delay 与运算量，避免滤波效果只按视觉排序。

## 误差出现在哪一层，就往哪条支路走

window、PSD variance 和有限记录主导时进入 spectral estimation/statistical DSP；imaging、alias rejection 与不同 rate 的计算量主导时进入 multirate；fixed-point、streaming buffer 和实时 deadline 主导时走 DSP implementation；channel、synchronization 与 RF hardware 成为核心时，进入[通信系统](../communications/index.md)或 SDR。分支比较沿用相同 data 与 baseline，只改变新问题层。

EE 123 的 SDR/业余无线电任务需要硬件、当地频率法规与执照；未经许可不做 RF 发射。没有相应条件时，可以完成 baseband array 或录制数据分析，并清楚说明 hardware behavior 尚未验证。DSP 真正成为工程工具的标志，是能从一个错误样本追到表示、算法、数值实现或硬件接口中的具体位置，视频序列长度与此无关。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Digital Signal Processing](088-res-6-008.md) | MIT | 主课 | 公开材料导读 | 部分开放或受限 |
| [Discrete-Time Signal Processing](089-6-341.md) | MIT | 可替代 | 公开材料导读 | 有公开作业或实验 |
| [Digital Signal Processing 1: Basic Concepts and Algorithms](090-dsp-1.md) | EPFL | 可替代 | 公开材料导读 | 部分开放或受限 |
| [Digital Signal Processing 2: Filtering](091-dsp-2.md) | EPFL | 可替代 | 公开材料导读 | 部分开放或受限 |
| [Digital Signal Processing 3: Analog versus Digital](092-dsp-3.md) | EPFL | 可替代 | 公开材料导读 | 部分开放或受限 |
| [Digital Signal Processing 4: Applications](093-dsp-4.md) | EPFL | 可替代 | 公开材料导读 | 有公开作业或实验 |
| [Digital Signal Processing](096-ee-123.md) | University of California, Berkeley | 可替代 | 公开材料导读 | 有公开作业或实验 |
| [Digital Signal Processing I](094-ece-310.md) | University of Illinois Urbana-Champaign | 可替代 | 资料索引；不是完整课程替代 | 未核到公开练习 |
| [Digital Signal Processing Laboratory](095-ece-311.md) | University of Illinois Urbana-Champaign | 可替代 | 资料索引；不是完整课程替代 | 未核到公开练习 |
