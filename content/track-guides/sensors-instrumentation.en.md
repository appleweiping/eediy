## Course 136 teaches instruments; Course 137 explains transduction

[NPTEL Electrical Measurement and Electronic Instruments](136-108105153.md) uses more than 84 videos/demonstrations on its [official page](https://nptel.ac.in/courses/108105153) to cover meters, bridges, oscilloscopes, transducers, and instruments. It maps measurement but offers no reproducible home lab, source, or answer loop. [Sensor Technologies](137-108106193.md) connects sensor physics, fabrication, and circuits over 8 weeks on its [official page](https://nptel.ac.in/courses/108106193), with no open build-and-test loop.

Both are lecture/demonstration resources. They omit calibration references, BOMs, raw observations, and stepwise feedback, so an outside learner has not performed those experiments. Course 136 asks how an instrument represents and loads a quantity; Course 137 asks how material or structure turns the measurand into an electrical quantity.

For each demonstration, tabulate measurand, reference, excitation, instrument range, displayed result, and any unpublished calibration step. For Course 137, add the sensor transfer relation, temperature dependence, and main noise or drift source. Joining the tables keeps device physics distinct from instrument readout.

## Course 138 is a specific, potentially paid PSoC sensor chain

[Sensors and Sensor Circuit Design](138-ecea-5340.md) has 5 modules, 5 assignments, a thermistor lab, and a project on its [Coursera page](https://www.coursera.org/learn/sensors-circuit-interface); the [Colorado media page](https://www.colorado.edu/ecee/media/2412) identifies material provenance. Practice requires a PSoC 5LP, LCD, components, oscilloscope, Windows tools, and possibly paid platform access. Treat Course 138 as the original project route only when hardware and registered access both exist.

Without PSoC or platform access, use Course 136 for measurement, selected 137 units for sensor physics, and an independent low-voltage implementation for practice. It is not a 138 assignment, grader result, or project. Taking all three repeats taxonomy without automatically improving calibration, uncertainty, or fault detection.

The PSoC route joins analog front end, ADC, firmware display, and assignments on one platform. A port must redefine how input range maps to ADC code, how sampling is triggered, and how an LCD or host marks invalid state; new drivers and board support remain independent work.

## Every stage from measurand to ADC carries units, noise, and headroom

Draw `measurand → transduction → excitation/bridge → gain/filter → ADC` for a thermistor, strain gauge, or capacitive sensor. State units, range, source impedance, noise, saturation, power, and bandwidth at every stage. Put amplifier common-mode/swing/noise from [analog electronics](../analog-electronics/index.md), sampling/settling from [signals and systems](../signals-systems/index.md), and reference/probe/grounding from [electronics laboratory](../electronics-laboratory/index.md) in the same table.

Translate the smallest required measurand change into sensor output, front-end voltage, and ADC codes. Refer reference, offset, gain, quantization, and noise errors back to measurand units. Resolution, accuracy, repeatability, hysteresis, and sensitivity receive separate entries. Digital averaging cannot recover front-end clipping, violated amplifier common-mode range, or sensor self-heating. A signal visible only through display decimal places already lacks analog headroom.

Give the error budget typical and worst-case columns. Calibration may estimate offset and gain; ADC steps set quantization; bandwidth and sample statistics describe random noise. Hysteresis and drift do not disappear into one static fit. Once all terms share measurand units, the useful change—gain, ADC bits, or reference quality—becomes visible.

## Put the thermistor laboratory through heating, cooling, and held-out data

For a low-voltage thermistor divider, set temperature range, response time, allowable self-heating, sample rate, and target error. Predict divider voltage from the datasheet model and actual resistance, then choose excitation and reference resistance for ADC headroom across the range. State reference-thermometer specification, supply, ADC reference, environmental settling time, and connection drawing. Collect repeated raw values at 5 or more points in both rising and falling directions.

Separate calibration data from an untouched test set and compare at least two of Steinhart-Hart, a lookup table, or a simple polynomial. Report residuals, repeatability, hysteresis, settling, and uncertainty rather than only \(R^2\). Change excitation or sample interval and test whether self-heating and dynamic lag move as predicted. Public or synthetic data can support analysis but cannot establish real ageing, contact thermal resistance, sensor accuracy, or front-end noise.

Plot heating and cooling separately on the same temperature axis. Define platform stability from reference-thermometer slope and wait time, retaining timestamps for a new settling calculation. Evaluate held-out data only after model selection; once its residuals drive a change in polynomial order, it is no longer an independent test set.

## Platform migration and industrial loops face separate version and safety boundaries

PSoC 5LP, LCD, components, and Windows IDE define Course 138. Another MCU requires new ADC reference, input-range, timing, driver, and test decisions; pin changes are not equivalence. Include schematic, firmware/notebook, raw/calibration/test splits, instrument range/state, environment, software release, and residuals. After normal tests, inject open, short, ADC saturation, overrange, or drift and require an explicit fault state.

Physical work remains isolated, current-bounded, and low voltage. Unknown industrial transducers, 4–20 mA loops, mains-referenced instruments, and body-contact measurements may introduce external supplies, ground potential, and isolation hazards and belong in suitable facilities. Replacing the acquisition tool does not change ratings or safe-connection requirements, and a course title is not permission to cross those boundaries.

Inject faults inside that low-energy boundary, using a controlled resistor or software stub for open/short cases rather than damaging unknown equipment. Keep faults distinct from normal overrange at raw-code, engineering-unit, and display layers. Requirements must say whether recovery is automatic, manually acknowledged, or latched.
