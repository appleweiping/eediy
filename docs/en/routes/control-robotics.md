---
title: "Control, Robotics, and Autonomous Systems"
description: "Close the perception–planning–control loop in simulation or on safe hardware, reporting stability, error, and failure modes."
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 04fcaf2df37ad360 -->

# Control, Robotics, and Autonomous Systems

[中文](../../routes/control-robotics.md) · [← Learning routes](index.md)

## Audience

Learners integrating dynamics, estimation, planning, and manipulation into autonomous systems

## Final outcome

Close the perception–planning–control loop in simulation or on safe hardware, reporting stability, error, and failure modes.

!!! warning "Mainline audit review in this route"
    - [Feedback Systems: An Introduction for Scientists and Engineers](../courses/control-systems/073-cds-101-cds-110.md): The author-maintained second-edition companion provides the open text, examples, exercises, and updated Python figure sources, but it is not a complete current course run; the instructor exercise manual remains restricted. Last audited: 2026-07-29.

## Stages

### Mathematics and dynamics

**Selection rule:** Complete all 4 required courses.

- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **Required**; MIT; Mainline; S
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **Required**; MIT; Mainline; S
- [Classical Mechanics](../courses/physics/010-8-01sc.md) — **Required**; MIT; Mainline; S
- [Introduction to Linear Dynamical Systems](../courses/control-systems/068-ee-263.md) — **Required**; Stanford University; Mainline; S

**Stage exit criterion:** Derive a multistate system from physical assumptions, identify its parameters, and validate on a trajectory excluded from fitting; normalized state-prediction error must be below 10%, with controllability and observability rank checks completed.

### Feedback and optimal control

**Selection rule:** Complete all 1 required course and choose 1 of 2 elective options. The other course is an optional supplement and does not count toward the elective requirement.

- [Feedback Systems](../courses/control-systems/067-6-302.md) — **Required**; MIT; Mainline; A
- [Dynamic Systems and Control](../courses/control-systems/069-6-241j.md) — **Elective option**; MIT; Alternative; A
- [Feedback Systems: An Introduction for Scientists and Engineers](../courses/control-systems/073-cds-101-cds-110.md) — **Optional supplement**; Caltech; Mainline; S; **Audit review**
- [Dynamic Programming and Stochastic Control](../courses/control-systems/072-6-231.md) — **Elective option**; MIT; Supplement; A

**Stage exit criterion:** Implement a classical or optimal controller for one plant, recording gain/phase margins, overshoot, and settling time; stability must hold across at least 100 parameter perturbations, with the worst-performing sample explained.

### Robotic systems

**Selection rule:** choose 1 of the 2 complete paths below and finish every course in the selected path in the listed order.

**Complete path option — MIT Robotics path (complete in the listed order)**

1. [Robotic Manipulation](../courses/robotics/074-6-4210.md) — **Course in selected path**; MIT; Mainline; S
2. [Underactuated Robotics](../courses/robotics/075-6-832.md) — **Course in selected path**; MIT; Mainline; S

**Complete path option — Complete Modern Robotics path (Courses 1–6 in order; full platform access may be paid) (complete in the listed order)**

1. [Modern Robotics, Course 1: Foundations of Robot Motion](../courses/robotics/077-modern-robotics-1.md) — **Course in selected path**; Northwestern University; Alternative; A
2. [Modern Robotics, Course 2: Robot Kinematics](../courses/robotics/078-modern-robotics-2.md) — **Course in selected path**; Northwestern University; Alternative; A
3. [Modern Robotics, Course 3: Robot Dynamics](../courses/robotics/079-modern-robotics-3.md) — **Course in selected path**; Northwestern University; Alternative; A
4. [Modern Robotics, Course 4: Robot Motion Planning and Control](../courses/robotics/080-modern-robotics-4.md) — **Course in selected path**; Northwestern University; Alternative; A
5. [Modern Robotics, Course 5: Robot Manipulation and Wheeled Mobile Robots](../courses/robotics/081-modern-robotics-5.md) — **Course in selected path**; Northwestern University; Alternative; A
6. [Modern Robotics, Course 6: Capstone Project, Mobile Manipulation](../courses/robotics/082-modern-robotics-6.md) — **Course in selected path**; Northwestern University; Supplement; A

**Stage exit criterion:** Close a perception-planning-control loop in simulation or on a safe platform, achieving at least 90% task success and zero collisions over twenty perturbed trials; submit the trajectory-error distribution and a failure-mode review.

## Execution rules

- Follow each stage's selection rule: complete every required course and the stated number of electives; when complete path options are provided, choose one and finish every course in its listed order; use optional supplements only to close a specific gap.
- Produce at least one reproducible artifact per stage and include failed attempts in the retrospective.
- Work involving mains voltage, high voltage, RF exposure, lasers, chemicals, or fabrication equipment requires local-law compliance and qualified supervision.
