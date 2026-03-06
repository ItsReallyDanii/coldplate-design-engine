# Stage 7 Instrumentation and Sensors

**Document ID:** STAGE7-INS-001  
**Date:** 2026-03-06  
**Status:** PROPOSED  
**Companion to:** BENCHTOP_VALIDATION_PLAN.md, TEST_MATRIX.md  

---

## 1. Instrumentation Overview

| Channel | Measurement | Instrument type | Qty | Critical? |
|---------|------------|----------------|-----|-----------|
| T_in | Inlet coolant temperature | Type-T thermocouple | 1 | Yes |
| T_out | Outlet coolant temperature | Type-T thermocouple | 1 | Yes |
| T_heater | Heater surface temperature | Type-T thermocouple, embedded | 1 | Yes |
| T_top | Cold plate top surface temperature | Type-T thermocouple, surface-mount | 1 | No (informational) |
| P_in | Inlet pressure | Pressure transducer | 1 | Yes |
| P_out | Outlet pressure | Pressure transducer | 1 | Yes |
| Q | Volumetric flow rate | Turbine or ultrasonic flow meter | 1 | Yes |
| P_elec | Heater electrical power | Power meter (V × I) | 1 | Yes |

Total analog channels required: 8 minimum.

---

## 2. Sensor Specifications

### 2.1 Thermocouples

| Parameter | Specification |
|-----------|--------------|
| Type | Type-T (copper-constantan) |
| Range | −40 to +125 °C |
| Accuracy | ±0.5 °C (standard grade) or ±0.25 °C (special grade) |
| Response time | < 1 s (in water) |
| Junction | Exposed or grounded, depending on mounting |
| Wire gauge | 30 AWG (0.254 mm) for minimal conduction error |
| Quantity | 4 (T_in, T_out, T_heater, T_top) |

**Mounting notes:**

- T_in: Immersed in flow, 5 pipe diameters upstream of test section. Probe tip at center of flow channel.
- T_out: Immersed in flow, 10 pipe diameters downstream. Probe tip at center of flow channel.
- T_heater: Embedded in a shallow groove on the heater face, centered. Fixed with thermal paste.
- T_top: Surface-mounted on top face of cold plate, centered. Fixed with thermal tape or adhesive.

### 2.2 Pressure Transducers

| Parameter | Specification |
|-----------|--------------|
| Type | Piezoresistive or capacitive, gauge or differential |
| Range | 0–5 kPa (differential) or 0–110 kPa (absolute, 2 units) |
| Accuracy | ±0.5% FS (±25 Pa at 5 kPa range) |
| Output | 4–20 mA or 0–5 V analog |
| Wetted material | 316 SS or equivalent (compatible with DI water) |
| Quantity | 2 (P_in, P_out) |

**Mounting notes:**

- Co-located with thermocouple taps (same axial station).
- Pressure taps flush with pipe wall, no burrs.
- Short lines (< 30 cm) between tap and transducer to minimize lag.
- Bleed air from lines before each test session.

**Preferred configuration:** Single differential transducer across test section. If unavailable, use two absolute transducers and compute ΔP = P_in − P_out.

### 2.3 Flow Meter

| Parameter | Specification |
|-----------|--------------|
| Type | Turbine, ultrasonic (transit-time), or Coriolis |
| Range | 0–100 LPM (must cover expected ~44 LPM and sweep range) |
| Accuracy | ±2% of reading (or better) |
| Output | Pulse (turbine) or analog/digital |
| Wetted material | Compatible with DI water |
| Quantity | 1 |

**Mounting notes:**

- Downstream of test section (reduces bubble interference).
- ≥ 10D straight pipe upstream of meter, ≥ 5D downstream.
- Verify against timed volumetric collection (bucket test) at campaign start.

**Note on flow range:** Stage 4 predicts 44 LPM for candidate_02 at ΔP = 1000 Pa. This is an analytical estimate. Actual flow rates may differ significantly. Select meter range to cover 0.3× to 3× predicted (13–132 LPM). If actual flows are much lower than predicted, ensure meter accuracy is acceptable at the lower range.

### 2.4 Power Meter

| Parameter | Specification |
|-----------|--------------|
| Type | DC power meter or separate V + I measurement |
| Power range | 0–100 W |
| Accuracy | ±1% of reading |
| Measurement | True RMS voltage × current (if AC heater) or DC V × I |
| Quantity | 1 |

**Mounting notes:**

- Measure at heater terminals (excludes wiring losses).
- If using separate V and I: 4-wire voltage measurement, shunt or Hall-effect current sensor.

---

## 3. Data Acquisition System

| Parameter | Specification |
|-----------|--------------|
| Channels | ≥ 8 analog inputs |
| Resolution | ≥ 16-bit |
| Sample rate | 1 Hz per channel (minimum); 10 Hz if available |
| Thermocouple input | Built-in cold-junction compensation or external reference |
| Analog input | 0–5 V or 4–20 mA compatible |
| Interface | USB, Ethernet, or serial to logging PC |
| Software | LabVIEW, Python (with NI-DAQmx or equivalent), or MATLAB |

**Acceptable systems:**

