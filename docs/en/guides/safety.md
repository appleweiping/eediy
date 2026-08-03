---
title: Laboratory Safety
description: Manage EE experiment risk with hazard identification, energy classes, stop conditions, and supervision boundaries.
---

<div class="ee-language" markdown>
[简体中文](../../guides/safety.md)
</div>

# Laboratory Safety

!!! danger "This page is not a safety qualification or work authorization"
    It helps identify risk but cannot replace institutional training, standard operating procedures, equipment manuals, a task-specific assessment, or qualified supervision. Follow the stricter rule when requirements differ. Without trained supervision, an appropriate facility, and confirmed ratings, do not work with mains electricity, exposed energized parts, high stored energy, powerful lasers, RF power, moving machinery, vacuum, high temperature, or hazardous chemicals.

Safety is not a paragraph added after the project. It is a design input that decides **whether to proceed, where, by whom, and how to stop**.

## Classify energy and hazards first

| Class | Typical activity | Default decision |
| --- | --- | --- |
| Green: software and passive analysis | Hand analysis, simulation, public data, de-energized visual inspection | Independent work is reasonable; protect data, vision, and ergonomics |
| Blue: bounded low-energy teaching work | Protected low-energy supply, known parts, conservative current limit | Proceed after ratings and wiring checks; have the first setup reviewed |
| Orange: specialist controls required | Larger battery packs, motors, heating, strong fields, solder fume, uncertain grounding | Written assessment, appropriate facility, and trained supervision |
| Red: outside unsupervised self-study | Mains, exposed high voltage/fault current, energized service, Class 3B/4 laser, RF transmit power, cleanroom chemistry | Authorized laboratory and qualified personnel under a formal procedure |

“Below a voltage threshold” does not mean universally safe. Stored energy, fault current, moisture, damaged skin, sharp probes, heating, motion, and battery chemistry can make low-voltage systems dangerous.

## Five questions that cannot be skipped

1. **Where can energy come from?** Include supplies, batteries, capacitors, inductive kick, inertia, heat, light, and pressure.
2. **How is it isolated and released?** Switched off is not necessarily discharged; define how the de-energized state is verified.
3. **What is the worst credible failure?** Short, reversal, heating, rupture, uncontrolled motion, beam reflection, fume, or software miscommand.
4. **Who is qualified to review it?** Identify the supervisor, facility rules, and stop authority.
5. **How do you exit an abnormal state?** Establish isolation, evacuation, and local emergency procedures before applying energy.

## Pre-energization checklist

<div class="ee-checklist">
  <label><input type="checkbox" data-ee-check="scope">I can identify the source, maximum voltage/current, stored energy, and non-electrical hazards.</label>
  <label><input type="checkbox" data-ee-check="ratings">Parts, wire, probes, instrument inputs, fuses, and connectors cover the worst-case ratings.</label>
  <label><input type="checkbox" data-ee-check="schematic">I checked polarity, pins, grounds, feedback paths, and possible shorts against the schematic.</label>
  <label><input type="checkbox" data-ee-check="limit">Power is off, output is at zero or a conservative value, current limit is set, and initial energy is minimized.</label>
  <label><input type="checkbox" data-ee-check="instrument">I understand input impedance, common-mode range, grounding, and probe attenuation.</label>
  <label><input type="checkbox" data-ee-check="workspace">The area is dry, orderly, stable, lit, and ventilated; people, jewelry, combustibles, and loose conductors are clear.</label>
  <label><input type="checkbox" data-ee-check="stop">I can isolate energy from a safe position if heat, odor, smoke, noise, waveform, or motion becomes abnormal.</label>
  <label><input type="checkbox" data-ee-check="supervision">Where the risk class requires supervision, a qualified person is present and has approved the step.</label>
  <div class="ee-checklist__footer">
    <span class="ee-check-progress" data-complete-label="Complete" data-of-label="of"></span>
    <button class="ee-reset-progress" type="button">Clear page progress</button>
  </div>
</div>

If any item is uncertain, keep the system de-energized and return to simulation, documentation, or qualified review.

## Discipline during work

### Electrical and stored energy

- Work de-energized by default; fixed equipment must follow the facility’s energy-isolation, tagging, and verification procedure.
- After disconnection, verify state with suitable equipment known to function; switch position is not proof.
- Capacitors, batteries, and inductive loads can retain or create energy after disconnection. Use designed discharge, protection, and verification.
- Remove energy before changing wiring, moving probes, switching range, or replacing a part.
- Never bypass a fuse, interlock, protective earth, isolation barrier, enclosure, or equipment protection.

