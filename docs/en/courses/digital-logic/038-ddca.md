---
title: "Digital Design and Computer Architecture"
description: "ETH Zurich's Digital Design and Computer Architecture connects digital design and computer architecture through complete 2025 videos, notes, exercises, and code, while its separately hosted materials need manual access checks."
page_type: course
course_id: "course-038"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: a708f0a6d5685ae9 -->

# ETH Zurich DDCA: Digital Design and Computer Architecture

## Course Overview

- **University:** ETH Zurich
- **Course code:** DDCA
- **Official prerequisites:** No provider-published hard prerequisite verified; recheck the course page
- **EEDIY preparation:** Programming and Engineering Computing; Circuit Analysis
- **Access:** Open without registration
- **Material status:** 2026-07-30; public-material guide

### A Course That Really Moves from Gates to a Processor

Onur Mutlu's material landing page changes across years; this guide fixes
**ETH Zürich Spring 2025**. The official
[schedule](https://safari.ethz.ch/ddca/spring2025/doku.php?id=schedule) moves
from Boolean logic, FSMs, Verilog, and timing into MIPS, single-cycle,
multicycle, and pipelined processors, then branch prediction, SIMD/GPU,
caches, multicore, and virtual memory. Choose it to connect RTL, an FPGA, and
architecture. The second half is wider than needed for HDL syntax alone.
Recordings are linked from Mutlu's
[materials entry](https://people.inf.ethz.ch/omutlu/lecture-videos.html), but
keep them aligned with the Spring 2025 files.

### Coursework

The [homeworks](https://safari.ethz.ch/ddca/spring2025/doku.php?id=homeworks)
provide 6 optional sets with solutions across RTL, ISA, pipelines, memory, and
advanced architecture. Optional described campus scoring, not their value for
self-study. Draw complete timing, pipeline, and cache decompositions before
reading a solution, then redo errors from blank paper.

The [labs](https://safari.ethz.ch/ddca/spring2025/doku.php?id=labs) list 9
experiments, progressing through circuit drawing, FPGA work, combinational
logic, FSMs, an ALU, and assembly into processor integration and MIPS
performance. Both stages of Lab 8 form a cumulative system. Preserve
interfaces and bit widths, RTL, self-checking testbenches, simulation
transcripts, synthesis/timing results, and a bug log. LEDs alone are weak
evidence. Keep the original [Lab 6 bundle](https://safari.ethz.ch/ddca/spring2025/lib/exe/fetch.php?media=lab6_files.zip)
unchanged and version personal work separately.

### Describe Board Status Precisely

The original flow uses Vivado and a Basys 3. Without a board, simulation and
synthesis support “pre-board complete,” not a physical demonstration. A board
result should preserve the board, target part, constraints, tool version, and
timing report. Investigate latch, width-truncation, and unconstrained-clock
warnings instead of silencing them.

Make the architecture half quantitative. Compare critical path and CPI for
an instruction trace under single-cycle, multicycle, and pipelined execution.
Split cache addresses into tag, index, and offset and count hits and misses.
Report clock, cycle and instruction counts, memory behavior, and timing slack
together.

### Use One Instruction to Check the ISA, Datapath, and Board

The [exam page](https://safari.ethz.ch/ddca/spring2025/doku.php?id=exams) is
the assessment entry for this term. After the sets and labs, take an unseen
paper under its printed rules. Finally, trace a MIPS instruction from ISA
semantics through control, datapath, pipeline, memory transaction, and an
FPGA-visible result. Mark bit width, clock boundary, and observation point at
every layer. The course has worked when an internal trace localizes a defect
before the final output fails. A bad state transition sends you back to RTL;
negative slack or a bad constraint sends you back to clocks and
implementation. One board demonstration cannot blur that distinction.

## Course Resources

- [Course home](https://people.inf.ethz.ch/omutlu/lecture-videos.html)
- [Code · DDCA Spring 2025 Lab 6 project archive](https://safari.ethz.ch/ddca/spring2025/lib/exe/fetch.php?media=lab6_files.zip)

## Resource Summary

Every public entry point verified in this review is listed above. Use the feedback and corrections links below to submit a completion record, another resource, or a broken-link report.
