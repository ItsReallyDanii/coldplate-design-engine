# Port Edit Execution Packet — candidate_02_diamond_2d_s1045

**Document ID:** STAGE7-PE-002  
**Date:** 2026-03-06  
**Status:** ACTIVE — execution readiness package for STL port addition  
**Candidate:** candidate_02_diamond_2d_s1045 (Diamond TPMS, 2D-promoted)  
**Companion documents:**  
- STL_PORT_EDIT_PLAN.md (STAGE7-PE-001) — source plan this packet translates  
- FABRICATION_HANDOFF_READY.md (STAGE7-FH-001)  
- AM_BUILD_SPECIFICATION.md (STAGE7-AM-001)  
- WAVE0_CLOSURE_SUMMARY.md (STAGE7-AP-001-W0-CLOSE)

> **Scope discipline:** This document translates STAGE7-PE-001 into a
> step-numbered execution checklist and separates items by their current
> gate status.  It introduces no new geometry claims, no simulation
> results, and no fabrication progress claims.  All field values cited
> are drawn from repository artifacts as they exist at the date above.

---

## 1. Artifact Identity — Pre-Edit Baseline

The following values are taken directly from
`results/stage7_benchtop/fabrication/stl_export_manifest.json` and must be
confirmed before any editing begins.

| Field | Value |
|-------|-------|
| Filename | `candidate_02_solid_phase.stl` |
| Manifest path | `results/stage7_benchtop/fabrication/stl_export_manifest.json` |
| STL path (gitignored) | `results/stage7_benchtop/fabrication/candidate_02_solid_phase.stl` |
| SHA-256 (pre-port) | `7b24b9a437ae84e131e8d3680f57841bb8c22bbeaf910b299ab717c17c888340` |
| File size (pre-port) | 1,987,553 bytes |
| Triangle count (pre-port) | 7,976 |
| Domain size | 5.0 × 5.0 × 5.0 mm |
| Voxel pitch | 0.25 mm |
| Resolution | 20 × 20 × 20 voxels |
| Watertight (pre-port) | open_edges = 0, non_manifold_edges = 0, watertight = true |
| Enclosed volume (pre-port) | 53.7031 mm³ |

**Blocker statement:** The internal Diamond TPMS channel network is fully
enclosed.  No inlet or outlet port openings exist.  The file cannot be
transmitted to an AM vendor for L-PBF slicing in its current form.

---

## 2. Pre-Edit Preconditions

All items in this section must be satisfied before any CAD or mesh editing
begins.  No editing should proceed until each item is confirmed.

| # | Precondition | How to confirm |
|---|--------------|----------------|
| PRE-01 | The pre-port STL file is present locally | `sha256sum results/stage7_benchtop/fabrication/candidate_02_solid_phase.stl` — output must match `7b24b9a437ae84e131e8d3680f57841bb8c22bbeaf910b299ab717c17c888340` |
| PRE-02 | If the STL file is absent, reproduce it from the Stage 3 volume | Run `python src/stage3_geometry/cli.py smoke` then execute the generation method in `stl_export_manifest.json` (`generation_method` field); verify SHA-256 before continuing |
| PRE-03 | A CAD or mesh-editing tool capable of Boolean mesh operations and STL export is available | Acceptable tools: FreeCAD ≥ 0.20, Meshmixer (any current version), nTopology, or equivalent; tool and version must be recorded in the `port_addition` manifest entry |
| PRE-04 | The operator has read STAGE7-PE-001 §3 (Safe Edit and Re-verification Workflow) in full | No shortened procedure substitutes |
| PRE-05 | No port face location or transition boss geometry has been selected or committed to in advance | Face selection requires visual inspection of the STL (see Section 4 below) |
| PRE-06 | A copy of `stl_export_manifest.json` is open and the pre-port fields are recorded separately before editing begins | The pre-port `sha256`, `file_size_bytes`, `triangle_count`, and `watertight_check` fields must not be modified; only a new `port_addition` sub-object is added |

---

## 3. Execution Checklist — Port Edit Steps

Steps are numbered to match STAGE7-PE-001 §3.  Each step maps directly to the
plan; no steps are added or removed.

### 3A. Preparation

- [ ] **Step 1** — Confirm pre-port STL SHA-256 matches `7b24b9a…8340` (PRE-01 / PRE-02 above).
- [ ] **Step 2** — Open `candidate_02_solid_phase.stl` in the chosen CAD or mesh-editing tool.

### 3B. Visual Inspection Before Adding Ports (resolve geometry decisions)

