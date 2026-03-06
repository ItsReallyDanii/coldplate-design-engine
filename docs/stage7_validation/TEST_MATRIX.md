# Stage 7 Test Matrix

**Document ID:** STAGE7-TM-001  
**Date:** 2026-03-06  
**Status:** PROPOSED — RECONCILED PER AUDIT MEMO STAGE7-AUD-001  
**Companion to:** BENCHTOP_VALIDATION_PLAN.md  

> **Reconciliation note (STAGE7-AUD-001, 2026-03-06):** Section 1 corrects the simulation
> domain (2 mm, not 5 mm).  Section 5.1 adds a non-physicality caveat to the 44.02 LPM
> flow-rate prediction.  Section 5.2 removes the Q acceptance band (not usable for
> pass/fail because the underlying prediction is non-physical).  Section 2.2 documents
> that nominal Q cannot be defined from Stage 4 output and must be set from a pre-test
> physics-based estimate.

---

## 1. Candidate Under Test

| Field | Value |
|-------|-------|
| Candidate ID | candidate_02_diamond_2d_s1045 |
| Geometry family | Diamond TPMS (2D-promoted) |
| Voxel size | 0.25 mm |
| Resolution | 20 × 20 × 20 |
| Fabrication domain target | 5.0 × 5.0 × 5.0 mm |
| Simulation domain (actual) | **2.0 × 2.0 × 2.0 mm** (domain_volume_mm3 = 8.0 in Stage 4/5 results — see BENCHTOP_VALIDATION_PLAN.md Section 3.1 note) |
| Porosity | 56.3% |
| Material | Aluminum 6061-T6 |
| Fabrication | L-PBF (SLM/DMLS) |

Backup: candidate_01_diamond_2d_s1127 (identical screening outcome, lower flow rate).

---

## 2. Test Conditions Summary

### 2.1 Constant Parameters (All Tests)

| Parameter | Value | Tolerance |
|-----------|-------|-----------|
| Coolant | Deionized water | — |
| Inlet temperature | 25 °C | ±1 °C |
| Outlet back-pressure | Atmospheric (~101,325 Pa) | — |
| Data sample rate | 1 Hz | — |
| Steady-state hold | 10 min recording after 5 min warmup | — |
| Steady-state criterion | < 0.5 °C/min drift for 5 consecutive min, evaluated on **T_heater** (slowest channel) | — |

### 2.2 Variable Parameters

| Parameter | Nominal | Sweep values |
|-----------|---------|-------------|
| Heater power (P_elec) | 25 W | 10, 25, 50 W |
| Flow rate (Q) | Set pump to achieve ΔP ≈ 1000 Pa; measure resulting Q | 3 rates: 0.5×, 1×, 1.5× nominal (where nominal is the measured flow at ΔP ≈ 1000 Pa) |

> **Flow-rate baseline note (audit finding W-2 / H-1):** "Nominal Q" cannot be defined
> from Stage 4 output (Q = 44.02 LPM is non-physical — see Section 5.1).  Nominal Q is
> defined operationally as the flow rate measured on the bench when the pump achieves
> ΔP ≈ 1000 Pa.  Sweep targets (0.5×, 1×, 1.5×) are relative to that measured baseline.
> Before testing, derive a physics-based flow-rate estimate (Hagen-Poiseuille or Ergun
> from CT channel geometry) to confirm pump and flow meter adequacy.

---

## 3. Test Matrix

### 3.1 Phase A — Pre-Test Characterization (No Flow)

| Test ID | Description | Measurement | Acceptance |
|---------|-------------|-------------|------------|
| A-01 | CT scan | Internal geometry, wall/channel dimensions | < 30% deviation from design |
| A-02 | Mass measurement | Dry mass (±0.01 g) | Cross-check porosity |
| A-03 | External dimensions | Caliper (±0.01 mm) | Match 5.0 mm ± tolerance |
| A-04 | Powder evacuation check | Mass before/after ultrasonic cleaning | < 0.5% mass change |
| A-05 | Leak test (hydrostatic) | Apply 2× operating ΔP, hold 5 min | No visible leak |

