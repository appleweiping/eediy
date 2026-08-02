---
title: "Digital Signal Processing"
description: "Discrete transforms, filters, spectral estimation, multirate systems, and implementations validated with code and metrics."
page_type: track
track_id: "track-dsp"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 77f3112bcd49a2cf -->

# Digital Signal Processing

## Track position

Discrete transforms, filters, spectral estimation, multirate systems, and implementations validated with code and metrics.

## Recommended prerequisite tracks

- [Signals and Systems](../signals-systems/index.md)
- [Probability, Statistics, and Random Processes](../probability-statistics/index.md)
- [Programming and Engineering Computing](../programming-tools/index.md)

## RES.6-008 and 6.341 are two kinds of historical theory spine

The [official MIT RES.6-008 archive](https://ocw.mit.edu/courses/res-6-008-digital-signal-processing-spring-2011) gives [RES.6-008](088-res-6-008.md) 20 video-and-note lessons and 19 solution packets for Lectures 2–20. It is a systematic route through discrete representations, z transforms, the DFT, filters, and algorithm realization. The recordings date to 1987 and the core text is older; the mathematics remains useful, while the execution environment is not a modern coding baseline. [MIT 6.341](089-6-341.md) adds 11 problem sets, 2 projects, and 3 exam collections for graduate derivation, design, and reporting after introductory DSP.

The Athena and MATLAB projects in 6.341 need migration, but their phase comparison, operation count, and report requirements are worth retaining. A new Python or Julia implementation should be distinguished from the original prompt rather than presented as course work merely because its library interface is current. Use RES.6-008 for a first theory spine; enter 6.341 directly when discrete systems are already familiar and a long project is desirable.

## Select among the four EPFL courses by problem, not course number

[DSP 1](090-dsp-1.md), [DSP 2](091-dsp-2.md), and [DSP 3](092-dsp-3.md) cover basic representations, filtering, and the analog/digital boundary, while [DSP 4](093-dsp-4.md) turns to applications. The current [official DSP 4 page](https://www.coursera.org/learn/dsp4) lists 3 modules, 2 graded assignments, and 4 ungraded labs, not 3 assignments. The older public repository does not map item for item to current platform labs, and old NumEx work is not current graded work. Full platform access may also be paid.

[Illinois ECE 310](094-ece-310.md) can serve as a text-first map, while [ECE 311](095-ece-311.md) exposes laboratory scope. As checked anonymously on 2026-07-30, ECE 310 homework and exam files return HTTP 401; ECE 311 Lab 1–7 and final ZIP files are similarly restricted, and walkthroughs enter Illinois SSO. [Berkeley EE 123](096-ee-123.md) carries DSP into wireless projects, but the confirmed directly downloadable machine package covers HW11 rather than the whole course. A course title on a public page does not imply open assignments, starters, and feedback.

These pages can establish topic scope and tool requirements; they cannot turn a self-authored notebook into an original course laboratory. If public access changes, describe only the materials obtained in that particular check rather than filling restricted files from mirrors or inference.

## One signal should expose representations, filtering, and numerical error

[Signals and systems](../signals-systems/index.md) supplies convolution, LTI systems, sampling, Fourier and z transforms, and poles and zeros. [Probability and statistics](../probability-statistics/index.md) supplies random processes, expectation, correlation, and noise. [Programming and engineering tools](../programming-tools/index.md) supplies a reproducible environment, tests, and raw-data practice. Choose audio, sensor, or baseband data with provenance and state sample rate, record length, units, and raw checksum.

Hand-calculate one short convolution and DFT and define hertz, radians per sample, and FFT normalization. Change sample rate, window, and record length separately, predicting aliasing, resolution, and leakage. Then compare an FIR and IIR under stated passband, stopband, transition width, delay, complexity, and allowable distortion. On a hand-solvable sequence, compare a SciPy reference with an independent implementation. An anomaly caused by padding, data type, filter state, coefficient quantization, or an unstable pole should lead to a specific sample and processing stage rather than only a smoother-looking plot.

Time-domain, frequency-domain, and pole-zero views should explain the same event. For example, transient ringing should agree with impulse-response length, transition-band behavior, and pole location; contradictory stories call for checking normalization and boundary handling first. Include delay and operation count in the comparison so filters are not ranked by appearance alone.

## The layer containing the error points to the next branch

Windows, PSD variance, and finite records point toward spectral estimation or statistical DSP. Imaging, alias rejection, and computation at different rates point toward multirate work. Fixed-point effects, streaming buffers, and real-time deadlines point toward DSP implementation. When channels, synchronization, and RF hardware dominate, move into [communication systems](../communications/index.md) or SDR. Reuse the same data and baseline while changing the new problem layer.

EE 123 SDR and amateur-radio work requires hardware, local spectrum rules, and licensing. No RF transmission belongs in independent work without authorization. A baseband array or recorded-data analysis is valid when hardware is unavailable, provided untested physical behavior is explicit. DSP has become an engineering tool when one erroneous sample can be traced to a representation, algorithm, numerical implementation, or hardware interface, not when the longest video sequence has been watched.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Digital Signal Processing](088-res-6-008.md) | MIT | Main course | Public-material guide | Partial or restricted |
| [Discrete-Time Signal Processing](089-6-341.md) | MIT | Alternative | Public-material guide | Public assignments or labs |
| [Digital Signal Processing 1: Basic Concepts and Algorithms](090-dsp-1.md) | EPFL | Alternative | Public-material guide | Partial or restricted |
| [Digital Signal Processing 2: Filtering](091-dsp-2.md) | EPFL | Alternative | Public-material guide | Partial or restricted |
| [Digital Signal Processing 3: Analog versus Digital](092-dsp-3.md) | EPFL | Alternative | Public-material guide | Partial or restricted |
| [Digital Signal Processing 4: Applications](093-dsp-4.md) | EPFL | Alternative | Public-material guide | Public assignments or labs |
| [Digital Signal Processing](096-ee-123.md) | University of California, Berkeley | Alternative | Public-material guide | Public assignments or labs |
| [Digital Signal Processing I](094-ece-310.md) | University of Illinois Urbana-Champaign | Alternative | Catalogue only; not a complete course substitute | No public practice found |
| [Digital Signal Processing Laboratory](095-ece-311.md) | University of Illinois Urbana-Champaign | Alternative | Catalogue only; not a complete course substitute | No public practice found |
