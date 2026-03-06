# STL Port-Edit Readiness Plan — candidate_02_diamond_2d_s1045

**Document ID:** STAGE7-PE-001  
**Date:** 2026-03-06  
**Status:** ACTIVE — blocking AM vendor transmission  
**Candidate:** candidate_02_diamond_2d_s1045 (Diamond TPMS, 2D-promoted)  
**Companion documents:** FABRICATION_HANDOFF_READY.md (STAGE7-FH-001),
AM_BUILD_SPECIFICATION.md (STAGE7-AM-001), WAVE0_CLOSURE_SUMMARY.md (STAGE7-AP-001-W0-CLOSE)

> **Scope discipline:** This document records what is and is not yet done
> regarding STL port addition.  It introduces no new geometry claims, no new
> physics claims, and no simulation results.  All numerical values cited are
> taken directly from existing repo artifacts.

---

## 1. Current STL State — Exact Blocker Description

### 1.1 Artifact identity

| Field | Value | Source |
|-------|-------|--------|
| Filename | `candidate_02_solid_phase.stl` | stl_export_manifest.json |
| Manifest path | `results/stage7_benchtop/fabrication/stl_export_manifest.json` | repository |
| STL path (gitignored) | `results/stage7_benchtop/fabrication/candidate_02_solid_phase.stl` | `.gitignore: *.stl` |
| SHA-256 (pre-port) | `7b24b9a437ae84e131e8d3680f57841bb8c22bbeaf910b299ab717c17c888340` | stl_export_manifest.json |
| File size (pre-port) | 1,987,553 bytes | stl_export_manifest.json |
| Triangle count (pre-port) | 7,976 | stl_export_manifest.json |
| Domain size | 5.0 × 5.0 × 5.0 mm | stl_export_manifest.json |
| Voxel pitch | 0.25 mm | stl_export_manifest.json |
| Watertight check (pre-port) | open_edges = 0, non_manifold_edges = 0 | stl_export_manifest.json |
| Enclosed volume | 53.70 mm³ | stl_export_manifest.json |

### 1.2 Generation method (pre-port)

The STL was produced by:

1. Loading the Stage 3 fluid-binary volume (`volume.npy`) for
   `candidate_02_diamond_2d_s1045` from
   `results/stage3_geometry_smoke/candidate_02_diamond_2d_s1045/geometry/volume.npy`.
2. Inverting to solid phase (fluid=1 → 0, solid=0 → 1).
3. Padding the inverted volume with one voxel of fluid (value=1) on all six
   faces.
4. Applying `skimage.measure.marching_cubes` at level=0.5, spacing=0.25 mm.

The result is a closed solid body representing the Al metal walls and
surrounding material.  The Diamond TPMS channel network is present as enclosed
internal voids.

### 1.3 Blocker

**The internal channel network is fully enclosed.  There are no inlet or outlet
port openings.**  A vendor cannot slice this file for L-PBF and produce a part
with functional coolant flow paths.  The STL cannot be transmitted to an AM
vendor in its current state.

Additional geometry constraint relevant to port sizing: the minimum internal
channel diameter in the TPMS lattice is 0.5 mm (Stage 6 structural screening,
`results/stage6_structural_smoke/candidate_02_diamond_2d_s1045/structural_metrics.json`,
field `feature_size.min_channel_diameter_mm`).  A ≥ 3 mm port bore is
therefore ~6× larger than the minimum internal channel opening.  A transition
manifold boss connecting the external ≥ 3 mm port to the sub-millimeter
channel network will almost certainly be required.  This must be confirmed by
visual inspection of the STL in a CAD tool before committing to port geometry.

---

## 2. Minimum Acceptable Port-Edit Objectives

The following are the minimum conditions that the port-edited STL must satisfy
before the file is eligible for AM vendor transmission.  No additional geometry
objectives are imposed.

| # | Requirement | Specification | Source |
|---|-------------|---------------|--------|
| P-01 | Inlet port present | One through-opening from an exterior face into the internal channel network | AM_BUILD_SPECIFICATION.md §d |
| P-02 | Outlet port present | One through-opening on the opposing or adjacent exterior face | AM_BUILD_SPECIFICATION.md §d |
| P-03 | Minimum port bore diameter | ≥ 3 mm clear bore at the face plane | AM_BUILD_SPECIFICATION.md §d (powder evacuation), FABRICATION_HANDOFF_READY.md §3.2 |
| P-04 | Port location | On an exterior face plane of the 5 mm cube; no boss geometry extending into the TPMS lattice region interior | FABRICATION_HANDOFF_READY.md §3.3 |
| P-05 | Powder evacuation path | At least one port must provide a clear through-path to permit pressurized powder evacuation from the internal channel network | AM_BUILD_SPECIFICATION.md §d |
| P-06 | STL remains watertight | open_edges = 0, non_manifold_edges = 0 after port edit | stl_export_manifest.json watertight_check schema |
| P-07 | Manifest updated | stl_export_manifest.json updated with new SHA-256, byte size, triangle count, port_addition record; committed to repo | FABRICATION_HANDOFF_READY.md §3.4 |

