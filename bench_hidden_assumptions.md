# bench_hidden_assumptions.md — Hidden Assumptions and Failure Modes

**Date:** 2026-03-30  
**Role:** Skeptical Reviewer  
**Evidence standard:** Per AGENT_MISSION.md  

---

## 1. Hidden Assumptions (by category)

### Simulation-to-bench boundary condition mismatch

| # | Assumption | Severity | Likelihood |
|---|-----------|----------|------------|
| H-1 | Simulation domain is 2 mm; fabrication domain is 5 mm. R_th and ΔP scale non-linearly with domain size. | **HIGH** | **CERTAIN** — documented in SIMREF |
| H-2 | Simulation heat input is 4 W (1 MW/m² on 4 mm²); test plan says 25 W. R_th linearity across this range is assumed but not verified. | **MEDIUM** | **HIGH** |
| H-3 | Simulation imposes 1000 Pa as a boundary condition, not as a prediction. The test will measure ΔP, not impose it. These are different experiments. | **MEDIUM** | **CERTAIN** |
| H-4 | Inlet boundary in simulation is a full-face pressure condition. Real specimen has 3 mm bore ports (partial face). Flow distribution will differ. | **MEDIUM** | **HIGH** |

### Fabrication / print fidelity

| # | Assumption | Severity | Likelihood |
|---|-----------|----------|------------|
| F-1 | Feature sizes at 0.5 mm are exactly at the AM manufacturability limit. Any print variability could close channels. | **HIGH** | **MEDIUM** |
| F-2 | LPBF aluminum surface roughness (Ra 10–30 µm) is unmodeled. On 0.5 mm channels, roughness is 2–6% of channel diameter. | **MEDIUM** | **HIGH** |
| F-3 | No powder evacuation holes are explicitly designed in the TPMS geometry. Port bores may not access all internal voids. | **HIGH** | **MEDIUM** |
| F-4 | Build orientation is unspecified. TPMS overhang behavior varies dramatically with orientation. | **MEDIUM** | **MEDIUM** |

### Roughness and blockage effects

| # | Assumption | Severity | Likelihood |
|---|-----------|----------|------------|
| R-1 | Simulation uses smooth-wall Darcy permeability (k=10⁻⁶ m²). Real channels have roughness that increases effective resistance. | **HIGH** | **CERTAIN** |
| R-2 | Partially sintered particles on channel walls reduce effective channel diameter by 0.05–0.15 mm. On 0.5 mm channels, this is 10–30% blockage. | **HIGH** | **HIGH** |

### Contact resistance / thermal interface

| # | Assumption | Severity | Likelihood |
|---|-----------|----------|------------|
| C-1 | Simulation assumes perfect thermal contact between heater and cold plate (zero interface resistance). Real interfaces have R_contact = 5–50+ K·mm²/W. | **HIGH** | **CERTAIN** |
| C-2 | On a 25 mm² heater face, even R_contact = 20 K·mm²/W gives 0.8 K/W additional resistance — 7% of the simulated 11.27 K/W. At higher contact resistance, this becomes significant. | **MEDIUM** | **HIGH** |

### Flow conditioning / pump curve mismatch

| # | Assumption | Severity | Likelihood |
|---|-----------|----------|------------|
| P-1 | Stage 4 predicts 44 LPM flow rate. Real flow will be 0.01–1 LPM. Any equipment sized to the simulation spec will have inadequate resolution at actual conditions. | **HIGH** | **CERTAIN** — documented in SIMREF |
| P-2 | At very low flow rates (< 0.1 LPM), flow may be in the laminar-to-transitional regime inside TPMS channels. Stage 4 Darcy model does not account for Reynolds-number-dependent permeability. | **MEDIUM** | **HIGH** |

### Instrumentation and calibration error

| # | Assumption | Severity | Likelihood |
|---|-----------|----------|------------|
| I-1 | At 4 W heat load and ~11 K/W R_th, the temperature rise is ~44 °C. This is well above thermocouple accuracy (±0.5 °C). Signal-to-noise is adequate. | **LOW** | LOW |
| I-2 | ΔP at very low flow rates through a 5 mm TPMS cube may be 1–100 Pa, which requires a sensitive transducer. A 0–10 kPa transducer at ±0.5% FS has ±50 Pa uncertainty — marginal for low-ΔP conditions. | **MEDIUM** | **MEDIUM** |

### Candidate-selection bias

| # | Assumption | Severity | Likelihood |
|---|-----------|----------|------------|
| S-1 | Both candidates are from the same family (diamond_2d) and differ by < 1% in R_th. Testing one candidate validates one geometry, not the pipeline's ability to discriminate between designs. | **HIGH** | **CERTAIN** |
| S-2 | No baseline geometry (e.g., straight channels) is planned for bench testing. Without a baseline, a "pass" proves the geometry works, not that the pipeline selects better geometries. | **HIGH** | **CERTAIN** |

