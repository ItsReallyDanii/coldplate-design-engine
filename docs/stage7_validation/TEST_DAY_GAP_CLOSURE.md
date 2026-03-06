# Stage 7 Test-Day Gap-Closure Memo

**Document ID:** STAGE7-GC-001  
**Date:** 2026-03-06  
**Status:** DRAFT — FOR REVIEW BEFORE TEST DAY  
**Candidate:** candidate_02_diamond_2d_s1045  
**Companion documents:** ARTIFACT_CHECKLIST_PRE_TEST.md, PREFLIGHT_VERIFICATION.md,
INSTRUMENTATION_AND_SENSORS.md, DATA_SCHEMA_STAGE7.md  

> **Scope:** This memo identifies which of the 24 outstanding items in
> ARTIFACT_CHECKLIST_PRE_TEST.md (as of 2026-03-06) block test execution, which
> can be deferred to test day, and which are optional.  No test results are
> presented; no simulation claims are modified.  Current status: **NO GO**.

---

## 1. Current Gate State

ARTIFACT_CHECKLIST_PRE_TEST.md Section 7 records **24 of 26 items open**
as of 2026-03-06.  The two closed items are:

| Item | Description | Status |
|------|-------------|--------|
| 1.3 | Stage 5 thermal_metrics.json for candidate_02 | EXISTS |
| 1.4 | Stage 6 structural_metrics.json for candidate_02 | EXISTS |
| 6.5 | Stage 7 planning docs at known git SHA | EXISTS — current HEAD |

The 24 remaining open items span five categories: simulation reference artifacts,
fabrication, instrumentation, TIM, test infrastructure, and documentation.

Test day is not cleared until all must-have items in Section 2 below are closed.

---

## 2. Must-Have Before Any Test

These items must be physically complete, verified, and recorded **before arriving
at the bench**.  A single open item in this list is a hard NO-GO.

### 2.1 Simulation Reference (ARTIFACT_CHECKLIST_PRE_TEST Section 1)

| Item | Artifact | Blocking reason |
|------|----------|----------------|
| 1.1 | `results/stage7_benchtop/simulation_reference/`<br>`simulation_reference_candidate_02.json` | Prediction values must be committed and immutable before test data exist.  Populating after testing introduces hindsight bias. |
| 1.2 | `results/stage7_benchtop/simulation_reference/`<br>`pipeline_git_sha.txt` | Required for Stage 8 provenance chain.  Must record the HEAD SHA at the time 1.1 is created, not at test time. |

**Correct field values for 1.1** (per DATA_SCHEMA_STAGE7.md v1.1.0 Section 6):

```
total_power_w               = 4.0          (NOT 25 W — Stage 5 actual heat input)
thermal_resistance_KW       = 11.265617018419787
peak_temperature_C          = 70.062
heat_flux_w_m2              = 1000000.0
simulation_domain_mm        = [2.0, 2.0, 2.0]  (NOT 5.0 mm — Stage 4/5 actual domain)
pressure_drop_Pa            = 1000.0
stage4.flow_rate_LPM        = 44.02  (NON-PHYSICAL — Darcy artifact; caveat required)
stage3_source               = candidate_02_diamond_2d_s1045
pipeline_git_sha            = <SHA at lock time>
```

Do not alter these fields after fabrication begins.

### 2.2 Geometry and Fabrication (ARTIFACT_CHECKLIST_PRE_TEST Section 2)

| Item | Artifact | Blocking reason |
|------|----------|----------------|
| 2.1 | STL export of candidate_02 at 0.25 mm voxel | Required input to AM vendor; must be verified watertight before sending. |
| 2.2 | AM build specification (material, laser params, orientation, support strategy) | Without this, no specimen can be ordered. |
| 2.3 | Fabrication vendor confirmed; order placed; 0.5 mm min-feature capability confirmed | Vendor must verify process capability before committing. |
| 2.4 | At least one specimen received and logged as S7-C02-001 | No specimen, no test. |
| 2.5 | Pre-test CT scan of S7-C02-001 completed; report as `ct_report_S7-C02-001.pdf` | Geometry fidelity gate: deviation must be < 30% from design before proceeding.  CT deviation > 50% is an immediate stop. |
| 2.6 | `ct_measurements_S7-C02-001.json` committed (channel diameters, wall thickness, effective porosity) | Required for back-simulation traceability (audit finding M-5) and for item 2.7. |
| 2.7 | Physics-based flow-rate estimate from CT channel geometry (Hagen-Poiseuille or Ergun) | **Critical path for instrument procurement** (audit finding H-1).  Flow meter and pump cannot be correctly sized until this estimate exists.  Do not size from Stage 4 Q = 44.02 LPM; that value is non-physical. |

