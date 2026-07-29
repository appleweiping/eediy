---
title: "RF and Millimeter-Wave Circuit Design"
description: "Eindhoven University of Technology's RF and Millimeter-Wave Circuit Design builds a simulation-first RF and millimeter-wave circuit path in Qucs-S and Octave, with about seventy percent reproducible and hardware optional."
page_type: course
course_id: "course-111"
editorial_status: "researched"
evidence_level: "R0"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 5a7d9303bf9bac7f -->

# RF and Millimeter-Wave Circuit Design

## Course Overview

- **University:** Eindhoven University of Technology
- **Course code:** RF and Millimeter-Wave Circuit Design
- **Prerequisites:** Recommended foundation: Electromagnetic Fields and Waves; Recommended foundation: Circuit Analysis; Recommended foundation: Communication Systems
- **Track:** [RF, Microwave, and Antennas](index.md)
- **Path role:** Mainline
- **Public materials:** Core materials available
- **Last reviewed:** 2026-07-29

> **Desk-researched (R0):** The official course materials were checked item by item on 2026-07-29, but no traceable full-course report has been accepted. This guide therefore makes no first-hand claims; completers can submit a report below.

## Treat the course as five design reviews

Eindhoven University of Technology's **RF and millimeter-Wave Circuit Design** on Coursera is not a tour of component names. On 2026-07-29, the provider [course page](https://www.coursera.org/learn/rf-mmwave-circuit-design) displayed 6 modules and 19 assignments. It opens with wireless systems, then covers amplifiers, mixers, oscillators, and synthesizers. Modules 2–6 each contain a peer-reviewed design lab: Wireless Tin Can Telephone system analysis, LNA/PA, up- and down-conversion mixers, a VCO, and a frequency-divider/phase-detector synthesizer. Reading the course as 5 design reviews is more faithful to its engineering structure than merely finishing 6 video modules.

The same page says all design labs are optional for the certificate but recommended; about 70% can be performed with simulation tools, while about 30% needs an electronics laboratory or purchased off-the-shelf components. That 70/30 split is the provider's description of its labs, not EEDIY safety advice, and it does not make an arbitrary home bench acceptable. This is a living Coursera offering. Its public marketing page does not pin a semester or starter-file version, so records must include the review date and the versions of material actually obtained.

## Three entry problems are better than prior analog-circuit coursework

Problem 1: given carrier frequency, a free-space Friis propagation model, transmit power, antenna gains, distance, receiver bandwidth, a 290 K reference noise temperature, noise figure, and target SNR, produce a complete link budget with explicit dB/dBm conversions, thermal noise, implementation margin, and receiver sensitivity. Problem 2: use a 2-port S-parameter set to obtain input and output reflection, transducer gain, and a stability judgment, then explain on a Smith chart why matching is not simply “make every reflection zero.” Problem 3: draw a frequency plan for a mixer or oscillator, labeling the fundamental, image, LO leakage, major harmonics, and the route by which phase noise or compression reaches a system specification.

Complete at least 2 of the 3 with units and reference planes intact before Module 1. A learner comfortable only with low-frequency small-signal gain should first review microwave networks, S-parameters, and noise cascades. A learner who can quote Friis path loss but cannot derive block specifications from sensitivity should not jump into the PA or VCO lab. This is an EEDIY placement diagnostic, not a Coursera enrollment rule.

## The 19 assignments and 5 labs create two parallel evidence chains

Module 1 contains 1 assignment, Modules 2–5 contain 4 each, and Module 6 contains 2, for 19 total. They move from wireless-system introduction, path loss, sensitivity, and selectivity through LNA matching, PA classes, mixer images and harmonics, oscillator phase noise, and type-I and type-II PLLs. Each module also lists supporting material. When lawfully accessible, attempt the assessment before viewing a solution video, then locate the first failure in the specification, equation, simulation setup, or interpretation.

The 5 peer-review labs form a separate design chain. Preserve a specification table, assumptions, schematic or block diagram, simulation configuration, pass/fail plots, corner or sensitivity check, and open issues for each review. Retain at least 1 rejected candidate, name its failed metric or corner, and classify peer comments as accepted, rejected, or pending with plot or calculation evidence. Preserve before-and-after metrics; when 2 candidates pass nominal conditions, use temperature, model tolerance, or load perturbation to justify the choice rather than appearance. The official tasks allow simulation and implementation layers, but hardware is not required for the certificate; EEDIY defaults to the simulation layer only. Without a paid enrollment or an available Full Course, No Certificate path, do not obtain locked assignments, supporting files, or solution videos from unofficial mirrors.

## Tool versions belong to the artifact, not the course title

