# Stage 7 Wave 0 / Wave 1 Action Packet

**Document ID:** STAGE7-AP-001  
**Date:** 2026-03-06  
**Status:** ACTIVE — first-closure packet  
**Scope:** Converts OPEN_ITEMS_CLOSURE_ORDER.md (STAGE7-OI-001) Wave 0 and Wave 1
items into per-item closure actions with owner assignments, dependencies, and
verifiable closure evidence.  
**Companion documents:** OPEN_ITEMS_CLOSURE_ORDER.md (STAGE7-OI-001),
ARTIFACT_CHECKLIST_PRE_TEST.md (STAGE7-AC-001), DATA_SCHEMA_STAGE7.md
(STAGE7-DS-001), PREFLIGHT_VERIFICATION.md (STAGE7-PF-001),
STAGE7_VALIDATION_AUDIT_MEMO.md (STAGE7-AUD-001)  
**Candidate:** candidate_02_diamond_2d_s1045

> **Scope discipline:** This document introduces no code changes, no new
> simulation results, and no new physics claims.  It converts already-agreed
> open items into step-level actions for immediate execution.

---

## 1. Owner-Type Key

| Tag | Role |
|-----|------|
| **docs** | One person with repo write access and existing data in `results/`; no external dependency |
| **procurement** | Purchasing lead with budget authority; requires external vendor contact and purchase order |
| **fabrication** | AM vendor or in-house machine shop; long external lead time |
| **setup** | Lab engineer with physical bench access and procured equipment |

---

## 2. Wave 0 — Immediate Repo Actions (Day 0)

**Condition to enter:** None.  All six items are executable with data already
present in the repository.  No external procurement, no hardware, no test bench
required.

**Completion gate:** All six items committed to the repo before any Wave 1
procurement order is issued.  OI-01 and OI-02 must be the first two commits;
they establish the immutable prediction record.

---

### 2.1 Wave 0 Action Table

