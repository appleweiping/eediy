---
title: Data and Laboratory Records
description: Trace a measurement back through wiring, instruments, raw files, and processing code so the record can explain where the number came from.
page_type: guide
comments: true
---


# Data and Laboratory Records

The hardest part of a lab record to reconstruct is rarely the conclusion. It is the detail that seemed impossible to forget at the time: whether the probe was at 1× or 10×, which firmware commit was running, or whether the CSV time column meant seconds or milliseconds. Once a curve looks suspicious, any one of those omissions can make the measurement impossible to interpret.

Do not begin by shopping for an electronic lab notebook. Begin with one small measurement, such as a safe low-voltage RC step response, and require a path from any point in the final plot back to a run, a raw file, a wiring and instrument state, the processing code, and the reason that point appears in the figure.

## First ask what produced this row

Before power is applied, assign a short, stable `run_id`. Record UTC time, hardware revision, firmware commit, instrument model, probe ratio, range, sample rate, stimulus, relevant environment, and calibration reference. The ID is a join key, not a filename into which every condition must be compressed. A changed condition creates a new run. A mistaken entry gets an appended correction rather than a rewrite that makes the past look cleaner than it was.

Place a machine-readable data dictionary beside each raw CSV. At minimum it should define column names, types, units, allowed ranges, missing-value representation, and the time basis. The W3C [Model for Tabular Data and Metadata on the Web](https://www.w3.org/TR/tabular-data-model/) describes metadata at table, row, column, and cell level and treats validation separately from display. A small project need not implement the full standard; the useful lesson is that units and constraints are part of the data interface, not facts kept in someone's memory.

A compact run record should answer questions like these:

| Object | Minimum information | When it matters |
| --- | --- | --- |
| Device under test | board or part ID, revision, connection drawing | two nominally identical boards behave differently |
| Acquisition chain | instrument, channel, probe, range, sample settings | diagnosing clipping, aliasing, or probe-ratio errors |
| Time | UTC, device-relative time, trigger point | joining streams from multiple devices |
| Data | file checksum, schema version, missing-data note | a file is moved, renamed, or damaged |
| Processing | code revision, parameters, input and output IDs | a plot no longer agrees with the measurement |

## A notebook may explain data, but it must not rewrite the event

When acquisition finishes, close the file and calculate its checksum before analysis is allowed to read it. Keep instrument exports and acquisition-time metadata under `data/raw/`; write baseline correction, resampling, filtering, and unit conversion to `data/derived/`. If a raw file contains a malformed row, do not quietly repair it in place. Make the transform report the row, the chosen treatment, and the new output. That separation preserves the difference between what the instrument emitted and how it was later interpreted.

Jupyter is useful for placing equations, plots, and commentary together, but it is a poor sole chronology. Cells can run out of order and memory can retain stale variables. Let the notebook call ordinary read and analysis functions, and make it run top to bottom from an empty kernel; retain acquisition logs, raw files, and parameters elsewhere. When the chain spans several datasets or people, the Entity, Activity, and Agent relations in W3C [PROV-O](https://www.w3.org/TR/prov-o/) are a useful naming test: an activity uses an input entity, generates another entity, and is associated with a person or software agent. The point is a legible lineage, not a knowledge graph for a single RC experiment.

There is a direct test of whether this works. Pick a point in the final figure at random and locate, within a few minutes, the derived-table row, transform parameters, raw row, and run settings. A notebook screenshot is not enough. A CSV with the right name but a different checksum is not enough either.

The repository's [offline RC low-pass
starter](https://github.com/appleweiping/eediy/tree/main/examples/rc-lowpass)
provides a small version of that trace. Its `manifest.json` labels the data
`analytic_reference` and records units, parameters, row counts, and CSV
SHA-256 values; a test tampers with one row and requires analysis to stop.
Because no instrument was involved, that manifest is not a measurement log.

## Make three RC steps expose the weak parts of the record

Use synthetic data, or collect three RC step responses under limited low-voltage conditions. Before the first run, state the nominal resistor and capacitor values and tolerances, predicted time constant, sample rate, and stop conditions. The circuit may remain unchanged across the three runs, or one run may deliberately use a different sample rate. What matters is that each run retains its identity instead of becoming three anonymous traces pasted into one table.

Then make the automated checks encounter three bad inputs:

- relabel one file's time unit from `ms` to `s`; a range or order-of-magnitude check should stop before fitting;
- duplicate a `run_id`; the uniqueness check should identify both conflicting records;
- remove the probe ratio or calibration date; the run should be marked insufficiently described rather than silently receiving a default.

For the valid files, use one script to estimate all three time constants. Report repeatability and identify other uncertainty components from instrument resolution, component tolerance, or calibration. NIST [Technical Note 1297](https://www.nist.gov/pml/nist-technical-note-1297) distinguishes components evaluated statistically from those evaluated by other information and describes how to combine and report them. It is useful after the measurand and inputs are explicit; it is not a formal name for an unexplained standard deviation. A sound result presents value, unit, uncertainty, and domain together instead of displaying unsupported decimal places.

## Recomputable does not automatically mean publishable

Before sharing, separate what another person needs for recomputation from what you have no right to disclose. Identity, health, location, credentials, vendor-confidential models, and license-restricted datasets do not become public merely because the project uses a public repository. For human or patient data, self-study should use lawfully published, de-identified datasets; removing names alone is not a sufficient analysis of re-identification risk.

If the dataset is ready for a durable deposit, add a stable title, creators, publisher, publication year, resource type, version, rights, and related-resource identifiers. The DataCite [Metadata Schema](https://schema.datacite.org/) is a practical way to check the information needed to identify, discover, and cite data. It belongs at publication time and does not replace probe settings or anomaly notes captured during acquisition. Citation and redistribution permission for third-party data are separate questions.

Finally, rerun the analysis from an empty directory and have another machine locate the same input using only the run record. If a large raw file cannot be public, publish its schema, field definitions, checksum, a way to create a small synthetic example, and the lawful access path. The analysis entry point can then move into [Reproducible Engineering](reproducibility.md), while [Technical Writing](technical-writing.md) can carry the plot lineage into the report.
