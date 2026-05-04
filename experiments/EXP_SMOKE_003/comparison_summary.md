# EXP_SMOKE_003: Porosity-Matched Comparison

**Timestamp:** 2026-04-29T04:24:44.870597+00:00
**Solver:** scipy.sparse.linalg.spsolve (direct)
**Labels:** SCREENING_ONLY / FLOW_SIMULATED / THERMAL_SCREENED / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED

**Purpose:** Fairness control. Remove porosity confound from EXP_SMOKE_002.

## 20x20x20

Domain: 5.0mm | Voxel: 0.25mm

### Geometry [GEOMETRIC]

| | straight | serpentine | pin_fin | diamond_tpms |
|--|---|---|---|---|
| Porosity | 0.4500 | 0.5000 | 0.4575 | 0.4714 |
| Inlet fluid | 180 | 200 | 400 | 189 |
| Connected | True | True | True | True |

### Flow [FLOW_SIMULATED / NOT_FULL_CFD]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| dP (Pa) | 1000.00 | 1000.00 | 1000.00 | 1000.00 |
| Q (m3/s) | 2.3684e-03 | 2.6316e-03 | 1.2759e-03 | 1.3570e-03 |
| Q (LPM) | 142.1053 | 157.8947 | 76.5558 | 81.4197 |
| R_h (Pa*s/m3) | 4.2222e+05 | 3.8000e+05 | 7.8374e+05 | 7.3692e+05 |
| v_mean (m/s) | 2.1053e+02 | 2.1053e+02 | 1.0995e+02 | 1.5555e+02 |
| Flow CV | 0.0000 | 0.0000 | 0.8552 | 0.2862 |

### Thermal [THERMAL_SCREENED / NOT_FULL_CHT]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| T_peak solid (C) | 254.33 | 44.75 | 49.37 | 113.30 |
| T_mean solid (C) | 66.59 | 37.45 | 41.07 | 37.01 |
| R_th (K/W) | 9.1732e+00 | 7.8987e-01 | 2.1175e+00 | 3.5320e+00 |
| Temp spread (C) | 229.33 | 10.88 | 12.72 | 82.43 |
| Temp uniformity CV | 1.324641 | 0.089614 | 0.085589 | 0.159472 |

### Warnings

- [straight/flow] Non-physical velocity 210.5 m/s (Darcy artifact)
- [straight/flow] Non-physical flow rate 142.1 LPM
- [serpentine/flow] Non-physical velocity 210.5 m/s (Darcy artifact)
- [serpentine/flow] Non-physical flow rate 157.9 LPM
- [pin_fin/flow] Non-physical velocity 109.9 m/s (Darcy artifact)
- [pin_fin/flow] Non-physical flow rate 76.6 LPM
- [diamond_tpms/flow] Non-physical velocity 155.5 m/s (Darcy artifact)
- [diamond_tpms/flow] Non-physical flow rate 81.4 LPM

## 40x40x40

Domain: 10.0mm | Voxel: 0.25mm

### Geometry [GEOMETRIC]

| | straight | serpentine | pin_fin | diamond_tpms |
|--|---|---|---|---|
| Porosity | 0.4500 | 0.4500 | 0.4406 | 0.4698 |
| Inlet fluid | 720 | 720 | 1600 | 779 |
| Connected | True | True | True | True |

### Flow [FLOW_SIMULATED / NOT_FULL_CFD]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| dP (Pa) | 1000.00 | 1000.00 | 1000.00 | 1000.00 |
| Q (m3/s) | 4.6154e-03 | 4.6154e-03 | 1.8364e-03 | 2.7010e-03 |
| Q (LPM) | 276.9231 | 276.9231 | 110.1820 | 162.0599 |
| R_h (Pa*s/m3) | 2.1667e+05 | 2.1667e+05 | 5.4455e+05 | 3.7023e+05 |
| v_mean (m/s) | 1.0256e+02 | 1.0256e+02 | 4.3052e+01 | 7.6763e+01 |
| Flow CV | 0.0000 | 0.0000 | 1.1380 | 0.2487 |

### Thermal [THERMAL_SCREENED / NOT_FULL_CHT]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| T_peak solid (C) | 259.33 | 68.98 | 66.35 | 113.30 |
| T_mean solid (C) | 88.06 | 47.11 | 46.16 | 30.91 |
| R_th (K/W) | 2.3433e+00 | 4.3982e-01 | 4.9076e+00 | 8.8301e-01 |
| Temp spread (C) | 234.33 | 32.70 | 28.25 | 87.63 |
| Temp uniformity CV | 1.169439 | 0.156956 | 0.147732 | 0.200522 |

### Warnings

- [straight/flow] Non-physical velocity 102.6 m/s (Darcy artifact)
- [straight/flow] Non-physical flow rate 276.9 LPM
- [serpentine/flow] Non-physical velocity 102.6 m/s (Darcy artifact)
- [serpentine/flow] Non-physical flow rate 276.9 LPM
- [pin_fin/flow] Non-physical velocity 43.1 m/s (Darcy artifact)
- [pin_fin/flow] Non-physical flow rate 110.2 LPM
- [diamond_tpms/flow] Non-physical velocity 76.8 m/s (Darcy artifact)
- [diamond_tpms/flow] Non-physical flow rate 162.1 LPM
