---
title: C, Build Systems, and Hardware-Adjacent Programming
description: Move from portable host programs to constrained embedded code with a compile, test, and diagnosis loop.
---

<div class="ee-language" markdown>
[简体中文](../../guides/c-cmake.md)
</div>

# C, Build Systems, and Hardware-Adjacent Programming

The point of learning C is to understand representation, memory, compilation boundaries, and hardware interfaces—not to memorize syntax. A build system makes relationships among sources, options, dependencies, and artifacts explicit. CMake is one common example, but the workflow applies to other scriptable build tools.

## Purpose and learning outcomes

- Express hardware-adjacent data with fixed-width types and explicit units.
- Separate driver logic, algorithms, and platform interfaces.
- Find defects early with warnings, static checks, and host tests.
- Configure, build, test, and package repeatably from an empty directory.
- Read compiler, linker, map, and runtime diagnostics.

## Minimal environment

- A C compiler suited to the learning objective.
- A scriptable build tool.
- A debugger or runtime diagnostic tool.
- Version control and a plain-text editor.
- A host-side exercise; no development board is required for the core task.

Retain the actual compiler and build-tool versions, target architecture, and important options. Do not copy unexplained compiler flags; each option needs a stated purpose.

## Learning sequence

1. **Representation:** practice integer widths, signedness, shifts, byte order, and structure layout.
2. **Boundaries:** define contracts for array length, buffer capacity, errors, and ownership.
3. **Layers:** separate pure algorithms from registers, timers, serial ports, and other platform access.
4. **Build:** define libraries, executables, include paths, compile options, and test targets.
5. **Diagnosis:** treat significant warnings as failures and run host unit tests and runtime diagnostics.
6. **Cross-compilation:** only then add a target toolchain file, linker script, and flashing step.

Treat `volatile`, interrupt-shared data, and memory-mapped registers according to language and platform semantics. They are not general-purpose thread synchronization.

## Verification task: a portable ring buffer

Implement a fixed-capacity ring buffer for sample data:

1. Specify capacity, overflow policy, input type, and error behavior.
2. Implement initialization, write, read, and status queries on the host.
3. Test empty, full, wraparound, boundary length, and invalid parameters.
4. Use compiler warnings and available runtime diagnostics to detect bounds errors and undefined behavior.
5. Build a library and test program from an empty build directory.
6. Add a thin platform adapter that simulates samples from an interrupt and consumption in a main loop.

Acceptance includes passing tests, zero unexplained warnings, and a map or size summary that accounts for memory cost.

## Common failures and diagnosis

- **Results differ across platforms:** inspect type widths, alignment, byte order, and undefined behavior.
- **The linker reports an undefined symbol:** check declaration versus definition, link order, target dependencies, and name mangling.
- **A header change does not rebuild:** make dependency tracking explicit instead of relying on manual command order.
- **The fault appears only with optimization:** look for bounds errors, uninitialized data, races, and incorrect `volatile` assumptions.
- **Tests run only on the board:** extract pure logic and hardware interfaces, then use test doubles on the host.
- **The device disappears after flashing:** preserve a recovery interface and conservative clock setup before checking pins and boot mode.

## Reproducible evidence

- Source, public headers, and interface contracts.
- Build configuration, toolchain file, and observed compile commands.
- Test inventory, test log, and boundary-coverage notes.
- Compiler-warning policy and a zero-unexplained-warning record.
- Binary size, map file, or symbol summary.
- Target board, clocks, memory layout, and flashing procedure.
- Implementation-defined behavior, platform assumptions, and recovery steps.

## Cost, licensing, and accessibility

Host exercises can use free compilers and build tools and require no hardware. Record library licenses, provenance, and build configuration. Do not redistribute vendor-restricted packages in a public repository.

Make terminal commands available as scripts and retain errors as text. Do not express state only with LED color; provide serial logs, test reports, or readable status codes. Learners with limited hardware can preserve the objective through host simulation.

## Safety boundaries

- Bounds errors, integer overflow, and invalid pointers can become physical device hazards, not merely software defects.
- Before flashing, verify target, supply, debug voltage, pin multiplexing, and recovery path.
- Watchdog, actuator, and power-control code needs a safe default state and timeout.
- Never run unknown firmware on unverified hardware.
- Motors, heaters, stored energy, or RF transmission require supervised facilities and independent hardware protection.

## Completion checklist

- [ ] The project configures, compiles, and tests from an empty build directory.
- [ ] Fixed-width types, units, and interface ownership are documented.
- [ ] Core logic is testable without real hardware.
- [ ] Boundary, error, and wraparound behavior have tests.
- [ ] No compiler or linker warning remains unexplained.
- [ ] Toolchain, target, memory cost, and recovery procedure are recorded.
- [ ] Third-party code provenance and licensing are clear.
- [ ] The hardware adapter has a safe default state and stop conditions.

Next, continue to [Embedded Toolchains](embedded-toolchains.md), or use [Version Control](version-control.md) to preserve each verified milestone.
