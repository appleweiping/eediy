---
title: "嵌入式、实时系统与板级设计"
description: "做出一台低压嵌入式设备：它能采集传感器、按时完成控制与通信任务，拥有自制 PCB、可重跑测试、故障恢复和现场演示记录。"
page_type: route
route_id: "route-embedded-maker"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: f3969bdd1cd6c22d -->

# 嵌入式、实时系统与板级设计

## 适合人群

想从数字逻辑和 C 一直做到 MCU、实时任务、PCB 与可演示设备的人

## 学完能做什么

做出一台低压嵌入式设备：它能采集传感器、按时完成控制与通信任务，拥有自制 PCB、可重跑测试、故障恢复和现场演示记录。

## 先读数据手册，再选板子

先选一个低压外设和一个失败模式，例如 I²C 温度传感器断线。用数据手册写出电压、地址、更新率、超时和恢复动作；若这五项还不清楚，先不要选 RTOS 或画 PCB。

## 围绕一个外设闭环

- 先用 Python 生成寄存器与边界输入的黄金向量，再用 C 写最小驱动；逻辑分析 trace 必须能对应数据手册中的启动、读写、超时与错误恢复。
- 裸机、MSPM0 或 Raspberry Pi 路线只选一个可取得的平台。测量最坏响应时间和 deadline miss，而不是用“看起来实时”代替时序证据。
- 只有板卡、调试器、低压限流电源、仪器、器件和预算都落实后才画自制板；否则保留可复现的外设模型、固件测试和 pre-board 接口。
- 已有 HDL、寄存器和 C 内存模型基础时跳过对应 DDCA 与入门编程章节；不要为同一个外设同时换三块开发板。

## 明确停在 pre-board，或把它做成设备

- 只做轮询设备时先跳过高级 RTOS 理论和任务关键分支；只有测到调度或恢复问题后再补。
- 无板卡时，黄金模型、固件测试、时序假设和未验证电气项全部写清，可在 pre-board 处诚实停止。
- 有实体条件时，设备在标称、边界、断线和复位场景下连续通过，逻辑 trace、deadline 统计、BOM 与演示记录能由同一版本复现。

## 怎么走

### 外设从模型到时序

**为什么这样排：** 围绕一个外设驱动学习：Python 写参考模型和测试，C 写固件，6.002 说明引脚外侧的电气限制，6.004 说明寄存器与数字时序。若 HDL、时序图或处理器数据通路仍不熟，再查 DDCA 对应章节；不必为了“读完一本书”重复已经掌握的部分。

- [Introduction to CS and Programming Using Python](../courses/programming-tools/015-6-100l.md) — **必学**; MIT
- [Practical Programming in C](../courses/programming-tools/016-6-087.md) — **必学**; MIT
- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **必学**; MIT
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **必学**; MIT
- [Digital Design and Computer Architecture](../courses/digital-logic/038-ddca.md) — **按需补充**; ETH Zurich

**做到这里再往下：** 用 C 写出驱动和寄存器级外设模型，并在主机端保留参考实现。测试覆盖每个寄存器字段、边界值、无效状态与恢复路径，随机测试保存种子和覆盖率。逻辑分析仪记录或时序仿真还要证明建立、保持时间满足数据手册。

### 裸机、RTOS 与时间

**为什么这样排：** CS 107E 用来理解裸机启动和外设，把刚写好的驱动、参考模型与随机测试直接放进固件。开始前先确认 Mango Pi、启动链和公开 starter 是否还能取得。偏向 MSPM0 外设练习时选 EE 319K；只有确有 Raspberry Pi、Linux 与 Coursera 实验权限，并且目标是调度分析时才选 RTES 1，完成后再考虑 RTES 2。没有板卡可以模拟外设，但必须列出尚未验证的电气和中断时序。

- [Computer Systems from the Ground Up](../courses/embedded-systems/058-cs-107e.md) — **必学**; Stanford University
- [Embedded Systems: Shape the World](../courses/embedded-systems/059-ee-319k-volume-1.md) — **选 1 门**; The University of Texas at Austin
- [Real-Time Embedded Systems Concepts and Practices](../courses/real-time-cps/063-real-time-embedded-systems-1.md) — **选 1 门**; University of Colorado Boulder
- [Real-Time Embedded Systems Theory and Analysis](../courses/real-time-cps/064-real-time-embedded-systems-2.md) — **按需补充**; University of Colorado Boulder

**做到这里再往下：** 做出带中断、周期任务和故障恢复的裸机或 RTOS 原型。先规定观察时长和测试负载，再报告周期数、抖动分布、观测到的最大执行时间与 CPU 占用；有限测量不能写成 WCET 证明。每次 deadline miss 都要由检测器记录并与预算对照。

### 把它做成一台设备

**为什么这样排：** 固件、timing trace、deadline detector 和故障恢复钩子都继续用于同一台设备。PCB workshop 帮你把设计送到可制造状态，ECE 4760/5730 用来完成系统集成。RTES 3 只在 Coursera 内容和指定硬件都可用时补任务关键系统与 FMEA，RTES 4 留作后续扩展。先确认低压板卡、调试器、仪器、器件和预算；缺少实体条件就停在 pre-board。

- [The Art and Science of PCB Design](../courses/pcb-eda/055-iap-pcb-2026.md) — **必学**; MIT
- [Digital Systems Design Using Microcontrollers](../courses/capstone-practice/057-ece-4760-ece-5730.md) — **必学**; Cornell University
- [Real-Time Mission-Critical Systems Design](../courses/real-time-cps/065-real-time-embedded-systems-3.md) — **按需补充**; University of Colorado Boulder
- [Real-Time Project for Embedded Systems](../courses/real-time-cps/066-real-time-embedded-systems-4.md) — **按需补充**; University of Colorado Boulder

**做到这里再往下：** 设备应包含传感、通信、自制 PCB 和固件更新路径，并记录额定值、功耗预算、看门狗或安全状态、热与过流停机条件及故障注入。测试逐项覆盖需求、接口、故障状态和更新回滚；最后在有人监看下运行预先规定的演示，包含冷启动、稳态、最慢周期任务、回滚与每类已声明故障，并记录实际时长。这只能说明原型在这些场景中的表现，不是可靠性认证。
