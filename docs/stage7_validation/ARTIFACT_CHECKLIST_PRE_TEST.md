# Stage 7 Artifact Checklist — Pre-Test Day Requirements

**Document ID:** STAGE7-AC-001  
**Date:** 2026-03-06  
**Status:** READY FOR USE  
**Candidate:** candidate_02_diamond_2d_s1045  
**Companion documents:** BENCHTOP_EXECUTION_CHECKLIST.md, ARTIFACT_LAYOUT.md  

> **Scope:** Every item below must exist and be verified before test day.
> Nothing here implies fabrication is complete; items marked NOT PROCURED /
> NOT STARTED remain outstanding and block execution.

---

## 1. Simulation Reference Artifacts

These files must be committed to the repo **at the specific git SHA used for
predictions** before testing begins.  They must not be updated after
fabrication starts.

| # | File | Status | Notes |
|---|------|--------|-------|
| 1.1 | `results/stage7_benchtop/simulation_reference/simulation_reference_candidate_02.json` | NOT CREATED | Must contain Stage 3–6 predictions; see DATA_SCHEMA_STAGE7.md Section 6 for schema including `heat_flux_w_m2` and `total_power_w` fields |
| 1.2 | `results/stage7_benchtop/simulation_reference/pipeline_git_sha.txt` | NOT CREATED | Must record the exact git SHA at the time predictions are locked |
| 1.3 | Stage 5 thermal_metrics.json (candidate_02) | EXISTS: `results/stage5_thermal_smoke/candidate_02_diamond_2d_s1045/thermal_metrics.json` | R_th = 11.27 K/W at Q_total = 4.0 W; domain = 2.0 mm |
| 1.4 | Stage 6 structural_metrics.json (candidate_02) | EXISTS: `results/stage6_structural_smoke/candidate_02_diamond_2d_s1045/structural_metrics.json` | Overall pass = true; min feature = 0.5 mm |

**Before fabrication:** create `simulation_reference_candidate_02.json`
populated from the above sources.  Key required fields (per DATA_SCHEMA_STAGE7.md
Section 6, schema v1.1.0):

```
thermal_resistance_KW       = 11.265617018419787
peak_temperature_C          = 70.062 (T_max from Stage 5)
pressure_drop_Pa            = 1000.0
heat_flux_w_m2              = 1000000.0   (1 MW/m²)
total_power_w               = 4.0         (NOT 25 W)
simulation_domain_mm        = 2.0         (NOT 5.0 mm)
stage3_source               = candidate_02_diamond_2d_s1045
pipeline_git_sha            = <sha at lock time>
```

---

## 2. Geometry and Fabrication Artifacts

| # | Artifact | Status | Notes |
|---|---------|--------|-------|
| 2.1 | STL export of candidate_02 geometry | NOT CREATED | Export from Stage 3 volume.npy at 0.25 mm voxel; verify watertight before sending to AM vendor |
| 2.2 | AM build specification (material, laser parameters, orientation, support strategy) | NOT CREATED | Aluminum 6061-T6 (or equivalent Al alloy available from AM vendor); confirm 0.5 mm min feature is within vendor process capability |
| 2.3 | Fabrication vendor confirmed and order placed | NOT STARTED | Vendor must confirm minimum feature capability ≤ 0.5 mm for the chosen process |
| 2.4 | At least one specimen received and logged with specimen ID S7-C02-001 | NOT STARTED | Two specimens recommended (S7-C02-001 and S7-C02-002) to cover rework risk |
| 2.5 | Pre-test CT scan completed on S7-C02-001 | NOT STARTED | Deviation < 30% from design; report committed as `ct_report_S7-C02-001.pdf` |
| 2.6 | CT measurements committed as `ct_measurements_S7-C02-001.json` | NOT STARTED | Must include channel diameters, wall thickness measurements, and effective porosity from CT |
| 2.7 | Physics-based flow-rate estimate completed from CT channel geometry | NOT STARTED | Required before flow meter procurement (see H-1 in STAGE7-AUD-001); use Hagen-Poiseuille or Ergun equation with CT-measured channel diameter |

---

## 3. Instrumentation Artifacts