| Item ID | Category | Closure Action | Owner Type | Dependency | Evidence to Mark Closed |
|---------|----------|---------------|------------|------------|------------------------|
| OI-01 | DOC | Create `results/stage7_benchtop/simulation_reference/simulation_reference_candidate_02.json`. Populate using values already in the repository: `thermal_resistance_KW = 11.265617018419787` (from `results/stage5_thermal_smoke/candidate_02_diamond_2d_s1045/thermal_metrics.json`); `peak_temperature_C = 70.062`; `pressure_drop_Pa = 1000.0`; `heat_flux_w_m2 = 1000000.0`; `total_power_w = 4.0` (not 25 W — STAGE7-AUD-001 W-1); `simulation_domain_mm = [2.0, 2.0, 2.0]` (not 5 mm — STAGE7-AUD-001 H-2); `stage3_source = "candidate_02_diamond_2d_s1045"`; `schema_version = "1.1.0"`; leave `pipeline_git_sha` as a placeholder until OI-02. | docs | None — all values are in existing results files | File present at exact path; `schema_version` field = `"1.1.0"`; `total_power_w = 4.0`; `simulation_domain_mm` is a three-element array of 2.0; no field contains 25 W or 5.0 mm domain as a value |
| OI-02 | DOC | Immediately after OI-01 is committed, run `git rev-parse HEAD` and write the resulting 40-character SHA to `results/stage7_benchtop/simulation_reference/pipeline_git_sha.txt` (single line, no trailing whitespace). Commit this file. The SHA in the file must match the git log entry for the OI-01 commit; it must not be updated again after this point. | docs | OI-01 must be committed before this step | File present at exact path; SHA in file is 40 hex characters; `git log --oneline` confirms that SHA is the commit that introduced `simulation_reference_candidate_02.json` |
| OI-03 | DOC | Export an STL from `results/stage3_geometry_smoke/candidate_02_diamond_2d_s1045/volume.npy` (or the remediated equivalent at 0.25 mm voxel pitch). Apply marching-cubes triangulation and scale so that one voxel = 0.25 mm in world units. Run a mesh-repair check (e.g., `admesh --analyze`) to confirm: zero open edges, zero non-manifold edges, positive volume. Commit the STL or commit a manifest file that records the STL filename, byte size, SHA-256 hash, watertight-check tool name and version, and check result. | docs | Remediated Stage 3 `volume.npy` must exist in `results/` (it does — see `results/stage3_geometry_smoke/`) | STL file or manifest committed; manifest (or inline record) shows zero open edges and zero non-manifold edges; file is available for vendor transmission |
| OI-04 | DOC | Write an AM build specification document and commit it to `docs/stage7_validation/` or `results/stage7_benchtop/fabrication/`. Required sections: (a) material — Al 6061-T6 or equivalent Al alloy within vendor L-PBF qualification portfolio; (b) minimum feature requirement — ≤ 0.5 mm, vendor must provide process capability evidence; (c) build orientation — note channel directionality and confirm with vendor prior to build start; (d) support strategy — minimize supports inside internal channels; include powder evacuation access holes; (e) post-processing — support removal, T6 stress relief per AMS 2770 or equivalent, bead blast for surface finish; (f) acceptance criteria — two specimens (S7-C02-001 and S7-C02-002); powder evacuation confirmed by vendor before shipping; (g) laser and scan parameters — leave as vendor-fill fields; do not specify. | docs | OI-03 (STL must exist to accompany the spec to vendor); OI-04 body text may be written in parallel with OI-03 | Build specification document committed to repo; all six required sections present; no vendor laser parameters assumed or filled in; powder evacuation requirement explicitly stated |
| OI-17 | DOC | Populate PREFLIGHT_VERIFICATION.md §2 (Thermal Interface Material Specification) with: TIM type (paste / pad / foil / solder / other); product name and manufacturer; lot number (fill in when TIM is received); thermal conductivity in W/(m·K); expected contact resistance at the applied bond-line thickness in K·cm²/W; note that at the 4 mm² heated footprint, a contact resistance of 0.5 K·cm²/W adds approximately 12.5 K/W to measured R_th (STAGE7-AUD-001 W-4); note that the contact resistance contribution must be subtracted from measured R_th before applying the 2× acceptance band. Select a TIM type now; record it here before ordering (OI-18). | docs | None | PREFLIGHT_VERIFICATION.md §2 contains all required fields with no blank entries except lot number (which will be filled on receipt); contact resistance value is numeric, not a placeholder; audit memo W-4 cross-reference present |
| OI-27 | DOC | Create `results/stage7_benchtop/README.md` as a campaign summary stub. Required fields: candidate ID (`candidate_02_diamond_2d_s1045`); specimen IDs (`S7-C02-001`, `S7-C02-002`); target test date (fill-in field; populate when vendor confirms delivery); companion document list (at minimum: BENCHTOP_VALIDATION_PLAN.md, ARTIFACT_CHECKLIST_PRE_TEST.md, TEST_MATRIX.md, OPEN_ITEMS_CLOSURE_ORDER.md, WAVE0_WAVE1_ACTION_PACKET.md, DATA_SCHEMA_STAGE7.md, INSTRUMENTATION_AND_SENSORS.md, PREFLIGHT_VERIFICATION.md, RUN_SHEET_CANDIDATE_02.md). | docs | None | File present at `results/stage7_benchtop/README.md`; all four required fields present; target test date field exists even if value is TBD |

---

## 3. Wave 1 — Concurrent Procurement (Days 1–3, after Wave 0 complete)

**Condition to enter:** All six Wave 0 items committed.  OI-03 and OI-04 must
be complete before the AM vendor order (OI-05) can be issued.  OI-17 must be
complete before TIM procurement (OI-18) can be issued.  Instruments OI-11
through OI-15 and pump OI-20 carry no dependency on fabrication or on each
other and may be ordered simultaneously.

**Completion gate:** All eight purchase orders placed within 24 hours of Wave 0
completion.  Delivery tracking for each order recorded in the instrument
inventory log.

---