The U.S. Occupational Safety and Health Administration requires de-energization as the default control where someone may be exposed to live parts and restricts energized work to qualified people with appropriate controls. Treat this as a baseline warning, not permission for home work. See [OSHA 1910.333](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.333).

### Batteries

- Use traceable, correctly specified batteries and chargers with appropriate protection.
- Do not use swollen, damaged, hot, leaking, or unknown cells.
- Keep tools, jewelry, and loose metal from bridging terminals.
- Follow manufacturer and local rules for charging, storage, transport, and disposal.
- Do not dismantle cells or use loose industrial cells as unprotected consumer batteries.

High-energy-density batteries can cause overheating, thermal burns, fire, and explosion. The U.S. Consumer Product Safety Commission has specifically warned about loose 18650 cells during shorting, storage, transport, and charging. See the [CPSC high-energy-density battery page](https://www.cpsc.gov/Regulations-Laws--Standards/Voluntary-Standards/Batteries-Fire-High-Energy-Density) and [loose-cell warning](https://www.cpsc.gov/Newsroom/News-Releases/2021/CPSC-Issues-Consumer-Safety-Warning-Serious-Injury-or-Death-Can-Occur-if-Lithium-Ion-Battery-Cells-Are-Separated-from-Battery-Packs-and-Used-to-Power-Devices).

### Soldering, rework, and materials

- Use a stable holder, heat-resistant surface, eye protection, and effective fume control close to the source.
- Return the iron to its stand immediately and treat it as hot until cooled; control the direction of clipped leads.
- Do not eat or drink in the work area; wash hands and prevent lead or other contamination from entering living spaces.
- Read safety data sheets for solder, flux, cleaners, and adhesives.

Rosin-based flux fume can cause occupational asthma. A general fan that moves fumes toward another person is not source control. See the UK Health and Safety Executive’s [guidance for solderers using rosin-based flux](https://www.hse.gov.uk/asthma/solderers.htm).

### Lasers, RF, and electromagnetic fields

- Never look into a laser beam, and never infer power from apparent brightness.
- Do not use an unknown, modified, or incompletely labeled laser.
- Class 3B/4 systems, or anything capable of a hazardous direct or specular reflection, belong in a qualified laser facility.
- Before RF transmission, confirm authorization, band, power, load, and exposure controls. Start with receive-only, simulation, or shielded small-signal tests.
- Strong magnetic fields can attract tools, affect implanted medical devices, and store mechanical energy; they require specific controls.

The U.S. Food and Drug Administration notes that visible brightness is not a reliable indication of laser power and that Class 3B/4 products can present immediate eye, skin, or fire hazards. See the [FDA laser FAQ](https://www.fda.gov/radiation-emitting-products/laser-products-and-instruments/frequently-asked-questions-about-lasers).

### Mechanical, thermal, vacuum, and chemical

- Limit speed, torque, travel, and test area for actuators, drones, robots, and motors before free motion.
- Heaters, power devices, and loads can burn after power is removed.
- Vacuum chambers, pressure vessels, refrigerants, etchants/cleaners, and microfabrication equipment are outside an unsupervised home laboratory.
- Eye protection is not a universal control. Eliminate, substitute, isolate, and engineer out hazards before selecting task-specific personal protection.

## Stop conditions

<div class="ee-status ee-status--stop">
  <strong>Stop immediately and isolate energy from a safe position:</strong> smoke, sparks, abnormal odor, swelling, leakage, rapid heating, protection activation, unexplained current, uncontrolled motion, structural damage, loss of instrument reference, or any state outside the plan. Do not re-energize “for one more measurement.”
</div>

After stopping:

1. isolate energy without approaching the hazard; if that cannot be done safely, evacuate and activate the local emergency process;
2. do not touch equipment that may remain energized, hot, pressurized, or chemically active;
3. contact local emergency services and the responsible facility person when medical, fire, or specialist response is needed;
4. preserve the scene and data; do not resume until qualified review updates the controls.

Do not directly touch a person who remains connected to an electrical source. Disconnect power only when you can do so without becoming another casualty, then follow local emergency-dispatch and first-aid training.

## Safety evidence in a design review

Attach at least:

- hazards, energy sources, and exposed people/property;
- the order of elimination, substitution, isolation, engineering, procedural, and personal controls;
- component and instrument rating table;
- normal, single-fault, and foreseeable-misuse tests;
- evidence for interlocks, fusing, limiting, discharge, and thermal protection;
- stop conditions, supervisor, and restart approval;
- residual risk and explicitly prohibited scenarios.

A safety review is inspectable design evidence, not a checkbox saying “read the warnings.”
