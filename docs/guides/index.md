---
title: 实践指南
description: 将电子工程课程知识转化为可执行、可验证、可复现的工程能力。
---

<div class="ee-language" markdown>
[English version](../en/guides/index.md)
</div>

# 实践指南

这些指南解决“学完课程后如何真正做出来”。每页都给出最小环境、学习顺序、验证任务、排查方法、证据清单、成本与许可、无障碍要求以及安全停止边界。先选择与你当前项目直接相关的一页，不必一次安装全部工具。

## 建议使用方法

1. 阅读[实验安全](safety.md)，确定工作属于纯软件、受限低能量还是必须受监督的等级。
2. 用[工具与环境](tools.md)选择最小工具链，不因工具数量分散学习目标。
3. 从下列主题选一项，先写预测、验收条件和停止条件。
4. 完成页面中的验证任务，并保存可由他人审阅的证据。
5. 用[项目实践](projects.md)把多个微任务组合成作品集项目。
6. 用[可复现工程](reproducibility.md)从干净环境重建，未通过就不视为完成。

## 工程基础

- [版本控制与工程协作](version-control.md)：原子提交、分支实验、标签与敏感信息边界。
- [Python、Jupyter 与工程计算](python-jupyter.md)：单位、数据、测试与无状态重跑。
- [C、构建系统与硬件邻近编程](c-cmake.md)：表示、内存、分层和主机测试。
- [数值计算与模型验证](numerical-computing.md)：尺度、收敛、敏感度与独立基准。
- [可复现工程与自动验证](reproducibility.md)：锁定环境、统一入口和证据清单。

## 电路、硬件与数字系统

- [SPICE 电路仿真](spice-simulation.md)：工作点、AC/瞬态、模型和容差分析。
- [PCB 与 KiCad 工作流](pcb-kicad.md)：需求、封装、规则、制造输出和受控上电。
- [HDL、仿真与 FPGA](hdl-fpga.md)：自检查测试、综合、约束和时序证据。
- [嵌入式工具链与板级调试](embedded-toolchains.md)：可恢复烧录、外设分层与故障路径。
- [仪器、测量与不确定度](instrumentation-measurement.md)：量程、带宽、探头、校准与不确定度。

## 研究、记录与表达

- [数据与实验记录](data-lab-notebooks.md)：运行标识、只读原始层、元数据和处理追踪。
- [文献检索与证据评估](literature-research.md)：问题拆解、来源分层、反例和证据矩阵。
- [技术写作与设计评审](technical-writing.md)：需求、结论、图表、决策和同行复现。

## 跨主题指南

- [工具与环境](tools.md)：软件、仪器、文件、单位和低带宽替代路径。
- [实验安全](safety.md)：风险分级、停止条件、监督范围和事故响应。
- [项目实践](projects.md)：从学习目标到项目范围、里程碑、验收与作品集证据。

## 三条推荐实践链

### 软件与信号分析

[Python/Jupyter](python-jupyter.md) → [数值验证](numerical-computing.md) → [数据记录](data-lab-notebooks.md) → [技术写作](technical-writing.md) → [可复现工程](reproducibility.md)

适合信号处理、控制、通信和公开数据项目。最终证据应包含原始数据、带测试脚本、单位明确的图表和干净重建日志。

### 电路与 PCB

[SPICE](spice-simulation.md) → [PCB](pcb-kicad.md) → [仪器测量](instrumentation-measurement.md) → [数据记录](data-lab-notebooks.md) → [项目实践](projects.md)

初学时限定为纯仿真或受限低能量设计。任何较高能量、储能、激光、功率射频或人体连接工作都必须转入合格设施与监督。

### 数字硬件与嵌入式

[C 与构建](c-cmake.md) → [HDL/FPGA](hdl-fpga.md) 或 [嵌入式工具链](embedded-toolchains.md) → [版本控制](version-control.md) → [可复现工程](reproducibility.md)

把主机测试、自动仿真、可恢复烧录、板级日志和时序报告作为同一证据链，而不是只展示最终演示视频。

## 完成标准

完成一篇指南意味着你能提交可复查的结果，而非只读完页面。至少应有：事前预测、明确验收、故障注入或边界测试、原始输入、自动化步骤、结果解释、安全审查和一份别人能按说明重放的证据包。
