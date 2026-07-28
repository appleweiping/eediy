---
title: "Sensors, Instrumentation, and Biomedical Electronics"
description: "Build a measurement system with calibration, uncertainty, isolation/safety analysis, and signal processing; use compliant data or supervision for human subjects."
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: cac14cc66ccffd61 -->

# Sensors, Instrumentation, and Biomedical Electronics

[中文](../../routes/instrumentation-biomedical.md) · [← Learning routes](index.md)

## Audience

Learners combining sensors, analog front ends, measurement, and physiological signal processing

## Final outcome

Build a measurement system with calibration, uncertainty, isolation/safety analysis, and signal processing; use compliant data or supervision for human subjects.

## Stages

### Circuits and measurement

**Selection rule:** Complete all 3 required courses; use the other 1 option only to close a specific gap.

- [Circuits and Electronics](../courses/circuits/021-6-002.md) — **Required**; MIT; Mainline; S
- [Introduction to Electronics, Signals, and Measurement](../courses/electronics-laboratory/024-6-071j.md) — **Optional supplement**; MIT; Alternative; A
- [Real Analog Courses](../courses/electronics-laboratory/027-real-analog.md) — **Required**; Digilent; Mainline; A
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **Required**; MIT; Mainline; S

**Stage exit criterion:** Build a traceable measurement chain and perform a calibration at five or more points, submitting an uncertainty budget for gain, offset, bandwidth, noise, and quantization; every calibration residual must fall within the predeclared tolerance band.

### Sensors and interfaces

**Selection rule:** Complete all 2 required courses; use the other 1 option only to close a specific gap.

- [Electrical Measurement and Electronic Instruments](../courses/sensors-instrumentation/136-108105153.md) — **Required**; IIT Kharagpur / NPTEL; Mainline; A
- [Sensor Technologies: Physics, Fabrication, and Circuits](../courses/sensors-instrumentation/137-108106193.md) — **Required**; IISER Bhopal / NPTEL; Mainline; A
- [Sensors and Sensor Circuit Design](../courses/sensors-instrumentation/138-ecea-5340.md) — **Optional supplement**; University of Colorado Boulder; Alternative; A

**Stage exit criterion:** Complete excitation, conditioning, sampling, and digital output for one sensor, measuring linearity, hysteresis, noise, and drift across full scale; compare every result against a reference instrument or trustworthy datasheet.

### Biomedical applications

**Selection rule:** Complete all 2 required courses; use the other 1 option only to close a specific gap.

- [Digital Signal Processing](../courses/dsp/088-res-6-008.md) — **Required**; MIT; Mainline; S
- [Biomedical Instrumentation](../courses/biomedical/139-102106669.md) — **Required**; IIT Madras / NPTEL; Mainline; A
- [Biomedical Signal and Image Processing](../courses/biomedical/140-hst-582j.md) — **Optional supplement**; MIT; Supplement; A

**Stage exit criterion:** Validate a physiological-signal pipeline using only public or synthetic data, reporting SNR improvement, artifact-rejection rate, and held-out error; attach isolation, privacy, ethics, and non-diagnostic-use checks, with no unapproved human experimentation.

## Execution rules

- Follow each stage's selection rule: complete every required course and the stated number of electives; when complete path options are provided, choose one and finish every course in its listed order; use optional supplements only to close a specific gap.
- Produce at least one reproducible artifact per stage and include failed attempts in the retrospective.
- Work involving mains voltage, high voltage, RF exposure, lasers, chemicals, or fabrication equipment requires local-law compliance and qualified supervision.
