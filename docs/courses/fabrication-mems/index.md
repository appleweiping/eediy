---
title: "微纳工艺与 MEMS"
description: "沉积、光刻、刻蚀、工艺集成和微机电设计；无洁净室时只做工艺计划、仿真和案例分析。"
page_type: track
track_id: "track-fabrication-mems"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: f41efc617c1e8045 -->

# 微纳工艺与 MEMS

## 方向定位

沉积、光刻、刻蚀、工艺集成和微机电设计；无洁净室时只做工艺计划、仿真和案例分析。

## 建议先修方向

- [半导体器件](../semiconductor-devices/index.md)
- [物理基础](../physics/index.md)

## 6.152J 讲工艺骨架，6.777J 才进入 MEMS 设计

[MIT 6.152J](126-6-152j.md)是工艺骨架，按氧化、扩散、注入、沉积、光刻、刻蚀与集成约束推进。它的[官方作业页](https://ocw.mit.edu/courses/6-152j-micro-nano-processing-technology-fall-2005/pages/assignments/)只列 Problem Set 1–8，且八套都有解；[考试页](https://ocw.mit.edu/courses/6-152j-micro-nano-processing-technology-fall-2005/pages/exams/)另有一份公开 take-home exam，以及来自不同学期的 quiz 题或答案。这组材料只支持 PS1–8，PS9–10 并不存在；另一门课的 design problem 也不属于这里。[MIT 6.777J](129-6-777j.md)才把力学、电学与制造约束放进 MEMS device design：它的[课程大纲](https://ocw.mit.edu/courses/6-777j-design-and-fabrication-of-microelectromechanical-devices-spring-2007/pages/syllabus/)明确要求七次 homework、take-home design problem 和团队 final project，但[公开作业页](https://ocw.mit.edu/courses/6-777j-design-and-fabrication-of-microelectromechanical-devices-spring-2007/pages/assignments/)只有 PS1–7，PS5 无解，take-home design problem 也未公开。[EPFL memsX](127-memsx.md)的洁净室视频适合观察 CVD、PVD、光刻、干湿法刻蚀和计量，却无法代替设备操作训练；[NPTEL 工艺概览](128-108104865.md)适合快速得到 12 周全景。若目标只是读懂 IC cross-section，6.152J 加 memsX 或 NPTEL 选段已经够用；确实要设计 membrane、cantilever 或 resonator 时，再走到 6.777J。

## 连续截面是这组课程真正的学习单位

基础来自[半导体器件](../semiconductor-devices/index.md)中的结、MOS capacitor/MOSFET、掺杂与载流子行为，以及[物理基础](../physics/index.md)里的扩散、热过程、力学和尺度分析。选 planar diode 或悬臂梁，从起始 wafer 连续画出 3 到 5 步截面；每一步注明增加、移除或掺杂了什么材料，温度范围、关键尺寸、界面和可测量量是什么，以及它怎样改变最终电学或机械指标。dose、concentration、film thickness、sheet resistance 与 stress 的单位若分不清，就回到量纲和器件；若只会画漂亮的最终结构，却无法说明 release、mask alignment 或 thermal budget 怎样到达那里，也不宜马上进入 6.777J。制造学习的核心是顺序与兼容性，设备名称只是索引。

## 仿真和版图工具停在洁净室门外

KLayout、gdsfactory 与 Python/Jupyter 可以生成 mask、逐步截面、参数扫描和容差分析，适合在纸面上发现材料顺序冲突、未释放结构或不可测步骤。公开课程并未提供设施准入、设备资格、批准配方、正式 wafer traveler、污染规则、原始计量数据和废弃物流程；memsX 的高级内容还可能收费，NPTEL 也没有实体实验闭环。真空、高温、等离子体、离子注入、特种气体、光刻化学品和湿法腐蚀只能在受控设施中由受训人员操作，不能从视频反推家庭 recipe。模型中的每个数值都注明来自课程材料、当前一手资料或教学假设，非授权 slide 镜像也不适合用来填补缺页。

## 一条虚拟流程只回答一个器件问题

为 MEMS membrane、cantilever、interdigitated capacitor，或简化 CMOS/diode 选一个明确指标，随后给出 mask list、连续 cross-section、热预算、污染兼容性、关键尺寸以及 2 处合适的测量位置。对 lithography bias、etch bias、film stress、oxide thickness 或 implant dose 至少做一项 sensitivity 或 Monte Carlo 分析，把变化连到 resonance、capacitance、sheet resistance 或 threshold。把一条可接受流程和一条被拒流程并排，标出材料顺序、release、热预算或 metrology 第一次使二者分开的步骤。该步骤若改变 junction、threshold 或 yield，就把同一组截面交给 process integration；若改变结构 mode、transduction 或 control interface，就交给 MEMS design。没有机构设施时，两种结论都只是声明假设下的内部一致性检查，不是上机经历。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Micro/Nano Processing Technology](126-6-152j.md) | MIT | 主课 | 公开材料导读 | 部分开放或受限 |
| [Design and Fabrication of Microelectromechanical Devices](129-6-777j.md) | MIT | 主课 | 公开材料导读 | 部分开放或受限 |
| [Micro and Nanofabrication (MEMS)](127-memsx.md) | EPFL | 可替代 | 公开材料导读 | 部分开放或受限 |
| [Basic Overview of Semiconductor Device Processing and IC Fabrication](128-108104865.md) | IIT Kanpur / NPTEL | 补充材料 | 公开材料导读 | 部分开放或受限 |
