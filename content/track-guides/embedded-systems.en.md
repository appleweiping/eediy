## CS 107E explains reset to application; EE 319K first establishes an MCU rhythm

The [current Stanford CS 107E site](https://cs107e.github.io/) builds [CS 107E](058-cs-107e.md) from RISC-V bare metal through startup, memory, and peripherals. Its Spring 2026 notes, labs, and some code are current and suit someone willing to follow the linker, boot flow, and registers. Formal lectures are not recorded, Mango Pi availability varies by region, and enrolled starter and staff repositories are private. The [official UT Austin Volume 1 page](https://users.ece.utexas.edu/~valvano/Volume1/IntroToEmbSys) gives [EE 319K](059-ee-319k-volume-1.md) an open text, chapter videos, and activities for GPIO, timers, interrupts, and sensors, making a gentler first MCU route.

Choose CS 107E to understand a machine from reset to application, or EE 319K to establish a dependable peripheral-laboratory rhythm. Prefer the MSPM0 edition of EE 319K rather than mixing in the older TM4C123 and archived edX environment. Local supply of the board, debugger, and replacements can decide the route more than the catalogue schedule.

Both routes require reading the board schematic and the MCU datasheet. One emphasizes startup and systems software while the other emphasizes microcontroller activities; the distinction is not which board happens to be more fashionable.

## One datasheet sentence should reach registers and a pin waveform

[Digital logic](../digital-logic/index.md) contributes registers, FSMs, clock and reset, and timing. [Programming and tools](../programming-tools/index.md) contributes C, pointers, masks, linking and building, Git, and tests. [Electronics laboratory](../electronics-laboratory/index.md) contributes low-voltage power, oscilloscope use, grounding, and raw-data practice. Select a timer, GPIO, or UART and write its register-level driver without a convenience library. Explain memory-mapped I/O, `volatile`, read-modify-write, and interrupt concurrency.

Draw the expected interrupt-latency timeline from the datasheet and compare it with a logic-analyzer or simulated trace. Repair pointers and linker maps in systems programming, unclear clock or FSM behavior in digital logic, and uncertain GPIO voltage, pull-ups, debounce, or ground reference at the bench. A complex RTOS belongs after the datasheet and bare-metal state are explainable; otherwise a successful API call hides the lower-level assumptions.

For every register write, identify write-one-to-clear, read-only, and reserved bits so an accidental read-modify-write cannot corrupt neighboring state. When an interrupt handler and main loop share data, explain the ordering and atomicity of the exact accesses involved.

## A board port is organized around clock tree, pin multiplexing, and equivalence tests

Check the Mango Pi, boot flow, and RISC-V peripheral map against the current CS 107E repository and schematic. An emulator or logic model can stand in for missing hardware only as a software or model result. MSPM0, TM4C123, and archived EE 319K edX materials do not share starters, IDEs, compilers, debug probes, or register addresses. A port states MCU and board revision, toolchain, headers, clock tree, pin multiplexing, I/O voltage, programmer, and licenses, with an equivalence test for every timer, GPIO, or serial interface.

Attribute third-party drivers and vendor examples; a renamed demonstration is still external code. Physical interfaces stay at safe low voltage. Motors, relays, and larger loads require isolation, protection, supply and thermal calculations, and power-off rewiring. If a new board changes interrupt latency, clock accuracy, or electrical levels, the test result should expose the difference rather than merely show successful compilation.

Clock and pin-multiplexing defaults deserve their own check. When a peripheral appears silent, verify that its clock is enabled, the pin function is selected, and logic levels match before treating the protocol algorithm as the leading suspect.

## One abnormal timeline explains more than a row of peripheral demonstrations

Build either a sensor→processing→output chain or a small communication node containing a learner-written register driver, interrupt or timer, state machine or buffer, and an externally observable result. Measure interrupt latency, period jitter, buffer overflow, or a power mode, then introduce a stuck sensor, delayed input, communication error, or reset. One timeline should show which module detects the condition, which state degrades or clears it, and when output becomes valid. A simulator and mocked peripheral can verify software when no board exists, while electrical and physical timing claims remain untested.

Select one abnormal run and label its source revision, build command, board revision, datasheet clause, register transition, pin waveform, and captured data. The first broken link in that chain chooses the continuation: deadline or shared-resource behavior goes to real-time systems; cache, DMA, virtual-memory, or boot behavior goes to computer architecture; a stable protocol limited by datapath throughput goes to FPGA/SoC; sensor accuracy or calibration goes to instrumentation. Re-run the same case after the transition so the new subject must explain an existing failure rather than start another blinking demonstration.