**What is not required at this stage:**

- Thread form or fitting geometry (defined by test team per OI-04; standard
  barbed or NPT acceptable; not a blocking item for STL submission).
- Full CAD parametric model (mesh-editing tool output is sufficient).
- Re-running the simulation pipeline (port geometry is added by CAD
  post-processing, not by re-executing Stage 3–6).

---

## 3. Safe Edit and Re-verification Workflow

### 3.1 Preparation

1. Reproduce the STL from the repo if the file is not already present locally:  
   Run `python src/stage3_geometry/cli.py smoke` then execute the solid-phase
   export step documented in `stl_export_manifest.json`
   (`generation_method` field).  Verify the SHA-256 of the output matches
   `7b24b9a437ae84e131e8d3680f57841bb8c22bbeaf910b299ab717c17c888340`
   before proceeding.

2. Open `candidate_02_solid_phase.stl` in a CAD or mesh-editing tool
   (FreeCAD, Meshmixer, nTopology, or equivalent capable of Boolean mesh
   operations and STL export).

### 3.2 Visual inspection before adding ports

3. Inspect the +Z face (Z = 5.0 mm, voxel row 20) and the −Z face (Z = 0 mm,
   voxel row 0) of the 5 mm cube for visible channel openings at the
   isosurface boundary.

4. Assess whether any channel opening at the face is large enough to connect
   to a ≥ 3 mm bore without removing more than the solid shell at that face.
   Given the 0.5 mm minimum channel diameter, a transition boss or manifold
   geometry bridging from ≥ 3 mm external bore to the sub-millimeter
   channel network is expected to be necessary.  If so, design the transition
   boss as a tapered or stepped reducer added to the exterior of the face.

5. If no channel opening is visible or accessible at the selected face,
   choose an alternate face (+X/−X or +Y/−Y) and repeat the inspection.
   Record the face selected in the port_addition manifest entry.

### 3.3 Port geometry addition

6. For each port (inlet and outlet):  
   a. Add a cylindrical boss (≥ 3 mm inner diameter, wall thickness and
      height per test-team discretion) positioned at the selected face,
      centered on the channel entry point identified in step 4–5.  
   b. Merge the boss with the existing solid body (Boolean union).  
   c. Remove the solid material at the bore to open the connection to the
      internal channel (Boolean subtract of the bore cylinder from the
      solid body).  
   d. Verify the bore passes through the exterior face and connects to the
      enclosed void region.

7. Do not add any geometry into the interior of the 5 mm cube beyond what is
   necessary to transition from the exterior face to the channel opening.

### 3.4 STL export

8. Export the modified mesh as binary STL, units in millimetres.  Do not
   rescale.  Name the output file `candidate_02_solid_phase.stl` (same
   filename; the pre-port file is superseded).

### 3.5 Watertight re-verification

9. Run edge-manifold analysis on the exported STL (trimesh or equivalent).
   Required result:

   | Metric | Required value |
   |--------|---------------|
   | `open_edges` | 0 |
   | `non_manifold_edges` | 0 |
   | `enclosed_volume_mm3` | positive (exact value will differ from 53.70 due to port geometry) |
   | `watertight` | true |

   If `open_edges > 0` or `non_manifold_edges > 0`, do not proceed.  Repair
   the mesh using the CAD tool's mesh-repair function and re-export before
   re-running the check.

### 3.6 Manifest update

10. Compute SHA-256 and byte size of the port-added STL.

11. Add a `port_addition` sub-object to `stl_export_manifest.json`.  Do not
    alter any existing top-level fields (sha256, file_size_bytes,
    triangle_count, watertight_check) — those record the pre-port state.
    Append the following structure:

    ```json
    "port_addition": {
      "date": "<ISO-8601 date>",
      "operator": "<name or tool>",
      "tool": "<CAD/mesh tool and version>",
      "inlet_face": "<+Z | -Z | +X | -X | +Y | -Y>",
      "outlet_face": "<+Z | -Z | +X | -X | +Y | -Y>",
      "port_bore_diameter_mm": <float, must be >= 3.0>,
      "transition_boss": <true | false>,
      "post_edit_sha256": "<64-char hex>",
      "post_edit_file_size_bytes": <int>,
      "post_edit_triangle_count": <int>,
      "post_edit_watertight_check": {
        "tool": "<tool and version>",
        "open_edges": 0,
        "non_manifold_edges": 0,
        "enclosed_volume_mm3": <float>,
        "watertight": true,
        "result": "PASS"
      }
    }
    ```

12. Commit the updated `stl_export_manifest.json` to the repository.  The
    STL file remains gitignored; deliver it out-of-band to the vendor with
    the manifest as the integrity record.

---

## 4. What Must Be Rechecked After the Edit

The following checks are required after the port edit is complete and before
the vendor package is transmitted.

---

### REQUIRED BEFORE VENDOR SEND

