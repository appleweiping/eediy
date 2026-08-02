---
title: SPICE Circuit Simulation
description: Make operating point, AC analysis, and transient analysis cross-check one circuit instead of treating a waveform screenshot as a conclusion.
page_type: guide
comments: true
---


# SPICE Circuit Simulation

The easiest bad habit to learn from SPICE is clicking Run first and selecting
an answer-looking feature from the waveform afterward. Reverse that order.
Before opening the solver, write down the expected order of magnitude of node
voltages, the likely dominant pole, and the direction of the step response.
Simulation should test those judgments, not invent them for you.

The tool need not be universal. The ngspice [documentation
page](https://ngspice.sourceforge.io/docs.html) provides its current manual
and archived versions, while the official
[tutorials](https://ngspice.sourceforge.io/tutorials.html) offer shorter
starting examples. Learners who prefer a graphical interface can use Analog
Devices' [LTspice technical
guides](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator/ltspice-recommended-reading-list.html).
What must remain consistent is the relationship among netlist, model,
parameters, analysis conditions, and conclusion.

## Leave three falsifiable predictions on paper first

Choose a safe small-signal active low-pass filter or two-stage amplifier. Draw
the supplies, reference ground, and a DC path for every node. Then estimate
three things by hand: the operating point and device region, the order of
magnitude of midband gain, and the pole most likely to dominate bandwidth.
Write the input amplitude, source impedance, load, temperature, and device
approximations beside them. A prediction need not be exact, but the simulation
must be able to disprove it.

Build the first circuit with ideal R and C elements and controlled sources.
This version checks topology and signs. Adding a complex vendor model at the
start mixes wiring faults, model faults, and numerical problems. Centralize
parameters and state their units in the netlist. If a GUI produces the
schematic, export and inspect a readable netlist so the simulated nodes and
parts are known to match what appears on screen.

Do not continue to the AC plot when the operating point is implausible. Check
bias current, power in each device, output headroom, and the point about which
the circuit is linearized. An amplifier that is already saturated at zero
input can still produce an attractive AC curve because the solver faithfully
linearized the wrong operating condition.

## Make `.op`, AC, and transient answer the same question

Compare `.op` with the handwritten operating point first. Then run an AC
sweep and extract midband gain, cutoff frequency, and phase as values, not
only as a screenshot. Use measurement statements or a script to write them to
text. Predict the direction of change before sweeping load or a key
capacitance. Use enough points to resolve the trend; a dense sweep cannot make
an incorrect model true.

Give a transient source a finite rise time and extend the observation window
beyond the expected time constant. Inspect clipping, slew, startup, and
settling. When AC and transient appear inconsistent, compare input amplitude,
bias, initial conditions, and the small-signal assumption. For a first-order
network, put the analytic response, AC cutoff, and step-response time constant
in one short report; all three should imply compatible parameters.

The repository's [offline RC low-pass
starter](https://github.com/appleweiping/eediy/tree/main/examples/rc-lowpass)
pairs a batch ngspice deck with an independent analytical generator. The deck
runs `.op`, transient, and AC analyses and reports \(t_0\), the 63.2% time,
delay-corrected \(\tau\), and half-power cutoff. Its README keeps analytical
reference, solver output, and the absent measurement class separate.

Now introduce a fault: open the bias path, leave one node without a DC path,
or move the load outside its intended range. An existing check should fail
unambiguously. If the only effect is that the plot “looks somewhat worse” and
no quantitative condition triggers, the process still depends on selecting a
story after the run.

## A convergence failure usually points to something unnatural

A singular matrix often indicates a floating node or missing DC path. A
collapsing time step often involves ideal switches, discontinuous sources,
stiff models, or unrealistic parasitic combinations. Reduce the circuit to
the last working minimum and restore elements one at a time. Blindly loosening
`reltol`, `abstol`, or the maximum time step can merely persuade the solver to
accept an untrustworthy trajectory.

When adding a transistor, op-amp, or power-device model, retain its retrieval
page, part number, version or integrity information, temperature range, and
license boundary. Public download does not necessarily grant redistribution
in a repository. Solvers also differ in dialect and extension support.
Sandia's [Xyce documentation and
tutorials](https://xyce.sandia.gov/documentation-tutorials/) provide a user
guide, reference guide, and netlist-translation material; consult the actual
compatibility information when batch or cross-solver work matters rather than
assuming that one `.cir` file is universally equivalent.

Review a model upgrade like any other design change. Freeze the inputs and
measurements, switch model versions, and compare operating point, bandwidth,
peaking, power, and convergence. A difference may represent more accurate
device behavior, or it may be a pin-order, default-parameter, or unit error.
Locate its origin before deciding that the new result is more credible.

## The simulation ends before power-up

Retain the schematic source, text netlist, solver and model provenance,
handwritten predictions, batch command, raw numeric output, and a short
account of mismatches. Add one component-tolerance or temperature study and
report the worst condition and its cause rather than typical only. Deleting
the output directory and running the batch command should regenerate every
number; the report should identify conclusions that still depend on
unmodeled package, layout, thermal, or manufacturing effects.

Stop once at this boundary. Simulated ground is not protective earth, an
ideal supply omits wiring and fault energy, and an absolute maximum rating is
not an operating recommendation. A passing waveform does not authorize
connection to mains, substantial stored energy, high-power RF, lasers, or
rotating loads. Those require qualified facilities, trained supervision,
independent protection, and physical measurement. Without those conditions,
finish the project explicitly as a simulation result.

Next, use [PCB and KiCad Workflow](pcb-kicad.md) to translate model
assumptions into layout, return-path, and test-point constraints, or
[Numerical Computing](numerical-computing.md) to study step size, residuals,
and convergence. The valuable SPICE artifact is not a waveform picture; it is
a traceable prediction that was confirmed, corrected, or rejected.
