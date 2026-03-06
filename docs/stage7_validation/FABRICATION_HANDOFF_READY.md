# Fabrication Handoff Readiness — candidate_02_diamond_2d_s1045

**Document ID:** STAGE7-FH-001  
**Date:** 2026-03-06  
**Status:** ACTIVE — Wave 0 complete; STL port addition pending; Wave 1 procurement pending  
**Candidate:** candidate_02_diamond_2d_s1045 (Diamond TPMS, 2D-promoted)  
**Specimen IDs:** S7-C02-001 (primary), S7-C02-002 (repeat)  
**Companion documents:** WAVE0_CLOSURE_SUMMARY.md, AM_BUILD_SPECIFICATION.md (STAGE7-AM-001),
WAVE0_WAVE1_ACTION_PACKET.md (STAGE7-AP-001), OPEN_ITEMS_CLOSURE_ORDER.md (STAGE7-OI-001)

> **Scope discipline:** This document states what is ready, what is not, and
> what must be done before AM vendor transmission.  It introduces no new physics
> claims, no simulation results, and no fabricated bench data.

---

## 1. Summary

Wave 0 repo/doc closure is complete (6 of 6 items closed).  The AM vendor
transmission package is almost ready.  One action blocks transmission: the
solid-phase STL does not yet contain inlet/outlet port openings and cannot be
sent to a vendor for slicing in its current form.  All other vendor package
documents are committed and ready.

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
| Solid-phase STL (watertight body) | `results/stage7_benchtop/fabrication/candidate_02_solid_phase.stl` | Gitignored; reproducible from Stage 3 volume.npy using the method in the manifest; 7 976 triangles; enclosed_volume_mm3 = 53.70; watertight = true — **see Section 3 before transmitting** |
| Specimen directory | `results/stage7_benchtop/fabrication/specimen_S7-C02-001/` | Placeholder directory for post-build artifacts |
| AM build specification | `docs/stage7_validation/AM_BUILD_SPECIFICATION.md` | All six required sections present: material, minimum feature, build orientation, support strategy, post-processing, acceptance criteria |

### 2.3 Validation Planning Artifacts (for vendor awareness)

| Artifact | Path | Notes |
|----------|------|-------|
| Campaign README | `results/stage7_benchtop/README.md` | Candidate ID, specimen IDs, companion document list |
| Benchtop validation plan | `docs/stage7_validation/BENCHTOP_VALIDATION_PLAN.md` | Pass criteria: R_th within 2×, ΔP within 3× of simulation |
| Preflight verification | `docs/stage7_validation/PREFLIGHT_VERIFICATION.md` | TIM specification populated (Shin-Etsu X-23-7921-5, 6.0 W/(m·K), 0.10 mm BLT at 50 psi, R_contact = 0.17 K·cm²/W) |

---

## 3. REQUIRES STL EDIT

**This section describes the single blocking action before vendor transmission.**

### 3.1 Current STL State

The watertight solid-phase STL (`candidate_02_solid_phase.stl`) represents the
closed Al metal body with internal Diamond TPMS channels present as enclosed
voids.  The STL has zero open edges and zero non-manifold edges.  It is
suitable as a base geometry for downstream CAD post-processing.

**The STL does not contain inlet or outlet port openings.**  The internal
channel network is fully enclosed.  A vendor cannot slice this file for L-PBF
in its current form and produce a part with functional coolant flow paths.

### 3.2 Required Port Addition

Before transmitting to an AM vendor, the following must be added by CAD
post-processing (not by re-running the pipeline):

| Requirement | Specification | Source |
|-------------|---------------|--------|
| Inlet port | Through-hole or boss from the exterior face into the internal channel network | AM_BUILD_SPECIFICATION.md §c, §d |
| Outlet port | Through-hole or boss on the opposing or adjacent face | AM_BUILD_SPECIFICATION.md §c, §d |
| Port minimum diameter | ≥ 3 mm to allow powder evacuation | AM_BUILD_SPECIFICATION.md §d |
| Port thread or fitting type | To be defined by test team per OI-04; standard barbed or NPT fitting acceptable | AM_BUILD_SPECIFICATION.md §d |
| Port location | Oppose the channel entry and exit planes; do not block the primary coolant flow path | AM_BUILD_SPECIFICATION.md §c |
| Powder evacuation access | At least one port must provide a clear evacuation path through the internal channel network | AM_BUILD_SPECIFICATION.md §d |

