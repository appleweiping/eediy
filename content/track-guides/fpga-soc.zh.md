## 6.111 是默认公开档案主线，ECE 5760 是依赖板卡的当前替代

[MIT 6.111](042-6-111.md)的[官方 lab 档案](https://ocw.mit.edu/courses/6-111-introductory-digital-systems-laboratory-spring-2006/pages/labs/)公开 4 份 Verilog lab assignment 和大型 final project。板卡与 EDA flow 来自 2006 年，但公开题面、项目报告和当年的实现约束仍构成默认的可核查练习主线。[Cornell ECE 5760](052-ece-5760.md)的[Spring 2026 主页](https://people.ece.cornell.edu/land/courses/ece5760/)公开当前 lab 索引、C/Verilog/MATLAB 示例与 Quartus 工程；只有在能取得 DE1-SoC/Cyclone V、合法使用所需 Quartus 流程，并确实运行或认真迁移板卡特定项目时，它才是更强的当前替代。

两门主线按板卡、合法许可证与可下载工程择一。6.111 适合研究从 lab 逐步长成系统的历史案例；ECE 5760 更强调硬件加速、处理器接口和当前项目。把两套 project 混成一门无年份的“FPGA 大课”，会同时丢掉工具条件与题目上下文。

选择时还要看课程公开的是完整工程、题面还是项目展示；三者能支持的复现强度并不相同。

## ECE 385 和 EE 180 只能用来核对范围

[UIUC ECE 385](043-ece-385.md)的[官方课程页](https://ece.illinois.edu/academics/courses/ece385)公开 SystemVerilog/FPGA/SoC 范围与先修，不公开当前 assignments、starter、rubric、feedback 和完整 project package。本站课程页给出的 RTL 题只能称为**独立项目地图**，不能冒充 ECE 385 lab。[Stanford EE 180](045-ee-180.md)的[Winter 2026 主页](https://web.stanford.edu/class/ee180/)能看到 topic、reading 和 Homework 1–3/Lab 1–4 的发布节奏，但 assignment button、完整 handout、starter、slide、Gradescope 与 FPGA allocation 需要 SUNet/Canvas。

因此 ECE 385 是目录级课程范围，EE 180 是受限 syllabus index；它们不构成第三、第四条公开 lab sequence。比较这些页面时可以检查 coverage 与 prerequisite，不能根据标题推断已经取得可执行材料，更不能为凑课程数量补写不存在的公开考核。

目录页可以回答“这门课讲什么”，受限大纲还能回答“作业大致如何排布”，但二者都无法提供校外可运行的 starter、隐藏测试或反馈。独立练习应使用自己的题面和验收条件，并明确与原校课程的边界。

## 一个 ready/valid FIFO 足以完成第一次交底

[数字逻辑](../digital-logic/index.md)需要提供 synthesizable HDL、FSM、reset、testbench 与 timing，[计算机体系结构](../computer-architecture/index.md)需要提供 ISA/datapath、memory hierarchy、bus/peripheral 与 performance counter。实现 ready/valid FIFO 或小型 memory-mapped peripheral，使 interface、latency 与 reset semantics 能从 RTL 和 testbench 直接读出。

随机流量覆盖不同 reset 时刻、持续 backpressure、边界数据宽度及 full/empty transition。occupancy 始终等于已接受写入减读取；pointer wrap-around 后，full 与 empty 不能只看相同低位地址。assertion 可以约束 occupancy 不越界、满时不写、空时不读、transaction 成功才移动 pointer，以及同周期 enqueue/dequeue 不改变 occupancy。综合报告中的 utilization、critical path 与 unconstrained-path warning，比一条正常波形更早暴露结构缺口。

同一组随机输入最好由软件 reference queue 计算期望输出，波形只负责定位首次偏离的周期。这样可以区分协议错误、数据错误和测试平台本身的观测遗漏，也能在换 simulator 后沿用相同判据。

## 移植要比较行为，新 bitstream 只是其中一步

6.111 的旧 FPGA、ECE 5760 的 Quartus 18.1/DE1-SoC，以及 ECE 385 的 legacy VHDL/TTL 文件分属不同环境。迁移前在原 tool、board 与 IP 条件下确定一小组 reference vector、cycle-level assertion 和 software workload，再让新平台运行同一输入，比较 clock/reset、pinout、interface、latency 和 throughput。

工程说明包含 simulator、synthesis/implementation version、device part、constraints、IP license、warning policy 与 build command。PLL、memory controller 或 vendor IP 被替换后，latency、initialization-complete condition 与 reset recovery 都重新测，尤其观察 transaction 中途 reset。没有板卡时，结论止于 simulation 与 implementation report；接实体 I/O 时按 schematic 和 bank voltage 操作，断电接线，并使用限流与 level shifting。

原平台已经无法取得时，迁移基线可以来自公开 testbench 与题面明确给出的周期行为，但需说明哪些 board-level 特性没有参照。工具升级也应分两步：同一 RTL 在新工具中跑回归，再修改结构；否则 warning、推断规则和设计变化会混成一项差异。constraint 缺失或时钟未声明时，implementation 成功没有时序意义。

## SoC 项目围绕可定位的系统边界展开

可以实现 small processor + memory/peripheral，或 streaming accelerator + host interface。集成前写清 address map、data width、clock domain、latency、interrupt/handshake 与 reset contract；unit test 检查 property 和 boundary，subsystem test 注入 backpressure、reset 与 boundary address，system test 再运行固定 software workload 并与 reference model 比较。性能表同时给 clock frequency、cycle count、memory stall、host-transfer time 与 end-to-end latency。

每个模块接入系统时，都应能在该模块边界单独重放一个出错输入。software-visible mismatch 由 address、transaction 和 cycle 逐层缩小，timing closure 问题则沿 clock domain、constraint 和 routing 报告定位。bitstream 对应的 source commit、constraint 和软件输入放在同一版本记录中，板上现象才有可追溯的实现。

用追踪链中第一个无法继续缩小的 mismatch 选择下一门课。pipeline、cache 或 software-workload 语义问题进入体系结构；property、CDC、reset recovery 或 coverage 缺口进入数字验证；计算正确但 throughput/energy 受限时进入 accelerator/HLS；bank voltage、connector 或 signal integrity fault 则回 PCB 与电子实验。先在新边界重现同一 mismatch，再决定是否扩大 SoC 规模。
