---
title: "本科 EE 核心路线"
description: "从数学、物理和编程一路走到电路、信号、数字系统、电磁场、器件、实验与方向综合。它可以帮助发现本科基础中的空缺，但不等同于大学学位、学分或任何认证。"
page_type: route
route_id: "route-undergraduate-core"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 27e446ecb4c0d43d -->

# 本科 EE 核心路线

## 适合人群

想按本科培养的广度与深度重建 EE 基础，并愿意完成实验和综合设计的人

## 学完能做什么

从数学、物理和编程一路走到电路、信号、数字系统、电磁场、器件、实验与方向综合。它可以帮助发现本科基础中的空缺，但不等同于大学学位、学分或任何认证。

## 先定位，不先抄培养方案

先从五类题各抽一题：微积分、线性代数、电磁学、电路暂态和概率。再写一个最小 Python 模型。把不会做或只能照答案做的项记成缺口；这张缺口表决定课程顺序，而不是学校名称。

## 每一层只留一条主线

- 每个阶段选一个贯穿对象，例如二阶 RLC 网络或电机—变换器；数学推导、代码、场模型和实验都更新同一组参数，不另起互不相干的课程作业集。
- 先做阶段末任务，再补真正失败的课程单元。实验阶段保留校准、不确定度、额定值和失败记录；仿真、公开数据与实测分别标注。
- 综合设计只接两个确实共享接口的方向，并在开工前写出接口量、单位、更新率、允许误差和停机条件。

## 把方向课推迟到基础会反驳你

- 能在新参数上独立通过阶段任务的课程直接跳过；同一缺口不要同时修两门替代课。
- 器材、许可证或校内 starter 不可得时，跳过对应实体复现，改用边界清楚的仿真或公开数据，不把缺口藏在“等以后补”。

## 本科广度要用跨层产物验收

- 五个阶段各有一份可复核产物，前一阶段的参数和失败能追到后一阶段，综合设计的两个接口场景均按预先写下的允许误差通过。
- 若目标只是补某一方向，完成相应阶段即可转入专门路线；不必为了“本科完整感”继续堆课，也不得把路线完成写成学位或认证。

## 怎么走

### 先把单变量微积分做实

**为什么这样排：** 18.01SC 是后续 18.02SC 与概率课共同依赖的起点。先做课程的诊断题；若极限、微分、积分和级数已经稳定，可以只完成未通过的单元，但必须保留改换参数后的闭卷复测，不能用“学过”代替证据。

- [Single Variable Calculus](../courses/mathematics/001-18-01sc.md) — **必学**; MIT

**做到这里再往下：** 在不查答案的情况下完成一组覆盖极限、微分、定积分与级数的新题，并把一个带单位的物理量从模型、解析结果到数值图完整算通；每一步的定义域和单位一致。

### 多变量、物理与编程

**为什么这样排：** 沿用上一段的单变量基础，用 18.02SC、18.06SC 和 8.01SC/8.02X 的题目检查多变量微积分、线性代数、力学与电磁学，只重学真正薄弱的单元。6.100L 负责 Python 建模，6.087 负责 C 与内存，两种实现处理同一个物理案例。只有具备课程要求的安全器材时才复现物理实验；否则改用公开数据或仿真，并在 README 中明确说明数据来自哪里。

- [Multivariable Calculus](../courses/mathematics/002-18-02sc.md) — **必学**; MIT
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **必学**; MIT
- [Classical Mechanics](../courses/physics/010-8-01sc.md) — **必学**; MIT
- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **必学**; MIT
- [Introduction to CS and Programming Using Python](../courses/programming-tools/015-6-100l.md) — **必学**; MIT
- [Practical Programming in C](../courses/programming-tools/016-6-087.md) — **必学**; MIT

**做到这里再往下：** 微积分、线性代数、力学和电磁学中任何会妨碍后续课程的错题，都要补学后换一组参数重做。再选一个力学或电磁案例，完成数据采集或公开数据导入、单位检查和拟合；换一台机器仅凭 README 就能重建全部图表，仿真和回放不得写成实测。

### 电路与动态系统

**为什么这样排：** 让 18.03SC、6.002 和 6.003 共同解释一个二阶网络：先写微分方程，再落到电路参数，最后用系统表示连接阶跃和频率响应。前一段的建模、单位检查和拟合代码直接沿用。只有当仪器、误差或测量链仍是短板时，才加入 6.071J；它不能替代三门基础课。

- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **必学**; MIT
- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **必学**; MIT
- [Introduction to Electronics, Signals, and Measurement](../courses/electronics-laboratory/024-6-071j.md) — **按需补充**; MIT
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **必学**; MIT

**做到这里再往下：** 从微分方程推出二阶电路的状态与频域模型，再测量或仿真阶跃和扫频响应。调参前，根据元件容差、仪器不确定度或数值精度写明主极点、直流增益和带宽允许偏差，并用一组未参与拟合的数据验证。

### 概率、数字系统与电磁

**为什么这样排：** 6.041SC 负责随机输入，6.004 负责数字实现，ECE 3030 解释互连中的场，ECE 3150 说明晶体管边界；做过 FPGA 也不能跳过概率或电磁。先把上一段二阶系统的激励和参考响应改成随机数字测试，再让同一接口进入场模型和器件模型。

- [Probabilistic Systems Analysis and Applied Probability](../courses/probability-statistics/007-6-041sc.md) — **必学**; MIT
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **必学**; MIT
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **必学**; Cornell University
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **必学**; Cornell University

**做到这里再往下：** 数字模块的定向测试要覆盖全部状态转移、接口边界和无效输入；随机测试保存种子与覆盖率变化，并与参考模型零失配。互连场模型还要通过网格加密显示传播量收敛，端口功率不平衡不得超过求解器给出的数值误差。

### 实验、PCB 与系统集成

**为什么这样排：** 把模拟网络、数字模块和随机回归放到同一块板上。6.101 用来学模拟调试，MIT PCB workshop 负责投板准备，ECE 4760/5730 负责系统集成。开工前确认旧器件的替代 BOM、隔离限流电源、示波器或万用表、目标 MCU 和打样预算；条件不足可以停在 pre-board，但还没有完成这段实验。已有经验也不能省掉校准、返修和需求到测试的对应关系。

- [Introductory Analog Electronics Laboratory](../courses/analog-electronics/026-6-101.md) — **必学**; MIT
- [The Art and Science of PCB Design](../courses/pcb-eda/055-iap-pcb-2026.md) — **必学**; MIT
- [Digital Systems Design Using Microcontrollers](../courses/capstone-practice/057-ece-4760-ece-5730.md) — **必学**; Cornell University

**做到这里再往下：** 在隔离、限流、低压条件下制造并调通含模拟前端与数字控制的 PCB。测试要覆盖工作范围端点、标称点、关键角落和保护边界，并保留额定值核对、停机条件、校准原始数据、返修记录与实物照片；每项需求都能指向一次测试，不连接市电、人体或未知电源。

### 两个方向的综合设计

**为什么这样排：** RES.6-008 提供共同的信号处理基础；通信分支使用不依赖 6.011 前序的 6.02，而不是直接跳入研究生数字通信。再从通信、线性动态、功率电子、半导体器件和光子学中选两个真正会在系统里相接的方向。先写清两个子系统各自的指标和接口，再决定需要读哪些章节；上一段的板级测试或 pre-board 接口应成为共同输入，而不是按学校名气另起两个无关项目。

- [Digital Signal Processing](../courses/dsp/088-res-6-008.md) — **必学**; MIT
- [Introduction to EECS II: Digital Communication Systems](../courses/communications/099-6-02.md) — **选 2 门**; MIT
- [Introduction to Linear Dynamical Systems (2008 Archive)](../courses/control-systems/068-ee-263.md) — **选 2 门**; Stanford University
- [Power Electronics](../courses/power-electronics/114-6-622.md) — **选 2 门**; MIT
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **选 2 门**; Cornell University
- [Introduction to Photonics](../courses/optics-photonics/132-108106135.md) — **选 2 门**; IIT Madras / NPTEL

**做到这里再往下：** 最终设计要把信号处理与两个方向接成一个系统，每个方向都有从系统需求推导出的性能和接口指标，默认以仿真或公开数据验证。涉及高压或大电流、RF、激光、化学品或加工设备时，只能在合规设施和合格监督下实测。报告写清哪些结论来自仿真、公开数据或实测，并保留一次真正促使设计改变的失败。
