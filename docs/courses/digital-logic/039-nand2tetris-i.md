---
title: "Build a Modern Computer from First Principles: From Nand to Tetris, Part I"
description: "Hebrew University of Jerusalem 的《Build a Modern Computer from First Principles: From Nand to Tetris, Part I》以自包含 HDL 模拟器和逐级项目训练数字逻辑；项目链完整，但平台访问条款可能变化。"
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 9ee2c95aacb3aa0a -->

# Build a Modern Computer from First Principles: From Nand to Tetris, Part I

[English](../../en/courses/digital-logic/039-nand2tetris-i.md) · [← 数字逻辑与计算结构](index.md)

> Hebrew University of Jerusalem 的《Build a Modern Computer from First Principles: From Nand to Tetris, Part I》以自包含 HDL 模拟器和逐级项目训练数字逻辑；项目链完整，但平台访问条款可能变化。

## 课程定位

| 属性 | 值 |
|---|---|
| **机构** | Hebrew University of Jerusalem |
| **课程编号** | Nand2Tetris I |
| **方向** | [数字逻辑与计算结构](index.md) |
| **评级** | S |
| **角色** | 替代 |
| **难度** | 提供方未标准化（请按先修判断） |
| **最近复核** | 2026-07-28 |

## 为什么选择这门课

替代课程，资源完整、教学设计清晰，适合作为该方向的优先选择。（审阅记录：S content / A access）

## 学习前准备

- 建议先完成方向基础：编程与工程计算
- 建议先完成方向基础：电路分析

## 可验证的学习成果

- 解释数字逻辑与计算结构中的核心模型，并说明主要假设与适用边界
- 独立完成代表性推导与题目，并用量纲、极限情形或数值结果交叉检查
- 完成可复现实验或实现，保留原始数据、参数、版本和验证记录

## 工时与节奏

**11 周，每周 9 小时。** 这是维护者规划估计，依据课程角色与公开练习、实验密度生成，不是提供方工时承诺。先试学两周，分别记录授课、练习、实验和复盘时间；若实际偏差超过 25%，据实调整剩余计划。

## 软件、硬件与成本

### 软件

- 维护者建议的开源/免费验证路径：Logisim Evolution、Icarus Verilog 或 Verilator，以及 GTKWave
- 资源清单包含公开代码覆盖；复现时固定解释器、依赖、工具链、数据集和 PDK（如适用）版本

### 硬件

- 资源清单包含实验覆盖；本课程的维护者路径明确将其限定为计算或仿真实验。只假设一台能运行上述软件并保存结果的通用计算机；不采购或连接课程明确指定的逻辑实验板、USB 编程器和逻辑分析仪

### 成本说明

当前维护者路径只使用计算与仿真，不设专用硬件采购；建议软件优先采用开源/免费工具。这不是提供方要求，平台访问、商业软件或云算力费用仍随提供方、地区与方案而变。

## 安全等级

**仅仿真。** 默认实践范围仅限软件、计算或仿真；不得因资源清单中的“实验”标签自行连接实体设备，任何硬件扩展都必须重新核对提供方范围并进行风险评估。

## 公开资源完整度

| 资源类型 | 完整度 |
|---|---|
| 视频 | 完整 |
| 讲义 | 部分 |
| 练习 | 完整 |
| 实验 | 完整 |
| 考试 | 无公开材料 |
| 代码 | 完整 |

## 资源与访问条件

| 资源 | 访问 | 许可 | 状态 | 复核日期 |
|---|---|---|---|---|
| [课程主页](https://www.coursera.org/learn/build-a-computer) | 注册后访问 | Coursera Terms of Use | 官方页已列出 | 2026-07-28 |
| [Build a Modern Computer from First Principles: Nand to Tetris Part II (project-centered course)](https://www.coursera.org/learn/nand2tetris2) | 注册后访问 | Coursera Terms of Use | 官方页已列出 | 2026-07-28 |

> “官方页已列出”表示核验日从成功访问的官方来源页发现该链接，不保证目标文件在所有地区或账号状态下都能直接打开。访问不代表获得再分发权；下载、改编或公开发布前，应重新核对提供方页面、目标链接及其中第三方材料的许可。

## 实践闭环

### 《Build a Modern Computer from First Principles: From Nand to Tetris, Part I · Hebrew University of Jerusalem Nand2Tetris I》带形式化检查的流式数字单元

这是维护者为《Build a Modern Computer from First Principles: From Nand to Tetris, Part I · Hebrew University of Jerusalem Nand2Tetris I》建议的自学项目，不是课程官方作业。为数字逻辑与计算结构实现一个带握手的参数化流式运算单元，用 RTL 仿真、断言和随机测试验证功能、时序协议与复位边界。

**来源：** 维护者建议项目

**交付物**

- 接口时序图、位宽/溢出策略、状态机和延迟规格
- 可综合 RTL、参考模型、测试平台和协议断言源文件
- 至少 10000 个随机事务的种子、原始日志、覆盖率和波形
- 一份验证报告，列出吞吐/延迟、覆盖空洞和一个已修复反例

**验收**

- 10000 个随机事务与软件参考逐位一致，断言零失败
- 覆盖最小/最大操作数、连续 backpressure、复位中断和计数回绕
- 用穷举检查所有 8 位配置，或对更大位宽运行等价/形式化性质
- 注入一处 off-by-one 或握手缺陷，证明测试能稳定复现并定位

**复现要求**

- 提交 RTL、参考模型、断言、测试和波形查看说明
- 固定模拟器/综合器版本、随机种子、参数和单命令回归入口
- 保存原始回归日志、覆盖数据库摘要和自动生成报告

**安全边界：** 仅仿真 — 默认仅做 RTL 仿真与综合报告；不要把未经时钟、复位和接口验证的设计下载到实体系统。

## 风险、缺口与边界

HDL 模拟器和项目可自包含完成，但 Coursera 的试用、付费及完整课程访问条款可能变化。

## 完成证据

- 按周学习日志：投入时间、问题、错误订正、决策、下一步，并链接本周可复现产物
- 设计审查包：需求与约束、方案权衡、可编辑源文件、适用的 ERC/DRC/时序/稳定性检查、导出物与复现实验
- 代码仓库：固定依赖和工具链、最小运行命令、测试或波形/基准、预期输出与许可说明
- 仿真包：模型或网表、输入、求解器与版本、参数扫描脚本、基准对照、预期结果及一条重新运行命令
