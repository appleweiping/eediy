---
title: "Solar Energy Engineering: Photovoltaic Energy Conversion"
description: "Delft University of Technology 的《Solar Energy Engineering: Photovoltaic Energy Conversion》通过视频、讲义、练习、实验与代码建立光伏能量转换主线；目前有匹配的 TU Delft 开放课程入口、公开视频与讲义，但 edX 审计与证书访问受限。"
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 4bbbe1e3e647cba8 -->

# Solar Energy Engineering: Photovoltaic Energy Conversion

[English](../../en/courses/energy-storage-pv/122-pv-energy-conversion.md) · [← 储能与光伏](index.md)

> Delft University of Technology 的《Solar Energy Engineering: Photovoltaic Energy Conversion》通过视频、讲义、练习、实验与代码建立光伏能量转换主线；目前有匹配的 TU Delft 开放课程入口、公开视频与讲义，但 edX 审计与证书访问受限。

## 课程定位

| 属性 | 值 |
|---|---|
| **机构** | Delft University of Technology |
| **课程编号** | PV Energy Conversion |
| **方向** | [储能与光伏](index.md) |
| **评级** | A |
| **角色** | 主线 |
| **难度** | 进阶 |
| **最近复核** | 2026-07-28 |

## 为什么选择这门课

主线课程，核心内容可靠，适合按自身背景作为主课或高质量替代。

## 学习前准备

- 建议先完成方向基础：半导体器件
- 建议先完成方向基础：电路分析
- 建议先完成方向基础：工程数学

## 可验证的学习成果

- 解释储能与光伏中的核心模型，并说明主要假设与适用边界
- 独立完成代表性推导与题目，并用量纲、极限情形或数值结果交叉检查
- 完成可复现实验或实现，保留原始数据、参数、版本和验证记录

## 工时与节奏

**12 周，每周 10.5 小时。** 提供方公布 12 周、每周 10–11 小时；上方每周工时采用区间中点便于规划。先试学两周并记录授课、练习、实验和复盘时间，若实际偏差超过 25%，据实调整剩余计划。

## 软件、硬件与成本

### 软件

- 维护者建议的开源/免费验证路径：pvlib-python、PyBaMM、Python 3、Jupyter 与 pandas
- 资源清单包含公开代码覆盖；复现时固定解释器、依赖、工具链、数据集和 PDK（如适用）版本

### 硬件

- 资源清单包含实验覆盖；本课程的维护者路径明确将其限定为计算或仿真实验。只假设一台能运行上述软件并保存结果的通用计算机；不采购或连接课程指定且受保护的低压光伏/电池教学模块、温度与电流传感器、电子负载及防护容器

### 成本说明

当前维护者路径只使用计算与仿真，不设专用硬件采购；建议软件优先采用开源/免费工具。这不是提供方要求，平台访问、商业软件或云算力费用仍随提供方、地区与方案而变。

## 安全等级

**仅仿真。** 默认实践范围仅限软件、计算或仿真；不得因资源清单中的“实验”标签自行连接实体设备，任何硬件扩展都必须重新核对提供方范围并进行风险评估。

## 公开资源完整度

| 资源类型 | 完整度 |
|---|---|
| 视频 | 完整 |
| 讲义 | 完整 |
| 练习 | 部分 |
| 实验 | 部分 |
| 考试 | 无公开材料 |
| 代码 | 部分 |

## 资源与访问条件

| 资源 | 访问 | 许可 | 状态 | 复核日期 |
|---|---|---|---|---|
| [课程主页](https://www.edx.org/learn/solar-energy/delft-university-of-technology-solar-energy-photovoltaic-pv-energy-conversion) | 可免费旁听 | edX Terms of Service | 官方页已列出 | 2026-07-28 |
| [备用课程入口](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion) | 无需注册公开访问 | Provider-specific terms; verify before reuse | 官方页已列出 | 2026-07-28 |
| [Course readings](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion?view=readings) | 无需注册公开访问 | Provider-specific terms; verify before reuse | 官方页已列出 | 2026-07-28 |
| [Video lectures](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion?view=lectures) | 无需注册公开访问 | Provider-specific terms; verify before reuse | 官方页已列出 | 2026-07-28 |

> “官方页已列出”表示核验日从成功访问的官方来源页发现该链接，不保证目标文件在所有地区或账号状态下都能直接打开。访问不代表获得再分发权；下载、改编或公开发布前，应重新核对提供方页面、目标链接及其中第三方材料的许可。

## 实践闭环

### 《Solar Energy Engineering: Photovoltaic Energy Conversion · Delft University of Technology PV Energy Conversion》电池/光伏能量管理数字孪生

这是维护者为《Solar Energy Engineering: Photovoltaic Energy Conversion · Delft University of Technology PV Energy Conversion》建议的自学项目，不是课程官方作业。为储能与光伏用公开/合成数据建立电池或光伏数字孪生，评估状态估计、能量调度、温度/辐照变化和安全约束。

**来源：** 维护者建议项目

**交付物**

- 等效模型、状态/参数、功率与温度边界、调度目标和数据来源
- 模型校准、状态估计、调度、约束检查与场景仿真源文件
- 原始公开/合成曲线、拟合残差、SOC/功率轨迹和约束日志
- 一份报告，比较基线/改进策略并分析老化、遮挡或温漂失效

**验收**

- 保留数据上的电压/功率归一化 RMSE 低于 5%，或据数据噪声声明阈值
- 覆盖空/满状态边界、温度极值、功率突变和传感偏置
- 用能量积分交叉核对 SOC 或累计发电量，归一化残差低于 2%
- 注入容量衰减或局部遮挡，证明约束检查阻止越界调度

**复现要求**

- 提交模型、校准、估计、调度、场景和绘图源文件
- 固定数据版本、单位、求解器、参数、随机种子和环境
- 保存原始公开/合成数据、来源/许可、校验和与自动报告

**安全边界：** 仅仿真 — 仅使用公开/合成数据和仿真；不得充放真实电池、拆解电芯、连接光伏阵列、市电、高压或激光光源。

## 风险、缺口与边界

edX 审计路径受限，证书价格可能变化；配套开放材料采用 CC BY-NC-SA 许可。

## 完成证据

- 按周学习日志：投入时间、问题、错误订正、决策、下一步，并链接本周可复现产物
- 理论推导档案：逐项列出假设、符号、推导、单位与边界条件，并用至少一种独立方法复核
- 仿真包：模型或网表、输入、求解器与版本、参数扫描脚本、基准对照、预期结果及一条重新运行命令
- 代码仓库：固定依赖和工具链、最小运行命令、测试或波形/基准、预期输出与许可说明
