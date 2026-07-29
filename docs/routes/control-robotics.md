---
title: "控制、机器人与自主系统"
description: "在仿真或安全实体平台上完成感知—规划—控制闭环，并报告稳定性、误差和失败模式。"
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 04fcaf2df37ad360 -->

# 控制、机器人与自主系统

## 适合人群

希望把动态系统、估计、规划和操控整合成自主系统的学习者

## 最终验收

在仿真或安全实体平台上完成感知—规划—控制闭环，并报告稳定性、误差和失败模式。

!!! warning "路线中的主线审计复核项"
    - [Feedback Systems: An Introduction for Scientists and Engineers](../courses/control-systems/073-cds-101-cds-110.md)：入口是作者维护的第二版教材配套站，提供开放文本、实例、习题和更新后的 Python 图源，但不是当前完整课程运行页；教师习题手册仍受限。 最近审计：2026-07-29。

## 阶段安排

### 数学与动态

**选课要求：** 完成全部 4 门必修。

- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **必修**; MIT; 主线; S
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **必修**; MIT; 主线; S
- [Classical Mechanics](../courses/physics/010-8-01sc.md) — **必修**; MIT; 主线; S
- [Introduction to Linear Dynamical Systems](../courses/control-systems/068-ee-263.md) — **必修**; Stanford University; 主线; S

**阶段退出条件：** 从物理假设推导一个多状态系统，识别参数并在未参与拟合的轨迹上验证；状态预测归一化误差低于 10%，且完成可控性与可观性秩检查。

### 反馈与最优控制

**选课要求：** 完成全部 1 门必修，并从 2 门选修候选中选择 1 门。其余 1 门为可选补充，不计入本阶段选修数。

- [Feedback Systems](../courses/control-systems/067-6-302.md) — **必修**; MIT; 主线; A
- [Dynamic Systems and Control](../courses/control-systems/069-6-241j.md) — **选修候选**; MIT; 替代; A
- [Feedback Systems: An Introduction for Scientists and Engineers](../courses/control-systems/073-cds-101-cds-110.md) — **可选补充**; Caltech; 主线; S; **审计复核中**
- [Dynamic Programming and Stochastic Control](../courses/control-systems/072-6-231.md) — **选修候选**; MIT; 补充; A

**阶段退出条件：** 为同一被控对象实现经典或最优控制器，记录增益/相位裕量、超调和调节时间；在不少于 100 组参数扰动中保持稳定，并解释最差性能样本。

### 机器人系统

**选课要求：** 从以下 2 条完整路径中选择 1 条，并按列出顺序完成所选路径的全部课程。

**完整路径选项 — MIT 机器人路径（按序完成）**

1. [Robotic Manipulation](../courses/robotics/074-6-4210.md) — **路径内课程**; MIT; 主线; S
2. [Underactuated Robotics](../courses/robotics/075-6-832.md) — **路径内课程**; MIT; 主线; S

**完整路径选项 — Modern Robotics 完整路径（课程 1–6 按序；平台完整访问可能收费）（按序完成）**

1. [Modern Robotics, Course 1: Foundations of Robot Motion](../courses/robotics/077-modern-robotics-1.md) — **路径内课程**; Northwestern University; 替代; A
2. [Modern Robotics, Course 2: Robot Kinematics](../courses/robotics/078-modern-robotics-2.md) — **路径内课程**; Northwestern University; 替代; A
3. [Modern Robotics, Course 3: Robot Dynamics](../courses/robotics/079-modern-robotics-3.md) — **路径内课程**; Northwestern University; 替代; A
4. [Modern Robotics, Course 4: Robot Motion Planning and Control](../courses/robotics/080-modern-robotics-4.md) — **路径内课程**; Northwestern University; 替代; A
5. [Modern Robotics, Course 5: Robot Manipulation and Wheeled Mobile Robots](../courses/robotics/081-modern-robotics-5.md) — **路径内课程**; Northwestern University; 替代; A
6. [Modern Robotics, Course 6: Capstone Project, Mobile Manipulation](../courses/robotics/082-modern-robotics-6.md) — **路径内课程**; Northwestern University; 补充; A

**阶段退出条件：** 在仿真或安全平台上闭合感知—规划—控制链路，20 次带扰动试验中任务成功率至少 90%、碰撞为零；提交轨迹误差分布和失败模式复盘。

## 执行规则

- 按每个阶段的选课要求完成全部必修与指定数量的选修；若提供完整路径选项，只选择一条并按序完成其中全部课程；可选补充只用于填补明确缺口。
- 阶段内至少完成一个可复现产物，并把失败记录纳入复盘。
- 涉及市电、高压、射频辐射、激光、化学品或加工设备时，必须遵守本地法规并由合格人员监督。
