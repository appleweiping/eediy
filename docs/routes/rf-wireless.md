---
title: "电磁、射频、微波与无线"
description: "完成一个含匹配、链路预算、天线/通道模型和法规检查的射频设计或仿真项目。"
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 3a3de7081796fc19 -->

# 电磁、射频、微波与无线

## 适合人群

希望从场与波进入射频电路、天线、接收机和无线链路的学习者

## 最终验收

完成一个含匹配、链路预算、天线/通道模型和法规检查的射频设计或仿真项目。

!!! warning "路线中的主线审计复核项"
    - [Analysis and Design Principles of Microwave Antennas](../courses/rf-microwave-antennas/112-108105114.md)：官方身份是“微波天线分析与设计原理”，不是通用微波工程；没有开放实验或代码。资源清单中的旧 www 主机抓取记录仍为待复核，需要在下一次证据刷新中重抓。 最近审计：2026-07-29。

## 阶段安排

### 场与传输线

**选课要求：** 完成全部 4 门必修；其余 1 门仅在需要补缺时选学。

- [Multivariable Calculus](../courses/mathematics/002-18-02sc.md) — **必修**; MIT; 主线; S
- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **必修**; MIT; 主线; S
- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **必修**; MIT; 主线; A
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **必修**; Cornell University; 主线; S
- [Electromagnetics and Applications](../courses/electromagnetics/108-6-013.md) — **可选补充**; MIT; 主线; S

**阶段退出条件：** 建立一段传输线或波导的解析与数值模型，完成至少 3 档网格的收敛研究；传播常数偏差低于 3%，端口功率平衡残差低于 5%。

### 射频电路与天线

**选课要求：** 完成全部 1 门必修，并从 2 门选修候选中选择 1 门。其余 1 门为可选补充，不计入本阶段选修数。

- [Radio Frequency Systems](../courses/rf-microwave-antennas/110-ece-4880.md) — **选修候选**; Cornell University; 替代; A
- [RF and Millimeter-Wave Circuit Design](../courses/rf-microwave-antennas/111-rf-and-millimeter-wave-circuit-design.md) — **必修**; Eindhoven University of Technology; 主线; A
- [Analysis and Design Principles of Microwave Antennas](../courses/rf-microwave-antennas/112-108105114.md) — **可选补充**; IIT Kharagpur / NPTEL; 主线; A; **审计复核中**
- [Receivers, Antennas, and Signals](../courses/rf-microwave-antennas/113-6-661.md) — **选修候选**; MIT; 补充; B

**阶段退出条件：** 完成一个匹配网络、射频前端或天线设计，在声明频段达到 S11 低于 −10 dB 或经论证的等效目标；同时提交增益、噪声和稳定性预算。

### 无线系统

**选课要求：** 完成全部 1 门必修，并从 3 门选修候选中选择 1 门。

- [Principles of Digital Communications I](../courses/communications/100-6-450.md) — **必修**; MIT; 主线; S
- [Principles of Wireless Communications](../courses/communications/104-6-452.md) — **选修候选**; MIT; 补充; B
- [Wireless Communications](../courses/communications/105-ee-359.md) — **选修候选**; Stanford University; 替代; A
- [Principles of Digital Communications](../courses/communications/106-108101113.md) — **选修候选**; IIT Bombay / NPTEL; 替代; A

**阶段退出条件：** 给出可复算的链路预算和含衰落/干扰的信道仿真，绘制接收灵敏度与 BER/吞吐量曲线；频率、带宽、发射功率和占空比通过目标地区法规清单核对。

## 执行规则

- 按每个阶段的选课要求完成全部必修与指定数量的选修；若提供完整路径选项，只选择一条并按序完成其中全部课程；可选补充只用于填补明确缺口。
- 阶段内至少完成一个可复现产物，并把失败记录纳入复盘。
- 涉及市电、高压、射频辐射、激光、化学品或加工设备时，必须遵守本地法规并由合格人员监督。
