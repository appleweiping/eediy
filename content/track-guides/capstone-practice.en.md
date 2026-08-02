## Three public archives describe three different project studios

[Cornell ECE 4760 / 5730](057-ece-4760-ece-5730.md) is organized around an embedded product. Its [current course site](https://ece4760.github.io/) uses the RP2350 and Pico 2, with labs, demonstrations, and years of student project pages joining implementation, measurement, and presentation. The [public Cornell ECE 3400 archive](https://ocw.ece.cornell.edu/courses/ece-3400-ece-practice-and-design) uses a maze robot to connect mechanics, circuits, perception, and software, although lectures, assessment, and several links are incomplete. The [2005 MIT 6.270 page](https://ocw.mit.edu/courses/6-270-autonomous-robot-design-competition-january-iap-2005) publishes Assignments 1–7, team process, and competition work, while its controller and sensors are historical hardware.

These are not three instances of one universal capstone template. Follow the ECE 4760 lab-to-project rhythm for an MCU product, the subsystem interfaces of [ECE 3400](062-ece-3400.md) for a mobile robot, or the strategy, division of work, and event constraints of [6.270](076-6-270.md) for a short competition. One real problem setting is more useful than a merged shopping list.

## ECE 4760 earns its value through a sequence of small implementations

The current ECE 4760 pages expose RP2350 and Pico 2 labs, C examples, video demonstrations, and student archives. Their value is not a project to copy, but the movement from timing, peripherals, and communication toward an output that can be measured. An independent topic should connect sensor→state transition→observable output early, with input range, units, update rate, abnormal state, and one external measurement defined at the interface.

[Electronics laboratory](../electronics-laboratory/index.md) contributes current-limited power, measurement, and wiring. [Programming and tools](../programming-tools/index.md) contributes a rebuildable environment, tests, and version history. [Embedded systems](../embedded-systems/index.md) contributes interrupts, timers, drivers, and concurrency. A build that works only through undocumented steps on its author's machine is first a tooling problem. A symptom that cannot be separated into software state and electrical input needs observation on both sides of the interface, not a cloud service or vision model.

## ECE 3400 and 6.270 emphasize physical integration and team cadence

A maze robot places motors, power, sensing, localization, and strategy in one constrained space. Integration can follow physical coupling: establish power and emergency stop, attach one drive, let one sensing channel control one action, and only then add mapping or planning. Dividing a team into mechanical, electrical, and software silos until final assembly delays the most important interface questions. Organizing around running subsystem slices exposes them earlier.

The public 6.270 assignments show how decisions and tests are compressed into a short schedule, but the 2005 controller, sensors, and arena are not current purchasing advice. Competition results, residential guidance, and team feedback are also unavailable off campus. A strategy comparison can use fixed starting conditions in simulation or a safe arena, with randomness, collision rules, and scoring stated. Scores from different hardware, maps, and software versions do not belong in one unconditional ranking.

## Age, substitutions, and energy boundaries are part of the design

The RP2350/Pico 2 setting, ECE 3400 robot kit, and 6.270 controller belong to different years and access conditions. A BOM needs revision, datasheet, voltage and current, mechanical interface, compiler or SDK, license, spare, and a substitution check. A new sensor, driver, or board can change electrical, timing, and mechanical behavior; compare the decisive interfaces on a small fixture before choosing the scope of a port.

Physical work stays low voltage and current limited. Motors, batteries and chargers, moving mechanisms, optical emitters, and high-current drivers each need energy bounds, pinch, fire, or eye precautions, and an emergency stop. An action that cannot be tested safely becomes a dummy load, bench fixture, or simulation. Peers outside a class can discuss a design and watch a demonstration, but they cannot provide Cornell or MIT credit, competition standing, or qualified on-site safety supervision.

Safety conditions should change project scope directly instead of appearing only at the end of the report.

## The least-explained interface points to the project's next subject

A transferable project builds and flashes from a clean environment and exposes its source, schematic or pin map, BOM, interface notes, test inputs, raw traces, demonstration, and short postmortem. There is no universal requirement for a PCB, cloud service, or complicated mechanism. A course-specific endpoint might be an RP2350 peripheral measurement, one maze-robot integration result, or a strategy comparison under explicit competition rules.

Use the postmortem to select one interface whose input, output, and failure evidence are still incomplete, then turn it into the first question of the next course. A timer, driver, memory, or concurrency trace belongs in embedded systems; a calibration residual belongs in instrumentation or DSP; an estimation or dynamics mismatch belongs in robotics or control; repeated power or signal-integrity faults return to laboratory design. This handoff reuses the same trace and subsystem instead of relabeling the project as a larger generic capstone.
