# Stage 7 Validation Package — Technical Audit Memo

**Document ID:** STAGE7-AUD-001  
**Date:** 2026-03-06  
**Status:** FINAL  
**Scope:** Technical audit of merged Stage 7 benchtop validation planning docs  
**Audited documents:** BENCHTOP_VALIDATION_PLAN.md, TEST_MATRIX.md, INSTRUMENTATION_AND_SENSORS.md, DATA_SCHEMA_STAGE7.md, ARTIFACT_LAYOUT.md, CAMBER_STAGE7_WORKLOAD_TEMPLATE.md  

---

## Classification Key

Each finding is tagged:

- **(planning-quality)** — Document or process defect, fixable without touching physics.
- **(physics-performance)** — Rooted in the simulation models; affects whether bench data can be meaningfully compared to predictions.

---

## 1. GOOD

1. **Document coverage.** Six documents span plan, test matrix, instrumentation, data schema, artifact layout, and tooling decision (Camber defer). No obvious category is missing from the package structure.

2. **Provenance chain.** ARTIFACT_LAYOUT.md defines a clear traceability flow: Stage 3 geometry → Stage 4/5 simulation → Stage 6 screening → simulation reference snapshot → fabricated specimen → CT scan → test runs → campaign summary → verdict. Git SHA pinning is included. Sufficient for Stage 8 handoff if followed.

3. **Quantity labeling.** SIMULATED, FLOW_SIMULATED, STRUCTURAL_SCREENED, MANUFACTURABILITY_SCREENED, MEASURED, DERIVED, CT_MEASURED labels are consistent with upstream stages and are carried through the data schema. Good for audit trail.

4. **Phased test sequencing.** A → B → E priority path is sensible: characterize, test nominal, confirm integrity. Extended phases (C, D) are correctly flagged as optional.

5. **Immediate-stop criteria.** Leak, R_th > 3×, ΔP > 5×, CT deviation > 50% — these are defined and actionable.

6. **Safety instrumentation.** GFCI, E-stop, over-temperature shutoff, overpressure relief, drip tray. Adequate for a water bench at ≤ 50 W.

7. **Calibration protocol.** Ice-point and boiling-point TC checks, zero-check on pressure transducers, bucket-test for flow meter, precision-load for power meter. Each has frequency and acceptance criteria.

8. **Energy balance closure.** > 90% threshold as a measurement integrity check. Correctly classified as secondary.

9. **Scope discipline.** Explicit statement that Stage 7 is not product qualification, not certification, not optimal-design selection. Repeated in plan and matrix.

10. **Schema versioning.** Semver in all JSON schemas with forward-compatibility plan. Good for downstream tooling.

---

## 2. WEAK

### W-1. Simulation heat input vs bench power — factual misstatement (planning-quality)

BENCHTOP_VALIDATION_PLAN.md Section 5.4 states "Nominal power: 25 W" and "Matches Stage 5 boundary condition."

Actual Stage 5 boundary condition: heat_flux = 1 MW/m² applied to the bottom face of the computational domain. The simulation domain is 20 × 20 voxels at 0.1 mm per voxel (see geometric_quantities.domain_volume_mm3 = 8.0 in thermal_metrics.json), giving a heated surface area of 4 mm² and total heat input Q_total = 4.0 W. This is recorded in the metrics: `"heat_input_w": 4.000000000000001`.

25 W ≠ 4 W. The plan's claim of "matching" is incorrect.

If R_th is power-independent (single-phase, no boiling, linear conduction), the mismatch does not invalidate the R_th comparison. But the document should state this assumption explicitly rather than claiming a match that does not exist.

### W-2. Predicted flow rate is non-physical (physics-performance)

Stage 4 predicts Q = 44.02 LPM (0.000734 m³/s) at ΔP = 1000 Pa for the candidate geometry. Through a domain cross-section of 4 mm² (2 × 2 mm), this implies a mean velocity of ~183 m/s. Through the porous volume (56% porosity), effective velocity is ~327 m/s.

For water at 25 °C, this exceeds the speed of sound by approximately a factor of 0.22 (sound speed ≈ 1497 m/s) — not supersonic, but still 4–5 orders of magnitude above what any realistic porous-medium flow at 1000 Pa would produce.