### Synthetic-versus-real geometry contamination

| # | Assumption | Severity | Likelihood |
|---|-----------|----------|------------|
| G-1 | The remediated pipeline (0.25 mm voxels, 20³) has been configured but the geometry files are not currently on disk. The locked SIMREF references a specific git SHA (800bba1d). If the pipeline is re-run, the new geometry may differ from the original due to floating-point or random-seed differences. | **MEDIUM** | **MEDIUM** |
| G-2 | The original Stage 4/5 "full" results in the repo were run with 50³ resolution (0.1 mm voxels), but the Stage 6 remediation changed to 20³ (0.25 mm voxels). The locked SIMREF uses the remediated values. However, the earlier R_th ≈ 1.03 K/W predictions from Stage 5 remain in the comparison.json and README, creating a confusing dual-truth in the repo. | **HIGH** | **CERTAIN** |

---

## 2. Failure Interpretation Matrix

| Mismatch scenario | Model inadequacy | Fabrication artifact | Test-rig issue | Instrumentation issue | Ambiguous cause |
|-------------------|-----------------|---------------------|----------------|----------------------|-----------------|
| R_th 2–5× sim | ✓ Likely (domain mismatch, convection model) | △ Possible (partial blockage) | △ Possible (contact resistance) | ✗ Unlikely | |
| R_th 5–10× sim | ✓ Likely | ✓ Likely (roughness, partial blockage) | △ Possible | ✗ Unlikely | |
| R_th > 10× sim | △ Possible | ✓ Very Likely (severe blockage) | ✓ Likely (poor mount) | ✗ Unlikely | |
| R_th > 30× sim | △ Possible (fundamental physics wrong) | ✓ Very Likely | ✓ Likely | ✗ Unlikely | |
| ΔP 10×+ higher than expected | ✓ Likely (permeability model wrong) | ✓ Likely (roughness, blockage) | △ Possible | ✗ Unlikely | ✓ **Cannot separate** without µCT |
| Zero flow | ✗ Unlikely | ✓ Very Likely (powder entrapment) | △ Possible (wrong port) | ✗ Unlikely | |
| Leak | ✗ Unlikely | ✓ Very Likely (print defect, port seal) | ✓ Possible (O-ring failure) | ✗ Unlikely | |
| Energy balance > 30% mismatch | ✗ Unlikely | ✗ Unlikely | ✓ Very Likely (heat loss) | △ Possible (cal error) | |

---

## 3. Overclaim Guardrails

### After a good match (R_th within 2×):
**DO NOT conclude:**
- "The simulation pipeline is validated" — one data point on one geometry at one condition is not validation
- "The Darcy permeability model is correct" — a good R_th match with a wrong flow rate means error cancellation
- "The design is optimized" — no comparison to alternative geometries has been made
- "The pipeline can predict absolute performance" — directional agreement ≠ quantitative accuracy

### After a 20% miss:
**DO NOT conclude:**
- "The model is wrong" — 20% is excellent for a first-principles simplified solver with known domain mismatch
- "The design needs improvement" — 20% accuracy would be remarkable at this fidelity level

### After a 50% miss:
**DO NOT conclude:**
- "The pipeline is useless" — 50% error with a Darcy model missing contact resistance, roughness, and entrance effects is within expected uncertainty
- "The design concept is flawed" — the miss may be entirely in the model, not the geometry

### After a 3× miss:
**DO NOT conclude:**
- "The Darcy approach can never work" — unless you've verified geometry fidelity (µCT), contact resistance (measured), and domain match (re-simulated at 5 mm)
- "TPMS cold plates don't work" — one geometry at one scale under one set of conditions is not generalizable

---

## 4. Missing Data Audit

| # | Missing measurement or control | Impact | Severity |
|---|-------------------------------|--------|----------|
| 1 | Actual flow rate at operating ΔP (current spec cites 0–200 LPM range — wrong by 100×) | Cannot size pump, flow meter, or interpret results | **CRITICAL** |
| 2 | Contact resistance between heater and cold plate | Cannot separate thermal interface contribution from R_th_total | **HIGH** |
| 3 | Baseline (straight-channel) test article | Cannot validate pipeline discrimination, only single-geometry function | **HIGH** |
| 4 | Pre-test µCT scan | Cannot verify channels are open before testing; any failure is ambiguous | **HIGH** |
| 5 | Actual specimen mass (compare to predicted) | Simple check for gross porosity or density anomaly | **MEDIUM** |
| 6 | Simulation at fabrication domain (5 mm, 25 W) | No apples-to-apples prediction to compare against | **HIGH** |
| 7 | Corrected simulation with physical permeability model | Current Darcy k=10⁻⁶ m² is not a physical permeability; it's a placeholder | **HIGH** |
