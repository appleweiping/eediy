---
title: "电子工程导论"
description: "用跨越电路、信号、计算和机电系统的综合课程建立全景认知，并尽早完成小型系统。"
page_type: track
track_id: "track-ee-introduction"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 2fe551f0b877bd77 -->

# 电子工程导论

## 方向定位

用跨越电路、信号、计算和机电系统的综合课程建立全景认知，并尽早完成小型系统。

## 建议先修方向

- [工程数学](../mathematics/index.md)
- [编程与工程计算](../programming-tools/index.md)

## 6.01SC 从状态和程序进入，6.007 从能量和场进入

[MIT 6.01SC](019-6-01sc.md)的[官方档案](https://ocw.mit.edu/courses/6-01sc-introduction-to-electrical-engineering-and-computer-science-i-spring-2011)把 Python、状态机、信号、电路、概率化机器人和软件组织放在一套材料里，适合尚未选方向、愿意用程序连接抽象层的人。机器人平台和部分软件已有年代，不宜原样采购；值得学习的是模型怎样进入实现和测试。

[MIT 6.007](020-6-007.md)的[官方课程页](https://ocw.mit.edu/courses/6-007-electromagnetic-energy-from-motors-to-lasers-spring-2011)用电磁能量、执行器、传感、传输和光电系统建立另一幅 EE 图景。它会较早暴露 motor、power、RF、device 与 photonics 中的 field、geometry 和 energy 问题。公开视频主要是实验演示，题目没有解答，也没有公开考试，不能沿用 6.01SC 的完成标准。两门通常择一为入口，再从另一门抽取与小作品有关的一章。

## 两个小问题足以判断哪一种入口更适合

起点只要求[工程数学](../mathematics/index.md)中的基本微积分、向量和单位可用，也能在[编程工具](../programming-tools/index.md)中写一个带测试的小程序。用 6.01SC 做 state machine→sensor model→controller 的短闭环，再用 6.007 对 motor、transmission 或 optical sensing 画能量流并做数量级估计。两项工作各自留下代码或推导、输入条件和一个与预测不符的现象。

程序能跑却解释不了 sensor、actuator 和 feedback 的关系时，6.01SC 的系统路线更合适；会列电路方程却无法从 energy、field 和 geometry 解释器件时，6.007 更有价值。数学和编程都不稳时，两门都无法充当捷径，导论也不能在短时间内替代物理、电路与工具基础。

随后只做一个含两个子系统的安全小作品，例如仿真移动机器人、低压光传感器、software communication link 或完全仿真的 motor。system boundary、input/output、state 或 energy flow、关键假设与三到五个端到端测试比功能数量更重要。没有实体器材可以全部仿真，但数据来源、仿真边界和未验证 hardware behavior 要写清。

## 第一处无法解释的接口，决定下一门课

KCL/KVL、初值和器件工作点反复出错时，转[电路分析](../circuits/index.md)；convolution、sampling、noise 和 filter 主导时，转[信号与系统](../signals-systems/index.md)；geometry、boundary condition 和 energy propagation 主导时，转[电磁场](../electromagnetics/index.md)；build、test 和数据结构拖住作品时，则回编程工具。

方向选择应引用作品中一处具体接口：模型缺了什么，哪项预测方向相反，或哪一种单位无法统一。一个动画、传感器读数或顺利运行的视频不能单独回答这些问题。导论最有价值的结果并非“看遍 EE”，而是能用同一小系统说明接下来补什么、为什么，以及目前哪些硬件行为还没有被验证。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Introduction to Electrical Engineering and Computer Science I](019-6-01sc.md) | MIT | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Electromagnetic Energy: From Motors to Lasers](020-6-007.md) | MIT | 可替代 | 公开材料导读 | 部分开放或受限 |
