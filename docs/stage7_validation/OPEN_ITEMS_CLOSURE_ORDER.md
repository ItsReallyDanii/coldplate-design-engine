# Stage 7 Open Items — Closure Order

**Document ID:** STAGE7-OI-001  
**Date:** 2026-03-06  
**Status:** FINAL  
**Scope:** Shortest-path closure plan for the 29 items remaining open in
ARTIFACT_CHECKLIST_PRE_TEST.md as of 2026-03-06 (27 hard pre-test blockers +
2 same-day tasks; the source checklist header states "24 of 26" but an actual
enumeration of its rows yields 29 open items across sections 1–6).  
**Companion documents:** ARTIFACT_CHECKLIST_PRE_TEST.md (STAGE7-AC-001),
TEST_DAY_GAP_CLOSURE.md (STAGE7-GC-001), STAGE7_VALIDATION_AUDIT_MEMO.md
(STAGE7-AUD-001), DATA_SCHEMA_STAGE7.md, PREFLIGHT_VERIFICATION.md  
**Candidate:** candidate_02_diamond_2d_s1045  

> **Scope discipline:** This document lists open items, assigns categories, and
> orders closure by dependency and lead time.  No code changes, no new physics
> claims, no simulation results are introduced here.

---

## 1. Category Key

| Tag | Meaning |
|-----|---------|
| **PROC** | Procurement — purchase or commission from an external supplier; requires quotation, lead time, and delivery |
| **FAB** | Fabrication — physical manufacturing of a part or assembly; may be internal or contracted; lead time dominates the critical path |
| **SETUP** | Setup — installation, wiring, software configuration, calibration, or bench assembly using already-procured equipment |
| **DOC** | Documentation — creating or populating a file, record, or calculation; no external dependency; executable by one person with existing data |

---

## 2. Complete Open-Item Register

All 29 items from ARTIFACT_CHECKLIST_PRE_TEST.md that are currently NOT CREATED
or NOT STARTED.  Two items (1.3 and 1.4) and one item (6.5) are already closed
and excluded.  Twenty-seven items are classified as hard pre-test blockers and
listed in this register; two items (6.3 and 6.4) are same-day tasks and are
addressed in Section 4 of this document.

