---
title: "Linear Circuits 2: AC Analysis"
description: "Georgia Institute of Technology 的《Linear Circuits 2: AC Analysis》承接直流分析并训练交流电路方法；视频、45 项作业与实验演示可用，但没有完整搭建循环。"
page_type: course
course_id: "course-023"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: ed52f562ac8a8d44 -->

# Georgia Institute of Technology: Linear Circuits 2: AC Analysis

## 课程简介

- **所属大学：** Georgia Institute of Technology
- **课程编号：** Linear Circuits 2
- **官方先修：** 本次未核到提供方公布的硬性先修；开始前请复核课程主页
- **本站建议背景：** 工程数学；物理基础；直流电路分析或同等基础；第一门课程可作为配套，但不是不可替代的硬先修
- **访问条件：** 需注册；可用范围以平台为准
- **资料状态：** 2026-07-30；公开材料导读

### 这门课从相量开始

Georgia Tech 官方的 [Linear Circuits 2 课程与 assignments](https://www.coursera.org/learn/linear-circuits-ac-analysis)
有 5 个 modules，主线是 sinusoid/phasor、frequency response、filter、complex power
和 transformer。它不会重教 KVL/KCL、node/mesh、Thévenin/Norton 或一阶 transient；
这些由前一门 [Linear Circuits 1](https://www.coursera.org/learn/linear-circuits-dcanalysis)
覆盖。可拿串联 RLC 检查准备程度：从时域关系转到 impedance，求电流相量，再还原 amplitude
与 phase，并解释频率变化时谁主导。若只能算复数却说不清超前/滞后，复数几何和储能元件就是当前缺口。
官方 Coursera 页面中的 graded exercises 会受当期登录与访问权限影响。

### 每次计算都要回到波形

从 \(v(t)\) 得到 phasor 后，一定再还原时域；从 transfer function 画 Bode asymptote 后，
选几个频点做精确计算。AC power 要声明 phasor 是 peak 还是 RMS，区分 W、var、VA；
maximum power transfer 与 maximum efficiency 回答的是两个不同问题。transformer 则要确定 dot
convention 和 reference direction，再反射 impedance。

filter 设计不能只算 cutoff。写出 passband、stopband、source/load、元件系列和 tolerance，
再考虑 op-amp gain-bandwidth、slew rate、output swing 与 probe loading 怎样移动原来的
poles/zeros。

画图前写下低频、高频和 resonance 附近的趋势预测；如果精确曲线违反这些极限，优先检查 phasor
约定、传递函数归一化与测量负载。修改坐标范围只会把异常藏起来。

### 用传感器滤波器检查相量、频响和波形

课程演示 guitar filtering、RLC 与 sensors，但 Georgia Tech 校内
[ECE 3710 说明](https://pe.gatech.edu/sites/default/files/agendas/ECE-3710-Circuits%20and%20Electronics.pdf)
中的 myDAQ 实验属于校内配置，MOOC 页面并未公开对应的 lab 包。自学可为窄带传感器设计 filter：从 spectrum
写规格，推导 transfer function，做 SPICE magnitude/phase sweep，再低压测几个关键频点。
没有硬件时做 tolerance sweep，并明确是仿真。最后若能预测新网络的数量级、相位方向和频率
极限，再用复数计算验证，相量才真正成了工程工具。

## 课程资源

- [课程主页](https://www.coursera.org/learn/linear-circuits-ac-analysis)

## 资源汇总

本次核对的公开入口已全部列在上方；若你有完成记录、补充材料或失效链接，可通过页末反馈与纠错入口提交依据。