- [ ] **Step 3** — Inspect the +Z face (Z = 5.0 mm) and −Z face (Z = 0 mm) for visible channel openings at the isosurface boundary.
- [ ] **Step 4** — Assess whether any channel opening at the selected face is large enough to connect to a ≥ 3 mm bore.  Given the 0.5 mm minimum channel diameter (Stage 6 structural metrics), a transition boss bridging from ≥ 3 mm external bore to the sub-millimeter channel network is expected to be necessary; confirm or refute by inspection.
- [ ] **Step 5** — If no suitable opening is found on ±Z faces, repeat inspection on +X/−X or +Y/−Y faces.  Record the face(s) selected.

### 3C. Port Geometry Addition

For each port (inlet and outlet):

- [ ] **Step 6a** — Add a cylindrical boss (≥ 3 mm inner diameter) positioned at the selected face, centered on the identified channel entry point.
- [ ] **Step 6b** — Merge the boss with the existing solid body (Boolean union).
- [ ] **Step 6c** — Open the connection to the internal channel void by subtracting the bore cylinder from the solid body (Boolean subtract).
- [ ] **Step 6d** — Visually confirm the bore passes through the exterior face and connects to the enclosed void region (cross-section view in CAD tool).
- [ ] **Step 7** — Confirm that no geometry was added into the interior of the 5 mm cube beyond the face-to-channel transition.

### 3D. STL Export

- [ ] **Step 8** — Export modified mesh as binary STL, units in millimetres, no rescaling.  Output filename: `candidate_02_solid_phase.stl` (supersedes pre-port file).

### 3E. Watertight Re-Verification

- [ ] **Step 9** — Run edge-manifold analysis on the exported STL (see Section 6 for verification command).  Required result: open_edges = 0, non_manifold_edges = 0, watertight = true.  If open_edges > 0 or non_manifold_edges > 0: repair mesh in the CAD tool and re-export before continuing.

### 3F. Manifest Update

- [ ] **Step 10** — Compute SHA-256 and byte size of the port-added STL.
- [ ] **Step 11** — Add the `port_addition` sub-object to `stl_export_manifest.json` per the schema in STAGE7-PE-001 §3.6.  Do not alter any pre-port fields.
- [ ] **Step 12** — Commit the updated `stl_export_manifest.json` to the repository.  The STL file remains gitignored; deliver out-of-band to the vendor with the manifest as the integrity record.

### 3G. Companion Document Updates (after manifest is committed)

- [ ] **Step 13** — Mark all four gate items in `FABRICATION_HANDOFF_READY.md` §6 as checked.
- [ ] **Step 14** — Increment `FABRICATION_HANDOFF_READY.md` document version to 1.1.
- [ ] **Step 15** — If port faces other than ±Z were selected in Step 5, update `AM_BUILD_SPECIFICATION.md` §d port location note accordingly and record the change in its revision history.

---

## 4. Status Triage

### 4A — READY TO EDIT NOW

The following items have no unresolved dependencies.  The operator may
proceed with them immediately upon satisfying the PRE-0x preconditions.

| Item | Basis |
|------|-------|
| STL file is reproducible from repo | `stl_export_manifest.json` `generation_method` field provides the exact Python call chain; `volume.npy` path is recorded in the manifest |
| CAD tool import and visual inspection | No geometry decisions are required before opening the file |
| `stl_export_manifest.json` schema for `port_addition` sub-object | Schema is fully defined in STAGE7-PE-001 §3.6; no further decision is needed |
| Watertight check procedure | Verification commands are defined in Section 6 of this document; trimesh is available in `requirements.txt` |
| Manifest commit | No approvals or external dependencies block a manifest commit |

### 4B — BLOCKED BY MISSING GEOMETRY DECISION

The following items cannot be completed until the operator performs a visual
inspection of the STL in a CAD tool.  They are not resolvable from repo
artifacts alone and must not be assumed or pre-decided.

| # | Blocked item | Why blocked | Unblocking action |
|---|--------------|-------------|-------------------|
| GD-01 | Port face selection (inlet) | The TPMS channel topology at each face of the 5 mm cube is not catalogued in repo artifacts; channel openings may be absent, undersized, or misaligned with a ≥ 3 mm bore on the ±Z faces | Visual inspection of STL in CAD tool (Step 3–5) |
| GD-02 | Port face selection (outlet) | Same as GD-01; outlet must oppose or be adjacent to the inlet face | Visual inspection of STL in CAD tool (Step 3–5) |
| GD-03 | Transition boss required or not | A transition from ≥ 3 mm port bore to 0.5 mm minimum channel diameter is expected to be necessary, but cannot be confirmed without visual inspection | Visual inspection of cross-section in CAD tool (Step 4) |
| GD-04 | Port boss height and wall thickness | No test-team requirement has been specified; test-team discretion per STAGE7-PE-001 §3.3 Step 6a | Test-team decision; not a blocking item for STL creation, but must be recorded in the `port_addition` manifest entry |
| GD-05 | Thread form or fitting type (OI-04) | Not yet defined by test team; documented as non-blocking in STAGE7-PE-001 §2 | Test-team decision; not required before AM vendor transmission |