| ID | Checklist Ref | Description | Category | Blocking role |
|----|--------------|-------------|----------|--------------|
| OI-01 | AC §1.1 | Create `results/stage7_benchtop/simulation_reference/simulation_reference_candidate_02.json` with correct schema v1.1.0 field values (total_power_w = 4.0, simulation_domain_mm = [2.0, 2.0, 2.0], heat_flux_w_m2 = 1 000 000, thermal_resistance_KW = 11.2656, peak_temperature_C = 70.062, pressure_drop_Pa = 1000, stage4 flow caveat noted) | DOC | Hard pre-test blocker; must be committed and immutable before any test data are written |
| OI-02 | AC §1.2 | Create `results/stage7_benchtop/simulation_reference/pipeline_git_sha.txt`; record the HEAD SHA at the moment OI-01 is committed | DOC | Hard pre-test blocker; required for Stage 8 provenance chain |
| OI-03 | AC §2.1 | Export STL from Stage 3 `results/.../volume.npy` at 0.25 mm voxel; verify watertight using mesh-repair tooling before transmitting to AM vendor | DOC | Blocks OI-05 (vendor order) |
| OI-04 | AC §2.2 | Write AM build specification: material (Al 6061-T6 or equivalent), laser parameters (to be filled by vendor), build orientation, support strategy, post-processing steps (support removal, T6 stress relief, bead blast), powder evacuation requirement | DOC | Blocks OI-05 (vendor order) |
| OI-05 | AC §2.3 | Confirm AM vendor; verify vendor process capability ≤ 0.5 mm minimum feature in Al alloy; place order for two specimens (S7-C02-001 and S7-C02-002) | PROC | Critical-path blocker; longest single lead time in the plan (typically 2–6 weeks for metal L-PBF); blocks OI-06, OI-07, OI-08, OI-09 |
| OI-06 | AC §2.4 | Receive specimen S7-C02-001 from vendor; assign specimen ID; log receipt in build log | FAB | Hard pre-test blocker; blocks OI-07, OI-08, OI-09, OI-10 |
| OI-07 | AC §2.5 | Perform pre-test micro-CT scan of S7-C02-001 at ≤ 50 µm resolution; commit `ct_report_S7-C02-001.pdf`; confirm deviation < 30% from design | SETUP | Hard pre-test blocker; blocks OI-08, OI-09; CT deviation ≥ 50% is an immediate stop |
| OI-08 | AC §2.6 | Reduce CT scan to `ct_measurements_S7-C02-001.json`; record channel diameters, wall thicknesses, and effective porosity from scan | DOC | Blocks OI-09 (flow estimate); required for back-simulation traceability (STAGE7-AUD-001 M-5) |
| OI-09 | AC §2.7 | Compute physics-based flow-rate estimate using CT-measured channel diameter and Hagen-Poiseuille or Ergun equation; bound realistic operating flow range (likely mL/min, not LPM) | DOC | Blocks OI-10 (flow meter procurement) and OI-14 (pump sizing); do not use Stage 4 Q = 44.02 LPM (STAGE7-AUD-001 H-1) |
| OI-10 | AC §3.1 | Procure flow meter; range must be sized from OI-09 estimate (lower bound ≤ 50% of estimated flow, upper bound ≥ 2×); accuracy ≥ ±2% of reading at the expected operating point | PROC | Hard pre-test blocker; cannot finalize until OI-09 is complete |
| OI-11 | AC §3.2 | Procure differential pressure transducer: 0–5 kPa range, ±25 Pa accuracy, DI-water-compatible wetted materials | PROC | Hard pre-test blocker; independent of fabrication critical path |
| OI-12 | AC §3.3 | Procure 4× Type-T thermocouples for T_in, T_out, T_heater, T_top; 30 AWG, ±0.5 °C accuracy | PROC | Hard pre-test blocker; independent of fabrication critical path |
| OI-13 | AC §3.4 | Procure 1× ambient temperature sensor (TC or thermistor) for T_amb; free-air installation, ±1 °C; adds column `T_amb_C` per DATA_SCHEMA_STAGE7.md v1.1.0 | PROC | Hard pre-test blocker; independent of fabrication critical path |
| OI-14 | AC §3.5 | Procure DC power meter: 0–100 W, ±1%; connect at heater terminals | PROC | Hard pre-test blocker; independent of fabrication critical path |
| OI-15 | AC §3.6 | Procure or verify DAQ system: ≥ 9 analog input channels, ≥ 16-bit, ≥ 1 Hz sample rate | PROC | Hard pre-test blocker; independent of fabrication critical path |
| OI-16 | AC §3.7 | Obtain current, NIST-traceable (or equivalent) calibration records for all instruments (OI-10 through OI-15); confirm calibration intervals not exceeded before test day | DOC | Hard pre-test blocker; cannot be finalized until all instruments are in hand |
| OI-17 | AC §4.1 | Specify TIM in writing: type (paste, pad, foil, or solder), product name, manufacturer, lot number, thermal conductivity (W/m·K), expected contact resistance at applied bond-line thickness (K·cm²/W); enter in PREFLIGHT_VERIFICATION.md §2 | DOC | Hard pre-test blocker; contact resistance is first-order contributor to measured R_th (STAGE7-AUD-001 W-4, M-2); must be specified before fixture assembly |
| OI-18 | AC §4.2 | Procure TIM per OI-17 specification; quantity sufficient for initial application plus one rework | PROC | Hard pre-test blocker; blocks fixture assembly |
| OI-19 | AC §5.1 | Commission coolant circulation loop: DI-water chiller set to 25 ± 1 °C inlet; verify hose and fitting compatibility; confirm degassing reservoir and bleed valve present | SETUP | Hard pre-test blocker; independent of fabrication critical path |
| OI-20 | AC §5.2 | Procure variable-speed pump (or fixed pump with adjustable bypass); provisional sizing must be revised after OI-09 flow estimate | PROC | Hard pre-test blocker; size from OI-09, not from Stage 4 Q |
| OI-21 | AC §5.3 | Fabricate or commission test fixture: machined Al or acetal block; sealed inlet/outlet around 5 mm × 5 mm footprint; TC mount bosses; fastened clamp for controlled heater contact force | FAB | Hard pre-test blocker; nominally parallel with AM specimen lead time |
| OI-22 | AC §5.4 | Install GFCI outlet on heater power circuit; verify trip function | SETUP | Safety — mandatory before any heater energization; can be completed in parallel with fabrication |
| OI-23 | AC §5.5 | Wire and function-test E-stop and over-temperature shutoff (T_cutoff = 100 °C); confirm automatic heater power-off on trigger | SETUP | Safety — mandatory before any heater energization |
| OI-24 | AC §5.6 | Place drip tray under test section; minimum 2 L capacity | SETUP | Safety — mandatory before any pressurized coolant flow |
| OI-25 | AC §5.7 | Install DAQ software on test computer; configure 9-channel logging at 1 Hz to `results/stage7_benchtop/test_data/phase_{X}/`; confirm writable output directory; perform 60-second test recording and verify all 10 CSV columns per DATA_SCHEMA_STAGE7.md v1.1.0 | SETUP | Hard pre-test blocker; must be verified before test day |
| OI-26 | AC §6.1 | Create and populate `results/stage7_benchtop/fabrication/build_log.md` with AM build parameters, material batch, machine ID, build orientation, post-processing records | DOC | Hard pre-test blocker; populate when specimens are received (OI-06) |
| OI-27 | AC §6.2 | Create `results/stage7_benchtop/README.md` as campaign summary stub: candidate ID, specimen IDs, target test date, companion document list | DOC | Hard pre-test blocker (organizational traceability); can be created immediately |

