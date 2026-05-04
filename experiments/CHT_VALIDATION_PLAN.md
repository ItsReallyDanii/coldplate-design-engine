# CHT Validation Plan: EXP_MICROCOOL_001 Phase 2

**Date:** 2026-04-30
**Status:** PLAN -- not yet executing
**Preceding:** EXP_RESOLUTION_001 (PRELIMINARY_AMBIGUOUS), M0.6 Benchmark Lock

---

## 1. Objective

Validate the hybrid_25 screening result using laminar Navier-Stokes + conjugate heat transfer (CHT). This replaces the Darcy-permeability screening solver with a physics-resolving flow solver where convective coefficients emerge from the flow field rather than being estimated per-voxel.

This is the gate between "screening-level technical win" and "publishable computational result."

---

## 2. Tool

**Primary:** OpenFOAM (open-source, reproducible, standard in the literature)

Specific solver: `chtMultiRegionFoam` (steady-state conjugate heat transfer, handles solid + fluid regions with coupled thermal BCs).

Alternative if OpenFOAM setup proves intractable: COMSOL Multiphysics (if license available), or SU2 (open-source, supports CHT but less commonly used).

**Why OpenFOAM:** Rogié 2023 (DTU), Gilmore 2021 (UNSW), and Hu 2020 used COMSOL or commercial CFD for validation. OpenFOAM is free, reproducible, and avoids license barriers. The literature accepts OpenFOAM for microchannel CHT.

---

## 3. Geometries

| ID | Geometry | Role |
|----|----------|------|
| G1 | serpentine | Strongest channel baseline from screening |
| G2 | raw_diamond | TPMS baseline / hybrid parent |
| G3 | hybrid_25 | Lead candidate (25% serpentine + 75% diamond) |

Same physical dimensions as EXP_RESOLUTION_001:
- Serpentine: 1.50mm channel width, 3 passes
- Diamond: 2.50mm wavelength, threshold calibrated to ~0.47 porosity
- Hybrid: hard split at 2.50mm from inlet

---

## 4. Domain

Fixed 10mm x 10mm x 10mm cube. Same as screening experiments.

