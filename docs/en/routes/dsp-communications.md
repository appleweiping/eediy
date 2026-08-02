---
title: "Signal Processing, Communications, and Information Theory"
description: "Implement a repeatable communication link with synchronization, modulation and demodulation, channel coding, and error-rate measurement, and explain where simulation departs from theory."
page_type: route
route_id: "route-dsp-communications"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: a1c43aa134ca11de -->

# Signal Processing, Communications, and Information Theory

## Audience

Learners who want to connect Fourier analysis, random processes, and DSP to digital communications, wireless channels, and coding

## What you should be able to do

Implement a repeatable communication link with synchronization, modulation and demodulation, channel coding, and error-rate measurement, and explain where simulation departs from theory.

## Freeze one signal chain first

Begin with one script that generates a sinusoid plus white noise, plots time and spectrum, and estimates power. If sampling rate, Parseval, expectation, and variance cannot all be explained, remain with LTI systems and probability instead of memorizing modulation names.

## Reuse the same samples across analysis, floating point, fixed point, and the link

- Use one seeded sample set for the analytic LTI model, floating-point DSP, and fixed-point implementation, stating passband, stopband, aliasing, and quantization-noise limits first.
- Choose either 6.450 digital communications or EE 359 wireless channels as the main branch, and keep the preceding filter at the transmitter or receiver front end.
- Sweep BER across failure, waterfall, and target regions, retaining bit count and confidence interval at every point and separating synchronization failures from decoding errors.
- Keep one main exercise set for overlapping Fourier material in 6.003 and EE 261. Skip inaccessible EPFL modules rather than treating a product page as a notebook.

## Leave RF hardware outside the boundary for now

- Skip 6.451 until the detector and error-rate curve are secure, and do not complete both the digital-communications and wireless branches.

## Stop at the layer you actually chose

- One command rebuilds waveforms, spectra, floating/fixed differences, and BER plots from a fixed configuration, and departures from theory trace to finite samples, synchronization, quantization, or channel assumptions.
- A DSP-only learner may stop after the second stage with that boundary stated. The communications exit adds a reproducible end-to-end link and confidence intervals; no physical transmission is required.

## How to proceed

### Single-variable calculus

**Why these courses:** The published preparation for 6.041SC begins with 18.01. Use closed-book 18.01SC problems on limits, derivatives, integrals, and series as the diagnostic, and continue only when those operations can support probability-density normalization, expectation integrals, and convergence arguments.

- [Single Variable Calculus](../courses/mathematics/001-18-01sc.md) — **Required**; MIT

**Move on when:** Solve a changed-parameter calculus set independently, then compute probability and expectation for one normalized density by both analytical and numerical integration. Numerical error must converge with step size, with consistent units and domains.

### Multivariable calculus, differential equations, and vector spaces

**Why these courses:** 18.02SC supplies the multiple-integral background published for 6.041SC, 18.03SC supplies linear ODEs and eigenstructure, and 18.06SC supplies vector spaces and projection. Keep all three attached to one second-order LTI model rather than completing unrelated exercise sets.

- [Multivariable Calculus](../courses/mathematics/002-18-02sc.md) — **Required**; MIT
- [Differential Equations](../courses/mathematics/003-18-03sc.md) — **Required**; MIT
- [Linear Algebra](../courses/mathematics/004-18-06sc.md) — **Required**; MIT

**Move on when:** Derive a state model, eigenvalues, and analytical response from the differential equation, then recompute with a matrix exponential and numerical integration. A basis change must preserve the input-output response, and residuals must converge with time step.

### Connect probability to signals and systems

**Why these courses:** Use 6.041SC for random variables and processes, 6.003 for time-, frequency-, and system-domain representations, and EE 261 only for the Fourier depth needed by the project. Keep the preceding LTI model and replace its deterministic input with a seeded random process; retain one main exercise set for overlapping Fourier material.

