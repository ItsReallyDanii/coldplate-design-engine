# EXP_HYBRID_001: Serpentine + TPMS Hybrid Comparison

**Timestamp:** 2026-04-29T05:21:09.412892+00:00
**Resolution:** 40^3 | Domain: 10mm | Total: 100W
**Labels:** SCREENING_ONLY / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED

**Hybrid rule:** HYBRID_HARD_SPLIT
- hybrid_25: 10/40 layers serpentine (inlet side), 30/40 diamond
- hybrid_50: 20/40 layers serpentine, 20/40 diamond

## Porosity

| | serpentine | raw_diamond | hybrid_25 | hybrid_50 |
|--|---|---|---|---|
| Porosity | 0.4500 | 0.4698 | 0.4646 | 0.4603 |

## Flow [FLOW_SIMULATED]

| Metric | serpentine | raw_diamond | hybrid_25 | hybrid_50 |
|--------|---|---|---|---|
| R_h | 2.1667e+05 | 3.7023e+05 | 3.5571e+05 | 3.1889e+05 |
| Q (LPM) | 276.9231 | 162.0599 | 168.6747 | 188.1512 |
| Flow CV | 0.0000 | 0.2487 | 0.2749 | 0.2455 |

## Thermal: uniform [THERMAL_SCREENED]

| Metric | serpentine | raw_diamond | hybrid_25 | hybrid_50 |
|--------|---|---|---|---|
| T_peak solid | 68.98 | 113.30 | 51.79 | 55.43 |
| T_p95 solid | 60.05 | 45.05 | 46.33 | 49.19 |
| T_mean solid | 47.11 | 30.91 | 32.57 | 35.47 |
| T_hotspot local | 47.11 | 31.00 | 35.07 | 38.66 |
| R_th (K/W) | 4.3982e-01 | 8.8301e-01 | 4.7121e-01 | 4.5491e-01 |
| Temp spread | 32.70 | 87.63 | 25.89 | 28.71 |
| Temp CV | 0.1570 | 0.2005 | 0.1934 | 0.1893 |

## Thermal: center_hotspot [THERMAL_SCREENED]

| Metric | serpentine | raw_diamond | hybrid_25 | hybrid_50 |
|--------|---|---|---|---|
| T_peak solid | 78.97 | 76.24 | 71.09 | 70.60 |
| T_p95 solid | 63.06 | 43.98 | 45.19 | 49.82 |
| T_mean solid | 46.30 | 30.94 | 32.40 | 35.38 |
| T_hotspot local | 47.88 | 27.92 | 32.57 | 37.87 |
| R_th (K/W) | 5.7279e-01 | 5.6616e-01 | 5.6627e-01 | 7.9742e-01 |
| Temp spread | 47.22 | 50.55 | 45.20 | 43.92 |
| Temp CV | 0.1822 | 0.2092 | 0.2009 | 0.1999 |

## Thermal: off_center_hotspot [THERMAL_SCREENED]

| Metric | serpentine | raw_diamond | hybrid_25 | hybrid_50 |
|--------|---|---|---|---|
| T_peak solid | 89.31 | 103.76 | 73.10 | 78.80 |
| T_p95 solid | 65.41 | 44.43 | 47.53 | 53.57 |
| T_mean solid | 46.07 | 30.87 | 32.78 | 35.94 |
| T_hotspot local | 67.24 | 37.83 | 49.77 | 57.08 |
| R_th (K/W) | 6.4306e-01 | 7.8762e-01 | 9.9310e-01 | 5.5228e-01 |
| Temp spread | 54.36 | 78.21 | 47.33 | 52.36 |
| Temp CV | 0.2072 | 0.2209 | 0.2264 | 0.2391 |

## Thermal: dual_hotspot [THERMAL_SCREENED]

| Metric | serpentine | raw_diamond | hybrid_25 | hybrid_50 |
|--------|---|---|---|---|
| T_peak solid | 79.50 | 70.57 | 69.14 | 69.63 |
| T_p95 solid | 64.71 | 44.25 | 45.86 | 50.26 |
| T_mean solid | 46.76 | 30.85 | 32.35 | 35.42 |
| T_hotspot local | 49.30 | 28.61 | 34.14 | 39.59 |
| R_th (K/W) | 5.4504e-01 | 5.6450e-01 | 9.1649e-01 | 6.2265e-01 |
| Temp spread | 48.27 | 44.87 | 43.25 | 43.03 |
| Temp CV | 0.1908 | 0.2061 | 0.2012 | 0.2095 |