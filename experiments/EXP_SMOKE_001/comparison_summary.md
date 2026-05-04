# EXP_SMOKE_001: Comparison Summary

**Timestamp:** 2026-04-29T03:56:03.603536+00:00
**Solver:** scipy.sparse.linalg.spsolve (direct)
**Labels:** SCREENING_ONLY / FLOW_SIMULATED / THERMAL_SCREENED / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED

## Bug Found

**stage3_geometry/channels3d.py :: generate_straight_channel_3d**

Channels are created as slabs at specific X positions (axis 2 cross-sections),
but flow BCs in mesh_or_grid.py define inlet/outlet on axis 2 endpoints.
Channels are perpendicular to flow direction -- zero net throughput.

The `straight_repo` geometry below demonstrates this bug.
`straight_fixed` is a corrected baseline with channels aligned to the flow axis.

## 20x20x20

Domain: 5.0mm cube | Voxel: 0.25mm

### Flow Results [FLOW_SIMULATED / NOT_FULL_CFD]

| Metric | straight_repo | straight_fixed | diamond_tpms | Label |
|--------|---------------|----------------|--------------|-------|
| Porosity | 0.3000 | 0.4500 | 0.4928 | GEOMETRIC |
| Pressure drop (Pa) | 1000.00 | 1000.00 | 1000.00 | FLOW_SIMULATED |
| Flow rate (m3/s) | 0.000000e+00 | 2.368421e-03 | 1.416881e-03 | FLOW_SIMULATED |
| Flow rate (LPM) | 0.0000 | 142.1053 | 85.0129 | FLOW_SIMULATED |
| Hydraulic resist (Pa*s/m3) | 1.0000e+06 | 4.2222e+05 | 7.0578e+05 | FLOW_SIMULATED |
| Mean velocity (m/s) | 6.0000e-04 | 2.1053e+02 | 1.5886e+02 | FLOW_SIMULATED |
| Max velocity (m/s) | 6.0000e-04 | 2.1053e+02 | 3.3582e+02 | FLOW_SIMULATED |
| Flow uniformity CV | 0.0000 | 0.0000 | 0.2723 | FLOW_SIMULATED |

| Solver Info | straight_repo | straight_fixed | diamond |
|-------------|---------------|----------------|---------|
| converged | True | True | True |
| solve_time_s | 0.461 | 0.546 | 0.464 |
| build_time_s | 0.090 | 0.091 | 0.094 |
| total_time_s | 0.557 | 0.639 | 0.560 |
| matrix_size | 8000 | 8000 | 8000 |
| matrix_nnz | 49760 | 49760 | 49760 |

### Thermal Results [THERMAL_SCREENED / NOT_FULL_CHT]

| Metric | straight_fixed | diamond_tpms | Label |
|--------|----------------|--------------|-------|
| T_peak overall (C) | 254.33 | 113.30 | THERMAL_SCREENED |
| T_peak solid (C) | 254.33 | 113.30 | THERMAL_SCREENED |
| T_mean solid (C) | 66.59 | 36.96 | THERMAL_SCREENED |
| T_mean fluid (C) | 27.22 | 27.03 | THERMAL_SCREENED |
| Thermal resist (K/W) | 9.1732e+00 | 3.5320e+00 | THERMAL_SCREENED |
| Temp spread solid (C) | 229.33 | 82.75 | THERMAL_SCREENED |
| Temp uniformity CV | 1.324641 | 0.168625 | THERMAL_SCREENED |

| Thermal Solver | straight_fixed | diamond |
|----------------|----------------|---------|
| converged | True | True |
| solve_time_s | 0.681 | 0.724 |
| residual | 2.5405e-02 | 9.9874e-03 |
| total_time_s | 0.708 | 0.742 |

### Warnings

- [straight_repo/flow] Near-zero flow rate -- geometry likely disconnected from inlet to outlet
- [straight_fixed/flow] Non-physical velocity: 210.5 m/s (Darcy artifact)
- [straight_fixed/flow] Non-physical flow rate: 142.1 LPM
- [diamond/flow] Non-physical velocity: 158.9 m/s (Darcy artifact)
- [diamond/flow] Non-physical flow rate: 85.0 LPM

## 40x40x40

Domain: 10.0mm cube | Voxel: 0.25mm

### Flow Results [FLOW_SIMULATED / NOT_FULL_CFD]

| Metric | straight_repo | straight_fixed | diamond_tpms | Label |
|--------|---------------|----------------|--------------|-------|
| Porosity | 0.3000 | 0.3750 | 0.4982 | GEOMETRIC |
| Pressure drop (Pa) | 1000.00 | 1000.00 | 1000.00 | FLOW_SIMULATED |
| Flow rate (m3/s) | 0.000000e+00 | 3.846154e-03 | 2.858445e-03 | FLOW_SIMULATED |
| Flow rate (LPM) | 0.0000 | 230.7692 | 171.5067 | FLOW_SIMULATED |
| Hydraulic resist (Pa*s/m3) | 1.0000e+06 | 2.6000e+05 | 3.4984e+05 | FLOW_SIMULATED |
| Mean velocity (m/s) | 2.0833e-04 | 1.0256e+02 | 7.8334e+01 | FLOW_SIMULATED |
| Max velocity (m/s) | 2.5000e-04 | 1.0256e+02 | 1.6571e+02 | FLOW_SIMULATED |
| Flow uniformity CV | 0.2000 | 0.0000 | 0.2388 | FLOW_SIMULATED |

| Solver Info | straight_repo | straight_fixed | diamond |
|-------------|---------------|----------------|---------|
| converged | True | True | True |
| solve_time_s | 62.881 | 37.436 | 36.417 |
| build_time_s | 0.843 | 0.682 | 0.570 |
| total_time_s | 63.749 | 38.124 | 36.991 |
| matrix_size | 64000 | 64000 | 64000 |
| matrix_nnz | 422720 | 422720 | 422720 |

### Thermal Results [THERMAL_SCREENED / NOT_FULL_CHT]

| Metric | straight_fixed | diamond_tpms | Label |
|--------|----------------|--------------|-------|
| T_peak overall (C) | 256.83 | 113.30 | THERMAL_SCREENED |
| T_peak solid (C) | 256.83 | 113.30 | THERMAL_SCREENED |
| T_mean solid (C) | 61.79 | 30.87 | THERMAL_SCREENED |
| T_mean fluid (C) | 26.33 | 26.01 | THERMAL_SCREENED |
| Thermal resist (K/W) | 2.3183e+00 | 8.8301e-01 | THERMAL_SCREENED |
| Temp spread solid (C) | 231.83 | 87.72 | THERMAL_SCREENED |
| Temp uniformity CV | 1.364315 | 0.211033 | THERMAL_SCREENED |

| Thermal Solver | straight_fixed | diamond |
|----------------|----------------|---------|
| converged | True | True |
| solve_time_s | 38.555 | 37.170 |
| residual | 1.3526e-01 | 3.4828e-02 |
| total_time_s | 38.630 | 37.250 |

### Warnings

- [straight_repo/flow] Near-zero flow rate -- geometry likely disconnected from inlet to outlet
- [straight_fixed/flow] Non-physical velocity: 102.6 m/s (Darcy artifact)
- [straight_fixed/flow] Non-physical flow rate: 230.8 LPM
- [diamond/flow] Non-physical velocity: 78.3 m/s (Darcy artifact)
- [diamond/flow] Non-physical flow rate: 171.5 LPM
