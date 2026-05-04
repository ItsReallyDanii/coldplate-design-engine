# EXP_RESOLUTION_001: Mesh Convergence Comparison

**Completed:** 40^3, 60^3
**Domain:** 10.0mm (fixed) | **Solver:** spsolve
**Labels:** SCREENING_ONLY / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED

## 40^3 (voxel=0.25mm)

### Porosity
| | serpentine | raw_diamond | hybrid_25 |
|--|---|---|---|
| Porosity | 0.4500 | 0.4698 | 0.4646 |

### uniform
| Metric | serpentine | raw_diamond | hybrid_25 |
|--------|---|---|---|
| T_peak solid | 68.98 | 113.30 | 51.79 |
| T_p95 solid | 60.05 | 45.05 | 46.33 |
| T_mean solid | 47.11 | 30.91 | 32.57 |
| R_th (K/W) | 4.3982e-01 | 8.8301e-01 | 4.7121e-01 |
| Temp CV | 0.1570 | 0.2005 | 0.1934 |

### center_hotspot
| Metric | serpentine | raw_diamond | hybrid_25 |
|--------|---|---|---|
| T_peak solid | 77.41 | 75.98 | 71.83 |
| T_p95 solid | 62.79 | 44.02 | 45.36 |
| T_mean solid | 46.27 | 30.94 | 32.42 |
| R_th (K/W) | 5.7277e-01 | 5.6111e-01 | 5.6122e-01 |
| Temp CV | 0.1801 | 0.2092 | 0.2012 |

### off_center_hotspot
| Metric | serpentine | raw_diamond | hybrid_25 |
|--------|---|---|---|
| T_peak solid | 88.95 | 109.94 | 73.61 |
| T_p95 solid | 64.87 | 44.35 | 47.54 |
| T_mean solid | 46.04 | 30.87 | 32.79 |
| R_th (K/W) | 6.3955e-01 | 8.4938e-01 | 9.6593e-01 |
| Temp CV | 0.2044 | 0.2221 | 0.2274 |

### dual_hotspot
| Metric | serpentine | raw_diamond | hybrid_25 |
|--------|---|---|---|
| T_peak solid | 79.47 | 70.88 | 69.37 |
| T_p95 solid | 64.94 | 44.28 | 46.05 |
| T_mean solid | 46.80 | 30.86 | 32.39 |
| R_th (K/W) | 5.4466e-01 | 5.7017e-01 | 9.4517e-01 |
| Temp CV | 0.1926 | 0.2061 | 0.2023 |

## 60^3 (voxel=0.1667mm)

### Porosity
| | serpentine | raw_diamond | hybrid_25 |
|--|---|---|---|
| Porosity | 0.4000 | 0.4693 | 0.4520 |

### uniform
| Metric | serpentine | raw_diamond | hybrid_25 |
|--------|---|---|---|
| T_peak solid | 55.21 | 89.52 | 47.54 |
| T_p95 solid | 52.86 | 40.87 | 42.42 |
| T_mean solid | 41.26 | 29.28 | 30.65 |
| R_th (K/W) | 3.0199e-01 | 6.4499e-01 | 4.3565e-01 |
| Temp CV | 0.1427 | 0.1703 | 0.1720 |

### center_hotspot
| Metric | serpentine | raw_diamond | hybrid_25 |
|--------|---|---|---|
| T_peak solid | 68.32 | 65.93 | 66.66 |
| T_p95 solid | 56.44 | 39.98 | 41.43 |
| T_mean solid | 41.20 | 29.26 | 30.44 |
| R_th (K/W) | 5.6103e-01 | 5.5332e-01 | 5.5347e-01 |
| Temp CV | 0.1845 | 0.1778 | 0.1763 |

### off_center_hotspot
| Metric | serpentine | raw_diamond | hybrid_25 |
|--------|---|---|---|
| T_peak solid | 80.25 | 85.60 | 67.93 |
| T_p95 solid | 58.58 | 40.30 | 44.44 |
| T_mean solid | 41.15 | 29.29 | 31.03 |
| R_th (K/W) | 5.5888e-01 | 6.0580e-01 | 8.7886e-01 |
| Temp CV | 0.2069 | 0.1907 | 0.2109 |

### dual_hotspot
| Metric | serpentine | raw_diamond | hybrid_25 |
|--------|---|---|---|
| T_peak solid | 73.46 | 62.39 | 65.07 |
| T_p95 solid | 59.15 | 40.39 | 42.14 |
| T_mean solid | 41.73 | 29.28 | 30.54 |
| R_th (K/W) | 4.8437e-01 | 5.6009e-01 | 8.3875e-01 |
| Temp CV | 0.2015 | 0.1780 | 0.1820 |


## Drift: 40^3_to_60^3

| Geometry | Heat map | T_peak drift | T_p95 drift | R_th drift |
|----------|----------|-------------|------------|------------|
| serpentine | uniform | 19.96% | 11.98% | 31.34% |
| serpentine | center_hotspot | 11.74% | 10.11% | 2.05% |
| serpentine | off_center_hotspot | 9.79% | 9.69% | 12.61% |
| serpentine | dual_hotspot | 7.56% | 8.90% | 11.07% |
| raw_diamond | uniform | 20.99% | 9.27% | 26.96% |
| raw_diamond | center_hotspot | 13.23% | 9.16% | 1.39% |
| raw_diamond | off_center_hotspot | 22.13% | 9.11% | 28.68% |
| raw_diamond | dual_hotspot | 11.98% | 8.80% | 1.77% |
| hybrid_25 | uniform | 8.21% | 8.45% | 7.55% |
| hybrid_25 | center_hotspot | 7.21% | 8.68% | 1.38% |
| hybrid_25 | off_center_hotspot | 7.72% | 6.50% | 9.01% |
| hybrid_25 | dual_hotspot | 6.20% | 8.51% | 11.26% |