### 2.3 Instrumentation (ARTIFACT_CHECKLIST_PRE_TEST Section 3)

All items are hard blockers; missing any instrument prevents data collection.

| Item | Instrument | Critical requirement |
|------|-----------|---------------------|
| 3.1 | Flow meter | Range sized from item 2.7, not from Stage 4 output.  Accuracy ≥ ±2% of reading at expected operating point. |
| 3.2 | Differential pressure transducer (0–5 kPa, ±25 Pa) | Required for ΔP measurement — the one Stage 4 output used for acceptance (ΔP = 1000 Pa). |
| 3.3 | 4× Type-T thermocouples: T_in, T_out, T_heater, T_top (30 AWG, ±0.5 °C) | R_th computation requires T_heater and T_in at minimum. |
| 3.4 | 1× ambient temperature sensor T_amb (TC or thermistor, free air, ±1 °C) | Required for parasitic-loss scaling and ambient drift flag (> 3 °C shift triggers run flag). |
| 3.5 | DC power meter 0–100 W, ±1% | Heat input denominator for R_th.  Must read at heater terminals. |
| 3.6 | DAQ with ≥ 9 analog input channels, ≥ 16-bit, 1 Hz minimum | 9 channels: T_in, T_out, T_heater, T_top, T_amb, P_in, P_out, Q, P_elec. |
| 3.7 | Current calibration records for all instruments (NIST-traceable or equivalent) | Ice-bath TC check, pressure zero-check, flow bucket test, power precision-load check (see INSTRUMENTATION_AND_SENSORS.md Section 4). |

### 2.4 Thermal Interface Material (ARTIFACT_CHECKLIST_PRE_TEST Section 4)

| Item | Artifact | Blocking reason |
|------|----------|----------------|
| 4.1 | TIM type and specification confirmed in writing (type, thermal conductivity, expected contact resistance at bond-line thickness) | Contact resistance adds directly to measured R_th.  For a 4 mm² heater at nominal power, even 0.5 K·cm²/W contact resistance contributes ~12.5 K/W — comparable to the simulation R_th of 11.27 K/W (audit finding W-4 / M-2).  Must be specified and reported so the bench comparison can account for it. |
| 4.2 | TIM on hand, sufficient quantity for initial application plus one rework | Cannot assemble fixture without TIM. |

### 2.5 Test Infrastructure (ARTIFACT_CHECKLIST_PRE_TEST Section 5)

| Item | Artifact | Blocking reason |
|------|----------|----------------|
| 5.1 | Coolant circulation loop with chiller, 25 ± 1 °C, DI water | No cooling, no test. |
| 5.2 | Pump sized from item 2.7 flow estimate; variable-speed or adjustable-bypass preferred | Pump must deliver the bench operating ΔP without destructive overpressure. |
| 5.3 | Fixture to constrain specimen against heater block, TC mounts | Specimen must be rigidly located and repeatable between runs. |
| 5.4 | GFCI outlet on heater power circuit | **Safety — mandatory before any heater energization.** |
| 5.5 | E-stop and over-temperature shutoff wired and tested (T_cutoff = 100 °C) | **Safety — mandatory before any heater energization.** |
| 5.6 | Drip tray under test section (≥ 2 L capacity) | Safety — contains spills from pressurized DI water loop. |
| 5.7 | DAQ software installed, verified logging all 10 timeseries columns at 1 Hz, output path confirmed writable | Cannot capture data without confirmed DAQ configuration. |

### 2.6 Documentation Artifacts (ARTIFACT_CHECKLIST_PRE_TEST Section 6 — pre-test subset)

| Item | Artifact | Blocking reason |
|------|----------|----------------|
| 6.1 | `results/stage7_benchtop/fabrication/build_log.md` created and populated | AM build parameters and material batch must be in provenance before test. |
| 6.2 | `results/stage7_benchtop/README.md` with campaign summary stub (candidate ID, specimen IDs, target test date) | Organizational traceability; required to associate test artifacts with specimen and candidate. |

---

## 3. Can Be Completed or Recorded on Test Day

