---
title: "Embedded Systems and Intelligent Hardware"
description: "Build an embedded system with sensing, real-time control, communications, schematic/PCB artifacts, test records, and a demo."
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 43d04b1b154b370e -->

# Embedded Systems and Intelligent Hardware

## Audience

Learners moving from digital logic to MCUs, real-time systems, PCBs, and complete hardware builds

## Final outcome

Build an embedded system with sensing, real-time control, communications, schematic/PCB artifacts, test records, and a demo.

## Stages

### Low-level foundations

**Selection rule:** Complete all 4 required courses; use the other 1 option only to close a specific gap.

- [Introduction to CS and Programming Using Python](../courses/programming-tools/015-6-100l.md) — **Required**; MIT; Mainline; S
- [Practical Programming in C](../courses/programming-tools/016-6-087.md) — **Required**; MIT; Mainline; A
- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **Required**; MIT; Mainline; S
- [Computation Structures](../courses/digital-logic/037-6-004.md) — **Required**; MIT; Mainline; S
- [Digital Design and Computer Architecture](../courses/digital-logic/038-ddca.md) — **Optional supplement**; ETH Zurich; Alternative; S

**Stage exit criterion:** Implement a C driver against a register-level peripheral model and build a host-side reference model; at least 200 boundary and randomized tests must pass, while logic-analyzer traces or timing simulation demonstrate datasheet-compliant setup and hold margins.

### Bare metal and real time

**Selection rule:** Complete all 1 required course and choose 1 of 2 elective options. The other course is an optional supplement and does not count toward the elective requirement.

- [Computer Systems from the Ground Up](../courses/embedded-systems/058-cs-107e.md) — **Required**; Stanford University; Mainline; S
- [Embedded Systems: Shape the World](../courses/embedded-systems/059-ee-319k-volume-1.md) — **Elective option**; The University of Texas at Austin; Mainline; S
- [Real-Time Embedded Systems Concepts and Practices](../courses/real-time-cps/063-real-time-embedded-systems-1.md) — **Elective option**; University of Colorado Boulder; Alternative; A
- [Real-Time Embedded Systems Theory and Analysis](../courses/real-time-cps/064-real-time-embedded-systems-2.md) — **Optional supplement**; University of Colorado Boulder; Alternative; A

**Stage exit criterion:** Build a bare-metal or RTOS prototype with interrupts, periodic tasks, and fault recovery, reporting worst-case execution time, CPU utilization, and jitter over 1,000 periods; every deadline must satisfy the predeclared budget.

### System projects

**Selection rule:** Complete all 2 required courses and complete the elective option. The other course is an optional supplement and does not count toward the elective requirement.

- [The Art and Science of PCB Design](../courses/pcb-eda/055-iap-pcb-2026.md) — **Required**; MIT; Mainline; S
- [Digital Systems Design Using Microcontrollers](../courses/capstone-practice/057-ece-4760-ece-5730.md) — **Required**; Cornell University; Mainline; S
- [Real-Time Mission-Critical Systems Design](../courses/real-time-cps/065-real-time-embedded-systems-3.md) — **Elective option**; University of Colorado Boulder; Alternative; A
- [Real-Time Project for Embedded Systems](../courses/real-time-cps/066-real-time-embedded-systems-4.md) — **Optional supplement**; University of Colorado Boulder; Alternative; A

**Stage exit criterion:** Complete an intelligent device with sensing, communications, a custom PCB, and a firmware-update path, including a power budget and fault-injection record; at least twenty automated system tests must pass with a continuous 30-minute run log.

## Execution rules

- Follow each stage's selection rule: complete every required course and the stated number of electives; when complete path options are provided, choose one and finish every course in its listed order; use optional supplements only to close a specific gap.
- Produce at least one reproducible artifact per stage and include failed attempts in the retrospective.
- Work involving mains voltage, high voltage, RF exposure, lasers, chemicals, or fabrication equipment requires local-law compliance and qualified supervision.
