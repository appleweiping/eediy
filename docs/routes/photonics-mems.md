---
title: "光电、光子与 MEMS"
description: "完成一个光子或光电 MEMS 设计，包含模式与器件仿真、虚拟工艺约束、版图和系统性能预算；若只想学纯 MEMS，这不是最短路线。"
page_type: route
route_id: "route-photonics-mems"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 1a749ed6ae1f8677 -->

# 光电、光子与 MEMS

## 适合人群

想从波、材料与模式进入光电器件，并可把可动结构作为 MEMS 分支加入的人

## 学完能做什么

完成一个光子或光电 MEMS 设计，包含模式与器件仿真、虚拟工艺约束、版图和系统性能预算；若只想学纯 MEMS，这不是最短路线。

## 先解模式题，再看器件菜单

先解一个平板波导或 Fabry–Pérot 腔的模式题，写出材料折射率、波长、边界条件和归一化方式。若波动、电磁边界或能带仍靠记忆，先补共同物理；纯 MEMS 目标应改走微纳工艺路线。

## 先让求解器经得起复核

- 用解析或第二求解器复核模式有效折射率，并做网格、边界距离和材料参数收敛；保存归一化与功率定义。

## 器件机制选一条，系统出口也选一条

- 从 ECE 5330、ECE 5310 或 6.777J 中只选与器件机制相符的分支，把虚拟工艺尺寸与容差传入器件角落扫描。
- 系统阶段在 2.71、3.46 或确有完整访问的 UBC Silicon Photonics 中选一条，链路预算沿用真实器件损耗与尺寸敏感度。
- 已有量子能力时跳过 8.04，但不能跳过能带、态密度、发射与吸收能力检查；不要同时修所有器件分支。
- 没有 PDK、求解器、制造和测量数据流程时跳过 UBC 实验声明；产品页或受限 lab 不算完成。

## 以性能预算收口，不冒充实验

- 模式与器件结果对网格、边界和关键尺寸收敛，虚拟工艺角落能一条命令重跑，未制造与未测量项明确。
- 系统预算使用上述器件结果而非理想目录值，并能指出哪一个材料、尺寸或耦合假设主导性能；不需要洁净室或激光实测。

!!! warning "开始前请确认这些课程的材料限制"
    - [Silicon Photonics Design, Fabrication and Data Analysis](../courses/optics-photonics/133-phot1x.md)：KLayout、SiEPIC、gdsfactory、远程流片与测量构成了难得的选课后完整闭环，但公开 edX 页面没有提供固定的官方 PDK、版图、求解器或测量数据包。课程包含的流程默认不会向每位参与者邮寄一颗个人芯片；当前 FAQ 表示可在课程进行期间或结束后另行购买个人芯片。因此，流片日期、工具许可、地区访问、购买资格、价格、运输以及其他条款都必须重新核对。 最近核对：2026-07-31。

## 怎么走

### 光子器件前的共同物理

**为什么这样排：** 8.02X、8.03SC、ECE 3030 和 ECE 4070 分别补电磁、波、工程场以及材料与器件。后面要读的 ECE 5330 明确要求量子力学：若还不能解释能带、态密度、发射和吸收，就先学 8.04 相关单元或用等价背景补足。已有这部分基础可以跳过 8.04，但只能替换课程，不能省掉量子能力。

- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **必学**; MIT
- [Physics III: Vibrations and Waves](../courses/physics/012-8-03sc.md) — **必学**; MIT
- [Quantum Physics I](../courses/physics/013-8-04.md) — **按需补充**; MIT
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **必学**; Cornell University
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **必学**; Cornell University

**做到这里再往下：** 求出波导或谐振腔在声明频段内的全部相关模式，并用另一种数值方法复核。逐步加密网格，直到本征频率和归一化场能量稳定；允许误差由离散化趋势和器件规格共同确定。

### 从模式到器件和工艺

**为什么这样排：** 继续使用前面的模式求解器、场归一化、材料参数和收敛结果，把它们转成器件指标与自动仿真测试。6.152J 用于理解虚拟工艺约束，ECE 5330 负责半导体光电器件；前者不授权家庭加工。可动结构、微加工和机电耦合选 6.777J，发射或探测中的量子态与噪声选 ECE 5310。洁净室、激光、化学品和加工设备只限合规设施与合格监督。

- [Micro/Nano Processing Technology](../courses/fabrication-mems/126-6-152j.md) — **必学**; MIT
- [Design and Fabrication of Microelectromechanical Devices](../courses/fabrication-mems/129-6-777j.md) — **选 1 门**; MIT
- [Quantum Optics for Photonics](../courses/optics-photonics/130-ece-5310.md) — **选 1 门**; Cornell University
- [Semiconductor Optoelectronics](../courses/optics-photonics/131-ece-5330.md) — **必学**; Cornell University

**做到这里再往下：** 设计一个绑定具体工艺的光电、波导或 MEMS 器件。依据工艺规则和失效分析，找出所有可能使性能越界的尺寸与材料变量，逐项做灵敏度和角落扫描；报告可接受容差、最坏角落性能，并让版图通过所采用的规则检查。

### 光子系统

**为什么这样排：** NPTEL Introduction to Photonics 只建立共同系统词汇，随后三门严格三选一：有完整 PDK 与数据流程时走 UBC Silicon Photonics；做自由空间成像与 Fourier optics 时走 MIT 2.71；做材料、波导和器件实现时走 MIT 3.46。三条分支都必须沿用前一阶段的器件模型、工艺角落和尺寸敏感度，不能用目录理想值替换。

- [Introduction to Photonics](../courses/optics-photonics/132-108106135.md) — **必学**; IIT Madras / NPTEL

**完整路线 — UBC Silicon Photonics（按列出顺序学习）**

1. [Silicon Photonics Design, Fabrication and Data Analysis](../courses/optics-photonics/133-phot1x.md) — **路线内课程**; University of British Columbia; **材料限制待确认**

**这条分支做到哪里：** 只有 PDK、版图或求解器、制造与测量数据流程都可访问时才走这条分支；产物包含可重跑版图—器件—链路预算及未取得的制造或测量证据清单。

**完整路线 — MIT 2.71 自由空间与 Fourier optics（按列出顺序学习）**

1. [Optics](../courses/optics-photonics/134-2-71.md) — **路线内课程**; MIT

**这条分支做到哪里：** 完成自由空间成像或 Fourier-optics 系统预算与容差扫描；没有公开完整实验包时明确停在解析和仿真。

**完整路线 — MIT 3.46 光子材料与器件（按列出顺序学习）**

1. [Photonic Materials and Devices](../courses/optics-photonics/135-3-46.md) — **路线内课程**; MIT

**这条分支做到哪里：** 把材料色散和损耗传入波导或器件实现，完成尺寸与材料角落下的链路预算；受限制造或测量不写成已完成。

**做到这里再往下：** 完成片上或自由空间光链路预算，检查插入损耗、带宽、串扰和每比特能耗。对尺寸与材料偏差运行可复现的蒙特卡洛分析；样本数由目标良率附近需要的置信区间宽度决定，必要时继续增加。最终一起报告随机种子、达标率和置信区间。