### 3.1 Wave 1 Action Table

| Item ID | Category | Closure Action | Owner Type | Dependency | Evidence to Mark Closed |
|---------|----------|---------------|------------|------------|------------------------|
| OI-05 | PROC | Issue RFQ to at least two metal L-PBF vendors referencing the OI-03 STL and OI-04 build specification. Require each vendor to provide documented process capability evidence showing ≤ 0.5 mm minimum feature size in Al alloy L-PBF. Select vendor; place order for two specimens (S7-C02-001 and S7-C02-002) with serial numbers pre-assigned by the test team. Record vendor name, purchase order number, quoted delivery date, and vendor capability record. | procurement | OI-03 (STL available for RFQ), OI-04 (build spec available for RFQ) | Purchase order number on file; vendor capability record (stating ≤ 0.5 mm in Al L-PBF) filed; expected delivery date recorded; two specimen serial numbers assigned |
| OI-11 | PROC | Order one differential pressure transducer: 0–5 kPa full-scale range (or two absolute pressure transducers, each 0–110 kPa, with ΔP derived by subtraction); ±25 Pa accuracy at the operating point; wetted materials DI-water-compatible (316L stainless steel or PTFE); analog output 4–20 mA or 0–5 V compatible with DAQ (OI-15). Record make, model, serial number, and calibration certificate. | procurement | None | Transducer in hand; make/model/serial logged in instrument inventory; calibration certificate on file showing current calibration date |
| OI-12 | PROC | Order 4× Type-T thermocouples: 30 AWG conductors, PFA or PTFE insulation, ±0.5 °C accuracy at 0–100 °C. One each for T_in (immersion), T_out (immersion), T_heater (embedded in heater block), T_top (surface-mount on cold plate top face). Record lot number and calibration certificate for each. | procurement | None | 4 thermocouples in hand; lot number and individual calibration certificate (or batch certificate) on file for all four |
| OI-13 | PROC | Order 1× ambient temperature sensor: Type-T or Type-K thermocouple, or NTC thermistor (10 kΩ nominal); ±1 °C accuracy; mounted in free air, not in the coolant flow path; compatible with an available DAQ channel (OI-15). This sensor provides the `T_amb_C` column required by DATA_SCHEMA_STAGE7.md v1.1.0. Record make, model, and calibration certificate. | procurement | None | Sensor in hand; spec sheet confirming ±1 °C accuracy; compatibility with DAQ channel type verified; `T_amb_C` column presence confirmed in 60-second test recording (verified at OI-25) |
| OI-14 | PROC | Order 1× DC power meter: 0–100 W range, ±1% of reading accuracy; must connect directly at heater terminals (not upstream in the power supply); 4-wire (Kelvin) connection preferred for heater resistances below 10 Ω; analog or RS-232/USB output compatible with DAQ or separate logging. Record make, model, serial number, and calibration certificate. | procurement | None | Power meter in hand; make/model/serial logged; calibration certificate on file; instrument measures at heater terminals as confirmed at OI-25 test recording |
| OI-15 | PROC | Order a DAQ system with: ≥ 9 analog input channels (10 recommended: 5 thermocouple-direct or CJC-compensated channels, 2 pressure channels, 1 flow channel, 1 power channel, 1 spare); ≥ 16-bit analog-to-digital resolution; ≥ 1 Hz sample rate on all channels simultaneously; software or firmware capable of writing a single 10-column CSV at 1 Hz to a user-specified output directory. Record make, model, and software version. | procurement | None | DAQ system in hand; make/model/software version logged; 60-second test recording at OI-25 confirms all 10 DATA_SCHEMA_STAGE7.md v1.1.0 columns present at 1 Hz |
| OI-18 | PROC | Order TIM per the type and specification entered in PREFLIGHT_VERIFICATION.md §2 under OI-17. Quantity must be sufficient for the initial application plus one full rework at the 5 mm × 5 mm contact footprint (for thermal paste: approximately 5–10 g; for pad-type: at least 2 pads). Store per manufacturer instructions (temperature, humidity). Record product name, manufacturer, lot number, and quantity received; enter lot number in PREFLIGHT_VERIFICATION.md §2. | procurement | OI-17 (TIM type and specification must be entered before placing this order) | TIM on hand; product matches OI-17 specification exactly (type, manufacturer, grade, thermal conductivity); quantity sufficient for rework confirmed; lot number entered in PREFLIGHT_VERIFICATION.md §2 |
| OI-20 | PROC | Order a variable-speed pump (or fixed pump with adjustable bypass valve) sized at provisional upper-bound capacity: 0–500 mL/min flow range with ≥ 50 kPa head at maximum flow. DI-water-compatible wetted materials. Record make, model, serial number. Note in the closure record that this sizing is provisional pending OI-09 (physics-based flow estimate from CT); if OI-09 result differs from the provisional 0–500 mL/min range by more than 2×, the pump must be replaced or a bypass added before test day. Do not use Stage 4 Q = 44.02 LPM for sizing (STAGE7-AUD-001 H-1). | procurement | None for provisional order; OI-09 required for final validation before test day | Pump in hand; make/model/serial logged; provisional sizing (0–500 mL/min, ≥ 50 kPa) documented; post-OI-09 confirmation note attached, confirming that sizing will be re-evaluated when CT flow estimate is available |

