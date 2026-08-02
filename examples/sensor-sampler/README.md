# Timeout-aware sensor sampler / 带超时的传感器采样器

This starter separates a small timeout state machine from a target adapter.
The checked-in host mock executes one successful transaction and five fault
injections: sensor missing, bus busy, CRC error, output buffer full, and a
delayed interrupt. Every failure leaves the public outcome invalid with the
default value `0`; the log identifies the reason with stable key-value fields.

这个 starter 把超时状态机与 target adapter 分开。仓库中的 host mock 会真实
执行一次正常事务，并依次注入 sensor missing、bus busy、CRC error、
buffer full 和 delayed interrupt。每个失败都把公开结果置为 invalid，数值
回到默认值 `0`，日志则用稳定的键值字段给出原因。

## Interface and state contract / 接口与状态契约

`include/target_adapter.h` is the only hardware-facing seam:

- `start` begins a transaction or reports a missing sensor/busy bus;
- `poll` returns pending, a value, or a CRC failure;
- `cancel` abandons a transaction at its deadline;
- `publish` accepts a valid sample or reports that the output buffer is full.

`include/sampler.h` retains only `idle` and `waiting` states. A request started
at `t=0 ms` has a declared deadline of `t=5 ms`. Polls at 1 ms and 4 ms may
remain pending; at 5 ms the sampler cancels without another driver poll,
publishes no value, records `delayed_interrupt`, and returns to `idle`.
Unsigned timestamp comparison is wrap-safe for intervals shorter than
half the `uint32_t` range.

`include/target_adapter.h` 是唯一面向硬件的接缝：`start` 开始事务，
`poll` 返回 pending/value/CRC fault，`cancel` 在截止点中止事务，
`publish` 把有效样本送入输出队列。状态机只有 `idle` 与 `waiting`。
在 `t=0 ms` 启动、超时设为 5 ms 时，1 ms 和 4 ms 可继续等待；到 5 ms
直接取消，不再调用 driver poll，不发布数值，记录 `delayed_interrupt`
并回到 `idle`。

| Injection / 注入 | Observable result / 可观察结果 |
| --- | --- |
| none / 无 | `valid`, value `2500`, published once at 1 ms |
| sensor missing | `invalid`, value `0`, `sensor_missing` |
| bus busy | `invalid`, value `0`, `bus_busy` |
| CRC error | `invalid`, value `0`, `crc_error` |
| buffer full | valid driver value is not exposed; `invalid`, value `0`, `buffer_full` |
| delayed interrupt | two pending polls, one cancel at 5 ms, `invalid`, value `0`, `delayed_interrupt` |

## One-command rebuild / 一条命令重建

Requirements: CMake 3.25 or newer, Ninja, and GCC or Clang. From this
directory, run:

```console
cmake --workflow --preset host-sanitized
```

The workflow compiles with warnings as errors and ASan/UBSan, then runs the
host fault matrix. Its version-independent acceptance invariant is:

```text
sensor_sampler_fault_matrix = Passed
CTest pass rate = 100% (1/1)
```

该 workflow 使用“警告即错误”和 ASan/UBSan 编译，再执行 host fault
matrix；不同 CTest 版本的摘要措辞可以变化，验收不变量是具名测试为 Passed、
合计 1/1。工具路径与耗时随机器变化，不写死。

The test executable's deterministic log is:

```text
scenario=default_safe event=state t_ms=0 validity=invalid value_milli=0 reason=not_ready state=idle
scenario=normal event=request t_ms=0 state=waiting deadline_ms=5
scenario=normal event=outcome t_ms=1 validity=valid value_milli=2500 reason=none state=idle
scenario=sensor_missing event=outcome t_ms=0 validity=invalid value_milli=0 reason=sensor_missing state=idle
scenario=bus_busy event=outcome t_ms=0 validity=invalid value_milli=0 reason=bus_busy state=idle
scenario=crc_error event=request t_ms=0 state=waiting deadline_ms=5
scenario=crc_error event=outcome t_ms=1 validity=invalid value_milli=0 reason=crc_error state=idle
scenario=buffer_full event=request t_ms=0 state=waiting deadline_ms=5
scenario=buffer_full event=outcome t_ms=1 validity=invalid value_milli=0 reason=buffer_full state=idle
scenario=delayed_interrupt event=request t_ms=0 state=waiting deadline_ms=5
scenario=delayed_interrupt event=outcome t_ms=5 validity=invalid value_milli=0 reason=delayed_interrupt state=idle
sensor-sampler summary=PASS scenarios=6
```

These lines were obtained by compiling and running the checked-in sources
with GCC 14.2.0 on 2026-07-31. Repository tests execute the binary and compare
the log; the pasted transcript is not used as a substitute for execution.

以上日志来自 2026-07-31 使用 GCC 14.2.0 对仓库源码的实际编译运行。
仓库测试会重编译、执行并核对日志，文档中的复制文本不代替执行证据。

## Replacing the mock / 替换 mock

Keep `sampler.c` unchanged and implement the four adapter callbacks for the
chosen driver. State exactly where CRC is checked, what `publish` owns or
copies, and whether `cancel` can race with an ISR. Convert raw codes and units
in one named layer before publishing. On a board, add measured sample period,
jitter, interrupt service time, and a recovery trace; do not infer them from
the host timestamps.

换到真实板卡时保持 `sampler.c` 不变，只实现四个 adapter callback。文档必须
说明 CRC 在哪层检查、`publish` 是转移所有权还是复制，以及 `cancel` 是否
可能与 ISR 竞争；raw code 与单位换算也应集中在一个有名字的层。板上另测
采样周期、jitter、ISR 时间和恢复轨迹，不能把 host mock 时间戳当实测。

## Limits and safety / 局限与安全

No physical sensor, bus, MCU, watchdog, actuator, voltage, startup time, or
power consumption was tested here. The default value is a software state, not
an independent hardware interlock. Any actuator or higher-energy output still
needs a safe reset state, timeout, ratings check, and hardware protection that
does not depend on this task running.

这里没有测试实体传感器、总线、MCU、watchdog、actuator、电压、启动时间或
功耗。默认值只是软件状态，不是独立硬件联锁；任何执行器或更高能量输出仍
需要安全复位态、超时、额定值检查，以及不依赖该 task 正常运行的硬件保护。
