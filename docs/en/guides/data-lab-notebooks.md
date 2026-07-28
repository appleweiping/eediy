---
title: Data and Laboratory Records
description: Make experiments reviewable and recomputable with an immutable raw layer, structured metadata, and traceable analysis.
---

<div class="ee-language" markdown>
[简体中文](../../guides/data-lab-notebooks.md)
</div>

# Data and Laboratory Records

A laboratory record lets your future self or another learner answer what actually happened. A strong record connects plan, equipment, connection, raw data, anomalies, processing, and conclusions while protecting personal and restricted information.

## Purpose and learning outcomes

- Define samples, fields, units, naming, and stop conditions before an experiment.
- Separate an immutable raw layer from rebuildable processing.
- Record instrument settings, calibration, environment, and hardware revision.
- Trace every plot and conclusion to source data and code.
- Decide explicitly on privacy, retention, licensing, and sharing.

## Minimal environment

- An append-only paper or digital laboratory log.
- Open text or tabular data formats and version control.
- A way to generate unique run identifiers.
- A checksum tool and backup location.
- One low-risk simulated or measured dataset.

A computational notebook may support analysis but does not replace a chronological laboratory log. Record actual tool and format versions, and do not let a cloud service become the only copy.

## Learning sequence

1. **Plan template:** state objective, variables, controls, risks, stop conditions, and acceptance before work.
2. **Run identity:** assign a stable ID to each run and link hardware, firmware, operator, and time.
3. **Raw layer:** append without overwriting, then record checksums and any missing data immediately.
4. **Processing layer:** generate cleaned data by script and retain parameters, logs, and source-file mappings.
5. **Quality checks:** validate schema, units, ranges, monotonic time, missing values, and duplicate records.
6. **Conclusion links:** make report plots, tables, and numbers point to run IDs and analysis commits.

## Verification task: record three repeated measurements

Use synthetic data or a safe low-voltage RC measurement:

1. Create a data dictionary with fields, types, units, allowed ranges, and missing-value conventions.
2. Complete three independent runs and record settings, environment, and anomalies.
3. Freeze raw files and create a manifest with checksums.
4. Validate the schema and produce a tidy derived table by script.
5. Calculate repeatability and one uncertainty measure.
6. Starting from one run ID, locate the connection drawing, raw file, script, and final plot.

Acceptance requires an explicit quality-check failure when a unit is deleted or a run ID is duplicated.

## Common failures and diagnosis

- **File names cannot distinguish runs:** use stable IDs and put conditions in metadata rather than endlessly extending names.
- **Raw data was overwritten by cleaning:** restore a read-only raw layer and write every transform to a new directory.
- **Timestamps disagree:** record time zone, clock source, and mapping from device-relative time.
- **Units depend on memory:** define a data dictionary and preserve units in headers or metadata.
- **A plot has no provenance:** embed data ID, script commit, and parameter summary during generation.
- **An anomaly is deleted as an outlier:** first record a physical cause; exclusions need predefined, auditable rules.

## Reproducible evidence

- Experiment plan, risks, and stop conditions.
- Run manifest, data dictionary, and naming rules.
- Hardware, firmware, instrument identity, and settings.
- Read-only raw files, checksums, and backup record.
- Schema checks, cleaning scripts, and processing logs.
- Derived data and source mapping.
- Deviation, anomaly, exclusion, and correction logs.

## Cost, licensing, and accessibility

Text, CSV, and open compression formats are generally free and durable. For cloud storage, check capacity, export, region, and retention terms. Preserve license, citation, and redistribution conditions for third-party data in the manifest.

Use complete headers and units and do not encode status only by color. Give plots textual summaries and accessible tables. Low-bandwidth sharing can send metadata, summaries, and checksums first, then fetch large raw files when needed.

## Safety boundaries

- Do not publish identity, health, location, credentials, or restricted device data.
- Do not use real human-subject or patient data for unapproved self-study; prefer public de-identified data.
- A log is not a reason to continue past a real-time stop condition.
- On unexpected heat, current, odor, or damage, stop and isolate first, then record.
- Deletion must follow consent, institutional, and legal requirements, including backups.

## Completion checklist

- [ ] The data dictionary includes fields, types, units, and allowed ranges.
- [ ] Every run has a unique ID and complete environment/equipment metadata.
- [ ] The raw layer is append-only and checksummed.
- [ ] Processing is scripted and retains logs.
- [ ] Schema, missing, duplicate, range, and time checks are automated.
- [ ] Plots and conclusions trace to data and code.
- [ ] Anomalies, exclusions, and corrections are recorded explicitly.
- [ ] Licensing, privacy, sharing, and retention decisions are complete.

Next, create the experiment report with [Technical Writing](technical-writing.md), or automate data-quality checks through [Reproducible Engineering](reproducibility.md).
