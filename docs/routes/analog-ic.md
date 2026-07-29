---
title: "模拟、混合信号与集成电路"
description: "完成一个带规格、角落仿真、噪声/功耗权衡和版图检查的模拟或混合信号设计。"
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 27c5f4701740fac0 -->

# 模拟、混合信号与集成电路

## 适合人群

希望从电路和器件进入晶体管级设计、仿真与版图的学习者

## 最终验收

完成一个带规格、角落仿真、噪声/功耗权衡和版图检查的模拟或混合信号设计。

## 阶段安排

### 电路与器件

**选课要求：** 完成全部 3 门必修，并从 2 门选修候选中选择 1 门。

- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **必修**; MIT; 主线; S
- [Microelectronics](../courses/microelectronics/029-ece-3150.md) — **必修**; Cornell University; 主线; S
- [Microelectronic Devices and Circuits](../courses/microelectronics/030-6-012.md) — **选修候选**; MIT; 替代; A
- [Microelectronic Devices and Circuits](../courses/microelectronics/031-ee-105.md) — **选修候选**; University of California, Berkeley; 替代; A
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **必修**; Cornell University; 主线; A

**阶段退出条件：** 从公开或仿真 I–V/C–V 曲线提取 MOS 器件参数，并用同一模型预测一个偏置电路的 DC、AC 与瞬态响应；留出数据上的归一化均方根误差低于 10%。

### 模拟设计

**选课要求：** 完成全部 1 门必修，并从 3 门选修候选中选择 2 门。其余 1 门为可选补充，不计入本阶段选修数。

- [Introductory Analog Electronics Laboratory](../courses/analog-electronics/026-6-101.md) — **必修**; MIT; 主线; S
- [Solid-State Circuits](../courses/analog-electronics/032-6-301.md) — **选修候选**; MIT; 补充; B
- [Analog Circuits](../courses/analog-electronics/034-108101094.md) — **选修候选**; IIT Bombay / NPTEL; 替代; A
- [Integrated Circuits, MOSFETs, OP-Amps and Their Applications](../courses/analog-electronics/035-108108111.md) — **选修候选**; Indian Institute of Science / NPTEL; 替代; A
- [Analog IC Design](../courses/analog-ic/036-108106105-noc26-ee66.md) — **可选补充**; IIT Madras / NPTEL; 补充; A

**阶段退出条件：** 设计运算放大器或低噪声前端，逐项验证增益、带宽、相位裕量、噪声、摆率和功耗规格；PVT 与负载角落均通过，未通过项必须形成可复现的权衡记录。

### 集成实现

**选课要求：** 完成全部 2 门必修；其余 1 门仅在需要补缺时选学。

- [Analysis and Design of Digital Integrated Circuits](../courses/vlsi-ic/050-6-374.md) — **必修**; MIT; 主线; A
- [VLSI Systems](../courses/vlsi-ic/051-ece-4740.md) — **可选补充**; Cornell University; 补充; A
- [Micro/Nano Processing Technology](../courses/fabrication-mems/126-6-152j.md) — **必修**; MIT; 主线; S

**阶段退出条件：** 提交带工艺假设的版图与签核包，DRC 和 LVS 零错误，并比较前后仿真的关键指标；寄生导致的性能变化须量化，且每项超差都有版图层面的修正建议。

## 执行规则

- 按每个阶段的选课要求完成全部必修与指定数量的选修；若提供完整路径选项，只选择一条并按序完成其中全部课程；可选补充只用于填补明确缺口。
- 阶段内至少完成一个可复现产物，并把失败记录纳入复盘。
- 涉及市电、高压、射频辐射、激光、化学品或加工设备时，必须遵守本地法规并由合格人员监督。