> **Numbering note:** The checklist rows yield 29 open items (sections 1–6,
> excluding closed items 1.3, 1.4, and 6.5).  Items 6.3 (run sheet print)
> and 6.4 (preflight sign-off) are same-day actions captured in Section 4
> of this document and are not assigned OI numbers in the register above.

---

## 3. Closure Waves — Dependency-Ordered Execution

Waves run sequentially where blocked by upstream outputs; items within a wave
are independent and may be worked in parallel.

---

### Wave 0 — Immediate (Day 0, no external dependencies)

Complete before issuing any procurement order or contacting any vendor.
All are documentation tasks executable with data already in the repository.

| OI | Description | Category | Output |
|----|------------|----------|--------|
| OI-01 | Create simulation_reference_candidate_02.json | DOC | `results/stage7_benchtop/simulation_reference/simulation_reference_candidate_02.json` |
| OI-02 | Record pipeline_git_sha.txt at OI-01 commit | DOC | `results/stage7_benchtop/simulation_reference/pipeline_git_sha.txt` |
| OI-03 | Export STL from Stage 3 volume.npy; verify watertight | DOC | STL file for vendor submittal |
| OI-04 | Write AM build specification | DOC | Build spec document |
| OI-17 | Specify TIM type and contact resistance in writing | DOC | PREFLIGHT_VERIFICATION.md §2 entry |
| OI-27 | Create campaign README.md stub | DOC | `results/stage7_benchtop/README.md` |

**Rationale:** OI-01 and OI-02 must be committed before any test data files
are created; populating them after test results exist introduces hindsight
bias.  OI-03 and OI-04 are required inputs to the vendor order (OI-05) and
must be ready before that call.  OI-17 requires no hardware; specifying
TIM early ensures it is ordered alongside instruments.

---

### Wave 1 — Concurrent Procurement (Days 1–3, after Wave 0 complete)

Issue all procurement orders that are fully specified and carry no dependency
on CT measurements.  OI-10 (flow meter) is withheld until Wave 3 because its
range cannot be finalized before OI-09 (physics-based flow estimate from CT).
OI-20 (pump) is provisionally ordered now at the widest plausible capacity and
must be confirmed or replaced after OI-09.

| OI | Description | Category | Output |
|----|------------|----------|--------|
| OI-05 | Confirm AM vendor; verify 0.5 mm capability; place specimen order | PROC | Purchase order for S7-C02-001 and S7-C02-002 |
| OI-11 | Procure differential pressure transducer (0–5 kPa, ±25 Pa) | PROC | Instrument in hand |
| OI-12 | Procure 4× Type-T thermocouples (30 AWG, ±0.5 °C) | PROC | Instruments in hand |
| OI-13 | Procure ambient temperature sensor (±1 °C, free air) | PROC | Instrument in hand |
| OI-14 | Procure DC power meter (0–100 W, ±1%) | PROC | Instrument in hand |
| OI-15 | Procure DAQ system (≥ 9 channels, ≥ 16-bit, ≥ 1 Hz) | PROC | System in hand |
| OI-18 | Procure TIM per OI-17 specification | PROC | TIM on hand |
| OI-20 | Procure pump (provisional sizing; confirm or replace after OI-09) | PROC | Pump in hand (provisional) |

