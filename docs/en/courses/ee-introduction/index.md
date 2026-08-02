---
title: "Introduction to Electrical Engineering"
description: "Survey courses spanning circuits, signals, computation, and electromechanical systems, with early system-building practice."
page_type: track
track_id: "track-ee-introduction"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 2fe551f0b877bd77 -->

# Introduction to Electrical Engineering

## Track position

Survey courses spanning circuits, signals, computation, and electromechanical systems, with early system-building practice.

## Recommended prerequisite tracks

- [Engineering Mathematics](../mathematics/index.md)
- [Programming and Engineering Computing](../programming-tools/index.md)

## 6.01SC enters through state and programs; 6.007 through energy and fields

The [official MIT 6.01SC archive](https://ocw.mit.edu/courses/6-01sc-introduction-to-electrical-engineering-and-computer-science-i-spring-2011) places Python, state machines, signals, circuits, probabilistic robotics, and software organization in one set of materials. [6.01SC](019-6-01sc.md) suits a learner who has not selected a concentration and wants programs to connect abstraction layers. The robot platform and some software are dated and are poor literal purchasing advice; the durable subject is how a model enters implementation and testing.

The [official MIT 6.007 page](https://ocw.mit.edu/courses/6-007-electromagnetic-energy-from-motors-to-lasers-spring-2011) builds a different picture of EE from electromagnetic energy, actuators, sensing, transmission, and optoelectronic systems. [6.007](020-6-007.md) exposes field, geometry, and energy questions early for motors, power, RF, devices, and photonics. Its public videos are mainly demonstrations, its problems have no solutions, and it has no public exams, so the 6.01SC definition of completion does not transfer. Usually choose one entrance and draw one relevant chapter from the other.

## Two small questions are enough to choose an entrance

The starting background is modest: basic calculus, vectors, and units from [engineering mathematics](../mathematics/index.md) should be usable, and [programming tools](../programming-tools/index.md) should support a small tested program. Use 6.01SC for a state-machine→sensor-model→controller loop. Use 6.007 to draw energy flow and derive an order-of-magnitude estimate for a motor, transmission, or optical-sensing example. Each piece should expose its code or derivation, input conditions, and one observation that disagreed with the prediction.

If a program runs but the interaction among sensor, actuator, and feedback remains unclear, the 6.01SC system route is the better entrance. If circuit equations are familiar but a device cannot be explained through energy, fields, and geometry, 6.007 is more useful. Neither course is a shortcut when mathematics and programming are both weak; an introduction cannot replace physics, circuits, and tools in a short interval.

Then build one safe object containing only two subsystems: a simulated mobile robot, low-voltage optical sensor, software communication link, or fully simulated motor. The system boundary, inputs and outputs, state or energy flow, decisive assumptions, and three to five end-to-end tests matter more than feature count. A simulation-only result is valid when its data source, simulation boundary, and unverified hardware behavior are explicit.

## The first unexplained interface chooses the next course

Repeated trouble with KCL, KVL, initial conditions, or device operating points points to [circuit analysis](../circuits/index.md). Convolution, sampling, noise, or filters point to [signals and systems](../signals-systems/index.md). Geometry, boundary conditions, or energy propagation point to [electromagnetics](../electromagnetics/index.md). Builds, tests, and data structures point back to programming tools.

Justify the direction with one interface from the small project: a missing model, a prediction that reversed, or units that could not be reconciled. An animation, sensor reading, or smooth demonstration cannot answer those questions by itself. The introduction has done useful work when one small system can explain what to learn next, why, and which physical behaviors have not yet been tested.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Introduction to Electrical Engineering and Computer Science I](019-6-01sc.md) | MIT | Main course | Public-material guide | Public assignments or labs |
| [Electromagnetic Energy: From Motors to Lasers](020-6-007.md) | MIT | Alternative | Public-material guide | Partial or restricted |
