---
title: "Hardware Security"
description: "Side channels, fault attacks, trusted execution, and secure architecture using real processors and testable threat models."
page_type: track
track_id: "track-hardware-security"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 582e50716e02e38f -->

# Hardware Security

## Track position

Side channels, fault attacks, trusted execution, and secure architecture using real processors and testable threat models.

## Recommended prerequisite tracks

- [Digital Logic and Computation Structures](../digital-logic/index.md)
- [Computer Architecture](../computer-architecture/index.md)

## The public scope of 6.5950 changes lab by lab

The [official Spring 2025 MIT 6.5950 archive](https://ocw.mit.edu/courses/6-5950-secure-hardware-design-spring-2025) places cache side channels, transient execution, Rowhammer, hardware-software contracts, CPU fuzzing, formal verification, and TEEs under one question: how a secret or privilege state crosses a boundary assumed to hold. Public learners can inspect the [2025 lab index](https://shd.mit.edu/2025/labs.html), use the [official starter repository](https://github.com/MATCHA-MIT/SHD-StarterCode), and run locally supported portions of Lab 0, Lab 1, and Lab 7. Labs 2–5 depend on assigned bare-metal hosts or selected DRAM, while Lab 6 depends on a course server, dedicated debug port, and RTL environment.

Repository visibility is not equivalent to all laboratory conditions. Describe each lab honestly as executed, simulated, reasoned from the handout, or inaccessible, and do not reconstruct Gradescope, Piazza, hidden tests, or classroom feedback. The track currently has no interchangeable alternative; the strength of [6.5950](053-6-5950.md) is seeing attacks, contracts, and verification in one course.

Public handouts support a threat model and local code analysis; assigned servers and specified hardware determine which empirical claims can be made. Treat those two evidence layers separately.

## A threat model comes before an attack script

[Digital logic](../digital-logic/index.md) should already provide synchronous RTL, reset, assertions, and waveform reading. [Computer architecture](../computer-architecture/index.md) should provide cache mapping, virtual memory, exceptions, privilege, and speculative state. [Programming and engineering tools](../programming-tools/index.md) should cover C memory defects, sanitizers, GDB, Git, and containers. Decompose a virtual address into page, tag, index, and offset, distinguish architectural from microarchitectural state, and write a safety property plus counterexample for a short SystemVerilog machine.

Every exercise should answer four questions: the protected asset, attacker capabilities, observable channel, and violated property. Recognizing the names Spectre or Rowhammer without identifying the observer and state boundary is not improved by executing another script. Hardware security is not a reel of attack demonstrations; it is a system model explaining why information crosses a particular boundary.

For the same event, separate the architecturally visible outcome from residual microarchitectural state. That prevents timing differences, cache state, and permission checks from being collapsed into one vague “vulnerability” label.

## Course experiments belong only on authorized, production-isolated equipment

Run website fingerprinting only on self-authored pages and controlled tabs. Cache, ASLR, Spectre, Rowhammer, and fault experiments belong only on personally owned or explicitly permitted equipment isolated from production work. When compliant bare metal, vulnerable DRAM, HTCondor, Unicorn, or course credentials are unavailable, handout derivations, public traces, local Docker results, and defensive analysis remain possible, but a VM substitute is still an independent exercise.

State the Spring 2025 material version, starter commit, compiler, Yosys, Rosette, or sanitizer version, equipment ownership, isolation, and stop conditions. A third party's device is outside the scope of scanning, weakening protections, or secret recovery. Missing course infrastructure cannot be repaired by expanding authority; the security boundary is itself part of the subject.

## Make fuzzing and formal methods inspect the same self-authored defect

Use a self-authored small RISC-V or RTL block and seed one documented arithmetic, permission, or state-update defect in simulation. One path uses differential fuzzing to find and minimize a triggering input; the other writes formal assertions and produces a counterexample. After the correction, both regressions should check the same property, with the unexamined state space stated. The project distinguishes MIT material, public portions actually run, and independently constructed content, and states that no third-party device or real secret was touched.

Place the minimized fuzzing input and the formal counterexample beside one defensive claim, then identify the first state transition on which their explanations differ. A disagreement in cache, speculation, or TEE state becomes a microarchitectural-security question; a disagreement in assertions, model coverage, or proof assumptions becomes a hardware-formal-verification question; a disagreement at C, compiler, or OS semantics becomes a systems-security question. The next course inherits that counterexample and property, so progress is measured by closing an explicit threat-model gap rather than collecting attack output.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Secure Hardware Design](053-6-5950.md) | MIT | Main course | Public-material guide | Public assignments or labs |
