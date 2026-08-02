---
title: "数字系统、FPGA 与体系结构"
description: "实现一个流水线处理器或自定义加速器，用参考模型和回归测试验证，并让软件在 FPGA 或固定器件的可复现仿真中运行。"
page_type: route
route_id: "route-digital-fpga-architecture"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 8e7c7b9a0a16b583 -->

# 数字系统、FPGA 与体系结构

## 适合人群

想从逻辑门和 RTL 走到 FPGA、流水线处理器、加速器与 SoC 的硬件学习者

## 学完能做什么

实现一个流水线处理器或自定义加速器，用参考模型和回归测试验证，并让软件在 FPGA 或固定器件的可复现仿真中运行。

## 先分清硬件出口和软件出口

先判断出口是硬件还是软件。想从门电路得到 Hack 计算机，走 Nand2Tetris I；已有等价数据通路、只想做 assembler、VM 与 compiler，走 Part II。Part II 的软件栈不能当作 FPGA/RTL 已完成的证据。

## Nand2Tetris 只走完一条分支

- 两条 Nand2Tetris 分支只走一条，并使用各自的测试：硬件分支验证芯片、CPU、内存和整机；软件分支验证 assembler、VM translator、Jack compiler 与 OS 模块。
- 不要同时浅尝 Nand2Tetris I 与 II，也不要公开提供方要求保持私有的答案代码；作品集可以解释测试方法和结果。

## 用 RTL、约束和回归赢得 FPGA 声明

- 进入 FPGA 阶段前必须有可综合 RTL、self-checking testbench、固定器件与时序约束。只有 Part II 产物时，先补一个独立 RTL 模块，不能把 compiler 测试移作硬件验收。
- 体系结构阶段沿用同一参考解释器和 workload，分别报告控制流、访存与计算瓶颈；板卡不可得时保留固定器件的综合与静态时序结果。
- 没有目标板、EDA 许可证或完整 starter 时，跳过依赖该环境的分支；不要用课程概览或截图代替综合、时序和回归。

## 软件栈和硬件主线各有自己的终点

- Part II 分支在软件工具链通过其官方测试时可以单独结束，但只能称为软件栈完成；要继续 FPGA，仍需另有可综合 RTL 与硬件测试。
- 硬件主线在参考输出零失配、无未解释 X/Z、固定器件时序收敛且性能数据可重跑时结束；有板才增加实机声明。

!!! warning "开始前请确认这些课程的材料限制"
    - [Digital Systems Laboratory](../courses/fpga-soc/043-ece-385.md)：当前院系页、课程目录和 Course Explorer 没有公开 assignment、starter、rubric、staff feedback 或完整工程包；任何自建 RTL/FPGA 练习都必须标为独立项目，不能冒充 ECE 385 官方实验。 最近核对：2026-07-30。
    - [Digital Systems Architecture](../courses/fpga-soc/045-ee-180.md)：完整 handout、starter、slides、答案、Gradescope、FPGA allocation 与教学反馈需要 SUNet 或 Canvas；公开页不是可独立执行的讲义、作业和实验包，只能作为受限大纲索引。 最近核对：2026-07-31。

## 怎么走

### 从逻辑门到可运行计算机

**为什么这样排：** 6.004 负责数字抽象和处理器边界。第一次从门电路搭整机就选 Nand2Tetris I；若已有等价数据通路，目标转向 assembler、VM 和 compiler，才选 Part II。两条路只走一条，不必各看一点。Nand2Tetris 的实现按官方要求保持私有，公开作品集可以展示测试方法，但不能公开答案代码。

- [Computation Structures](../courses/digital-logic/037-6-004.md) — **必学**; MIT

**完整路线 — Nand2Tetris I 硬件计算机（按列出顺序学习）**

1. [Build a Modern Computer from First Principles: From Nand to Tetris, Part I](../courses/digital-logic/039-nand2tetris-i.md) — **路线内课程**; Hebrew University of Jerusalem

**这条分支做到哪里：** HDL 芯片、CPU、内存与 Hack 计算机分别通过对应测试，最终系统能运行目标机器代码；这份产物可以接入后面的 RTL/FPGA 阶段。

**完整路线 — Nand2Tetris II 软件工具链（按列出顺序学习）**

1. [Build a Modern Computer from First Principles: From Nand to Tetris, Part II](../courses/computer-architecture/040-nand2tetris-ii.md) — **路线内课程**; Hebrew University of Jerusalem

**这条分支做到哪里：** assembler、VM translator、Jack compiler 与所做 OS 模块通过各自测试；这里只验收软件栈，不声称实现了门电路、RTL 或 FPGA。

**做到这里再往下：** 按所选分支使用上面的独立停止条件。只有硬件分支或另行完成的等价 RTL 能直接进入 FPGA；软件分支可以在这里结束，或先补硬件产物再继续。

### RTL 在 FPGA 上站稳

**为什么这样排：** 以 6.111 的 FPGA 项目组织方式为参考，优先继续使用前面的 datapath、参考解释器和随机指令测试；换成别的 RTL 模块也保留同一个 self-checking harness。分支由实际条件决定：有 Illinois 环境选 ECE 385，想走 ASIC 综合选 EECS 151，想加强体系结构 RTL 选 EE 180。先核对板卡、EDA 许可和作业访问，缺哪一项就及时换路。

- [Introductory Digital Systems Laboratory](../courses/fpga-soc/042-6-111.md) — **必学**; MIT
- [Digital Systems Laboratory](../courses/fpga-soc/043-ece-385.md) — **选 1 门**; University of Illinois Urbana-Champaign; **材料限制待确认**
- [Digital Design and Integrated Circuits](../courses/vlsi-ic/044-eecs-151.md) — **选 1 门**; University of California, Berkeley
- [Digital Systems Architecture](../courses/fpga-soc/045-ee-180.md) — **选 1 门**; Stanford University; **材料限制待确认**

**做到这里再往下：** 含跨时钟域接口的 RTL 模块要完成自检仿真、lint、约束、综合和静态时序，目标时钟下最差裕量不得为负。有匹配板卡时再部署，并让板上输出逐项对齐黄金向量；没有板卡就标为 pre-board，给出固定器件型号的实现结果，不得虚构硬件运行。

### 流水线、加速器与 SoC

**为什么这样排：** ECE 4750 用来学习流水线与性能评测，6.5950 用来梳理资产、攻击入口和信任边界；直接从上一段的 RTL、约束、回归和软件 workload 继续。ECE 4750 的团队仓库、服务器和部分 starter 不公开，因此要为公开材料自建可重跑测试，不能声称通过 Cornell lab 或 autograder。最后按短板选 6.823、CS 61C，或只在 DE1-SoC 与 Quartus 可用时选 ECE 5760，不必三门都浅尝。

- [Computer Architecture](../courses/computer-architecture/046-ece-4750.md) — **必学**; Cornell University
- [Computer System Architecture](../courses/computer-architecture/047-6-823.md) — **选 1 门**; MIT
- [Great Ideas in Computer Architecture](../courses/computer-architecture/048-cs-61c.md) — **选 1 门**; University of California, Berkeley
- [Hardware Acceleration via FPGA](../courses/fpga-soc/052-ece-5760.md) — **选 1 门**; Cornell University
- [Secure Hardware Design](../courses/hardware-security/053-6-5950.md) — **必学**; MIT

**做到这里再往下：** 实现流水线处理器或自定义加速器，基准集要能分别暴露控制流、访存和计算瓶颈，输出与软件参考结果零差异。分别报告各类负载的吞吐量、面积和功耗估计，再按列出的资产、入口和信任边界说明威胁与缓解方法。
