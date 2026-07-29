---
title: "Real Analog Courses"
description: "Digilent 的《Real Analog Courses》以讲义、练习和配套仪器实验构建真实模拟电路实践链；资源可操作性强，但依赖特定 Analog Discovery 硬件。"
page_type: course
course_id: "course-027"
editorial_status: "researched"
evidence_level: "R0"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 0cd52b8e826c0714 -->

# Real Analog Courses

## 课程简介

- **所属大学：** Digilent
- **课程编号：** Real Analog
- **先修要求：** 建议先完成方向基础：电路分析
- **方向：** [电子实验与测量](index.md)
- **路线角色：** 主线
- **公开材料：** 核心材料可访问
- **最近复核：** 2026-07-29

> **资料考察（R0）：** 正文于 2026-07-29 逐项核对课程官方材料，但还没有可核验的完整学习复盘，因此不冒充亲历。完成过课程的读者可以从页末提交复盘。

## 先确认：仪器本身也属于被测系统

Real Analog 不是把示波器截图附在电路教材末尾，而是要求分析与测量互相校验。Digilent 的[当前课程资源页](https://digilent.com/shop/coursework-learning-resources/)把它列为免费模拟电子材料，并明确说课程主要按 Analog Discovery 2（AD2）编写，概念与练习兼容 Analog Discovery 3（AD3）。这句话只保证学习目标可以迁移，不保证旧讲义里的 WaveForms 按钮、量程、接线图和 AD3 当前界面逐项相同。采购前应先抽查实验 PDF，而不是仅凭“兼容”二字下单。

官方[第 1–12 章总目录](https://digilent.com/reference/_media/learn/courses/real-analog/real-analog-chapters-1-12-toc.pdf)给出的主线很清楚：第 1–5 章从电压、电流、功率和 KCL/KVL，推进到 circuit reduction、nodal/mesh analysis、network theorems 与 op-amp；第 6–9 章进入储能元件、一阶与二阶电路、state-variable methods；第 10–12 章处理 sinusoidal steady state、frequency response/filtering 与 sinusoidal power。这里的价值不是“有 12 份讲义”，而是同一套符号从静态模型走到时域、状态空间和频域，实验也随着模型变化。

## 入口诊断：先写预测，再打开 WaveForms

本页核验的官方材料没有给出一门可直接照抄的先修课程号，所以 EEDIY 不替提供方虚构 prerequisite。更实际的入口测试是：给一个含独立源和 3 个电阻的网络，先标被动符号约定，再用 KCL/KVL 或 nodal analysis 求节点电压、电流和功率；随后说明 DMM 的有限输入电阻为何会改变待测电路。若代数能算完却说不清参考地、极性和仪表加载，应从第 1 章开始；若这些动作已经稳定，可较快阅读第 1–4 章，但仍要做实验预测。

官方[Chapter 1 PDF](https://digilent.com/reference/_media/learn/courses/real-analog-chapter-1/real-analog-chapter-1.pdf)共 82 页，标题页标为 Revised 2017。它把正文、section exercises、lab projects、lab worksheets 和 Homework 放进同一个文件，而不是把实验另藏在一套不相干的手册里。第 1 章含 9 个实验编号：1.1，1.2.1，1.2.2，1.3.1，1.3.2，以及 1.4.1–1.4.4。先试做 1.1 的 breadboard/ohmmeter 与 1.2.1 的 source/meter 操作；如果断电查短路、量程选择或电流表串接仍会出错，就不要急着进入 op-amp。

## 每个实验都压成“预测—测量—残差”

原课实验的符号表会分别标出 pre-lab 分析、PSpice 或 MATLAB 数值工作、实验记录，以及需要 TA 在 notebook/grade sheet 上签字的 demo。以 1.3.2 为例，任务不是只测一个电阻值，而是从 V–I 数据做 least-squares 拟合；1.4.4 又把温敏电阻、signal conditioning 和设计判断接到同一条测量链。公开访客可以执行计算与低压接线，却拿不到课堂 TA 的观察、签字和追问，因此一张“波形看起来对”的截图不能替代原反馈。

EEDIY 建议给每个官方 Lab 留一组相互引用的记录，这是一项 EEDIY 补充，不是 Digilent 官方作业：`prediction` 写原理图、模型、单位、预期值和容许区间；`setup` 写 AD2/AD3、DMM、探头、量程、WaveForms 版本与接地点；`raw` 保存未加工导出数据；`residual` 计算实测减预测并画出残差；`correction` 记录是元件容差、仪表加载、寄生效应、接线错误还是模型边界造成差异。这个结构保留的是判断链，而不是给所有实验套一张空泛周报。

## Chapter 1 同时暴露了公开材料的长处和缺口

官方 Chapter 1 把 1.1 breadboard、1.2.2 dependent source/MOSFET、1.3.1 resistance variation、1.3.2 V–I regression、1.4.1 dusk-to-dawn light、1.4.2 power dissipation、1.4.3 input resistance 与 1.4.4 temperature measurement 串在一起。早期实验先让仪表成为被分析对象，后期才把器件和系统功能接进来。学习记录也应保持这个顺序：先证明量测链可信，再用它证明电路可信；反过来只会把 probe、ground 或 range 错误误诊为电路理论错误。

答案边界必须按当前文件本身写。82 页目录确实列出 “Exercise Solutions” 与 “Homework Solutions”，但两处都是 “Error! Bookmark not defined.”；文件正文实际在 Homework 1.16 后结束，没有随后出现的解答页，也没有公开 grader。不能因为目录出现 solution 字样，就宣称第 1 章提供完整答案闭环；也不能把提供方较早的宣传文字外推成当前 12 章每题都有可用解答。自学时先冻结首次答案，再用量纲、功率平衡、极限情形、第二种推导或 SPICE 交叉检查，并把“仍无官方判分”写在更正页上。

## Chapter 9 是从波形转入状态的关键折点

官方[Chapter 9 PDF](https://digilent.com/reference/_media/learn/courses/real-analog-chapter-9/real-analog-chapter-9.pdf)只有 26 页，却不是可以跳过的短附录。它把电路写成状态方程中的 A、b、c、d，说明如何选储能变量，并用 MATLAB Control System Toolbox 的 `ss`、`step`、`initial` 检查模型；文本也给出 Octave 替代路径。读到这里若只能套二阶响应公式、不能从 RLC 原理图写出状态变量和初值，应退回第 6–8 章补能量连续性与微分方程，而不是先复制 MATLAB 命令。

同一官方文件含 2 个实验：9.3.1 对 series RLC 建立 state-variable model，9.3.2 比较 second-order system response。合格记录至少应同时出现手工方程、参数与初值、模拟曲线、实测曲线、overlay residual 和 state trajectory；若峰值时间相近而衰减包络不合，应检查电感串联电阻和元件容差，若初始点就错，应先检查状态定义、探头参考与初始条件。把所有差异归因于“noise”会丢掉这一章最重要的模型诊断。

## 锁定 AD 硬件，也锁定 WaveForms 软件

Real Analog 的实体路线需要 AD2 或 AD3、Analog Parts Kit/等效元件与面包板，部分实验还需要 DMM；具体器件应逐项从所做 Lab 的清单核对。课程页所说的 AD3 兼容性并不会自动更新 PDF 中的旧 UI 文案，也不会证明第三方等效 parts kit 的阻值、传感器、op-amp 或 pinout 相同。仓库应保存板卡型号、序列/固件（若可取得）、元件实测值和接线照片，但不要把 Digilent PDF 重新打包进仓库：当前 Chapter 1 明示 Copyright Digilent, Inc.，公开下载不等于可重新分发。

官方[WaveForms 页面](https://digilent.com/shop/waveforms/)说明软件可免费下载和使用，也可在没有硬件时进入 demo mode；随安装提供的 SDK 含 C、Python 等示例。官方[版本页](https://digilent.com/reference/software/waveforms/waveforms-3/previous-versions)在核验时把 3.25.1 列为当前版，发布日期为 2026-03-06；Qt6 包要求 Windows 10+、macOS 12+，Linux 的基线包写 Ubuntu 22.04+，旧平台另列 Qt5 包。报告要记录实际 OS、WaveForms build 和导出格式；“软件免费”并不等于 AD 硬件、元件与 DMM 免费，demo mode 也不会生成真实电路数据。

## USB 仪器不是隔离变压器

这里应把“便携”与“浮地”分开。[AD2 Reference Manual](https://digilent.com/reference/_media/reference/test-and-measurement/analog-discovery-2/ad2_rm.pdf)直接把示波器 GND 称为 USB ground，并说明：应用若不能让二者共地，需要另行采用 USB isolation solution。因此默认应把 AD ground 视为与 USB host 共参考，不能假定 galvanic isolation，也不能把 scope ground 随意夹到浮动电源或未知节点。先断电测电源与 ground 间电阻，核对 AD 输入/输出额定、元件功耗和极性，设置限流，再上电观察供电电流。换线、换档或换元件前断电，电容确认放电后再触碰。

EEDIY 的实体复建只限与市电和其他危险外部源断开、限流、低能量的电路；不接人体、不接大功率负载，也不以 USB 连接代替安全隔离。若某项实验需要超出手边设备额定，停止实体步骤，保留分析、SPICE 与明确标注的 demo-mode 截图；这些替代能训练模型和界面，却不能写成完成了原测量。没有可靠 DMM、限流供电和清楚的 ground path 时，先借用设备比凭猜测接线更合理。

## 与 MIT 6.071J 的差别决定选哪一门

MIT 6.071J Spring 2006 的官方档案公开 25 份编号 Lab，并另有 heart-rate monitor 项目，覆盖的 electronics、signals 与 measurement 面更宽；代价是实验依赖旧 NI ELVIS、LabVIEW 和当年的 PC/PCI 环境。Real Analog 则把 12 章 Circuits 1 理论与 AD 仪器实验绑得更紧，AD2/AD3 路线通常更适合希望把 KCL/KVL、暂态、状态空间和频响串成一条便携实验链的人。

选择时不要按“哪页资源更多”判断。需要跨器件、信号和综合仪器训练，并愿意重建旧平台差异，可读 6.071J；需要一条围绕电路分析、可在同一 AD 环境反复做 predicted-versus-measured 对照的主线，优先 Real Analog。两门课都无法由仿真完全替代实体测量，也都不能在缺少原班 TA、统一硬件和课堂 checkoff 时宣称等价完成。

## 结束时交三份审查包，而不是一叠截图

官方 12 章的 exercises、Homework、Lab 与 worksheet 应按原依赖推进；EEDIY 另外选 3 个审查点来检验材料是否真的连起来，这 3 个审查点不是 Digilent 官方评分项。静态审查包用 1.3.2 与 1.4.4 展示 V–I 拟合、input loading、温度链和 residual；动态审查包用 9.3.1 与 9.3.2 展示状态方程、初值、simulation/measurement overlay 与 state trajectory；频域审查包从第 11 章选一个 filter，把手算 Bode 预期、逐点 scope 测量与 Network Analyzer sweep 放在同一坐标上。

每份审查包都应能从断电状态复建，并包含 schematic、BOM、仪器与软件版本、接线照片、原始数据、分析脚本、残差图、失败记录和更正说明。读者应能区分 original prediction、raw observation 与 post-hoc explanation；若只保留最终拟合曲线，就无法判断元数据、删点或量程是否改变了结论。实验未做、仅用 AD3 迁移、只跑 demo mode 或缺少官方答案的部分，都要在封面逐项列出。

最后可做一项 EEDIY 测量链校准与不确定度账本补充项目；它不是 Real Analog 官方 project。选一个低压 source–network–instrument chain，先用已知参考检查 offset、gain、linearity 与 repeatability，再故意改错一次 probe factor 或 range 设置，验证检查表能否在首轮读数中暴露异常。与 ground 有关的故障只在已保存数据或 SPICE 模型里离线改变参考节点，不通过危险的实体误接来制造。它把全课反复出现的预测—测量—残差压成可审阅产物，同时保持最重要的诚实边界：公开材料能复建知识与实验推理，不能复建 TA 签字、官方 grader 或课堂身份。

## 课程资源

<details markdown="1">
<summary>展开完整资源索引（1 项）</summary>

### 材料覆盖

| 类型 | 完整度 |
|---|---|
| 视频 | 部分 |
| 讲义 | 完整 |
| 练习 | 完整 |
| 实验 | 完整 |
| 考试 | 无公开材料 |
| 代码 | 部分 |

### 资源

| 资源 | 访问 | 状态 | 复核日期 |
|---|---|---|---|
| [课程主页](https://digilent.com/shop/coursework-learning-resources) | 无需注册公开访问 | 官方页已列出 | 2026-07-28 |

> 链接在所列日期由官方来源页发现；可访问不等于可转载。地区、账号、第三方版权和后续改版仍可能改变实际可用性。

</details>
