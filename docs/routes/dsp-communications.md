---
title: "信号处理、通信与信息论"
description: "实现一条可重跑的通信链路，包含同步、调制解调、信道编码和误码率测量，并能说明理论曲线与仿真偏差来自哪里。"
page_type: route
route_id: "route-dsp-communications"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: a1c43aa134ca11de -->

# 信号处理、通信与信息论

## 适合人群

想把傅里叶、随机过程与 DSP 真正接到数字通信、无线信道和纠错码上的学习者

## 学完能做什么

实现一条可重跑的通信链路，包含同步、调制解调、信道编码和误码率测量，并能说明理论曲线与仿真偏差来自哪里。

## 先冻结一条信号链

先用一个脚本生成正弦加白噪声，画时域、频谱并估计功率。若采样率、Parseval、期望与方差还不能同时解释，先停在 LTI 与概率；不要直接从调制名称开始背。

## 解析、浮点、定点和链路共用样本

- 在同一组带种子的样本上完成解析 LTI、浮点 DSP 和定点实现，先写通带、阻带、混叠与量化噪声的允许范围。
- 通信链路只选 6.450 数字通信或 EE 359 无线信道之一作为主分支；发送端或接收端继续使用前面的滤波模块。
- BER 扫描覆盖失效区、瀑布区与目标区，每点保留比特数和置信区间，并把同步失败与译码错误分开统计。
- 6.003 与 EE 261 的重复 Fourier 单元只留一套主练习；EPFL 模块打不开时跳过，不把产品介绍页当 notebook。

## 先把射频硬件留在边界外

- 没有先完成检测器与误码曲线时跳过 6.451；不同时做数字通信和无线两条完整路线。

## 在自己选定的层级收口

- 一条命令能从固定配置重建波形、频谱、浮点/定点差异和 BER 图，理论偏差可追到有限样本、同步、量化或信道假设。
- 只做到 DSP 时可在第二阶段停止并明确边界；完成通信出口时，还需链路端到端复现与置信区间，不需要实体发射。

## 怎么走

### 单变量微积分

**为什么这样排：** 6.041SC 的正式准备从 18.01 开始。先用 18.01SC 的极限、微分、积分和级数题做闭卷诊断；只有这些运算能够稳定支撑概率密度归一化、期望积分和级数收敛时，才进入下一段。

- [Single Variable Calculus](../courses/mathematics/001-18-01sc.md) — **必学**; MIT

**做到这里再往下：** 独立完成一组改换参数的微积分题，并用解析积分与数值积分计算同一个归一化密度的概率和期望；数值误差随步长收敛，单位与定义域一致。

### 多变量、微分方程与向量空间

**为什么这样排：** 18.02SC 补齐 6.041SC 正式列出的多重积分背景，18.03SC 负责线性常微分方程与特征结构，18.06SC 负责向量空间和投影。三门课都围绕同一个二阶 LTI 模型工作，不各做一套互不相干的例题。

- [Multivariable Calculus](../courses/mathematics/002-18-02sc.md) — **必学**; MIT
- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **必学**; MIT
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **必学**; MIT

**做到这里再往下：** 从微分方程得到状态模型、特征值与解析响应，再用矩阵指数和数值积分复算。改变基底后，输入输出响应保持不变；残差随时间步长收敛。

### 把概率接到信号系统

**为什么这样排：** 6.041SC 处理随机变量与随机过程，6.003 连接时域、频域和系统表示，EE 261 只深入项目需要的 Fourier 内容。继续使用上一段的 LTI 模型，把确定性输入改为带固定种子的随机过程；6.003 与 EE 261 重叠的 Fourier 单元只保留一套主练习。

- [Probabilistic Systems Analysis and Applied Probability](../courses/probability-statistics/007-6-041sc.md) — **必学**; MIT
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **必学**; MIT
- [The Fourier Transform and Its Applications](../courses/signals-systems/097-ee-261.md) — **必学**; Stanford University

