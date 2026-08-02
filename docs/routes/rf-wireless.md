---
title: "电磁、射频、微波与无线"
description: "完成一个射频或无线设计，把 S 参数、匹配、增益与噪声、天线或通道模型接进同一份链路预算，并核对目标地区法规。"
page_type: route
route_id: "route-rf-wireless"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 167d91f19e232f3d -->

# 电磁、射频、微波与无线

## 适合人群

想从边界条件和传输线走到匹配网络、天线、接收机与完整无线链路的人

## 学完能做什么

完成一个射频或无线设计，把 S 参数、匹配、增益与噪声、天线或通道模型接进同一份链路预算，并核对目标地区法规。

## 先校准电磁模型

先在纸上处理一段有损传输线：由负载与特性阻抗算反射系数、驻波比和输入阻抗，再用无源性检查结果。若端口功率和场边界还接不上，先补 ECE 3030/6.013，不要先画天线。

## 一份频率规划，一条收发链

- 让场模型、S 参数、匹配网络、增益/噪声预算和信道使用同一频段、参考阻抗与功率单位，先写端口定义再仿真。
- 射频电路与天线阶段只选一条可执行材料路径；匿名自学优先用 6.661，校内或平台分支必须先实际打开作业、工具和实验说明。
- 无线链路把前一段器件或天线模型接进检测器和 BER 基线，并在报告中注明目标地区、频段与法规核对日期。
- 缺少 Cornell 前五讲、付费教材、Simulink 或实验条件时跳过 ECE 4880 完整复现；未注册并核实作业/实验访问时跳过 TU/e 路线。
- 家中自学默认跳过辐射测试和发射；仿真或课程页面不构成频谱使用、实验室操作或合规许可。

## 仿真路线也有真正的终点

- S 参数满足无源性/互易性等适用检查，匹配与噪声预算能从固定输入重建，网格或频率步长收敛已记录。
- 链路出口在不发射的情况下完成：天线或信道模型进入 BER/容量结果，假设、法规边界和未实测项清楚可见。

## 怎么走

### 单变量微积分准备

**为什么这样排：** 18.02SC 正式建立在 18.01 上，因此先用 18.01SC 核对微分、积分、级数和参数曲线。已有等价背景时可用闭卷题证明，不必重复所有讲次；没有通过就先补对应单元。

- [Single Variable Calculus](../courses/mathematics/001-18-01sc.md) — **必学**; MIT

**做到这里再往下：** 独立完成一组新的微积分题，并从一个带单位的场量积分得到总电荷、能量或功率；解析结果与数值积分在步长收敛范围内一致。

### 从边界条件到端口

**为什么这样排：** 先用 18.02SC、18.03SC 和 8.02X 补齐向量微积分、波动与边界条件，再由 ECE 3030 把它们变成工程场问题。若传输线、波导和能量流之间仍连不起来，就加入 6.013 的相关章节；已有等价推导和题目训练时不必重复。

- [Multivariable Calculus](../courses/mathematics/002-18-02sc.md) — **必学**; MIT
- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **必学**; MIT
- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **必学**; MIT
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **必学**; Cornell University
- [Electromagnetics and Applications](../courses/electromagnetics/108-6-013.md) — **按需补充**; MIT

**做到这里再往下：** 为一段传输线或波导同时建立解析和数值模型，不断加密网格，直到传播常数与端口功率平衡的变化小于事先写明的离散化误差。这个误差范围要能由求解器阶次、网格收敛趋势和项目规格解释，并保留完整收敛表。

### 射频电路与天线

**为什么这样排：** 这一段没有一门对所有人都成立的默认主课。能匿名使用公开材料时，选 MIT 6.661，以开放讲义和 13 套带解答习题完成接收、天线与匹配分析；需要系统级作业和实验说明时选 Cornell ECE 4880，但缺失的前 5 讲、付费教材、Simulink 与实验条件都要先补齐；只有实际注册 Coursera 并确认能打开 19 份作业和 5 个实验时，才选 TU/e 电路路线，公开课程概览本身不算可学材料。三条路线只走一条，NPTEL 天线课只用于按需补讲解。任何实体测量都必须在合规 RF 实验室由合格人员监督，课程页面和仿真均不构成辐射测试许可。

**完整路线 — 开放理论路线（MIT 6.661）（按列出顺序学习）**

1. [Receivers, Antennas, and Signals](../courses/rf-microwave-antennas/113-6-661.md) — **路线内课程**; MIT

**完整路线 — 射频系统与实验路线（Cornell ECE 4880）（按列出顺序学习）**

1. [Radio Frequency Systems](../courses/rf-microwave-antennas/110-ece-4880.md) — **路线内课程**; Cornell University

**完整路线 — Coursera 电路路线（TU/e；需注册访问）（按列出顺序学习）**

1. [RF and Millimeter-Wave Circuit Design](../courses/rf-microwave-antennas/111-rf-and-millimeter-wave-circuit-design.md) — **路线内课程**; Eindhoven University of Technology

- [Analysis and Design Principles of Microwave Antennas](../courses/rf-microwave-antennas/112-108105114.md) — **按需补充**; IIT Kharagpur / NPTEL

**做到这里再往下：** 完成匹配网络、射频前端或天线中的一个设计。S11 目标必须从链路预算、允许失配损耗和带宽要求推出；−10 dB 只有在其失配损耗确实可接受时才能作为起点，不能替代系统论证。增益、噪声和稳定性预算也要同时闭合。

### 让预算经受真实信道

**为什么这样排：** 用 6.02 建立同步、编码、检测与误码率基线，它不会暗中要求本路线尚未保证的 6.011 前序。把刚完成的 S 参数、增益与噪声预算或天线模型直接放到链路前端，再按访问条件从 EE 359 无线系统与 NPTEL 长视频讲解中选一门加深。6.450/6.452 属于另一个以 6.011 为前置的研究生序列，不计入本路线。

- [Introduction to EECS II: Digital Communication Systems](../courses/communications/099-6-02.md) — **必学**; MIT
- [Wireless Communications](../courses/communications/105-ee-359.md) — **选 1 门**; Stanford University
- [Principles of Digital Communications](../courses/communications/106-108101113.md) — **选 1 门**; IIT Bombay / NPTEL

**做到这里再往下：** 完成可复算的链路预算和含衰落、干扰的信道仿真，画出接收灵敏度与 BER 或吞吐量的关系。频率、带宽、发射功率和占空比逐项对照目标地区当前法规；没有合规实验条件时只做仿真，不发射。