---

## 4. Closure Classification

### 4.1 Can Be Closed Immediately in the Repository

These items require only existing data in `results/` and write access to the
repository.  No hardware, no procurement, no external contact required.  All
are Wave 0.

| Item ID | Category | Action location |
|---------|----------|----------------|
| OI-01 | DOC | Create `results/stage7_benchtop/simulation_reference/simulation_reference_candidate_02.json` |
| OI-02 | DOC | Create `results/stage7_benchtop/simulation_reference/pipeline_git_sha.txt` after OI-01 commit |
| OI-03 | DOC | Generate STL from `results/stage3_geometry_smoke/…/volume.npy`; commit STL or manifest |
| OI-04 | DOC | Write build specification; commit to `docs/stage7_validation/` or `results/stage7_benchtop/fabrication/` |
| OI-17 | DOC | Edit `docs/stage7_validation/PREFLIGHT_VERIFICATION.md` §2 to populate TIM specification |
| OI-27 | DOC | Create `results/stage7_benchtop/README.md` |

**Note on OI-02:** Although OI-02 is a repo-only action, it must execute after
OI-01 is committed and its SHA is known.  It cannot be done in parallel with
OI-01.

**Note on OI-03:** STL generation requires a mesh export step (marching-cubes
or equivalent) and a watertight verification step.  Both are executable locally
with open-source tooling (scikit-image, Open3D, admesh) without external
dependencies.

---

### 4.2 Requires Outside Procurement or Fabrication

These items cannot be closed without contacting an external vendor and placing
an order.  All are Wave 1.  Lead times are external and not controlled by the
test team.

| Item ID | Category | Estimated lead time | Critical-path role |
|---------|----------|--------------------|--------------------|
| OI-05 | PROC | 2–6 weeks (metal L-PBF fabrication) | **Critical path** — controls test date; longest single lead time in the plan |
| OI-11 | PROC | 1–5 business days | Not on critical path if ordered on Day 1 |
| OI-12 | PROC | 1–5 business days | Not on critical path if ordered on Day 1 |
| OI-13 | PROC | 1–5 business days | Not on critical path if ordered on Day 1 |
| OI-14 | PROC | 1–5 business days | Not on critical path if ordered on Day 1 |
| OI-15 | PROC | 1–10 business days (DAQ systems vary) | Not on critical path if ordered on Day 1 |
| OI-18 | PROC | 1–5 business days | Not on critical path if ordered on Day 1 |
| OI-20 | PROC | 1–5 business days | Not on critical path if ordered on Day 1; provisional sizing must be validated against OI-09 before test day |

