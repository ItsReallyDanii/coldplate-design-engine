# Stage 7 Benchtop Validation Plan

**Document ID:** STAGE7-BVP-001  
**Date:** 2026-03-06  
**Status:** PROPOSED  
**Author:** Validation Planning Engineer  

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
| Domain | 5.0 × 5.0 × 5.0 mm | Stage 3 config | IMPLEMENTED |
| Porosity | 56.3% | Stage 3 measured | IMPLEMENTED |
| Min wall thickness | 0.5 mm | Stage 6 measured | IMPLEMENTED |
| Min feature size | 0.5 mm | Stage 6 measured | IMPLEMENTED |
| Thermal resistance | 11.27 K/W | Stage 5 simulated | SIMULATED |
| Pressure drop | 1000 Pa | Stage 4 matched condition | SIMULATED |
| Flow rate | 44.02 LPM | Stage 4 simulated | FLOW_SIMULATED |
| Combined stress | 55.70 MPa (allowable: 92.0 MPa) | Stage 6 screened | STRUCTURAL_SCREENED |
| Manufacturability | Pass (0.5 mm features) | Stage 6 screened | MANUFACTURABILITY_SCREENED |

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
| Nominal power | 25 W | Matches Stage 5 boundary condition |
| Power sweep | 10, 25, 50 W | Extended matrix only |
| Application | Uniform, bottom face | Matches Stage 5 boundary condition |
| Control | Closed-loop power supply, power-meter feedback | ±1% accuracy |

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

### 6.2 Derived Quantities

| Quantity | Formula | Predicted value | Units |
|----------|---------|----------------|-------|
| Pressure drop | ΔP = P_in − P_out | 1000 Pa | Pa |
| Thermal resistance | R_th = (T_heater − T_in) / P_elec | 11.27 K/W | K/W |
| Hydraulic resistance | R_hyd = ΔP / Q | 1,362,912 Pa·s/m³ | Pa·s/m³ |
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
| Q ratio (measured / predicted) | 0.5 to 2.0 | Derived from ΔP at controlled conditions |
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
| Thermocouple (T) | ±0.5 °C | ±0.04 K/W (~0.4%) | — |
| Pressure transducer | ±0.5% FS (±25 Pa at 5 kPa range) | — | ±50 Pa (~5%) |
| Flow meter | ±2% reading | — | — |
| Power meter | ±1% reading | ±0.11 K/W (~1%) | — |
| Combined (RSS) | — | ~±1.1% | ~±5.1% |

### 8.2 Repeat Count

| Condition | Repeats | Justification |
|-----------|---------|---------------|
| Nominal (25 W, target ΔP) | 3 minimum, 5 preferred | Mean ± 2σ confidence |
| Power sweep (10, 50 W) | 2 each | Trend validation only |
| Flow sweep (3 rates) | 2 each | Trend validation only |

### 8.3 Replication Guidance

- **Within-sample:** 3–5 repeats, same specimen, same day. Reports measurement system variability.
- **Between-sample:** If budget permits, fabricate 2 specimens from same build. Reports AM process variability.
- **Steady-state criterion:** Temperature drift < 0.5 °C/min for 5 consecutive minutes.
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

1. Set chiller to 25 °C. Circulate until stable (< 0.2 °C drift / 5 min).
2. Set pump to target flow rate (measured, not set-point).
3. Enable heater at target power. Wait for steady state (< 0.5 °C/min).
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

1. **Simulation fidelity:** Stages 4/5 use analytical permeability and simplified thermal models. Agreement within 2–3× is the goal, not ±10%.
2. **Single geometry family:** Both candidates are diamond TPMS. Stage 7 tests the simulation pipeline, not whether diamond is optimal.
3. **Smoke resolution:** 20 × 20 × 20 is coarse. Results inform whether higher-resolution runs are worth pursuing.
4. **Small domain:** 5 mm × 5 mm × 5 mm is a unit cell. Edge effects in the test fixture may dominate. Account for this in analysis.
5. **Material properties:** Stage 6 uses literature Al 6061-T6 values. As-built AM properties may differ (lower ductility, anisotropy). Acceptable for Stage 7 but must be revisited for product readiness.

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
