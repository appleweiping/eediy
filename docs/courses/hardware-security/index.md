---
title: "硬件安全"
description: "侧信道、故障攻击、可信执行与安全架构，在真实处理器和可验证威胁模型上学习。"
page_type: track
track_id: "track-hardware-security"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 582e50716e02e38f -->

# 硬件安全

## 方向定位

侧信道、故障攻击、可信执行与安全架构，在真实处理器和可验证威胁模型上学习。

## 建议先修方向

- [数字逻辑与计算结构](../digital-logic/index.md)
- [计算机体系结构](../computer-architecture/index.md)

## 6.5950 的公开范围随实验条件逐项变化

[MIT 6.5950](053-6-5950.md)的[官方 Spring 2025 档案](https://ocw.mit.edu/courses/6-5950-secure-hardware-design-spring-2025)把 cache side channel、transient execution、Rowhammer、hardware-software contract、CPU fuzzing、formal verification 与 TEE 放在同一个问题下：secret 或 privilege state 怎样越过原本假定存在的边界。校外学习者可以查看[2025 lab 索引](https://shd.mit.edu/2025/labs.html)、使用[官方 starter repository](https://github.com/MATCHA-MIT/SHD-StarterCode)，并运行 Lab 0、Lab 1、Lab 7 中本地可支持的部分；Lab 2–5 依赖指定 bare-metal host 或特定 DRAM，Lab 6 依赖课程 server、专用 debug port 和 RTL environment。

repository 可见并不代表全部实验条件已经取得。每个 lab 应按实际情况区分 executed、simulated、根据 handout 推演或 inaccessible，也不能补写 Gradescope、Piazza、hidden test 与课堂反馈。这里没有可直接互换的 alternative；6.5950 主线的价值就在一门课里同时看到攻击、合同和验证。

公开 handout 能支持威胁模型和局部代码分析，专用服务器与指定硬件则决定哪些实测结论成立，两种材料需要分别陈述。

## 威胁模型要写在攻击脚本之前

[数字逻辑](../digital-logic/index.md)需要提供 synchronous RTL、reset、assertion 与 waveform reading，[计算机体系结构](../computer-architecture/index.md)需要提供 cache mapping、virtual memory、exception、privilege 与 speculative state，[编程与工程工具](../programming-tools/index.md)需要覆盖 C memory defect、sanitizer、GDB、Git 与 container。把 virtual address 拆成 page、tag、index、offset，再区分 architectural 与 microarchitectural state，并为短 SystemVerilog machine 写一条 safety property 与 counterexample。

每项练习都回答四件事：受保护的 asset、attacker capability、observable channel、被破坏的 property。只能复述 Spectre 或 Rowhammer 名称，却无法指出观测者和状态边界时，运行脚本不会增加理解。硬件安全的核心是用清楚的系统模型说明信息为何从某个边界泄漏，攻击演示只是检验方式之一。

同一现象还要区分架构可见结果与微架构残留状态，避免把时间差、缓存状态和权限检查混成一个模糊的“漏洞”标签。

## 课程实验只属于获准且与生产隔离的设备

website fingerprinting 只使用自建页面与受控标签页；cache、ASLR、Spectre、Rowhammer 或 fault 实验只在本人所有或取得书面许可、并与生产任务隔离的设备上运行。缺 compliant bare metal、vulnerable DRAM、HTCondor、Unicorn 或课程账号时，可以做 handout 推导、公开 trace、局部 Docker 结果与防御分析，但 VM substitute 仍是独立练习。

运行条件注明 Spring 2025 material version、starter commit、compiler、Yosys/Rosette/sanitizer version、设备所有权、隔离方式和停止条件。第三方设备不在 scan、降级保护或 secret recovery 的实验范围内。课程环境的缺失不能靠扩大权限弥补，安全边界本身就是这门课要学习的对象。

## 让 fuzzing 和 formal method 检查同一个自建缺陷

选择自写的小型 RISC-V 或 RTL module，在 simulation 中植入一处有说明的 arithmetic、permission 或 state-update defect。一条路径用 differential fuzzing 找到并最小化 trigger input，另一条路径用 formal assertion 生成 counterexample；修复后让两套 regression 检查同一性质，并说明仍未覆盖的状态空间。项目说明区分 MIT material、实际运行的公开部分和独立构造内容，并明确没有触碰第三方设备或真实 secret。

把最小 fuzzing input 与 formal counterexample 并排放在同一条 defensive claim 下，找出两种解释第一次分歧的 state transition。分歧落在 cache、speculation 或 TEE state 时进入 microarchitectural security；落在 assertion、model coverage 或 proof assumption 时进入 hardware formal verification；落在 C、compiler 或 OS semantics 时进入 systems security。下一门课继续使用这条 counterexample 和 property，以关闭明确的 threat-model gap，而不是继续收集攻击输出。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Secure Hardware Design](053-6-5950.md) | MIT | 主课 | 公开材料导读 | 有公开作业或实验 |