### 4C — MUST PASS BEFORE VENDOR SEND

No items in this section may be bypassed.  All must be confirmed and recorded
in the updated `stl_export_manifest.json` before the STL file and manifest
are transmitted to any AM vendor.

| # | Check | Required result | Method |
|---|-------|-----------------|--------|
| VS-01 | Inlet port present | Through-opening from an exterior face into the internal channel void | Visual cross-section in CAD tool (Step 6d) |
| VS-02 | Outlet port present | Through-opening on the opposing or adjacent exterior face into the internal channel void | Visual cross-section in CAD tool (Step 6d) |
| VS-03 | Inlet port bore diameter | ≥ 3.0 mm clear internal diameter at the face plane | Caliper measurement in CAD tool before export |
| VS-04 | Outlet port bore diameter | ≥ 3.0 mm clear internal diameter at the face plane | Caliper measurement in CAD tool before export |
| VS-05 | Port location — inlet | On exterior face of 5 mm cube; no boss geometry extending into the lattice interior | Visual inspection in CAD tool |
| VS-06 | Port location — outlet | On exterior face of 5 mm cube; no boss geometry extending into the lattice interior | Visual inspection in CAD tool |
| VS-07 | Powder evacuation path | At least one port provides a clear through-path to the internal channel network | Visual inspection of cross-section in CAD tool |
| VS-08 | STL watertight — open_edges | 0 | Edge-manifold analysis (Step 9 / Section 6) |
| VS-09 | STL watertight — non_manifold_edges | 0 | Edge-manifold analysis (Step 9 / Section 6) |
| VS-10 | STL watertight — watertight flag | true | Edge-manifold analysis (Step 9 / Section 6) |
| VS-11 | STL enclosed volume | positive value (exact value will differ from 53.7031 mm³ due to port geometry) | Edge-manifold analysis (Step 9 / Section 6) |
| VS-12 | STL unit scale | 1 unit = 1 mm; no rescaling occurred during export | Confirm bounding box in CAD tool; 20 voxels × 0.25 mm = 5.0 mm per side |
| VS-13 | `stl_export_manifest.json` `port_addition` sub-object present | All required fields populated per STAGE7-PE-001 §3.6 schema | File inspection |
| VS-14 | `stl_export_manifest.json` pre-port fields unchanged | `sha256`, `file_size_bytes`, `triangle_count`, `watertight_check` identical to pre-port values | File inspection / diff against committed version |
| VS-15 | Updated manifest committed | `stl_export_manifest.json` with `port_addition` sub-object present in repository | `git log results/stage7_benchtop/fabrication/stl_export_manifest.json` |

---

## 5. Required Post-Edit Verification Outputs

The following outputs are required before vendor transmission.  No output
may be omitted or approximated.

| Output | Format | Where recorded |
|--------|--------|----------------|
| Post-edit SHA-256 of `candidate_02_solid_phase.stl` | 64-character hex string | `stl_export_manifest.json` → `port_addition.post_edit_sha256` |
| Post-edit file size of `candidate_02_solid_phase.stl` | integer bytes | `stl_export_manifest.json` → `port_addition.post_edit_file_size_bytes` |
| Post-edit triangle count | integer | `stl_export_manifest.json` → `port_addition.post_edit_triangle_count` |
| Watertight check result — open_edges | integer = 0 | `stl_export_manifest.json` → `port_addition.post_edit_watertight_check.open_edges` |
| Watertight check result — non_manifold_edges | integer = 0 | `stl_export_manifest.json` → `port_addition.post_edit_watertight_check.non_manifold_edges` |
| Watertight check result — enclosed_volume_mm3 | float > 0 | `stl_export_manifest.json` → `port_addition.post_edit_watertight_check.enclosed_volume_mm3` |
| Watertight check result — watertight flag | true | `stl_export_manifest.json` → `port_addition.post_edit_watertight_check.watertight` |
| Watertight check tool and version | string | `stl_export_manifest.json` → `port_addition.post_edit_watertight_check.tool` |
| Inlet face selected | one of: +Z, −Z, +X, −X, +Y, −Y | `stl_export_manifest.json` → `port_addition.inlet_face` |
| Outlet face selected | one of: +Z, −Z, +X, −X, +Y, −Y | `stl_export_manifest.json` → `port_addition.outlet_face` |
| Port bore diameter used | float ≥ 3.0 | `stl_export_manifest.json` → `port_addition.port_bore_diameter_mm` |
| Transition boss used | boolean | `stl_export_manifest.json` → `port_addition.transition_boss` |
| CAD or mesh tool used | name and version string | `stl_export_manifest.json` → `port_addition.tool` |
| Operator or tool identifier | name or automated tool ID | `stl_export_manifest.json` → `port_addition.operator` |
| Edit date | ISO-8601 date string | `stl_export_manifest.json` → `port_addition.date` |