**Rationale:** Instruments OI-11 through OI-15 are fully specified in
INSTRUMENTATION_AND_SENSORS.md and carry no dependency on fabrication or CT.
Order all in parallel to minimize elapsed time.  OI-10 (flow meter) is
intentionally deferred to Wave 3; its operating range cannot be finalized until
OI-09 provides the physics-based flow estimate from CT measurements.  OI-20
(pump) is ordered provisionally now to avoid an additional procurement delay
after specimen receipt; the provisional specification must be validated against
OI-09 before test day.

---

### Wave 2 — Bench Assembly (Days 3–14, parallel with specimen fabrication)

These items require only procured equipment and lab facilities, not the
specimen itself.  Execute during the AM fabrication lead time to arrive at
bench-ready before specimen delivery.

| OI | Description | Category | Output |
|----|------------|----------|--------|
| OI-19 | Commission chiller and DI-water coolant loop | SETUP | Loop operating at 25 ± 1 °C; degassing confirmed |
| OI-21 | Fabricate or commission test fixture for 5 mm specimen | FAB | Fixture assembled, leak-checked, TC mount positions verified |
| OI-22 | Install GFCI outlet on heater circuit | SETUP | GFCI installed; trip function verified |
| OI-23 | Wire and test E-stop and over-temperature shutoff | SETUP | Shutoff triggers at T = 100 °C; function test logged |
| OI-24 | Place drip tray under test section | SETUP | Drip tray in place; capacity ≥ 2 L confirmed |
| OI-25 | Install DAQ software; configure and test 60-second recording | SETUP | 60-second test CSV with all 10 columns verified; `T_amb_C` column present |

**Rationale:** None of these tasks requires the specimen.  Running them in
parallel with the AM lead time (OI-05 through OI-06) eliminates wasted idle
time.  OI-21 (fixture) is the highest-effort item in this wave; its
fabrication should begin immediately after OI-04 confirms the specimen
envelope (nominally 5 mm × 5 mm).

---

### Wave 3 — Post-Receipt Characterization (Days after OI-06 specimen delivery)

These items are gated on specimen receipt.

| OI | Description | Category | Upstream dependency |
|----|------------|----------|--------------------|
| OI-06 | Receive specimen S7-C02-001; assign ID; log receipt | FAB | OI-05 (AM order) |
| OI-26 | Populate build_log.md from AM vendor build data | DOC | OI-06 |
| OI-07 | Perform pre-test CT scan at ≤ 50 µm; commit PDF report | SETUP | OI-06 |
| OI-08 | Extract CT measurements to `ct_measurements_S7-C02-001.json` | DOC | OI-07 |
| OI-09 | Compute Hagen-Poiseuille / Ergun flow-rate estimate from CT channel diameter; bound realistic operating range | DOC | OI-08 |
| OI-10 | Procure flow meter, range sized from OI-09 estimate | PROC | OI-09 |
| OI-16 | Obtain and file current calibration records for all instruments | DOC | OI-10 through OI-15 all in hand |

> **CT gate:** If CT geometry deviation ≥ 50%, testing is halted regardless
> of all other items.  If deviation is 30–50%, proceed to test but document
> the exceedance in every run summary JSON.  If deviation < 30%, proceed
> normally.

> **OI-09 → OI-20 revisit:** After OI-09 is complete, confirm that the pump
> ordered under OI-20 (Wave 1, provisional sizing) is adequate.  If the
> physics-based flow estimate differs from the provisional sizing assumption
> by more than 2×, replace or re-specify the pump before test day.

---

### Wave 4 — Test-Day Tasks (Day of first heater energization)

These are same-day actions; they require no lead time beyond test-morning
preparation.  They are not pre-test blockers in the procurement or fabrication
sense, but all must be complete before heater energization.