Module 1 explicitly introduces Qucs-S and Octave, but the public page pins no releases. On 2026-07-29, the official [Qucs-S repository](https://github.com/ra3xdh/qucs_s) listed 26.1.1 as the latest release, and its README states that releases from 25.1.0 use Qt6 only. The official [installation guide](https://qucs-s-help.readthedocs.io/en/latest/installation/installing-qucs-s.html) also documents platform-dependent backends: Windows packages include ngspice and QucsatorRF, macOS packages include only QucsatorRF, and other backends may require separate installation. If a course file fails in a newer release, record the original file, backend, netlist, and error before changing simulators.

The GNU [download page](https://octave.org/download.html) listed Octave 11.3.0 as the stable release on the same review date. That makes it a candidate reproducibility environment, not evidence that TU/e supporting files were validated against 11.3.0. Each lab should include an `environment.md` naming the OS, Qucs-S release, backend, Octave release, device-model source, and hash. Preserve baseline plots before an upgrade and compare results with numerical tolerances rather than visual resemblance.

## Each review needs one decision that cannot be hand-waved

The wireless-system review must derive transceiver block specifications from range, bandwidth, sensitivity, selectivity, and distortion instead of selecting parts first. The amplifier review must separately resolve LNA noise, matching, and stability and PA gain, compression, and efficiency; small-signal S-parameters are not a large-signal conclusion. The mixer review needs a complete frequency table with wanted product, image, spurs, and filtering assumptions. The oscillator review must address startup, amplitude limiting, tuning range, phase noise, output buffering, and load pulling. The synthesizer review must explain loop type, bandwidth, reference and divider noise, and lock behavior.

Exit to link budgets if the Module 2 system budget and block specifications cannot be reconciled. Do not proceed from Module 3 to a PA implementation when nominal LNA gain passes but stability and noise have no evidence. Stop in Module 5 if a single transient trace is still being presented as phase-noise performance. These exit rules prevent an attractive plot from concealing the wrong metric.

## “Build a transceiver at home” is not authorization from this page

The provider uses the 70% simulation and 30% laboratory or components split for optional labs and discusses a physical transceiver. EEDIY nevertheless defaults to simulation only: do not build, drive, or connect an RF PA; connect an oscillator or mixer chain to an antenna; radiate into free space; or connect an unknown VNA, signal generator, bias tee, battery, or mains-powered instrument. The Tin Can Telephone lab name does not relax this boundary.

If an institution approves physical work, qualified RF supervision is required. Before power-up, review frequency authorization, exposure, source power, 50-ohm termination, rated attenuators, cables and connectors, DC current limits, ESD control, shielding or interlocks, and emergency shutdown. Never reconnect a high-power port while energized, look into or touch an open waveguide or aperture, or use an absolute maximum rating as an operating point. TU/e's paper on a [remote RF laboratory](https://research.tue.nl/en/publications/rf-circuits-laboratory-for-remote-learning-and-massive-open-onlin/) describes purpose-built controlled infrastructure, not an arbitrary home-bench recipe.

## Without platform access, only a clearly labeled supplement is valid

An enrolled learner should prioritize the official 19 assignments and the accessible portions of all 5 peer-review labs, preserving Coursera feedback. Platform grades, peer reviews, and certificates cannot be reproduced by a local script. The Coursera FAQ says materials, assignments, and a certificate normally require purchasing the certificate experience. Eligible learners may receive a free trial, and some courses may offer Full Course, No Certificate; neither option is guaranteed. Check payment, login, and regional availability before starting.

Without access, create only a clean-room transceiver-budget notebook: derive specifications, a block cascade, noise and linearity budgets, and 5 idealized simulation blocks from publicly available equations without copying a locked prompt, supporting file, or solution. It must be labeled an EEDIY supplement, not an official lab, and cannot earn a Coursera grade. The final dossier should separate official attempted, official inaccessible, and EEDIY supplement items and include the 3 entry problems, a 19-item status table, 5 design reviews, environment lock files, and a safety scope.

This page has R0 evidence from provider pages and official tool documentation; it claims neither course completion nor physical experimentation. Corrections should identify course ID 111, the exact module, assignment, or lab, the review date, and a provider source. Do not submit paid material, a peer's private work, hazardous RF bench records, or unauthorized transmission results.

## Course Resources

<details markdown="1">
<summary>Expand the complete resource index (1 items)</summary>

### Material coverage

| Type | Completeness |
|---|---|
| Video | Complete |
| Notes | Partial |
| Practice | Complete |
| Labs | Complete |
| Exams | No public material |
| Code | Complete |

### Resource

| Resource | Access | Status | Verified |
|---|---|---|---|
| [Course home](https://www.coursera.org/learn/rf-mmwave-circuit-design) | Registration required | Listed by official page | 2026-07-28 |

> Links were discovered from official sources on the recorded date. Access does not grant redistribution rights, and region, account, third-party rights, or later redesigns may change availability.

</details>
