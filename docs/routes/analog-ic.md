---
title: "模拟、混合信号与集成电路"
description: "以 Berkeley EE 140/240A 的公开题目和实验说明为模拟 IC 主线，完成规格、偏置、噪声以及模型确实支持的 PVT/负载角落。默认出口是 schematic-level；只有独立核实开放 EDA、合法教育 PDK、DRC/LVS 和提取模型后，才追加独立版图研习，不承诺复现 Berkeley 的校内 Cadence 流程或完整 PEX。"
page_type: route
route_id: "route-analog-ic"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: fb3fbf2319786712 -->

# 模拟、混合信号与集成电路

## 适合人群

想从器件曲线和小信号电路走到晶体管级设计、角落仿真与版图的人

## 学完能做什么

以 Berkeley EE 140/240A 的公开题目和实验说明为模拟 IC 主线，完成规格、偏置、噪声以及模型确实支持的 PVT/负载角落。默认出口是 schematic-level；只有独立核实开放 EDA、合法教育 PDK、DRC/LVS 和提取模型后，才追加独立版图研习，不承诺复现 Berkeley 的校内 Cadence 流程或完整 PEX。

## 装 PDK 前先过 EE 105 能力检查

先做 EE 105/6.012 层级的 MOS 偏置与小信号题，再打开 EE 140/240A Spring 2025 的 HW1 和公开 Lab 1。若 gm、ro、极点和反馈还不能独立算，先补器件桥梁；不要先装 PDK。

先以 EE 105、6.002 和 ECE 3150 连接器件曲线、偏置与小信号；6.012 或 ECE 4070 只补缺失的器件物理，不重复修概论。

## 先把 schematic 主线做实

- 以 EE 140/240A 为晶体管级主线：按公开作业做偏置、增益、频率响应、反馈、噪声和输出摆幅，并用 Lab 1 的 LTspice 范围建立可在校外复现的基线。
- 若另行验证开放工具与教育 PDK，再把一个已冻结的 schematic 做 DRC/LVS；只有提取规则和模型真实可用时才比较寄生前后，所有结论限定在所声明的 PDK 与工具版本。

## 版图是另一层证据，不是默认赠品

- 模拟 IC 路线不再借用 MIT 6.374 或 Cornell ECE 4740 的数字 IC/VLSI 实验作为终点；它们属于数字版图路线。
- 没有 Berkeley 服务器权限时跳过 Labs 2–8 和课程 project 的“原样复现”声明；没有可验证提取模型时也跳过 PEX 数字，而不是填一个占位结果。
- 默认在 schematic-level 停止：规格表、偏置、AC/瞬态/噪声以及实际模型覆盖的 PVT/负载扫描可重跑，失败角落和取舍没有被删掉。
- 独立版图分支只有在 DRC/LVS 对所声明规则为零错误时才算完成；PEX 是可选的下一层，不是无公开提取证据时必须假装达到的门槛。

## 怎么走

### 从器件曲线到偏置

**为什么这样排：** 6.002 负责电路，ECE 3150 负责小信号器件。EE 140/240A 明确以 EE 105 为先修，因此 EE 105 是这条路线的必经桥梁；已有等价能力可以用一组无提示的 MOS 偏置、小信号、频率响应与反馈诊断题替代整门重修，但不能跳过能力验收。6.012 与 ECE 4070 只补器件推导或半导体物理缺口。

- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **必学**; MIT
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **必学**; Cornell University
- [Microelectronic Devices and Circuits](../courses/microelectronics/031-ee-105.md) — **必学**; University of California, Berkeley
- [Microelectronic Devices and Circuits](../courses/microelectronics/030-6-012.md) — **按需补充**; MIT
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **按需补充**; Cornell University

**做到这里再往下：** 从公开或仿真的 I–V/C–V 曲线提取 MOS 参数，再用同一模型预测偏置电路的 DC、AC 和瞬态响应。拟合前依据数据分辨率、噪声或求解器误差写出允许误差，最后在留出数据上报告归一化 RMSE，并标出模型失效的偏置区间。

### EE 140/240A 主线与诚实的版图上限

**为什么这样排：** EE 140/240A 的 Spring 2025 公开作业、部分解答、考试和 Lab 1 构成主线；Labs 2–8 与 project 的 Cadence/Virtuoso、Berkeley 服务器和 SKY130 环境并未形成已验证的校外复现包。NPTEL 材料用于补讲解，6.152J 只补工艺语境，6.101 只在确有低压台面条件时补离散模拟调试。版图属于另行验证工具后的独立研习，不是这些材料自动提供的课程实验。

- [Analog Integrated Circuits](../courses/analog-ic/141-ee-140-ee-240a.md) — **必学**; University of California, Berkeley
- [Analog Circuits](../courses/analog-electronics/034-108101094.md) — **按需补充**; IIT Bombay / NPTEL
- [Integrated Circuits, MOSFETs, OP-Amps and Their Applications](../courses/analog-electronics/035-108108111.md) — **按需补充**; Indian Institute of Science / NPTEL
- [Analog IC Design](../courses/analog-ic/036-108106105-noc26-ee66.md) — **按需补充**; IIT Madras / NPTEL
- [Micro/Nano Processing Technology](../courses/fabrication-mems/126-6-152j.md) — **按需补充**; MIT
- [Introductory Analog Electronics Laboratory](../courses/analog-electronics/026-6-101.md) — **按需补充**; MIT

**做到这里再往下：** 先交付 schematic-level 设计：增益、带宽、相位裕量、噪声、摆率、功耗与模型支持的 PVT/负载角落可重跑，未达标项保留。若另做版图，注明工具、教育 PDK 和 rule deck，DRC/LVS 清零；只有实际存在提取规则与模型时才报告 PEX，且不称为流片签核。
