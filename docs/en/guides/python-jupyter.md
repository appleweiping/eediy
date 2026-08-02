---
title: Python, Jupyter, and Engineering Computation
description: Use one RC step-response dataset to connect equations, arrays, fitting, units, and a replayable computational record.
page_type: guide
comments: true
---


# Python, Jupyter, and Engineering Computation

This page analyzes one RC step-response dataset instead of cataloguing
Jupyter features. Fix the input, parameter, two estimators, and numerical
tolerance before opening the notebook. Plots and fits then answer those
questions instead of redefining success after a polished curve appears.

| Record field | What to state before computation |
| --- | --- |
| Input | Read-only CSV, time/voltage units, sample interval, and checksum |
| Parameter | RC time constant \(\tau\) |
| Methods | \(1-1/e\) threshold interpolation relative to step onset \(t_0\), plus exponential-model fitting |
| Synthetic-data acceptance | For example, \(\lvert\hat{\tau}-\tau_\mathrm{ref}\rvert \le \max(0.02\tau_\mathrm{ref}, \Delta t)\), fixed before viewing the result |
| Measured-data acceptance | A prior tolerance from sampling, noise, instrument, and model uncertainty—not an automatic 2% |

This compact experiment still requires equations, arrays, validation,
fitting, residuals, and units without expensive hardware. The official
[Python tutorial](https://docs.python.org/3/tutorial/index.html) is a useful
language reference. A learner who can already write functions and read files
does not need to finish the whole tutorial before beginning the record.

## Put decisive calculations in functions, not hidden cell state

Put reading, validation, estimation, and plotting in ordinary Python
functions. Let the notebook select an input, call those functions, and explain
the result. This is not ceremony for its own sake: it makes the calculation
testable and lets it run on a machine without a notebook front end. Consult
NumPy's [Quickstart](https://numpy.org/doc/stable/user/quickstart.html) as
needed, paying particular attention to shape, axis, slicing, and
broadcasting. A smooth plot is not evidence that an array has the intended
dimensions.

A sufficient project can remain small:

```text
rc-step/
├── data/raw/step.csv
├── src/rcfit.py
├── notebooks/rc-step.ipynb
├── tests/test_rcfit.py
└── results/
```

Treat `data/raw` as read-only and make `results` disposable. The input
loader should check required column names, finite values, strictly increasing
time, and sampling intervals; the parser must know whether a time field is in
seconds or milliseconds. Normalize units inside the computation and choose a
convenient SI prefix only for presentation. Suffixes such as `_s` and `_v`
are not a complete unit system, but they are safer than silent guessing.

## Estimate the same time constant in two ways

First generate a synthetic response with a known \(\tau\) and fixed random
seed. Replace it with a real CSV only when safe low-voltage measurement is
available. Locate the step onset \(t_0\) from the input channel or an explicit
trigger marker, then interpolate the time \(t_{63.2\%}\) at which the output
reaches \(1-1/e\) of its final change. The threshold estimate is
\(t_{63.2\%}-t_0\); treating the absolute threshold timestamp as \(\tau\)
would incorrectly include trigger delay. A second method can fit an
exponential model with \(t_0\) or delay represented explicitly. When
using SciPy, read the official [`curve_fit`
reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)
and state the initial values, parameter bounds, and what the returned
covariance does and does not show. Optimizer convergence alone does not make a
parameter physically meaningful.

The repository's [offline RC low-pass
starter](https://github.com/appleweiping/eediy/tree/main/examples/rc-lowpass)
deliberately sets \(t_0\) to 2 ms. Its standard-library analysis reports both
the absolute threshold timestamp and \(\tau\) after subtracting the trigger
delay, making the common mix-up directly testable.

Plot the original samples, fitted curve, and residuals. Report sample rate,
the estimated \(\tau\), the difference between the two methods, and the
assumptions behind threshold interpolation and model fitting. Then create
three deliberately bad inputs:

- remove a required column and require the input loader to fail immediately;
- shuffle the time values and forbid the fit from continuing silently;
- interpret milliseconds as seconds and require a numerical or dimensional
  check to catch the three-order-of-magnitude error.

Calculate a small array by hand as well. Legal NumPy broadcasting can produce
an output whose size appears plausible even when the operands are wrong.
Assertions at function boundaries are more useful than diagnosing the final
plot. If residuals retain a time-dependent structure, investigate the model,
baseline, delay, and sampling before printing more decimal places.

## Restart the kernel and run from the first cell

Jupyter's official [install and use
page](https://docs.jupyter.org/en/latest/install.html) distinguishes the
Notebook interface, JupyterLab, and kernels. Create an isolated environment
for the project and record the Python and package versions actually used;
“latest” is not a reproducible version. Clear output, restart the kernel, and
execute from the first cell. A failure reveals hidden state. Fix it in `src/`
and the tests instead of adding a note that says to run cell 17 first.

Also provide a command-line entry that rebuilds a result table, plot, and
short textual summary from the raw CSV. Put generated files in their own
directory, label axes with units, and use line style or markers as well as
color. The static summary should say what was estimated, how large the error
was, and where the model failed, so a screen-reader user, low-bandwidth
reader, or reviewer without the notebook can still understand the conclusion.

Environment locking should be proportional. Preserve a dependency manifest
and an observed version snapshot, but do not commit the interpreter, caches,
or an entire virtual environment. If the analysis must cross platforms, run
it in a second clean environment before deciding whether every patch version
must be fixed or a compatibility range is sufficient.

## Connect an instrument only after synthetic data works

Only after the synthetic-data path works should the input become a serial
stream, oscilloscope export, or acquisition interface. The acquisition
program needs an explicit range, sample rate, duration, timeout, and safe
default state. An exception must not leave a supply, heater, or actuator at
the last command. Preserve raw data without overwriting it; implement cleaning
and filtering in code and state beside the plot what was removed.

Before archival, run the command-line entry once in a clean environment. For
the same input, \(\tau\) must fall within the prior, physically justified
numerical tolerance, and the residual metric and expected failing tests must
also agree; matching only the order of magnitude is not the same result. The
record also carries the random seed, units, dependency versions, fit
parameters, tolerance rationale, and method limitations. Do not expose
patient data, personal identifiers, restricted device data, or credentials
through notebook cells or outputs.

Use [Data and Laboratory Records](data-lab-notebooks.md) for the metadata
fields and [Reproducible Engineering](reproducibility.md) for automated replay
and comparison rules. A numerical fit supports only the stated data range and
assumptions; it cannot replace ratings, protection, and on-site supervision
for higher-energy hardware.
