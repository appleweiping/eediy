---
title: "微电子学"
description: "从器件模型到晶体管级放大器和数字门，连接半导体物理、模拟和集成电路设计。"
page_type: track
track_id: "track-microelectronics"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 1f9f760308fdf8c3 -->

# 微电子学

## 方向定位

从器件模型到晶体管级放大器和数字门，连接半导体物理、模拟和集成电路设计。

## 建议先修方向

- [半导体器件](../semiconductor-devices/index.md)
- [电路分析](../circuits/index.md)

## 三份历史归档提供三种器件—电路接口

[Cornell ECE 3150](029-ece-3150.md)的[官方 OCW 页面](https://ocw.ece.cornell.edu/courses/ece-3150-microelectronics/)用 27 份 notes、12 份带解作业、带解考试和 4 个 lab，把 diode、BJT、MOS、amplifier 与 digital logic 串成最连续的纸笔主线。[MIT 6.012](030-6-012.md)的[官方 syllabus](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/pages/syllabus/)更强调器件物理与 take-home design，题目和考试很强，但没有视频，工具与工艺参考要放回 Fall 2009。[Berkeley EE 105](031-ee-105.md)的[官方历史站](https://people.eecs.berkeley.edu/~boser/courses/105/index.html)从模型做到 AM radio，公开讲义、作业和 lab 可用，Razavi 教材付费且答案不完整。多数人以 ECE 3150 贯穿全程，再按问题抽取 6.012 的 design 或 EE 105 的 radio thread；从头重复三套 small-signal analysis 收益很低。只选一门时，ECE 3150 的解答链更适合独学；已有器件基础再转 6.012，已有系统目标再借 EE 105，材料与需求能一一对应。

## 一只 MOSFET 要从载流子模型走到节点方程

[半导体器件](../semiconductor-devices/index.md)提供 junction、MOS electrostatics、carrier 与 I–V approximation，[电路分析](../circuits/index.md)提供 KCL/KVL、Thevenin/Norton、frequency response 与 transient。对同一只 MOSFET，由课程模型或 datasheet 判断 operating region，计算 \(g_m,r_o\)，画 common-source 的 DC bias 与 small-signal equivalent，再预测 load、body effect 或 capacitance 改变时 gain、swing 与 bandwidth 怎样移动。每个节点标参考方向和单位，并用 supply current、power 与极限情形做数量级检查。

这一步最容易揭示概念混淆：threshold、overdrive 与 saturation condition 含义不同；\(g_m\) 也随 bias current 改变。只会代 gain 公式却画不出等效电路，应回到 node equation；模型参数变化而电路结论完全不动，则说明器件层与电路层尚未真正连接。再用一个 BJT common-emitter 小题重复上述过程，可检验方法是否真的跨器件成立。

## 公开 lab 能提供题意，不能重建当年的台面

ECE 3150 的 4 个 lab 公开程度不一致，历史 curve tracer、oscilloscope、器件库存与课堂反馈无法从 PDF 复原；6.012 和 EE 105 也依赖各自年代的 process、text 或 campus facility。校外可在 SPICE 中比较 bias、gain、bandwidth、transient 与 corner，再选择最能区分模型的节点进入低压台面。有合规仪器时，测量写明 probe、supply current、temperature 与原始 CSV；台面条件不足时，结论明确停在 simulation。

替换 BJT 或 MOS 型号时重新核对 pinout、voltage、power、frequency、SOA 与 thermal limit，现代料号不会自动复现历史器件。fabrication、高压 breakdown 与市电不属于这些公开页面授权的家庭实验。仿真曲线也观察不到真实温升、probe loading 与供电异常，报告中应将这些量列为未测。

## I–V 拟合后的 residual 应当改动放大器

选择 diode、BJT 或 MOS 做 characterization，再用同一器件设计 single-stage 或 differential amplifier。由公开或安全实测 I-V 拟合关键参数并画 residual，随后用这组参数预测 DC bias、small-signal response、frequency response 与 large-signal swing。至少挑一个偏差显著的 operating point，判断应修改 resistor、load、device size、operating current 还是模型本身，并在修改后重新计算同一组指标。

结尾用一张修改前后对照表收束偏差最大的 operating point：左侧放拟合参数与 residual，右侧放由此改变的 bias、gain、bandwidth 或 swing。针对 resistor、load、device size、operating current 或模型本身做一次有依据的修改，再重算同一组指标，器件模型误差怎样传进放大器决策就会清楚可见。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Microelectronics](029-ece-3150.md) | Cornell University | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Microelectronic Devices and Circuits](030-6-012.md) | MIT | 可替代 | 公开材料导读 | 有公开作业或实验 |
| [Microelectronic Devices and Circuits](031-ee-105.md) | University of California, Berkeley | 可替代 | 公开材料导读 | 部分开放或受限 |
