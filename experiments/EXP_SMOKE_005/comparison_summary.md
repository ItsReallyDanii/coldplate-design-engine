# EXP_SMOKE_005: Graded Diamond TPMS Comparison

**Timestamp:** 2026-04-29T05:02:34.107665+00:00
**Resolution:** 40^3 | Domain: 10mm | Total: 100W
**Labels:** SCREENING_ONLY / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED

**Grading:** threshold = th_base + 0.3 * (1 - normalized_heatmap)
**Porosity normalized** to ~0.47 per heatmap case.

## uniform

| | serpentine | raw_diamond | graded_diamond |
|--|---|---|---|
| Porosity | 0.4500 | 0.4698 | 0.4698 |

### Flow

| Metric | serpentine | raw_diamond | graded_diamond |
|--------|---|---|---|
| R_h (Pa*s/m3) | 2.1667e+05 | 3.7023e+05 | 3.7023e+05 |
| Q (LPM) | 276.9231 | 162.0599 | 162.0599 |
| Flow CV | 0.0000 | 0.2487 | 0.2487 |

### Thermal

| Metric | serpentine | raw_diamond | graded_diamond |
|--------|---|---|---|
| T_peak solid | 68.98 | 113.30 | 113.30 |
| T_p95 solid | 60.05 | 45.05 | 45.05 |
| T_mean solid | 47.11 | 30.91 | 30.91 |
| T_hotspot local | 47.11 | 31.00 | 31.00 |
| R_th (K/W) | 4.3982e-01 | 8.8301e-01 | 8.8301e-01 |
| Temp spread | 32.70 | 87.63 | 87.63 |
| Temp CV | 0.1570 | 0.2005 | 0.2005 |

## center_hotspot

| | serpentine | raw_diamond | graded_diamond |
|--|---|---|---|
| Porosity | 0.4500 | 0.4698 | 0.4708 |

### Flow

| Metric | serpentine | raw_diamond | graded_diamond |
|--------|---|---|---|
| R_h (Pa*s/m3) | 2.1667e+05 | 3.7023e+05 | 3.6951e+05 |
| Q (LPM) | 276.9231 | 162.0599 | 162.3761 |
| Flow CV | 0.0000 | 0.2487 | 0.2514 |

### Thermal

| Metric | serpentine | raw_diamond | graded_diamond |
|--------|---|---|---|
| T_peak solid | 78.97 | 76.24 | 76.24 |
| T_p95 solid | 63.06 | 43.98 | 45.01 |
| T_mean solid | 46.30 | 30.94 | 31.34 |
| T_hotspot local | 47.88 | 27.92 | 28.00 |
| R_th (K/W) | 5.7279e-01 | 5.6616e-01 | 5.6642e-01 |
| Temp spread | 47.22 | 50.55 | 50.54 |
| Temp CV | 0.1822 | 0.2092 | 0.2204 |

## off_center_hotspot

| | serpentine | raw_diamond | graded_diamond |
|--|---|---|---|
| Porosity | 0.4500 | 0.4698 | 0.4699 |

### Flow

| Metric | serpentine | raw_diamond | graded_diamond |
|--------|---|---|---|
| R_h (Pa*s/m3) | 2.1667e+05 | 3.7023e+05 | 3.8073e+05 |
| Q (LPM) | 276.9231 | 162.0599 | 157.5938 |
| Flow CV | 0.0000 | 0.2487 | 0.2492 |

### Thermal

| Metric | serpentine | raw_diamond | graded_diamond |
|--------|---|---|---|
| T_peak solid | 89.31 | 103.76 | 103.76 |
| T_p95 solid | 65.41 | 44.43 | 45.15 |
| T_mean solid | 46.07 | 30.87 | 30.82 |
| T_hotspot local | 67.24 | 37.83 | 38.11 |
| R_th (K/W) | 6.4306e-01 | 7.8762e-01 | 7.8762e-01 |
| Temp spread | 54.36 | 78.21 | 78.18 |
| Temp CV | 0.2072 | 0.2209 | 0.2326 |

## dual_hotspot

| | serpentine | raw_diamond | graded_diamond |
|--|---|---|---|
| Porosity | 0.4500 | 0.4698 | 0.4702 |

### Flow

| Metric | serpentine | raw_diamond | graded_diamond |
|--------|---|---|---|
| R_h (Pa*s/m3) | 2.1667e+05 | 3.7023e+05 | 3.7682e+05 |
| Q (LPM) | 276.9231 | 162.0599 | 159.2267 |
| Flow CV | 0.0000 | 0.2487 | 0.2488 |

### Thermal

| Metric | serpentine | raw_diamond | graded_diamond |
|--------|---|---|---|
| T_peak solid | 79.50 | 70.57 | 70.57 |
| T_p95 solid | 64.71 | 44.25 | 45.08 |
| T_mean solid | 46.76 | 30.85 | 31.16 |
| T_hotspot local | 49.30 | 28.61 | 28.74 |
| R_th (K/W) | 5.4504e-01 | 5.6450e-01 | 5.6433e-01 |
| Temp spread | 48.27 | 44.87 | 44.86 |
| Temp CV | 0.1908 | 0.2061 | 0.2141 |
