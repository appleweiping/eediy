---
title: C, CMake, and Hardware-Adjacent Programs
description: Use one module that runs on a host and an MCU to understand C memory boundaries, build graphs, and cross-compilation.
page_type: guide
comments: true
---


# C, CMake, and Hardware-Adjacent Programs

A ring buffer is a useful way to learn C near hardware. It is easy to test on
a computer, yet an MCU quickly adds interrupts, memory layout, and throughput
limits. A common failure is a buffer that passes every host test, loses
samples on the board, and changes behavior with the optimization level. That
calls for separating algorithm, build, and hardware adaptation instead of
blaming the compiler by intuition.

| Exercise boundary | Object used on this page |
| --- | --- |
| Unit under test | A fixed-capacity `ring_buffer` and a thin ADC/DMA adapter |
| Visible symptom | Sequence gaps, a wrong overflow count, or an out-of-bounds access introduced on a test branch |
| Control environments | Host debug/AddressSanitizer and target firmware builds |
| Result to check | Reproduce with fixed input, locate the interface, memory, build, or concurrency boundary, and verify the repair |

The ring buffer is small enough to enumerate by hand, but it still exposes
integer widths, array bounds, wraparound, error reporting, and data shared
with an interrupt. Investigation begins with a core module that runs on a
computer; hardware returns only in the second half.

## Test the ring buffer boundaries on the host

Write a `ring_buffer` module for sample data with only initialization, write,
read, and status operations in its public interface. Specify capacity,
element type, overwrite-versus-reject behavior when full, and the result of an
empty read. A caller should not need to inspect the implementation to infer
the contract. Fixed-width types from `stdint.h` express storage intent, but
they do not by themselves solve arithmetic overflow, alignment, or byte
order; a serialized format still needs an explicit byte-level definition.

Test the empty state, exact capacity, head/tail wraparound, repeated overflow,
and invalid parameters on the host. Do not copy a mysterious bundle of
compiler flags. Use GCC's [Warning
Options](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html) to identify
what each selected warning checks, and retain the actual compile command. On
a platform with Clang, make a separate test build following the official
[AddressSanitizer documentation](https://clang.llvm.org/docs/AddressSanitizer.html)
so out-of-bounds access and use-after-free fail on the host. A sanitizer is
for the test build; it is not a runtime to place in the target firmware.

Hide register access and timer calls behind a thin platform interface. During
testing, substitute an adapter that generates samples; on the board, replace
only that adapter with the real ADC or DMA path. `volatile` can express some
memory-mapped I/O accesses, but it is not a substitute for the atomicity,
critical sections, or memory ordering needed between an interrupt and the
main loop. If the core logic cannot run away from the board, the algorithm
and platform boundary is probably still tangled.

The repository's [fixed-capacity ring-buffer
starter](https://github.com/appleweiping/eediy/tree/main/examples/ring-buffer)
contains public headers, a thin ADC/DMA adapter, empty/full/wrap/boundary
tests, and a separate faulty target. From the starter directory,
`cmake --workflow --preset host-sanitized` compiles with warnings as errors,
ASan, and UBSan before running the normal contract and negative test. The
faulty library deliberately overwrites an old sample while full and reports
success; the test passes only when its probe really exits 7 and reports the
observed contract breach, so pasted expected output cannot substitute for
execution.

## Inspect what CMake actually invokes

Start with one library target and one test executable. Keep `CMakeLists.txt`
with the source and put all output in a separate `build/` directory. Deleting
that directory should allow a clean configure without copying headers by hand
or repairing an IDE cache. CMake's official [step-by-step
tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)
begins with executables, libraries, and target linkage, so it can be followed
while the ring-buffer project grows; there is no need to read the entire
reference first.

Attach include directories, compile definitions, and warning policy to the
targets that need them. Global flags tend to leak assumptions into every
target. Make tests part of the graph as well: configure, build, and test
should each have a clear command, and a failed test must return a nonzero
status. Inspect verbose build output to verify which compiler actually ran.
For an undefined reference, check whether the declaration has a definition,
whether the executable links the library, and whether static-library ordering
is correct before repeatedly clearing caches.

When a team or CI needs a shared configuration, the official [CMake Presets
manual](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html)
explains the split: project settings belong in `CMakePresets.json`, while
machine-specific paths and personal choices belong in the uncommitted
`CMakeUserPresets.json`. A preset makes one configuration repeatable; it does
not make nonportable source portable.

## Keep separate host and target builds for the same core

Only after host tests pass should the project acquire a cross-compiler,
toolchain file, linker script, and startup code. Do not collapse them into the
only build. Retain two independent entries:

```text
host-debug  -> ring_buffer + tests + sanitizer
target      -> ring_buffer + hardware adapter + firmware image
```

Both paths compile the same core implementation, but answer different
questions. The host path supports broad boundary testing and diagnostics. The
target path checks the ABI, memory layout, startup sequence, registers, and
real-time constraints. After a target build, read the map file or size
summary well enough to locate code, read-only data, initialized data,
zero-initialized storage, and the rough stack/heap budget. An image that can
be flashed does not establish that RAM fits or that an interrupt-rate stream
will not lose samples.

Before using a board, drive the adapter with a fake interrupt and deliberately
make the consumer slow. Observe whether the chosen overflow policy really
takes effect. On hardware, begin with a conservative clock, current-limited
supply, and a debug interface that still permits recovery. The first run
should compare sequence numbers, counts, and error codes for a known input.
If a fault appears only under optimization, investigate undefined behavior,
uninitialized state, and concurrency boundaries before treating disabled
optimization as a fix.

## What a useful debugging record retains

Leave one host command that works from a fresh directory, one target-build
command, and one intentional failure. The failure might use a boundary
capacity, make the producer outrun the consumer, or introduce an
out-of-bounds access on a test branch; the test should explain why it failed.
Retain the interface note, test log, compiler version, observed commands,
image size, and board and clock details. Those items should be sufficient to
rerun the host-side behavior and the same class of failure without the
development board.

The original symptom, minimal reproduction, root cause, repair, and regression
test should point to one another. [Embedded
Toolchains](embedded-toolchains.md) extends the investigation through ELF,
flashing, and startup; [Version Control](version-control.md) separates
algorithm, hardware-adapter, and build changes into traceable commits.
Motors, heaters, stored energy, and RF transmission still require hardware
limits, timeouts, rating checks, and supervised facilities; software tests
cannot replace them.