| Check | Pass criterion | Method |
|-------|---------------|--------|
| Port bore diameter (inlet) | ≥ 3.0 mm clear internal diameter at the face plane | Caliper measurement in CAD tool before export |
| Port bore diameter (outlet) | ≥ 3.0 mm clear internal diameter at the face plane | Caliper measurement in CAD tool before export |
| Port location (inlet) | On exterior face of 5 mm cube; no boss geometry inside lattice interior | Visual inspection in CAD tool |
| Port location (outlet) | On exterior face of 5 mm cube; no boss geometry inside lattice interior | Visual inspection in CAD tool |
| Bore-to-channel connectivity (inlet) | Bore opening connects to the internal void region | Visual inspection of cross-section in CAD tool |
| Bore-to-channel connectivity (outlet) | Bore opening connects to the internal void region | Visual inspection of cross-section in CAD tool |
| STL watertight check | open_edges = 0, non_manifold_edges = 0, watertight = true | Edge-manifold analysis (trimesh or equivalent) |
| stl_export_manifest.json updated | post_edit_sha256, post_edit_file_size_bytes, post_edit_triangle_count, post_edit_watertight_check all present | File inspection |
| Manifest committed | Updated stl_export_manifest.json present in repository | git log |

---

### RE-VERIFY AFTER EDIT

The following items were verified before the port edit and must be
confirmed as unaffected or re-verified after the edit.

| Item | Pre-edit status | Re-verify action |
|------|-----------------|-----------------|
| STL domain size | 5.0 × 5.0 × 5.0 mm (from manifest) | Confirm bounding box in CAD tool; port bosses extending beyond this envelope are permitted |
| STL unit scale | 1 unit = 1 mm (from manifest: spacing=0.25 mm/voxel, 20 voxels) | Confirm no rescaling occurred during CAD export |
| stl_export_manifest.json pre-port fields | SHA-256 = 7b24b…8340, triangle_count = 7976, watertight.result = PASS | Do not modify pre-port fields; confirm they are preserved in the updated manifest |
| AM_BUILD_SPECIFICATION.md §d port location note | States ports on Z-max and Z-min faces | If alternate faces are selected during inspection (step 5 above), document the change and update AM_BUILD_SPECIFICATION.md §d accordingly before vendor transmission |
| FABRICATION_HANDOFF_READY.md §6 gate checklist | Items 1–4 all unchecked | After edit, mark all four gate items checked and update FABRICATION_HANDOFF_READY.md document version |

---

### STILL OUTSIDE ACTION

The following items are not affected by the port edit and remain as
procurement or external actions.  They are listed here for completeness;
no repo changes are needed.

| Item ID | Action | Dependency on port edit |
|---------|--------|------------------------|
| OI-05 | Issue RFQ to ≥ 2 metal L-PBF vendors; place order for S7-C02-001 and S7-C02-002 | Cannot proceed until port-added STL and updated manifest are ready; port edit is the current blocker |
| OI-11 | Order differential pressure transducer (0–5 kPa, ±25 Pa) | None — may proceed now |
| OI-12 | Order 4× Type-T thermocouples, 30 AWG, ±0.5 °C | None — may proceed now |
| OI-13 | Order 1× ambient temperature sensor (T_amb_C column) | None — may proceed now |
| OI-14 | Order DC power meter, 0–100 W, ±1% of reading | None — may proceed now |
| OI-15 | Order DAQ system, ≥ 9 analog inputs, ≥ 16-bit, ≥ 1 Hz | None — may proceed now |
| OI-18 | Procure TIM: Shin-Etsu X-23-7921-5; enter lot number in PREFLIGHT_VERIFICATION.md §2 | None — may proceed now |
| OI-20 | Order variable-speed pump, 0–500 mL/min provisional range | None — may proceed now; do not size from Stage 4 Q = 44 LPM (non-physical Darcy artifact) |
| OI-07 | CT scan of primary specimen S7-C02-001 post-build | Requires vendor delivery; no repo action now |
| OI-09 | CT-based flow estimate for pump sizing correction | Requires OI-07 CT data; no repo action now |

---

## 5. Artifacts to Update After Port Edit

The following repository artifacts must be updated after the port edit is
complete.  No other files require changes.

| Artifact | Update required | Timing |
|----------|-----------------|--------|
| `results/stage7_benchtop/fabrication/stl_export_manifest.json` | Add `port_addition` sub-object per Section 3.6; commit | After port edit and watertight re-check pass |
| `docs/stage7_validation/FABRICATION_HANDOFF_READY.md` | Mark all four gate checklist items in §6 as checked; increment document version to 1.1 | After manifest is committed |

The following artifact is updated but is **not committed to the repo**
(gitignored by `*.stl` in `.gitignore`):

| Artifact | Update required | Delivery method |
|----------|-----------------|-----------------|
| `results/stage7_benchtop/fabrication/candidate_02_solid_phase.stl` | Port-added version supersedes pre-port STL | Deliver out-of-band to AM vendor; use post_edit_sha256 from manifest for integrity verification |

No other simulation, provenance, or documentation files require changes as a
result of the port edit.  The port addition is a CAD post-processing step and
does not alter Stage 3–6 pipeline outputs.

---

## 6. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial STL port-edit readiness plan |
