---
title: Technical Writing
description: Write EE problems, methods, data, and limits so another person can judge and reproduce the work.
page_type: guide
comments: true
---

# Technical Writing

A weak technical document leaves the reader with only the author's assurance that the work was done. The question, operating conditions, conclusion supported by the data, and remaining unknowns should all be findable in the text. A test report, design note, and operating procedure serve different readers, but each must connect engineering judgment to traceable facts.

## Decide what the reader must do next

Before drafting, complete the sentence “The reader will use this document to …” A design choice calls for requirements, candidate designs, and tradeoffs. Reproduction calls for equipment, connections, versions, steps, raw data, and abnormal conditions. Maintenance calls for interfaces, normal state, hazard boundaries, and a diagnostic path. One long document that tries to be paper, manual, and lab notebook usually gives none of those readers a clear entry point.

The IEEE Professional Communication Society guidance on [effective engineering reports](https://procomm.ieee.org/communication-resources-for-engineers/written-reports/write-effective-reports/) separates methods, results, and discussion: what was done, what was obtained, and what the result means. That distinction is valuable even for a course project. Do not announce success inside the methods section, and do not introduce new data for the first time in the conclusion.

Make the title and opening specific to the object and operating range. “Low-noise amplifier design” reveals little; “Noise–bandwidth tradeoff in a 5 V, 1 kHz–100 kHz sensor front end” identifies the boundary. A useful opening can often be four sentences: problem, method, principal quantitative result, and most important limitation. If those four cannot be written, the engineering question may still be too broad.

## Keep the conditions attached to every claim

A reliable engineering claim names the object, conditions, metric, value or direction, and method. “At 5 V, with a 10 kΩ load and 10× probe, the prototype's \(-3\ \mathrm{dB}\) bandwidth was … from three frequency sweeps” can be challenged and repeated. “The circuit had good bandwidth” cannot.

Distinguish predicted, simulated, and measured values. A simulation needs simulator and model source, versions, corner, initial conditions, and relevant solver settings. A measurement needs instrument, probe, calibration state, sampling, and processing. A theoretical result needs assumptions and the range in which its approximation holds. If all three curves share a plot, neither the legend nor the prose should call them simply “results.”

That IEEE engineering-report guidance also reflects several useful
habits: use terms consistently, define a symbol on first use, number figures
and tables in order, and tell the reader what each figure demonstrates. A
class report need not imitate an entire publication format, but formatting
must not hide definitions and conditions.

## Make figures state quantities, units, and test conditions

A plot must first answer what each axis represents. Quantity, unit, scale, sample interval, and processing should not exist only inside a script. Distinguish datasets with line style or marker as well as color. Split an overloaded figure instead of placing a legend over the data. Oscilloscope screenshots can preserve an abnormal event, but a report should also export data and redraw axes with proper quantities and units.

NIST's [SI manuscript guidance](https://www.nist.gov/pml/special-publication-811/nist-guide-si-check-list-reviewing-manuscripts) calls for standard quantity and unit symbols and warns against ambiguous, improvised abbreviations. In EE writing, pay special attention to `m` versus `M`, `V` versus `dBV`, Hz versus rad·s\(^{-1}\), RMS versus peak or peak-to-peak, and the reference behind any dB quantity. Put units in table headings and axes; do not leave a bare number to carry a dimension by implication.

A caption should contain the conditions needed to read the figure, not repeat its title. A frequency-response caption may name supply, load, probe, sweep method, and nominal or corner case. A waveform should state trigger, bandwidth limit, averaging, and time origin. A photograph should identify the test point and signal direction. If the reader must search three pages to learn what the blue trace represents, the figure has not finished its job.

## Keep uncertainty, anomalies, and negative results in the report

A measured value is not an error-free truth. NIST [Technical Note 1297](https://www.nist.gov/pml/nist-technical-note-1297) describes how to evaluate and express measurement uncertainty, distinguishing components obtained from repeated observations from those estimated using instrument specifications, calibration, and other information. A course report should at least state repetition and spread, the source of instrument accuracy and resolution, processing steps, and why the displayed significant digits are justified.

Do not add error bars to a figure before defining the measurand. Is it an instantaneous voltage, a steady-state mean, a fitted gain, or noise integrated over a band? State that first, then identify the factors that change it. When a complete uncertainty budget is unrealistic, report a known bound, repeatability, and the components that remain unquantified.

A negative result is design information. Oscillation that appears only with one probe ground lead suggests the measurement connection is part of the system. A corner that does not converge may be a numerical issue or a model boundary. If only two of three boards pass, showing the best board alone is misleading. Record the observation, diagnostic order, and strongest current explanation, and label a hypothesis as a hypothesis.

## Make every citation and version lead back to its source

Place a citation next to the claim it supports. For a datasheet, name manufacturer, part number, revision, and relevant table or figure. For a standard or paper, identify edition, date, or DOI. Prefer an institution's or author's primary page over a repost. The current IEEE Author Center [Reference Style Guide for Authors](https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?usp=sharing) covers common forms including datasheets, standards, reports, software, and online sources. A citation manager can format them, but it cannot verify that the cited version supports the sentence.

Keep the reproduction entry short and explicit: where the data live, which commit applies, what command to run, and which figure it creates. Preserve native schematic and PCB project files whether they are text or binary, and also export a PDF, netlist, BOM, or fabrication outputs so a reader without the same software and license can inspect the design. Large raw data may live in external storage if the document gives a stable identifier, checksum, or version.

A direct test is to give the document to someone unfamiliar with the project and ask that person to locate the conditions behind one major claim, recompute one metric from raw data, and distinguish measured from simulated work. If all three can be done without an oral rescue, the document is carrying its engineering meaning.
