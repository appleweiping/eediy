---
title: "Modern Robotics, Course 6: Capstone Project, Mobile Manipulation"
description: "Northwestern University's Modern Robotics, Course 6: Capstone Project, Mobile Manipulation closes the sequence with a complete simulated pick-and-place project that reuses earlier software and concepts; the provider highly recommends the series order, and full access may be paid."
page_type: course
course_id: "course-082"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 0b24533ac17d5b16 -->

# Northwestern University Modern Robotics 6: Modern Robotics, Course 6: Capstone Project, Mobile Manipulation

## Course Overview

- **University:** Northwestern University
- **Course code:** Modern Robotics 6
- **Official prerequisites:** The Coursera specialization page says Courses 1–6 are highly recommended in order because the material builds on itself
- **EEDIY preparation:** Complete Courses 1–5 first because the capstone reuses prior software plus trajectory planning, odometry, and feedback control; this is EEDIY's project-dependency study order
- **Access:** Open entry; some materials require registration or are limited
- **Material status:** 2026-07-30; public-material guide

### The youBot capstone connects three explicit interfaces into one transfer

Coursera’s [Mobile Manipulation Capstone](https://www.coursera.org/learn/modernrobotics-course6) is the specialization's sixth course and joins the first five in one pipeline. The [project specification](https://hades.mech.northwestern.edu/index.php/Mobile_Manipulation_Capstone) fixes a KUKA youBot with an omnidirectional chassis and 5-joint arm, moving a block to a target configuration in CoppeliaSim. It fits learners who can test kinematics, trajectories, feedback, and Chapter 13 base updates separately; otherwise the animation is difficult to debug.

Pin the [MR repository](https://github.com/NxRLab/ModernRobotics) language/commit, scene, and \(\Delta t\). Use the formulas on [Modern Robotics home](https://hades.mech.northwestern.edu/index.php/Modern_Robotics).

### The 3 milestones each have a numerical oracle

Milestone 1 `NextState` takes a 12-vector state (3 chassis, 5 arm, 4 wheel) and 9-vector controls (4 wheel, 5 joint), with an Euler update and speed clipping. In the official 1-second tests, forward and sideways motion are each about 0.475 m, rotation about 1.234 rad, and a speed limit reduced from 10 to 5 halves displacement. Test zero, single-joint, single-wheel, and clipping cases before writing the 13-column CSV.

Milestone 2 `TrajectoryGenerator` divides the path into 8 segments: approach, descend, grasp, rise, transfer, descend, release, and retreat. Define each segment’s pose, interpolation, duration, gripper state, and boundary-duplicate handling. Replay the reference alone before closing the loop.

Milestone 3 `FeedbackControl` computes a feedforward + PI body twist from \(X,X_d,X_{d,next},K_p,K_i,\Delta t\), then maps it through the mobile-manipulator Jacobian pseudoinverse to wheel/joint speed. Check the official fixture’s \(V_d\), adjoint, \(X_{err}\), \(J_e\), and controls before testing zero error, position-only, orientation-only, near-singular, and saturated cases.

The three modules communicate through explicit data. `NextState` does not read controller globals, each trajectory row has a fixed transform-and-gripper schema, and feedback returns error and command. Shape, finite-value, frame, and clipping assertions at the function boundaries let each milestone run without notebook history.

At trajectory boundaries, check pose continuity, monotonic timestamps, row count, and gripper transitions. Leave a stationary window around gripper actions so contact does not coincide with fast motion. If the reference swaps block and end-effector frames, no feedback gain can repair it.

### Judge the final run by its error log

Start the final experiment with at least 30° orientation error and 0.2 m position error, comparing feedforward-only, feedforward+P, and feedforward+PI. Show the 6-vector \(X_{err}(t)\), commands, saturation, condition number, configuration CSV, grasp/release times, and video in the same set of plots and logs. Scene 6 recommends 10 ms. Contact-engine slip can be discussed separately, but frame, CSV-order, and clipping mistakes cannot be blamed on physics.

Compare at least feedforward, P, and PI in the final run. Error at the end of the first segment, maximum error, command-saturation fraction, and final block pose are enough to expose the difference; then use one failed grasp to decide whether the cause was the reference, a frame, the Jacobian, saturation, or contact.

The [CoppeliaSim setup](https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_CoppeliaSim_Simulator) defines chassis/arm/wheel/gripper column order. The official example can check the playback chain; identify the simulator, physics engine, and scene hash beside your own output.

The official submission includes a README, authored or modified `code/`, runnable scripts for each task, and configuration, error, and video outputs. For independent study, a script that rebuilds the CSV and error plots plus the failed-grasp case says more about reliability than a seamless animation; record the configuration-column order, units, and scene version as well.

[Coursera Resources](https://hades.mech.northwestern.edu/index.php/Coursera_Resources) collects the public specification, preprint, code, and scene; peer assessment, certificate, and platform tests remain access-controlled. Success in the simulator does not establish calibration, motor current, physical contact, or perception on a real youBot.

If time is limited, finish all three milestones and one P/PI comparison before reducing gain sweeps and animation polish. A block that happens to land near the target is less useful than one failed trajectory you can explain.

## Course Resources

- [Course home](https://www.coursera.org/learn/modernrobotics-course6)
- [Code · Modern Robotics official software library](https://github.com/NxRLab/ModernRobotics)

## Resource Summary

Every public entry point verified in this review is listed above. Use the feedback and corrections links below to submit a completion record, another resource, or a broken-link report.
