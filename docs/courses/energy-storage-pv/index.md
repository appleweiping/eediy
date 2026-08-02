---
title: "储能与光伏"
description: "电化学储能、太阳能电池、系统建模与能量管理，明确电池、激光和高压安全边界。"
page_type: track
track_id: "track-energy-storage-pv"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 99855e0c76a51a45 -->

# 储能与光伏

## 方向定位

电化学储能、太阳能电池、系统建模与能量管理，明确电池、激光和高压安全边界。

## 建议先修方向

- [半导体器件](../semiconductor-devices/index.md)
- [电路分析](../circuits/index.md)
- [工程数学](../mathematics/index.md)

## 光伏与电化学是两条器件主线，只有系统问题才把它们相连

[TU Delft Photovoltaic Energy Conversion](122-pv-energy-conversion.md)的[官方课程页](https://www.edx.org/learn/solar-energy/delft-university-of-technology-solar-energy-photovoltaic-pv-energy-conversion)沿太阳光谱、solar cell、module 和 system 组织 PV，适合研究 irradiance 与 temperature 怎样变成 DC power，也能支撑逐时 energy-yield model。视频、讲义和开放配套材料可用，edX 免费访问、证书与活动则可能随期次变化。

[MIT 10.626](123-10-626.md)的[官方档案](https://ocw.mit.edu/courses/10-626-electrochemical-energy-systems-spring-2014)用 38 次 class session、5 份无解 problem set、1 份带解 midterm 和 1 份无解 final 讲 thermodynamics、kinetics、transport、battery、fuel cell 与其他 electrochemical system。它是 Chemical Engineering 研究生课程，官方先修为 10.50 Analysis of Transport Phenomena，不是 pack integration 或 BMS 课程。两门相互独立：太阳能电池、组件和发电量走 TU Delft，电化学 cell-scale model 走 10.626；load、sunlight 与 storage 确实在同一时间轴交换 power 时，才需要把两边接成系统。

一开始就把两种模型耦合，会让光照预测、器件转换、电池状态与调度误差混在一起。分别建立可检查的输入输出关系，再讨论能量如何在它们之间分配，因果关系会清楚得多。

## PV 从结与等效电路出发，storage 从守恒与传输出发

PV 需要[半导体器件](../semiconductor-devices/index.md)中的 pn junction、generation/recombination、I–V 与 temperature dependence，以及[电路分析](../circuits/index.md)中的 equivalent circuit、power、efficiency 与 dynamic load。简化 one-diode model 应能预测 irradiance/temperature 改变时 `Isc`、`Voc` 和 maximum-power point 的方向，并说明 series/shunt resistance 在曲线哪一段显现。

10.626 更依赖[工程数学](../mathematics/index.md)中的 differential equation、diffusion、nondimensionalization、parameter estimation 和 numerical stability。由 conservation 与 boundary condition 建立一维 diffusion/reaction model，区分 voltage loss、SOC、capacity、energy、power 与 charge。只会拟合 curve 却说不清 parameter identifiability 时，复杂 dispatch optimization 还没有可信的 component model。

光伏曲线至少检查开路、短路和最大功率点三个极限；电化学模型至少检查质量或电荷守恒、初始状态与边界通量。参数即使能拟合一段数据，也可能彼此补偿而没有唯一物理含义，因此要报告可辨识范围而非只给最优值。

PV 可以使用 pvlib 和公开 weather/module data，storage 可以使用 PyBaMM 与公开 cell dataset。software version、license、time resolution、missing-data treatment、parameter set、solver tolerance 和 thermal boundary 都会影响结果。默认不制造或拆解 cell，不循环未知或受损 battery，不搭无保护 high-voltage pack，也不把 rooftop PV 接 mains；有受监督的台面条件也只使用合格低压模块、BMS、限流、温度监测与防火隔离。

数据与仿真已经足以完成许多器件问题。缺少监督和合格硬件时，把结论限定在模型层并不会降低严谨性，反而避免用危险操作换取无法校准的读数。

## 在阴天、低电量和高温处检查模型的适用范围

PV 模型可连接 irradiance、temperature、module 与 MPPT，storage 模型可连接 current、SOC、voltage 与 temperature。用手算极限和一段数据识别参数，再拿未参与拟合的 weather 或 drive cycle 检查 energy error、voltage/temperature residual 与 constraint violation。分别改变一个 device parameter 与一个 operating condition，避免总体 RMSE 把 low irradiance、low SOC、temperature extreme 或 ageing mismatch 平均掉。

junction/recombination 主导误差时继续 PV device；electrode kinetics 和 transport 主导时转 electrochemical material；component model 已可信，而剩余问题是 converter、MPPT 或 grid control 时，转 power electronics。只有 PV 与 storage 各自的端口模型都能独立解释数据后，coupled dispatch 才能回答系统问题，避免用调度算法掩盖器件模型的缺口。

结果还应按工况展示残差，例如分别列阴天、低荷电状态和高温区间。若误差只在这些边界突然增大，就需要修正适用范围或物理模型，一个总体平均数无法替它作结论。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Solar Energy Engineering: Photovoltaic Energy Conversion](122-pv-energy-conversion.md) | Delft University of Technology | 主课 | 公开材料导读 | 部分开放或受限 |
| [Electrochemical Energy Systems](123-10-626.md) | MIT | 主课 | 公开材料导读 | 部分开放或受限 |
