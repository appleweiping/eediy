---
title: "通信系统"
description: "调制、检测、信道、同步、链路预算与无线系统，从波形到端到端可靠通信。"
page_type: track
track_id: "track-communications"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: b8cf5d5fa4de8bc1 -->

# 通信系统

## 方向定位

调制、检测、信道、同步、链路预算与无线系统，从波形到端到端可靠通信。

## 建议先修方向

- [信号与系统](../signals-systems/index.md)
- [概率、统计与随机过程](../probability-statistics/index.md)

## 6.02 把 bit、waveform、channel 和 packet 连成一条链

[MIT 6.02](099-6-02.md)的[官方 2012 档案](https://ocw.mit.edu/courses/6-02-introduction-to-eecs-ii-digital-communication-systems-fall-2012)适合第一次看通信系统：compression/coding、baseband signal、noisy channel 和 packet/network 被放在端到端因果链里。Audiocom、旧 Python 接口和 speaker 路径已有年代，可以从确定的 WAV/array 输入重建核心任务，再决定是否接音频硬件。课程价值在于一项 bit error 能追到信源、编码、同步、判决或网络层，旧软件能否启动只是次要问题。

从[信号与系统](../signals-systems/index.md)带入 convolution、Fourier、sampling、filter 和 complex baseband，从[概率与统计](../probability-statistics/index.md)带入 conditional probability、Gaussian variable、random process 与 hypothesis test。对 BPSK over AWGN，手推 matched-filter statistic 与 decision threshold，并把 symbol energy、noise PSD、sample rate 和 BER 的单位接起来。这个接口还说不清时，后续 coding 或 wireless 只会堆出更多符号。

最好让一小段确定比特同时经过连续时间表达、离散采样和最终判决，逐处写清归一化。这样可以看见某个系数究竟来自脉冲能量、采样间隔还是噪声定义，而不会靠套公式碰巧得到正确曲线。

## 6.450 与 6.451 是检测和编码的两级深入

[MIT 6.450](100-6-450.md)从 waveform、detection、modulation 和 AWGN 建立数字通信核心；[官方档案](https://ocw.mit.edu/courses/6-450-principles-of-digital-communications-i-fall-2006)保留题目和考试，但 homework solutions 未公开，材料残缺的 2009 版也不能替代 2006 主线。只有 distance、finite-length code 与 iterative decoding 成为项目问题时，才继续 [6.451](101-6-451.md)，无需按编号自动连修。

一条未知 phase 的 received-sample 序列很适合检验理解：同步误差怎样进入统计量，decoder 又不能补救哪些失真。除了 BER，还要给 error count、confidence interval 和停止条件；编码增益与带宽开销、译码计算和 latency 放在同一张表里。新增 Monte Carlo notebook 应标为独立练习，不能冒充原课 lab 或校内评分。

若解析式和仿真在高信噪比（SNR）处偏离，优先检查样本数量与置信区间；若在全部区间呈固定偏移，再核对单边或双边噪声谱密度（PSD）以及每比特、每符号能量的换算。

## 无线课程替换的是 channel 假设

[Stanford EE 359](105-ee-359.md)适合 fading、diversity 与 MIMO，[NPTEL Principles of Digital Communications](106-108101113.md)提供 65 讲的长视频节奏；二者按讲解方式和无线深度择一。[MIT 6.452](104-6-452.md)定位为特定 wireless topic，放在第一门通信课之后。EE 359 的 reader、作业、项目和公开考试题可用，视频留在 Canvas，一份解答进入 Stanford SAML，部分协议背景停在 2020 年；6.452 有题目、项目和 readings，却没有连续视频或讲义；NPTEL 认证考试限时付费，也没有 lab/code 闭环。

无线仿真注明 channel model、coherence、CSI、synchronization、coding、seed 与 SNR 定义。理想 AWGN 曲线不能外推成 RF link，flat fading 结果也不能自动说明 frequency-selective channel。每次只替换一个假设，才看得出 diversity、equalization 或 coding 分别修正了什么。

接收端拥有完美信道状态和只能估计信道时，应分别列结果；否则“多天线更好”可能只是把额外先验信息藏进算法输入。

## 一条 baseband link 应能追到第一个 error event

选定 message bits 与 frame，依次实现 source/channel code、pulse shaping、channel、matched filter、timing/phase impairment、detector 和 decoder。在 AWGN 下让 simulated BER 对齐解析式或已知 bound，再加入一种 fading、frequency offset 或 synchronization error。错误样本包含 constellation、decision statistic、decoded bits、frame 与 symbol position；一条平滑曲线无法说明哪个模块最早出错。

同一配置报告 throughput、latency、computation 与 uncertainty，代码、seed、raw arrays 和一条端到端命令足以重跑。改变 SNR 或 offset 前给出方向判断，再查看实际错误落在同步、检测还是译码。若迁移旧代码，调制和判决规则与库/接口升级分开修改，避免把环境差异误当算法改进。

第一个错误事件还应能回溯到发射比特和信道样本；只有汇总百分比时，译码器前后的错误传播会被平均值遮住。

## Coding、wireless 和 SDR 的分界在硬件进入模型的位置

distance spectrum、decoder complexity 或 finite-length behavior 主导时进入 6.451 的 coding；fading、CSI、diversity 或 MIMO 主导时走 EE 359/NPTEL；只有 oscillator、ADC/DAC、dynamic range、synchronization 和真实 RF front end 成为核心时，才进入 SDR。三条分支可沿用相同 baseband link，却分别固定 channel、code 或理想硬件中的不同部分。

真实 SDR 实验只在许可频段、dummy load 或屏蔽有线路径中进行，并重新核对当地法规与硬件功率。若项目还说不清错误属于 source、synchronization、detection、decoding 还是 RF，缩短 frame 和处理级数比同时加入新编码、衰落与硬件更有效。

最终选课理由应指出被替换的具体假设，以及现有基线为何无法回答它；这比笼统地追求更低误码率（BER）更能区分 coding、wireless 与 SDR 三条路线。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Introduction to EECS II: Digital Communication Systems](099-6-02.md) | MIT | 主课 | 公开材料导读 | 部分开放或受限 |
| [Principles of Digital Communications I](100-6-450.md) | MIT | 主课 | 公开材料导读 | 部分开放或受限 |
| [Principles of Digital Communication II](101-6-451.md) | MIT | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Wireless Communications](105-ee-359.md) | Stanford University | 可替代 | 公开材料导读 | 有公开作业或实验 |
| [Principles of Digital Communications](106-108101113.md) | IIT Bombay / NPTEL | 可替代 | 公开材料导读 | 部分开放或受限 |
| [Principles of Wireless Communications](104-6-452.md) | MIT | 补充材料 | 公开材料导读 | 部分开放或受限 |