| Ref | Description | Category |
|-----|------------|----------|
| AC §6.3 | Print or load RUN_SHEET_CANDIDATE_02.md; review with operator before first run | SETUP |
| AC §6.4 | Complete and countersign all five sections of PREFLIGHT_VERIFICATION.md | SETUP |
| PF §1 spot checks | Ice-bath TC check (0 ± 0.5 °C); pressure transducer zero-check (±25 Pa); power meter zero (±0.05 W); flow meter bucket check (±3%) | SETUP |
| PF §4 | Fixture-loss calibration run at 10, 25, 50 W with no specimen; record η_fixture in `calibration/fixture_loss_cal.json`; η_fixture ≥ 80% at all levels required to proceed | SETUP |

> **Same-day gate:** If η_fixture < 80% at any power level, do not install
> specimen.  Fix fixture insulation and re-run calibration.

---

## 4. True Blockers vs Same-Day Tasks

### 4.1 True Blockers

These items must be completed before arriving at the bench on test day.  A
single open item in this group is a hard NO-GO regardless of all other
preparation.

| OI | Category | Why it blocks |
|----|----------|--------------|
| OI-01 | DOC | Prediction record must be immutable before test data exist; cannot be back-filled |
| OI-02 | DOC | Git SHA must correspond to the state at prediction lock, not at test time |
| OI-03 | DOC | AM vendor cannot begin fabrication without the STL input |
| OI-04 | DOC | AM vendor cannot accept an order without a complete build specification |
| OI-05 | PROC | No specimen without a placed order; longest lead time on the critical path |
| OI-06 | FAB | No specimen, no test |
| OI-07 | SETUP | CT deviation gate must be evaluated before any flow or thermal test |
| OI-08 | DOC | CT measurements required for OI-09 and for back-simulation traceability |
| OI-09 | DOC | Flow meter and pump cannot be correctly sized until this estimate exists |
| OI-10 | PROC | No flow rate measurement without a correctly ranged flow meter |
| OI-11 | PROC | No pressure drop measurement without a transducer |
| OI-12 | PROC | R_th calculation requires T_heater and T_in at minimum |
| OI-13 | PROC | Ambient temperature logging required for parasitic-loss scaling |
| OI-14 | PROC | Heat input denominator for R_th must be measured at heater terminals |
| OI-15 | PROC | No data capture without a DAQ system |
| OI-16 | DOC | Uncalibrated instruments do not produce valid data |
| OI-17 | DOC | TIM contact resistance must be specified before fixture assembly and reported in every run summary |
| OI-18 | PROC | Cannot assemble fixture without TIM on hand |
| OI-19 | SETUP | No cooling, no test |
| OI-20 | PROC | Pump required to establish flow and ΔP target |
| OI-21 | FAB | Specimen must be constrained against heater face with repeatable force |
| OI-22 | SETUP | Safety — GFCI required before any heater energization |
| OI-23 | SETUP | Safety — E-stop required before any heater energization |
| OI-24 | SETUP | Safety — drip tray required before any pressurized flow |
| OI-25 | SETUP | No data capture without confirmed DAQ configuration |
| OI-26 | DOC | Build parameters must be in provenance before test to support Stage 8 handoff |
| OI-27 | DOC | Organizational traceability; must associate test artifacts with candidate and specimen IDs before test files are created |

### 4.2 Same-Day Tasks

These require no procurement, fabrication, or external lead time.  They are
operationally completed on test day (morning before first heater energization).
They do not drive the timeline; the critical path is the AM fabrication lead
time.

| Ref | Description | Category |
|-----|------------|----------|
| AC §6.3 | Review and print run sheet | SETUP |
| AC §6.4 | Complete and countersign PREFLIGHT_VERIFICATION.md | SETUP |
| PF §1 spot checks | Instrument spot calibration checks | SETUP |
| PF §4 | Fixture-loss calibration run | SETUP |

---

## 5. Critical Path

The minimum elapsed time to test day is dominated by the AM specimen
fabrication lead time, not by documentation or instrumentation.