- [Probabilistic Systems Analysis and Applied Probability](../courses/probability-statistics/007-6-041sc.md) — **Required**; MIT
- [Signals and Systems](../courses/signals-systems/083-6-003.md) — **Required**; MIT
- [The Fourier Transform and Its Applications](../courses/signals-systems/097-ee-261.md) — **Required**; Stanford University

**Move on when:** Derive and numerically verify the system's time-domain, frequency-domain, and stochastic responses in one notebook. Preserve the seed and sample count, compare Monte Carlo means at a confidence level chosen before the run, and drive the Parseval residual below an error derived from windowing and discretization.

### Turn DSP into an implementation

**Why these courses:** RES.6-008 is the main DSP course; keep the stochastic-LTI data, sampling definition, and golden output from the preceding work. The counted depth course is one relevant EPFL DSP 1–4 module chosen for an algorithm, filtering, sampling, or application gap. Because 6.341 explicitly builds on 6.011, use it only as uncounted theory after taking the later 6.011→6.450 digital-communications path. If an EPFL module is inaccessible, complete only public RES.6-008 rather than treating a product page as a lab.

- [Digital Signal Processing](../courses/dsp/088-res-6-008.md) — **Required**; MIT
- [Discrete-Time Signal Processing](../courses/dsp/089-6-341.md) — **Use if needed**; MIT
- [Digital Signal Processing 1: Basic Concepts and Algorithms](../courses/dsp/090-dsp-1.md) — **Choose 1**; EPFL
- [Digital Signal Processing 2: Filtering](../courses/dsp/091-dsp-2.md) — **Choose 1**; EPFL
- [Digital Signal Processing 3: Analog versus Digital](../courses/dsp/092-dsp-3.md) — **Choose 1**; EPFL
- [Digital Signal Processing 4: Applications](../courses/dsp/093-dsp-4.md) — **Choose 1**; EPFL

**Move on when:** Implement a filtering or spectral-processing pipeline and check passband, stopband, and aliasing with synthetic samples and one real dataset. Run floating- and fixed-point versions on the same inputs, report SNR, runtime, and memory use, and provide one command that reproduces the comparison.

### Bits over a noisy link

**Why these courses:** Start the link in 6.02 with synchronization, coding, and system intuition, while EE 276 sets the information-theoretic limits. Keep the preceding filter or fixed-point block as the transmitter or receiver front end. Then choose one complete path: 6.011→6.450 in that order for digital communications, or EE 359 for wireless channels. Use 6.451 only as uncounted depth after the digital path and after the detector and error-rate curve are understood; this is a knowledge dependency, not a certificate rule.

- [Introduction to EECS II: Digital Communication Systems](../courses/communications/099-6-02.md) — **Required**; MIT

- [Information Theory](../courses/information-theory-coding/102-ee-276.md) — **Required**; Stanford University

**Complete path — Digital communications with its prerequisite (6.011→6.450) (take these in the listed order)**

1. [Introduction to Communication, Control, and Signal Processing](../courses/signals-systems/098-6-011.md) — **Course in this path**; MIT
2. [Principles of Digital Communications I](../courses/communications/100-6-450.md) — **Course in this path**; MIT

**This branch is done when:** Use 6.011 for the estimation or detection baseline before entering 6.450 modulation, detection, and error rates, keeping one stochastic-LTI model and test dataset across both. Treat 6.451 as uncounted depth only after this path.

**Complete path — Wireless-channel path (EE 359) (take these in the listed order)**

1. [Wireless Communications](../courses/communications/105-ee-359.md) — **Course in this path**; Stanford University

**This branch is done when:** Extend the 6.02 link with EE 359 fading and wireless-channel models, retaining the previous filter, fixed seeds, and error-rate statistics without also repeating the digital-communications path.

- [Principles of Digital Communication II](../courses/communications/101-6-451.md) — **Use if needed**; MIT

**Move on when:** Build an end-to-end link with synchronization, modulation, channel, and error correction. With fixed seeds, sweep an Eb/N0 range spanning low-SNR failure, the waterfall, and the target operating region, with denser points near the transition. Plot theory or a baseline beside BER, include sample count and confidence interval at every point, and report synchronization failures separately.
