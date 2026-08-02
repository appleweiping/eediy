---
title: "Converter Circuits"
description: "University of Colorado Boulder's Converter Circuits specializes in converter circuits after the introductory course, using videos, practice, simulation, and code under an explicit prerequisite and possible access fee."
page_type: course
course_id: "course-116"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 5a6c758acb968326 -->

# University of Colorado Boulder Power Electronics 2: Converter Circuits

## Course Overview

- **University:** University of Colorado Boulder
- **Course code:** Power Electronics 2
- **Official prerequisites:** CU Boulder Converter Circuits is the second course in its power-electronics sequence and assumes prior Introduction to Power Electronics
- **EEDIY preparation:** No additional EEDIY preparation requirement
- **Access:** Registration required; scope varies by platform
- **Material status:** 2026-07-30; public-material guide

### Course fit

The University of Colorado Boulder [Converter Circuits](https://www.coursera.org/learn/converter-circuits) course is the second course in its power-electronics sequence. The official course page lists 4 modules and 4 graded assignments, with a reference pace of 2 weeks at 10 hours per week. It assumes prior study of [Introduction to Power Electronics](https://www.coursera.org/learn/power-electronics). Review the preceding course first if deriving a buck or boost averaged model from switching states, or explaining volt-second and charge balance, is still difficult.

The [Power Electronics specialization](https://www.coursera.org/specializations/power-electronics) confirms the sequence. Login, subscription, grading feedback, and certificate terms still depend on the current Coursera presentation. A public overview establishes that assignments exist; it does not replace their actual prompts.

### Learn Switch Realization and Transfer the Method Across Topologies

Chapter 4.1 moves from an ideal switch to physical realization through switching quadrants, bidirectional power flow, and synchronous switching. Mark the permitted voltage and current directions before choosing a diode, MOSFET, or combination; do not identify a device from the familiar shape of a schematic. Chapter 4.2 covers diodes, MOSFETs, IGBTs, gate drivers, and switching loss, with an LTspice synchronous-boost study. Separate conduction loss from switching loss and identify the device parameter behind every term. A single efficiency figure often hides a bad model.

Chapter 5 introduces DCM. Once inductor current reaches 0 A, the state sequence and conversion relation change, so a CCM expression cannot simply be extrapolated. Chapter 6 expands the set to inverters, isolated converters, transformers, forward converters, and flyback converters. For each magnetic topology, explain when energy is stored and transferred and how magnetizing current is reset.

### One topology table beats four disconnected notebooks

The 4 official assignments provide chapter-by-chapter checks. For independent study, maintain a topology table recording port polarity, switching states, supported quadrants, the CCM/DCM boundary, device stress, dominant losses, isolation, and flux reset. Then simulate a synchronous boost and a flyback. Use the former to inspect dead time and body-diode current paths, and the latter to test magnetizing-energy and reset assumptions. These are independent exercises, not course laboratories.

The public material does not teach breadboards, PCB layout, probe selection, insulation, or thermal qualification. Do not transfer a simulation result directly to a mains-connected or high-power build. Proceed to [Converter Control](https://www.coursera.org/learn/converter-control) after an unfamiliar topology can be decomposed into switching states, its voltage and current relations derived, and its DCM boundary and device stresses explained. Otherwise the next course's small-signal models will become formula matching.

## Course Resources

The guide above links each core resource where its version and access conditions are explained. To avoid relabeling a sequence course, archived syllabus, or restricted item out of context, this page does not repeat a generic resource list.

## Resource Summary

This page does not repeat resources outside their version context. The links and version notes in the overview are the complete verified summary for this review.
