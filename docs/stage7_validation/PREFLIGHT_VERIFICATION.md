# Stage 7 Preflight Verification List

**Document ID:** STAGE7-PF-001  
**Date:** 2026-03-06  
**Status:** READY FOR USE — complete before test day  
**Candidate:** candidate_02_diamond_2d_s1045  
**Companion documents:** BENCHTOP_EXECUTION_CHECKLIST.md, RUN_SHEET_CANDIDATE_02.md  

> **Purpose:** Confirm that all bench-side readiness conditions are satisfied
> before the first heater power-on.  All five sections must be signed off.
> This document is a one-time pre-test check, not a recurring procedure.

Completed by: _____________________________  
Date: _____________________________  
Countersigned by: _____________________________  

---

## 1. Instrumentation Availability

Confirm each instrument is physically present, powered, and reading correctly
before specimen installation.

| # | Instrument | Required spec | Present? | Reading plausible? | Calibration current? | Notes |
|---|-----------|--------------|---------|-------------------|---------------------|-------|
| 1.1 | Thermocouple — T_in (Type-T, 30 AWG) | ±0.5 °C | ☐ | ☐ | ☐ | |
| 1.2 | Thermocouple — T_out (Type-T, 30 AWG) | ±0.5 °C | ☐ | ☐ | ☐ | |
| 1.3 | Thermocouple — T_heater (Type-T, embedded) | ±0.5 °C | ☐ | ☐ | ☐ | |
| 1.4 | Thermocouple — T_top (Type-T, surface-mount) | ±0.5 °C | ☐ | ☐ | ☐ | |
| 1.5 | Ambient temperature sensor — T_amb (TC or thermistor, free air) | ±1 °C | ☐ | ☐ | ☐ | |
| 1.6 | Pressure transducer — P_in | 0–5 kPa differential or 0–110 kPa absolute; ±25 Pa | ☐ | ☐ | ☐ | |
| 1.7 | Pressure transducer — P_out | Same as P_in | ☐ | ☐ | ☐ | |
| 1.8 | Flow meter — Q | Range set from physics-based estimate (not Stage 4 Q); ±2% of reading at expected flow | ☐ | ☐ | ☐ | Range (LPM or mL/min): ______ |
| 1.9 | DC power meter — P_elec | 0–100 W; ±1% | ☐ | ☐ | ☐ | |
| 1.10 | DAQ / data logger | ≥ 9 channels; 1 Hz minimum sample rate | ☐ | ☐ | ☐ | Channels confirmed: ______ |

**Day-of calibration spot checks (record results):**

| Check | Instrument | Expected | Measured | Pass? |
|-------|-----------|---------|---------|------|
| TC ice-bath (0 °C) | T_in, T_out, T_heater, T_top, T_amb | 0.0 ± 0.5 °C | | |
| Pressure zero (lines closed, atmospheric) | P_in, P_out | 0 Pa ± 25 Pa differential | | |
| Power meter zero (heater disconnected) | P_elec | 0.00 ± 0.05 W | | |
| Flow meter bucket check | Q | Volume match ±3% | | |

**Section 1 sign-off:** All 10 instruments present, reading, and calibration
current.  Spot checks passed.

Signature: _____________________________  Date/Time: _____________________________

---

## 2. Thermal Interface Material Specification

Specify the TIM **before** mounting the specimen.  Record here and in the
run sheet.

| Field | Value to record |
|-------|----------------|
| TIM type | (paste / pad / foil / solder / other) |
| Product name and manufacturer | |
| Lot or batch number | |
| Thermal conductivity (W/m·K) | |
| Typical bond-line thickness at specified clamp pressure (mm) | |
| Expected thermal contact resistance at bond-line thickness (K·cm²/W) | |
| Applied using | (syringe / spatula / pre-cut / other) |
| Applied by | |
| Clamp pressure or torque spec used | |

> **Why this matters:** TIM contact resistance adds directly to measured R_th.
> For the 4 mm² heater footprint at nominal 25 W, even 0.5 K·cm²/W contact
> resistance contributes approximately 12.5 K/W — comparable to the simulation
> R_th of 11.27 K/W.  The simulation does not model contact resistance; the bench
> comparison must account for it in the uncertainty budget (see STAGE7-AUD-001
> W-4 and M-2).  TIM must be identical across all repeats.

**TIM application procedure:**

1. Clean heater face and specimen bottom face with isopropyl alcohol; allow
   to dry fully.
2. Apply TIM per manufacturer application instructions for the specified type.
3. Assemble and apply specified clamp pressure or fastener torque.
4. Allow cure time per manufacturer datasheet (if applicable) before
   starting coolant flow.

**Section 2 sign-off:** TIM type, batch, and contact resistance estimate
recorded above.  Application procedure followed.

Signature: _____________________________  Date/Time: _____________________________

---

## 3. Ambient Logging

Ambient temperature affects parasitic heat loss to the environment.  It
must be logged continuously throughout the test session.

| # | Requirement | Status |
|---|------------|--------|
| 3.1 | T_amb sensor is installed in free air, away from heater exhaust and coolant lines | ☐ |
| 3.2 | T_amb channel is included in the DAQ recording and will appear in all timeseries CSV files | ☐ |
| 3.3 | Ambient temperature at session start is recorded in the run sheet end-of-session record | ☐ (fill in at start) |
| 3.4 | Ambient temperature at session end is recorded in the run sheet end-of-session record | ☐ (fill in at end) |
| 3.5 | If T_amb changes > 3 °C during a single test run, that run is flagged in its summary JSON | ☐ (monitor during test) |