---

## 6. Artifacts to Regenerate or Update

### Must update in repository

| Artifact | Path | Required change |
|----------|------|-----------------|
| STL export manifest | `results/stage7_benchtop/fabrication/stl_export_manifest.json` | Add `port_addition` sub-object per STAGE7-PE-001 §3.6 schema; commit; do not modify pre-port fields |
| Fabrication handoff readiness | `docs/stage7_validation/FABRICATION_HANDOFF_READY.md` | Mark all four §6 gate checklist items as checked; increment document version to 1.1 |
| AM build specification (conditional) | `docs/stage7_validation/AM_BUILD_SPECIFICATION.md` | Update §d port location note and revision history only if port faces other than ±Z are selected (GD-01/GD-02) |

### Updated but not committed (gitignored)

| Artifact | Path | Delivery method |
|----------|------|-----------------|
| Port-added solid-phase STL | `results/stage7_benchtop/fabrication/candidate_02_solid_phase.stl` | Deliver out-of-band to AM vendor; use `post_edit_sha256` from manifest for integrity verification |

### Not affected by the port edit — no change required

| Artifact | Reason |
|----------|--------|
| Stage 3–6 pipeline outputs (volume.npy, provenance.json, metrics.json, etc.) | Port addition is a CAD post-processing step; it does not alter any pipeline computation |
| Simulation reference JSON | Simulation predictions are locked; port geometry does not change them |
| `pipeline_git_sha.txt` | Already records the commit at which simulation predictions were locked; port edit is a post-pipeline CAD step |
| Benchtop validation plan, test matrix, run sheet | These documents reference simulation predictions, not STL geometry; no update required |
| Stage 6 structural metrics JSON | Stage 6 characterises the interior lattice; port addition is external and does not change internal lattice geometry |

---

## 7. Recommended Verification Procedure

The following procedure uses Python with `trimesh` (already listed in
`requirements.txt`) to perform the watertight re-verification required by
VS-08 through VS-11.  Run this after Step 8 (export) and before Step 10
(manifest update).

No geometry results are claimed here.  The operator must run the procedure and
record the actual output values.

### 7.1 SHA-256 and file size (Step 10)

```bash
python - <<'EOF'
import hashlib, pathlib

stl = pathlib.Path(
    "results/stage7_benchtop/fabrication/candidate_02_solid_phase.stl"
)
data = stl.read_bytes()
sha256 = hashlib.sha256(data).hexdigest()
size   = len(data)
print(f"sha256           : {sha256}")
print(f"file_size_bytes  : {size}")
EOF
```

### 7.2 Watertight and manifold check (Step 9)

```bash
python - <<'EOF'
import trimesh, pathlib
import numpy as np

stl = pathlib.Path(
    "results/stage7_benchtop/fabrication/candidate_02_solid_phase.stl"
)
mesh = trimesh.load_mesh(str(stl), process=False)

edges = mesh.edges_sorted
_, counts        = np.unique(edges, axis=0, return_counts=True)
open_edge_count      = int(np.sum(counts == 1))
non_manifold_count   = int(np.sum(counts > 2))
enclosed_volume_mm3  = float(abs(mesh.volume))

print(f"watertight           : {mesh.is_watertight}")
print(f"open_edges           : {open_edge_count}")
print(f"non_manifold_edges   : {non_manifold_count}")
print(f"enclosed_volume_mm3  : {enclosed_volume_mm3:.4f}")
print(f"triangle_count       : {len(mesh.faces)}")
print()
print("PASS criteria: open_edges == 0, non_manifold_edges == 0, watertight == True")
EOF
```

**Required output for VS-08 through VS-11:**

```
watertight         : True
open_edges         : 0
non_manifold_edges : 0
enclosed_volume_mm3: <positive float>
```

If `open_edges > 0` or `non_manifold_edges > 0`, stop.  Repair the mesh in the
CAD tool and re-export before re-running this check.

### 7.3 Bounding box and unit scale check (VS-12)

```bash
python - <<'EOF'
import trimesh, pathlib

stl = pathlib.Path(
    "results/stage7_benchtop/fabrication/candidate_02_solid_phase.stl"
)
mesh = trimesh.load_mesh(str(stl), process=False)
bb = mesh.bounding_box.extents   # [x_extent_mm, y_extent_mm, z_extent_mm]
print(f"bounding_box_extents_mm : {bb.tolist()}")
print("Expected: values >= 5.0 mm per axis for core body; port bosses may extend beyond 5 mm")
EOF
```

---

## 8. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial port edit execution packet; translates STAGE7-PE-001 into step-numbered checklist |