### 3.3 Assumptions and Constraints

The following assumptions apply.  They are not new geometry claims; they are
the minimum defaults that must hold to proceed without additional geometry
analysis:

- **Port diameter ≥ 3 mm** is required per the AM build specification powder
  evacuation requirement.  The 5 mm × 5 mm × 5 mm domain is the full part
  envelope.  Port bosses extending beyond this envelope are permitted; the
  build specification does not constrain total envelope size.
- **Port geometry must not extend into the Diamond TPMS lattice region.**
  The lattice occupies the interior of the 5 mm cube.  Ports must be placed at
  or transitioning from the face of the cube into the channel network.  The
  exact entry point must be confirmed by visual inspection of the STL in a
  CAD tool before adding the port feature.
- **No claim is made here about the channel diameter or connectivity at the
  port entry location.**  The channel geometry at the face of the cube is
  governed by the Diamond TPMS topology at 0.25 mm voxel pitch.  If the
  channel opening at the selected face is insufficient for a ≥ 3 mm port,
  a transition boss or manifold must be added.
- **The STL must remain watertight after port addition.**  The watertight check
  (0 open edges, 0 non-manifold edges) must be re-run and recorded in the
  manifest after the port edit before transmission.

### 3.4 STL Edit Process (minimum steps)

1. Import `candidate_02_solid_phase.stl` into a CAD or mesh-editing tool (e.g.,
   FreeCAD, Meshmixer, nTopology, or equivalent).
2. Identify the channel exit/entry faces on the +Z and −Z faces of the 5 mm cube
   (or +X/−X if the build orientation is changed per AM_BUILD_SPECIFICATION.md §c).
3. Add a cylindrical port boss (≥ 3 mm ID) at each selected face, merging the
   cylinder into the solid body (Boolean union) and opening the connection to the
   internal channel (Boolean subtract from the solid).
4. Re-run watertight check.  Confirm: open_edges = 0, non_manifold_edges = 0.
5. Update `stl_export_manifest.json`: record new SHA-256, byte size, triangle
   count, and port addition method/date.  Do not alter the original generation
   fields; add a `port_addition` sub-object.
6. Commit the updated manifest.  The STL remains gitignored; deliver it
   out-of-band with the manifest as the integrity record.

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
| V-01 | `candidate_02_solid_phase.stl` (with inlet/outlet ports) | **PENDING** | Ports must be added per Section 3; re-run watertight check; update manifest |
| V-02 | `results/stage7_benchtop/fabrication/stl_export_manifest.json` | **READY** (update after port edit) | Transmit the updated version after port addition is complete |
| V-03 | `docs/stage7_validation/AM_BUILD_SPECIFICATION.md` | **READY** | All six required sections present; STAGE7-AM-001 |
| V-04 | `results/stage7_benchtop/simulation_reference/simulation_reference_candidate_02.json` | **READY** | For vendor awareness of acceptance criteria context only |

**Do not transmit** the fluid-channel STL
(`results/stage3_geometry_smoke/candidate_02_diamond_2d_s1045/geometry/geometry.stl`).
It has 573 open boundary edges and is not suitable for L-PBF slicing.

---

## 6. Blocking Item Closure Gate

The AM vendor order (OI-05) must not be issued until:

1. ☐ Inlet and outlet ports are added to `candidate_02_solid_phase.stl`
2. ☐ Watertight check re-run on port-added STL confirms open_edges = 0
3. ☐ `stl_export_manifest.json` updated with new SHA-256, triangle count, and port_addition record
4. ☐ Updated manifest committed to repo

All other Wave 1 procurement orders (OI-11, OI-12, OI-13, OI-14, OI-15, OI-18,
OI-20) may proceed in parallel with the STL port edit; they carry no dependency
on STL readiness.

---

## 7. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial fabrication handoff readiness assessment; Wave 0 complete |
