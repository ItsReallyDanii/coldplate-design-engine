# EXP_SMOKE_004: Non-Uniform Heat Map Comparison

**Timestamp:** 2026-04-29T04:38:33.763753+00:00
**Solver:** scipy.sparse.linalg.spsolve (direct)
**Labels:** SCREENING_ONLY / FLOW_SIMULATED / THERMAL_SCREENED / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED

**Purpose:** Test whether distributed TPMS cooling improves under non-uniform heating.

## 20x20x20
Domain: 5.0mm | Total heat: 25.0W

### Porosity [GEOMETRIC]

| | straight | serpentine | pin_fin | diamond_tpms |
|--|---|---|---|---|
| Porosity | 0.4500 | 0.5000 | 0.4575 | 0.4714 |

### Heat Maps

| Case | Peak/Mean | Total W | Provenance |
|------|-----------|---------|------------|
| uniform | 1.00 | 25.0 | N/A |
| center_hotspot | 3.00 | 25.0 | SYNTHETIC_HEATMAP |
| off_center_hotspot | 3.00 | 25.0 | SYNTHETIC_HEATMAP |
| dual_hotspot | 3.00 | 25.0 | SYNTHETIC_HEATMAP |

### Thermal: uniform [THERMAL_SCREENED]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| T_peak solid (C) | 254.33 | 44.75 | 49.37 | 113.30 |
| T_p95 solid (C) | 254.33 | 43.56 | 47.95 | 48.97 |
| T_mean solid (C) | 66.59 | 37.45 | 41.07 | 37.01 |
| T_hotspot local (C) | 66.59 | 37.45 | 40.63 | 37.22 |
| R_th (K/W) | 9.1732e+00 | 7.8987e-01 | 2.1175e+00 | 3.5320e+00 |
| Temp spread (C) | 229.33 | 10.88 | 12.72 | 82.43 |
| Temp CV | 1.3246 | 0.0896 | 0.0856 | 0.1595 |

### Thermal: center_hotspot [THERMAL_SCREENED]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| T_peak solid (C) | 263.52 | 58.35 | 59.40 | 76.26 |
| T_p95 solid (C) | 255.29 | 49.11 | 51.93 | 49.20 |
| T_mean solid (C) | 66.59 | 37.44 | 43.83 | 37.17 |
| T_hotspot local (C) | 25.01 | 40.56 | 42.14 | 35.27 |
| R_th (K/W) | 9.5408e+00 | 2.2084e+00 | 5.2175e+00 | 2.1912e+00 |
| Temp spread (C) | 238.52 | 28.09 | 20.90 | 45.21 |
| Temp CV | 1.3248 | 0.1489 | 0.0969 | 0.1607 |

### Thermal: off_center_hotspot [THERMAL_SCREENED]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| T_peak solid (C) | 274.30 | 59.89 | 60.09 | 104.07 |
| T_p95 solid (C) | 259.27 | 48.75 | 49.69 | 48.95 |
| T_mean solid (C) | 66.59 | 37.42 | 41.80 | 36.87 |
| T_hotspot local (C) | 25.02 | 47.81 | 48.38 | 48.67 |
| R_th (K/W) | 9.9718e+00 | 2.2134e+00 | 2.5770e+00 | 3.1629e+00 |
| Temp spread (C) | 249.30 | 29.35 | 23.00 | 73.67 |
| Temp CV | 1.3261 | 0.1511 | 0.0986 | 0.1746 |

### Thermal: dual_hotspot [THERMAL_SCREENED]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| T_peak solid (C) | 262.17 | 55.47 | 58.70 | 69.98 |
| T_p95 solid (C) | 256.68 | 46.94 | 52.84 | 48.02 |
| T_mean solid (C) | 66.59 | 37.44 | 44.15 | 36.86 |
| T_hotspot local (C) | 25.01 | 39.16 | 42.56 | 33.62 |
| R_th (K/W) | 9.4869e+00 | 2.1880e+00 | 3.6463e+00 | 2.2092e+00 |
| Temp spread (C) | 237.17 | 25.75 | 19.90 | 39.08 |
| Temp CV | 1.3249 | 0.1313 | 0.0982 | 0.1583 |

### Flow (geometry-level, heat-map-independent) [FLOW_SIMULATED]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| R_h (Pa*s/m3) | 4.2222e+05 | 3.8000e+05 | 7.8374e+05 | 7.3692e+05 |
| Q (LPM) | 142.1053 | 157.8947 | 76.5558 | 81.4197 |
| Flow CV | 0.0000 | 0.0000 | 0.8552 | 0.2862 |

### Warnings

- [straight/flow] Non-physical velocity 210.5 m/s
- [straight/flow] Non-physical flow rate 142.1 LPM
- [serpentine/flow] Non-physical velocity 210.5 m/s
- [serpentine/flow] Non-physical flow rate 157.9 LPM
- [pin_fin/flow] Non-physical velocity 109.9 m/s
- [pin_fin/flow] Non-physical flow rate 76.6 LPM
- [diamond_tpms/flow] Non-physical velocity 155.5 m/s
- [diamond_tpms/flow] Non-physical flow rate 81.4 LPM

