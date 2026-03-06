# Fabrication Handoff Readiness — candidate_02_diamond_2d_s1045

**Document ID:** STAGE7-FH-001  
**Date:** 2026-03-06  
**Status:** ACTIVE — Wave 0 complete; STL port addition COMPLETE; Wave 1 procurement pending  
**Candidate:** candidate_02_diamond_2d_s1045 (Diamond TPMS, 2D-promoted)  
**Specimen IDs:** S7-C02-001 (primary), S7-C02-002 (repeat)  
**Companion documents:** WAVE0_CLOSURE_SUMMARY.md, AM_BUILD_SPECIFICATION.md (STAGE7-AM-001),
WAVE0_WAVE1_ACTION_PACKET.md (STAGE7-AP-001), OPEN_ITEMS_CLOSURE_ORDER.md (STAGE7-OI-001)

> **Scope discipline:** This document states what is ready, what is not, and
> what must be done before AM vendor transmission.  It introduces no new physics
> claims, no simulation results, and no fabricated bench data.

---

## 1. Summary

Wave 0 repo/doc closure is complete (6 of 6 items closed).  STL port addition
is now **COMPLETE**: inlet (−Z face) and outlet (+Z face) cylindrical port
bosses (3.0 mm bore, 4.0 mm OD, 2.0 mm height) have been added to
`candidate_02_solid_phase.stl` by voxel-domain modification and marching-cubes
re-export.  The port-added STL passes watertight re-verification (0 open edges,
0 non-manifold edges, trimesh.is_watertight = True).  The updated manifest is
committed.  All four Section 6 gate items are now closed.  The vendor
transmission package is complete pending only the out-of-band STL file
delivery.

---

## 2. READY NOW

The following artifacts are committed to the repository and are ready for
inclusion in the vendor transmission package without further modification.

### 2.1 Simulation Reference Artifacts

| Artifact | Path | Notes |
|----------|------|-------|
| Simulation reference JSON | `results/stage7_benchtop/simulation_reference/simulation_reference_candidate_02.json` | Schema v1.1.0; total_power_w = 4.0; simulation_domain_mm = [2.0, 2.0, 2.0]; thermal_resistance_KW = 11.265617018419787 |
| Pipeline git SHA | `results/stage7_benchtop/simulation_reference/pipeline_git_sha.txt` | 40-character hex SHA; records the commit at which simulation predictions were locked |

### 2.2 Geometry and Fabrication Artifacts

| Artifact | Path | Notes |
|----------|------|-------|
| STL export manifest | `results/stage7_benchtop/fabrication/stl_export_manifest.json` | Records STL filename, SHA-256, byte size, watertight check result (0 open edges, 0 non-manifold edges), voxel scale (0.25 mm/voxel), and generation method |
| Solid-phase STL (port-added, watertight) | `results/stage7_benchtop/fabrication/candidate_02_solid_phase.stl` | Gitignored; 12 488 triangles; port bosses added on ±Z faces (3.0 mm bore, 4.0 mm OD, 2.0 mm height); enclosed_volume_mm3 = 72.56; watertight = true; see `port_addition` in manifest |
| Specimen directory | `results/stage7_benchtop/fabrication/specimen_S7-C02-001/` | Placeholder directory for post-build artifacts |
| AM build specification | `docs/stage7_validation/AM_BUILD_SPECIFICATION.md` | All six required sections present: material, minimum feature, build orientation, support strategy, post-processing, acceptance criteria |

### 2.3 Validation Planning Artifacts (for vendor awareness)

| Artifact | Path | Notes |
|----------|------|-------|
| Campaign README | `results/stage7_benchtop/README.md` | Candidate ID, specimen IDs, companion document list |
| Benchtop validation plan | `docs/stage7_validation/BENCHTOP_VALIDATION_PLAN.md` | Pass criteria: R_th within 2×, ΔP within 3× of simulation |
| Preflight verification | `docs/stage7_validation/PREFLIGHT_VERIFICATION.md` | TIM specification populated (Shin-Etsu X-23-7921-5, 6.0 W/(m·K), 0.10 mm BLT at 50 psi, R_contact = 0.17 K·cm²/W) |

---

## 3. STL PORT ADDITION — COMPLETE

Port addition was performed by voxel-domain modification (see `port_addition`
entry in `stl_export_manifest.json`) and has passed all required verification
checks.  The details below are retained for audit traceability.

### 3.1 Port Addition Summary (as executed)

| Field | Value |
|-------|-------|
| Inlet face | −Z (z = 0 mm, original TPMS face z = 0) |
| Outlet face | +Z (z = 5.0 mm, original TPMS face z = 19) |
| Port bore diameter | 3.0 mm (R_bore = 6 voxels × 0.25 mm) |
| Boss outer diameter | 4.0 mm (R_boss = 8 voxels × 0.25 mm) |
| Boss height | 2.0 mm per port (8 voxels × 0.25 mm) |
| Boss centre (original face) | voxel (10, 10) — confirmed fluid (channel void) by volumetric assertion |
| Transition boss | Yes |
| Method | numpy voxel extension + marching_cubes re-export (binary STL) |
| Geometry decision basis | Volumetric analysis of volume.npy; no CAD visual inspection required; all 6 TPMS faces ~56% fluid; centre (10,10) on ±Z faces confirmed channel void |

