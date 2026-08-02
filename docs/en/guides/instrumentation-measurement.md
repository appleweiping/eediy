---
title: Instrumentation, Measurement, and Uncertainty
description: Start with probe loading, grounding, and sampling, then produce an explainable and reproducible RC sweep.
page_type: guide
comments: true
---

# Instrumentation, Measurement, and Uncertainty

An oscilloscope trace is not the circuit node itself. It is the joint response of the device under test, probe, oscilloscope front end, sampling, and processing. Extra decimal places cannot recover information lost through a ground short, probe loading, or aliasing. This guide separates those effects and then reconnects them in one low-voltage RC low-pass experiment. Before wiring anything, run the repository's [offline RC low-pass starter](https://github.com/appleweiping/eediy/tree/main/examples/rc-lowpass) and use its analytical response as the pre-measurement baseline. It contains no measured data and does not replace the connection, probe, or uncertainty records below.

The hardware is modest: a source capable of roughly a 1 V sine wave, a two-channel oscilloscope, intact passive probes with known ratings, a 1 MΩ resistor, and a 1 nF capacitor. Without physical equipment, add the probe's input resistance, capacitance, and ground-lead inductance explicitly to a SPICE model and make the same comparisons.

## Connecting a probe changes the circuit

A probe's DC input resistance is only one part of its model. At higher frequency, probe and scope input capacitance lower the input impedance, while ground-lead inductance can resonate with that capacitance. Tektronix's note on [minimizing probe loading](https://www.tek.com/en/documents/application-note/how-minimize-probe-loading-low-capacitance-probes-0) shows why high-impedance nodes are particularly sensitive to input capacitance. Keysight's [oscilloscope-probe selection guide](https://www.keysight.com/us/en/lib/resources/selection-guides/oscilloscope-probes.html) treats bandwidth, dynamic range, input impedance, and physical connection as properties of one measurement system rather than attributes of the scope alone.

Before measuring, copy four values from the probe or instrument documentation: attenuation, input resistance, input capacitance, and rated bandwidth. The scope-channel attenuation setting must match the probe's physical switch or the displayed units will be wrong by a fixed factor. Compensate an adjustable passive probe on the scope's reference square wave. Correct compensation there is necessary, but it does not prove negligible loading at every source impedance.

When investigating high-frequency ringing, avoid repeated use of Autoset as the only experiment. Keep the test point, vertical scale, and bandwidth fixed; compare the standard ground clip with a short ground spring, then use a probe with known input capacitance. Ringing that changes substantially with the connection points first to the measurement loop. A feature stable across all three connections is better evidence for an impedance discontinuity, poor decoupling, or a real oscillation in the circuit. This comparison is also why a trace image is incomplete without the probe model and attachment method.

## A ground clip is not an arbitrary zero-volt label

Tektronix's [ABCs of Probes primer](https://www.tek.com/en/documents/whitepaper/abcs-probes-primer) gives explicit guidance on grounding, terminal ratings, and connection order. On most bench oscilloscopes, the probe clip is bonded through the BNC shell and power cord to protective earth; channel grounds are bonded to each other as well. Attaching that clip to a non-ground node does not redefine the node as zero. It can short the node to earth through a low-impedance conductor.

For the safe, low-voltage, common-ground RC circuit in this guide:

1. Connect the probe to the scope first and verify attenuation and input mode.
2. With the circuit unpowered, connect the ground lead to the confirmed circuit common.
3. Attach the probe tip, make sure exposed contacts cannot brush adjacent nodes, and only then energize the circuit.
4. On removal, disconnect the tip first and the ground lead last.

Never remove protective earth, use a cheater plug, or otherwise “float the scope” to reach a floating node. Subtracting two ordinary channels does not increase either input's common-mode rating. A differential probe is suitable only when its differential range, common-mode range, earth rating, frequency derating, and measurement category all cover the application. A USB scope may still acquire an earth path through its computer, supply, or another instrument. Mains, high voltage, stored energy, switching-power nodes, RF power, and unknown floating systems are outside this exercise and belong in a lab with appropriate training, isolation strategy, and rated equipment.

## Bandwidth, sample rate, and record length answer different questions

NI's tutorial on [bandwidth, Nyquist sampling, and aliasing](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/acquiring-an-analog-signal--bandwidth--nyquist-sampling-theorem-.html) separates the analog front end from discrete sampling. Twice the highest frequency is a lower bound for an ideally band-limited signal, not a universal setting for faithful waveform shape. Practical waveform work usually needs a higher ratio. Once an out-of-band component has passed into the sampler and aliased, a digital filter applied afterward cannot reconstruct its original frequency.

| Control | What it determines | Frequent misinterpretation |
| --- | --- | --- |
| Probe/front-end bandwidth | Which components reach the sampler, with what amplitude and phase error | Reading only the scope's headline bandwidth and ignoring probe or bandwidth-limit settings |
| Sample rate | Time spacing and the frequency range representable without aliasing | Treating many samples as proof that the analog input was faithful |
| Record length | Captured duration and attainable frequency resolution | Using a short window and declaring an intermittent or slow effect stable |
| Vertical range and offset | Front-end headroom and use of converter resolution | Assuming that a trace inside the display cannot have overloaded an earlier stage |
| Trigger and acquisition mode | Which event is aligned and which rare events may be missed | Mistaking unstable triggering for a changing signal frequency |

Start by naming the highest frequency that matters to the question. A sine-amplitude measurement concerns its fundamental; a digital edge contains harmonics and cannot be specified by clock frequency alone. For an approximately first-order response, $0.35/t_r$ is a useful starting estimate from rise time to bandwidth, not a law for every pulse or filter. Deliberately toggle the analog bandwidth limit, increase sample rate, and extend the record. A spike that moves with those settings implicates the instrument chain. If the feature stays put while only noise grows, the added bandwidth is not helping this measurement.

## Use an RC cutoff to expose probe loading

Choose $R=1\ \mathrm{M\Omega}$ and $C=1\ \mathrm{nF}$, taking the output across the capacitor. The ideal cutoff is

$$
f_c=\frac{1}{2\pi RC}\approx 159\ \mathrm{Hz}.
$$

The relatively high resistance is intentional: the difference between ordinary 1× and 10× passive probes may become visible. If the probe is approximated as $R_p\parallel C_p$, connecting it across the output changes both the DC gain and the pole:

$$
f_{c,\mathrm{loaded}}\approx
\frac{1}{2\pi(R\parallel R_p)(C+C_p)}.
$$

This expression is a prediction to challenge with data, not a reason to trust nominal probe values blindly. Run the experiment as follows:

1. Measure R and C first, retaining the meter range and component tolerances. Set the source to about 1 Vpp with zero DC offset, and check whether its amplitude display assumes a 50 Ω or high-impedance load.
2. Measure input on CH1 and output on CH2 with matched attenuation and compensated probes. Begin with 10× probes and short ground connections to the same circuit common.
3. Sweep from 0.1 to 10 times the predicted cutoff with at least 15 logarithmically spaced points. After settling at each point, record frequency, input and output amplitude, and phase difference rather than saving only an image.
4. Compute $20\log_{10}|V_\text{out}/V_\text{in}|$. Estimate cutoff where the curve is 3 dB below its measured low-frequency gain. If that gain is not 0 dB, searching for an absolute -3 dB value is incorrect.
5. Keep the source, frequency points, and acquisition settings fixed while changing only the output probe to 1× (and correcting that channel's attenuation setting), or add one known shunt capacitor. Compare the shift in cutoff and low-frequency gain with the direction predicted above.

For a mismatch, localize along the influence chain: measured R and C and source output impedance first; probe $R_p/C_p$, attenuation, and ground length next; parasitics or a deficient model afterward. Change one factor at a time. Simultaneously changing probe, scale, sample rate, and wiring produces a difference that cannot be attributed.

## Carry uncertainty from specifications into the result

Resolution states a display or code increment; it does not state distance from the true value. NI's explanation of [absolute and system accuracy](https://www.ni.com/en/support/documentation/supplemental/18/calculating-absolute-accuracy-or-system-accuracy.html) shows how range, gain error, offset error, noise, and specifications for components in the chain contribute to a final result. For the RC sweep, include at least:

- uncertainty and temperature coefficients of the R and C measurements, which enter the theoretical cutoff directly;
- source frequency accuracy and output impedance, plus any load dependence of source amplitude;
- scope vertical gain, timebase, noise, and mismatch between channels;
- probe attenuation error, input resistance/capacitance, compensation state, and connection repeatability;
- uncertainty introduced by frequency spacing and the method used to estimate the crossing.

Label each input as a maximum bound, a standard uncertainty, or a statistic from repeated observations before combining it. Choose conservative bounds, propagation after conversion to standard uncertainties, or direct interval propagation to match that information. Root-sum-square combination is meaningful only when independence and distribution assumptions are defensible. Repetition estimates repeatability; it does not replace calibration or remove a systematic shift caused by the same probe.

A compact project can retain `connections.pdf`, `settings.md`, append-only `raw/rc_sweep.csv`, an analysis script or notebook, and `result.md` with model, values, units, and uncertainty interval. The raw CSV should include frequency, both channel amplitudes, phase, attenuation, bandwidth, sample rate, and record length. Mark overload, trigger loss, rewiring, or aborted points beside the affected observation. With those files, another person can recompute the curve and decide whether the conclusion belongs to the circuit or the measurement chain.

Next, organize scripts and metadata with [Data and Laboratory Records](data-lab-notebooks.md). If the experiment exceeds the energy classes excluded here, consult [Laboratory Safety](safety.md) and move it to a qualified facility.
