---
title: "Introduction to Power Electronics"
description: "University of Colorado Boulder 的《Introduction to Power Electronics》通过视频、练习、仿真和代码提供电力电子入门；仿真实践有价值，但平台与评分访问可能收费或变化。"
page_type: course
course_id: "course-115"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 05e0ccf60c3f0624 -->

# University of Colorado Boulder Power Electronics 1: Introduction to Power Electronics

## 课程简介

- **所属大学：** University of Colorado Boulder
- **课程编号：** Power Electronics 1
- **官方先修：** 本次未核到提供方公布的硬性先修；开始前请复核课程主页
- **本站建议背景：** 电路分析；控制系统；电子实验与测量
- **访问条件：** 需注册；可用范围以平台为准
- **资料状态：** 2026-07-30；公开材料导读

### 课程定位

University of Colorado Boulder 的 [Introduction to Power Electronics](https://www.coursera.org/learn/power-electronics) 是 [Power Electronics 专项](https://www.coursera.org/specializations/power-electronics)的第一门。官方课程页当前列出 3 个 module、3 份作业和“1 周、每周 10 小时”，三项作业依次围绕 boost simulation、converter analysis 与 equivalent-circuit modeling；专项页则写约 12 小时。第一次自己推平均模型，留 3–4 周更从容。这门课最适合电路基础已经过关、想把 buck/boost 从开关状态推到稳态模型的人。

开课前应能用 KCL/KVL 写出理想 buck 两个区间的电感电压，再用 volt-second balance 得到转换比。若这一步只能背公式，需要补 RC/RL 暂态、功率和理想开关分析。课程会用到 LTspice，但仿真只是检验推导的工具。

### 课程结构

Chapter 1 用 buck/boost 和一次 boost 仿真说明 switched converter；Chapter 2 进入 steady state、small-ripple approximation 与 converter analysis；Chapter 3 建 averaged equivalent circuit、损耗和效率模型。做题时固定写出 switching states、周期稳态条件、平均量/纹波和假设边界。电感电流已经进入 DCM，就应回头检查 CCM，原式不再适用。

具体题面与反馈受 Coursera 登录状态影响；“Enroll for free”并不保证所有账号都能长期访问评分项，报名前应直接查看结算页。

### 作业与反馈

另建一个 12 V 到 5 V 的低功率 buck notebook：由纹波目标选 `L`、`C`，扫描 duty、负载和开关频率，再加入 ESR 与导通损耗。每张图同时给手算预期、稳态取样区间和误差。软件和现行文档从 Analog Devices 的 [LTspice 页面](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html)取得；第三方电路或排错建议仍需自己核对假设与模型。

一个够用的结课检查是：从两段状态方程推平均模型，让 LTspice 中的电流斜率、平均输出和功率收支与手算同向，并能解释启动暂态为何不受周期稳态的 volt-second balance 约束。

### 后续顺序

建议接着学 [Converter Circuits](https://www.coursera.org/learn/converter-circuits)，再学 [Converter Control](https://www.coursera.org/learn/converter-control)。本课没有 bench lab；磁性元件、栅极驱动、布局、热设计和安全测量需要另找实验训练。

## 课程资源

- [课程主页](https://www.coursera.org/learn/power-electronics)

## 资源汇总

本次核对的公开入口已全部列在上方；若你有完成记录、补充材料或失效链接，可通过页末反馈与纠错入口提交依据。
