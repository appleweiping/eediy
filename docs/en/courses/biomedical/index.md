---
title: "Biomedical Electronics and Signals"
description: "Physiological signals, medical imaging, and instrumentation with patient safety, ethics, isolation, and supervision."
page_type: track
track_id: "track-biomedical"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 1c006d5eb86d9161 -->

# Biomedical Electronics and Signals

## Track position

Physiological signals, medical imaging, and instrumentation with patient safety, ethics, isolation, and supervision.

## Recommended prerequisite tracks

- [Sensors and Instrumentation](../sensors-instrumentation/index.md)
- [Digital Signal Processing](../dsp/index.md)
- [Physics Foundations](../physics/index.md)

## NPTEL begins with electrodes and sensors, not a classifier

The [official NPTEL Biomedical Instrumentation page](https://nptel.ac.in/courses/102106669) makes [Biomedical Instrumentation](139-102106669.md) the natural first spine. Physiological signals, electrodes, and sensors lead into amplification, recording, safety, and clinical applications. The public video sequence does not map perfectly to the 12-week syllabus, and Weeks 11–12 on lasers, safety, and regulation lack a clear correspondence. There is also no open project, laboratory, code, or item-by-item answer sequence. The course can explain the parts of a measurement chain, but it cannot supply a reproducible laboratory by itself.

Choose ECG, EEG, or PPG and draw physiology→electrode or sensor→front end→filter→ADC→stored record. For every stage, state units, dynamic range, bandwidth, noise source, saturation mode, and likely artifact. A clean-looking trace has little meaning while the conversion from ADC counts to voltage, electrode impedance, or the isolation boundary remains unknown.

Distinguish a schematic waveform used to teach a principle from a data record that documents acquisition conditions, annotation rules, and missing values. They support different strengths of evidence.

## One public ECG tests instrumentation, DSP, and physiological interpretation together

[Sensors and instrumentation](../sensors-instrumentation/index.md) supplies front ends, calibration, uncertainty, CMRR, and isolation. [Digital signal processing](../dsp/index.md) supplies sampling, filtering, spectra, phase delay, and validation. [Physics foundations](../physics/index.md) supplies bioelectric, optical, or acoustic interactions. For a clearly licensed public ECG, read the sampling rate, lead, units, annotations, and missing-data notes before marking baseline wander, mains interference, motion artifact, and clipping.

The processing task can have one objective, such as reducing mains interference without materially shifting QRS timing. Place raw and processed segments side by side, quantify amplitude and delay, and locate each anomaly in physiology, electrode, front end, or algorithm. “Smoother” is not a DSP metric, and device output is not diagnostic truth. A larger model cannot rescue an artifact that has no explanation in units and coupling.

If error distributions differ materially across leads, subjects, or devices, report those sources separately instead of publishing only one aggregate average.

## HST.582J becomes useful after the measurement chain is credible

The [public MIT HST.582J archive](https://ocw.mit.edu/courses/hst-582j-biomedical-signal-and-image-processing-spring-2007) supports [HST.582J](140-hst-582j.md) study in ECG or EEG processing, statistical estimation, image reconstruction, and segmentation. Many notes, labs, and MATLAB workflows are available, while several MRI, surgical-application, Random Signals III, and summary lectures lack notes. Old data links and MATLAB interfaces also need migration. A move to Python, MNE, NeuroKit2, or WFDB should use the same data, subject-level split, and metric and should be identified as a new implementation rather than the original MIT lab.

Before modeling, define the record list, annotation provenance, baseline, denominator, and non-diagnostic scope. Adjacent windows from one subject do not belong on opposite sides of a random train/test split. Claims about sensitivity, specificity, or segmentation error must weaken when annotation is not a clinical gold standard. A more complex model is worth discussing only after a simple baseline excludes subject leakage and acquisition-device shortcuts.

Image reconstruction and segmentation also require pixel spacing, scan protocol, and preprocessing to be recorded. If those acquisition differences correlate with labels, the model may be identifying a scanner or hospital rather than the intended physiological structure.

## Human subjects, safety, and privacy set the project boundary

Default to de-identified, clearly licensed public data or synthetic signals. State dataset version, checksum, sampling and units, license, exclusions, and retention. Do not collect human signals without ethics approval, and never connect homemade mains-powered, non-medically isolated, or unknown-leakage equipment to a person. Even a low-voltage wearable raises consent, privacy, skin-contact, battery, and deletion questions.

A credible closing work is either an error and safety budget for a public waveform or a strictly non-diagnostic beat-quality, artifact-rejection, or segmentation study. The first explains how saturation, disconnect, or motion propagates through the chain; the second gives the data version, code environment, result table, and anomalous records. Course material does not grant medical-device certification, clinical training, or diagnostic authority. Human acquisition, patient decisions, and device validation require ethics, clinical support, and qualified hardware.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Biomedical Instrumentation](139-102106669.md) | IIT Madras / NPTEL | Main course | Public-material guide | Partial or restricted |
| [Biomedical Signal and Image Processing](140-hst-582j.md) | MIT | Supplement | Public-material guide | Public assignments or labs |
