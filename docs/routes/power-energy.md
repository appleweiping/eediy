---
title: "电力、电机、电力电子与能源"
description: "在仿真范围内完成变换器控制，并把它接入电机、电网或能源场景；每一步都能解释能量流、器件应力、稳定性和故障后的约束变化。"
page_type: route
route_id: "route-power-energy"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 5068d405572a5227 -->

# 电力、电机、电力电子与能源

## 适合人群

想把磁性元件、功率变换、电机、电网与光伏或储能接在同一个能量系统里的人

## 学完能做什么

在仿真范围内完成变换器控制，并把它接入电机、电网或能源场景；每一步都能解释能量流、器件应力、稳定性和故障后的约束变化。

## 先把能量账算平

先用理想 buck 变换器做功率守恒：给定 Vin、占空比、L、C 与负载，算稳态输出、电感纹波和器件应力，再用平均模型复核。若额定值和能量流还说不清，路线保持 simulation-only。

## 从场模型走到受控变换器

- 让 6.002 的端口功率与 ECE 3030 的磁场模型解释同一个电感器、变压器或电机，记录饱和、损耗与额定值假设。
- 在 6.622/Power Electronics 主线中从开关模型到平均模型再到闭环，分别检查稳态、启动、负载阶跃、饱和和保护边界。

## 只接一个系统，并在仿真证据处收口

- 最后只接一个系统：电网、电机、光伏或储能；变换器控制器、应力和降额必须进入同一份能量平衡与故障场景。
- 先跳过不能独立完成的高压、大电流和并网硬件；课程仿真不授权搭建市电变换器。
- Converter Circuits 与 Converter Control 只在前一模块完成且平台可访问时顺序追加；能源方向只选一个。
- 固定配置可重跑开关与平均模型、闭环稳定性、器件应力和降额检查，能量不平衡落在预先解释的数值或损耗范围内。
- 故障注入后，保护动作、恢复条件和系统约束变化可见；在没有合规实验室与监督时，仿真就是完整且诚实的出口。

## 怎么走

### 磁场如何变成端口功率

**为什么这样排：** 6.002 负责集总电路和功率，ECE 3030 负责磁场与边界；两门始终分析同一个电感器、变压器或电机，不把磁路和端口模型拆开。只有传输线、波导或 Poynting 能量流的推导仍不稳时，才加入 6.013 对应章节。

- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **必学**; MIT
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **必学**; Cornell University
- [Electromagnetics and Applications](../courses/electromagnetics/108-6-013.md) — **按需补充**; MIT

**做到这里再往下：** 建立电感器、变压器或电机磁路的场—路联合模型，核对磁通、储能和端口功率。稳态量的允许差异由材料参数容差、手算近似与网格收敛误差共同决定；瞬态能量差额必须能由损耗项和数值误差解释。

### 变换器与闭环

**为什么这样排：** 把刚完成的磁性元件模型带入 6.622，保留参数、额定值和能量检查；6.622 是闭环变换器主线。需要更多分步练习且 Coursera 可访问时，才追加下面完整的 Power Electronics 1→2→3 有序扩展。这个扩展必须从 1 开始顺序走完，不能把 2、3 当作无序补充，也不改变默认 simulation-only 边界。

- [Power Electronics](../courses/power-electronics/114-6-622.md) — **必学**; MIT
- [Introduction to Power Electronics](../courses/power-electronics/115-power-electronics-1.md) — **按需补充**; University of Colorado Boulder
- [Converter Circuits](../courses/power-electronics/116-power-electronics-2.md) — **按需补充**; University of Colorado Boulder
- [Converter Control](../courses/power-electronics/117-power-electronics-3.md) — **按需补充**; University of Colorado Boulder

**可选有序扩展 — Coursera Power Electronics 1→2→3（按列出顺序学习）**

1. [Introduction to Power Electronics](../courses/power-electronics/115-power-electronics-1.md) — **扩展内课程**; University of Colorado Boulder
2. [Converter Circuits](../courses/power-electronics/116-power-electronics-2.md) — **扩展内课程**; University of Colorado Boulder
3. [Converter Control](../courses/power-electronics/117-power-electronics-3.md) — **扩展内课程**; University of Colorado Boulder

**扩展做到哪里：** 按 1→2→3 的顺序完成建模、变换器电路和控制；每一门的模型与测试必须成为下一门的输入。若平台访问或前一门产物缺失，就在最后完成的模块停止，不把后续标题列为已完成。

**做到这里再往下：** 在仿真中实现一种变换器及其闭环控制，检查纹波、效率、稳定裕量、器件应力和降额。实体变换器不属于本路线默认范围；若要扩展，必须重新核对课程范围、接受合格监督并做风险评估。不得自行连接市电、高压或大电流，也不得把仿真写成硬件测试。

### 并入电网、电机或能源系统

**为什么这样排：** 下面四条是互斥的完整出口，只走一条：电网分析、电机与驱动、光伏能量转换或电化学储能。每条都从前一阶段带入同一个变换器模型、控制器以及应力与降额检查。不要为了路线看起来“全面”同时强制电网和电机；若目标后来改变，另开一次路线记录。

**完整路线 — 电网分析（按列出顺序学习）**

1. [Power System Analysis](../courses/power-systems-machines/118-117105140.md) — **路线内课程**; IIT Kharagpur / NPTEL

**这条分支做到哪里：** 把变换器作为受控注入或负载接入固定基值的电网模型，完成潮流与一个 N−1 或故障场景，报告残差、约束违例和恢复条件。

**完整路线 — 电机与驱动（按列出顺序学习）**

1. [Electric Machines](../courses/power-systems-machines/120-6-685.md) — **路线内课程**; MIT

**这条分支做到哪里：** 把变换器接到电机模型，完成启动、负载跃迁和一个失速或限流场景，能量、转矩、速度和器件应力使用同一时间轴。

**完整路线 — 光伏能量转换（按列出顺序学习）**

1. [Solar Energy Engineering: Photovoltaic Energy Conversion](../courses/energy-storage-pv/122-pv-energy-conversion.md) — **路线内课程**; Delft University of Technology

**这条分支做到哪里：** 把光伏 I–V/P–V 模型接入变换器，完成辐照度与温度跃迁、最大功率点跟踪和降额检查，并报告能量损失去向。

**完整路线 — 电化学储能（按列出顺序学习）**

1. [Electrochemical Energy Systems](../courses/energy-storage-pv/123-10-626.md) — **路线内课程**; MIT

**这条分支做到哪里：** 把带 SOC、倍率和热约束的储能模型接入变换器，完成充放电跃迁和一个保护触发场景，报告效率、约束违例与恢复条件。

**做到这里再往下：** 完成所选分支的能量平衡与一个适合该系统的故障或工况跃迁，残差容差由系统基值、求解器和模型精度共同决定。报告保护动作、约束违例和恢复条件；未选分支不计入完成要求。
