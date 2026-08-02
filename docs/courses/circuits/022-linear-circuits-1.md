---
title: "Linear Circuits 1: DC Analysis"
description: "Georgia Institute of Technology 的《Linear Circuits 1: DC Analysis》通过视频和一百余道练习强化直流电路分析；练习反馈丰富，但缺少真正的家庭实验闭环。"
page_type: course
course_id: "course-022"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 3c0e0434ba1256ce -->

# Georgia Institute of Technology: Linear Circuits 1: DC Analysis

## 课程简介

- **所属大学：** Georgia Institute of Technology
- **课程编号：** Linear Circuits 1
- **官方先修：** 本次未核到提供方公布的硬性先修；开始前请复核课程主页
- **本站建议背景：** 工程数学；物理基础
- **访问条件：** 需注册；可用范围以平台为准
- **资料状态：** 2026-07-30；公开材料导读

### 大量短题练的是方法选择

Georgia Tech 官方的 [Linear Circuits 1 课程与 assignments](https://www.coursera.org/learn/linear-circuits-dcanalysis)
是一门 7-module Coursera 课程，从电流、电压和功率讲到 KVL/KCL、node/mesh、dependent
source、Thévenin/Norton、RC/RL transient 与二阶 RLC。Georgia Tech 的
[课程说明](https://pe.gatech.edu/courses/linear-circuits-1-dc-analysis) 建议有 calculus
与 physics 背景；实际门槛是能解线性方程，并始终保持电压、电流参考方向一致。它适合需要题量
把方法练熟的人，不适合已经会分析任意拓扑、只缺实验项目的人。
官方 Coursera 页面把 graded assignments 放在 modules 内，具体访问范围随平台权限变化。

### 学习建议

打开 sample problem 的解法前暂停，标 branch direction、reference node、未知量和单位，再列方程。
同一小网络至少用 node analysis 与另一种方法各算一次，比较未知数多少和符号约定。解完用
KCL residual 与 delivered/absorbed power 双重检查。

动态电路写出 \(0^-\)、\(0^+\)、\(\infty\) 与 continuity rule 后求 time constant；二阶
电路需要判断 roots、damping 和初始储能。平台通常只收一个数，但你应保留这条推导，否则很容易
只在见过的图形上“会做”。

### 做一个低压端到端例子

选 Wheatstone sensor、RC transient 或 RLC response，手算与 SPICE 预测完成后才在隔离限流
低压下测量；保存接线、仪器设置、原始波形，并解释元件公差、source/load impedance 与 probe
loading。没有仪器时可以只做仿真，但要加入公差与源负载，不把曲线叫作测量。

学完应能为含 dependent source 的陌生网络重新建立方程，并从初值和终值推出响应。下一步可进
[Linear Circuits 2](https://www.coursera.org/learn/linear-circuits-ac-analysis) 学 phasor、
frequency response、filter 与 AC power。Coursera 的试看和 graded access 会变化，真正应
带走的是面对新拓扑时仍能选对方程与检查方式；progress bar 只说明页面走到了哪里。

## 课程资源

- [课程主页](https://www.coursera.org/learn/linear-circuits-dcanalysis)

## 资源汇总

本次核对的公开入口已全部列在上方；若你有完成记录、补充材料或失效链接，可通过页末反馈与纠错入口提交依据。