The AM specimen order (OI-05) is the single item that sets the test date.
All other Wave 1 items have lead times short enough that ordering on Day 1
(the day after Wave 0 completion) will result in delivery before specimen
receipt regardless of vendor selection.

---

### 4.3 Can Proceed in Parallel

The table below identifies which Wave 0 and Wave 1 items may be worked
simultaneously without waiting for each other.

| Parallel group | Items | Coordination note |
|---------------|-------|------------------|
| Wave 0 — primary parallel set | OI-01, OI-03, OI-04, OI-17, OI-27 | All five are independent; assign to different individuals if available |
| Wave 0 — serial follow-on | OI-02 | Must follow OI-01 commit; takes < 5 minutes once OI-01 is merged |
| OI-03 and OI-04 | OI-03 (STL), OI-04 (build spec) | The body of OI-04 may be drafted before OI-03 is complete; STL must be appended and watertight check confirmed before the package is transmitted to the AM vendor |
| Wave 1 — instrument procurement block | OI-11, OI-12, OI-13, OI-14, OI-15 | All five are fully specified in INSTRUMENTATION_AND_SENSORS.md; no inter-dependencies; issue all five purchase orders on the same business day |
| Wave 1 — TIM procurement | OI-18 | Parallel with instrument block; requires OI-17 to be committed first |
| Wave 1 — pump provisional | OI-20 | Parallel with instrument block and OI-18; provisional specification is independent of CT results |
| Wave 1 — AM vendor order | OI-05 | Parallel with instrument block, OI-18, and OI-20; requires OI-03 + OI-04 only |
| Wave 2 bench assembly (outside scope of this document) | OI-19, OI-21, OI-22, OI-23, OI-24, OI-25 | All may begin as soon as procured equipment arrives; run in parallel with AM specimen fabrication lead time |

**Items intentionally excluded from Wave 1:**

- **OI-10 (flow meter):** Range cannot be finalized until OI-09 (physics-based
  flow estimate from CT channel geometry) is complete.  OI-09 cannot be
  completed until OI-07 (CT scan) is available, which is gated on OI-06
  (specimen receipt).  OI-10 is a Wave 3 item.

---

## 5. Minimum Path to First Specimen-Ready State

> **One-page summary.** "Specimen-ready" means: one cold-plate specimen
> (S7-C02-001) has been received, CT-scanned, and CT-qualified; the bench is
> assembled, safety-checked, and DAQ-verified; all instruments are calibrated
> and on hand; the prediction record is locked in the repo.  This state
> immediately precedes test-day Wave 4 tasks and first heater energization.

---

### Step 1 — Lock the prediction record (Day 0, ~4 hours)

Execute Wave 0 in a single working session.  Assign one person per item where
possible.  Strict ordering applies only within the OI-01 → OI-02 pair.

1. **OI-01:** Populate and commit `simulation_reference_candidate_02.json` using
   values already in `results/`.  Confirm `total_power_w = 4.0` and
   `simulation_domain_mm = [2.0, 2.0, 2.0]` before committing.
2. **OI-02:** Record the HEAD SHA in `pipeline_git_sha.txt`; commit.  The
   prediction record is now immutable.
3. **OI-03, OI-04, OI-17, OI-27:** Complete in parallel.  OI-03 and OI-04 are
   required inputs for the AM vendor order.  OI-17 is required before TIM
   procurement.  OI-27 establishes campaign traceability.

**Exit criterion:** Six files created or updated and committed to the repo.

---

### Step 2 — Issue all procurement orders (Day 1, one business day)

Issue all eight Wave 1 orders on the same business day.

- AM vendor order (OI-05): longest lead time; place first; 2–6 week window
  begins on the day the order is confirmed by the vendor.
- Instruments (OI-11, OI-12, OI-13, OI-14, OI-15): order in parallel; expected
  delivery within 1–10 business days; will arrive before specimen receipt.
- TIM (OI-18): order in parallel with instruments; 1–5 business days.
- Pump provisional (OI-20): order in parallel with instruments; 0–500 mL/min
  provisional sizing; will be validated against OI-09 after CT.

