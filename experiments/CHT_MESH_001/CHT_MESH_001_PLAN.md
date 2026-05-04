# CHT_MESH_001: Body-Fitted Mesh for Hybrid_25

**Date:** 2026-05-01
**Status:** PLAN
**Preceding:** CHT_PREP_001 (serpentine CHT PASSED, hybrid voxel CHT FAILED)

---

## Why this exists

CHT_PREP_001 demonstrated that:
- Serpentine geometry runs clean on a voxel/topoSet mesh (CHT converged, clean End)
- Hybrid_25 TPMS geometry CRASHES on a voxel mesh (staircase artifacts create artificial
  constrictions, deltaT collapses to 8e-8, negative temperature, solver abort)

The fix: body-fitted mesh via snappyHexMesh using the hybrid_25 STL surface. This produces
smooth solid-fluid boundaries that the N-S solver can handle.

## Approach

Adapted from the working heatedDuct tutorial snappyHexMeshDict:

1. blockMesh: 10mm cube background grid (reuse existing)
2. Load hybrid_25 solid-phase STL as an internal surface
3. snappyHexMesh: snap mesh to STL, define solid cellZone via insidePoint
4. splitMeshRegions -cellZonesOnly: create fluid + solid regions
5. Copy proven BC/material files from serpentine run
6. foamMultiRun (chtMultiRegionFoam)

## Key difference from voxel approach

| Aspect | Voxel/topoSet (failed) | snappyHexMesh (this plan) |
|--------|----------------------|--------------------------|
| Solid-fluid boundary | Staircase (axis-aligned voxel faces) | Smooth (surface-conforming) |
| Narrow passage handling | Artificial constrictions from staircase | Resolved with proper cell shapes |
| Mesh quality near interface | Poor (90-degree corners) | Good (snapped to surface) |
| Cell count | Fixed 64K | ~100-300K (refined near surface) |

## Labels

INFRASTRUCTURE / NOT_A_RESULT / NO_CLAIM