- National Instruments USB-6009/6211 + thermocouple module (e.g., NI-9213)
- Keysight 34970A/34972A data acquisition switch
- Pico Technology TC-08 (thermocouples) + separate analog DAQ for pressure/flow
- Arduino-based DAQ (only if calibrated and validated; not preferred)

**Output format:** Timestamped CSV. See DATA_SCHEMA_STAGE7.md for column definitions.

---

## 4. Calibration Requirements

### 4.1 Thermocouples

| Requirement | Specification |
|-------------|--------------|
| Method | Ice-point check (0 °C) and boiling-point check (100 °C, adjusted for altitude) |
| Frequency | Before first test, and weekly during campaign |
| Acceptance | ±0.5 °C at both reference points |
| Record | Calibration date, offset, certificate number (if NIST-traceable) |

### 4.2 Pressure Transducers

| Requirement | Specification |
|-------------|--------------|
| Method | Zero-check (no flow, equalized lines) and span check against reference manometer or deadweight tester |
| Frequency | Before each test session |
| Acceptance | ±0.5% FS |
| Record | Calibration date, zero offset, span factor |

### 4.3 Flow Meter

| Requirement | Specification |
|-------------|--------------|
| Method | Timed volumetric collection (bucket test) at 3 flow rates |
| Frequency | At start of campaign and after any system change |
| Acceptance | ±3% agreement between meter reading and volumetric measurement |
| Record | Calibration date, flow rates tested, deviations |

### 4.4 Power Meter

| Requirement | Specification |
|-------------|--------------|
| Method | Verify against precision resistive load (known V, known R → known P) |
| Frequency | At start of campaign |
| Acceptance | ±1% of reading |
| Record | Calibration date, reference load, deviation |

---

## 5. Measurement Uncertainty Summary

| Measurement | Uncertainty | Propagated effect on R_th | Propagated effect on ΔP |
|-------------|-----------|--------------------------|------------------------|
| Temperature (T) | ±0.5 °C | ±0.04 K/W (~0.4% at 25 W, ΔT ≈ 280 °C·W) | — |
| Pressure (P) | ±25 Pa (0.5% FS) | — | ±50 Pa (~5% of 1000 Pa) |
| Flow rate (Q) | ±2% reading | negligible direct effect on R_th | ±2% on R_hyd |
| Power (P_elec) | ±1% reading | ±0.11 K/W (~1%) | — |
| **Combined (RSS)** | — | **~±1.1%** | **~±5.1%** |

These are instrument-level uncertainties. Systematic errors (parasitic heat loss, fixture conduction, pressure-tap misalignment) are not included. Minimize systematically through insulation, consistent tap placement, and energy-balance closure checks.

---

## 6. Safety Instrumentation

| Item | Specification | Purpose |
|------|--------------|---------|
| Over-temperature shutoff | Thermostat on heater, trip at 90 °C | Prevent thermal runaway |
| Overpressure relief | Relief valve set at 5× operating ΔP (5 kPa gauge) | Protect plumbing and transducers |
| Leak tray | Drip tray under test section, ≥ 1 L capacity | Contain spills |
| Emergency stop | Latching E-stop button on heater power supply | Cut heater power immediately |
| Ground fault protection | GFCI on heater circuit | Electrical safety with water present |

---

## 7. Optional Instrumentation

These are not required for Stage 7 pass/fail determination but provide additional diagnostic value.

| Instrument | Purpose | Priority |
|-----------|---------|----------|
| IR camera | Surface temperature mapping (top face) | Low — useful for uniformity but not required |
| Additional thermocouples (2–4) | Temperature profile across heater face | Medium — helps diagnose hotspots |
| Transparent test section | Flow visualization | Low — qualitative only |
| High-speed camera + dye | Flow distribution visualization | Low — qualitative only |
| Micro-CT (post-test) | Detect internal damage after testing | Medium — confirms structural integrity |

---

## 8. Procurement Checklist

| Item | Qty | Status |
|------|-----|--------|
| Type-T thermocouple, 30 AWG, exposed junction | 4 | NOT PROCURED |
| Pressure transducer, 0–5 kPa differential, ±0.5% FS | 1 (or 2 absolute) | NOT PROCURED |
| Flow meter, 0–100 LPM, ±2%, DI water compatible | 1 | NOT PROCURED |
| Power meter or V + I sensors, ±1% | 1 set | NOT PROCURED |
| DAQ system, ≥ 8 channels, ≥ 16-bit, TC-compatible | 1 | NOT PROCURED |
| Heater, thin-film or cartridge, 50 W max | 1 | NOT PROCURED |
| DC power supply, 0–50 W, controlled | 1 | NOT PROCURED |
| Chiller or constant-temperature bath, 25 °C ± 1 °C | 1 | NOT PROCURED |
| Pump, variable-speed, 0–100+ LPM | 1 | NOT PROCURED |
| Tubing, fittings, O-rings, thermal paste | Assorted | NOT PROCURED |
| Relief valve, E-stop, GFCI, drip tray | 1 each | NOT PROCURED |

---

## 9. Document Status

| Item | Status |
|------|--------|
| Instrumentation specification | PROPOSED — this document |
| Procurement | NOT STARTED |
| Calibration | NOT STARTED |
| Installation | NOT STARTED |

---

**End of document.**
