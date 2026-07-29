---
title: "Solar Energy Engineering: Photovoltaic Energy Conversion"
description: "Delft University of Technology 的《Solar Energy Engineering: Photovoltaic Energy Conversion》通过视频、讲义、练习、实验与代码建立光伏能量转换主线；目前有匹配的 TU Delft 开放课程入口、公开视频与讲义，但 edX 审计与证书访问受限。"
page_type: course
course_id: "course-122"
editorial_status: "researched"
evidence_level: "R0"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 2400983e7a6a3424 -->

# Solar Energy Engineering: Photovoltaic Energy Conversion

## 课程简介

- **所属大学：** Delft University of Technology
- **课程编号：** PV Energy Conversion
- **先修要求：** 建议先完成方向基础：半导体器件；建议先完成方向基础：电路分析；建议先完成方向基础：工程数学
- **方向：** [储能与光伏](index.md)
- **路线角色：** 主线
- **公开材料：** 核心材料可访问
- **最近复核：** 2026-07-29

> **资料考察（R0）：** 正文于 2026-07-29 逐项核对课程官方材料，但还没有可核验的完整学习复盘，因此不冒充亲历。完成过课程的读者可以从页末提交复盘。

## 先把 solar cell、PV module 和 PV system 分开

TU Delft 的 [Photovoltaic Energy Conversion 开放页](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion/)
围绕 solar cell 展开：从太阳辐照与 photovoltaic effect，进入 semiconductor physics、
generation/recombination、受光 p-n junction、heterojunction、light management、
external quantum efficiency，最后讨论 Shockley–Queisser limit、额外损失和
third-generation concepts。官方把材料分成 Module 1–8，并标出 121 小时 study load；
这是一份提供方的课程量级说明，不是 EEDIY 对每个学习者的工时承诺。

