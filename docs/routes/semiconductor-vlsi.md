---
title: "半导体、微纳工艺与 VLSI"
description: "完成一个数字芯片设计，使器件参数、工艺假设、RTL、时序与功耗约束、验证结果和版图使用同一套前提。"
page_type: route
route_id: "route-semiconductor-vlsi"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 60f1ab2f0fdd42e8 -->

# 半导体、微纳工艺与 VLSI

## 适合人群

想把半导体器件、微纳工艺、数字 IC 和物理实现连成一条设计链的人

## 学完能做什么

完成一个数字芯片设计，使器件参数、工艺假设、RTL、时序与功耗约束、验证结果和版图使用同一套前提。

## 先选器件问题还是版图问题

选一个 CMOS 反相器，写出使用的器件模型、VDD、温度、负载和工艺假设；从 I–V 曲线估算开关点与延迟。若这些前提不能固定，先停在器件模型，不要把 RTL 直接送进版图。

## 只把一个经检验的器件模型向前传

- 从能带、器件曲线和紧凑模型得到一套版本化参数，再把关键尺寸、容差与工艺规则传到门级延迟和功耗估计。
- 微纳工艺只做虚拟流程与案例分析；选择 MEMS、系统微加工或 IC 产线概览之一，不把洁净室内容改写成家庭实验。

## 工具、PDK 与公开材料各有边界

- 数字实现路径只选一条公开条件可满足的流程，固定 RTL、测试、时序/功耗约束、教育 PDK 与工具版本，并保留迁移旧流程时的差异。
- 量子基础、6.012 和 6.701 只补实际缺口，不把三门都当概论；同一数字版图问题不同时走 6.884、6.374 与 ECE 4740。

## 在 tapeout 话术之前停下

- 没有授权 PDK、商业 EDA 或配套文件时跳过对应签核声明；公开教育流程不能写成 foundry signoff。
- 器件参数、工艺假设、RTL 回归、综合/时序/功耗和版图检查能追到同一版本，任何模型替换都触发对应回归。
- 版图只对所声明教育规则完成 DRC/LVS 与可用的寄生分析；没有制造和硅片测量时停在教育流程，不宣称流片。

## 怎么走

### 波与量子准备

**为什么这样排：** 8.04 的正式前置是 8.03，因此先用 8.03SC 建立波动、复振幅、边界条件和 Fourier 表示。若这些内容已有等价训练，可以直接做课程题证明；否则补完会影响量子与器件模型的单元。

- [Physics III: Vibrations and Waves](../courses/physics/012-8-03sc.md) — **必学**; MIT

**做到这里再往下：** 推导并数值复算一个带边界条件的波动本征问题，网格加密时本征值和归一化误差收敛，并能说明它与后续量子能级模型的对应关系。

### 从能带到紧凑模型

**为什么这样排：** ECE 3150 与 6.012 把器件物理连接到电路模型，ECE 4070 提供半导体物理，6.004 则补齐后续数字 VLSI 路线需要的逻辑设计背景。再按实际短板选一门：量子基础不足选 8.04，需要纳米尺度输运时选 6.701；两者不是可互换的器件概论。

- [Quantum Physics I](../courses/physics/013-8-04.md) — **选 1 门**; MIT
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **必学**; Cornell University
- [Microelectronic Devices and Circuits](../courses/microelectronics/030-6-012.md) — **必学**; MIT
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **必学**; MIT
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **必学**; Cornell University
- [Introduction to Nanoelectronics](../courses/semiconductor-devices/125-6-701.md) — **选 1 门**; MIT

**做到这里再往下：** 从能带和输运假设推出器件 I–V/C–V，再从公开或仿真数据提取紧凑模型参数。拟合前依据数据分辨率、噪声或求解器误差写明允许误差；在留出的偏置区间报告归一化 RMSE，并标出模型开始失效的位置。

### 把器件变成工艺流程

**为什么这样排：** 把已经得到的紧凑模型、偏置范围和器件假设翻译成关键尺寸、工艺目标与容差。6.152J 提供共同的微纳工艺基础；目标确实是 MEMS 才选 6.777J，需要系统的微加工顺序选 memsX，想了解 IC 产线全貌选 NPTEL。独立学习只做仿真和案例分析，不意味着可以在家搭洁净室。化学品、真空、高温和加工设备只允许在合规设施中由合格人员监督使用。

- [Micro/Nano Processing Technology](../courses/fabrication-mems/126-6-152j.md) — **必学**; MIT
- [Micro and Nanofabrication (MEMS)](../courses/fabrication-mems/127-memsx.md) — **选 1 门**; EPFL
- [Basic Overview of Semiconductor Device Processing and IC Fabrication](../courses/fabrication-mems/128-108104865.md) — **选 1 门**; IIT Kanpur / NPTEL
- [Design and Fabrication of Microelectromechanical Devices](../courses/fabrication-mems/129-6-777j.md) — **选 1 门**; MIT

**做到这里再往下：** 画出掩膜层、器件截面和逐步工艺流程，并为每个会影响性能或良率的关键尺寸写明容差及来源。用设计规则检查和 FMEA 找出主要失效机理，至少量化一个工艺变量对良率的敏感度。

### 从晶体管到数字版图

**为什么这样排：** 这里的三条路线都有缺口，开始前必须先打开材料和工具。匿名自学优先选 6.884：讲义、实验和代码公开，但旧标准单元假设与商业 EDA 不能照搬，分析应迁移到注明版本的现代工具。6.374 只在能合法取得教材或历史材料时选择；公开档案缺少视频和完整授课讲义，2003 年专有流程也只能作为历史案例。ECE 4740 只在商业 EDA、5 个公开实验和配套文件均可用时选择，并标明没有公开解答和期末项目。EECS 151 适合核对当前课程结构和公开考题，但 CalNet 后的教学站点不能算一条可执行路线。无论选哪条，都沿用前面的器件参数、工艺规则、掩膜和容差；没有授权 PDK 时，结论只能限于所声明的教育工艺。

**完整路线 — 公开历史系统路线（MIT 6.884）（按列出顺序学习）**

1. [Complex Digital Systems](../courses/vlsi-ic/049-6-884.md) — **路线内课程**; MIT

**完整路线 — 历史晶体管设计路线（MIT 6.374）（按列出顺序学习）**

1. [Analysis and Design of Digital Integrated Circuits](../courses/vlsi-ic/050-6-374.md) — **路线内课程**; MIT

**完整路线 — 商业工具实验路线（Cornell ECE 4740）（按列出顺序学习）**

1. [VLSI Systems](../courses/vlsi-ic/051-ece-4740.md) — **路线内课程**; Cornell University

- [Digital Design and Integrated Circuits](../courses/vlsi-ic/044-eecs-151.md) — **按需补充**; University of California, Berkeley

**做到这里再往下：** 完成一个可综合数字模块的规格、RTL、验证和实现。回归测试必须零失配，目标约束下时序收敛，并报告面积、功耗估计以及一项真正由规格推动的设计取舍。
