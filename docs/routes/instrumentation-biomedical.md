---
title: "传感、仪器与生物医学电子"
description: "完成一个可校准的测量系统，给出不确定度、隔离与安全分析，再用公开或合成生理数据验证处理算法；未经另行批准，不接触人体实验。"
page_type: route
route_id: "route-instrumentation-biomedical"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 639c460dc5695c7b -->

# 传感、仪器与生物医学电子

## 适合人群

想把传感器、模拟前端、校准与信号处理连成一条完整测量链的人

## 学完能做什么

完成一个可校准的测量系统，给出不确定度、隔离与安全分析，再用公开或合成生理数据验证处理算法；未经另行批准，不接触人体实验。

## 先画测量链，再谈应用

先选一个非人体、低压传感量，例如光敏电阻或温度，写出量程、带宽、分辨率、允许误差和校准参考。若无法说明误差从传感器、前端、ADC 还是算法进入，先画测量链。

让 6.002、6.071J 与 6.003 解释同一传感信号，分开增益、偏置、带宽、噪声、采样与系统响应，并迁移旧 LabVIEW/DAQ 实验的测量定义而非硬装环境。

## 把校准、接口和失败模式放在一起

- 传感阶段用真实 datasheet、校准点和不确定度预算决定接口；只读项目所用传感器的对应单元，不虚构课程未公开的实验。
- 生理信号阶段只用公开或合成数据，把前端误差与校准传播到 DSP；原始数据来源、许可、去标识和预处理全部记录。
- 没有 Analog Discovery 2/3 时跳过 Real Analog 台面复现；使用仿真或公开数据，并明确标注。

## 分开台面证据、公开数据与临床声明

- 不接人体、不作诊断、不把旧研究生课程当伦理或医疗安全批准；任何人体研究都需要独立机构流程。
- 非人体测量链可由原始校准数据重建，误差预算能解释参考值与输出差异，重复测量与漂移结果在预设范围内。
- 算法在公开或合成生理数据上有留出验证，并保留校准与前端误差；完成不包含人体安全、临床有效性或医疗器械声明。

## 怎么走

### 电路与测量

**为什么这样排：** 围绕同一个传感信号，6.002 解释前端电路，6.071J 组织测量链，6.003 处理系统响应。6.071J 的 LabVIEW、DAQ 和器件环境已经较旧，应迁移测量定义，不要假装复刻原实验。只有手头确有 Analog Discovery 2 或 3，并能遵守低压限流范围时才加入 Real Analog 台面练习；否则使用仿真或公开数据并明确标注。

- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **必学**; MIT
- [Introduction to Electronics, Signals, and Measurement](../courses/electronics-laboratory/024-6-071j.md) — **必学**; MIT
- [Real Analog Courses](../courses/electronics-laboratory/027-real-analog.md) — **按需补充**; Digilent
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **必学**; MIT

**做到这里再往下：** 校准点要覆盖量程端点、标称区以及任何非线性转折或饱和附近，并另留一组独立点检查拟合。把增益、偏置、带宽、噪声和量化误差换算到同一不确定度预算中；留出点的残差必须落在这份预算事先给出的范围内。

### 传感与接口

**为什么这样排：** 前面的测量链、校准数据和不确定度预算现在用来决定接口增益、带宽、采样率与允许漂移。NPTEL Electrical Measurement and Electronic Instruments 是共同的测量基础；Sensors and Sensor Circuit Design 用来补接口和调理，Sensor Technologies 用来理解器件物理、制造和不同传感器的差别。只读项目所用传感器的相关单元，也不要虚构课程并未公开的实验条件。

- [Electrical Measurement and Electronic Instruments](../courses/sensors-instrumentation/136-108105153.md) — **必学**; IIT Kharagpur / NPTEL
- [Sensors and Sensor Circuit Design](../courses/sensors-instrumentation/138-ecea-5340.md) — **按需补充**; University of Colorado Boulder
- [Sensor Technologies: Physics, Fabrication, and Circuits](../courses/sensors-instrumentation/137-108106193.md) — **按需补充**; IISER Bhopal / NPTEL

**做到这里再往下：** 为一种传感器完成激励、调理、采样和数字输出，可使用公开或合成数据、仿真，或安全低压台面。全量程线性度、迟滞、噪声和漂移要与参考仪器或可信数据表逐项比较。没有课程权限或器材时，明确写出仿真或回放范围，不得声称完成实体实验。

### 从测量到生理信号

**为什么这样排：** 把传感器接口、原始输出和每项误差接进处理算法，同时保留校准和不确定度；预处理后的公开数据不能冒充自制前端测量。RES.6-008 提供 DSP 方法，NPTEL Biomedical Instrumentation 解释传感器、前端和临床语境，两门要结合使用。需要更深的生理信号或图像算法再读 HST.582J，但这套旧研究生材料不能代替伦理、隐私和医疗安全要求。

- [Digital Signal Processing](../courses/dsp/088-res-6-008.md) — **必学**; MIT
- [Biomedical Instrumentation](../courses/biomedical/139-102106669.md) — **必学**; IIT Madras / NPTEL
- [Biomedical Signal and Image Processing](../courses/biomedical/140-hst-582j.md) — **按需补充**; MIT

**做到这里再往下：** 只用公开或合成数据验证生理信号处理链，报告信噪比改善、伪迹抑制率和留出集误差。逐项说明隔离、隐私、伦理和“不得用于诊断”的限制，不开展任何未经批准的人体实验。
