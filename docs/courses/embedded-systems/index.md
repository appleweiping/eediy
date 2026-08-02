---
title: "嵌入式系统"
description: "裸机程序、外设、实时采样、通信和系统集成，要求可重复构建的硬件项目。"
page_type: track
track_id: "track-embedded-systems"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 3704fd6fa7856636 -->

# 嵌入式系统

## 方向定位

裸机程序、外设、实时采样、通信和系统集成，要求可重复构建的硬件项目。

## 建议先修方向

- [数字逻辑与计算结构](../digital-logic/index.md)
- [编程与工程计算](../programming-tools/index.md)
- [电子实验与测量](../electronics-laboratory/index.md)

## CS 107E 解释复位到应用，EE 319K 建立 MCU 节奏

[Stanford CS 107E](058-cs-107e.md)的[当前课程站](https://cs107e.github.io/)从 RISC-V 裸机启动、内存与外设建立 computer systems。Spring 2026 notes、labs 和部分 code 较新，适合愿意追到 linker、boot flow 与 register 层的人；正式 lecture 不录制，Mango Pi kit 的地区可得性以及非公开 starter/staff repository 是实际缺口。[UT Austin EE 319K / Volume 1](059-ee-319k-volume-1.md)的[官方教材页](https://users.ece.utexas.edu/~valvano/Volume1/IntroToEmbSys)以开放文本、章节视频和活动讲 GPIO、timer、interrupt 与 sensor interface，第一次做 MCU 会更平缓。

想理解一台机器怎样从 reset 走到 application，选 CS 107E；想尽快形成可靠的 peripheral lab 节奏，选 EE 319K。MSPM0 是 EE 319K 更合适的当前版本，旧 TM4C123 与归档 edX 路线属于另一代环境。板卡、调试器和替换件在本地能否稳定取得，往往比目录上的周次更能决定实际选课。

两门课都需要真正阅读原理图和 MCU 芯片手册；一门更强调启动与系统软件，另一门更强调微控制器活动，差别不在于哪块板更流行。

## 一句 datasheet 描述要落到寄存器和引脚波形

[数字逻辑](../digital-logic/index.md)提供 register、FSM、clock/reset 与时序，[编程与工具](../programming-tools/index.md)提供 C、pointer、bit mask、link/build、Git 和 test，[电子实验](../electronics-laboratory/index.md)提供低压供电、示波器、接地和原始数据习惯。选择 timer、GPIO 或 UART 中一个 peripheral，不依赖便利库写 register-level driver，解释 memory-mapped I/O、`volatile`、read-modify-write 与 interrupt concurrency。

根据 datasheet 画预期 interrupt-latency 时间线，再用 logic analyzer 或 simulated trace 对照。pointer 和 linker map 不熟时补系统编程，clock/reset 与 FSM 含糊时补数字逻辑，GPIO voltage、pull-up、debounce 与 ground reference 说不清时回实验基础。复杂 RTOS 应在 datasheet 和裸机状态可解释之后出现，否则 API 成功只会遮住底层假设。

读写寄存器时还要说明哪些位具有写一清零、只读或保留语义，避免一次无意的读改写破坏相邻状态。中断服务与主循环共享数据时，时序和原子性也要落到具体访问上。

## 换板迁移以 clock tree、pinmux 和等价测试为核心

CS 107E 的 Mango Pi、boot flow 和 RISC-V peripheral map 要按当前 repository 与 schematic 核对；缺板时可使用 emulator 或 logic model，但只能报告 software/model result。EE 319K 的 MSPM0、TM4C123 与旧 edX materials 不共享 starter、IDE、compiler、debug probe 和 register address。迁移说明列 MCU/board revision、toolchain、headers、clock tree、pinmux、I/O voltage、programmer 和 license，并给每个 timer、GPIO 或 serial interface 一项等价测试。

第三方 driver 与 vendor example 注明来源，改名 demo 仍是外部示例。实体接口限定在安全低压；motor、relay 或较大电流负载需要 isolation、protection、supply 和 thermal calculation，并在断电状态改线。一个新板卡若改变 interrupt latency、clock accuracy 或 electrical level，测试结果应说明差异，代码重新编译成功只覆盖软件构建。

引脚复用和时钟树的默认值尤其不能照搬：外设看似没有输出时，应优先核对时钟是否开启、引脚功能是否选择正确以及逻辑电平是否匹配，再怀疑协议算法。

## 一个异常时间线比一排外设 demo 更有解释力

项目可以是 sensor→processing→output，或小型 communication node，但至少含自写 register driver、interrupt/timer、state machine/buffer 与外部可观察输出。测 interrupt latency、period jitter、buffer overflow 或 power mode，再加入 stuck sensor、delayed input、communication error 或 reset；用一条时间线说明哪个模块发现异常、哪个状态降级或清除、输出何时恢复。没有板卡时，simulator 与 mocked peripheral 可以验证软件，电气和物理时序结论则保持未验证。

选一次 abnormal run，逐项标出 source revision、build command、board revision、datasheet 条款、register transition、pin waveform 与 captured data。链条最先断开的地方决定后续：deadline 或共享资源行为进入实时系统；cache、DMA、virtual memory 或 boot 行为进入计算机体系结构；协议稳定但 datapath throughput 受限时进入 FPGA/SoC；sensor accuracy 或 calibration 问题进入仪器。换方向后重跑同一案例，让新课程解释已存在的失效，而不是另做一个亮灯演示。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Computer Systems from the Ground Up](058-cs-107e.md) | Stanford University | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Embedded Systems: Shape the World](059-ee-319k-volume-1.md) | The University of Texas at Austin | 主课 | 公开材料导读 | 部分开放或受限 |
