---
title: Laboratory Safety
description: Identify energy, respect supervision boundaries, and stop an EE experiment when critical conditions are unknown.
page_type: guide
comments: true
---

# Laboratory Safety

!!! danger "This is not work authorization"
    This page cannot replace institutional training, equipment manuals, standard operating procedures, a task-specific risk assessment, or qualified supervision. Follow the stricter rule when requirements differ. Without an appropriate facility, confirmed ratings, and trained supervision, do not work with mains electricity, exposed high voltage, high stored energy, Class 3B/4 lasers, hazardous chemicals, or unguarded rotating machinery.

Before an experiment begins, trace how electrical, thermal, optical, mechanical, or chemical energy could reach a person. Then decide whether you have the competence and facility to control it. Safety glasses may be one layer in a particular setup; they do not replace that analysis. For a student, recognizing a stop condition is often more important than memorizing a universal threshold.

## Start with the worst credible energy release

Trace every energy source: primary and back-fed supplies, charged capacitors, batteries, motors and flywheels, springs and pressure, lasers, RF, hot surfaces, vacuum vessels, and chemical reactions. “Low voltage” does not automatically mean low risk. A high-current source can arc or burn, capacitor energy grows as \(CV^2/2\), and a shorted battery or failed rotor can release substantial energy very quickly.

Ask three practical questions. How will the source be isolated? How will isolation be verified? If control is lost, can energy be removed without approaching the hazard? A switch, software stop button, or control signal can fail and is not necessarily physical isolation. If maximum voltage, available fault current, stored energy, speed, laser class, or chemical identity is unknown, there is not enough information to begin.

First energization should minimize energy, voltage, current, duration, and system scope. Put the emergency disconnect where it can be reached without leaning over the apparatus. The more actions a person must perform after energization, the stronger the case for adding test points, guards, remote control, or isolation before continuing.

## Mains, high voltage, and stored energy require qualified control

U.S. OSHA [rule 1910.333](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.333) makes de-energization the default where someone may be exposed to live parts and restricts justified energized work to qualified people using suitable protection. This workplace rule is a baseline warning, not permission to work on exposed mains or high voltage at home or in an ordinary teaching setup. An unqualified learner should use enclosed, compliant power supplies, never open the primary side, and never float a normally grounded oscilloscope. One-hand technique or insulating gloves do not turn unqualified energized work into safe work.

Power removed is not the same as energy removed. OSHA's [hazardous-energy rule 1910.147](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147) addresses unexpected start-up and residual or stored energy and requires isolation to be verified. Discharge capacitors through a designed path, wait for the equipment's specified interval, and confirm with appropriately rated test equipment; do not short them with a screwdriver. Consider backfeed, multiple supplies, motor regeneration, mechanical inertia, and stored energy that can reaccumulate.

Use lithium batteries only within manufacturer limits for voltage, current, temperature, charger, and protection. The CPSC warning on [loose 18650 cells removed from packs](https://www.cpsc.gov/Newsroom/News-Releases/2021/CPSC-Issues-Consumer-Safety-Warning-Serious-Injury-or-Death-Can-Occur-if-Lithium-Ion-Battery-Cells-Are-Separated-from-Battery-Packs-and-Used-to-Power-Devices) explains that exposed terminals, shorts, and unsuitable charging can lead to thermal runaway, fire, and explosion. Do not continue testing an unknown, torn, swollen, leaking, abnormally hot, or impact-damaged cell. Clear people from the area and use the institution's battery-incident procedure.

## Laser and chemical hazards cannot be judged by brightness or smell

The FDA [laser classification summary](https://www.fda.gov/radiation-emitting-products/laser-products-and-instruments/frequently-asked-questions-about-lasers) identifies Class 3B direct beams as immediate eye and skin hazards and Class 4 direct or reflected beams as eye, skin, and possible fire hazards. Visible brightness does not establish safe power. Stop if class, wavelength, maximum output, beam termination, reflective surfaces, or eyewear range is unknown. Class 3B/4 systems, open beams, and any work requiring an interlock bypass belong only in a controlled laboratory under trained supervision. A camera or phone display is not eye protection.

A chemical needs a readable label and current SDS, plus the ventilation, PPE, storage, spill response, and waste route required by that SDS. Otherwise, do not use it. Familiar electronics materials are not exempt: the UK HSE's [health guidance for solderers](https://www.hse.gov.uk/asthma/solderers.htm) explains that rosin-based flux fume can cause occupational asthma and requires effective controls such as extraction at the source. A room fan that moves fumes toward someone else is not local extraction.

Unknown solvents, transferred or unlabeled containers, incompatible cleaning agents, uncontrolled powders, and processes without a lawful waste route belong in a properly managed laboratory. Smell is not a measurement. Eye or airway irritation, breathing difficulty, skin exposure, or an unexpected reaction means stop, leave the exposure area, and follow the SDS and local emergency procedure.

## Rotating machinery, heat, and pressure need physical boundaries

OSHA's [machine-guarding rule 1910.212](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.212) explicitly covers rotating parts, nip points, flying chips, and sparks. A guard or interlock is part of the control, not an accessory to remove for filming or debugging. Before running a motor, fan, spindle, or flywheel, secure the workpiece and sensors and keep leads, tools, hair, and loose clothing out of the operating envelope. Observe from outside the danger zone.

If a hand or probe must enter the motion envelope, a guard cannot be fitted, a rotor is cracked or unbalanced, fixture ratings are unknown, or vibration and sound change unexpectedly, isolate power and wait for all motion to stop. Oscilloscope grounds, sensor wires, and USB leads can also become entanglement hazards; cable restraint is part of mechanical safety.

Soldering irons, power devices, hot plates, and heat sinks can burn after power removal. Pressure and vacuum vessels can release energy suddenly when a window, fitting, or material fails. Do not improvise if temperature or pressure ratings, vessel condition, shielding, or qualified supervision are unclear. Temporary glassware, printed parts, and unknown adhesives should not carry pressure, vacuum, or high temperature without engineering validation for that exact use.

## Stop on any of these conditions

Stopping is evidence that the experiment remains under control. Do not “try once more” when any of the following is true:

- source, rating, grounding, energy, or safety class cannot be confirmed;
- the task exposes mains or high voltage, bypasses an interlock, or requires energized probing without qualified supervision;
- electrical or mechanical stored energy lacks a verifiable isolation and release path or can reaccumulate;
- laser class, beam termination, reflection risk, or eyewear wavelength and optical density are unknown;
- a chemical lacks a label or SDS, or required ventilation, spill control, and waste handling are absent;
- rotating equipment has no guard, an insecure workpiece or rotor, loose wiring, or a task that puts a person in the danger zone;
- there is smoke, arcing, odor, unexpected heat, swelling, leakage, tripping, uncontrolled motion, unusual sound, or vibration;
- you are fatigued, alone, unable to explain the next action, or unable to leave and disconnect energy safely.

Use the preplanned remote or safe disconnect during an abnormal event. Do not grab the apparatus, move a swollen cell, or touch a person or equipment that may remain energized. Leave the hazard area, keep others away, and contact qualified site personnel or local emergency services. Do not restart in the same session until the cause is understood, controls are corrected, and the operating boundary is confirmed again.
