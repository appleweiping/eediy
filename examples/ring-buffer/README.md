# Fixed-capacity ring buffer / 固定容量环形缓冲区

This starter is a host-executable C exercise, not pseudocode. The production
library rejects a ninth `uint16_t` sample when its eight-slot buffer is full,
preserves FIFO order through wraparound, and counts every rejected write. A
thin ADC/DMA adapter accepts a completed block and reports whether the whole
block fitted. It contains no MCU register access and makes no claim about
interrupt safety or board timing.

这是一个能在主机上编译执行的 C 练习，不是伪代码。正常库的缓冲区固定为
8 个 `uint16_t` 样本：装满后拒绝第 9 个样本，回绕后仍保持 FIFO 顺序，并对
每次拒绝计数。薄 ADC/DMA 适配层接收一个“DMA 已完成”的样本块并报告是否
完整写入；它不访问 MCU 寄存器，也不声称已经验证中断并发或板级时序。

## What is being tested / 测试边界

| Path | Evidence in this directory |
| --- | --- |
| Empty and invalid calls / 空与非法调用 | Empty reads and null arguments return `false`; no caller-provided output is touched. |
| Exact capacity and full / 容量与满状态 | Eight pushes succeed, the ninth fails, and `rejected_writes` increments. |
| Wraparound / 回绕 | Three slots are freed, reused, and then read in the original FIFO order. |
| Repeated boundary / 重复边界 | 64 full-fill/full-drain cycles exercise both indices repeatedly. |
| ADC/DMA adapter / 适配层 | A ten-sample block yields eight accepted and two dropped samples. |
| Runtime diagnostics / 运行时诊断 | The `host-sanitized` preset compiles and links both test paths with ASan and UBSan under GCC or Clang. |

`include/ring_buffer.h` is the public contract. `include/adc_dma_adapter.h`
is the platform seam: a real target should replace the producer outside the
core library and must supply the synchronization required between an ISR/DMA
callback and a consumer. `volatile` alone is not that synchronization.

`include/ring_buffer.h` 是公开契约；`include/adc_dma_adapter.h` 是平台接缝。
真实目标只替换核心库外面的生产端，并自行实现 ISR/DMA 回调与消费端之间
所需的原子性、临界区或内存顺序，不能用 `volatile` 代替同步。

## One-command rebuild / 一条命令重建

Requirements: CMake 3.25 or newer, Ninja, and GCC or Clang. From this
directory, run:

```console
cmake --workflow --preset host-sanitized
```

The workflow configures a fresh out-of-source build, compiles with warnings
as errors plus ASan/UBSan, and runs two CTest cases. Its stable acceptance
invariant is:

```text
ring_buffer_contract = Passed
ring_buffer_deliberate_fault = Passed
CTest pass rate = 100% (2/2)
```

该 workflow 会在独立构建目录中配置工程，以“警告即错误”和 ASan/UBSan
编译，再运行两个 CTest。不同 CTest 版本的摘要措辞并不相同；验收不变量是
上面两个具名测试均为 Passed，合计 2/2。编译器路径和耗时不应写死为证据。

The normal executable itself prints:

```text
ring-buffer check=empty-and-invalid result=PASS
ring-buffer check=exact-capacity-and-full result=PASS
ring-buffer check=fifo-wraparound result=PASS
ring-buffer check=repeated-boundary result=PASS
ring-buffer check=adc-dma-adapter result=PASS
ring-buffer check=adapter-arguments result=PASS
ring-buffer summary=PASS checks=6
```

These lines were obtained by compiling the checked-in sources with GCC
14.2.0 on 2026-07-31; the automated tests compare behavior rather than
trusting this pasted transcript.

以上输出来自 2026-07-31 使用 GCC 14.2.0 对仓库源码的实际编译运行。
自动测试重新执行程序并核对行为，不把这段文档日志当成通过证据。

## Deliberate negative path / 故意失败路径

`ring_buffer_faulty` compiles the same implementation with
`RING_BUFFER_DELIBERATE_FULL_FAULT=1`. It deliberately overwrites the oldest
sample and reports success when full, violating the public reject-on-full
contract. `ring_buffer_fault_probe` therefore exits with code 7 and prints:

```text
deliberate-fault: accepted sample 999 while full
```

`cmake/ExpectFailure.cmake` makes the CTest pass only when both the nonzero
exit code and that observed contract breach are present. If the faulty
program exits zero, the negative test fails. The macro is private to a
separate library target; it is never enabled in `ring_buffer`.

`ring_buffer_faulty` 用同一实现编译一个独立故障目标：满时错误地覆盖旧样本
并返回成功。探针必须真实退出 7，CMake 包装器同时核对退出码和故障信息；
若故障程序返回 0，负向测试反而失败。该宏只属于独立测试库，正常
`ring_buffer` 从不启用它。

## Limits / 局限

The host tests establish the data-structure contract and adapter accounting.
They do not establish lock-free ISR safety, DMA cache coherency, memory
barriers, worst-case execution time, or loss-free operation at a hardware
sample rate. Those require a named MCU, memory architecture, clock, producer
rate, consumer budget, and measured target evidence.

主机测试只证明数据结构契约和适配层计数。它没有证明 ISR 无锁安全、DMA
cache coherency、memory barrier、最坏执行时间，或某个硬件采样率下不丢样；
这些结论必须绑定具体 MCU、内存结构、时钟、生产/消费预算和板上测量。
