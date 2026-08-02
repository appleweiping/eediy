---
title: "Energy Storage and Photovoltaics"
description: "Electrochemical storage, solar cells, system modeling, and energy management with explicit battery, laser, and high-voltage safety."
page_type: track
track_id: "track-energy-storage-pv"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 99855e0c76a51a45 -->

# Energy Storage and Photovoltaics

## Track position

Electrochemical storage, solar cells, system modeling, and energy management with explicit battery, laser, and high-voltage safety.

## Recommended prerequisite tracks

- [Semiconductor Devices](../semiconductor-devices/index.md)
- [Circuit Analysis](../circuits/index.md)
- [Engineering Mathematics](../mathematics/index.md)

## Photovoltaics and electrochemistry are separate device spines until a system question joins them

The [official TU Delft Photovoltaic Energy Conversion page](https://www.edx.org/learn/solar-energy/delft-university-of-technology-solar-energy-photovoltaic-pv-energy-conversion) organizes [Photovoltaic Energy Conversion](122-pv-energy-conversion.md) (PV) around sunlight, the solar cell, modules, and systems. It fits questions about how irradiance and temperature become DC power and supports hourly energy-yield models. Videos, notes, and open companion material are available, while free edX access, certificates, and activities can change by session.

The [official MIT 10.626 archive](https://ocw.mit.edu/courses/10-626-electrochemical-energy-systems-spring-2014) gives [10.626](123-10-626.md) 38 class sessions, 5 problem sets without solutions, 1 solved midterm, and 1 unsolved final on thermodynamics, kinetics, transport, batteries, fuel cells, and other electrochemical systems. It is a graduate Chemical Engineering course with 10.50 Analysis of Transport Phenomena as its stated prerequisite, not a pack-integration or BMS course. The two courses are not sequential: choose TU Delft for solar cells, modules, and yield, and 10.626 for electrochemical cell-scale modeling. Study both only when load, sunlight, and storage exchange power on the same timeline.

Coupling both models immediately mixes irradiance forecasting, device conversion, cell state, and dispatch errors. Establish separately checkable input-output relations first; only then does an energy-allocation result have a readable causal chain.

## PV starts from junctions and equivalent circuits; storage from conservation and transport

PV uses pn junctions, generation and recombination, current-voltage behavior, and temperature dependence from [semiconductor devices](../semiconductor-devices/index.md), together with equivalent circuits, power, efficiency, and dynamic loads from [circuit analysis](../circuits/index.md). A simple one-diode model should predict how irradiance and temperature move `Isc`, `Voc`, and maximum power and show where series and shunt resistance appear on the curve.

MIT 10.626 relies more heavily on differential equations, diffusion, nondimensionalization, parameter estimation, and numerical stability from [engineering mathematics](../mathematics/index.md). Derive a one-dimensional diffusion or reaction model from conservation and boundary conditions, separating voltage loss, state of charge (SOC), capacity, energy, power, and charge. Curve fitting with no account of parameter identifiability is not yet a credible component model for dispatch optimization.

Check a photovoltaic curve at open circuit, short circuit, and the maximum-power point. Check an electrochemical model against mass or charge conservation, its initial state, and its boundary flux. Parameters can compensate for one another while fitting the same interval, so report an identifiable range rather than presenting one optimum as a unique physical value.

PV can use pvlib and public weather or module data, while storage can use PyBaMM and public cell datasets. Software version, license, temporal resolution, missing-data treatment, parameter set, solver tolerance, and thermal boundary all affect results. Do not fabricate or dismantle cells, cycle unknown or damaged batteries, assemble an unprotected high-voltage pack, or connect rooftop PV to mains. Even a supervised bench should use certified low-voltage modules, a BMS, current limiting, temperature monitoring, and fire containment.

Many device questions can be answered with public data and simulation. When qualified supervision and suitable hardware are absent, limiting conclusions to the model is more rigorous than exchanging safety for uncalibrated measurements.

## Test the model's range on cloudy, depleted, and hot cases

A PV model can connect irradiance, temperature, module behavior, and MPPT. A storage model can connect current, state of charge (SOC), voltage, and temperature. Use hand limits and one data interval to identify parameters, then apply weather or a drive cycle excluded from fitting to examine energy error, voltage or temperature residuals, and constraint violations. Change one device parameter and one operating condition so aggregate RMSE does not hide low irradiance, low state of charge, temperature extremes, or ageing mismatch.

Errors dominated by junction and recombination physics point toward PV devices. Electrode kinetics and transport point toward electrochemical materials. Once the component models are credible and conversion, MPPT, or grid control remains, power electronics is the narrower branch. Coupled dispatch answers a system question only after the PV and storage port models each explain data on their own rather than letting an optimizer conceal a device-model gap.

Show residuals by operating regime—for example cloudy intervals, low state of charge, and high temperature. A sharp increase near one boundary calls for a narrower validity claim or a revised physical model; an aggregate average cannot make that decision.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Solar Energy Engineering: Photovoltaic Energy Conversion](122-pv-energy-conversion.md) | Delft University of Technology | Main course | Public-material guide | Partial or restricted |
| [Electrochemical Energy Systems](123-10-626.md) | MIT | Main course | Public-material guide | Partial or restricted |
