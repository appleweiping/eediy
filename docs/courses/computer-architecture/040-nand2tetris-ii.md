---
title: "Build a Modern Computer from First Principles: From Nand to Tetris, Part II"
description: "Hebrew University of Jerusalem 的《Build a Modern Computer from First Principles: From Nand to Tetris, Part II》以六个自成体系的项目实现虚拟机、编译器与操作系统；需要入门编程能力、Python 或 Java 环境，且平台完整访问可能收费。"
page_type: course
course_id: "course-040"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 74c2fb9bdc836422 -->

# Hebrew University of Jerusalem Nand2Tetris II: Build a Modern Computer from First Principles: From Nand to Tetris, Part II

## 课程简介

- **所属大学：** Hebrew University of Jerusalem
- **课程编号：** Nand2Tetris II
- **官方先修：** 本次未核到提供方公布的硬性先修；开始前请复核课程主页
- **本站建议背景：** 数字逻辑与计算结构；编程与工程计算；入门编程能力；第一部分可配套学习，但第二部分官方说明为自成体系
- **访问条件：** 公开入口；部分材料需注册或受限
- **资料状态：** 2026-07-30；公开材料导读

### 课程定位

Nand2Tetris Part II 对应官方 [Course Page](https://www.nand2tetris.org/course) 的 Projects 7–12：2 个 VM translator 阶段、1 个 Jack app、2 个 compiler 阶段，以及 Project 12 的 Jack OS。它适合已经完成 Part I，想亲手看见高级语言怎样落到 Hack 指令的人。recursion、object state、parser、symbol table、stack frame 和 file I/O 是实际先修；进程、文件系统与网络则属于后续操作系统课程。

### 课程任务

Projects 7–8 从 arithmetic 和 memory segment 走到 branch、call/return、bootstrap 与 recursion。最容易出错的是 function frame：LCL、ARG、THIS、THAT 与 return address 的保存和恢复只要偏一格，递归程序才会暴露问题。Projects 10–11 把 tokenizer、parser、symbol table 和 VM generation 串成编译器；这一段的乐趣在于，一个 Jack 语义错误最终会变成一段可以逐层追踪的 VM 输出。

官方 [Project 12](https://www.nand2tetris.org/project12) 要用 Jack 实现 Math、String、Array、Output、Screen、Keyboard、Memory 与 Sys 共 8 个 class。Memory allocator 与 String 最能体现课程的取舍：它们足以支撑 Jack 程序，却没有 process isolation、filesystem 或 networking，因此这里的 “OS” 更像一组运行时库，而非现代 kernel。

### 课程材料

[Software](https://www.nand2tetris.org/software) 提供 browser 和 Java tools，调试时可以让官方实现暂时代替尚未完成的一层。这个设计非常适合定位问题：同一个最小 Jack program 分别经过自己的 compiler、VM translator 和 assembler，哪一次替换让错误消失，问题大致就落在哪一层。

官方 [Home](https://www.nand2tetris.org/) 免费提供 specifications 与 tools；[License](https://www.nand2tetris.org/license) 请求 solutions 保持非公开，因此 translator、compiler、OS 和 Jack app 源码适合放在 private repository。Part II 最值得抵达的时刻，是一个 Jack app 穿过 compiler、VM、assembler 和 Hack machine 正常运行，而你仍能说清 `Sys.init`、call frame、heap object 与 screen output 分别来自哪一层。

## 课程资源

- [代码 · Nand2Tetris projects and software suite](https://www.nand2tetris.org/software)
- [课程主页](https://www.coursera.org/learn/nand2tetris2)

## 资源汇总

本次核对的公开入口已全部列在上方；若你有完成记录、补充材料或失效链接，可通过页末反馈与纠错入口提交依据。