Root cause: the Darcy solver assigns k_fluid = 1e-6 m² to fluid voxels. Real porous media permeabilities are 1e-12 to 1e-8 m². The solver is not validated for absolute flow-rate prediction.

Downstream impact: INSTRUMENTATION_AND_SENSORS.md Section 2.3 sizes the flow meter to 0–100 LPM, and the pump to "0–100+ LPM." This is driven by the non-physical prediction. Real bench flow rates through a 5 mm TPMS cold plate at 1000 Pa will likely be mL/min, not L/min.

### W-3. Domain dimension inconsistency (planning-quality)

The validation plan (Section 3.1) states:

- Voxel size: 0.25 mm
- Resolution: 20 × 20 × 20
- Domain: 5.0 × 5.0 × 5.0 mm

These match the remediated Stage 3 config (src/stage3_geometry/config.py: VOXEL_SIZE_MM = 0.25, SMOKE_RESOLUTION = 20).

However, the actual Stage 4 and Stage 5 simulation results in the repository show `domain_volume_mm3: 8.0`, which corresponds to a 2.0 × 2.0 × 2.0 mm domain (20 voxels × 0.1 mm). The thermal and flow predictions (R_th = 11.27 K/W, ΔP = 1000 Pa, Q = 44.02 LPM) were computed on the 2 mm domain, not the 5 mm domain.

If the plan intends to fabricate a 5 mm specimen, all acceptance bands are anchored to predictions for a 2 mm specimen. R_th and ΔP scale non-linearly with domain size for TPMS geometries (different number of unit cells, different surface-area-to-volume ratio). The comparison is not invalid, but the validation plan does not acknowledge the mismatch.

### W-4. Contact resistance unmodeled (physics-performance)

Stage 5 solves conduction with perfect solid-fluid interface coupling. No thermal contact resistance is modeled between the heater face and the cold plate. In the bench test, heater-to-specimen contact resistance (even with thermal paste, typically 0.1–1.0 K·cm²/W) adds directly to measured R_th.

At the predicted R_th = 11.27 K/W for a 4 mm² heated area, even 0.5 K·cm²/W of contact resistance adds ~12.5 K/W — a 111% increase. The 2× acceptance band (0.5 to 2.0× predicted) would not accommodate this.

### W-5. Uncertainty budget covers only random instrument error (planning-quality)

Section 8.1 propagates TC, pressure, flow, and power uncertainties to ~1% on R_th and ~5% on ΔP. INSTRUMENTATION_AND_SENSORS.md Section 5 acknowledges systematic errors but states "Minimize systematically through insulation, consistent tap placement, and energy-balance closure checks" without quantifying them.

For a 5 mm cold plate at 25 W, the ratio of heated surface area to insulated surface area is small. Parasitic losses through fixture conduction, lead wires, and imperfect insulation could easily be 5–20% of applied power, biasing measured R_th upward by 5–20%. This dominates the ~1% instrument uncertainty and is not bounded in the acceptance criteria.

### W-6. Steady-state criterion under-specified (planning-quality)

"< 0.5 °C/min for 5 consecutive minutes" — applied to which channel? T_heater, T_out, T_in, or all? Not stated. For a small specimen at low power, T_in will stabilize almost instantly (chiller-controlled), but T_heater is the slow channel. The criterion should specify the controlling measurement.

---

## 3. MISSING

### M-1. Power-independence assumption not stated

The plan applies R_th = ΔT / P_elec and compares against simulation R_th computed at Q_total = 4 W. The bench test uses 25 W (nominal) with a sweep to 10 and 50 W. For the comparison to be valid, R_th must be independent of power in the tested range. This requires single-phase flow (no boiling), linear conduction, and negligible natural-convection effects. These conditions are likely met but the assumption is not stated or bounded (e.g., T_heater must stay below boiling at 50 W).

### M-2. Thermal interface material specification

No specification for how the heater is thermally coupled to the cold plate bottom face. Thermal paste, indium foil, solder, or dry contact? Each has different contact resistance. This is a first-order contributor to measured R_th (see W-4). Omission makes the test non-reproducible.

### M-3. Fixture loss calibration protocol

