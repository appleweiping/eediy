---
title: HDL、仿真与 FPGA
description: 用双模拟器、自检查 FIFO、通过的形式化结果、故意破坏版本的反例和完整时序约束建立可移植 RTL 工作流。
page_type: guide
comments: true
---

# HDL、仿真与 FPGA

本页围绕一个同步 FIFO 展开，并保留两个修订。`baseline` 的自检查测试和所声明的形式化 property 均应通过；`fault/read-pointer` 故意破坏读指针更新，用来确认测试和 property 确实能抓住错误。找到最短失败 seed 或 counterexample 后，再让修复后的 `baseline` 通过同一组检查。反例属于被破坏的修订，不是正确设计的交付要求。

仓库里的[同步 FIFO 验证 starter](https://github.com/appleweiping/eediy/tree/main/examples/sync-fifo)实现了下面这条链。在仓库根目录执行 `python examples/sync-fifo/run_checks.py`：已安装的 Icarus、Verilator、SymbiYosys/Z3 与 Yosys 会真实运行，缺失工具则明确打印 `CHECK_SKIP`；发布环境改用同一命令的 `--require-tools all` 形式，缺工具即失败。baseline 与读指针故障共用 testbench 和 formal reference model，故障构建必须非零退出并由 SBY 生成 counterexample；仓库不提交预制 PASS 日志。

| 修订 | 预期证据 | 不能接受的替代品 |
| --- | --- | --- |
| `baseline` | 两种模拟器的自检查 PASS；记录 assumption、mode、depth 的 formal PASS | 只有波形截图或一句“仿真正常” |
| `fault/read-pointer` | 自动测试失败；保存失败 cycle、seed 和 formal counterexample | 手工看波形后口头指出“这里像是错了” |
| 修复提交 | 同一失败输入转为 PASS，其他回归仍通过 | 删除触发用例或放宽 property |

这个 FIFO 随后经过仿真、形式验证、综合、CDC/时序和上板检查。每一步回答的问题不同；bitstream 能生成，不能替代前面的验证。

## 同一接口在 Icarus 与 Verilator 中运行

[Icarus Verilog 的入门文档](https://steveicarus.github.io/iverilog/usage/getting_started.html)把 `iverilog` 编译与 `vvp` 运行分开，并说明 `-c` file list 和 `-s` top module 对多文件工程的重要性。固定语言标准、top 和 file order，例如让脚本执行 `iverilog -g2012 -s fifo_tb -o build/fifo.vvp -c rtl.f`，再用 `vvp build/fifo.vvp` 运行编译产物；不依赖 shell glob 的偶然顺序，也不让多个未实例化 module 同时成为 root。

[Verilator 的官方概览](https://verilator.org/guide/latest/overview.html)强调它把 Verilog/SystemVerilog 编译成 C++ 或 SystemC model，并非传统事件模拟器。先用 lint 处理 width、signedness、unreachable code、latch 和 multiple-driver 提示，再让同一组 vector/reference model 通过 Verilator 与 Icarus。两者结果不同时，先缩小到最短 source list 和第一个分歧 cycle，检查 language extension、未初始化值、race、delay construct 与 simulator-specific behavior；不要用 `ifdef` 分别哄过两个工具。

测试结果必须由 scoreboard 或 assertion 自动判定，waveform 只用于解释失败。每次随机运行保存 seed，并在发现错误后保留最短输入序列；CI 的 stdout 应给出 testcase、cycle、expected/actual 和失败信号，即使没有 GUI 也能定位。

## 故意破坏一次，确认测试真的会失败

先实现 synchronous ready/valid FIFO，明确 depth、width、full/empty、同周期读写、reset 后输出以及非法请求的处理。reference queue 覆盖 empty→write→read、full 边界、wrap-around、持续 backpressure 与 reset 插入；若暂不支持非 2 次幂 depth，就在 elaboration 时拒绝，而不是让 pointer silently overflow。在独立的故障修订中改坏 read pointer 或 count，确认测试确实会失败；保存反例后回到正确修订，让同一测试和 property PASS。没有负向控制的“全部通过”信息量很低。

[SymbiYosys 的 FIFO quickstart](https://yosyshq.readthedocs.io/projects/sby/en/stable/quickstart.html)展示了 count、pointer difference、overflow/underflow property，以及失败时生成 counterexample trace 的完整路径。为自己的 FIFO 写 safety assertions：occupancy 不越界、accepted write/read 改变 count 的规则、读出顺序与 reset state；再写 cover 证明 empty、full 和 simultaneous read/write 可达。bounded proof 只覆盖配置中给定的时间深度，unbounded proof 也依赖环境 assumption；把 solver、mode、depth 和 assumption 与结果一起保存，不能把一张 PASS 截图写成“证明所有参数正确”。

## 综合结果说明 RTL 会变成什么硬件

[Yosys 文档](https://yosyshq.readthedocs.io/projects/yosys/en/latest/)对应的是 synthesis framework，不是第二个 simulator。用脚本固定 `read_verilog -sv`、`hierarchy -top`、process lowering、optimization、`check` 和 target-specific synthesis；查看 latch、combinational loop、undriven/multiple-driver、memory inference、cell count 和 hierarchy，而不只看综合成功。分别综合两个 FIFO depth，解释存储为何成为 register、distributed RAM 或 block RAM，并核对 read latency 是否随推断结构改变。

portable RTL 与 vendor primitive 要分层。核心控制和数据协议保持通用，PLL、block RAM mode、SERDES 或 debug core 放在薄 wrapper 内；仿真模型、综合源和 constraints 使用显式 file set。生成 netlist 或 bitstream 时记录 tool version、device part、parameter、constraint hash 与 source commit。若开源综合不支持某段 SystemVerilog，先判断它属于语言支持缺口还是原 RTL 本就依赖专有行为，不能把改写后的功能变化藏在“兼容性修复”里。

## CDC 结构与时序约束是两件事

CDC 先做结构，再做约束。单 bit level 可使用标注清楚的 synchronizer，但它只降低 metastability 传播概率，不保证窄 pulse 被目的域看到；pulse 或 command 需要 toggle/handshake，multi-bit payload 需要稳定数据加握手或经过验证的 asynchronous FIFO，不能把每一位各接两个 flip-flop。reset 可异步 assert，但应在每个 clock domain 内同步 deassert，并验证 clock 缺失、不同释放顺序与 reset crossing。

随后为 primary/generated clock、input/output delay 和真实 timing exception 写约束。[AMD 2026.1 UG903](https://docs.amd.com/r/en-US/ug903-vivado-using-constraints/All-Constraints)把 clock、I/O、asynchronous clock group、CDC synchronizer 与 constraint coverage 放在同一流程中；即使使用其他 vendor，也应达到同样的陈述完整度。`set_false_path` 只能描述本来就由正确 CDC 结构处理的异步关系，不能让坏 crossing 变安全。实现报告中逐项解释 unconstrained path、setup/hold、recovery/removal、clock uncertainty 与最差 slack；“timing passed”若仍有未约束路径，结论无效。

## 第一次上板只验证物理接口

第一次上板只连接受保护的 onboard LED、button 或 loopback。核对 schematic、bank voltage、pin direction、pull resistor、clock source 和 configuration-time state，断电后再接外设；motor、power stage、laser 和 RF transmitter 不能由未验证 RTL 直接驱动。输出在 configuration、reset、clock loss 与失锁时必须回到安全值。bitstream 与 source commit、constraints、device part 和固定 demo input 一一对应。

一份完整记录包括 RTL、interface timing diagram、两套 simulator 命令、自检查 testbench、固定 seed、正确修订的 formal PASS 结果，以及故意破坏修订产生的 counterexample 与对应补丁或提交。Yosys script、vendor constraints、resource/timing/CDC 摘要和可选的板上 trace 也应随项目保存。没有板卡时，工作可以停在 post-implementation report；有板卡只增加 I/O 与实际 clock 的观测，不会把未写的 property 或缺失的 constraint 自动补上。[嵌入式工具链](embedded-toolchains.md)负责 processor/firmware 加入后的证据链，[可复现工程](reproducibility.md)负责让这套回归跨机器保持稳定。