These items are either operationally completed on test day (before first heater
energization) or are records captured during the session.  They are not
pre-procured artifacts and require no lead time beyond test-morning setup.

| Item | Action | When |
|------|--------|------|
| 6.3 | Print or load RUN_SHEET_CANDIDATE_02.md for operator reference; review with operator | Morning before first run |
| 6.4 | Complete and countersign PREFLIGHT_VERIFICATION.md (all 5 sections) | Day-before or morning-of, before first heater energization |
| PREFLIGHT Section 4 | Execute fixture-loss calibration (heater-only, no specimen); record η_fixture at 10, 25, 50 W in `calibration/fixture_loss_cal.json`; η_fixture ≥ 80% at all levels required to proceed to Phase A | Morning of test, before specimen installation |
| Run sheet fields | Record T_amb at session start and end; record TIM batch, applied thickness, clamp torque | During session |
| PREFLIGHT Section 1 spot checks | Ice-bath TC check, pressure zero-check, flow bucket test, power meter zero | Morning before first run |

> **Note:** Fixture-loss calibration (PREFLIGHT Section 4) is executed on test day
> but produces a required artifact (`calibration/fixture_loss_cal.json`).
> If η_fixture < 80%, **do not proceed to Phase A**.  This is a same-day blocker,
> not a pre-test blocker, but failure here halts the session.

---

## 4. Optional but Valuable

These items are not required for Stage 7 pass/fail determination.  They improve
diagnostic resolution and reduce ambiguity in case of a result outside the
acceptance band.

| Item | Value | Priority |
|------|-------|----------|
| Second specimen S7-C02-002 | Covers rework risk if S7-C02-001 is damaged or yields anomalous results; enables repeat run with known-identical geometry | Medium |
| Back-simulation on as-built CT geometry (audit finding M-5) | Separates fabrication deviation from model error if the test result falls outside acceptance band.  Without it, a "fail" is ambiguous. | Medium — recommended if CT deviation > 10% from design |
| Higher-resolution simulation on 5 mm domain (audit finding H-2 / M-6) | All current predictions (R_th = 11.27 K/W, ΔP = 1000 Pa) are on a 2 mm domain; the fabricated specimen targets 5 mm.  A 50³ or 100³ run on the 5 mm domain would reduce comparison uncertainty. | High — recommended before committing to fabrication if schedule permits |
| IR camera for surface temperature mapping | Diagnoses heater uniformity and hotspots; not required for R_th computation | Low |
| Additional thermocouples (2–4) across heater face | Temperature profile; diagnoses contact resistance non-uniformity | Medium |
| Post-test CT scan | Detects internal damage (cracking, channel collapse) after thermal cycling | Medium |
| Reynolds number estimate from measured Q and CT channel diameter (audit finding M-8) | Confirms Darcy regime assumption; flags if inertial effects are significant | Low — compute from bench Q after test |

---

## 5. Strict Go/No-Go Checklist

Complete this checklist immediately before the first heater energization.
All six blocks must be GO to proceed.  One NO in any block halts the session.

### 5.1 Instrumentation Present

| # | Check | GO criterion | GO / NO |
|---|-------|-------------|---------|
| I-1 | Flow meter physically present, powered, reading | Meter energized; reading zero or atmospheric flow with pump off | ☐ |
| I-2 | Flow meter range covers physics-based estimate (item 2.7) | Meter lower range ≤ 50% of estimated operating flow; upper range ≥ 2× estimated flow | ☐ |
| I-3 | Differential pressure transducer (P_in, P_out) present | Both transducers energized; reading atmospheric or expected offset | ☐ |
| I-4 | 4× Type-T thermocouples (T_in, T_out, T_heater, T_top) installed | All reading within ±1 °C of ambient; no open-circuit indication | ☐ |
| I-5 | Ambient temperature sensor (T_amb) installed in free air | Reading plausible ambient; not in flow path or heater exhaust | ☐ |
| I-6 | DC power meter connected at heater terminals | Reading 0.0 ± 0.05 W with heater supply off | ☐ |
| I-7 | DAQ energized, all 9 input channels active at ≥ 1 Hz | Live display shows non-zero, plausible values on all 9 channels | ☐ |
| I-8 | Calibration records current for all instruments | Calibration date within required interval per INSTRUMENTATION_AND_SENSORS.md Section 4 | ☐ |
| I-9 | Day-of spot checks passed (TC ice-bath 0 ± 0.5 °C; pressure zero ± 25 Pa; power zero ± 0.05 W; flow bucket ± 3%) | All four spot checks within acceptance | ☐ |

