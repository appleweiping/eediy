---
title: "Real-Time Embedded Systems Theory and Analysis"
description: "University of Colorado Boulder 的《Real-Time Embedded Systems Theory and Analysis》承接实时系统实践并强化理论分析；视频、练习与考试可用，但要求完成前序课程且平台可能收费。"
page_type: course
course_id: "course-064"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 9e8afc6918a38fe1 -->

# University of Colorado Boulder Real-Time Embedded Systems 2: Real-Time Embedded Systems Theory and Analysis

## 课程简介

- **所属大学：** University of Colorado Boulder
- **课程编号：** Real-Time Embedded Systems 2
- **官方先修：** CU Boulder 将 ECEA 5316 设为序列第 2 门；它要求 ECEA 5315，并要求 C、体系结构、操作系统与 Linux
- **本站建议背景：** 本站未另设准备条件
- **访问条件：** 公开入口；部分材料需注册或受限
- **资料状态：** 2026-07-30；公开材料导读

### 5316 把调度公式和 Linux 实测对上

已经做完 5315 的 timing log、想把超时解释到调度公式，才适合 Coursera [ECEA 5316](https://www.coursera.org/learn/real-time-embedded-theory-analysis)。它是 specialization 第 2 门；[5316 官方 assignments 与 syllabus](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/curriculum/computer-engineering-embedded-systems/ecea-5316-theory-and-analysis) 还要求 C、architecture、OS 与 Linux。课程不止背 rate-monotonic utilization bound，而是手算 feasibility、生成 timing diagram，再用 POSIX service 检查模型。

所需基础是能为 periodic task 写 \(T_i,D_i,C_i\)，从 timestamp log 算 response time，并说清 sufficient bound 与 exact test 的区别。5315 日志尚不稳定时，不宜继续。

### 60% 的分数把推导、编程与互评绑在一起

官方课程页把 analysis coursework 分成 4 周，时数为 19、20、10、13，另有 2 小时 final。第 1 周推导 RM least-upper-bound、deadline-monotonic 与 exact completion test；第 2 周处理 service design、ISR synchronization 和 unbounded blocking；第 3 周比较 EDF 与 least-laxity-first；第 4 周把 memory、I/O、storage 等非 CPU 资源带回阻塞与恢复问题。

成绩由 quizzes 10%、programming assignments 与 peer reviews 合计 60%、final exam 30% 构成。这个结构意味着手算可调度还不够：课程要求把 multi-frequency executive、priority-preemptive service 或 Linux POSIX real-time thread 写出来，并让 timing diagram、实际 trace 与理论互相解释。CU 公开页没有拆出编程与互评各自在 60% 中的比例，不应自行补一个数字。

不必每周换例题。固定一组很小的 \(C,T,D\) 与 release offset，用 RM sufficient bound 和 exact test 解释 feasibility，再把 shared-resource blocking 加入 response-time analysis，最后在相同工作量上比较 EDF。相同 utilization 但不同周期关系的两组任务，往往比堆更多 service 更能显示充分条件与精确测试的区别。

### Cheddar 与 Linux 回答不同问题

Cheddar 把 period、deadline、priority、offset、execution time 与 resource protocol 变成可检查的 timeline；Linux 则暴露 scheduler、timer、cache、page fault 与 measurement overhead。两者不一致时，先找 priority convention、time unit、preemption 与 initial offset 的差异，再判断模型漏掉了什么。官方 [硬件要求](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/hardware-and-software-requirements) 以 Pi 3B+/4B 和 Raspberry Pi OS 为 starter-code 基线。

公开页不匿名提供 starter、Cheddar model、peer feedback 或 final。未注册者可做一个**非官方替代**：构造一组不可调度任务，只改变 execution budget、period 或 critical-section blocking 中的一项使它恢复，并用手算、Cheddar 与本地 C trace 解释差异。它只用于预习课程方法，不能获得官方 programming assignment 或 peer review 的身份。[Specialization](https://www.colorado.edu/ecee/real-time-embedded-systems) 的下一门 5317 才进入 fault tolerance，[访问页](https://www.colorado.edu/ali/cu-degrees-on-coursera/non-credit-courses) 则说明注册前仍需重查评测可见范围。

## 课程资源

- [课程主页](https://www.coursera.org/learn/real-time-embedded-theory-analysis)
- [ECEA 5316 课程大纲与作业概览](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/curriculum/computer-engineering-embedded-systems/ecea-5316-theory-and-analysis)
- [CU Boulder 软硬件要求说明（非公开实验）](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/hardware-and-software-requirements)

## 资源汇总

本次核对的公开入口已全部列在上方；若你有完成记录、补充材料或失效链接，可通过页末反馈与纠错入口提交依据。
