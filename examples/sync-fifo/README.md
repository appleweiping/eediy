# Synchronous FIFO verification starter / 同步 FIFO 验证 starter

This example is a small RTL project with a real negative control. The same
scoreboard and formal reference model check a correct `baseline` and a
`FAULT_READ_POINTER` build that deliberately stops the read pointer. No PASS
log, waveform, netlist, timing report, or board result is committed.

这个例子不是波形截图演示，而是一套带负向控制的最小 RTL 工程。同一份 scoreboard
和 formal reference model 同时检查正确的 `baseline`，以及故意让读指针停住的
`FAULT_READ_POINTER` 构建。仓库不提交 PASS 日志、波形、网表、时序报告或上板结果。

## One command / 一条命令

From the repository root:

```console
python examples/sync-fifo/run_checks.py
```

The runner executes every toolchain that is actually installed and prints an
explicit `CHECK_SKIP` for each unavailable path. A release or CI machine must
use `python examples/sync-fifo/run_checks.py --require-tools all`; that form
fails if Icarus, Verilator, SymbiYosys with Z3, or Yosys is absent.

这条命令只执行本机真实安装的工具；缺失路径会打印明确的 `CHECK_SKIP`，不会拿源码
扫描或旧日志冒充运行结果。发布与 CI 机器必须增加 `--require-tools all`，只要
Icarus、Verilator、带 Z3 的 SymbiYosys 或 Yosys 缺少一项就失败。

## Contract / 接口约定

`sync_fifo` is a synchronous, non-fall-through ready/valid FIFO. Reset is
synchronous and active low. `out_data` is meaningful only when `out_valid` is
high. A full FIFO raises `in_ready` when an accepted read on the same edge
makes room, so a full-state read and write may occur together without changing
`occupancy`. `DEPTH` must be a power of two and at least two.

`sync_fifo` 是同步、非 fall-through 的 ready/valid FIFO。reset 为同步低有效；
只有 `out_valid=1` 时 `out_data` 才有意义。FIFO 已满但同一沿会接受读取时，
`in_ready` 仍为高，因此满状态可同周期读写且 `occupancy` 不变。`DEPTH` 必须
是至少为 2 的二次幂。

The self-checking testbench covers:

- reset at startup and reset while data is queued;
- a read request while empty and a rejected write while full;
- output stability under backpressure;
- fill, ordered drain, pointer wraparound, and both full-state and non-full
  simultaneous read/write;
- the exact same sequence under `FAULT_READ_POINTER`, which must exit nonzero
  with `SYNC_FIFO_MISMATCH`.

自检查 testbench 覆盖启动 reset、队列中途 reset、空读请求、满写拒绝、
backpressure 下输出稳定、填满与顺序排空、指针回绕，以及满/非满状态的同周期
读写。同一序列在 `FAULT_READ_POINTER` 下必须以非零状态和
`SYNC_FIFO_MISMATCH` 失败。

## Formal scope / 形式验证边界

`formal/baseline.sby` has two tasks. `bmc` uses `smtbmc z3` with a depth of
12 and checks occupancy bounds, reset state, accepted-transfer count changes,
ready/valid state, and FIFO ordering against an independent reference queue.
`cover` has depth 8 and requires full, simultaneous transfer, and empty-read
request states to be reachable. The harness checks a 2-bit, depth-2 instance;
simulation separately exercises an 8-bit, depth-4 instance and synthesis
elaborates depth 16. The harness holds synchronous reset low through the first
two sampled edges; valid, ready, and data are otherwise unconstrained. A PASS is therefore a **bounded,
parameter-specific safety result through depth 12**, not an unbounded proof.

`formal/fault-read-pointer.sby` runs a depth-8 BMC with the read-pointer fault
enabled. It intentionally retains `expect pass`, so the discovered assertion
failure makes SBY return nonzero. `run_checks.py` additionally refuses to call
that result useful unless SBY generated a real `trace*.vcd` counterexample.
Generated work directories live below ignored `build/`; reproduce them with
the recorded tool versions instead of committing a screenshot.

`formal/baseline.sby` 的 `bmc` 任务使用 `smtbmc z3`、depth 12，对独立
reference queue 核对 occupancy 边界、reset 状态、accepted transfer 后的
count 变化、ready/valid 状态与 FIFO 顺序；depth 8 的 `cover` 要求 full、
同周期 transfer 和空读请求可达。harness 检查 2-bit、depth-2 实例；仿真另测
8-bit、depth-4，综合则展开 depth-16。harness 在最初两个采样沿保持同步 reset
为低，之后的
valid、ready 与 data 均不受约束。PASS 只表示该参数实例 depth 12 以内的
bounded safety result，不是无界证明。故障配置执行 depth-8 BMC，并刻意保留
`expect pass`，所以 assertion failure 会让 SBY 非零退出；runner 还要求它
确实生成 `trace*.vcd`，否则不接受“找到反例”的说法。

## Synthesis and constraints / 综合与约束

`synth/synth.ys` elaborates an 8-bit, depth-16 instance, runs generic Yosys
synthesis and `check -assert`, then writes disposable statistics and JSON
below `build/synth/`. `constraints/sync_fifo.sdc` is a generic 100 MHz
interface budget with input/output delays and clock uncertainty. It is not a
vendor constraint set: `build-metadata.json` deliberately leaves the device
and board pinout null.

Generic Yosys synthesis cannot establish FPGA memory mapping, post-route
timing, CDC safety, bitstream correctness, or board behavior. To make any of
those claims, add a named device/board, complete pin and electrical
constraints, the corresponding vendor or open-source implementation flow,
and fresh reports tied to a source revision.

`synth/synth.ys` 会展开 8-bit、depth-16 实例，执行 generic Yosys synthesis
与 `check -assert`，再把临时统计和 JSON 写进 `build/synth/`。
`constraints/sync_fifo.sdc` 只是带 input/output delay 与 clock uncertainty
的通用 100 MHz 接口预算，并非任何厂商器件的完整约束；
`build-metadata.json` 因此把 device 和 board pinout 保留为 null。它不能证明
FPGA memory mapping、布局布线后时序、CDC、bitstream 或上板行为。
