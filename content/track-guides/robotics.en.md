## 6.4210 and 6.832 center on manipulation and underactuation

[MIT 6.4210](074-6-4210.md) connects geometry, kinematics, planning, perception, and grasping through 10 problem sets and a Drake final project on its [official OCW page](https://ocw.mit.edu/courses/6-4210-robotic-manipulation-fall-2022/). [MIT 6.832](075-6-832.md) studies dynamics, optimization, and controllers exploiting natural motion on its [official page](https://ocw.mit.edu/courses/6-832-underactuated-robotics-spring-2022/). They are independently complete: choose pick-and-place or swing-up/dynamic motion, not consecutive numbers.

Organize 6.4210 work as object pose, grasp feasibility, collision-free path, and execution, then join the manipulation pipeline. In 6.832, move from equations of motion to trajectory optimization, a stability argument, and simulation trace. Geometry/perception interfaces constrain the first route; model/controller interfaces constrain the second.

## Modern Robotics is the one strictly cumulative six-course sequence

[Course 1](077-modern-robotics-1.md) and [Course 2](078-modern-robotics-2.md) establish rigid motion, kinematics, and Jacobians; [Course 3](079-modern-robotics-3.md) adds dynamics, [Course 4](080-modern-robotics-4.md) planning/control, and [Course 5](081-modern-robotics-5.md) manipulation/mobile robots. The [Course 6 capstone](082-modern-robotics-6.md) assumes all five. The [Coursera entry](https://www.coursera.org/learn/modernrobotics-course1), [official wiki](https://hades.mech.northwestern.edu/index.php/Modern_Robotics), and [code repository](https://github.com/NxRLab/ModernRobotics) expose the platform, text, and library; grading, peer work, trials, and prices can change.

This route suits a learner who wants one notation from SE(3) through the youBot capstone; it need not be stacked with complete 6.4210 or 6.832 courses. [MASLab](061-6-186.md) serves only as a 2005 whole-robot competition reference. Its OrcPad, Java/CVS stack, kit, and field no longer form a reproducible course environment.

Use one library example to expose dependency. Courses 1/2 produce frames and kinematics; Course 3 adds inertia/forces; Course 4 path/controller; Course 5 mobile/manipulation subsystems; Course 6 joins them. When a capstone Jacobian or odometry interface is unclear, return to the course that created it rather than infer its definition from the final scene.

## Give frames, Jacobians, dynamics, and collision independent numerical checks

State, stability, feedback, and actuator limits from [control systems](../control-systems/index.md); mechanics, energy, friction, and contact from [physics](../physics/index.md); and linear algebra, tests, and replay from [programming tools](../programming-tools/index.md) become checks. For a 2R arm, implement forward kinematics and a Jacobian with explicit frames, units, and joint order. Finite-difference one column and verify twist-wrench power pairing; identity, zero motion, a small step, and a known singularity need determinate results.

Next implement a pendulum mass matrix, gravity term, and feedback simulation and check signs through energy and limiting poses. Calibrate collision on known intersecting and separated geometry and fix random-planner seeds. Animation cannot establish a frame, one library result cannot establish a Jacobian sign, and planning success depends on collision tolerance.

Keep coordinates consistent across checks: forward-kinematic pose, collision transforms, controller state, and logged joint order must come from one model. At a nonzero pose, verify position, velocity, kinetic energy, and actuator effort by hand or a second implementation. Any quantity supported only by animation lacks an automatic regression.

## Version live textbooks, paid assignments, and obsolete platforms separately

The 6.4210 Fall 2022 prompts, Drake/pydrake notes, and repositories evolve. State prompt year, commit, Python, and solver; some grading and feedback are closed. Current 6.832 notes, Drake examples, and Colabs likewise lack complete assignment feedback. Modern Robotics publishes its text, wiki, and library, while Coursera graders and peer review require platform access. V-REP is the former name of CoppeliaSim, so identify scene, CSV, and library versions together.

A modern simulator or robot can revisit the MASLab engineering problem but does not become the original platform. Simulation success does not establish physical collision geometry, friction, latency, or actuator saturation. Real robots require emergency stop, speed/current limits, a separated collision area, supervision, and manufacturer battery procedures; otherwise the work remains in simulation.

Version the robot description, visual and collision meshes, physics engine, time step, solver, controller frequency, and random seed. A coarse visual mesh or shifted origin can corrupt collision conclusions. After changing Drake, CoppeliaSim, or a library release, rerun fixed small kinematics, collision, and dynamics cases before attributing a high-level change to the algorithm.

## The most informative interface case is a successful plan that the controller cannot execute

Choose desktop pick-and-place, underactuated swing-up, mobile navigation, or youBot mobile manipulation. State the model, environment, frames, joint/actuator limits, planner-controller interface, and success metric. Create deterministic tests for kinematics, dynamics, collision, planning, control, and state update, then vary initial conditions, obstacles, or parameters and report success rate, tracking error, minimum clearance, effort, and runtime with seeds and raw logs.

Analyze a collision-free plan that fails from saturation, contact, or model mismatch. Reduce it to a waypoint, state, or interface and add replay after correction. Include model, source, scene, environment release, logs, replay command, and safety limits. A changed initial condition or obstacle should localize the fault to kinematics, collision, planning, or control; video is only a time index.

Define the handoff with trajectory timestamps, state convention, interpolation, and actuator bounds. Geometric waypoints omit velocity and acceleration, so dynamic execution may violate a limit despite collision-free geometry. Plot planned against executed clearance and commanded against saturated effort; the failed grasp then narrows to a reproducible interval at the planner-controller boundary.
