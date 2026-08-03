---
title: Reproducible Engineering and Automated Verification
description: Rebuild EE results with pinned environments, one task entry point, automated tests, and an evidence manifest.
---

<div class="ee-language" markdown>
[简体中文](../../guides/reproducibility.md)
</div>

# Reproducible Engineering and Automated Verification

“It runs on my machine” is not reproducibility. Reproducible engineering derives accepted outputs from explicit inputs, environments, and commands and explains allowed differences. Hardware work must also separate what software can replay from what requires a named physical device.

## Purpose and learning outcomes

- Define raw inputs, authoritative parameters, generated artifacts, and nonrebuildable assets.
- Pin dependencies and record the observed runtime environment.
- Build, test, analyze, and document through one task entry point.
- Design deterministic checks and tolerance-aware numerical checks.
- Generate a machine-readable evidence manifest and useful failure diagnosis.

## Minimal environment

- Version control, a command line, and a small EE project.
- A textual environment or dependency manifest.
- Scriptable build and test tools.
- A checksum tool.
- Optional continuous integration; the core exercise runs entirely locally.

A container is an optional mechanism, not an automatic answer. Record its base image, target architecture, external models, hardware, and license requirements that cannot be packaged.

## Learning sequence

1. **Classify assets:** label source, raw data, configuration, generated output, and external artifacts.
2. **Create one entry:** expose stable commands for environment checks, tests, plot generation, and documentation.
3. **Pin the environment:** record tool and dependency versions, platform, and retrieval source.
4. **Control determinism:** fix random seeds, ordering, locale, and time handling.
5. **Define acceptance:** compare text exactly and use physically justified tolerances for floating-point or measured values.
6. **Rebuild cleanly:** run from scratch in a temporary or isolated environment and retain a manifest.

## Verification task: rebuild one complete micro-project

Choose a safe project containing computation, data, and a report:

1. Write an asset inventory and state whether each item is rebuildable and under what license.
2. Create one verification entry that checks environment, tests, data schema, figures, and documentation.
3. Fix seeds and make units, time zone, and sorting explicit.
4. Set a justified tolerance for key values and checksums for files.
5. Run twice from clean directories and compare evidence manifests.
6. Change one input deliberately and show that dependent output changes and verification identifies it.

Acceptance requires one command from source to report, with failures localized to a stage rather than a vague error.

## Common failures and diagnosis

- **An implicit dependency is missing:** start clean and record system-level tools.
- **Absolute paths leak into output:** use project-relative paths and configurable data roots.
- **Checksums differ every run:** remove timestamp metadata and fix order, seeds, and generator settings.
- **Floating-point output varies slightly:** use scientific tolerances and compare key quantities instead of full-file bytes.
- **A cache hides a missing step:** clear build directories and test a cache-disabled path.
- **Hardware results cannot replay exactly:** retain firmware, configuration, raw data, calibration, and an allowed statistical range.

## Reproducible evidence

- Source revision and annotated milestone.
- Environment, dependency, system-tool, and license manifests.
- Checksums for raw inputs and nonrebuildable assets.
- One build and verification command with stage logs.
- Test, schema, link, and documentation check summaries.
- Numerical tolerances, seeds, and allowed platform differences.
- Hardware revision, firmware, calibration, and measurement run IDs.

## Cost, licensing, and accessibility

Local scripts and free tools cover the core process. Cloud CI has quota, retention, and privacy costs; preserve a local equivalent first. Record commercial-tool license prerequisites and provide standard exports or alternative verification for people without access.

Use text logs with explicit stage names and errors. Automation must not convey result through red or green alone; output status words and diagnostic links. Low-bandwidth users can fetch a checksummed source snapshot and a small evidence bundle.

## Safety boundaries

- Review automation as code; do not expose secrets or attach hardware to untrusted contributions.
- Give CI credentials minimal scope and lifetime and keep them out of logs.
- Automated hardware tests need current limits, timeouts, emergency stop, and independent protection.
- Do not upload restricted models, personal data, or vendor-confidential material to public artifacts.
- Reproducible does not mean safe or correct; independent model and risk review remain necessary.

## Completion checklist

- [ ] Source, inputs, configuration, outputs, and external artifacts are classified.
- [ ] One stable command performs the build and all checks.
- [ ] Environment, dependencies, platform, and licenses are recorded.
- [ ] Randomness, ordering, units, and time handling are explicit.
- [ ] Deterministic and tolerance checks have stated rationale.
- [ ] The project rebuilds twice from clean directories.
- [ ] The evidence manifest traces to source, data, and hardware.
- [ ] Automation secrets and hardware risk boundaries are reviewed.

Next, apply the process to [Project Practice](projects.md) and freeze reproducible milestones through [Version Control](version-control.md).
