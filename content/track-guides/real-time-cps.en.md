## Read Colorado's four courses through their official assessment chain first

The [ECEA 5315 page](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/curriculum/computer-engineering-embedded-systems/ecea-5315-concept-and-practices) assigns 10% to quizzes, 30% each to programming and peer review, and 30% to the final, so [Real-Time Embedded Systems 1](063-real-time-embedded-systems-1.md) tests timing through code, review, and exam. [5316](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/curriculum/computer-engineering-embedded-systems/ecea-5316-theory-and-analysis) and [5317](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/curriculum/computer-engineering-embedded-systems/ecea-5317-mission-critical-sw) each assign 10% to quizzes, 60% jointly to programming/review, and 30% to the final. They map to schedulability in [Theory and Analysis](064-real-time-embedded-systems-2.md) and ECC, flash, redundancy, and FMEA in [Mission-Critical Systems Design](065-real-time-embedded-systems-3.md); the official pages give no finer split.

The [ECEA 5318 page](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/curriculum/computer-engineering-embedded-systems/ecea-5318-real-time-embedded) specifies a camera visual-synchronome [Project](066-real-time-embedded-systems-4.md), not a free-form capstone: 5 peer reviews are 50%, 3 quizzes 15%, and 1 Hz/10 Hz programming plus two final rate tests 35%. Stop after 5316 for scheduling; add the reliability course and then 5318 only when those outputs are needed. Graders, starters, peer review, and hardware may require paid registration.

Programming tests implementation, peer review an explainable design, and quizzes/finals timed individual analysis. Keep public material, independent exercises, and platform grades separate; a lecture download and thread demo do not reproduce all three.

## EECS 149 explains model composition; Colorado makes timing constraints concrete

[Berkeley EECS 149](060-eecs-149.md) uses an open text to connect computation models, embedded implementation, sensing/actuation, networking, and feedback. Its recordings, hardware, and tools are dated, so follow model relationships rather than recreate the platform. Colorado 5315/5316 assess periods, deadlines, priorities, blocking, and schedulability; 5317 adds reliability and 5318 a camera-rate pipeline.

[Embedded systems](../embedded-systems/index.md) should cover C, interrupts, timers, concurrency, memory-mapped I/O, and hardware observation. [Signals and systems](../signals-systems/index.md) supplies sampling, state, stability, and feedback. Real-time work establishes a testable relation among release, response, deadline, and sample age.

EECS 149 asks who produces an event, under which time semantics it is consumed, and how software exchanges state with a plant. Colorado turns that semantics into a task set: periodic/sporadic releases, execution budgets, priorities, and shared-resource blocking. The model explains why time matters; response-time reasoning tests one configuration.

## Begin periodic work with absolute release times and complete timestamps

Define two periods and explicit release, start, finish, deadline, priority, shared resources, and overrun behavior. Use a monotonic clock and absolute releases to avoid accumulated sleep drift. Trace preemption, blocking, priority inversion, or a cache/page fault. Mean, 99.9 percentile, and observed maximum answer different questions; an ordinary-Linux maximum is not WCET proof.

Predict with utilization, response-time analysis, or a schedule table, then compare idle and controlled load. Finish times alone cannot distinguish late dispatch, overrun, and missing samples. State duration, sample count, lost records, clock error, load range, and instrumentation overhead before interpreting “no miss.”

Join release, dispatch, preemption, resume, and completion by job ID and compute deadline-minus-completion slack. Put shared-resource intervals on the same axis to identify the lock holder behind an inversion. A measured maximum may challenge a WCET estimate, but their sources and applicable machine configurations remain separate.

## Tracing cost, kernel configuration, and actuator safety belong on the same page

State kernel, architecture, compiler, policy, priority, CPU affinity, clock, frequency scaling, background load, and logging. Compare latency with tracing on and off. Containers stabilize user-space packages but not interrupt latency, drivers, or CPU power states; general-purpose Linux measurements describe one configuration and window, not a hard-real-time guarantee.

Before an actuator, test timeout, watchdog, and safe state in plant simulation or low-energy hardware-in-the-loop. Physical systems need mechanical limits, speed/current bounds, manual stop, and a default after communication loss. Classroom FMEA is not certification; timing analysis and safeguards inform but do not replace each other.

Treat tracing as workload: flushes, console output, and timestamps may lengthen the critical path. Compare memory buffering with batched export and label distribution shifts as perturbation. Distinguish stale samples, late commands, and command loss; define safe-state triggers, reset, and physical limits outside controller logic.

## Non-CU project: induce a deadline miss and trace it into plant output

**This `sense → estimate/process → control → actuate` pipeline is a site-authored exercise, not a 5315–5318 assignment or assessment substitute.** For a simple plant, tabulate period, deadline, priority, shared resources, and WCET estimate; log release/start/finish, latency, jitter, misses, state estimate, and control output. Under controlled load, inject overrun, priority inversion, message delay, or sensor dropout separately.

Trace effects on sample age, estimation error, saturation, or plant state and add replay after correction. When also studying Mission-Critical Systems Design, separate severity, occurrence, detection, and mitigation. Change one period or workload, predict misses and control response, then rerun. Include task model, analysis, timestamps, raw distributions, build command, fallback, and localization; keep it distinct from Colorado's camera project.

Align job release/blocking/completion above sample age/controller output/plant state. Injection-to-deviation delay separates scheduler delay, estimator lag, and plant inertia. Target that mechanism with a shorter critical section, revised priority, or sampling policy. If only lower plotting rate removes the miss, observer load changed; the original question remains.
