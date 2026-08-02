---
title: "Modern Robotics, Course 2: Robot Kinematics"
description: "Northwestern University's Modern Robotics, Course 2: Robot Kinematics develops robot kinematics through videos, notes, practice, simulation, and code; the provider highly recommends the series order because this course builds on Course 1, and full access may be paid."
page_type: course
course_id: "course-078"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: ca3821751fc34bf2 -->

# Northwestern University Modern Robotics 2: Modern Robotics, Course 2: Robot Kinematics

## Course Overview

- **University:** Northwestern University
- **Course code:** Modern Robotics 2
- **Official prerequisites:** The Coursera specialization page says Courses 1–6 are highly recommended in order because the material builds on itself
- **EEDIY preparation:** Study Course 1's SE(3), twists, adjoints, and matrix exponential/logarithm first; the series is best followed in order, but the provider does not state a hard prerequisite
- **Access:** Open entry; some materials require registration or are limited
- **Material status:** 2026-07-30; public-material guide

### A hand-worked 2R oracle connects rigid-body language to manipulators

Coursera [Robot Kinematics](https://www.coursera.org/learn/modernrobotics-course2) corresponds to *Modern Robotics* Chapters 4–7: forward kinematics, velocity kinematics/statics, inverse kinematics, and closed chains. The [book home](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) provides the common preprint and errata. It fits learners who already command Course 1’s rigid-body language; if SE(3), twists, adjoints, and exp/log still require guessing transposes, revisit Chapter 3.

A 2R planar arm makes the prerequisites concrete: calculate the home configuration, space/body screw axes, forward kinematics, Jacobian, and a singular pose, then verify \(J\dot\theta\) by finite differences.

### POE, Jacobians, and IK share the same 2R arm

Chapter 4 writes space and body forward kinematics with the product of exponentials; with a consistent home pose and screw definitions, both must give the same \(T\). Chapter 5 derives Jacobians, wrench/torque relations, singularities, and manipulability. Check rank/singular values for non-square Jacobians and state scaling when angular and linear velocity units mix.

Chapter 6 numerical IK must report initial guess, frame convention, angular/linear tolerances, iteration count, and termination. Test reachable, unreachable, near-singular, workspace-boundary, and multiple-solution targets. In Chapter 7, write the loop-closure constraint, passive coordinates, and constraint Jacobian, then verify first-order residuals for allowable numerical perturbations.

The IK matrix should separate “converged to a different valid solution” from “algorithm failure.” Across fixed initial guesses, retain final joint angles, terminal rotation/translation error, minimum singular value, and termination cause. Near singularity, observe whether the update suddenly grows. If damping or a step limit is introduced, show the original failure beside the modified result rather than retaining only the final successful pose.

### Explain every official function input and output

The [ModernRobotics repository](https://github.com/NxRLab/ModernRobotics)
supplies `FKinSpace(M,Slist,thetalist) → T`,
`JacobianSpace(Slist,thetalist) → J_s`, and
`IKinSpace(Slist,M,T,thetalist0,eomg,ev) → (thetalist, success)`. Follow the
[library setup](https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_Modern_Robotics_Code_Library)
and pin the language, commit, and dependencies. Cross-check each interface
with a 2R hand result, library output, and small-\(\Delta t\) finite
difference. When they disagree, inspect axes, frames, and exponential order
instead of relaxing tolerance.

[Official Course 2 assignments and resources](https://hades.mech.northwestern.edu/index.php/Coursera_Resources) form the coursework and version hub. Keep the UR5 home pose, screw axes, joint order, and units as version-controlled data. Verify equal space/body forward kinematics at fixed random joint angles before running IK.

On load, validate every rotation block, matrix dimension, and \(q=0\) configuration. Random regression should cover ordinary poses plus fully extended, folded, and near-joint-boundary cases. Perturb each joint slightly and recover the predicted twist from the end-effector transform increment. This catches axis direction, joint ordering, and adjoint-direction mistakes even when the animation still resembles plausible arm motion.

### The UR5 CSV is the numerical export boundary

The [CoppeliaSim setup](https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_CoppeliaSim_Simulator) supplies a UR5 CSV scene. Before exporting each waypoint, calculate forward-kinematics error, minimum singular value, and joint jump. A successful animation still does not establish real joint limits, collision safety, calibration, or controller safety.

Solve and validate every waypoint independently before deciding how adjacent IK solutions connect. Simple interpolation may cross a joint limit, collision region, or discontinuous branch, so output joint increments and end-effector error together and retain rejected waypoints in the failure table. The scene should consume validated CSV; it should not silently repair numerical values during visualization.

The course record exposes five independent commands: 2R oracle, random regression, IK boundary matrix, closed-chain check, and scene export, with errata, library commit, scene, and tolerances recorded. No physical UR5 is required for the numerical objectives, and simulator precision cannot be converted into hardware accuracy.

Select one successful and one unreachable target and trace each from screw-axis
data through forward kinematics, Jacobian, IK iterations, and CSV output. Run
both with the same command and put reachability, conditioning, or iteration
budget beside the return value. An opaque `False` does not explain why IK
stopped.

## Course Resources

- [Course home](https://www.coursera.org/learn/modernrobotics-course2)
- [Code · Modern Robotics official software library](https://github.com/NxRLab/ModernRobotics)

## Resource Summary

Every public entry point verified in this review is listed above. Use the feedback and corrections links below to submit a completion record, another resource, or a broken-link report.
