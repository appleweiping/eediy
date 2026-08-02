---
title: "精简 EE 核心"
description: "用一个一阶 RC 低通把微积分、微分方程、概率、电路与信号接起来，留下可重跑的解析—仿真对照。做到这里就是这条最短主线的完整出口；数字系统、电磁场、器件和实体板卡都是后续分支，不冒充本科 EE 的完整广度。"
page_type: route
route_id: "route-essential-core"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 540605802e5820e2 -->

# 精简 EE 核心

## 适合人群

想补齐关键 EE 基础、但没有时间把每门公开课从头修完，并愿意围绕同一个项目学习的人

## 学完能做什么

用一个一阶 RC 低通把微积分、微分方程、概率、电路与信号接起来，留下可重跑的解析—仿真对照。做到这里就是这条最短主线的完整出口；数字系统、电磁场、器件和实体板卡都是后续分支，不冒充本科 EE 的完整广度。

## 先找第一处断点

先不要下载整套课程。给定 R = 1 kΩ、C = 1 µF，限时 45 分钟写出时间常数、单位阶跃响应和 −3 dB 频率，再用任意熟悉的语言画出响应。不会的那一步，才决定第一门要打开的课。

## 把不确定性接进 RC 电路

- 按导数与线性化→一阶微分方程→期望与方差→KCL 与一阶暂态的依赖顺序，每次只做一道未见过答案的诊断题。第一处独立完成失败就是停止点：只打开能修补该失败的最小课程单元，再用两道改变参数和表述的新题复测；通过后继续下一接口，不预设题目总数。
- 仍用同一个 RC 低通。先推导极点、阶跃和幅相响应，再把 R、C 建模为相互独立且截断为正值的随机变量，记录均值、标准差与分布依据。解析计算 E[RC] 与 Var(RC)，并用一阶误差传播近似 −3 dB 频率的均值和方差；6.003 只读完成 LTI 推导所需的单元。
- 用固定随机种子做 Monte Carlo，把时间常数和截止频率的样本均值、方差以及 5%/50%/95% 分位数与解析或 delta-method 近似并排比较；样本数增加一倍后关键分位数变化必须落入预先声明的容差。保存重跑命令、参数单位表、收敛图和至少一个故意保留的单位或求解设置失败例，仿真不得写成测量。

## 只认模型真正证明的出口

- 先跳过整门线性代数、C 语言、数字系统、电磁场和半导体器件课；只有项目后来需要状态空间、固件、接口、互连或器件模型时，才回到相应单元。
- 没有隔离限流电源、万用表或示波器、可替换 BOM 和打样预算时，跳过 PCB、固件和板上演示。它们不是完成精简主线的条件。
- 解析式与仿真在预先声明的数值容差内一致，容差扫描可一条命令重跑，失败例能指出是模型、单位还是求解设置出了问题。到这里可以诚实标记为“simulation-only 完成”。
- 若继续实体分支，只在隔离、限流、低压条件下比较测量与仿真；没有器材时停在原理图和仿真即可，不以“还没做板”否定前面的完成。

## 怎么走

### 先用题目定位缺口

**为什么这样排：** 18.01SC、18.03SC 和 6.100L 只提供前面列出的诊断单元。6.041SC 仅作为概率题参考，不计作本路线必修；若诊断显示需要系统学习概率，先另行补足它正式列出的 18.01 与 18.02 背景。18.06SC 在要改写状态空间时再用，6.087 只留给固件或嵌入式分支；这里不要求修完六门课。

- [Single Variable Calculus](../courses/mathematics/001-18-01sc.md) — **必学**; MIT
- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **必学**; MIT
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **按需补充**; MIT
- [Probabilistic Systems Analysis and Applied Probability](../courses/probability-statistics/007-6-041sc.md) — **按需补充**; MIT
- [Introduction to CS and Programming Using Python](../courses/programming-tools/015-6-100l.md) — **必学**; MIT
- [Practical Programming in C](../courses/programming-tools/016-6-087.md) — **按需补充**; MIT

**做到这里再往下：** 诊断链在第一处失败时确实停止，只补了对应的最小课程单元；随后两道改变参数与表述的新题均可无提示完成。RC 解析脚本能从干净环境一条命令运行，并拒绝没有单位或超出定义域的输入。

### 把 RC 手算接到仿真

**为什么这样排：** 6.002 只取 KCL、一阶暂态和小信号频率响应，6.003 只取连续时间 LTI、卷积与频率响应；6.041SC 的期望、方差与 Monte Carlo 接口必须继续作用在 R、C 容差上，而不是学完后丢掉。6.004、ECE 3030、ECE 3150 分别留给数字接口、互连和器件分支；PCB workshop 与 ECE 4760/5730 是实体扩展，不属于最短出口。

- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **必学**; MIT
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **必学**; MIT
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **按需补充**; MIT
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **按需补充**; Cornell University
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **按需补充**; Cornell University
- [The Art and Science of PCB Design](../courses/pcb-eda/055-iap-pcb-2026.md) — **按需补充**; MIT
- [Digital Systems Design Using Microcontrollers](../courses/capstone-practice/057-ece-4760-ece-5730.md) — **按需补充**; Cornell University

**做到这里再往下：** 同一组 R、C 分布和输入生成手算、解析脚本与数值或 SPICE 结果；E[RC]、Var(RC) 及截止频率的一阶近似与带固定 seed 的 Monte Carlo 均值、方差和 5%/50%/95% 分位数并排呈现。样本加倍后的分位数变化和解析—仿真差异落入事先声明的容差，并保留一个单位、步长或模型边界失败例。