For OpenFOAM, the voxel grid must be converted to a body-fitted mesh:
1. Export geometry as STL from voxel volume (marching cubes, as in repo's stage3 export)
2. Use `snappyHexMesh` to create a body-fitted mesh around the STL
3. Define solid and fluid regions for chtMultiRegionFoam

Target mesh: ~500K-2M cells (OpenFOAM handles this routinely). Mesh independence study required (run at 2-3 mesh densities).

---

## 5. Heat maps (priority order)

| Priority | Case | Rationale |
|----------|------|-----------|
| 1 | uniform | Baseline comparison, matches Yeranee 2022 |
| 2 | off_center_hotspot | Strongest hybrid_25 advantage in screening (15.3% at 60^3) |
| 3 | dual_hotspot | Second strongest (11.4% at 60^3), multi-zone test |
| 4 | center_hotspot | Known weakness (2.4% at 60^3), include as control if runtime allows |

Minimum: cases 1-3. Case 4 if compute budget permits.

Heat maps applied as spatially varying heat flux BC on the bottom face (same as screening, but now in OpenFOAM format: `fixedGradient` or `externalWallHeatFluxTemperature`).

Total heat input: 100W (1 MW/m^2 * 1e-4 m^2). Constant across all cases.

---

## 6. Boundary conditions

| Boundary | Flow BC | Thermal BC |
|----------|---------|------------|
| Inlet (x=0 face) | Fixed velocity or fixed pressure (1 kPa) | Fixed temperature: 25C |
| Outlet (x=end face) | Zero gradient / outlet | Zero gradient |
| Bottom face (z=0) | Wall (no-slip) | Spatially varying heat flux (heat map) |
| Top face (z=end) | Wall (no-slip) | Adiabatic |
| Side walls (y faces) | Wall (no-slip) | Adiabatic |
| Solid-fluid interface | Coupled (automatic in chtMultiRegionFoam) | Coupled (continuity of T and flux) |

Flow regime: Laminar. Re based on hydraulic diameter at microchannel scale should be well below 2000. Verify Re in the first run and switch to turbulence model only if Re > 500 in any region.

---

## 7. Material properties

| Property | Solid (aluminum) | Fluid (water at 25C) |
|----------|-----------------|---------------------|
| Density (kg/m^3) | 2700 | 998 |
| Thermal conductivity (W/m-K) | 200 | 0.6 |
| Specific heat (J/kg-K) | 900 | 4180 |
| Dynamic viscosity (Pa-s) | N/A | 0.001 |

---

## 8. Required outputs

For each geometry x heat map case:

| Output | Description |
|--------|-------------|
| T_peak_solid | Maximum temperature in solid region |
| T_p95_solid | 95th percentile temperature in solid |
| T_mean_solid | Mean solid temperature |
| T_peak_fluid | Maximum fluid temperature |
| T_mean_fluid | Mean fluid temperature |
| R_th | Thermal resistance: (T_peak - T_inlet) / Q_total |
| delta_P | Pressure drop: inlet mean - outlet mean |
| Q_flow | Volumetric flow rate at outlet |
| R_h | Hydraulic resistance: delta_P / Q_flow |
| Nu_avg | Average Nusselt number (if extractable) |
| COP | Thermal performance / pumping power |
| Temperature uniformity CV | Coefficient of variation in solid |
| Temperature field | ParaView-compatible VTK for visualization |
| Residuals | Solver convergence history |

---

## 9. Mesh convergence protocol

Run each geometry at 3 mesh densities:

| Level | Approximate cells | Purpose |
|-------|-------------------|---------|
| Coarse | ~200K | Quick sanity check |
| Medium | ~500K | Primary result |
| Fine | ~1-2M | Convergence confirmation |

Pass condition: T_peak and T_p95 change < 3% between medium and fine mesh. If not met, refine further.

---

## 10. Pass/fail thresholds (CHT level)

### Pass (publishable computational result)

| Criterion | Threshold |
|-----------|-----------|
| hybrid_25 beats serpentine on T_peak solid | >= 10% on at least 2 of 3 priority heat maps |
| hybrid_25 T_p95 <= serpentine T_p95 | All priority heat maps |
| Mesh converged | T_peak and T_p95 drift < 3% between medium and fine |
| Hydraulic penalty documented | R_h ratio reported honestly |
| All solvers converged | Residuals < 1e-4 |

### Publishable if pass

> Hybrid serpentine+TPMS geometry produces lower peak solid temperature and better bulk temperature distribution than serpentine or uniform TPMS baselines under non-uniform chip heat loads at microchannel scale, validated by laminar N-S conjugate heat transfer.

### Fail

| Criterion | Trigger |
|-----------|---------|
| hybrid_25 T_peak advantage < 5% at CHT level | Screening result was misleading |
| hybrid_25 loses T_p95 advantage | Bulk thermal benefit was a screening artifact |
| Mesh does not converge | Geometry features too fine for affordable mesh |

### If fail

> Methods paper: the auditable pipeline + governance framework is the contribution. The specific hybrid_25 geometry is documented as a screening candidate that did not survive CHT validation.

---

## 11. Geometry export pipeline

The screening pipeline produces voxel grids (numpy uint8 arrays). OpenFOAM needs STL surfaces. The conversion path:

1. **Voxel to STL:** Use `skimage.measure.marching_cubes` (already in repo's stage3 export.py) to extract the fluid-solid interface as a triangulated surface.
2. **STL to OpenFOAM mesh:** Use `snappyHexMesh` with the STL as the geometry input. Define `blockMesh` for the background hex grid, then snap to the STL surface.
3. **Region definition:** Mark fluid cells (inside STL) and solid cells (outside STL within domain). Set up `chtMultiRegionFoam` region dictionaries.

This pipeline needs to be built once and reused for all geometries.

---

## 12. Implementation phases

| Phase | Duration (est.) | Deliverable |
|-------|----------------|-------------|
| OpenFOAM installation + tutorial | 3-5 days | Working chtMultiRegionFoam on a simple test case |
| Geometry export pipeline (voxel->STL->mesh) | 3-5 days | Automated script that converts any voxel grid to OpenFOAM case |
| Single-geometry validation run | 2-3 days | serpentine at medium mesh, uniform heat flux |
| Mesh convergence study | 3-5 days | Coarse/medium/fine on serpentine |
| Full 3-geometry x 3-heatmap sweep | 5-7 days | 9 CHT runs, all outputs |
| Analysis + comparison with screening | 2-3 days | Does the ranking hold? |
| **Total** | **3-4 weeks** | |

---

## 13. Risk mitigation

| Risk | Mitigation |
|------|------------|
| OpenFOAM learning curve | Start with simpleFoam tutorial, then chtMultiRegionFoam. Many YouTube/tutorial resources. Budget 5 days. |
| snappyHexMesh quality on TPMS geometry | TPMS surfaces are smooth -- snappyHexMesh handles them well. Pin-fins or sharp channels would be harder. |
| Compute time per run | Each CHT run on a 500K mesh should take 30-60 min on a modern laptop. 9 runs = ~9 hrs total. |
| Memory | 2M cell mesh needs ~4-8 GB RAM. Your system shows ~16 GB available based on working set data. Should be fine. |
| Solver divergence on complex geometry | Start with serpentine (simplest). If it converges, diamond and hybrid should too. Use relaxation factors if needed. |

---

## 14. What this plan does NOT include

- Fabrication or experimental validation
- Roughness/tolerance sensitivity (separate experiment after CHT baseline)
- Topology-optimized baseline (B5 -- deferred)
- Literature-derived GPU heat map (aspirational -- use synthetic if unavailable)
- Patent/IP analysis
- Publication manuscript drafting

---

## 15. Labels

All CHT results will carry:
- HIGH_FIDELITY_CHT (replaces THERMAL_SCREENED)
- FLOW_SIMULATED (N-S, replaces Darcy)
- NOT_FABRICATED
- NOT_EXPERIMENTALLY_VALIDATED
- COMPUTATIONAL_ONLY

---

## 16. Claim language after CHT

If CHT pass:
> Resolution-stable, CHT-validated computational technical win. Hybrid serpentine+TPMS outperforms both parent baselines under non-uniform heating at microchannel scale. Pending: roughness/tolerance, experimental validation.

If CHT fail:
> Screening-level observation that did not survive CHT validation. Pipeline methodology is the primary contribution. Geometry result is documented as a negative finding.