No protocol to measure parasitic heat losses before the actual cold plate test. Standard practice: run the heater at each power level with either (a) no specimen (air gap), or (b) a solid reference block of known thermal conductivity, and quantify fixture losses. Without this, the energy balance closure check (>90%) is the only guard against systematic loss, and it cannot separate fixture loss from measurement error.

### M-4. Ambient temperature recording

No requirement to record room ambient temperature during testing. Parasitic losses scale with (T_heater − T_ambient). A 5 °C shift in ambient changes parasitic loss by a significant fraction. Ambient should be logged alongside test data or at minimum recorded in the run summary.

### M-5. As-built geometry back-simulation

The plan records as-built CT dimensions and compares to design (< 30% deviation gate). But there is no plan to feed the as-built geometry back into the simulation for a corrected comparison. If the as-built porosity is 48% instead of 56%, the predicted R_th and ΔP change. Without this, a "fail" could be ambiguous: is it a model failure or a fabrication failure?

### M-6. Smoke-resolution acknowledgment

All Stage 4/5 predictions are from 20 × 20 × 20 smoke-resolution runs. The validation plan does not note this limitation or recommend running higher-resolution simulations before committing to fabrication and testing. A single 50 × 50 × 50 or 100 × 100 × 100 run on the actual 5 mm domain would provide better reference predictions at modest computational cost.

### M-7. Simulation reference schema omits heat input

DATA_SCHEMA_STAGE7.md Section 6 (simulation_reference) includes Stage 5 thermal_resistance_KW and peak_temperature_C but does not include heat_flux_w_m2 or total_power_w. Without the denominator of the R_th calculation, a future reader cannot verify dimensional consistency or detect the 4 W vs 25 W discrepancy.

### M-8. No Reynolds number or flow-regime context

Neither the validation plan nor the data schema records the Reynolds number regime of the flow simulation. The solver uses a Darcy model (creeping flow assumption). If the actual flow is inertial or turbulent (Re_pore > 10), Darcy underpredicts ΔP. The test matrix sweeps flow rate but has no plan to estimate Re from measured Q and effective pore size.

### M-9. Procedure for unreachable ΔP target

The test protocol says "adjust pump to achieve ΔP ≈ 1000 Pa." If the real permeability is much lower than modeled (which is likely, given W-2), achieving 1000 Pa may require micro-liters-per-minute flow rates — below the accuracy floor of the specified flow meter (±2% of reading at low end). No fallback procedure is defined.

### M-10. No go/no-go gate between CT and flow test

Pre-test CT (Phase A) checks geometry fidelity with a 30% deviation threshold. But the plan allows testing to proceed even if as-built features are below 0.5 mm (Section 8.4: "If as-built features fall below 0.5 mm in CT, this does not invalidate the test"). The immediate-fail bound (CT deviation > 50%) is defined separately. Between 30% and 50% deviation, the test proceeds but the comparison against simulation predictions for the nominal geometry is compromised. A clear decision tree is needed.

---

## 4. HIGH-RISK

### H-1. Flow-rate prediction will mislead procurement (physics-performance + planning-quality)

The 44.02 LPM prediction at 1000 Pa is a direct output of a Darcy solver with unrealistic permeability (k = 1e-6 m²). If this number is used to size a pump or flow meter, the equipment will be 2–4 orders of magnitude oversized. A pump capable of 100 LPM through a 5 mm porous specimen at 1000 Pa will either:

- Deliver negligible flow at low speed (below meter accuracy), or
- Destroy the specimen at high speed.

**Recommendation:** Before procurement, run a Hagen-Poiseuille or Ergun-equation estimate using the CT-measured channel diameter to bracket the realistic flow range. Size instrumentation to that range, not to the Darcy-solver output.

### H-2. Simulation domain ≠ fabrication domain (planning-quality)

All quantitative predictions in the plan (R_th = 11.27 K/W, ΔP = 1000 Pa, Q = 44.02 LPM) are computed on a 2 mm × 2 mm × 2 mm domain. The plan specifies fabricating a 5 mm × 5 mm × 5 mm specimen. Scaling from 2 mm to 5 mm changes:

- The number of TPMS unit cells in each direction (non-linear effect on effective permeability and conductivity).
- The heated surface area (6.25× increase → Q_total changes if flux is held constant).
- Edge effects relative to bulk behavior.

The acceptance bands (R_th: 0.5–2.0×, ΔP: 0.33–3.0×) are wide enough to possibly accommodate the domain mismatch, but this is accidental, not by design. If the team intends to fabricate at 5 mm, the simulation should be rerun at the fabrication domain size before testing. Alternatively, fabricate at 2 mm to match the simulation domain exactly (mechanically challenging but physically consistent).

### H-3. Zero manufacturing margin (physics-performance + planning-quality)

Minimum feature size = 0.5 mm exactly equals the manufacturability threshold = 0.5 mm. AM process variability (±0.05–0.10 mm per the plan's own estimate in Section 8.4) means roughly 50% of builds will contain sub-threshold features.

The plan acknowledges this (Section 3.4) and proposes using as-built dimensions in post-test analysis. This is pragmatic but introduces an unbounded variable into the simulation comparison: if the as-built geometry deviates 25% from design, the test cannot distinguish "model is wrong" from "specimen doesn't match the modeled geometry."

The only mitigation is M-5 (back-simulate on as-built geometry), which is currently missing.

---

## 5. Summary Table

| ID | Category | Type | Severity |
|----|----------|------|----------|
| W-1 | WEAK | planning-quality | Medium — factual misstatement, easy fix |
| W-2 | WEAK | physics-performance | High — affects procurement |
| W-3 | WEAK | planning-quality | High — invalidates acceptance bands |
| W-4 | WEAK | physics-performance | Medium — biases R_th comparison |
| W-5 | WEAK | planning-quality | Low — acknowledged but not quantified |
| W-6 | WEAK | planning-quality | Low — ambiguous criterion |
| M-1 | MISSING | planning-quality | Low — likely valid, just unstated |
| M-2 | MISSING | planning-quality | Medium — reproducibility gap |
| M-3 | MISSING | planning-quality | Medium — systematic error uncontrolled |
| M-4 | MISSING | planning-quality | Low — standard practice omission |
| M-5 | MISSING | planning-quality | High — needed for H-3 mitigation |
| M-6 | MISSING | planning-quality | Medium — smoke resolution not flagged |
| M-7 | MISSING | planning-quality | Low — schema gap |
| M-8 | MISSING | physics-performance | Medium — flow regime unknown |
| M-9 | MISSING | planning-quality | Medium — no fallback for unreachable target |
| M-10 | MISSING | planning-quality | Medium — ambiguous decision tree |
| H-1 | HIGH-RISK | physics + planning | Critical — equipment damage risk |
| H-2 | HIGH-RISK | planning-quality | Critical — predictions on wrong domain |
| H-3 | HIGH-RISK | physics + planning | High — zero margin, no back-simulation |

---

## 6. Recommended Priority Actions (Not Rewrites)

These are not document rewrites. They are actions that should be completed before any procurement or fabrication is initiated.

1. **Re-run Stage 4/5 simulation on the fabrication-target domain** (5 mm if that is the intent, or explicitly downscope to 2 mm). Update simulation_reference accordingly.
2. **Add heat_flux_w_m2 and total_power_w to the simulation reference schema** (DATA_SCHEMA_STAGE7.md Section 6). One-line addition.
3. **Compute a Hagen-Poiseuille or Ergun-equation flow estimate** from the actual channel geometry (from Stage 3 distance transform or CT data) to bound the realistic flow range. Use this for instrument procurement, not the Darcy-solver output.
4. **Specify the thermal interface material** and add contact-resistance estimate to the uncertainty budget.
5. **Add a fixture-loss calibration run** to Phase A (before Phase B).
6. **Specify which temperature channel controls the steady-state criterion.**
7. **Define a CT go/no-go decision tree** for deviations between 30% and 50%.

---

## 7. Provenance Sufficiency for Stage 8

The provenance chain defined in ARTIFACT_LAYOUT.md (Section 4) is adequate for Stage 8 handoff **if** the following are true:

- The simulation reference snapshot is populated with corrected domain-size and power values (currently wrong per W-3).
- Fabrication batch IDs and CT scan IDs are actually recorded (currently "NOT PROCURED" / "NOT STARTED").
- The pipeline_git_sha.txt reflects the commit used for the prediction that the test compares against (not the latest HEAD at test time).

The schema supports the traceability; the risk is execution fidelity, not schema design.

---

**End of audit memo.**
