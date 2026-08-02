---
title: "计算机体系结构"
description: "ISA、流水线、缓存、并行与性能分析，解释数字系统如何执行真实程序。"
page_type: track
track_id: "track-computer-architecture"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 196b77a174a9effd -->

# 计算机体系结构

## 方向定位

ISA、流水线、缓存、并行与性能分析，解释数字系统如何执行真实程序。

## 建议先修方向

- [数字逻辑与计算结构](../digital-logic/index.md)
- [编程与工程计算](../programming-tools/index.md)

## CS 61C 从 C 往下追，ECE 4750 从流水线往上搭

[Berkeley CS 61C](048-cs-61c.md)把 C、RISC-V、memory hierarchy、parallelism 和项目放在软硬件接口上；[院系课程页](https://www2.eecs.berkeley.edu/Courses/CS61C/)稳定说明范围与先修要求，Fall 2024 的官方 lab/project starter 仍公开，但旧学期日历、discussion、homework、录播和评分已转入校内服务。[Cornell ECE 4750](046-ece-4750.md)更集中于 RISC-V 体系结构设计，[公开 handout 页](https://www.csl.cornell.edu/courses/ece4750/handouts.shtml)提供讲义、问题和实验描述，但团队仓库、server 与部分 starter 不匿名开放。软件背景强且尚未把程序追到硬件时选 61C；已经会 HDL、想设计 datapath 与 pipeline 时选 4750。

[MIT 6.823](047-6-823.md)是主线后的历史型高级档案，适合深入 pipeline、memory 与 parallelism。[Nand2Tetris II](040-nand2tetris-ii.md)训练 VM、compiler 和 OS 软件层，其定位在软件层级而非现代微体系结构。[6.1810](054-6-1810.md)把 RISC-V xv6 带到 page table、syscall 与 device interface，最好在理解处理器和 cache 之后进入。

两条主线的共同交底是能把一段程序解释到周期和存储访问；只会在软件端使用性能计时，或只会在 RTL 端观看波形，都还缺少另一半接口。

## 用同一条 instruction 贯穿 C、ISA 和控制信号

[数字逻辑](../digital-logic/index.md)应已覆盖 datapath、FSM、pipeline register 与 memory interface，[编程与工具](../programming-tools/index.md)应能处理 C pointer、bit operation、assembly、版本控制和自动测试。选择一段含 load、branch 和 function call 的 RISC-V 程序，逐条跟踪 register、memory、PC 与 calling convention，再把其中一条 instruction 映射到 decode、control、ALU、memory 和 writeback。

在五级 pipeline 上标出 data/control hazards，并写出 forwarding、stall 与 flush 发生的具体周期。若 C undefined behavior、stack/heap 或二进制表示含糊，回到系统编程；若 instruction 无法落到 control/data signals，回到数字逻辑。这一练习使用同一段程序，避免软件语义与硬件时序各自正确、接口处却没有人解释。

函数调用还会迫使寄存器约定、栈帧与返回地址进入轨迹；分支则把软件可见控制流和流水线清空联系起来。这两处最容易暴露抽象层之间被笔记省略的条件。

## Cache 实验要把“更快”拆成工作量、周期和时钟

可实现一个 cache simulator，或在公开 skeleton 上比较 size、associativity、block size 与 replacement policy。地址拆成 tag/index/offset，手算一段 trace 与 AMAT，再让 reference model 和 randomized tests 检查实现。性能表对同一 workload 同时给 instruction count、cycles、CPI、clock estimate、miss/stall、wall time、warm-up 和重复次数；旁边放 reference output 或功能哈希，防止错误结果因少做工作而显得更快。

一次使性能变差的优化很有价值：沿 specification→code/RTL→test→counter 解释，是 miss 降了但 critical path 增长，还是 locality 与预期相反。不同 simulator 对 cycle、cache 和 timing 的定义可能不同，统一观测口径后才比较。只换一个参数得到一条柱状图，却不说明工作量和时钟的变化，不足以形成体系结构结论。

## 6.823 与 xv6 分别把瓶颈推向硬件和操作系统

6.823 的 ISA、工具和性能案例有年代，迁移时保留原 architecture question，另行更新 simulator 和 toolchain。6.1810 的[官方 2023 档案](https://ocw.mit.edu/courses/6-1810-operating-system-engineering-fall-2023)公开 RISC-V xv6 代码和 labs，但没有完整视频与公开评分链；`xv6-labs-2023` 是仓库，`util`、`syscall` 等才是实验使用的分支，二者不能写反。外部重做只使用公开接口，并标成独立或迁移实验。

想研究 pipeline、branch prediction 与 memory consistency，沿 6.823 深入；page table、interrupt、syscall 和 device driver 成为主角时进入 xv6；compiler 或 VM 怎样生成 instruction 最有兴趣时，Nand2Tetris II 或编译器课更合适。课程代码能够启动问题，却不会替学习者定义 compiler、flags、workload、reference output 和计数口径。

## 最后的交底是一次可预测的结构修改

小核或 simulator 的 ISA/interface specification、directed/randomized tests、trace 和最小反例应能解释一次结构修改。新增一条 instruction，或改变一个 cache parameter，在动手前列出受影响的 decode、datapath、state、tests 和 counters；完成后比较预期与结果。工具环境注明 commit、compiler、flags 和运行命令，不声称通过未获得的原校 autograder。

把一次 specification change 的预测和实测放进同一张表，逐行列 decode、datapath、architectural state、tests 与 counters。第一行解释不了的结果决定后续：RTL timing/verification 回数字实现，compiler/VM 语义转软件栈，OS-boundary mismatch 进入 6.1810，pipeline/cache 行为继续高级体系结构。这张表就是交接材料；新的 benchmark 只有在能隔离那一行问题时才值得增加。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Computer Architecture](046-ece-4750.md) | Cornell University | 主课 | 公开材料导读 | 部分开放或受限 |
| [Great Ideas in Computer Architecture](048-cs-61c.md) | University of California, Berkeley | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Build a Modern Computer from First Principles: From Nand to Tetris, Part II](040-nand2tetris-ii.md) | Hebrew University of Jerusalem | 可替代 | 公开材料导读 | 有公开作业或实验 |
| [Computer System Architecture](047-6-823.md) | MIT | 可替代 | 公开材料导读 | 部分开放或受限 |
| [Operating System Engineering](054-6-1810.md) | MIT | 可替代 | 公开材料导读 | 有公开作业或实验 |
