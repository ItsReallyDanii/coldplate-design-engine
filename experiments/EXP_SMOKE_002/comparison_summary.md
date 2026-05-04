# EXP_SMOKE_002: 4-Geometry Comparison Summary

**Timestamp:** 2026-04-29T04:12:55.042905+00:00
**Solver:** scipy.sparse.linalg.spsolve (direct)
**Labels:** SCREENING_ONLY / FLOW_SIMULATED / THERMAL_SCREENED / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED

**Interpretation:** Beating straight channel is sanity only. Beating serpentine AND pin-fin is a stronger screening signal.

## 20x20x20

Domain: 5.0mm cube | Voxel: 0.25mm

### Geometry [GEOMETRIC]

| | straight | serpentine | pin_fin | diamond_tpms |
|--|---|---|---|---|
| Porosity | 0.4500 | 0.3000 | 0.7975 | 0.4928 |
| Inlet fluid | 180 | 120 | 400 | 189 |
| Outlet fluid | 180 | 120 | 400 | 189 |
| Connected | True | True | True | True |

### Flow [FLOW_SIMULATED / NOT_FULL_CFD]

| Metric | straight | serpentine | pin_fin | diamond_tpms | Label |
|--------|---|---|---|---|-------|
| dP (Pa) | 1000.00 | 1000.00 | 1000.00 | 1000.00 | FLOW_SIMULATED |
| Q (m3/s) | 2.3684e-03 | 1.5789e-03 | 3.4634e-03 | 1.4169e-03 | FLOW_SIMULATED |
| Q (LPM) | 142.1053 | 94.7368 | 207.8065 | 85.0129 | FLOW_SIMULATED |
| R_h (Pa*s/m3) | 4.2222e+05 | 6.3333e+05 | 2.8873e+05 | 7.0578e+05 | FLOW_SIMULATED |
| v_mean (m/s) | 2.1053e+02 | 2.1053e+02 | 1.7637e+02 | 1.5886e+02 | FLOW_SIMULATED |
| v_max (m/s) | 2.1053e+02 | 2.1053e+02 | 2.8436e+02 | 3.3582e+02 | FLOW_SIMULATED |
| Flow CV | 0.0000 | 0.0000 | 0.3612 | 0.2723 | FLOW_SIMULATED |

### Thermal [THERMAL_SCREENED / NOT_FULL_CHT]

| Metric | straight | serpentine | pin_fin | diamond_tpms | Label |
|--------|---|---|---|---|-------|
| T_peak overall (C) | 254.33 | 79.66 | 44.12 | 113.30 | THERMAL_SCREENED |
| T_peak solid (C) | 254.33 | 79.66 | 41.77 | 113.30 | THERMAL_SCREENED |
| T_mean solid (C) | 66.59 | 55.51 | 34.56 | 36.96 | THERMAL_SCREENED |
| T_mean fluid (C) | 27.22 | 28.33 | 26.25 | 27.03 | THERMAL_SCREENED |
| R_th (K/W) | 9.1732e+00 | 2.1866e+00 | 7.6490e-01 | 3.5320e+00 | THERMAL_SCREENED |
| Temp spread solid (C) | 229.33 | 34.61 | 10.66 | 82.75 | THERMAL_SCREENED |
| Temp uniformity CV | 1.324641 | 0.197621 | 0.094411 | 0.168625 | THERMAL_SCREENED |

### Warnings

- [straight/flow] Non-physical velocity 210.5 m/s (Darcy artifact)
- [straight/flow] Non-physical flow rate 142.1 LPM
- [serpentine/flow] Non-physical velocity 210.5 m/s (Darcy artifact)
- [serpentine/flow] Non-physical flow rate 94.7 LPM
- [pin_fin/flow] Non-physical velocity 176.4 m/s (Darcy artifact)
- [pin_fin/flow] Non-physical flow rate 207.8 LPM
- [diamond_tpms/flow] Non-physical velocity 158.9 m/s (Darcy artifact)
- [diamond_tpms/flow] Non-physical flow rate 85.0 LPM

## 40x40x40

Domain: 10.0mm cube | Voxel: 0.25mm

### Geometry [GEOMETRIC]

| | straight | serpentine | pin_fin | diamond_tpms |
|--|---|---|---|---|
| Porosity | 0.3750 | 0.1500 | 0.9494 | 0.4982 |
| Inlet fluid | 600 | 240 | 1600 | 779 |
| Outlet fluid | 600 | 240 | 1600 | 779 |
| Connected | True | True | True | True |

### Flow [FLOW_SIMULATED / NOT_FULL_CFD]

| Metric | straight | serpentine | pin_fin | diamond_tpms | Label |
|--------|---|---|---|---|-------|
| dP (Pa) | 1000.00 | 1000.00 | 1000.00 | 1000.00 | FLOW_SIMULATED |
| Q (m3/s) | 3.8462e-03 | 1.5385e-03 | 9.2487e-03 | 2.8584e-03 | FLOW_SIMULATED |
| Q (LPM) | 230.7692 | 92.3077 | 554.9191 | 171.5067 | FLOW_SIMULATED |
| R_h (Pa*s/m3) | 2.6000e+05 | 6.5000e+05 | 1.0812e+05 | 3.4984e+05 | FLOW_SIMULATED |
| v_mean (m/s) | 1.0256e+02 | 1.0256e+02 | 9.8191e+01 | 7.8334e+01 | FLOW_SIMULATED |
| v_max (m/s) | 1.0256e+02 | 1.0256e+02 | 1.4396e+02 | 1.6571e+02 | FLOW_SIMULATED |
| Flow CV | 0.0000 | 0.0000 | 0.1614 | 0.2388 | FLOW_SIMULATED |

### Thermal [THERMAL_SCREENED / NOT_FULL_CHT]

| Metric | straight | serpentine | pin_fin | diamond_tpms | Label |
|--------|---|---|---|---|-------|
| T_peak overall (C) | 256.83 | 81.23 | 44.12 | 113.30 | THERMAL_SCREENED |
| T_peak solid (C) | 256.83 | 81.23 | 40.67 | 113.30 | THERMAL_SCREENED |
| T_mean solid (C) | 61.79 | 58.59 | 29.77 | 30.87 | THERMAL_SCREENED |
| T_mean fluid (C) | 26.33 | 28.33 | 25.53 | 26.01 | THERMAL_SCREENED |
| R_th (K/W) | 2.3183e+00 | 5.6235e-01 | 1.9122e-01 | 8.8301e-01 | THERMAL_SCREENED |
| Temp spread solid (C) | 231.83 | 34.09 | 14.60 | 87.72 | THERMAL_SCREENED |
| Temp uniformity CV | 1.364315 | 0.130846 | 0.137643 | 0.211033 | THERMAL_SCREENED |

### Warnings

- [straight/flow] Non-physical velocity 102.6 m/s (Darcy artifact)
- [straight/flow] Non-physical flow rate 230.8 LPM
- [serpentine/flow] Non-physical velocity 102.6 m/s (Darcy artifact)
- [serpentine/flow] Non-physical flow rate 92.3 LPM
- [pin_fin/flow] Non-physical velocity 98.2 m/s (Darcy artifact)
- [pin_fin/flow] Non-physical flow rate 554.9 LPM
- [diamond_tpms/flow] Non-physical velocity 78.3 m/s (Darcy artifact)
- [diamond_tpms/flow] Non-physical flow rate 171.5 LPM
