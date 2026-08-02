## ECE 4880, the millimeter-wave circuit course, and the antenna course are three spines

[Cornell ECE 4880](110-ece-4880.md) moves from link budgets, noise, mixers, and PLLs into transceivers and 6 labs. Its [official archive](https://ocw.ece.cornell.edu/courses/ece-4880-radio-frequency-systems/) lacks Lectures 1–5; its text, Simulink, and bench add cost. ECE 4880 is preferred for the RF-systems branch, not as a universal entry for the circuit or antenna branches. [RF and Millimeter-Wave Circuit Design](111-rf-and-millimeter-wave-circuit-design.md) uses 19 assignments and 5 labs for matching, amplification, mixing, oscillation, and synthesis. Its Qucs-S/Octave flow is discrete-device teaching rather than an IC design flow based on a PDK.

[Microwave Antennas](112-108105114.md) develops field integrals, arrays, apertures, and reflectors in 40 lectures without an open lab or coding project. [MIT 6.661](113-6-661.md) reconnects receivers, antennas, and signals through notes and 13 solved sets. After the shared base, choose one spine.

Choose by output: cascaded gain, noise figure, and link budget point to ECE 4880; a matching network, amplifier, or oscillator to the circuit course; pattern, polarization, and aperture efficiency to antennas. Use 6.661 to explain receiver-antenna-signal relations behind those figures, with each course owning one output instead of becoming a single RF encyclopedia.

## Bind every number to a reference plane, \(Z_0\), and a power definition

[Electromagnetics](../electromagnetics/index.md) supplies Maxwell equations, boundaries, wave impedance, propagation, and radiation; [circuit analysis](../circuits/index.md) supplies phasors, resonance, two-ports, and noise; [communication systems](../communications/index.md) supplies modulation, detection, SNR, and link requirements. Before CAD, convert impedance and S parameters under stated \(Z_0\), explain the Smith-chart path, and label gain, noise factor, and reference plane through a Friis cascade.

Available gain, transducer gain, mismatch loss, and realized antenna gain differ. Test reciprocity, passivity, or energy balance on declared-passive data; reserve stability for active small-signal two-ports. Anomalies may come from noise, reversed ports, normalization, or reference-plane error. Graphs state dB, dBm, or linear power units, frequency units, port direction, polarization, and coordinates.

Moving a reference plane absorbs fixture phase/loss into or out of the DUT; changing \(Z_0\) changes wave normalization and S parameters. Define power wave, available power, and delivered power on one port diagram. For antennas, separate directivity, radiation efficiency, and mismatch. Show each conversion so changes can be assigned to device, matching, or coordinates.

## Outside work ends at calibrated passive data or explicitly scoped simulation

ECE 4880 retains useful problems and exams despite 5 missing lectures; its 6 labs need a source, scope or spectrum analyzer, and VNA capability. The provider says most millimeter-wave labs use Qucs-S/Octave, but the course may be paid and no stable anonymous official starter was verified. Antennas is lecture/assignment led. Outside a lab, use public S2P, circuit/EM simulation, and dummy-load/cabled models, stating grid, calibration plane, substrate, loss, mesh, boundary, power, and release.

With a VNA, perform open/short/load/thru or equivalent calibration, move the plane to the fixture, and compare raw with de-embedded results. Without standards, do not claim precise device parameters. Restrict work to rated passive or cabled dummy-load paths; do not radiate without authorization, call a low-cost SDR calibrated metrology, or reconnect under power. Public RF S parameters need device, bias, temperature, fixture, and de-embedding conditions.

On Touchstone import, check format, units, real-imaginary versus magnitude-angle encoding, and port order. For EM, state mesh refinement, radiation boundary, substrate stack, and conductor loss, then check passivity or energy balance. Keep calibration, fixture, and DUT data separate so de-embedding remains traceable.

## Evidence layers one and two: passive S parameters and the active small-signal chain

The first layer is **passive S-parameter** evidence: under fixed \(Z_0\) and reference plane, use matching-network, filter, or antenna-port S2P/EM data to report \(S_{11}\), \(S_{21}\), insertion loss, reciprocity, passivity, and energy balance. The [IBIS Touchstone 2.1 specification](https://ibis.org/touchstone_ver2.1/touchstone_ver2_1.pdf) defines a linear-network container, not a passive-only format: it can hold active small-signal parameters and optional two-port noise data. This selected passive S2P cannot support active gain, noise figure, or IIP3.

The second layer is the **active small-signal gain/noise chain**. For the LNA, mixer, and later stages, state \(S_{21}\) or transducer/available gain, active two-port stability, noise factor, mismatch, and reference plane. Calculate cascade gain and Friis noise figure only from explicit noise parameters or an active-device or behavioral model. Passive S2P supports only passive-loss impact on the noise budget; it does not turn \(S_{21}\) into LNA gain.

The boundary is the first active device’s input plane. A filter or cable before the LNA attenuates signal and worsens system noise figure according to physical temperature; the same loss after a high-gain LNA has a different effect. Use linear gain/noise factor in Friis and convert to dB only for display.

## Evidence layers three and four: two-tone IIP3 and LO phase-noise PSD

The third layer is **linearity**. For a nonlinear two-tone sweep, state tone spacing, input range, and output fundamental/IM3 fit intervals. Extrapolate IIP3 only where slopes remain near one and three before compression. Linear S-parameter simulation has no intermodulation mechanism and cannot establish blocker tolerance.

The fourth layer is **LO quality**. For an oscillator/PLL model, report phase-noise PSD versus offset, state the SSB convention, carrier frequency, and integration band, then calculate RMS phase/time jitter and connect it to mixer reciprocal mixing or sampling aperture. IIP3 describes amplitude nonlinearity and phase noise describes random phase; neither follows from the other or the same sweep, and a clean transient edge cannot replace the PSD and integration band.

The layers may share band, link budget, and port diagram, but each gives its model, units, command, and claim boundary. An antenna case adds impedance, efficiency, pattern, polarization, and mesh convergence. A compliant bench compares rated passive/cabled paths with calibration and repeats; other claims remain model-limited.

Label each row as public passive S2P, linear active/noise model, nonlinear device model, or oscillator/PLL model. Identical device names need not share bias, temperature, or process corner. The link budget must expose direct inputs, calculated results, and values awaiting compliant measurement.
