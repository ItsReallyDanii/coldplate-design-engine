# Run Sheet — candidate_02_diamond_2d_s1045 — Stage 7 Benchtop

**Document ID:** STAGE7-RS-C02-001  
**Date:** 2026-03-06  
**Status:** READY FOR USE — test has not yet been performed  
**Candidate:** candidate_02_diamond_2d_s1045  
**Specimen ID:** S7-C02-001 (primary), S7-C02-002 (backup if needed)  
**Operator:** ___________________________  
**Date of run:** ___________________________  
**Bench location:** ___________________________  

---

## 1. Candidate Summary

| Parameter | Value | Source |
|-----------|-------|--------|
| Candidate ID | candidate_02_diamond_2d_s1045 | Stage 2 inverse design |
| Geometry family | Diamond TPMS, 2D-promoted | Stage 3 |
| Voxel size | 0.25 mm | Stage 3 config (VOXEL_SIZE_MM = 0.25) |
| Simulation domain | 2.0 × 2.0 × 2.0 mm (8 mm³) | Stage 4/5 actual results |
| Fabrication domain target | 5.0 × 5.0 × 5.0 mm | Stage 3 config (SMOKE_RESOLUTION = 20) |
| Porosity | 56.34% | Stage 5 thermal_metrics.json |
| Min feature size (design) | 0.5 mm | Stage 6 structural_metrics.json |
| Material | Aluminum 6061-T6 | Stage 6 material_properties |
| Stage 6 verdict | PASS (structural + manufacturability) | Stage 6 structural_metrics.json |

**Simulation reference values** (from Stage 4/5 smoke-mode runs; domain =
2 mm, not fabrication-target 5 mm — see domain-size caveat below):

| Quantity | Value | Computed at |
|----------|-------|------------|
| Thermal resistance R_th | 11.27 K/W | Q_total = 4.0 W (1 MW/m² × 4 mm²); T_in = 25 °C |
| Pressure drop ΔP | 1000 Pa | Boundary condition (inlet); not a predicted output |
| Flow rate Q | 44.02 LPM (NON-PHYSICAL — do not use) | Stage 4 Darcy solver artifact; k_fluid = 1e-6 m² |

> **Domain-size caveat:** All simulation predictions above were computed on a
> 2.0 mm domain.  The fabricated specimen is 5.0 mm.  Scaling is non-linear.
> Accept/reject is based on directional agreement within the bands below, not
> exact quantitative match.

---

## 2. Acceptance Bands

| Metric | Simulated reference | Pass band (directional) | Fail threshold (immediate stop) |
|--------|-------------------|------------------------|--------------------------------|
| R_th (K/W) | 11.27 | 5.63 – 22.53 (0.5× – 2.0×) | > 33.80 (3×) |
| ΔP (Pa) | 1000 | 333 – 3000 (0.33× – 3.0×) | > 5000 (5×) |
| Energy balance η | — | > 90% (secondary integrity check) | < 80% (instrumentation problem) |

> **Q acceptance band:** Not defined.  Stage 4 Q = 44 LPM is non-physical and
> must not be used as a comparison reference.  Record measured Q; do not apply
> a pass/fail band to it.

---

## 3. Test Conditions

| Parameter | Value | Tolerance |
|-----------|-------|-----------|
| Coolant | Deionized water | — |
| Inlet temperature T_in | 25 °C | ±1 °C |
| Heater power P_elec (nominal) | 25 W | ±0.25 W |
| Target ΔP at inlet | 1000 Pa | Set operationally; record actual |
| Steady-state criterion | < 0.5 °C/min drift on T_heater for 5 consecutive min | — |
| Data sample rate | 1 Hz | — |
| Steady-state recording window | 10 min after steady-state criterion is met | — |
| Ambient temperature | 20–26 °C | Log continuously; do not control |

---

## 4. Phase A — Pre-Test Characterization

Record results in the named files.  Stop if A-05 fails.

