---
title: "Signal Processing, Communications, and Information Theory"
description: "Implement a reproducible link with synchronization, modulation/demodulation, channel coding, and measured error rates."
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 13b62bae6618e55e -->

# Signal Processing, Communications, and Information Theory

[中文](../../routes/dsp-communications.md) · [← Learning routes](index.md)

## Audience

Learners moving from Fourier analysis to digital communications, wireless systems, and coding

## Final outcome

Implement a reproducible link with synchronization, modulation/demodulation, channel coding, and measured error rates.

## Stages

### Signals and probability

**Selection rule:** Complete all 4 required courses; use the other 1 option only to close a specific gap.

- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **Required**; MIT; Mainline; S
- [Probabilistic Systems Analysis and Applied Probability](../courses/probability-statistics/007-6-041sc.md) — **Required**; MIT; Mainline; S
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **Required**; MIT; Mainline; S
- [The Fourier Transform and Its Applications](../courses/signals-systems/097-ee-261.md) — **Required**; Stanford University; Mainline; S
- [Introduction to Communication, Control, and Signal Processing](../courses/signals-systems/098-6-011.md) — **Optional supplement**; MIT; Supplement; B

**Stage exit criterion:** Analytically derive and numerically verify the time-domain, frequency-domain, and stochastic responses of one LTI system in a single notebook; Parseval energy residual must be below 1%, and the Monte Carlo mean must fall within the analytical 95% confidence interval.

### DSP implementation

**Selection rule:** Complete all 1 required course and choose 1 of 5 elective options.

- [Digital Signal Processing](../courses/dsp/088-res-6-008.md) — **Required**; MIT; Mainline; S
- [Discrete-Time Signal Processing](../courses/dsp/089-6-341.md) — **Elective option**; MIT; Alternative; A
- [Digital Signal Processing 1: Basic Concepts and Algorithms](../courses/dsp/090-dsp-1.md) — **Elective option**; EPFL; Alternative; A
- [Digital Signal Processing 2: Filtering](../courses/dsp/091-dsp-2.md) — **Elective option**; EPFL; Alternative; A
- [Digital Signal Processing 3: Analog versus Digital](../courses/dsp/092-dsp-3.md) — **Elective option**; EPFL; Alternative; A
- [Digital Signal Processing 4: Applications](../courses/dsp/093-dsp-4.md) — **Elective option**; EPFL; Alternative; A

**Stage exit criterion:** Implement a filtering or spectral-processing pipeline and verify passband, stopband, and aliasing requirements with synthetic and real samples; also report reproducible floating-point versus fixed-point SNR, runtime, and memory comparisons.

### Communications and coding

**Selection rule:** Complete all 2 required courses and choose 1 of 2 elective options. The other course is an optional supplement and does not count toward the elective requirement.

- [Introduction to EECS II: Digital Communication Systems](../courses/communications/099-6-02.md) — **Required**; MIT; Mainline; S
- [Principles of Digital Communications I](../courses/communications/100-6-450.md) — **Elective option**; MIT; Mainline; S
- [Principles of Digital Communication II](../courses/communications/101-6-451.md) — **Optional supplement**; MIT; Mainline; S
- [Information Theory](../courses/information-theory-coding/102-ee-276.md) — **Required**; Stanford University; Mainline; A
- [Wireless Communications](../courses/communications/105-ee-359.md) — **Elective option**; Stanford University; Alternative; A

**Stage exit criterion:** Build an end-to-end link with synchronization, modulation, channel, and error correction, using fixed seeds to plot BER at at least six Eb/N0 points; include a theory or baseline comparison, confidence intervals, and synchronization-failure rate.

## Execution rules

- Follow each stage's selection rule: complete every required course and the stated number of electives; when complete path options are provided, choose one and finish every course in its listed order; use optional supplements only to close a specific gap.
- Produce at least one reproducible artifact per stage and include failed attempts in the retrospective.
- Work involving mains voltage, high voltage, RF exposure, lasers, chemicals, or fabrication equipment requires local-law compliance and qualified supervision.