**Accepted ambient range:** 20–26 °C.  If T_amb is outside this range at
the start of a run, delay the run or record the out-of-range condition
and note it as a limitation in the run summary.

**Section 3 sign-off:** T_amb sensor installed; DAQ confirmed to log it;
monitoring plan confirmed.

Signature: _____________________________  Date/Time: _____________________________

---

## 4. Fixture-Loss Calibration

A fixture-loss calibration run is required **before** installing the specimen
and **before** Phase A characterization.  This procedure brackets the
parasitic heat loss fraction, which is used in the energy balance integrity
check during Phase B.

**Required equipment:** Heater block, coolant loop (same configuration as
primary test), power meter, DAQ.  No specimen installed.

| Step | Action | Record | Pass criterion |
|------|--------|--------|---------------|
| 4.1 | Confirm coolant is flowing at the same pump setting as planned for Phase B | Q_cal at calibration = _____ LPM | — |
| 4.2 | Set heater to 10 W; wait for steady state (T_heater drift < 0.5 °C/min for 5 min) | T_heater, T_in, T_out, Q, P_elec at steady state | Steady state reached |
| 4.3 | Compute η_fixture_10 = (Q × ρ × cp × (T_out − T_in)) / P_elec | η_fixture_10 = _____ % | > 80% |
| 4.4 | Set heater to 25 W; repeat | η_fixture_25 = _____ % | > 80% |
| 4.5 | Set heater to 50 W; repeat | η_fixture_50 = _____ % | > 80% |
| 4.6 | Record all values in `calibration/fixture_loss_cal.json` | File saved | File exists |

**Interpretation:** η_fixture represents the fraction of electrical power
delivered to the coolant with no specimen present.  (1 − η_fixture) is the
parasitic loss fraction.  During Phase B, if the measured energy balance η
drops more than 5 percentage points below η_fixture, suspect a new loss path
(e.g., specimen leak or insulation gap).

If η_fixture < 80% at any power level: investigate and fix the fixture before
installing the specimen.  Do not proceed to Phase A until η_fixture ≥ 80%.

**Section 4 sign-off:** Fixture-loss calibration complete; results in
`calibration/fixture_loss_cal.json`; η_fixture ≥ 80% at all power levels.

η_fixture_10 = _____ %  
η_fixture_25 = _____ %  
η_fixture_50 = _____ %  

Signature: _____________________________  Date/Time: _____________________________

---

## 5. Data Capture Fields

Confirm DAQ is configured to capture all required columns before starting
any test run.

### 5.1 Timeseries CSV — Required Columns

Verify live in the DAQ display before Phase A.

| Column | Channel | Units | Present in live view? | Present in saved CSV? |
|--------|---------|-------|----------------------|----------------------|
| `timestamp_s` | DAQ internal clock | s | ☐ | ☐ |
| `T_in_C` | T_in thermocouple | °C | ☐ | ☐ |
| `T_out_C` | T_out thermocouple | °C | ☐ | ☐ |
| `T_heater_C` | T_heater thermocouple | °C | ☐ | ☐ |
| `T_top_C` | T_top thermocouple | °C | ☐ | ☐ |
| `T_amb_C` | T_amb sensor | °C | ☐ | ☐ |
| `P_in_Pa` | P_in transducer | Pa | ☐ | ☐ |
| `P_out_Pa` | P_out transducer | Pa | ☐ | ☐ |
| `Q_LPM` | Flow meter | LPM (or mL/min — match units to meter output) | ☐ | ☐ |
| `P_elec_W` | Power meter | W | ☐ | ☐ |

> **Note on `Q_LPM`:** Use the actual units of the procured flow meter.
> If the meter outputs mL/min, record in mL/min and rename the column to
> `Q_mL_min`.  Update all run summary JSON files to use the same unit.
> Do not compare to Stage 4 Q = 44 LPM regardless of unit.

### 5.2 File-Naming Confirmation

| Requirement | Check |
|-------------|-------|
| DAQ is set to save files as `{test_id}_timeseries.csv` per ARTIFACT_LAYOUT.md convention | ☐ |
| Output directory maps to `results/stage7_benchtop/test_data/phase_{X}/` | ☐ |
| A test-write to a dummy file has confirmed the path is writable | ☐ |

### 5.3 Sample Rate Confirmation

| Requirement | Check |
|-------------|-------|
| DAQ sample rate is set to 1 Hz (or higher; 1 Hz is minimum) | ☐ |
| A 60-second test recording has been reviewed to confirm all 10 columns are present and non-zero | ☐ |

**Section 5 sign-off:** All 10 columns confirmed in live view and saved CSV;
file naming and path confirmed; sample rate confirmed.

Signature: _____________________________  Date/Time: _____________________________

---

## 6. Overall Preflight Sign-Off

All five sections must be signed before the first heater power-on.

| Section | Description | Signed off? |
|---------|-------------|------------|
| 1 | Instrumentation availability | ☐ |
| 2 | Thermal interface material specification | ☐ |
| 3 | Ambient logging | ☐ |
| 4 | Fixture-loss calibration | ☐ |
| 5 | Data capture fields | ☐ |

**Cleared for Phase A:** ☐ Yes  ☐ No — reason: _____________________________

Cleared by: _____________________________  Date/Time: _____________________________

---

## 7. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial release |

**End of document.**
