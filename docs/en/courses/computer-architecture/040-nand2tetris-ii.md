---
title: "Build a Modern Computer from First Principles: From Nand to Tetris, Part II"
description: "Hebrew University of Jerusalem's Build a Modern Computer from First Principles: From Nand to Tetris, Part II uses six self-contained projects to implement a virtual machine, compiler, and operating system, requiring introductory programming, Python or Java setup, and potentially paid platform access."
page_type: course
course_id: "course-040"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 6d3d3b373be5de80 -->

# Hebrew University of Jerusalem Nand2Tetris II: Build a Modern Computer from First Principles: From Nand to Tetris, Part II

## Course Overview

- **University:** Hebrew University of Jerusalem
- **Course code:** Nand2Tetris II
- **Official prerequisites:** No provider-published hard prerequisite verified; recheck the course page
- **EEDIY preparation:** Digital Logic and Computation Structures; Programming and Engineering Computing; Introductory programming; Part I is a useful companion, but the provider describes Part II as self-contained
- **Access:** Open entry; some materials require registration or are limited
- **Material status:** 2026-07-30; public-material guide

### Course fit

Nand2Tetris Part II covers Projects 7–12 on the official [course page](https://www.nand2tetris.org/course): 2 VM-translator stages, 1 Jack application, 2 compiler stages, and the Project 12 Jack OS. It fits learners who have finished Part I and want to see a high-level language reach Hack instructions by construction. Recursion, object state, parsing, symbol tables, stack frames, and file I/O are practical prerequisites; processes, filesystems, and networking belong in a later operating-systems course.

### Coursework

Projects 7–8 move from arithmetic and memory segments to branches, call/return, bootstrap, and recursion. Function frames are the subtle part: shifting the save or restore order for LCL, ARG, THIS, THAT, or the return address by a single slot may surface only in a recursive program. Projects 10–11 join a tokenizer, parser, symbol table, and VM generator into a compiler. Their appeal is that a Jack-language mistake eventually becomes VM output whose origin can be traced to a specific layer.

Official [Project 12](https://www.nand2tetris.org/project12) implements Math, String, Array, Output, Screen, Keyboard, Memory, and Sys: 8 Jack classes. The Memory allocator and String library show the course's deliberate boundary especially well. They are enough to support Jack programs, but there is no process isolation, filesystem, or networking; the “OS” is closer to a runtime library than a modern kernel.

### Course materials

The [software](https://www.nand2tetris.org/software) supplies browser and Java tools and lets an official implementation temporarily replace an unfinished layer. That makes debugging unusually clear: run the same minimal Jack program through a personal compiler, VM translator, and assembler, then observe which substitution makes the error disappear.

The official [home](https://www.nand2tetris.org/) provides free specifications and tools, while the [license](https://www.nand2tetris.org/license) asks learners not to publish solutions. Translator, compiler, OS, and Jack-application source should therefore remain in a private repository. The most satisfying point in Part II is seeing a Jack application pass through the compiler, VM, assembler, and Hack machine while still being able to explain which layer supplies `Sys.init`, the call frame, the heap object, and screen output.

## Course Resources

- [Code · Nand2Tetris projects and software suite](https://www.nand2tetris.org/software)
- [Course home](https://www.coursera.org/learn/nand2tetris2)

## Resource Summary

Every public entry point verified in this review is listed above. Use the feedback and corrections links below to submit a completion record, another resource, or a broken-link report.