### 3.2 Post-Edit Watertight Verification

| Check | Result | Required |
|-------|--------|---------|
| open_edges | 0 | 0 |
| non_manifold_edges | 0 | 0 |
| trimesh.is_watertight | True | True |
| enclosed_volume_mm3 | 72.5599 | > 0 |
| Result | **PASS** | PASS |

All verification outputs are recorded in `stl_export_manifest.json` →
`port_addition.post_edit_watertight_check`.

---

## 4. REQUIRES OUTSIDE ACTION

These items cannot be completed within the repository.  They are Wave 1
procurement actions and depend on Wave 0 being complete (which it is).

| Item ID | Action | Dependency |
|---------|--------|------------|
| OI-05 | Issue RFQ to ≥ 2 metal L-PBF vendors; place order for S7-C02-001 and S7-C02-002. STL must have ports added (Section 3) before transmission. Vendor must confirm ≤ 0.5 mm minimum feature capability in Al alloy. | STL port addition complete; OI-03 and OI-04 closed (✓) |
| OI-11 | Order differential pressure transducer (0–5 kPa, ±25 Pa, DI-water-compatible wetted material) | None |
| OI-12 | Order 4× Type-T thermocouples, 30 AWG, ±0.5 °C (T_in, T_out, T_heater, T_top) | None |
| OI-13 | Order 1× ambient temperature sensor (T_amb_C column per DATA_SCHEMA_STAGE7.md v1.1.0) | None |
| OI-14 | Order DC power meter, 0–100 W, ±1% of reading, 4-wire preferred | None |
| OI-15 | Order DAQ system, ≥ 9 analog input channels, ≥ 16-bit, ≥ 1 Hz simultaneous, 10-column CSV output | None |
| OI-18 | Procure TIM: Shin-Etsu X-23-7921-5 (or identical specification); enter lot number in PREFLIGHT_VERIFICATION.md §2 on receipt | OI-17 closed (✓) |
| OI-20 | Order variable-speed pump, 0–500 mL/min provisional range, ≥ 50 kPa head, DI-water-compatible. Do not size from Stage 4 Q = 44 LPM (non-physical). Re-evaluate sizing when CT-based flow estimate (OI-09) is available. | None for provisional order |

---

## 5. Vendor Transmission Package — Artifact Checklist

The following files constitute the minimum vendor transmission package for the
AM fabrication order.  All items marked **READY** are committed to the repo and
may be transmitted immediately.  Items marked **PENDING** must be completed
before transmission.

| # | Artifact | Status | Notes |
|---|----------|--------|-------|
| V-01 | `candidate_02_solid_phase.stl` (with inlet/outlet ports) | **READY** | Ports added on ±Z faces (3.0 mm bore, 4.0 mm OD, 2.0 mm height); watertight verified; SHA-256 in manifest `port_addition.post_edit_sha256`; deliver out-of-band |
| V-02 | `results/stage7_benchtop/fabrication/stl_export_manifest.json` | **READY** (update after port edit) | Transmit the updated version after port addition is complete |
| V-03 | `docs/stage7_validation/AM_BUILD_SPECIFICATION.md` | **READY** | All six required sections present; STAGE7-AM-001 |
| V-04 | `results/stage7_benchtop/simulation_reference/simulation_reference_candidate_02.json` | **READY** | For vendor awareness of acceptance criteria context only |

**Do not transmit** the fluid-channel STL
(`results/stage3_geometry_smoke/candidate_02_diamond_2d_s1045/geometry/geometry.stl`).
It has 573 open boundary edges and is not suitable for L-PBF slicing.

---

## 6. Blocking Item Closure Gate

The AM vendor order (OI-05) must not be issued until:

1. ☑ Inlet and outlet ports are added to `candidate_02_solid_phase.stl`
2. ☑ Watertight check re-run on port-added STL confirms open_edges = 0
3. ☑ `stl_export_manifest.json` updated with new SHA-256, triangle count, and port_addition record
4. ☑ Updated manifest committed to repo

All other Wave 1 procurement orders (OI-11, OI-12, OI-13, OI-14, OI-15, OI-18,
OI-20) may proceed in parallel with the STL port edit; they carry no dependency
on STL readiness.

---

## 7. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial fabrication handoff readiness assessment; Wave 0 complete |
| 1.1 | 2026-03-06 | STL port addition complete; all Section 6 gate items closed; Section 3 updated to reflect completed state; Section 5 V-01 status updated to READY; Section 2.2 STL row updated |
