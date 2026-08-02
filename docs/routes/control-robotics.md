---
title: "控制、机器人与自主系统"
description: "先在仿真中闭合感知—规划—控制链，再视安全条件转到低能量实体平台，并用稳定性、轨迹误差和失败案例说明系统表现。"
page_type: route
route_id: "route-control-robotics"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: e8f2e65ee77210f6 -->

# 控制、机器人与自主系统

## 适合人群

想把动力学、状态估计、规划与反馈控制接成一套机器人系统的人

## 学完能做什么

先在仿真中闭合感知—规划—控制链，再视安全条件转到低能量实体平台，并用稳定性、轨迹误差和失败案例说明系统表现。

## 先把 plant 说清楚

选一个能写出运动方程的对象，例如倒立摆或二轮车，先给出状态、输入、输出、单位和工作点。若线性化后还不会判断可控性或开环稳定性，先不要打开机器人课程。

从同一 plant 的物理方程、参数识别和留出轨迹开始；控制器只能使用训练数据未包含的轨迹检验。

## 先闭合控制环，再进入机器人

- 反馈阶段在写控制律前给出稳定性论证、执行器饱和和噪声模型；连续控制选 6.241J，随机序贯决策才选 6.231。
- 机器人阶段在 MIT 6.4210→6.832 与 Modern Robotics 1→6 之间选一条完整路径，沿用同一个 plant、controller 与失败注入。

## 把平台复杂度推迟到模型撑得住

- 已有微分方程、线性代数和力学能力时，直接从参数识别任务开始；不要为统一记号重复修多门控制概论。
- 只做控制系统时跳过机器人阶段；没有安全硬件与停机条件时跳过实体迁移，仿真完成仍然有效。

## 用失败统计验收，不用 demo 光泽验收

- 仿真出口要求留出轨迹误差、稳定性边界、饱和与传感噪声结果可重跑，并保留至少一个控制器失败案例。
- 机器人出口再要求所选完整路径的规划—控制闭环通过扰动与恢复场景；实体硬件只是有条件的扩展，不是默认验收。

!!! warning "开始前请确认这些课程的材料限制"
    - [Feedback Systems: An Introduction for Scientists and Engineers](../courses/control-systems/073-cds-101-cds-110.md)：入口是作者维护的第二版教材配套站，提供开放文本、实例、习题和更新后的 Python 图源，但不是当前完整课程运行页；教师习题手册仍受限。 最近核对：2026-07-29。

## 怎么走

### 从物理对象到状态模型

**为什么这样排：** 始终使用同一个机械或机电对象：18.03SC 写运动方程，18.06SC 处理线性代数，8.01SC 负责从受力与能量假设建模，EE 263 再把它改写成状态空间、最小二乘和动态系统问题。这样每个数学工具都有物理落点，也不会出现四门课分别做完却互相接不上。

- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **必学**; MIT
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **必学**; MIT
- [Classical Mechanics](../courses/physics/010-8-01sc.md) — **必学**; MIT
- [Introduction to Linear Dynamical Systems (2008 Archive)](../courses/control-systems/068-ee-263.md) — **必学**; Stanford University

**做到这里再往下：** 从物理假设推导多状态模型、识别参数，并在未参与拟合的轨迹上验证。拟合前依据传感器噪声、采样误差和模型近似写明状态预测允许误差；报告归一化误差和失效区间，同时给出可控性与可观性秩检查。

### 反馈与最优控制

**为什么这样排：** 6.302 直接拿上一段识别出的 plant、参数范围和留出轨迹来做反馈设计。想深入连续系统和状态空间时选 6.241J；问题属于序贯决策和随机最优控制时选 6.231。Caltech CDS 101/110 可以帮助统一记号和视角，但不能代替所选分支的题目和控制器实现。

- [Feedback Systems](../courses/control-systems/067-6-302.md) — **必学**; MIT
- [Dynamic Systems and Control](../courses/control-systems/069-6-241j.md) — **选 1 门**; MIT
- [Feedback Systems: An Introduction for Scientists and Engineers](../courses/control-systems/073-cds-101-cds-110.md) — **按需补充**; Caltech; **材料限制待确认**
- [Dynamic Programming and Stochastic Control](../courses/control-systems/072-6-231.md) — **选 1 门**; MIT

**做到这里再往下：** 为同一对象实现经典或最优控制器，并记录增益裕量、相位裕量、超调和调节时间。先写出参数不确定范围，再检查边界角落和一组可重现抽样；样本数由覆盖方法或所需置信区间决定。所有失稳案例必须列出，稳定案例中最差的一组也要解释。

### 机器人系统

**为什么这样排：** 两条路径择一并完整走通：MIT 路线按 6.4210→6.832 聚焦 manipulation 与欠驱动系统；Modern Robotics 路线按 Course 1–6 顺序完成，平台完整访问可能收费。无论选哪条，都把前面的 plant、controller 和测试带进机器人问题。这里的“走完”只指按顺序完成所选路径的工作，不代表获得课程结业或证书，也不能把两条路线各读一半后称为完整主线。

**完整路线 — MIT 机器人路径（按列出顺序学习）**

1. [Robotic Manipulation](../courses/robotics/074-6-4210.md) — **路线内课程**; MIT
2. [Underactuated Robotics](../courses/robotics/075-6-832.md) — **路线内课程**; MIT

**完整路线 — Modern Robotics 完整路径（课程 1–6 按序；平台完整访问可能收费）（按列出顺序学习）**

1. [Modern Robotics, Course 1: Foundations of Robot Motion](../courses/robotics/077-modern-robotics-1.md) — **路线内课程**; Northwestern University
2. [Modern Robotics, Course 2: Robot Kinematics](../courses/robotics/078-modern-robotics-2.md) — **路线内课程**; Northwestern University
3. [Modern Robotics, Course 3: Robot Dynamics](../courses/robotics/079-modern-robotics-3.md) — **路线内课程**; Northwestern University
4. [Modern Robotics, Course 4: Robot Motion Planning and Control](../courses/robotics/080-modern-robotics-4.md) — **路线内课程**; Northwestern University
5. [Modern Robotics, Course 5: Robot Manipulation and Wheeled Mobile Robots](../courses/robotics/081-modern-robotics-5.md) — **路线内课程**; Northwestern University
6. [Modern Robotics, Course 6: Capstone Project, Mobile Manipulation](../courses/robotics/082-modern-robotics-6.md) — **路线内课程**; Northwestern University

**做到这里再往下：** 先在仿真中闭合感知—规划—控制链。测试前写明成功率目标、扰动分布和置信区间精度，再由此确定试验数；报告成功率及区间、轨迹误差、每次失败和观察到的碰撞，有限次数的零碰撞不是安全保证。转到实体平台时，只能使用低能量、限速、有围挡和急停的设备，同样场景须先在仿真通过，任何安全停机都按任务失败统计。
