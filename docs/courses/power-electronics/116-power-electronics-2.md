---
title: "Converter Circuits"
description: "University of Colorado Boulder 的《Converter Circuits》在电力电子入门后专门训练变换器电路；视频、练习、仿真和代码可用，但有明确前序与平台付费风险。"
page_type: course
course_id: "course-116"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: fc0281915db33cfb -->

# University of Colorado Boulder Power Electronics 2: Converter Circuits

## 课程简介

- **所属大学：** University of Colorado Boulder
- **课程编号：** Power Electronics 2
- **官方先修：** CU Boulder Converter Circuits 是 power-electronics 序列第 2 门，并假定已学过 Introduction to Power Electronics
- **本站建议背景：** 本站未另设准备条件
- **访问条件：** 需注册；可用范围以平台为准
- **资料状态：** 2026-07-30；公开材料导读

### 课程定位

University of Colorado Boulder 的 [Converter Circuits](https://www.coursera.org/learn/converter-circuits) 是功率电子专项的第二门课。官方课程页列出 4 个 module、4 次作业（graded assignments），参考进度为 2 周、每周 10 小时；默认已经学过 [Introduction to Power Electronics](https://www.coursera.org/learn/power-electronics)。如果还不能从开关状态推出 buck/boost 的平均模型，或说不清 volt-second balance 与 charge balance，先补前一门会更省时间。

[Power Electronics 专项](https://www.coursera.org/specializations/power-electronics)可用来确认课程顺序，但登录、订阅、评分反馈和证书条件由 Coursera 当期页面决定。公开简介能证明有作业，不能替代实际题面。

### 真正要学会的是开关实现与拓扑迁移

Chapter 4.1 从理想开关走向 switch realization：象限、双向功率流与同步开关。读电路时先标电压和电流允许方向，再据此选择 diode、MOSFET 或组合；原理图外形不足以判断器件象限。Chapter 4.2 接着讲 diode、MOSFET、IGBT、栅极驱动与 switching loss，并用 LTspice 分析 synchronous boost。这里最值得做的是把 conduction loss 和 switching loss 分开，逐项注明所用器件参数；只给总效率，往往掩盖了错误模型。

Chapter 5 转入 DCM。电感电流到 0 A 后，状态序列和转换比都会改变，不能把 CCM 公式机械外推。Chapter 6 再扩展到 inverter、隔离变换器、transformer、forward 与 flyback；每种磁性拓扑都应回答能量何时储存、何时传递，以及磁化电流如何复位。

### 一张 topology table 比四份零散笔记有用

4 次官方作业适合逐章检查理解；自学时再维护一张 topology table，记录端口极性、开关状态、工作象限、CCM/DCM 边界、器件应力、主要损耗、是否隔离与磁复位方式。随后分别仿真 synchronous boost 和 flyback：前者观察 dead time 与 body-diode 电流路径，后者核对磁化能量和复位假设。它们属于独立练习，课程页面没有把它们列为实验。

这门课公开材料没有教授面包板、PCB、探头选择、绝缘与热测试，因此仿真结论只适用于模型，无法直接外推到市电或高功率装置。能对陌生拓扑先列开关状态、再推导电压电流关系，并解释 DCM 边界与器件应力后，再进入 [Converter Control](https://www.coursera.org/learn/converter-control)；否则控制课的小信号模型只会变成公式套用。

## 课程资源

本页已在正文中按版本与访问条件放置核心资料链接。为避免把前序课程、历史 syllabus 或受限材料脱离上下文误列为本课资源，这里不重复生成通用资源清单。

## 资源汇总

本页没有脱离上下文重复列出资源；正文中的链接及其版本说明构成本次核对的完整汇总。
