# Stage 7 Benchtop Execution Checklist — First Physical Run

**Document ID:** STAGE7-EC-001  
**Date:** 2026-03-06  
**Status:** READY FOR USE  
**Candidate:** candidate_02_diamond_2d_s1045  
**Companion documents:** PREFLIGHT_VERIFICATION.md, RUN_SHEET_CANDIDATE_02.md,
ARTIFACT_CHECKLIST_PRE_TEST.md, POST_RUN_DATA_INGEST_CHECKLIST.md  

> **Scope:** This checklist covers the sequence of actions for the first physical
> benchtop run only (Phases A and B of the test matrix).  Phases C, D, E are
> addressed in RUN_SHEET_CANDIDATE_02.md.  Nothing in this document implies that
> prior simulations have been physically validated; the test has not yet occurred.

---

## 0. Pre-Day Prerequisites (Must Be Complete Before Arriving at Bench)

All items in ARTIFACT_CHECKLIST_PRE_TEST.md must be checked off.  
PREFLIGHT_VERIFICATION.md Section 1 (instrumentation availability) must be
complete.  
If any prerequisite is open, **do not proceed**.

---

## 1. Bench Setup (Day-Of, Before Power-On)

| # | Action | Accept criterion | Initials |
|---|--------|-----------------|---------|
| 1.1 | Confirm ambient temperature is in range 20–26 °C | Measured by T_amb sensor | |
| 1.2 | Mount specimen S7-C02-001 in fixture | Fixture fasteners torqued to spec; no visual gaps between heater block and specimen bottom face | |
| 1.3 | Apply thermal interface material between heater block and specimen bottom face | TIM type, batch number, and applied thickness recorded in run notes (see PREFLIGHT_VERIFICATION.md Section 2) | |
| 1.4 | Connect coolant inlet and outlet lines | No visible leaks at fittings; all clamps seated | |
| 1.5 | Attach thermocouples: T_in, T_out, T_heater, T_top, T_amb | All channels reading within 1 °C of ambient; no open-circuit indication | |
| 1.6 | Connect pressure transducers P_in and P_out | Both reading atmospheric (or expected offset); bleed air from lines | |
| 1.7 | Connect flow meter Q | Flow meter primed; reading zero with pump off | |
| 1.8 | Connect power meter to heater terminals | Reading zero watts with heater supply off | |
| 1.9 | Verify DAQ is sampling all 9 channels at 1 Hz | Live display shows plausible values on all channels | |
| 1.10 | Start T_amb logging; record baseline ambient reading | Record value in run sheet | |

---

## 2. Fixture-Loss Calibration Run (Phase A Prerequisite)

Perform **before** installing specimen.  See PREFLIGHT_VERIFICATION.md Section 3
for full protocol.

| # | Action | Accept criterion | Initials |
|---|--------|-----------------|---------|
| 2.1 | Install heater block in fixture with no specimen (or reference block per protocol) | — | |
| 2.2 | Set pump to target ΔP; record Q, T_in, T_out, T_heater at steady state for each heater power level (10, 25, 50 W) | Steady state: < 0.5 °C/min on T_heater for 5 consecutive min | |
| 2.3 | Record parasitic loss fraction = (P_elec − Q_fluid × ρ × cp × ΔT) / P_elec for each level | Log; used in uncertainty budget for Phase B | |
| 2.4 | Remove heater block; install specimen per Section 1 above | — | |

---

## 3. Phase A — Pre-Test Characterization

Reference TEST_MATRIX.md Section 3.1 for full acceptance criteria.

| Test ID | Action | Record | Accept | Initials |
|---------|--------|--------|--------|---------|
| A-01 | Confirm CT scan report is on file and deviation < 30% | ct_scan_id in run notes | < 30% dimensional deviation | |
| A-02 | Dry-mass measurement (±0.01 g) | mass_g in A-02_mass.json | Cross-check porosity within 5% of design 56.3% | |
| A-03 | External caliper measurement | dimensions in A-03_dimensions.json | Within fabrication tolerance of nominal 5.0 mm | |
| A-04 | Powder evacuation check | mass before/after in A-04_powder_evac.json | < 0.5% mass change after ultrasonic cleaning | |
| A-05 | Hydrostatic leak test at 2× operating ΔP, hold 5 min | pass/fail in A-05_leak_test.json | No visible leak | |