**Block I verdict:** ☐ GO  ☐ NO-GO

---

### 5.2 TIM Specified

| # | Check | GO criterion | GO / NO |
|---|-------|-------------|---------|
| T-1 | TIM type recorded in PREFLIGHT_VERIFICATION.md Section 2 and run sheet | Field is not blank; type name and manufacturer specified | ☐ |
| T-2 | TIM thermal conductivity recorded | Value in W/m·K on file; source is manufacturer datasheet | ☐ |
| T-3 | TIM contact resistance estimate at applied bond-line thickness recorded | Value in K·cm²/W on file; to be included in uncertainty budget | ☐ |
| T-4 | TIM on hand and applied per PREFLIGHT_VERIFICATION.md Section 2 procedure | Heater face and specimen bottom cleaned with IPA; TIM applied; clamp torque to spec | ☐ |

**Block T verdict:** ☐ GO  ☐ NO-GO

---

### 5.3 Ambient Logging Ready

| # | Check | GO criterion | GO / NO |
|---|-------|-------------|---------|
| A-1 | T_amb sensor installed in free air, away from heater exhaust and coolant lines | Sensor location confirmed; reading plausible ambient | ☐ |
| A-2 | T_amb channel included in DAQ recording | `T_amb_C` column present in live DAQ display | ☐ |
| A-3 | T_amb appears in saved CSV output (test write confirmed) | Dummy 60-second recording reviewed; `T_amb_C` column present and non-zero | ☐ |
| A-4 | Starting ambient temperature is in accepted range (20–26 °C) | T_amb reading at session start within 20–26 °C; if out of range, record and note as limitation | ☐ |
| A-5 | Procedure for ambient drift flag confirmed with operator | Operator understands: if T_amb shifts > 3 °C during a single run, flag that run in its summary JSON | ☐ |

**Block A verdict:** ☐ GO  ☐ NO-GO

---

### 5.4 Fixture-Loss Calibration Ready

> This block is evaluated after the fixture-loss calibration run (PREFLIGHT
> Section 4, executed morning-of before specimen installation).

| # | Check | GO criterion | GO / NO |
|---|-------|-------------|---------|
| F-1 | Fixture-loss calibration run completed (heater-only, no specimen) | Three power levels (10, 25, 50 W) each reaching steady state | ☐ |
| F-2 | η_fixture ≥ 80% at 10 W | η_fixture_10 = _____ % | ☐ |
| F-3 | η_fixture ≥ 80% at 25 W | η_fixture_25 = _____ % | ☐ |
| F-4 | η_fixture ≥ 80% at 50 W | η_fixture_50 = _____ % | ☐ |
| F-5 | Results recorded in `calibration/fixture_loss_cal.json` | File exists and is committed or staged | ☐ |

**Block F verdict:** ☐ GO  ☐ NO-GO  
(If any η_fixture < 80%, fix fixture and re-run calibration before installing specimen.)

---

### 5.5 Candidate Specimen Available

| # | Check | GO criterion | GO / NO |
|---|-------|-------------|---------|
| S-1 | Specimen S7-C02-001 physically present and labeled | Specimen in hand; ID label affixed and matches fabrication log | ☐ |
| S-2 | Pre-test CT scan report committed (`ct_report_S7-C02-001.pdf`) | File committed; scan date and specimen ID in report header | ☐ |
| S-3 | CT geometry deviation < 30% from design | Maximum deviation field in ct_measurements_S7-C02-001.json ≤ 30% | ☐ |
| S-4 | CT geometry deviation < 50% (immediate-stop threshold) | Maximum deviation field < 50%; if ≥ 50%, stop and do not test | ☐ |
| S-5 | Powder evacuation confirmed (residual < 0.5% by mass) | `powder_evacuation.pass` = true in `pretest_S7-C02-001.json` | ☐ |
| S-6 | Leak test passed (no leak detected at specified hold pressure) | `leak_test.leak_detected` = false in `pretest_S7-C02-001.json` | ☐ |
| S-7 | Physics-based flow-rate estimate (item 2.7) available and used to size flow meter and pump | Estimate document or calculation on file; instrument ranges confirmed adequate | ☐ |

**Block S verdict:** ☐ GO  ☐ NO-GO

