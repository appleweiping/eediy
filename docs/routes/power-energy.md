---
title: "电力、电机、电力电子与能源"
description: "在安全边界内完成一个变换器、电机驱动、光伏或储能系统的仿真、控制和设计评审。"
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: b95403269cacd799 -->

# 电力、电机、电力电子与能源

## 适合人群

希望覆盖能量变换、设备、电网和储能系统的学习者

## 最终验收

在安全边界内完成一个变换器、电机驱动、光伏或储能系统的仿真、控制和设计评审。

## 阶段安排

### 电路与电磁

**选课要求：** 完成全部 2 门必修；其余 1 门仅在需要补缺时选学。

- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **必修**; MIT; 主线; S
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **必修**; Cornell University; 主线; S
- [Electromagnetics and Applications](../courses/electromagnetics/108-6-013.md) — **可选补充**; MIT; 主线; S

**阶段退出条件：** 建立电感器、变压器或电机磁路的场—路联合模型，核对磁通、储能与端口功率；稳态关键量与手算偏差低于 5%，瞬态能量守恒闭合。

### 变换与控制

**选课要求：** 完成全部 1 门必修，并完成该门选修候选。其余 2 门为可选补充，不计入本阶段选修数。

- [Power Electronics](../courses/power-electronics/114-6-622.md) — **必修**; MIT; 主线; S
- [Introduction to Power Electronics](../courses/power-electronics/115-power-electronics-1.md) — **选修候选**; University of Colorado Boulder; 替代; A
- [Converter Circuits](../courses/power-electronics/116-power-electronics-2.md) — **可选补充**; University of Colorado Boulder; 替代; A
- [Converter Control](../courses/power-electronics/117-power-electronics-3.md) — **可选补充**; University of Colorado Boulder; 替代; A

**阶段退出条件：** 在仿真或限能平台上实现一类变换器及其闭环控制，验证纹波、效率、稳定裕量和器件应力；所有工作点均保留降额检查，硬件测试须使用隔离与电流限制。

### 电网、电机与能源

**选课要求：** 完成全部 2 门必修，并从 4 门选修候选中选择 1 门。

- [Power System Analysis](../courses/power-systems-machines/118-117105140.md) — **必修**; IIT Kharagpur / NPTEL; 主线; A
- [Seminar in Electric Power Systems](../courses/power-systems-machines/119-6-691.md) — **选修候选**; MIT; 替代; A
- [Electric Machines](../courses/power-systems-machines/120-6-685.md) — **必修**; MIT; 主线; S
- [Electrical Machines II](../courses/power-systems-machines/121-108105131.md) — **选修候选**; IIT Kharagpur / NPTEL; 替代; A
- [Solar Energy Engineering: Photovoltaic Energy Conversion](../courses/energy-storage-pv/122-pv-energy-conversion.md) — **选修候选**; Delft University of Technology; 主线; A
- [Electrochemical Energy Systems](../courses/energy-storage-pv/123-10-626.md) — **选修候选**; MIT; 替代; A

**阶段退出条件：** 构建含电网、电机及所选能源技术的统一场景，潮流或能量平衡残差低于 1%；再执行一次 N−1、故障或工况跃迁分析并报告约束违例与恢复时间。

## 执行规则

- 按每个阶段的选课要求完成全部必修与指定数量的选修；若提供完整路径选项，只选择一条并按序完成其中全部课程；可选补充只用于填补明确缺口。
- 阶段内至少完成一个可复现产物，并把失败记录纳入复盘。
- 涉及市电、高压、射频辐射、激光、化学品或加工设备时，必须遵守本地法规并由合格人员监督。