**Exit criterion:** Eight purchase orders placed; vendor-confirmed delivery
dates recorded for all eight.

---

### Step 3 — Bench assembly during AM lead time (Days 3 to N−2)

While the AM specimen is being fabricated, complete Wave 2 bench assembly.
These tasks require only procured equipment and lab access.

| Wave 2 item | Prerequisite on hand |
|------------|---------------------|
| OI-19 — Commission chiller and DI-water loop | Chiller (lab facility); hoses; fittings |
| OI-21 — Fabricate test fixture | OI-04 build spec (specimen envelope confirmed as 5 mm × 5 mm) |
| OI-22 — Install GFCI outlet on heater circuit | Electrician access; GFCI device |
| OI-23 — Wire and test E-stop and over-temperature shutoff | Safety relay; thermocouple at T_cutoff = 100 °C |
| OI-24 — Place drip tray (≥ 2 L) | Drip tray |
| OI-25 — Install DAQ software; 60-second test recording with all 10 columns | OI-15 DAQ system delivered |

The bench must be fully assembled and all Wave 2 items closed before specimen
delivery.  Do not wait for the specimen to arrive before starting bench work.

**Exit criterion:** Wave 2 six items closed; bench is flow-circulating at
25 ± 1 °C; GFCI and E-stop function-tested; DAQ 60-second recording confirmed
with all 10 columns.

---

### Step 4 — Receive and qualify the specimen (Days N to N+4)

| Day | Action | Output |
|-----|--------|--------|
| N | OI-06: Receive S7-C02-001; assign specimen ID; log receipt in build log | Specimen logged |
| N | OI-26: Populate build_log.md from vendor-supplied build data | Build log committed |
| N+1 | OI-07: Submit S7-C02-001 for pre-test CT scan at ≤ 50 µm resolution | CT scan initiated |
| N+2 | OI-07 result: Evaluate geometry deviation. ≥ 50%: STOP. 30–50%: document, proceed with note. < 30%: proceed normally. Commit `ct_report_S7-C02-001.pdf`. | CT report on file |
| N+2 | OI-08: Extract CT measurements to `ct_measurements_S7-C02-001.json` (channel diameters, wall thicknesses, effective porosity) | CT JSON on file |
| N+3 | OI-09: Compute Hagen-Poiseuille or Ergun flow-rate estimate from CT-measured channel diameter; bound realistic operating range. Do not use Stage 4 Q = 44.02 LPM. | Flow estimate committed |
| N+3 | OI-20 revisit: Compare OI-09 estimate to provisional pump sizing. If > 2× difference, replace pump before test day. | Pump sizing confirmed |
| N+4 | OI-10: Place flow meter order sized from OI-09 estimate (lower bound ≤ 50% of estimate, upper bound ≥ 2×); expedite. | Flow meter on order |
| N+7 (approx.) | OI-10 delivered; OI-16: Obtain current calibration records for all instruments (OI-10 through OI-15) and file. | All instruments calibrated |

**Exit criterion:** All of OI-06, OI-07 (pass gate), OI-08, OI-09, OI-10,
OI-16, OI-26 closed.

---

### Step 5 — Test-day readiness confirmation (Day N+7 to N+10, approx.)

Install specimen S7-C02-001 in the test fixture.  Complete Wave 4 same-day
tasks in sequence before any heater energization.

| Ref | Action | Gate |
|-----|--------|------|
| AC §6.3 | Review and load RUN_SHEET_CANDIDATE_02.md; brief operator | Administrative |
| AC §6.4 | Complete and countersign all five sections of PREFLIGHT_VERIFICATION.md | Hard gate |
| PF §1 spot checks | TC ice-bath (0 ± 0.5 °C); pressure zero (±25 Pa); power meter zero (±0.05 W); flow meter bucket check (±3%) | Fail → do not energize |
| PF §4 | Fixture-loss calibration run at 10, 25, 50 W with no specimen; confirm η_fixture ≥ 80% at all levels | η_fixture < 80% → fix fixture insulation and repeat |

