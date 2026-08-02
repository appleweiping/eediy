---
title: "RF and Millimeter-Wave Circuit Design"
description: "Eindhoven University of Technology 的《RF and Millimeter-Wave Circuit Design》在 Coursera 内使用 Qucs-S 与 Octave 仿真材料讲授射频毫米波电路；公开页没有固定课程工程包。"
page_type: course
course_id: "course-111"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-29"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 0452d555905a125c -->

# Eindhoven University of Technology: RF and Millimeter-Wave Circuit Design

## 课程简介

- **所属大学：** Eindhoven University of Technology
- **课程编号：** RF and Millimeter-Wave Circuit Design
- **官方先修：** 本次未核到提供方公布的硬性先修；开始前请复核课程主页
- **本站建议背景：** 电磁场与波；电路分析；通信系统
- **访问条件：** 需注册；可用范围以平台为准
- **资料状态：** 2026-07-29；公开材料导读

### 把课程读成 5 次相互衔接的 RF 设计推进

TU/e 的 [RF and millimeter-Wave Circuit Design](https://www.coursera.org/learn/rf-mmwave-circuit-design)
在 2026-07-29 页面列出 6 modules、19 assignments，以及 5 个互评 design labs：
system、LNA/PA、mixer、VCO、synthesizer。提供方称约 70% 可仿真、30% 需要 lab/components。
它适合已经会 link budget、S-parameter、noise cascade 与 frequency planning，想把 block
specification 追到电路取舍的人；低频 small-signal gain 仍是主要工具时，需要补 microwave
network 与 RF systems。

### 五个模块各自排除一种 RF 设计错误

system 阶段从 range、bandwidth、sensitivity 和 selectivity 推 block specs；amplifier
分清 LNA noise/matching/stability 与 PA compression/efficiency；mixer 保存 wanted/image/
spur frequency table；VCO 同时看 startup、tuning、phase noise 与 load pulling；synthesizer
解释 loop type/bandwidth、reference/divider noise 和 lock behavior。每一轮都把 specification、
schematic/model、pass/fail plot、corner/sensitivity 与被否决方案放在一起比较，不用 nominal
gain 替代稳定性或系统预算。

### 工具版本会改变仿真答案

课程介绍 Qucs-S 与 Octave，却未在公开页固定 release。
[Qucs-S repository](https://github.com/ra3xdh/qucs_s) 和
[installation guide](https://qucs-s-help.readthedocs.io/en/latest/installation/installing-qucs-s.html)
显示不同 OS/backend 组合会变化；[Octave download](https://octave.org/download.html) 也只代表
当前可选环境。每次仿真都写明 OS、Qucs-S、backend、Octave、device model 与 hash；
换 simulator 时用同一 netlist 重跑 baseline，并先解释 parser、model 或 convergence 差异。

### 默认交 simulation-only 系统闭环

70/30 是课程构成说明，不是家庭 RF 安全结论。无机构批准实验室时，不连接 PA、antenna、
来源或状态不明的 VNA/source，也不做自由空间发射；TU/e 的
[remote RF laboratory](https://research.tue.nl/en/publications/rf-circuits-laboratory-for-remote-learning-and-massive-open-onlin/)
是专门的受控设施，不等于家庭台架许可。

有平台权限时，19 assignments、5 个互评任务和 peer feedback 构成原课程路线；没有权限时，
locked prompt、supporting files 与 solution 都不在材料范围内，下面只搭一个独立
clean-room model。让 idealized LNA、mixer、VCO、divider/phase detector 共用同一份
transceiver link budget，每轮把系统指标分到当前模块，再把超出的 noise、linearity 或 lock
要求退回预算表。

最后只看一台 transceiver：同一组 frequency plan、impedance 和 power assumptions 是否贯穿
五个模块？如果 LNA gain 的提高迫使 mixer compression、VCO phase noise 或 synthesizer
lock time 付出更大代价，就撤回这个局部最优。RF 设计的难点正是让五张各自漂亮的曲线描述同一
台机器。

## 课程资源

- [课程主页](https://www.coursera.org/learn/rf-mmwave-circuit-design)

## 资源汇总

本次核对的公开入口已全部列在上方；若你有完成记录、补充材料或失效链接，可通过页末反馈与纠错入口提交依据。
