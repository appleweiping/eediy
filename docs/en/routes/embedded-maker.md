---
title: "Embedded, Real-Time, and Board-Level Systems"
description: "Build a low-voltage embedded device that reads sensors, meets its control and communication timing, and includes a custom PCB, repeatable tests, fault recovery, and a recorded demonstration."
page_type: route
route_id: "route-embedded-maker"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: f3969bdd1cd6c22d -->

# Embedded, Real-Time, and Board-Level Systems

## Audience

Learners who want to move from digital logic and C through MCUs, real-time tasks, PCB design, and a working device

## What you should be able to do

Build a low-voltage embedded device that reads sensors, meets its control and communication timing, and includes a custom PCB, repeatable tests, fault recovery, and a recorded demonstration.

## Read the datasheet before choosing a board

Choose one low-voltage peripheral and one failure mode, such as an I²C temperature sensor disconnect. From the datasheet, write its voltage, address, update rate, timeout, and recovery action. Do not choose an RTOS or draw a PCB until those five are clear.

## Close the loop around one peripheral

- Generate golden register and boundary-input vectors in Python before writing the smallest C driver. A logic-analyzer trace must map to the datasheet's startup, read/write, timeout, and recovery behavior.
- Choose one obtainable platform: bare-metal, MSPM0, or Raspberry Pi. Measure worst-case response time and deadline misses instead of calling behavior real-time because it looks responsive.
- Draw a custom board only after the target, debugger, low-voltage current-limited supply, instruments, parts, and budget are real. Otherwise retain the reproducible peripheral model, firmware tests, and pre-board interface.
- Skip DDCA or introductory programming sections already covered by secure HDL, register, and C memory skills; do not move the same peripheral across three boards.

## Stop explicitly at pre-board, or make it a device

- For a polling-only device, skip advanced RTOS theory and mission-critical branches until measured scheduling or recovery behavior requires them.
- Without a board, stop honestly at pre-board once the golden model, firmware tests, timing assumptions, and unverified electrical behavior are explicit.
- With hardware, stop when nominal, boundary, disconnect, and reset scenarios pass repeatedly and the logic trace, deadline statistics, BOM, and demonstration all reproduce from one version.

## How to proceed

### A peripheral from model to timing

**Why these courses:** Organize the work around one peripheral driver. Use Python for the reference model and tests, C for firmware, 6.002 for the electrical limits outside the pins, and 6.004 for registers and digital timing. Consult the relevant DDCA chapters only if HDL, timing diagrams, or processor datapaths are still unfamiliar; there is no need to reread settled material merely to finish the book.

- [Introduction to CS and Programming Using Python](../courses/programming-tools/015-6-100l.md) — **Required**; MIT
- [Practical Programming in C](../courses/programming-tools/016-6-087.md) — **Required**; MIT
- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **Required**; MIT
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **Required**; MIT
- [Digital Design and Computer Architecture](../courses/digital-logic/038-ddca.md) — **Use if needed**; ETH Zurich

**Move on when:** Write the C driver and a register-level peripheral model, retaining a host-side reference implementation. Tests must cover every register field, boundary value, invalid state, and recovery path, with random seeds and coverage saved. Logic-analyzer traces or timing simulation must also show setup and hold margins that meet the datasheet.

### Bare metal, RTOS, and time

**Why these courses:** CS 107E is the route into bare-metal boot and peripherals; move the driver, reference model, and randomized tests directly into its firmware work. First confirm that the Mango Pi, boot chain, and public starter are still obtainable. Choose EE 319K for MSPM0 peripheral practice; choose RTES 1 only with Raspberry Pi, Linux, and Coursera lab access when scheduling is the goal, and consider RTES 2 afterward. A missing board can be modeled, but electrical behavior and interrupt timing remain explicitly unverified.

- [Computer Systems from the Ground Up](../courses/embedded-systems/058-cs-107e.md) — **Required**; Stanford University
- [Embedded Systems: Shape the World](../courses/embedded-systems/059-ee-319k-volume-1.md) — **Choose 1**; The University of Texas at Austin
- [Real-Time Embedded Systems Concepts and Practices](../courses/real-time-cps/063-real-time-embedded-systems-1.md) — **Choose 1**; University of Colorado Boulder
- [Real-Time Embedded Systems Theory and Analysis](../courses/real-time-cps/064-real-time-embedded-systems-2.md) — **Use if needed**; University of Colorado Boulder

**Move on when:** Build a bare-metal or RTOS prototype with interrupts, periodic tasks, and fault recovery. Define the observation duration and load first, then report cycle count, jitter distribution, observed maximum execution time, and CPU utilization; finite measurements are not a WCET proof. A detector must record every deadline miss against the stated budget.

### Turn it into a device

**Why these courses:** Keep the firmware, timing trace, deadline detector, and recovery hooks in the same device. Use the PCB workshop to make it manufacturable and ECE 4760/5730 to complete system integration. Add RTES 3 for mission-critical design and FMEA only when its Coursera material and specified hardware are available; leave RTES 4 for later. Confirm the low-voltage board, debugger, instruments, parts, and budget before committing, or stop at pre-board.

- [The Art and Science of PCB Design](../courses/pcb-eda/055-iap-pcb-2026.md) — **Required**; MIT
- [Digital Systems Design Using Microcontrollers](../courses/capstone-practice/057-ece-4760-ece-5730.md) — **Required**; Cornell University
- [Real-Time Mission-Critical Systems Design](../courses/real-time-cps/065-real-time-embedded-systems-3.md) — **Use if needed**; University of Colorado Boulder
- [Real-Time Project for Embedded Systems](../courses/real-time-cps/066-real-time-embedded-systems-4.md) — **Use if needed**; University of Colorado Boulder

**Move on when:** The device must include sensing, communications, a custom PCB, and a firmware-update path, with ratings, power budget, watchdog or safe state, thermal and overcurrent stops, and fault injections recorded. Tests cover each requirement, interface, fault state, and rollback. Finish with a supervised, predeclared run covering cold start, steady state, the slowest periodic task, rollback, and every declared fault class, recording its actual duration. The run describes prototype behavior in those scenarios; it is not reliability qualification.