**Exit criterion:** PREFLIGHT_VERIFICATION.md fully signed; η_fixture ≥ 80% at
all three power levels.  First heater energization (Phase A) may proceed.

---

### Minimum elapsed time estimate

| Segment | Elapsed time (calendar days) |
|---------|------------------------------|
| Wave 0 documentation | 1 |
| Wave 1 procurement initiation | 1 |
| AM specimen fabrication lead time | 14–42 (2–6 weeks; controls test date) |
| Bench assembly during AM lead time | Runs in parallel; does not add to elapsed time |
| Specimen receipt through CT qualification and flow meter delivery | ~7 |
| Test-day readiness confirmation | 0.5 |
| **Total minimum elapsed time** | **~23 days (if AM lead time is 2 weeks)** |

The AM specimen fabrication lead time is the only schedule-controlling variable
outside the test team's control.  Every other Wave 0, 1, and 2 item can be
closed before the specimen arrives.

---

## 6. Open Item Closure Status Summary

| Item ID | Wave | Owner Type | Status | Blocking downstream |
|---------|------|------------|--------|---------------------|
| OI-01 | 0 | docs | OPEN | OI-02; any test data file |
| OI-02 | 0 | docs | OPEN | Stage 8 provenance |
| OI-03 | 0 | docs | OPEN | OI-05 (AM vendor order) |
| OI-04 | 0 | docs | OPEN | OI-05 (AM vendor order) |
| OI-17 | 0 | docs | OPEN | OI-18 (TIM procurement); OI-21 (fixture assembly) |
| OI-27 | 0 | docs | OPEN | Campaign traceability |
| OI-05 | 1 | procurement | OPEN | OI-06, OI-07, OI-08, OI-09, OI-10, OI-21 (controls test date) |
| OI-11 | 1 | procurement | OPEN | OI-16 (calibration records) |
| OI-12 | 1 | procurement | OPEN | OI-16 (calibration records) |
| OI-13 | 1 | procurement | OPEN | OI-16 (calibration records); T_amb_C column in data |
| OI-14 | 1 | procurement | OPEN | OI-16 (calibration records) |
| OI-15 | 1 | procurement | OPEN | OI-25 (DAQ software config); OI-16 |
| OI-18 | 1 | procurement | OPEN | OI-21 (fixture assembly) |
| OI-20 | 1 | procurement | OPEN | Coolant flow; ΔP target; must be revalidated after OI-09 |

All 14 items in this packet are currently OPEN.  No items in Wave 0 or Wave 1
have been closed as of the date of this document.

---

## 7. Inherited Warnings — Carry Forward to Every Run Summary

Per STAGE7-AUD-001.  No new physics claims are introduced here.  These must
appear in every run summary JSON.

| Audit ID | Issue | Required action |
|----------|-------|----------------|
| H-1 | Stage 4 Q = 44.02 LPM is non-physical (Darcy permeability artifact; implies ~183 m/s mean velocity). | Size flow meter and pump exclusively from OI-09 estimate. Do not record Stage 4 Q as an acceptance criterion. |
| H-2 | Stage 4/5 predictions computed on a 2 mm domain; fabrication target is 5 mm. | Record domain mismatch in every run summary. Acceptance bands (R_th within 2×, ΔP within 3×) accommodate this; the mismatch is not by design. |
| W-1 | Stage 5 actual heat input is 4.0 W, not 25 W. | OI-01 records `total_power_w = 4.0`. State the power-independence assumption explicitly in every run summary. |
| W-3 | Simulation domain (2 mm) ≠ fabrication domain (5 mm). | Document in every run summary as a known limitation carried to Stage 8. |
| W-4 | Contact resistance is not modeled in Stage 5. At 4 mm² heated area, 0.5 K·cm²/W adds ~12.5 K/W to measured R_th. | Subtract TIM contact resistance from measured R_th before applying the 2× acceptance band. Report TIM contact resistance separately in every run summary. |

---

## 8. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial release |

**End of document.**
