# FIX_BASELINE_AXIS_001: Channel-Axis Alignment Patch

## Bug cause

`generate_straight_channel_3d` in `src/stage3_geometry/channels3d.py` created fluid slabs at specific axis-2 (x) positions via `volume[:, :, x_start:x_end] = 1`. The flow boundary conditions in `mesh_or_grid.get_inlet_outlet_faces` define inlet at `[:, :, 0]` and outlet at `[:, :, -1]` -- both axis-2 endpoints. The channels were cross-sections in the flow axis, not tubes running along it. Zero fluid at inlet and outlet faces. Zero net flow.

## Exact patch

**File changed:** `src/stage3_geometry/channels3d.py`

**Change:** Channel slabs now index into axis 0 (z) instead of axis 2 (x). Each slab spans all of axis 1 (y) and all of axis 2 (x = flow direction), ensuring fluid is present at every axis-2 position including inlet (index 0) and outlet (index -1).

```diff
-    pitch = nx / num_channels
+    pitch = nz / num_channels

-        x_start = max(0, center - half_width)
-        x_end = min(nx, center + half_width)
-        volume[:, :, x_start:x_end] = 1
+        z_start = max(0, center - half_width)
+        z_end = min(nz, center + half_width + 1)
+        volume[z_start:z_end, :, :] = 1
```

Also added `+1` to `z_end` to include the center+half_width voxel (off-by-one in original code caused narrower channels than intended).

Updated docstring to document the flow axis convention and the fix date.

Added module-level docstring noting the canonical flow axis convention.

## Other generators checked

| Generator | Axis bug? | Notes |
|-----------|-----------|-------|
| `generate_straight_channel_3d` | YES (fixed) | Channels were perpendicular to flow |
| `generate_serpentine_channel_3d` | No | Slabs in axis 1, span all axis 2. Accidentally correct. Missing U-bends (design limitation, not axis bug). |
| `generate_pin_fin_3d` | No | Starts all-fluid, subtracts cylindrical pins. Flow connectivity guaranteed at reasonable pin densities. |

## Files changed

1. `src/stage3_geometry/channels3d.py` -- axis fix + docstring update
2. `tests/test_stage3_channel_axis.py` -- NEW: 16 regression tests

## Tests added

`tests/test_stage3_channel_axis.py` -- 16 tests covering:

**Straight channel (12 tests):**
- Inlet has nonzero fluid at resolutions 10, 20, 40
- Outlet has nonzero fluid at resolutions 10, 20, 40
- Flood-fill connectivity from inlet to outlet at resolutions 10, 20, 40
- Channel slabs span every axis-2 position
- Porosity is in reasonable range
- Compatibility with mesh_or_grid inlet/outlet convention

**Serpentine (2 tests):**
- Inlet/outlet have nonzero fluid
- Flood-fill connectivity

**Pin-fin (2 tests):**
- Inlet/outlet have nonzero fluid
- Flood-fill connectivity

Tests can run via `pytest tests/test_stage3_channel_axis.py` or standalone via `python tests/test_stage3_channel_axis.py`.

## How to verify

```bash
cd coldplate-design-engine

# Run regression tests
pytest tests/test_stage3_channel_axis.py -v

# Run post-fix experiment (repo generator only, no workaround)
python experiments/EXP_SMOKE_001/run_exp_smoke_001_postfix.py
```

## Expected behavior after fix

The repo's `generate_straight_channel_3d` should now produce the same flow behavior as the `straight_fixed` workaround from EXP_SMOKE_001. Specifically:
- Nonzero flow rate
- Nonzero inlet/outlet fluid voxels
- Connected flow path
- Flow metrics matching EXP_SMOKE_001 straight_fixed within floating-point tolerance

## Narrative inconsistency resolution

EXP_SMOKE_000 reported straight channel screening better thermally (lower T_peak, lower R_th). EXP_SMOKE_001 showed the opposite -- diamond TPMS screening far better (T_peak 113C vs 254C, R_th 3.5 vs 9.2 K/W).

**Root cause: unconverged Jacobi solver in SMOKE_000.**

The numpy-only Jacobi fallback hit its 5000-iteration cap without converging. It also used a capped convective model (h max 1500 W/m2-K) that flattened the thermal difference between geometries. The scipy direct solver in SMOKE_001 converged correctly and used the repo's Dittus-Boelter correlation, which properly differentiates the convective cooling between distributed TPMS fluid and concentrated slab channels.

SMOKE_000's thermal direction was wrong. SMOKE_001 supersedes it.

## Labels

SCREENING_ONLY / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED
