# Stage 7 Benchtop Validation Plan

**Document ID:** STAGE7-BVP-001  
**Date:** 2026-03-06  
**Status:** PROPOSED — RECONCILED PER AUDIT MEMO STAGE7-AUD-001  
**Author:** Validation Planning Engineer  

> **Reconciliation note (STAGE7-AUD-001, 2026-03-06):** This document has been
> updated to correct three factual mismatches identified in the audit:
> (1) the Stage 5 simulation heat input is 4 W, not 25 W;
> (2) all Stage 4/5 predictions were computed on a 2 mm × 2 mm × 2 mm domain,
> not the 5 mm × 5 mm × 5 mm fabrication target;
> (3) the Stage 4 predicted flow rate of 44.02 LPM is non-physical and must not
> be used to size instrumentation or pump equipment.
> Acknowledged unknowns and missing assumptions have been added to Section 11.

---

## 1. Objective

Determine whether the software-screened TPMS coldplate candidate produces physically measurable thermal and hydraulic behavior that is directionally consistent with the analytical simulation pipeline (Stages 1–6).

Stage 7 is **not** a product qualification test. It is a model-validation gate: does the simulation framework predict trends correctly enough to justify continued refinement?

---

## 2. Hypothesis Under Test

**H₀ (null):** The analytical simulation pipeline (Stages 4–5) does not predict the direction of thermal-hydraulic performance for diamond TPMS coldplate geometry fabricated via metal additive manufacturing. Measured thermal resistance and pressure drop deviate from predictions by more than the acceptance bands defined in Section 7.

**H₁ (alternative):** Measured thermal resistance and pressure drop fall within the directional-agreement bands, confirming the simulation pipeline captures the governing physics well enough to guide design iteration.

**What this does NOT test:**

- Quantitative accuracy sufficient for certification
- Long-term reliability or fatigue life
- Production-readiness of the geometry or process
- Whether this candidate is the optimal design

---

## 3. Candidate Selection

### 3.1 Primary Candidate

**candidate_02_diamond_2d_s1045**

| Property | Value | Source | Label |
|----------|-------|--------|-------|
| Family | diamond TPMS (2D-promoted) | Stage 3 | IMPLEMENTED |
| Voxel size | 0.25 mm | Stage 3 config | IMPLEMENTED |
| Resolution | 20 × 20 × 20 | Stage 3 config | IMPLEMENTED |
| Fabrication domain target | 5.0 × 5.0 × 5.0 mm | Stage 3 remediated config | IMPLEMENTED |
| Simulation domain (actual) | 2.0 × 2.0 × 2.0 mm | Stage 4/5 results (domain_volume_mm3 = 8.0) | **MISMATCH — see note below** |
| Porosity | 56.3% | Stage 3 measured | IMPLEMENTED |
| Min wall thickness | 0.5 mm | Stage 6 measured | IMPLEMENTED |
| Min feature size | 0.5 mm | Stage 6 measured | IMPLEMENTED |
| Thermal resistance | 11.27 K/W | Stage 5 simulated on **2 mm domain** | SIMULATED |
| Pressure drop | 1000 Pa | Stage 4 matched condition on **2 mm domain** | SIMULATED |
| Flow rate | 44.02 LPM | Stage 4 Darcy solver — **non-physical, see Section 11** | FLOW_SIMULATED |
| Combined stress | 55.70 MPa (allowable: 92.0 MPa) | Stage 6 screened | STRUCTURAL_SCREENED |
| Manufacturability | Pass (0.5 mm features) | Stage 6 screened | MANUFACTURABILITY_SCREENED |

> **Domain mismatch (audit finding W-3 / H-2):** The Stage 3 remediated configuration
> targets a 5.0 × 5.0 × 5.0 mm domain (0.25 mm voxel × 20 resolution).  However, all
> Stage 4 and Stage 5 simulation results in the repository were computed on a
> 2.0 × 2.0 × 2.0 mm domain (0.1 mm voxel × 20 resolution; domain_volume_mm3 = 8.0 in
> thermal_metrics.json and metrics.json).  The simulation predictions for R_th, ΔP, and
> Q listed in this table are therefore not directly representative of the 5 mm fabrication
> target.  Acceptance bands are wide enough to allow for this mismatch, but the mismatch
> is not by design.  Before fabrication, the simulation should be rerun on the 5 mm domain,
> or the fabrication target should be revised to 2 mm to match the computed predictions.
> This comparison is logged as a known limitation, not a test-invaliding fault.

### 3.2 Selection Rationale

candidate_02 is selected because:

1. It passes both structural and manufacturability screening (Stage 6).
2. It has marginally better hydraulic resistance (1,362,912 vs 1,395,536 Pa·s/m³).
3. It has marginally higher porosity (56.3% vs 55.7%), reducing solid mass.
4. Thermal resistance is functionally identical between candidates (~11.27 K/W).

### 3.3 Backup Candidate

**candidate_01_diamond_2d_s1127** — same geometry family, same screening outcome, slightly lower flow rate. Available if primary candidate fabrication fails.

### 3.4 Margin Note

Both candidates pass manufacturability at the exact threshold (0.5 mm measured = 0.5 mm required). This is a tight margin. The validation plan accounts for the possibility that AM fabrication introduces sub-threshold features due to process variability (powder size distribution, laser spot size, thermal distortion). See Section 8.

---

## 4. Software-Screened Readiness vs Physical Validation vs Product Readiness

| Category | Definition | Current status |
|----------|-----------|----------------|
| **Software-screened readiness** | Candidate passes all analytical checks (structural, manufacturability, thermal, flow) using simplified models and literature properties. No physical testing. | **ACHIEVED** — 2/2 candidates pass Stage 6. IMPLEMENTED. |
| **Physical validation** | Fabricated prototype tested on bench. Measured R_th and ΔP compared against predictions. Directional agreement confirmed or refuted. | **NOT STARTED** — this plan addresses it. PROPOSED. |
| **Product readiness** | Full-fidelity simulation (CFD/FEA), multi-lot fabrication repeatability, reliability testing, system integration. Meets production specifications. | **NOT IN SCOPE** for Stage 7. |

---

## 5. Test Setup Assumptions

### 5.1 Fabrication

| Parameter | Assumption | Basis |
|-----------|-----------|-------|
| Process | Metal L-PBF (SLM/DMLS) | Standard for Al 6061 lattice structures |
| Material | Aluminum 6061-T6 | Stage 6 material model |
| Build orientation | TBD by vendor | Depends on support strategy for internal channels |
| Post-processing | Support removal, stress relief (T6 temper), bead blast | Standard AM post-processing |
| Feature resolution | Must resolve 0.5 mm wall/channel | Threshold from Stage 6 screening |
| Powder evacuation | Required — 56% porosity, interconnected | Design review with vendor pre-print |
| CT inspection | Pre-test, mandatory | Verify internal geometry fidelity |

**CRITICAL:** AM vendor must confirm capability to print 0.5 mm features in Al 6061. If not achievable, the plan halts until either a capable vendor is found or geometry is regenerated at coarser features (e.g., voxel_size = 0.35 mm → 0.7 mm minimum).

### 5.2 Test Fixture

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| Housing | Machined Al or acetal block, sealed inlet/outlet | Seals around 5 mm × 5 mm footprint |
| Heater | Thin-film or cartridge, 25 W nominal | Bottom face of cold plate |
| Thermal interface | **Specify before build:** thermal paste (record type and lot) or indium foil (record thickness). Dry contact is not acceptable. Contact resistance estimate must be added to uncertainty budget (see Section 11). | Omitting TIM specification makes the test non-reproducible. |
| Insulation | Aerogel or ceramic fiber, non-wetted faces | Minimize parasitic heat loss |
| Sealing | O-ring or gasket compression | No adhesives in flow path |
| Mounting | Bolted clamp, controlled torque | Prevent over-compression of porous core |

### 5.3 Coolant Loop

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| Fluid | Deionized water | Matches Stage 4/5 assumption |
| Inlet temperature | 25 ± 1 °C | Chiller-controlled |
| Flow control | Variable-speed pump or needle valve | Must achieve target ΔP |
| Degassing | Passive reservoir with bleed valve | Minimize air entrainment |
| Filtration | 10 µm inline filter | Protect porous core from particulate |

### 5.4 Thermal Load

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| Nominal power | 25 W | Bench test power. **Not the Stage 5 boundary condition** — see note below. |
| Power sweep | 10, 25, 50 W | Extended matrix only |
| Application | Uniform, bottom face | Matches Stage 5 boundary geometry |
| Control | Closed-loop power supply, power-meter feedback | ±1% accuracy |

> **Power mismatch (audit finding W-1 / M-1):** Stage 5 applied a heat flux of
> 1 MW/m² to the bottom face of a 2 mm × 2 mm domain (4 mm² heated area), giving
> total heat input Q_total = 4.0 W (recorded as `heat_input_w: 4.0` in
> thermal_metrics.json).  The bench nominal power of 25 W is **not** the Stage 5
> boundary condition.  The R_th comparison is valid only under the power-independence
> assumption: R_th = ΔT / P is constant with respect to P when the system operates
> in single-phase, linear conduction with negligible natural convection.  This
> assumption is likely satisfied at 10–50 W through a small Al specimen with forced
> water cooling, but it is not bounded in the simulation and must be checked
> experimentally (Phase C power sweep).  T_heater must remain below 95 °C at 50 W
> to rule out nucleate boiling.  The power-independence assumption must be stated
> explicitly in any report comparing bench R_th to the simulated 11.27 K/W value.

---

## 6. Measurements to Collect

### 6.1 Primary Measurements (Required)

| Measurement | Instrument | Location | Rate | Units |
|-------------|-----------|----------|------|-------|
| Inlet temperature (T_in) | Type-T thermocouple | 5D upstream of test section | 1 Hz | °C |
| Outlet temperature (T_out) | Type-T thermocouple | 10D downstream of test section | 1 Hz | °C |
| Heater surface temp (T_heater) | Type-T thermocouple, embedded | Center of heater face | 1 Hz | °C |
| Top surface temp (T_top) | Type-T thermocouple | Center of top face | 1 Hz | °C |
| Inlet pressure (P_in) | Pressure transducer | Co-located with T_in tap | 1 Hz | Pa |
| Outlet pressure (P_out) | Pressure transducer | Co-located with T_out tap | 1 Hz | Pa |
| Flow rate (Q) | Turbine or ultrasonic flow meter | Downstream of test section | 1 Hz | LPM |
| Heater power (P_elec) | Power meter (V × I) | Heater supply circuit | 1 Hz | W |
| Ambient temperature (T_amb) | Type-T thermocouple or thermistor | 0.5 m from test section, free air | Per run (record at start/end) | °C |

### 6.2 Derived Quantities

| Quantity | Formula | Predicted value | Units |
|----------|---------|----------------|-------|
| Pressure drop | ΔP = P_in − P_out | 1000 Pa | Pa |
| Thermal resistance | R_th = (T_heater − T_in) / P_elec | 11.27 K/W (**from 2 mm domain**) | K/W |
| Hydraulic resistance | R_hyd = ΔP / Q | 1,362,912 Pa·s/m³ (**from 2 mm domain**) | Pa·s/m³ |
| Energy balance | η = (T_out − T_in) × ṁ × c_p / P_elec | ~1.0 | — |

### 6.3 Pre-Test Measurements (Mandatory)

| Measurement | Method | Purpose |
|-------------|--------|---------|
| CT scan | X-ray micro-CT, ≤ 50 µm resolution | Verify internal geometry vs design |
| Mass | Precision balance (±0.01 g) | Cross-check porosity |
| External dimensions | Caliper (±0.01 mm) | Verify bounding box |
| Powder evacuation check | Mass before/after cleaning | Confirm no trapped powder |

---

## 7. Pass/Fail Criteria

### 7.1 Primary (Must Pass)

| Criterion | Acceptable range | Rationale |
|-----------|-----------------|-----------|
| R_th ratio (measured / predicted) | 0.5 to 2.0 | Analytical model: simplified conduction + permeability, no contact resistance, no entrance effects |
| ΔP ratio (measured / predicted) | 0.33 to 3.0 | Permeability model is first-order; no entrance/exit losses, no surface roughness |
| Structural integrity | No leaks at operating conditions for full test duration | Binary |
| Geometry fidelity | CT scan: < 30% deviation in wall/channel dimensions | AM process variability |

### 7.2 Secondary (Informational)

| Criterion | Target | Notes |
|-----------|--------|-------|
| Q ratio (measured / predicted) | **NOT USED FOR PASS/FAIL** | The Stage 4 predicted Q = 44.02 LPM implies a mean fluid velocity of ~183 m/s through the 4 mm² cross-section — non-physical for water at 1000 Pa. This prediction is an artifact of Darcy permeability k = 1e-6 m² assigned to fluid voxels in the solver, not a calibrated physical quantity. Real bench flow rates through this geometry at 1000 Pa are expected to be orders of magnitude lower (likely mL/min range). Do not use the 44 LPM prediction to size equipment or set pass/fail bounds. Measure actual Q on the bench and report as MEASURED. |
| Energy balance closure | > 90% | Measurement system integrity check |
| Temperature uniformity | Qualitative comparison to simulation | No hard pass/fail |
| Repeat-to-repeat CV | < 10% across 3 repeats | Measurement confidence |

### 7.3 Immediate-Stop Criteria

| Condition | Action |
|-----------|--------|
| Leak | Stop. Inspect. Root-cause (seal vs AM defect). |
| R_th ratio > 3.0 | Fail. Investigate blockage, fabrication defect, model breakdown. |
| ΔP ratio > 5.0 | Fail. Investigate flow restriction, powder entrapment, model error. |
| CT deviation > 50% | Do not proceed to flow test. Process not suitable. |

---

## 8. Error Bars, Repeat Count, and Replication Guidance

### 8.1 Measurement Uncertainty Budget

| Source | Estimated uncertainty | Propagated to R_th | Propagated to ΔP |
|--------|----------------------|--------------------|--------------------|
| Thermocouple (T) | ±0.5 °C | ±0.028 K/W (~0.25%)¹ | — |
| Pressure transducer | ±0.5% FS (±25 Pa at 5 kPa range) | — | ±50 Pa (~5% of 1000 Pa) |
| Flow meter | ±2% reading | — | — |
| Power meter | ±1% reading | ±0.11 K/W (~1%)² | — |
| Combined (RSS) | — | ~±1.0% | ~±5.1% |

¹ R_th = (T_heater − T_in) / P_elec. Two TCs in numerator: δR_th = √(2) × 0.5 / P_elec. At P_elec = 25 W: δR_th = 0.028 K/W. As fraction of predicted R_th = 11.27 K/W: 0.25%.  
² δR_th / R_th = δP_elec / P_elec = 1%.

### 8.2 Repeat Count

| Condition | Repeats | Justification |
|-----------|---------|---------------|
| Nominal (25 W, target ΔP) | 3 minimum, 5 preferred | Mean ± 2σ confidence |
| Power sweep (10, 50 W) | 2 each | Trend validation only |
| Flow sweep (3 rates) | 2 each | Trend validation only |

### 8.3 Replication Guidance

- **Within-sample:** 3–5 repeats, same specimen, same day. Reports measurement system variability.
- **Between-sample:** If budget permits, fabricate 2 specimens from same build. Reports AM process variability.
- **Steady-state criterion:** Temperature drift < 0.5 °C/min for 5 consecutive minutes, evaluated on **T_heater** (the slowest-stabilizing channel). T_in is chiller-controlled and will stabilize rapidly; T_heater is the controlling measurement.
- **Warmup:** Discard first 5 minutes. Record subsequent 10 minutes.
- **Outlier handling:** Flag if > 3σ from group mean. Report all data; do not discard.

### 8.4 Fabrication Variability Risk

0.5 mm features sit at the exact manufacturability threshold. Expected AM variability:

| Dimension | Expected tolerance |
|-----------|--------------------|
| Wall thickness | ±0.05–0.10 mm |
| Channel diameter | ±0.10–0.15 mm |
| Porosity | ±2–5% from nominal |

If as-built features fall below 0.5 mm in CT, this does not invalidate the test. Record as-built dimensions and use them in post-test analysis as the effective geometry.

---

## 9. Coolant, Thermal Load, and Pressure-Drop Measurement Plan

### 9.1 Coolant Specification

| Property | Value | Source |
|----------|-------|--------|
| Fluid | Deionized water | Stage 4/5 assumption |
| Density | 998 kg/m³ at 25 °C | NIST |
| Viscosity | 0.890 × 10⁻³ Pa·s at 25 °C | NIST |
| Specific heat | 4182 J/(kg·K) at 25 °C | NIST |
| Inlet temperature | 25 ± 1 °C | Chiller-controlled |

### 9.2 Thermal Load Protocol

**Step 0 (Fixture-loss calibration — required before Phase B):**

Run the heater at each intended power level (10, 25, 50 W) with a solid reference block of known thermal conductivity (e.g., machined Al 6061 billet) or with the test section inlet and outlet blocked (air-gap condition). Record steady-state T_heater, T_ambient, and P_elec. Compute parasitic fixture loss as P_fixture = P_elec − P_fluid_absorbed. If fixture loss exceeds 10% at any power level, improve insulation before proceeding to Phase B. Record fixture-loss correction factors for use in post-test analysis.

**Steps 1–6 (each test point):**

1. Set chiller to 25 °C. Circulate until stable (< 0.2 °C drift / 5 min).
2. Set pump to target flow rate (measured, not set-point).
3. Enable heater at target power. Wait for steady state (< 0.5 °C/min on T_heater).
4. Record data for 10 minutes at 1 Hz.
5. Power off. Cool to within 1 °C of inlet.
6. Repeat for each test point.

### 9.3 Pressure-Drop Measurement

- Taps ≥ 5D upstream, ≥ 10D downstream of test section.
- Zero-check transducers before each session (no flow, valves open).
- Record differential pressure at each steady-state condition.
- Verify with calibration orifice at start of each test day.

### 9.4 Flow-Rate Measurement

- Meter downstream of test section.
- Verify against timed volumetric collection (bucket test) at campaign start.
- Record at each steady-state condition.

> **Flow meter procurement warning (audit finding W-2 / H-1):** The Stage 4 predicted
> Q = 44.02 LPM is non-physical (mean fluid velocity ~183 m/s at 1000 Pa through a 4 mm²
> cross-section — a Darcy solver artifact, not a physical prediction).  Do not use this
> value to specify the flow meter range or pump capacity.  Before procuring instruments,
> derive a physics-based flow-rate estimate using the Hagen-Poiseuille or Ergun equation
> with the effective channel diameter from Stage 3 geometry or CT scan.  Size the flow
> meter to the resulting range.  If the pre-CT estimate suggests flow rates below the
> accuracy floor of any candidate meter, consult with an instrumentation engineer before
> proceeding.

### 9.5 CT Decision Tree (Pre-Test Gate)

After Phase A CT scan (test A-01), apply the following go/no-go logic before proceeding to Phase B:

| CT deviation from design | Action |
|--------------------------|--------|
| < 30% on all critical dimensions | Proceed to Phase B. Record as-built dimensions. |
| 30%–50% on any critical dimension | Conditional proceed. Document deviation. Rerun Stage 4/5 simulation on as-built geometry before comparing bench results to predictions. Note in campaign summary that nominal-geometry predictions are not directly applicable. |
| > 50% on any critical dimension | Do not proceed. Process not suitable for this geometry. Halt. |

> Critical dimensions are: minimum wall thickness, mean channel diameter, and bulk porosity.
> "Deviation" is defined as |as-built − design| / design × 100%.

---

## 10. Should Camber Be Used Here?

**Narrow answer: No, not at this stage.**

Camber adds value when:

1. Multiple parallel test campaigns require coordinated artifact tracking, OR
2. The data schema is complex enough that manual tracking risks reproducibility.

At Stage 7, the scope is small: 1 candidate, ~15 test points, 3–5 repeats each. Artifact flow is linear: one geometry → one fabricated part → one test campaign → one dataset. DATA_SCHEMA_STAGE7.md and ARTIFACT_LAYOUT.md define the naming and provenance chain. Manual compliance is sufficient.

**When Camber becomes useful:**

- Stage 8+ with multiple candidates, multi-lot fabrication, reliability campaigns.
- Team scales beyond 2–3 people handling test data.
- Automated pipeline re-runs triggering downstream updates.

**Decision: DEFER.** Revisit at Stage 8 planning.

---

## 11. Limitations and Caveats

The following limitations are known prior to testing. They do not invalidate the Stage 7 objective (directional agreement check), but must be stated in any report comparing bench results to simulation predictions.

### 11.1 Simulation-Conditioned Expectations

1. **Simulation fidelity:** Stages 4/5 use analytical permeability and simplified thermal models. Agreement within 2–3× is the goal, not ±10%.
2. **Single geometry family:** Both candidates are diamond TPMS. Stage 7 tests the simulation pipeline, not whether diamond is optimal.
3. **Smoke resolution:** All Stage 4/5 predictions were computed at 20 × 20 × 20 voxels (smoke-resolution run). This is a coarse discretization. Results indicate qualitative trends only. Higher-resolution simulations (50 × 50 × 50 or 100 × 100 × 100) on the actual 5 mm domain are recommended before committing to additional fabrication.
4. **Domain mismatch:** All quantitative predictions (R_th = 11.27 K/W, ΔP = 1000 Pa) were computed on a **2 mm × 2 mm × 2 mm** domain. The fabrication target is **5 mm × 5 mm × 5 mm**. Scaling from 2 mm to 5 mm changes the number of TPMS unit cells, the effective surface-area-to-volume ratio, and edge-effect contributions. The acceptance bands accommodate this uncertainty by design, but the mismatch is not by design. Report this fact explicitly in the Stage 7 verdict.
5. **Flow-rate prediction non-physicality:** The Stage 4 predicted Q = 44.02 LPM (v_mean ≈ 183 m/s at 1000 Pa) is an artifact of Darcy permeability k = 1e-6 m² assigned to fluid voxels. This is not a physical flow-rate prediction. Real bench flow rates through this geometry will be orders of magnitude lower. The flow meter range must be sized from a physics-based estimate, not from Stage 4 output.
6. **Power-independence assumption:** The R_th comparison is valid only if thermal resistance is independent of applied power (single-phase forced convection, no boiling, linear conduction). This is expected to hold at 10–50 W with forced water cooling, but must be confirmed from Phase C (power sweep). If R_th varies by more than 20% across the sweep, the linear model is inadequate and a power-dependent correction must be applied.

### 11.2 Bench-Test Requirements (Unknowns Requiring Physical Validation)

7. **Contact resistance uncertainty:** Stage 5 models perfect solid-fluid coupling with no contact resistance at the heater-specimen interface. Measured R_th includes heater-to-specimen contact resistance (typical: 0.1–1.0 K·cm²/W for thermal paste; higher for dry contact). At the predicted R_th = 11.27 K/W for a 4 mm² heated area, even 0.5 K·cm²/W contact resistance adds ~12.5 K/W — a ~111% increase. The 2× acceptance band accounts for this uncertainty, but contact resistance must be reported in the test record (TIM type, thickness, application method).
8. **Thermal interface material specification:** The thermal interface material between the heater and the specimen bottom face must be specified before the first test and held constant across all runs. Acceptable options: thermal paste (record manufacturer, grade, and lot number), indium foil (record thickness), or solder. Dry contact is not acceptable. This specification is required for reproducibility.
9. **Fixture-loss calibration:** Parasitic heat losses through fixture conduction, lead wires, and imperfect insulation can be 5–20% of applied power for small specimens at 25 W. The fixture-loss calibration run (Section 9.2, Step 0) must be completed before Phase B. Without this, a measured R_th that is higher than predicted cannot be attributed unambiguously to model error vs. fixture loss.
10. **Small domain — edge effects:** The 5 mm × 5 mm × 5 mm specimen is a single TPMS unit cell. Flow distribution and thermal behavior at the fixture boundaries may dominate over the bulk TPMS performance. Account for this in post-test analysis.
11. **Material properties:** Stage 6 uses literature Al 6061-T6 values. As-built AM properties may differ (lower ductility, anisotropy, surface roughness effects on heat transfer). Acceptable for Stage 7 but must be revisited for product readiness.
12. **Reynolds number and flow regime:** The Stage 4 solver uses Darcy's law, which assumes creeping (viscous-dominated) flow. If the actual bench flow produces pore Reynolds numbers Re_pore > 10 (inertial regime), Darcy's law underpredicts ΔP. During bench testing, estimate Re_pore = ρ v d / μ from measured Q, CT-derived channel diameter, and water properties. Report the flow regime in the campaign summary.
13. **No manufacturing margin:** Both candidates pass manufacturability at the exact threshold of 0.5 mm (measured = required). Expected AM process variability of ±0.05–0.10 mm means a fraction of builds will produce sub-threshold features. CT scan (Phase A) is the gate. If as-built features deviate 30–50% from design, back-simulate on the as-built geometry before interpreting test results (see Section 9.5 CT decision tree).

### 11.3 Unknowns Requiring Physical Validation

These are open items that cannot be resolved from the current simulation or design data:

- Actual bench flow rate through the 5 mm specimen at 1000 Pa (expected: orders of magnitude below 44 LPM).
- Contact resistance with the specified TIM under the specified clamping torque.
- Fixture parasitic heat loss at each power level.
- As-built porosity and feature sizes from CT scan.
- Reynolds number regime at actual bench flow rates.

---

## 12. Document Status

| Item | Status |
|------|--------|
| Software screening (Stages 3–6) | IMPLEMENTED — 2/2 pass, measured |
| This validation plan | PROPOSED |
| Fabrication | NOT STARTED |
| Test execution | NOT STARTED |
| Data analysis | NOT STARTED |

---

**End of document.**