这门课解决的是“一个 cell 为什么产生这样的 \(I\!-\!V\) 与效率”，并不完整解决
module wiring、partial shading、MPPT、inverter、battery、grid integration 或电站收益。
TU Delft 另有 [Photovoltaic Systems](https://ocw.tudelft.nl/courses/solar-energy-photovoltaic-pv-systems/)
课程，官方说明才是把 cells 连接成 modules，再把 modules 放进住宅或 utility-scale
system。若目标是系统集成，可以先用本课建立 cell model，再转入 systems 课；不要因为
课程名含 “Energy Conversion” 就把后半段系统工程想象成已经覆盖。

进入 Module 2 前，先检查 4 个动作：从 density of states 与 Fermi level 解释载流子浓度；
写出 drift、diffusion 与 continuity 的单位；画出暗态和受光 p-n junction 的 band
diagram；由 absorption coefficient 与 thickness 说明光生载流子为什么有空间分布。
卡在前 2 项时补 semiconductor physics，卡在第 3 项时补 junction electrostatics，卡在
第 4 项时补基础 optics。这个定位练习是 EEDIY 建议，不是 TU Delft 的官方先修门槛。

## 开放材料与 edX 反馈从第一天就要分流

TU Delft OCW 的 [Lectures](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion/?view=lectures)
按 8 个 module 分页保存公开视频；[Readings](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion/?view=readings)
索引则只列出 Module 1、2、6、8 的 4 个 reading 入口。不要把“有 readings”写成每个
module 都有一章完整开放教材。课程页及其材料明确采用 CC BY-NC-SA 4.0，但嵌入视频、
图片或外部材料仍要检查各自标注；可以按许可引用与改编，不能自动把第三方内容一并再分发。

edX 官方 [assignments 与 grader 访问入口](https://www.edx.org/learn/solar-energy/delft-university-of-technology-solar-energy-photovoltaic-pv-energy-conversion)
承担注册、session、讨论、graded work 与 certificate 路线，匿名页面内容会随地区、
session 和登录状态变化。本次审读没有从匿名 HTML 得到一份可长期固定的作业/考试清单，
因此不能声称 OCW 已公开 edX grader。edX 官方
[audit 说明](https://edxsupport.zendesk.com/hc/en-us/articles/1500003964681-What-is-the-audit-track)
写明：audit 若可用，访问是临时的，通常不含 graded assignments，也不提供 certificate；
并非每门课程都保证有 audit。选课当天应截图或记录实际 session、到期日和可访问项，不写
一个会迅速失效的统一价格。

因此有两条诚实的完成路线。开放路线使用 OCW 视频、4 个 readings 和自建校验，优点是
入口稳定、许可清楚，缺点是没有公开的 graded feedback。edX 路线只在账号实际显示可
加入的 session 时使用，得到哪些题、讨论或证书就记录哪些；不能把付费轨道曾经提供过的
功能写成所有地区、所有时间都存在。

## 同一个 cell 要经过三次模型升级

### 从载流子账到受光 p-n junction

Module 1–4 先把 irradiance、photon flux 与 photovoltaic effect 接到 equilibrium /
non-equilibrium semiconductor、drift-diffusion、generation/recombination 和 illuminated
p-n junction。读法不应是连续播放视频，而是维护一张 conservation sheet：光子输入、
体内 generation、bulk/surface recombination、terminal current 分别使用什么单位和
符号。每进入一个新 recombination mechanism，就重新画 minority-carrier profile，并
检查 dark limit 与 zero-generation limit 是否退回已知结果。

### 从界面与光路进入 external quantum efficiency

Module 5 处理 metal-semiconductor junction 与 heterojunction；Module 6–7 进入
refraction、dispersion、diffraction、scattering 和 external quantum efficiency。
这里最容易出现的错误不是积分算错，而是把 internal quantum efficiency、external
quantum efficiency、absorptance 和 collection probability 当成同一量。把 wavelength、
depth、absorption 和 collection 写进同一张图，再说明 reflection、parasitic absorption
与 recombination 分别从哪一项扣除；只报一个 efficiency 数字看不出模型是否守恒。

### Module 8 收到 cell efficiency，system 暂时不要越界

Module 8 的主题是 Shockley–Queisser limit、additional losses、loss reduction 与
third-generation cell concepts。到这里的产物应是 cell-level loss budget：bandgap、
radiative/non-radiative recombination、optical loss、series/shunt effect 与 operating
temperature 的角色各自可见。module mismatch、bypass diode、converter 和 grid
interaction 属于后续 PV Systems 课程；若在本课 notebook 中加入，只能标为 EEDIY
延伸，不能冒充 Module 8 的官方 assignment。

## 没有公开 grader，就让仿真留下可反驳的证据

EEDIY 建议补一份 simulation-only notebook；它不是 TU Delft lab、作业或结课项目。
先实现暗态 diode 与受光 \(I\!-\!V\)，再加入一项 recombination 与一项 optical loss，
最后对 irradiance、temperature、series resistance 和 thickness 做参数扫描。每增加
机制都保留前一模型作为 baseline，不要一步写成不可检查的“真实太阳能电池模型”。

验证不能只看曲线像不像。至少报告短路、开路与 maximum-power point 的求解方式；在
irradiance 为 0 时恢复 dark curve；在 series resistance 趋近 0、shunt resistance
增大时检查极限；对光谱积分写清 wavelength/energy 转换与单位；改变积分网格后确认
结论不依赖一个偶然步长。若使用外部 optical constants 或 EQE data，提交原始文件、
出处、许可、清洗脚本和 checksum。没有公开 dataset 时使用合成参数，并把它标为
synthetic，而不是伪装成实测。

结课目录可以按上述官方 OCW module 组织概念图、每次模型升级的推导、仿真源文件、原始
表格、环境锁定文件和一份 loss-budget 报告。edX 学习者可依照官方入口的实际可见状态，
另附 graded work 与 session 记录；开放路线不能把这些列为已完成。课程反馈最有价值的
内容，是在不复制受限题目的前提下报告 edX 地区/session/到期日变化，或指出某个 OCW
reading、video、字幕的失效位置。

## 实践止于低能量计算，不以接电站为毕业仪式

本课不要求校外学习者制作 cell、串接 module、接入 battery、inverter 或 grid。EEDIY
路线默认只做计算与仿真；半导体加工涉及化学品、真空、高温和洁净室，PV module/array
又会带来持续直流电压、故障电弧、储能和并网风险。屋顶、户外阵列、带电 DC cable、
battery pack 与 mains-connected inverter 都不属于家庭复刻范围，应留给具备合规设备、
隔离/保护、施工规程和专业监督的实验室或工程现场。

如果完成 cell loss budget 后仍主要想回答“选多大 inverter、怎样处理 shading、一天发
多少电”，就结束本课并转入 PV Systems，而不是继续给 cell model 堆系统参数。如果想研究
材料、junction、passivation、light trapping 或 efficiency limit，则保留在本课。这个
出口标准比“看完全部公开 module”更能证明方向选择正确，也不会把公开课件误当作开放实体实验。

## 课程资源

<details markdown="1">
<summary>展开完整资源索引（4 项）</summary>

### 材料覆盖

| 类型 | 完整度 |
|---|---|
| 视频 | 完整 |
| 讲义 | 完整 |
| 练习 | 部分 |
| 实验 | 部分 |
| 考试 | 无公开材料 |
| 代码 | 部分 |

### 资源

| 资源 | 访问 | 状态 | 复核日期 |
|---|---|---|---|
| [课程主页](https://www.edx.org/learn/solar-energy/delft-university-of-technology-solar-energy-photovoltaic-pv-energy-conversion) | 可免费旁听 | 官方页已列出 | 2026-07-28 |
| [备用课程入口](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion) | 无需注册公开访问 | 官方页已列出 | 2026-07-28 |
| [Course readings](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion?view=readings) | 无需注册公开访问 | 官方页已列出 | 2026-07-28 |
| [Video lectures](https://ocw.tudelft.nl/courses/solar-energy-engineering-photovoltaic-energy-conversion?view=lectures) | 无需注册公开访问 | 官方页已列出 | 2026-07-28 |

> 链接在所列日期由官方来源页发现；可访问不等于可转载。地区、账号、第三方版权和后续改版仍可能改变实际可用性。

</details>
