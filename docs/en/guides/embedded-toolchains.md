---
title: Embedded Toolchains and Board-Level Debugging
description: Build embedded work around a traceable ELF, recoverable flashing, and layered peripheral observations.
page_type: guide
comments: true
---

# Embedded Toolchains and Board-Level Debugging

The first embedded failure often produces no display at all. The fault may lie in compiler options, the linker script, a flash algorithm, startup code, power, reset, or application logic. A useful toolchain is more than an IDE that builds: it lets each symptom be assigned to one of those layers while preserving a route back to a known-good image.

## Make the ELF explain where it will run

Arm now publishes new GNU Toolchain releases in its [official release repository](https://gitlab.arm.com/tooling/gnu-toolchains-for-arm). Select a package by host OS, host architecture, and target triple. A typical Cortex-M bare-metal project needs `arm-none-eabi`; an Arm name does not make a Linux or AArch64 variant interchangeable. Preserve the archive checksum and record `arm-none-eabi-gcc --version`, `-mcpu`, `-mthumb`, `-mfloat-abi`, and the selected C library in the build log.

Do not flash the first successful build immediately. The linker script must place the vector table, text, data, bss, stack, and heap within the device memory map. Inspect the `.map` for entry point, section addresses, Flash and RAM use, and unexpectedly large objects, then cross-check with `size`, `nm`, or `objdump`. Keep the ELF and its checksum. A `.hex` carries addresses; a raw `.bin` does not, so the latter is safe only when the flashing command supplies the correct base address. Compile algorithms, protocol encoding, and filters into host tests first so a board failure does not also put the mathematics in doubt.

## Rehearse board recovery before the first flash

The [OpenOCD flash guide](https://openocd.org/doc/html/Flash-Programming.html) combines programming, verification, reset, and exit into a scriptable operation, such as `program firmware.elf verify reset exit` with the correct board configuration; a raw binary additionally needs an address. Its [reset configuration guide](https://openocd.org/doc/html/Reset-Configuration.html) makes clear that SRST, TRST, and halt-on-reset behavior depend on the target, board, and adapter. Do not copy a configuration from a related board and erase immediately, or treat repeated reset-button presses as a recovery design.

With pyOCD, read [target support](https://pyocd.io/docs/target_support.html) and run `pyocd list` and `pyocd list --targets`. The generic `cortex_m` target can provide basic CoreSight debugging but has no flash memory map or programming algorithm. Confirm a precise target or the correct CMSIS-Pack before writing flash. The [pyOCD command reference](https://pyocd.io/docs/command_reference.html) provides `load`, `compare`, `erase`, and `reset` for a recovery script, but mass erase, unlock, or protection changes belong only where the device manual permits them and loss of stored data has been accepted.

Before application firmware changes pin multiplexing, low-power state, or the debug port, retain a known-good minimal image, verify boot straps, reset pin, and debug voltage, and actually perform connect, permitted erase, program, compare, reset, and fixed-output observation. The debugger I/O voltage must match the target and board and probe need a common reference. Begin with protected onboard power or a conservative current limit, and prevent a programmer from back-powering an unpowered system.

## Bring up a peripheral with both logs and pin measurements

Start with the clock tree, reset cause, and one fixed serial message. Add GPIO, timer, interrupt, and a communication peripheral one layer at a time. Leave both a software and physical observation at each layer: a log names the initialization stage and error code, while a logic analyzer or oscilloscope measures level, period, and pulse width at the pin. For garbled serial, compare peripheral clock, baud divisor, frame format, and I/O voltage. For a silent GPIO, inspect reset state, clock enable, and pin multiplexing before rewriting the driver.

Classifying faults by boundary is faster than changing everything. Use compiler invocations, the map, and disassembly for build or link failures; power, ground, target ID, reset, and adapter speed for probe failures; reset handler, vector table, copy and zero loops, and fault handlers for startup; and stack watermark, races, barriers, interrupt priority, and watchdog state for runtime failures. Change one condition at a time and preserve the first bad log or trace. Behavior that changes with optimization usually exposes undefined behavior, a race, or a timing assumption rather than a compiler that has become random.

## A timeout-aware sampler exposes the whole chain

Build a low-risk sensor sampler in which a timer starts acquisition, the driver returns a timestamped value and status, and the main loop or task performs conversion and output. Test conversion, filtering, packet formation, and the timeout state machine on the host. On the board, measure sample period, jitter, and interrupt service time. Inject a missing sensor, busy bus, CRC error, full buffer, and delayed interrupt in turn. The system should abandon the transaction within a stated time, produce an explicit invalid or default state, and keep the log parseable.

Begin with the repository's [timeout-aware sensor-sampler
starter](https://github.com/appleweiping/eediy/tree/main/examples/sensor-sampler).
It keeps `start/poll/cancel/publish` behind a target-adapter interface and uses
a host mock to execute one normal transaction plus all five faults above.
From the starter directory, run
`cmake --workflow --preset host-sanitized`; the test compares the
deterministic key-value log line by line, checks that a delayed interrupt is
cancelled at the 5 ms deadline, and requires every fault to remain `invalid`
with default value `0`. This evidence covers the software state machine only,
not a physical sensor, bus timing, or power consumption.

Then power-cycle and trigger a controlled watchdog reset, retain the reset cause, and confirm that startup does not spuriously drive an actuator. The project should contain board revision, schematic and pin table, toolchain and SDK versions, linker map, known-good image, build, flash, and recovery commands, host tests, raw log, timing trace, and one timeline from reset through fault recovery. Without a board, a simulated target and mocked peripheral can cover the software path, while electrical behavior, startup time, and power remain explicitly unverified.

## Board debugging stops at a controlled low-energy system

A GPIO must not drive an excessive load directly. Motors, relays, heaters, lithium cells, body connections, and higher-energy supplies require separate drivers, isolation, protection, and qualified supervision. Radio operation is also subject to regional frequency and power rules. Every output needs a safe default during reset, bootloader execution, communication loss, and a firmware crash; hardware protection must not depend on software responding in time.

After the sampler, move to [Instrumentation and Measurement](instrumentation-measurement.md) when edges, jitter, or loading are the main unknowns, or to [HDL and FPGA](hdl-fpga.md) when throughput calls for a parallel datapath. The lasting result is not a vendor IDE click path. It is a route from ELF addresses through flash verification and startup logs to a pin waveform, plus a tested way to recover the board after firmware loses control.