| # | Artifact | Status | Notes |
|---|---------|--------|-------|
| 3.1 | Flow meter procured, range sized from physics-based estimate (Item 2.7) | NOT STARTED | Do NOT size from Stage 4 Q = 44 LPM; see INSTRUMENTATION_AND_SENSORS.md Section 2.3 |
| 3.2 | Differential pressure transducer (0–5 kPa) or two absolute transducers procured | NOT STARTED | ±25 Pa accuracy; DI-water-compatible wetted material |
| 3.3 | 4× Type-T thermocouples for T_in, T_out, T_heater, T_top | NOT STARTED | 30 AWG, ±0.5 °C or better |
| 3.4 | 1× ambient temperature sensor for T_amb | NOT STARTED | Thermocouple or thermistor; free-air installation, not in flow path |
| 3.5 | DC power meter 0–100 W, ±1% | NOT STARTED | Measure at heater terminals |
| 3.6 | DAQ with ≥ 9 analog input channels at 1 Hz minimum | NOT STARTED | Verify channel count before test day |
| 3.7 | Calibration records for all instruments, current and on file | NOT STARTED | Traceable to NIST or equivalent national standard; see INSTRUMENTATION_AND_SENSORS.md Section 4 |

---

## 4. Thermal Interface Material

| # | Artifact | Status | Notes |
|---|---------|--------|-------|
| 4.1 | TIM type and specification confirmed in writing | NOT STARTED | Specify type (paste, pad, foil, solder); record thermal conductivity and expected contact resistance at the applied bond-line thickness; see PREFLIGHT_VERIFICATION.md Section 2 |
| 4.2 | TIM procured and on hand | NOT STARTED | Sufficient quantity for initial application plus one rework |

---

## 5. Test Infrastructure

| # | Artifact | Status | Notes |
|---|---------|--------|-------|
| 5.1 | Coolant circulation loop with chiller set to 25 ± 1 °C | NOT STARTED | DI water; confirm hose compatibility |
| 5.2 | Pump capable of delivering target ΔP across the specimen | NOT STARTED | Size after Item 2.7 flow estimate; variable-speed or adjustable-bypass preferred |
| 5.3 | Fixture to hold specimen, heater block, and TC mounts | NOT STARTED | Must constrain specimen against heater face; record fixture thermal resistance if possible |
| 5.4 | GFCI outlet on heater power circuit | NOT STARTED | Required; see BENCHTOP_VALIDATION_PLAN.md Section 9 |
| 5.5 | E-stop and over-temperature shutoff wired and tested | NOT STARTED | Set T_cutoff = 100 °C |
| 5.6 | Drip tray in place under test section | NOT STARTED | Minimum 2 L capacity |
| 5.7 | Data acquisition software installed and verified | NOT STARTED | Log all 9 channels to CSV at 1 Hz; confirmed before test day |

---

## 6. Documentation Artifacts

| # | Artifact | Status | Notes |
|---|---------|--------|-------|
| 6.1 | `results/stage7_benchtop/fabrication/build_log.md` created and populated with AM build parameters | NOT CREATED | Includes machine, material batch, build orientation, post-processing steps |
| 6.2 | `results/stage7_benchtop/README.md` created with campaign summary stub | NOT CREATED | Fill in candidate ID, specimen IDs, target test date |
| 6.3 | RUN_SHEET_CANDIDATE_02.md printed or loaded for operator reference on test day | NOT STARTED | Review with operator before session |
| 6.4 | PREFLIGHT_VERIFICATION.md completed and countersigned | NOT STARTED | Must be completed day-before or morning-of |
| 6.5 | All existing Stage 7 planning documents committed at a known git SHA | EXISTS — current HEAD | Record SHA in `pipeline_git_sha.txt` |

---

## 7. Summary Gate

**Test day is cleared only when all items in Sections 1–6 are marked complete.**

Items still open on test day:

| Section | Open items |
|---------|-----------|
| 1 | 1.1, 1.2 |
| 2 | 2.1–2.7 |
| 3 | 3.1–3.7 |
| 4 | 4.1–4.2 |
| 5 | 5.1–5.7 |
| 6 | 6.1–6.4 |

Total open items: **24 of 26**.  Test day is not yet cleared.

---

## 8. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial release |

**End of document.**
