---
title: "Modern Robotics, Course 6: Capstone Project, Mobile Manipulation"
description: "Northwestern University's Modern Robotics, Course 6: Capstone Project, Mobile Manipulation closes the sequence with a complete simulated pick-and-place project, requiring all five prior courses and potentially paid access."
page_type: course
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: f74049b8d32f2cac -->

# Modern Robotics, Course 6: Capstone Project, Mobile Manipulation

[中文](../../../courses/robotics/082-modern-robotics-6.md) · [← Robotics and Autonomous Systems](index.md)

> Northwestern University's Modern Robotics, Course 6: Capstone Project, Mobile Manipulation closes the sequence with a complete simulated pick-and-place project, requiring all five prior courses and potentially paid access.

## Course position

| Attribute | Value |
|---|---|
| **Institution** | Northwestern University |
| **Course code** | Modern Robotics 6 |
| **Track** | [Robotics and Autonomous Systems](index.md) |
| **Tier** | A |
| **Role** | Supplement |
| **Level** | Intermediate |
| **Last reviewed** | 2026-07-28 |

## Why choose this course

Supplement course. A reliable option that can serve as a main course or strong alternative.

## Before you start

- Recommended foundation: Control Systems
- Recommended foundation: Programming and Engineering Computing
- Recommended foundation: Physics Foundations
- Course-sequence requirement: complete [Modern Robotics, Course 1: Foundations of Robot Motion](../robotics/077-modern-robotics-1.md) (Northwestern University Modern Robotics 1) first
- Course-sequence requirement: complete [Modern Robotics, Course 2: Robot Kinematics](../robotics/078-modern-robotics-2.md) (Northwestern University Modern Robotics 2) first
- Course-sequence requirement: complete [Modern Robotics, Course 3: Robot Dynamics](../robotics/079-modern-robotics-3.md) (Northwestern University Modern Robotics 3) first
- Course-sequence requirement: complete [Modern Robotics, Course 4: Robot Motion Planning and Control](../robotics/080-modern-robotics-4.md) (Northwestern University Modern Robotics 4) first
- Course-sequence requirement: complete [Modern Robotics, Course 5: Robot Manipulation and Wheeled Mobile Robots](../robotics/081-modern-robotics-5.md) (Northwestern University Modern Robotics 5) first

## Verifiable learning outcomes

- Explain the core models in Robotics and Autonomous Systems, including their assumptions and limits
- Solve representative derivations and problems, checking units, limiting cases, or numerical results
- Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification

## Workload and pacing

**2 weeks at 10 hours/week.** The provider publishes 2 weeks at 10 hours per week. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.

## Software, hardware, and cost

### Software

- Maintainer-suggested open-source/free verification path: ROS 2, Gazebo, RViz 2, Python or C++, and a version-pinned container environment
- The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable

### Hardware

- The resource inventory lists lab coverage, but this course's maintainer path explicitly limits it to computational or simulation work. It assumes only a general-purpose computer able to run the software above and retain results; do not purchase or connect a course-supported robot platform, sensors, low-voltage power, emergency stop, and safe test area

### Cost note

The current maintainer path uses computation and simulation only, with no dedicated hardware purchase, and prefers open-source/free tools. This is not a provider requirement; platform, commercial-software, or cloud-compute costs still vary by provider, region, and plan.

## Safety level

**Simulation only.** The default practice scope is software, computation, or simulation only; a lab label in the resource inventory does not authorize connecting physical equipment, and any hardware extension requires provider-scope verification and a new risk assessment.

## Public resource coverage

| Resource type | Completeness |
|---|---|
| Video | Complete |
| Notes | Complete |
| Practice | Complete |
| Labs | Complete |
| Exams | No public material |
| Code | Complete |

## Resources and access

| Resource | Access | License | Status | Verified |
|---|---|---|---|---|
| [Course home](https://www.coursera.org/learn/modernrobotics-course6) | Registration required | Coursera Terms of Use | Listed by official page | 2026-07-28 |

> “Listed by official page” means the link was discovered on a successfully fetched official source on the verification date; it does not guarantee that every region or account can open the target directly. Access does not grant redistribution rights. Re-check the provider page, target link, and third-party notices before downloading, adapting, or publishing material.

## Practice loop

### Modern Robotics, Course 6: Capstone Project, Mobile Manipulation · Northwestern University Modern Robotics 6: Robot Task Planning and Safe-Degradation Simulation

This is a maintainer-suggested self-study project for Modern Robotics, Course 6: Capstone Project, Mobile Manipulation · Northwestern University Modern Robotics 6, not an official course assignment. Complete a perception–planning–control task in simulation for Robotics and Autonomous Systems, quantifying success rate, collision margin, localization error, and safe stop after sensor failure.

**Origin:** Maintainer-suggested project

**Deliverables**

- A specification of task, robot and environment models, frames, constraints, and safe state
- Perception, planning, control, monitoring, and scenario-generation sources
- Raw trajectories, success or collision labels, minimum clearance, and runtime for at least 100 randomized scenes
- A report and screen recording comparing baseline and improved methods and reviewing the most hazardous failure

**Verification**

- Achieve at least 90% success over 100 nominal scenes with zero collisions and the predeclared minimum clearance
- Cover coincident start and goal, infeasible maps, narrow passages, localization drift, and sensor interruption
- Replay every trajectory through an independent collision checker and cross-check frame by frame
- Inject frozen sensing or control delay and show the monitor reaches a stopped state within the specified time

**Reproducibility**

- Commit robot and world models, algorithms, scenarios, tests, and recording scripts
- Pin simulator, physics step, maps, random seeds, and dependency versions
- Preserve raw trajectories and sensor data, scenario manifests, and the generated report

**Safety boundary:** Simulation only — Use robot simulation only; do not drive real mechanisms, vehicles, drones, or actuators without qualified supervision.

## Risks, gaps, and boundaries

The complete simulated pick-and-place capstone assumes all first five courses, and full Coursera access may require payment.

## Completion evidence

- Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts
- Design-review package with requirements and constraints, trade-offs, editable sources, applicable ERC/DRC/timing/stability checks, exports, and a reproduction test
- Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes
- Simulation package with model or netlist, inputs, solver and version, parameter-sweep script, benchmark comparison, expected results, and one rerun command
