# bench_measurement_plan.md — Minimum Measurement Set and Controls

**Date:** 2026-03-30  
**Evidence standard:** Per AGENT_MISSION.md  

---

## Test Article

| Item | Specification | Status |
|------|--------------|--------|
| S7-C02-001 | Diamond TPMS cold plate, Al 6061-T6, LPBF/SLM, 5 mm cube, 3 mm bore ports | NOT FABRICATED — STL not on disk |
| Baseline (recommended) | Straight-channel cold plate, same outer dimensions, same material, same ports | NOT DESIGNED |

---

## Boundary Conditions to Match

| Parameter | Simulation value | Bench target | Mismatch? |
|-----------|-----------------|--------------|-----------|
| Heat input | 4 W (sim domain) / 25 W (test plan) | Use 4 W for direct comparison OR re-run sim at 25 W | **YES — unresolved** |
| Inlet temperature | 25 °C | 25 °C ± 1 °C | No |
| Pressure drop | 1000 Pa (imposed BC) | Measure at whatever pump provides; do NOT force 1000 Pa | N/A — ΔP is measured |
| Fluid | DI water | DI water | No |
| Flow rate | 44 LPM (non-physical) | Measure actual. Expect 0.01–1 LPM | **YES — sim is non-physical** |
| Domain size | 2 mm sim / 5 mm fab | 5 mm fabrication | **YES — unresolved** |

---

## Must-Measure (Minimum)

| # | Observable | Instrument | Range | Accuracy | Sample rate |
|---|-----------|-----------|-------|----------|-------------|
| 1 | Inlet fluid temperature (T_in) | Type-T thermocouple | 15–40 °C | ±0.5 °C | 1 Hz |
| 2 | Outlet fluid temperature (T_out) | Type-T thermocouple | 15–80 °C | ±0.5 °C | 1 Hz |
| 3 | Base surface temperature (T_base) | Type-T thermocouple (bonded) | 15–150 °C | ±0.5 °C | 1 Hz |
| 4 | Heat input (Q) | Power supply wattage | 0–50 W | ±2% | 1 Hz |
| 5 | Pressure drop (ΔP) | Differential pressure transducer | 0–10 kPa | ±0.5% FS | 1 Hz |
| 6 | Volumetric flow rate (Q_flow) | Turbine or Coriolis flow meter | 0.01–5 LPM | ±2% | 1 Hz |
| 7 | Leak/no-leak | Pressure hold test at 2× operating P | Binary | Binary | Pre-test |

**CRITICAL CORRECTION:** The repo's existing instrumentation spec (INSTRUMENTATION_AND_SENSORS.md) calls for a 0–200 LPM flow meter based on the non-physical simulation flow rate (44–108 LPM). Real flow through a 5 mm TPMS cube at ~1000 Pa will be orders of magnitude lower. **Use 0.01–5 LPM.**

---

## Nice-to-Have (Not Required)

| # | Observable | Instrument | Value added |
|---|-----------|-----------|-------------|
| 8 | Surface temperature map | IR camera | Validates temperature uniformity |
| 9 | Pre-test internal geometry | µCT scan | Confirms channels are open |
| 10 | Post-test internal condition | µCT scan | Identifies degradation |

---

## Controls

1. **Steady-state criterion:** Temperature drift < 0.5 °C/min for ≥ 5 consecutive minutes
2. **Repeatability:** Minimum 3 repeat runs at nominal conditions
3. **Parasitic loss baseline:** At least one run with heater + empty fixture (no cold plate) to measure heat losses
4. **Thermocouple attachment:** Consistent bonding method — thermal paste, specified thickness, photo documented
5. **Flow conditioning:** Degas DI water before testing. Allow 5 min flow-through before recording

---

## Test Matrix (Minimum)

| Phase | Condition | Runs | Duration/run | Purpose |
|-------|----------|------|-------------|---------|
| A — Leak test | 2× operating P, no heater | 1 | 10 min | Structural integrity |
| B — Nominal | 4 W, 25 °C inlet, natural ΔP | 3 | 20 min | Primary R_th measurement |
| C — Power sweep | 2 W, 4 W, 10 W, 25 W | 1 each | 15 min | Linearity check |
| D — Flow sweep (if pump allows) | Vary pump speed, measure ΔP vs Q | 3–5 points | 10 min each | ΔP–Q curve |

**Total minimum test time:** ~3 hours active + setup/teardown

---

## Derived Quantities

| Quantity | Formula | Units |
|----------|---------|-------|
| Thermal resistance (R_th) | (T_base − T_in) / Q | K/W |
| Hydraulic resistance (R_hyd) | ΔP / Q_flow | Pa·s/m³ |
| Heat absorbed by fluid | ṁ × c_p × (T_out − T_in) | W |
| Energy balance check | Q_heater vs Q_fluid (should be within 20%) | % |

---

## Data Logging

- Format: CSV with headers
- Filename convention: `S7-C02-001_phaseB_run01_YYYYMMDD_HHMMSS.csv`
- Columns: `timestamp_s, T_in_C, T_out_C, T_base_C, Q_power_W, deltaP_Pa, Q_flow_LPM`
- Steady-state identification: Last 5 minutes of each run if convergence met