### 3.2 Phase B — Nominal Condition (Primary Data)

| Test ID | P_elec (W) | Flow target | Repeats | Purpose |
|---------|-----------|-------------|---------|---------|
| B-01 | 25 | ΔP ≈ 1000 Pa | 3 (min 3, prefer 5) | Primary R_th and ΔP measurement |
| B-02 | 25 | ΔP ≈ 1000 Pa | 2 | Same-day repeatability check |

**Data collected per run:** T_in, T_out, T_heater, T_top, P_in, P_out, Q, P_elec (all at 1 Hz for 10 min).

**Derived per run:** R_th, ΔP, R_hyd, energy balance η.

### 3.3 Phase C — Power Sweep (Trend Validation)

| Test ID | P_elec (W) | Flow target | Repeats | Purpose |
|---------|-----------|-------------|---------|---------|
| C-01 | 10 | ΔP ≈ 1000 Pa | 2 | Low-power R_th linearity check |
| C-02 | 50 | ΔP ≈ 1000 Pa | 2 | High-power R_th linearity check |

**Expected:** R_th should be approximately constant across power levels if the system is linear (single-phase, no boiling). Deviation indicates non-linearity or parasitic loss.

### 3.4 Phase D — Flow Sweep (Hydraulic Characterization)

| Test ID | P_elec (W) | Flow target | Repeats | Purpose |
|---------|-----------|-------------|---------|---------|
| D-01 | 25 | 0.5× nominal Q | 2 | Low-flow ΔP point |
| D-02 | 25 | 1.0× nominal Q | 2 | Reference (same as B-01) |
| D-03 | 25 | 1.5× nominal Q | 2 | High-flow ΔP point |

**Expected:** ΔP should scale approximately linearly with Q if flow is Darcy (low Re). Deviation indicates inertial effects or turbulence onset.

### 3.5 Phase E — Post-Test Characterization

| Test ID | Description | Measurement | Purpose |
|---------|-------------|-------------|---------|
| E-01 | Repeat leak test | Same as A-05 | Confirm no degradation |
| E-02 | Mass measurement | Dry mass after testing | Check for erosion/deposit |
| E-03 | CT scan (optional) | Internal geometry | Detect internal damage |

---

## 4. Total Test Count

| Phase | Tests | Repeats | Total runs |
|-------|-------|---------|------------|
| A (pre-test) | 5 | 1 each | 5 |
| B (nominal) | 2 | 3–5 + 2 | 5–7 |
| C (power sweep) | 2 | 2 each | 4 |
| D (flow sweep) | 3 | 2 each | 6 |
| E (post-test) | 3 | 1 each | 3 |
| **Total** | **15** | — | **23–25 runs** |

Estimated duration: 1–2 days of bench time (excluding setup and pre/post characterization).

---

## 5. Predicted Values and Acceptance Bands

### 5.1 Simulation Predictions (Stage 4/5)

| Quantity | Predicted | Source | Label |
|----------|----------|--------|-------|
| R_th | 11.27 K/W | Stage 5, **2 mm domain** | SIMULATED |
| ΔP | 1000 Pa | Stage 4, **2 mm domain** | SIMULATED |
| Q at ΔP = 1000 Pa | 44.02 LPM | Stage 4 Darcy solver — **non-physical; do not use for equipment sizing or pass/fail** | FLOW_SIMULATED |
| T_peak at 4 W heat input | 70.06 °C | Stage 5, 4 W actual heat input (not 25 W) | SIMULATED |

> **Q non-physicality (audit finding W-2 / H-1):** Stage 4 predicted Q = 44.02 LPM
> implies a mean fluid velocity of approximately 183 m/s through the 4 mm² domain
> cross-section.  This is an artifact of Darcy permeability k = 1e-6 m² assigned to
> fluid voxels in the solver, not a calibrated physical quantity.  Real flow rates
> through this geometry at 1000 Pa will be orders of magnitude lower.  The 44 LPM
> value is retained here for traceability only; it must not be used for instrument
> procurement or acceptance-band definition.