**做到这里再往下：** 在同一个 notebook 中推导并数值验证系统的时域、频域和随机响应。保存随机种子与样本数，用预先选定的置信水平核对蒙特卡洛均值，并使 Parseval 残差低于由采样窗口和离散化给出的误差。

### 把 DSP 算法变成实现

**为什么这样排：** 以 RES.6-008 为主要 DSP 课程，继续使用前一段的随机 LTI 数据、采样定义和 golden output。计入完成要求的加深课从 EPFL DSP 1–4 中按算法、滤波、采样边界或应用短板选一门。6.341 明确建立在 6.011 上，只在后来走完 6.011→6.450 数字通信分支时作为额外理论材料，不计作本阶段选修。EPFL 模块打不开就只完成公开的 RES.6-008，不能把产品介绍页当成实验。

- [Digital Signal Processing](../courses/dsp/088-res-6-008.md) — **必学**; MIT
- [Discrete-Time Signal Processing](../courses/dsp/089-6-341.md) — **按需补充**; MIT
- [Digital Signal Processing 1: Basic Concepts and Algorithms](../courses/dsp/090-dsp-1.md) — **选 1 门**; EPFL
- [Digital Signal Processing 2: Filtering](../courses/dsp/091-dsp-2.md) — **选 1 门**; EPFL
- [Digital Signal Processing 3: Analog versus Digital](../courses/dsp/092-dsp-3.md) — **选 1 门**; EPFL
- [Digital Signal Processing 4: Applications](../courses/dsp/093-dsp-4.md) — **选 1 门**; EPFL

**做到这里再往下：** 实现滤波或频谱处理流水线，用合成样本和一组真实数据检查通带、阻带与混叠。浮点和定点版本使用同一输入，报告信噪比、运行时间与内存占用，并提供一条命令重现比较。

### 从比特到有噪链路

**为什么这样排：** 6.02 建立同步、编码和链路直觉，EE 276 给出信息论边界；前一段的滤波或定点模块继续充当发送端或接收端前端。随后二选一：数字通信必须把 6.011→6.450 作为完整有序路径，无线信道则选 EE 359。6.451 只有在完成数字通信路径并能解释检测器与误码曲线后才作为未计数加深；这个顺序是知识依赖，不是证书要求。

- [Introduction to EECS II: Digital Communication Systems](../courses/communications/099-6-02.md) — **必学**; MIT

- [Information Theory](../courses/information-theory-coding/102-ee-276.md) — **必学**; Stanford University

**完整路线 — 数字通信完整前序（6.011→6.450）（按列出顺序学习）**

1. [Introduction to Communication, Control, and Signal Processing](../courses/signals-systems/098-6-011.md) — **路线内课程**; MIT
2. [Principles of Digital Communications I](../courses/communications/100-6-450.md) — **路线内课程**; MIT

**这条分支做到哪里：** 先用 6.011 完成估计或检测基线，再进入 6.450 的调制、检测与误码率；两门使用同一个随机 LTI 模型和测试数据。6.451 只作为完成该路径后的未计数加深。

**完整路线 — 无线信道路线（EE 359）（按列出顺序学习）**

1. [Wireless Communications](../courses/communications/105-ee-359.md) — **路线内课程**; Stanford University

**这条分支做到哪里：** 用 EE 359 的衰落与无线信道模型扩展 6.02 链路，保留前一阶段的滤波器、固定种子和误码率统计；不同时重复数字通信路径。

- [Principles of Digital Communication II](../courses/communications/101-6-451.md) — **按需补充**; MIT

**做到这里再往下：** 搭建包含同步、调制、信道和纠错的端到端链路。固定随机种子，扫描同时覆盖低 SNR 失效区、瀑布区和目标工作区的 Eb/N0，并在转折附近加密取点。BER 图要同时给理论或基线、每点样本数和置信区间，另外单独统计同步失败率。
