---
title: "Digital Design and Computer Architecture"
description: "ETH Zurich 的《Digital Design and Computer Architecture》用 2025 年视频、讲义、练习与代码连接数字设计和计算机体系结构；材料较新，但托管服务器需要人工检查可访问性。"
page_type: course
course_id: "course-038"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: ecd8992656067f25 -->

# ETH Zurich DDCA: Digital Design and Computer Architecture

## 课程简介

- **所属大学：** ETH Zurich
- **课程编号：** DDCA
- **官方先修：** 本次未核到提供方公布的硬性先修；开始前请复核课程主页
- **本站建议背景：** 编程与工程计算；电路分析
- **访问条件：** 无需注册公开访问
- **资料状态：** 2026-07-30；公开材料导读

### 一门真正从门电路走到处理器的课

Onur Mutlu 的材料入口会跨年份更新；这里固定 **ETH Zürich Spring 2025**。官方
[Schedule](https://safari.ethz.ch/ddca/spring2025/doku.php?id=schedule) 从 Boolean logic、
FSM、Verilog 与 timing 走到 MIPS、single/multicycle/pipeline，再延伸到 branch prediction、
SIMD/GPU、cache、multicore 与 virtual memory。它适合想把 RTL、FPGA 和体系结构接成一条线
的人；若只想学 HDL 语法，课程后半会显得过宽。录像可从 Mutlu 的
[课程材料入口](https://people.inf.ethz.ch/omutlu/lecture-videos.html) 找到，所选录像版本要与
Spring 2025 文件保持一致。

### 课程任务

[Homeworks](https://safari.ethz.ch/ddca/spring2025/doku.php?id=homeworks) 有 6 份 optional
homework 及解答，覆盖 RTL、ISA、pipeline、memory 与 advanced architecture。“optional”只描述校园计分，
自学仍值得完成：画出完整 timing/pipeline/cache 分解，再读 solution 并重做错题。

[Labs](https://safari.ethz.ch/ddca/spring2025/doku.php?id=labs) 列出 9 个实验，从画电路、
FPGA、combinational logic、FSM、ALU 和 assembly，累积到处理器集成与 MIPS performance。
Lab 8 的两个阶段属于同一系统。每个 lab 保存 interface/bit width、RTL、self-checking
testbench、simulation transcript、synthesis/timing 与 bug log；只有板上灯亮不够。
原始 [Lab 6 bundle](https://safari.ethz.ch/ddca/spring2025/lib/exe/fetch.php?media=lab6_files.zip)
应保持不改，个人代码另行版本控制。

### 板卡状态要说准确

原课用 Vivado 与 Basys 3。没有板时可以完成 simulation 和 synthesis，但状态只能写
pre-board complete；实体 demo 还需保存 board、target part、constraints、tool version
和 timing report。遇到 latch、width truncation 或 unconstrained clock warning，要解释
它对应的设计含义；静音会把真实缺陷一起藏掉。

体系结构后半也要落到数据：对同一 instruction trace 比较 single-cycle、multicycle 和
pipeline 的 critical path/CPI；对 cache 拆 tag/index/offset 并数 hit/miss。性能结果同时
报告 clock、cycle count、instruction count、memory behavior 和 timing slack。

### 拿一条指令检查 ISA、datapath 与板上行为

[Exams](https://safari.ethz.ch/ddca/spring2025/doku.php?id=exams) 是本学期考试入口。完成题目
和 labs 后，再按页面规则做一份未看过的卷。最后任选一条 MIPS instruction，从 ISA semantics
写到 control、datapath、pipeline、memory transaction 和 FPGA-visible result，并在每层标
bit width、clock boundary 与观察点。能在内部 trace 定位错误，无需等到最终输出失败，才说明
这门课的跨层能力真正建立。若第一次出错的 cycle 来自错误状态转移，就修 RTL；若来自
negative slack 或错误约束，就回到时钟与实现，二者不能被一张板上演示混为一谈。

## 课程资源

- [课程主页](https://people.inf.ethz.ch/omutlu/lecture-videos.html)
- [代码 · DDCA Spring 2025 Lab 6 project archive](https://safari.ethz.ch/ddca/spring2025/lib/exe/fetch.php?media=lab6_files.zip)

## 资源汇总

本次核对的公开入口已全部列在上方；若你有完成记录、补充材料或失效链接，可通过页末反馈与纠错入口提交依据。
