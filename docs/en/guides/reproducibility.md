---
title: Reproducible Engineering
description: Define what must agree, then use clean rebuilds, provenance, and safe automation to show that a result is not confined to one machine.
page_type: guide
comments: true
---


# Reproducible Engineering

“Reproducible” often hides three different promises: whether the same source builds a byte-identical firmware image, whether the same data yields metrics within a stated tolerance, and whether another run on the same hardware falls inside a predeclared statistical range. Each promise needs a different comparison. Putting every file in a container merely packages an undefined question.

Use a micro-project with input data, a calculation, and a short report. The objective is not an elaborate CI configuration. It is for another machine to run one command from explicit inputs, produce specified outputs, and know what to compare when the results differ.

The repository's [offline RC low-pass
starter](https://github.com/appleweiping/eediy/tree/main/examples/rc-lowpass)
is a runnable version of that exercise. Its Python path needs neither network
access nor third-party packages. From the repository root, run
`python examples/rc-lowpass/run.py`; it generates analytical inputs, writes
checksum-bearing provenance, computes step and AC metrics, and applies
precommitted tolerances. Its tests also require byte-identical inputs from two
fresh output directories.

## Name the kind of result that must be reproduced

For a compiled artifact, a strict definition is available. The Reproducible Builds project [defines a reproducible build](https://reproducible-builds.org/docs/definition/) as one in which any party, given the same source, build environment, and instructions, can recreate bit-for-bit identical copies of the specified artifacts. A matching checksum means something only after the specified artifacts and relevant environment are named. Decide in advance whether logs, signatures, and timestamps are inside or outside the comparison.

Numerical analysis should not automatically copy the byte-for-byte criterion. A different BLAS library, CPU, or parallel reduction order can alter trailing bits. Compare quantities with units, array shapes, conservation residuals, and physically justified tolerances instead. Hardware is less exact still: do not expect identical ADC samples. Fix the board revision, firmware, wiring, calibration, and environment, then compare a mean, spread, or frequency-response boundary. State the tolerance before seeing the second run, or it becomes an excuse invented for the discrepancy.

Write three sentences for the project:

1. **Inputs:** source revision, raw-data checksums, parameter files, and non-rebuildable external models.
2. **Outputs:** firmware, numerical tables, figures, and the parts of the report that actually support the conclusion.
3. **Comparator:** byte equality, numerical tolerance, structural property, or statistical interval.

If one sentence cannot be made concrete, narrow the claim before pinning more dependencies.

## One genuinely clean rebuild reveals hidden inputs

Keep one local entry point such as `make verify` or an equivalent task. It should read immutable inputs, generate into a new directory, and run schema checks, computation, tests, plots, and documentation in sequence. Execute it twice from a fresh clone, an empty cache, and a different absolute path. Any dependency on a user-directory setting, system font, “latest” model fetched from the network, or previous output should become visible.

The Reproducible Builds [technical documentation](https://reproducible-builds.org/docs/) catalogs timestamps, time zones, locales, file ordering, randomness, and build paths as common sources of variation. Do not add a cargo cult of environment variables. Change date, path, or locale one at a time, observe which value enters the output, and then remove it at the source or record it explicitly. A fixed random seed replays one sequence; it does not establish that a Monte Carlo conclusion is stable. Work that depends on randomness should also inspect the distribution across seeds.

A dependency record must answer both “which version was intended?” and “what was actually retrieved?” Retain direct and transitive versions, source locations, and checksums. When a commercial compiler, PDK, vendor model, or license server cannot be packaged, identify it as an external prerequisite and provide a lawful standard-format export or a smaller runnable substitute. A container describes user space; it does not automatically capture CPU features, instrument calibration, USB devices, or remote-service state.

## Provenance should explain one artifact, not merely list files

Generate a small `run.json` for each rebuild: source revision, entry command, public parameters, resolved dependencies, execution platform, start time, input and output checksums, tool versions, and hardware run IDs where applicable. SLSA 1.2 describes [provenance](https://slsa.dev/spec/v1.2/provenance) as verifiable information tracing an artifact to where, when, and how it was produced. A small project need not claim a SLSA level to benefit from separating the build definition from details of this particular execution.

Licensing needs more than a README sentence saying “open source.” The SPDX 3.0.1 [scope](https://spdx.github.io/spdx-spec/v3.0.1/scope/) covers software composition, build information, datasets, provenance and integrity, licenses, and copyrights. You may not need a complete SPDX document, but you should be able to answer whether each external library, model, and dataset may be modified, redistributed, or placed in a public artifact—and whether that answer remains true after a version change.

When comparing two `run.json` files, separate explanatory differences from accidental ones. Time and temporary paths that should not affect a specified output can be removed or normalized. Compiler, input checksum, or hardware-revision changes must remain because they may explain the result. A useful record leads from an anomalous figure to the inputs and command of that run, and from a dependency change to every output that needs rebuilding.

## CI is a second machine, not an arbiter

Make the local command reliable before delegating it to CI. A cloud failure can then be reduced locally, and the disappearance of a service does not remove the project's rebuild path. CI is good at exercising a clean environment, several platforms, and every commit. It is not a reason to give untrusted contributions access to credentials, license servers, or attached laboratory hardware.

GitHub Actions' [secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use) covers untrusted input and least-privilege tokens, and states that pinning a third-party action to a full commit SHA is the way to treat that reference as immutable. For an external pull request, separate jobs that read contributed source from jobs that hold secrets or control hardware. Logs must not expose tokens, patient data, or vendor-confidential material. Automated hardware also needs independent current limits, timeouts, an emergency stop, and a safe power-on state; a software assertion cannot be the only protection.

Finish with deliberate damage. Change one raw input and show that dependent figures and prose update. Remove an external tool and make the failure name the missing prerequisite. Change locale or working path and confirm that specified results still satisfy their comparison rules. The process becomes useful when another machine can start empty, reproduce the same class of conclusion, and explain unavoidable differences through a particular input or platform. Measurement files can then follow [Data and Laboratory Records](data-lab-notebooks.md), while [Version Control](version-control.md) preserves the rebuildable milestone.