> **T_peak note:** The simulated peak temperature of 70.06 °C corresponds to
> Stage 5 heat input of 4 W (1 MW/m² × 4 mm²), not to 25 W bench power.  Under the
> power-independence assumption, T_peak at 25 W bench ≈ T_in + R_th × 25 W ≈
> 25 + 11.27 × 25 ≈ 307 °C, which would indicate boiling.  In practice R_th at
> 25 W will be substantially lower than 11.27 K/W due to convective enhancement at
> realistic flow rates.  This estimate is provided to flag the danger of combining
> the 2 mm domain R_th with a 25 W bench power without rescaling.  Do not present
> 70.06 °C as the expected T_peak at 25 W bench power.

### 5.2 Acceptance Bands

| Quantity | Lower bound | Upper bound | Ratio basis |
|----------|------------|------------|-------------|
| R_th (K/W) | 5.63 | 22.53 | 0.5× to 2.0× predicted (11.27 K/W from 2 mm domain — domain mismatch acknowledged) |
| ΔP (Pa) | 333 | 3000 | 0.33× to 3.0× predicted (1000 Pa from 2 mm domain — domain mismatch acknowledged) |
| Q (LPM) | — | — | **No acceptance band.** Stage 4 Q prediction is non-physical. Measure and report bench Q as MEASURED; do not compare to 44.02 LPM. |

### 5.3 Immediate-Fail Bounds

| Quantity | Fail threshold | Ratio |
|----------|---------------|-------|
| R_th | > 33.8 K/W | > 3.0× predicted |
| ΔP | > 5000 Pa | > 5.0× predicted |
| Leak | Any | Binary |

---

## 6. Data Recording Requirements

### 6.1 Per-Run Data File

Each test run produces one time-series CSV with columns:

```
timestamp_s, T_in_C, T_out_C, T_heater_C, T_top_C, P_in_Pa, P_out_Pa, Q_LPM, P_elec_W
```

Sample rate: 1 Hz. Duration: 15 min (5 min warmup + 10 min recording).

### 6.2 Per-Run Summary Record

| Field | Value |
|-------|-------|
| test_id | e.g., B-01-R1 |
| candidate_id | candidate_02_diamond_2d_s1045 |
| date | ISO 8601 |
| operator | Name |
| P_elec_W | Measured mean |
| T_in_C | Measured mean |
| T_out_C | Measured mean |
| T_heater_C | Measured mean |
| P_in_Pa | Measured mean |
| P_out_Pa | Measured mean |
| Q_LPM | Measured mean |
| R_th_KW | Derived |
| dP_Pa | Derived |
| R_hyd_Pasm3 | Derived |
| energy_balance | Derived |
| steady_state_met | Boolean |
| notes | Free text |

### 6.3 Campaign Summary

One summary file aggregating all runs: mean, std, CV for each derived quantity across repeats at each condition.

---

## 7. Error-Bar Reporting

All reported values must include:

1. **Mean** across repeats at each condition.
2. **Standard deviation** across repeats.
3. **Number of repeats** (n).
4. **95% confidence interval** (mean ± t × s / √n, where t is from Student's t-distribution for n−1 degrees of freedom).

For n = 3: t₀.₀₂₅,₂ = 4.30 (wide interval — upgrade to n = 5 if feasible).
For n = 5: t₀.₀₂₅,₄ = 2.78.

---

## 8. Test Sequencing

Recommended execution order:

1. **Phase A** — Pre-test characterization (CT, mass, dimensions, leak).
2. **Phase B** — Nominal condition repeats (most important data first).
3. **Phase C** — Power sweep (builds on nominal baseline).
4. **Phase D** — Flow sweep (separate variable from power).
5. **Phase E** — Post-test characterization (confirm specimen integrity).

If time is limited, prioritize **A → B → E**. Phases C and D are extended characterization.

---

## 9. Document Status

| Item | Status |
|------|--------|
| Test matrix definition | PROPOSED — this document |
| Pre-test characterization | NOT STARTED |
| Nominal testing | NOT STARTED |
| Extended testing | NOT STARTED |
| Post-test characterization | NOT STARTED |

---

**End of document.**