---

### 5.6 Data Capture Schema Ready

| # | Check | GO criterion | GO / NO |
|---|-------|-------------|---------|
| D-1 | DAQ configured with correct column names per DATA_SCHEMA_STAGE7.md v1.1.0 Section 2.2 | All 10 columns present: `timestamp_s`, `T_in_C`, `T_out_C`, `T_heater_C`, `T_top_C`, `T_amb_C`, `P_in_Pa`, `P_out_Pa`, `Q_LPM`, `P_elec_W` | ☐ |
| D-2 | File naming configured as `{test_id}_timeseries.csv` | DAQ save-file template verified against ARTIFACT_LAYOUT.md convention | ☐ |
| D-3 | Output directory is `results/stage7_benchtop/test_data/phase_{X}/` | Directory exists and is writable; confirmed by test-write | ☐ |
| D-4 | Sample rate confirmed at ≥ 1 Hz | DAQ sample-rate setting verified; 60-second test recording reviewed | ☐ |
| D-5 | Simulation reference JSON (item 1.1) committed before any test data are written | `simulation_reference_candidate_02.json` at locked git SHA; field values match ARTIFACT_CHECKLIST_PRE_TEST Section 1 | ☐ |
| D-6 | Run summary JSON template loaded and operator briefed on required fields | operator understands measured_means, derived, quality, and provenance fields per DATA_SCHEMA_STAGE7.md Section 3.2 | ☐ |

**Block D verdict:** ☐ GO  ☐ NO-GO

---

### 5.7 Overall Go/No-Go

| Block | Description | Verdict |
|-------|-------------|---------|
| I | Instrumentation present | ☐ GO / ☐ NO-GO |
| T | TIM specified | ☐ GO / ☐ NO-GO |
| A | Ambient logging ready | ☐ GO / ☐ NO-GO |
| F | Fixture-loss calibration ready | ☐ GO / ☐ NO-GO |
| S | Candidate specimen available | ☐ GO / ☐ NO-GO |
| D | Data capture schema ready | ☐ GO / ☐ NO-GO |

**Cleared for Phase A heater energization:** ☐ YES — all six blocks GO  ☐ NO — specify block(s): _____________________________

Cleared by: _____________________________  Date/Time: _____________________________

---

## 6. Outstanding Warnings Inherited from Audit Memo (STAGE7-AUD-001)

These are known discrepancies between the simulation predictions and the fabrication
target.  They do not block testing but must be acknowledged in every run summary.

| ID | Issue | Implication for test comparison |
|----|-------|--------------------------------|
| H-1 | Stage 4 Q = 44.02 LPM is non-physical (Darcy solver artifact; implies ~183 m/s mean velocity).  Do not use for instrument sizing. | Real bench Q will likely be mL/min range, not LPM.  Flow meter must be sized from item 2.7 physics-based estimate.  Stage 4 Q acceptance band is void. |
| H-2 | All Stage 4/5 predictions were computed on a 2 mm domain; the fabricated specimen targets 5 mm.  The acceptance bands (R_th within 2×, ΔP within 3×) are wide enough to accommodate some scaling error, but this is not by design. | If result falls outside acceptance band, domain mismatch is a confound.  Recommend rerunning Stage 4/5 on 5 mm domain before fabrication if schedule allows. |
| W-1 | Stage 5 actual heat input is 4.0 W (1 MW/m² × 4 mm²), not 25 W.  R_th is power-independent only if single-phase, linear conduction holds at all bench power levels. | simulation_reference_candidate_02.json must record total_power_w = 4.0.  Bench comparison is to the R_th value, not to the power level.  Power-independence assumption should be verified across the 10–50 W sweep. |
| W-4 | Contact resistance (heater-to-specimen interface) is not modeled in Stage 5.  At 4 mm² heated area, 0.5 K·cm²/W adds ~12.5 K/W to measured R_th. | Measured R_th will exceed simulation R_th by at least the TIM contact resistance contribution.  Report TIM contact resistance separately in every run summary; subtract from measured R_th before applying the 2× acceptance band. |
| W-3 | Simulation domain (2 mm) ≠ fabrication domain (5 mm).  All Stage 4/5 quantitative predictions apply to the 2 mm geometry. | Document this mismatch in every run summary.  It does not invalidate the test but must be carried as a known limitation in Stage 8. |

---

## 7. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial release |

**End of document.**
