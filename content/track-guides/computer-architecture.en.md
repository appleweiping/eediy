## CS 61C descends from C; ECE 4750 builds upward from a pipeline

[Berkeley CS 61C](048-cs-61c.md) places C, RISC-V, memory hierarchy, parallelism, and projects at the hardware/software boundary. Its [department course page](https://www2.eecs.berkeley.edu/Courses/CS61C/) gives stable scope and prerequisites; official Fall 2024 lab/project starters remain public, while the old calendar, discussions, homework, recordings, and grading have moved behind campus services. [Cornell ECE 4750](046-ece-4750.md) concentrates on RISC-V design. Its [public handout page](https://www.csl.cornell.edu/courses/ece4750/handouts.shtml) supplies notes, problems, and lab descriptions, while team repositories, servers, and some starters are not anonymously available. Choose 61C for a software-oriented learner who has not followed a program into hardware, or 4750 for someone already comfortable with HDL who wants to design a datapath and pipeline.

[MIT 6.823](047-6-823.md) is a historical advanced archive for deeper pipeline, memory, and parallelism work after a spine. [Nand2Tetris II](040-nand2tetris-ii.md) develops the VM, compiler, and OS software layers rather than modern microarchitecture. [6.1810](054-6-1810.md) carries RISC-V xv6 into page tables, system calls, and device interfaces and fits best after processors and caches make sense.

Both first routes should end at the same handoff: explain a program down to cycles and memory accesses. Timing software without following the hardware, or reading RTL waveforms without the originating program semantics, leaves half of that interface unaccounted for.

## Carry one instruction through C, the ISA, and control signals

[Digital logic](../digital-logic/index.md) should already cover datapaths, FSMs, pipeline registers, and memory interfaces. [Programming and tools](../programming-tools/index.md) should support C pointers, bit operations, assembly, version control, and automated tests. Choose a short RISC-V program containing a load, branch, and function call. Trace registers, memory, PC, and calling convention, then map one instruction through decode, control, ALU, memory, and writeback.

Mark data and control hazards in a five-stage pipeline and name the exact forwarding, stall, and flush cycles. Confusion about undefined C behavior, stack and heap, or binary representation calls for systems-programming work. A broken instruction-to-signal mapping calls for digital logic. Using one program for the whole exercise prevents software semantics and hardware timing from being studied separately while their interface remains unexplained.

The function call brings register convention, stack frame, and return address into the trace; the branch connects software-visible control flow to pipeline flushing. Those are the two places where abbreviated notes most often omit an assumption between abstraction layers.

## A cache experiment must separate work, cycles, and clock

Implement a cache simulator or use a public skeleton to compare size, associativity, block size, and replacement policy. Split addresses into tag, index, and offset; calculate a short trace and AMAT by hand; then check the implementation with a reference model and randomized tests. On one workload, report instruction count, cycles, CPI, clock estimate, misses or stalls, wall time, warm-up, and repeat count. Add a reference output or functional hash so an incorrect result cannot look fast by doing less work.

An optimization that hurts performance can be especially informative. Follow specification→code or RTL→test→counter to decide whether misses fell while the critical path grew, or whether locality contradicted the hypothesis. Simulators can define cycles, caches, and timing differently, so align observation semantics before comparing them. A parameter sweep labeled only “faster” does not answer an architecture question.

## 6.823 and xv6 push bottlenecks toward hardware and the OS

The ISA, tools, and performance examples in 6.823 are dated; a port should retain the architecture question while updating simulator and toolchain separately. The [official 2023 MIT 6.1810 archive](https://ocw.mit.edu/courses/6-1810-operating-system-engineering-fall-2023) publishes RISC-V xv6 code and labs but no complete video and public grading sequence. `xv6-labs-2023` is the repository, while `util`, `syscall`, and similar names are the lab branches; reversing those descriptions creates an unusable setup. An external reconstruction uses public interfaces and identifies itself as independent or ported work.

Pipelines, branch prediction, and memory consistency point toward 6.823. Page tables, interrupts, system calls, and device drivers point toward xv6. Interest in how a compiler or VM creates instructions points toward Nand2Tetris II or compilers. Course code can start the problem, but it does not define the compiler, flags, workload, reference output, and counter semantics for an independent environment.

## The final check is one predictable structural change

A small core or simulator should expose its ISA and interface specification, directed and randomized tests, traces, and a minimized counterexample. Before adding an instruction or changing a cache parameter, list the affected decode, datapath, state, tests, and counters; afterward, compare prediction with observation. State the environment commit, compiler, flags, and commands rather than implying use of an unavailable institutional autograder.

Put the prediction and observation for one specification change in the same table, with rows for decode, datapath, architectural state, tests, and counters. The first row that cannot be explained selects the follow-on work: RTL timing or verification returns to digital implementation, compiler or VM semantics goes up the software stack, an OS-boundary mismatch goes to 6.1810, and pipeline or cache behavior goes to advanced architecture. That table is the handoff; another benchmark run is useful only if it isolates the unexplained row.