| Test ID | Description | Measurement | Accept | File | Result | Initials |
|---------|-------------|-------------|--------|------|--------|---------|
| A-01 | CT scan review | Confirm ct_report on file; extract max dimensional deviation | < 30% | ct_measurements_S7-C02-001.json | | |
| A-02 | Dry mass | Weigh to ±0.01 g | Porosity cross-check ≤ 5% error | A-02_mass.json | | |
| A-03 | External dimensions | Caliper, ±0.01 mm, all 3 axes | ≤ fab tolerance vs 5.0 mm | A-03_dimensions.json | | |
| A-04 | Powder evacuation | Mass before/after ultrasonic clean | < 0.5% mass change | A-04_powder_evac.json | | |
| A-05 | Hydrostatic leak test | 2× operating ΔP, 5 min hold | No leak | A-05_leak_test.json | | |

**CT decision tree (from STAGE7-AUD-001, M-10):**

| CT deviation (max) | Action |
|--------------------|--------|
| < 30% | Proceed normally |
| 30% – 50% | Note deviation in all run summaries; plan as-built geometry back-simulation before final verdict |
| > 50% | Stop; do not proceed to Phase B; escalate |

---

## 5. Fixture-Loss Calibration (Before Phase B)

| Step | Action | Record | Initials |
|------|--------|--------|---------|
| FC-1 | Install heater block without specimen | — | |
| FC-2 | Set coolant flow; set heater to 10 W; wait for steady state | T_in, T_out, T_heater, Q, P_elec at steady state | |
| FC-3 | Record η_10 = Q_fluid / P_elec | η_10 = _____  % | |
| FC-4 | Repeat at 25 W | η_25 = _____  % | |
| FC-5 | Repeat at 50 W | η_50 = _____  % | |
| FC-6 | Install specimen; proceed to Phase B | — | |

Fixture loss η is used in Phase B energy balance check.  η < 80% at any
power level indicates a fixturing or insulation problem — investigate before
proceeding.

---

## 6. Phase B — Nominal Condition (Primary Data)

Minimum 3 repeats of B-01 required.  Perform B-02 (same-day repeatability)
if time allows.

### 6.1 Repeat B-01-R1

| Step | Action | Record | Initials |
|------|--------|--------|---------|
| B1.1 | Confirm T_in = 25 ± 1 °C | T_in = _____ °C | |
| B1.2 | Set pump; adjust until P_in − P_out ≈ 1000 Pa | ΔP_set = _____ Pa; Q_measured = _____ LPM | |
| B1.3 | Set heater to 25 W; confirm P_elec on power meter | P_elec = _____ W | |
| B1.4 | Start DAQ; record start time | t_start = _____ | |
| B1.5 | Monitor T_heater; note time when drift < 0.5 °C/min | t_steady = _____ | |
| B1.6 | Hold steady state for 5 min; then record 10 min window | t_record_start = _____; t_record_end = _____ | |
| B1.7 | Note T_amb at end of run | T_amb = _____ °C | |
| B1.8 | Derive R_th = (T_heater_avg − T_in_avg) / P_elec | R_th = _____ K/W | |
| B1.9 | Derive ΔP = P_in_avg − P_out_avg | ΔP = _____ Pa | |
| B1.10 | Derive η = (Q × ρ × cp × (T_out − T_in)) / P_elec | η = _____ % | |
| B1.11 | Compare R_th to band 5.63–22.53 K/W | Pass / Fail | |
| B1.12 | Compare ΔP to band 333–3000 Pa | Pass / Fail | |
| B1.13 | Save `B-01-R1_timeseries.csv` and `B-01-R1_summary.json` | Confirmed | |

Immediate stop triggers: T_heater > 95 °C; R_th > 33.8 K/W; ΔP > 5000 Pa;
visible leak; η < 80%.

### 6.2 Repeat B-01-R2

Same procedure as 6.1.  Record in `B-01-R2_timeseries.csv` /
`B-01-R2_summary.json`.

| Derived quantity | Value | Pass/Fail |
|-----------------|-------|---------|
| R_th (K/W) | | |
| ΔP (Pa) | | |
| η (%) | | |

### 6.3 Repeat B-01-R3

Same procedure as 6.1.  Record in `B-01-R3_timeseries.csv` /
`B-01-R3_summary.json`.

| Derived quantity | Value | Pass/Fail |
|-----------------|-------|---------|
| R_th (K/W) | | |
| ΔP (Pa) | | |
| η (%) | | |

### 6.4 B-01 Repeatability Check

| Metric | R1 | R2 | R3 | Range / Mean | < 10%? |
|--------|----|----|----|----|--------|
| R_th (K/W) | | | | | |
| ΔP (Pa) | | | | | |