```
Day 0:  Complete Wave 0 (OI-01, -02, -03, -04, -17, -27)  — 1 day
Day 1:  Issue all Wave 1 procurement orders simultaneously
        Begin Wave 2 bench assembly (runs in parallel)
  |
  |   AM fabrication lead time: typically 2–6 weeks
  |   (controls test date; all other paths complete within this window)
  |
Day N:  OI-06 — specimen received
Day N+1 to N+3: OI-07 CT scan → OI-08 CT JSON → OI-09 flow estimate
Day N+4: OI-10 flow meter ordered and expedited; OI-16 calibration records filed
Day N+7 (approx): All instruments on hand with calibration records
  |
Test day: Wave 4 same-day tasks → GO/NO-GO → Phase A heater energization
```

All Wave 2 bench assembly tasks (OI-19 through OI-25) must be complete before
specimen delivery so the bench is ready to receive the specimen on arrival.

---

## 6. Dependency Graph Summary

```
OI-03 (STL) ──┐
OI-04 (spec) ─┴─► OI-05 (order) ──► OI-06 (receive) ──► OI-07 (CT scan)
                                                              │
                                                       OI-08 (CT JSON)
                                                              │
                                                       OI-09 (flow estimate)
                                                              │
                                               ┌─────────────┤
                                         OI-10 (flow meter)  OI-20 (pump confirm)

OI-01 (sim ref JSON) ──► OI-02 (git SHA)        [both: before any test data]

OI-11 through OI-15 (instruments) ──► OI-16 (calibration records)
                                                          [parallel with fabrication]

OI-17 (TIM spec) ──► OI-18 (TIM procure) ──► OI-21 (fixture) ──► OI-22/23/24 (safety)

OI-25 (DAQ software)                            [parallel with fabrication]
OI-26 (build log)                               [after OI-06]
OI-27 (README)                                  [Wave 0, no dependency]
```

---

## 7. Optional Items (Not in Critical Path)

Identified in TEST_DAY_GAP_CLOSURE.md Section 4.  Not required for Stage 7
pass/fail determination.  Recommended to reduce interpretation ambiguity.

| Item | Value | Recommended when |
|------|-------|-----------------|
| Second specimen S7-C02-002 | Covers rework risk; enables repeat with identical geometry | Order at OI-05 for no additional lead time |
| Back-simulation on as-built CT geometry (STAGE7-AUD-001 M-5) | Separates fabrication deviation from model error if result falls outside acceptance band | If OI-07 CT deviation > 10% from design |
| Higher-resolution Stage 4/5 simulation on 5 mm domain (STAGE7-AUD-001 H-2, M-6) | All current predictions were computed on a 2 mm domain; fabrication target is 5 mm | Before committing to fabrication if schedule permits |
| IR camera for surface temperature mapping | Diagnoses heater uniformity and hotspots | If T_heater repeatability is poor across runs |
| Post-test CT scan | Detects internal damage after thermal cycling | After Phase B |
| Reynolds number estimate from bench Q and CT channel diameter (STAGE7-AUD-001 M-8) | Confirms Darcy flow-regime assumption | Compute from measured Q after first Phase B run |

---

## 8. Inherited Warnings — Do Not Lose in Execution

These discrepancies from STAGE7-AUD-001 do not add open items but must be
acknowledged in every run summary JSON.  They are carried here as a reminder
to the test team.

| ID | Issue | Required action at test |
|----|-------|------------------------|
| H-1 | Stage 4 Q = 44.02 LPM is non-physical (Darcy solver artifact; implies ~183 m/s). | Size flow meter and pump from OI-09 estimate only. Do not apply Stage 4 Q as acceptance criterion. |
| H-2 | Stage 4/5 predictions were computed on a 2 mm domain; fabrication target is 5 mm. | Document domain mismatch in every run summary. Acceptance bands (R_th within 2×, ΔP within 3×) accommodate this, but the mismatch is not by design. |
| W-1 | Stage 5 actual heat input is 4.0 W, not 25 W. | Record total_power_w = 4.0 in OI-01 simulation reference. State the power-independence assumption explicitly in every run summary. |
| W-3 | Simulation domain (2 mm) ≠ fabrication domain (5 mm). | Document in every run summary. Does not invalidate the test; must be carried as a known limitation in Stage 8. |
| W-4 | Contact resistance (heater-to-specimen interface) is not modeled in Stage 5. At 4 mm² heated area, 0.5 K·cm²/W adds ~12.5 K/W to measured R_th. | Report TIM contact resistance separately in every run summary; subtract from measured R_th before applying the 2× acceptance band. |

---

## 9. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial release |

**End of document.**