If A-05 fails: **stop.  Do not proceed to Phase B.**  Record failure and
escalate before re-attempt.

---

## 4. Instrument Calibration Check (Day-Of)

| # | Action | Accept criterion | Initials |
|---|--------|-----------------|---------|
| 4.1 | TC ice-point check: all TCs in ice bath | All readings 0.0 ± 0.5 °C | |
| 4.2 | TC boiling-point check (if oven available) | All readings within ±1 °C of local boiling point at ambient pressure | |
| 4.3 | Pressure transducer zero check (valves closed, atmospheric reference) | P_in = P_out = 0 Pa differential (or atmospheric absolute) ± 25 Pa | |
| 4.4 | Power meter zero check with heater disconnected | Reading 0.00 W ± 0.05 W | |
| 4.5 | Flow meter bucket check at one representative flow rate | Meter vs collected volume within ±3% | |

If any calibration check fails its criterion: **do not use that instrument
for primary data until recalibrated or replaced.**

---

## 5. Phase B — Nominal Condition (Primary Test)

Reference TEST_MATRIX.md Section 3.2 and RUN_SHEET_CANDIDATE_02.md for
detailed step-by-step procedure.

| Step | Action | Record | Initials |
|------|--------|--------|---------|
| 5.1 | Set coolant inlet temperature to 25 ± 1 °C; confirm T_in stable | T_in at steady state | |
| 5.2 | Set pump to achieve ΔP ≈ 1000 Pa; record measured Q | Q_nominal in run sheet | |
| 5.3 | Set heater power to 25 W; start DAQ recording | P_elec confirmed on power meter | |
| 5.4 | Wait for steady state: T_heater drift < 0.5 °C/min for 5 consecutive min | Record time-to-steady-state | |
| 5.5 | Record 10 min of steady-state data at 1 Hz | timeseries CSV saved | |
| 5.6 | Compute and record R_th = (T_heater − T_in) / P_elec and ΔP = P_in − P_out from run average | Derived values in run summary JSON | |
| 5.7 | Compare R_th against acceptance band: 5.63–22.53 K/W | Pass/fail recorded | |
| 5.8 | Compare ΔP against acceptance band: 333–3000 Pa | Pass/fail recorded | |
| 5.9 | Repeat steps 5.3–5.8 for repeats R2 and R3 (minimum) | Separate files per repeat | |
| 5.10 | Check run-to-run repeatability: R_th range ≤ 10% across repeats | Flag if exceeded | |

**Immediate-stop criteria (any trigger → power off, stop flow, document):**

- Visible leak from specimen, fittings, or fixture  
- T_heater > 95 °C (heater malfunction risk)  
- R_th > 3× simulation value (> 33.8 K/W)  
- ΔP > 5× simulation value (> 5000 Pa)  
- Energy balance η < 80% (severe instrumentation or loss problem)  

---

## 6. Wrap-Up

| # | Action | Initials |
|---|--------|---------|
| 6.1 | Power off heater; record time | |
| 6.2 | Allow coolant to flow until T_heater < T_in + 5 °C before stopping pump | |
| 6.3 | Stop pump; depressurize lines | |
| 6.4 | Remove specimen; inspect for visible damage, discoloration, or deformation | |
| 6.5 | Perform Phase E post-test leak test (E-01) and mass check (E-02) | |
| 6.6 | Transfer all data files to designated archive location per POST_RUN_DATA_INGEST_CHECKLIST.md | |
| 6.7 | Record ambient temperature at end of session | |
| 6.8 | Complete run sheet and countersign | |

---

## 7. Pass/Fail Summary

After Phase B (minimum 3 repeats of B-01):

| Metric | Predicted (sim) | Acceptance band | Measured (fill in) | Pass/Fail |
|--------|----------------|----------------|-------------------|---------|
| R_th (K/W) | 11.27 | 5.63 – 22.53 | | |
| ΔP (Pa) | 1000 | 333 – 3000 | | |

> **Domain-size caveat:** The simulation predictions above were computed on a
> 2.0 × 2.0 × 2.0 mm domain (8 mm³).  The fabricated specimen targets 5.0 mm.
> The acceptance bands are wide enough to accommodate this mismatch by design,
> but a corrected simulation on the 5 mm domain is recommended before declaring
> a quantitative model-to-bench comparison valid (see STAGE7-AUD-001, H-2).

---

## 8. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial release |

**End of document.**