## 40x40x40
Domain: 10.0mm | Total heat: 100.0W

### Porosity [GEOMETRIC]

| | straight | serpentine | pin_fin | diamond_tpms |
|--|---|---|---|---|
| Porosity | 0.4500 | 0.4500 | 0.4406 | 0.4698 |

### Heat Maps

| Case | Peak/Mean | Total W | Provenance |
|------|-----------|---------|------------|
| uniform | 1.00 | 100.0 | N/A |
| center_hotspot | 3.00 | 100.0 | SYNTHETIC_HEATMAP |
| off_center_hotspot | 3.00 | 100.0 | SYNTHETIC_HEATMAP |
| dual_hotspot | 3.00 | 100.0 | SYNTHETIC_HEATMAP |

### Thermal: uniform [THERMAL_SCREENED]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| T_peak solid (C) | 259.33 | 68.98 | 66.35 | 113.30 |
| T_p95 solid (C) | 258.08 | 60.05 | 59.66 | 45.05 |
| T_mean solid (C) | 88.06 | 47.11 | 46.16 | 30.91 |
| T_hotspot local (C) | 88.06 | 47.11 | nan | 31.00 |
| R_th (K/W) | 2.3433e+00 | 4.3982e-01 | 4.9076e+00 | 8.8301e-01 |
| Temp spread (C) | 234.33 | 32.70 | 28.25 | 87.63 |
| Temp CV | 1.1694 | 0.1570 | 0.1477 | 0.2005 |

### Thermal: center_hotspot [THERMAL_SCREENED]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| T_peak solid (C) | 273.94 | 78.97 | 80.76 | 76.24 |
| T_p95 solid (C) | 260.35 | 63.06 | 65.15 | 43.98 |
| T_mean solid (C) | 88.06 | 46.30 | 49.56 | 30.94 |
| T_hotspot local (C) | 25.00 | 47.88 | nan | 27.92 |
| R_th (K/W) | 2.4894e+00 | 5.7279e-01 | 3.1594e+00 | 5.6616e-01 |
| Temp spread (C) | 248.94 | 47.22 | 40.67 | 50.55 |
| Temp CV | 1.1697 | 0.1822 | 0.1631 | 0.2092 |

### Thermal: off_center_hotspot [THERMAL_SCREENED]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| T_peak solid (C) | 288.56 | 89.31 | 82.82 | 103.76 |
| T_p95 solid (C) | 270.94 | 65.41 | 62.74 | 44.43 |
| T_mean solid (C) | 88.06 | 46.07 | 47.31 | 30.87 |
| T_hotspot local (C) | 151.01 | 67.24 | nan | 37.83 |
| R_th (K/W) | 2.6356e+00 | 6.4306e-01 | 5.0305e+00 | 7.8762e-01 |
| Temp spread (C) | 263.56 | 54.36 | 44.58 | 78.21 |
| Temp CV | 1.1720 | 0.2072 | 0.1662 | 0.2209 |

### Thermal: dual_hotspot [THERMAL_SCREENED]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| T_peak solid (C) | 271.10 | 79.50 | 78.77 | 70.57 |
| T_p95 solid (C) | 260.84 | 64.71 | 65.84 | 44.25 |
| T_mean solid (C) | 88.06 | 46.76 | 49.61 | 30.85 |
| T_hotspot local (C) | 25.00 | 49.30 | nan | 28.61 |
| R_th (K/W) | 2.4610e+00 | 5.4504e-01 | 2.8873e+00 | 5.6450e-01 |
| Temp spread (C) | 246.10 | 48.27 | 38.59 | 44.87 |
| Temp CV | 1.1698 | 0.1908 | 0.1635 | 0.2061 |

### Flow (geometry-level, heat-map-independent) [FLOW_SIMULATED]

| Metric | straight | serpentine | pin_fin | diamond_tpms |
|--------|---|---|---|---|
| R_h (Pa*s/m3) | 2.1667e+05 | 2.1667e+05 | 5.4455e+05 | 3.7023e+05 |
| Q (LPM) | 276.9231 | 276.9231 | 110.1820 | 162.0599 |
| Flow CV | 0.0000 | 0.0000 | 1.1380 | 0.2487 |

### Warnings

- [straight/flow] Non-physical velocity 102.6 m/s
- [straight/flow] Non-physical flow rate 276.9 LPM
- [serpentine/flow] Non-physical velocity 102.6 m/s
- [serpentine/flow] Non-physical flow rate 276.9 LPM
- [pin_fin/flow] Non-physical velocity 43.1 m/s
- [pin_fin/flow] Non-physical flow rate 110.2 LPM
- [diamond_tpms/flow] Non-physical velocity 76.8 m/s
- [diamond_tpms/flow] Non-physical flow rate 162.1 LPM
