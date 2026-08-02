## 6.071J, Real Analog, and 6.091 assume different benches

The [official MIT 6.071J archive](https://ocw.mit.edu/courses/6-071j-introduction-to-electronics-signals-and-measurement-spring-2006) joins electronics, signals, and measurement across 25 laboratory sessions plus written work and quizzes. [6.071J](024-6-071j.md) suits someone with general oscilloscopes, generators, and data-acquisition equipment who is willing to replace an old LabVIEW workflow; its public answer sequence is incomplete. [Real Analog](027-real-analog.md) connects notes, exercises, and experiments more tightly. Its [official equipment page](https://digilent.com/shop/coursework-learning-resources) centers on Analog Discovery 2 or 3, so price and regional supply directly affect feasibility. [MIT 6.091](025-6-091.md) is a compact immersion in soldering, transistors, logic parts, and motor interfaces rather than a semester of continuous feedback.

Normally use 6.071J or Real Analog as the through-line and select one 6.091 exercise for a specific weakness. A well-equipped general bench favors the range of 6.071J. Existing access to the specified Digilent instrument favors Real Analog. Limited bench time may support 6.091 for basic operation, but not replace continuous circuit and error analysis.

## The first experiment happens before power is applied

Given a schematic, use [circuit analysis](../circuits/index.md) to mark ground reference, test points, and current paths. Calculate the DC operating point, waveform range, and device dissipation, then state which reading requires immediate shutdown. A DMM current range can short a node, an earth-referenced oscilloscope clip cannot attach to an arbitrary floating point, and probe capacitance can alter a high-impedance node. These judgments come from circuit structure and instrument inputs rather than copied wiring diagrams.

If KCL and KVL, controlled sources, first-order transients, sinusoidal steady state, and elementary op amps remain uncertain, wiring mistakes will overwhelm the laboratory. If analysis is sound but current limits, probe attenuation, triggering, and sampling are unfamiliar, begin with the smallest 6.091 instrument exercise. The first result should be a prediction with units and tolerance that measurement is allowed to contradict, not a goal worded as “obtain the textbook waveform.”

## A migrated lab also changes instrument loading and error

The LabVIEW virtual instruments, old DAQ, and some components in 6.071J need replacement. Moving Real Analog from an Analog Discovery to a bench oscilloscope and source changes input impedance, range, sampling, and data export. The 555, TTL, and old ADC/DAC converters in 6.091 need fresh pinout and rating checks. Compare substitutes around the measurand, stimulus, bandwidth, accuracy, and decision rule; similar screenshots do not establish equivalent experiments.

Physical work stays isolated, low voltage, and current limited, with power removed for rewiring and no connection to mains, people, or unknown supplies. A public demonstration can explain a phenomenon, but it remains a demonstration when BOM, calibration, raw data, and anomalous runs are absent. A port should state the original year, substitutions, instrument models, and unavailable residential guidance rather than attributing modern-tool convenience to the course.

## One small system should survive repeated measurement

Choose a low-voltage system containing a sensor input, gain or filtering, and a load. Its schematic, BOM, rating check, instrument settings, calibration, hand prediction, raw data, and figure-building script should point to the same test nodes. Measure probe loading or component tolerance, then introduce an open circuit, wrong value, or bias fault. Explain the debugging sequence through actual observation, smallest hypothesis, one changed variable, and the new reading.

Separate resolution, repeatability, and systematic effects in the uncertainty budget, then hand the written procedure to another learner for one repeated metric. Log the first ground, range, test point, or shutdown condition they must guess and revise the procedure until that guess disappears. If the remaining discrepancy is a sensor transfer or noise term, carry the raw trace and calibration into instrumentation; if it is an event-timing or peripheral state, carry the same trace into embedded systems. The successful handoff is the repeatable measurement, not the number of laboratories attempted.