If R_th range / mean > 10%: note in campaign summary; investigate before
proceeding to Phase C.

---

## 7. Phase C — Power Sweep (Optional, Same Session)

Perform only after B-01 repeats are complete and all immediate-stop
criteria are clear.

| Test ID | P_elec (W) | Flow target | Record | Initials |
|---------|-----------|------------|--------|---------|
| C-01-R1 | 10 | ΔP ≈ 1000 Pa | `C-01-R1_timeseries.csv`, `C-01-R1_summary.json` | |
| C-01-R2 | 10 | ΔP ≈ 1000 Pa | `C-01-R2_timeseries.csv`, `C-01-R2_summary.json` | |
| C-02-R1 | 50 | ΔP ≈ 1000 Pa | `C-02-R1_timeseries.csv`, `C-02-R1_summary.json` | |
| C-02-R2 | 50 | ΔP ≈ 1000 Pa | `C-02-R2_timeseries.csv`, `C-02-R2_summary.json` | |

**Caution at 50 W:** Monitor T_heater continuously.  Abort if T_heater
approaches 90 °C.  Do not attempt 50 W if specimen shows any sign of
leak or thermal runaway during Phase B.

**R_th power-independence check:** R_th should be approximately constant
across 10, 25, 50 W if the system is single-phase and linear.  Deviation
> 20% across power levels indicates contact resistance non-linearity,
boiling onset, or parasitic loss change — record and flag for analysis.

---

## 8. Phase D — Flow Sweep (Optional, Separate Session)

To be scheduled separately if Phase B and C are successful.

| Test ID | P_elec (W) | Flow target | Record |
|---------|-----------|------------|--------|
| D-01-R1 | 25 | 0.5× Q_nominal | `D-01-R1_timeseries.csv`, `D-01-R1_summary.json` |
| D-01-R2 | 25 | 0.5× Q_nominal | `D-01-R2_timeseries.csv`, `D-01-R2_summary.json` |
| D-02-R1 | 25 | 1.0× Q_nominal | `D-02-R1_timeseries.csv`, `D-02-R1_summary.json` |
| D-02-R2 | 25 | 1.0× Q_nominal | `D-02-R2_timeseries.csv`, `D-02-R2_summary.json` |
| D-03-R1 | 25 | 1.5× Q_nominal | `D-03-R1_timeseries.csv`, `D-03-R1_summary.json` |
| D-03-R2 | 25 | 1.5× Q_nominal | `D-03-R2_timeseries.csv`, `D-03-R2_summary.json` |

> Q_nominal = flow rate measured during B-01 at ΔP ≈ 1000 Pa.

**Unreachable ΔP fallback (from STAGE7-AUD-001, M-9):** If the pump cannot
reach ΔP = 1000 Pa within the flow meter's accuracy range, record the
maximum achievable ΔP and corresponding Q; annotate run as
"ΔP_target_not_reached"; do not extrapolate.

---

## 9. Phase E — Post-Test Characterization

| Test ID | Description | Record | Accept | Initials |
|---------|-------------|--------|--------|---------|
| E-01 | Leak test (repeat A-05 conditions) | E-01_leak_test.json | No new leak indication | |
| E-02 | Post-test mass measurement | E-02_mass.json | Compare to A-02 mass; note any change | |
| E-03 | Post-test CT scan (optional) | E-03_ct_scan.json | Visual inspection for deformation or channel collapse | |

---

## 10. End-of-Session Record

| Field | Value |
|-------|-------|
| Test date | |
| Operator | |
| Specimen ID | |
| Ambient temperature at start (°C) | |
| Ambient temperature at end (°C) | |
| TIM type and lot | |
| Fixture-loss η at 25 W (%) | |
| B-01 repeats completed | |
| B-01 R_th mean (K/W) | |
| B-01 ΔP mean (Pa) | |
| B-01 overall verdict | PASS / FAIL / INCONCLUSIVE |
| Phase C completed? | Yes / No |
| Any immediate-stop triggered? | Yes / No — describe if yes |
| Data files transferred to archive? | Yes / No |
| Notes | |

Countersigned by: _____________________________  Date: _____________

---

## 11. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial release |

**End of document.**
