---
title: "Control, Robotics, and Autonomous Systems"
description: "Close a perception–planning–control loop in simulation first, then move to low-energy hardware only when safe, using stability, trajectory error, and failed cases to describe system performance."
page_type: route
route_id: "route-control-robotics"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: e8f2e65ee77210f6 -->

# Control, Robotics, and Autonomous Systems

## Audience

Learners who want dynamics, state estimation, planning, and feedback control to work together in one robotic system

## What you should be able to do

Close a perception–planning–control loop in simulation first, then move to low-energy hardware only when safe, using stability, trajectory error, and failed cases to describe system performance.

## Name the plant before choosing a controller

Choose a plant whose equations of motion you can write, such as an inverted pendulum or differential-drive robot. State its state, input, output, units, and operating point. If controllability or open-loop stability after linearization is unclear, do not open a robotics course yet.

Begin with the same plant's physical equations, parameter identification, and held-out trajectory; evaluate the controller on trajectories not used for fitting.

## Close the control loop before entering robotics

- Before writing the control law, state the stability argument, actuator saturation, and noise model. Choose 6.241J for continuous control or 6.231 only for stochastic sequential decisions.
- At the robotics stage, choose one complete path—MIT 6.4210 to 6.832 or Modern Robotics 1 through 6—and retain the same plant, controller, and injected failures.

## Defer platform complexity until the model can support it

- With secure differential equations, linear algebra, and mechanics, begin at the identification task; do not repeat multiple control surveys merely to align notation.
- Skip robotics for a control-only goal, and skip physical deployment without safe hardware and shutdown conditions. A completed simulation remains valid.

## Accept measured failures, not demo polish

- The simulation exit requires repeatable held-out trajectory error, stability limits, saturation and sensor-noise results, plus at least one retained controller failure.
- The robotics exit additionally requires the chosen complete path's planning-control loop to survive disturbance and recovery scenarios. Physical hardware is conditional, not the default acceptance.

!!! warning "Check these course materials before starting"
    - [Feedback Systems: An Introduction for Scientists and Engineers](../courses/control-systems/073-cds-101-cds-110.md): The author-maintained second-edition companion provides the open text, examples, exercises, and updated Python figure sources, but it is not a complete current course run; the instructor exercise manual remains restricted. Last checked: 2026-07-29.

## How to proceed

### From a physical plant to a state model

**Why these courses:** Keep one mechanical or electromechanical plant throughout. Use 18.03SC for its equations of motion, 18.06SC for the linear algebra, 8.01SC to derive the model from force and energy assumptions, and EE 263 to express it through state space, least squares, and dynamical-systems tools. Each mathematical idea then has a physical use instead of becoming an isolated course exercise.

- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **Required**; MIT
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **Required**; MIT
- [Classical Mechanics](../courses/physics/010-8-01sc.md) — **Required**; MIT
- [Introduction to Linear Dynamical Systems (2008 Archive)](../courses/control-systems/068-ee-263.md) — **Required**; Stanford University

**Move on when:** Derive a multistate model from physical assumptions, identify its parameters, and validate it on a trajectory excluded from fitting. Before fitting, set allowed state-prediction error from sensor noise, sampling error, and model approximation. Report normalized error and failure regions, together with controllability and observability rank checks.

### Feedback and optimal control

**Why these courses:** Apply 6.302 directly to the identified plant, parameter range, and held-out trajectory from the preceding work. Choose 6.241J for greater depth in continuous systems and state space, or 6.231 when the problem is sequential decision-making and stochastic optimal control. Caltech CDS 101/110 can unify notation and perspective, but it does not replace the chosen branch's problems and controller implementation.

- [Feedback Systems](../courses/control-systems/067-6-302.md) — **Required**; MIT
- [Dynamic Systems and Control](../courses/control-systems/069-6-241j.md) — **Choose 1**; MIT
- [Feedback Systems: An Introduction for Scientists and Engineers](../courses/control-systems/073-cds-101-cds-110.md) — **Use if needed**; Caltech; **Check material limits**
- [Dynamic Programming and Stochastic Control](../courses/control-systems/072-6-231.md) — **Choose 1**; MIT

**Move on when:** Implement a classical or optimal controller for the same plant and record gain margin, phase margin, overshoot, and settling time. State the parameter-uncertainty range first, then test its boundary corners and a reproducible sample sized by the coverage method or desired confidence interval. List every unstable case and explain the worst stable case.

### Robotic systems

**Why these courses:** Complete one coherent path. The MIT path runs 6.4210 then 6.832 for manipulation and underactuated systems; the Modern Robotics path runs Courses 1–6 in order and may require paid platform access. Whichever path is chosen, bring the existing plant, controller, and tests into the robotics problem. Finishing here means completing the chosen sequence in order, not earning a course credential, and two half-routes do not make one complete path.

**Complete path — MIT Robotics path (take these in the listed order)**

1. [Robotic Manipulation](../courses/robotics/074-6-4210.md) — **Course in this path**; MIT
2. [Underactuated Robotics](../courses/robotics/075-6-832.md) — **Course in this path**; MIT

**Complete path — Complete Modern Robotics path (Courses 1–6 in order; full platform access may be paid) (take these in the listed order)**

1. [Modern Robotics, Course 1: Foundations of Robot Motion](../courses/robotics/077-modern-robotics-1.md) — **Course in this path**; Northwestern University
2. [Modern Robotics, Course 2: Robot Kinematics](../courses/robotics/078-modern-robotics-2.md) — **Course in this path**; Northwestern University
3. [Modern Robotics, Course 3: Robot Dynamics](../courses/robotics/079-modern-robotics-3.md) — **Course in this path**; Northwestern University
4. [Modern Robotics, Course 4: Robot Motion Planning and Control](../courses/robotics/080-modern-robotics-4.md) — **Course in this path**; Northwestern University
5. [Modern Robotics, Course 5: Robot Manipulation and Wheeled Mobile Robots](../courses/robotics/081-modern-robotics-5.md) — **Course in this path**; Northwestern University
6. [Modern Robotics, Course 6: Capstone Project, Mobile Manipulation](../courses/robotics/082-modern-robotics-6.md) — **Course in this path**; Northwestern University

**Move on when:** Close the perception–planning–control loop in simulation first. State the success target, perturbation distribution, and desired confidence-interval precision before choosing the trial count. Report success with its interval, trajectory error, every failure, and every observed collision; zero collisions in a finite test is not a safety guarantee. Physical transfer is limited to low-energy, speed-limited, guarded hardware with an emergency stop after the same scenarios pass in simulation. Count every safety stop as a task failure.
