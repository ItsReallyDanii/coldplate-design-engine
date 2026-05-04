"""
Regression tests for channel-axis alignment (FIX_BASELINE_AXIS_001).

Verifies that all channel-family generators produce geometry with:
  1. Nonzero fluid voxels at the inlet face (axis-2 index 0)
  2. Nonzero fluid voxels at the outlet face (axis-2 index -1)
  3. Connected flow path from inlet to outlet

Flow axis convention (from stage4_sim.mesh_or_grid.get_inlet_outlet_faces):
  Inlet  = volume[:, :, 0]   (axis-2 index 0)
  Outlet = volume[:, :, -1]  (axis-2 index -1)

These tests exist because the original generate_straight_channel_3d placed
channels as cross-sections in axis 2, perpendicular to flow. Fixed 2026-04-29.
"""

import sys
import os
import numpy as np
import pytest

# Ensure src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from stage3_geometry.channels3d import (
    generate_straight_channel_3d,
    generate_serpentine_channel_3d,
    generate_pin_fin_3d,
)
from stage4_sim.mesh_or_grid import get_inlet_outlet_faces


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _check_inlet_outlet(volume: np.ndarray, label: str):
    """Assert nonzero fluid at inlet and outlet faces."""
    inlet_fluid = np.sum(volume[:, :, 0])
    outlet_fluid = np.sum(volume[:, :, -1])
    assert inlet_fluid > 0, f"{label}: zero fluid voxels at inlet face ([:, :, 0])"
    assert outlet_fluid > 0, f"{label}: zero fluid voxels at outlet face ([:, :, -1])"
    return int(inlet_fluid), int(outlet_fluid)


def _check_flow_connectivity(volume: np.ndarray, label: str):
    """
    Verify there exists at least one continuous fluid path from inlet to outlet.
    Uses flood-fill from inlet face along axis 2.
    """
    fluid = volume.astype(bool)
    nz, ny, nx = fluid.shape

    # Seed: all fluid voxels on inlet face (axis-2 index 0)
    visited = np.zeros_like(fluid, dtype=bool)
    stack = []
    for z in range(nz):
        for y in range(ny):
            if fluid[z, y, 0]:
                visited[z, y, 0] = True
                stack.append((z, y, 0))

    # Flood fill through 6-connected neighbors
    while stack:
        cz, cy, cx = stack.pop()
        for dz, dy, dx in [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]:
            nz_, ny_, nx_ = cz+dz, cy+dy, cx+dx
            if 0 <= nz_ < nz and 0 <= ny_ < ny and 0 <= nx_ < nx:
                if fluid[nz_, ny_, nx_] and not visited[nz_, ny_, nx_]:
                    visited[nz_, ny_, nx_] = True
                    stack.append((nz_, ny_, nx_))

    # Check: did flood fill reach any outlet voxel?
    outlet_reached = np.any(visited[:, :, -1])
    assert outlet_reached, (
        f"{label}: no connected fluid path from inlet ([:,:,0]) to outlet ([:,:,-1]). "
        f"Flood fill from inlet reached {np.sum(visited)} of {np.sum(fluid)} fluid voxels."
    )


# ---------------------------------------------------------------------------
# Straight channel tests
# ---------------------------------------------------------------------------

class TestStraightChannelAxis:
    """Regression tests for straight channel flow-axis alignment."""

    @pytest.mark.parametrize("resolution", [10, 20, 40])
    def test_inlet_has_fluid(self, resolution):
        vol, _ = generate_straight_channel_3d(
            params={"num_channels": 3, "channel_width_fraction": 0.3},
            grid_config={},
            resolution=resolution,
        )
        inlet_fluid = int(np.sum(vol[:, :, 0]))
        assert inlet_fluid > 0, f"res={resolution}: zero fluid at inlet"

    @pytest.mark.parametrize("resolution", [10, 20, 40])
    def test_outlet_has_fluid(self, resolution):
        vol, _ = generate_straight_channel_3d(
            params={"num_channels": 3, "channel_width_fraction": 0.3},
            grid_config={},
            resolution=resolution,
        )
        outlet_fluid = int(np.sum(vol[:, :, -1]))
        assert outlet_fluid > 0, f"res={resolution}: zero fluid at outlet"

    @pytest.mark.parametrize("resolution", [10, 20, 40])
    def test_flow_connectivity(self, resolution):
        vol, _ = generate_straight_channel_3d(
            params={"num_channels": 3, "channel_width_fraction": 0.3},
            grid_config={},
            resolution=resolution,
        )
        _check_flow_connectivity(vol, f"straight_channel res={resolution}")

    def test_channels_span_flow_axis(self):
        """Each channel slab should have fluid at EVERY axis-2 position."""
        vol, _ = generate_straight_channel_3d(
            params={"num_channels": 3, "channel_width_fraction": 0.3},
            grid_config={},
            resolution=20,
        )
        # For each z-slice that has fluid, it should have fluid at every x
        for z in range(20):
            if np.any(vol[z, :, :]):
                for x in range(20):
                    assert np.any(vol[z, :, x]), (
                        f"Channel slab at z={z} missing fluid at x={x}"
                    )

    def test_porosity_reasonable(self):
        """Porosity should be roughly channel_width_fraction (within rounding)."""
        vol, _ = generate_straight_channel_3d(
            params={"num_channels": 3, "channel_width_fraction": 0.3},
            grid_config={},
            resolution=20,
        )
        porosity = float(np.mean(vol))
        assert 0.2 < porosity < 0.6, f"Unexpected porosity: {porosity}"

    def test_consistent_with_mesh_or_grid_convention(self):
        """Volume shape and inlet/outlet masks should be compatible."""
        vol, meta = generate_straight_channel_3d(
            params={"num_channels": 3, "channel_width_fraction": 0.3},
            grid_config={},
            resolution=20,
        )
        faces = get_inlet_outlet_faces(vol.shape)
        inlet_mask = faces["inlet_mask"]
        outlet_mask = faces["outlet_mask"]

        # Inlet/outlet should overlap with fluid
        assert np.any(vol[inlet_mask]), "No fluid at inlet face per mesh_or_grid convention"
        assert np.any(vol[outlet_mask]), "No fluid at outlet face per mesh_or_grid convention"


# ---------------------------------------------------------------------------
# Serpentine channel tests (axis alignment -- no bug, but verify)
# ---------------------------------------------------------------------------

class TestSerpentineChannelAxis:

    def test_inlet_outlet_have_fluid(self):
        vol, _ = generate_serpentine_channel_3d(
            params={"channel_width_px": 3, "num_passes": 3},
            grid_config={},
            resolution=20,
        )
        _check_inlet_outlet(vol, "serpentine")

    def test_flow_connectivity(self):
        vol, _ = generate_serpentine_channel_3d(
            params={"channel_width_px": 3, "num_passes": 3},
            grid_config={},
            resolution=20,
        )
        _check_flow_connectivity(vol, "serpentine")


# ---------------------------------------------------------------------------
# Pin-fin tests (axis alignment -- no bug, but verify)
# ---------------------------------------------------------------------------

class TestPinFinAxis:

    def test_inlet_outlet_have_fluid(self):
        vol, _ = generate_pin_fin_3d(
            params={"pin_diameter_px": 3, "nx_pins": 3, "ny_pins": 3},
            grid_config={},
            resolution=20,
        )
        _check_inlet_outlet(vol, "pin_fin")

    def test_flow_connectivity(self):
        vol, _ = generate_pin_fin_3d(
            params={"pin_diameter_px": 3, "nx_pins": 3, "ny_pins": 3},
            grid_config={},
            resolution=20,
        )
        _check_flow_connectivity(vol, "pin_fin")


# ---------------------------------------------------------------------------
# Run standalone
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Running channel-axis regression tests...\n")
    
    # Quick inline runner for environments without pytest
    passed = 0
    failed = 0
    
    tests = [
        ("straight_10_inlet", lambda: TestStraightChannelAxis().test_inlet_has_fluid(10)),
        ("straight_10_outlet", lambda: TestStraightChannelAxis().test_outlet_has_fluid(10)),
        ("straight_10_connected", lambda: TestStraightChannelAxis().test_flow_connectivity(10)),
        ("straight_20_inlet", lambda: TestStraightChannelAxis().test_inlet_has_fluid(20)),
        ("straight_20_outlet", lambda: TestStraightChannelAxis().test_outlet_has_fluid(20)),
        ("straight_20_connected", lambda: TestStraightChannelAxis().test_flow_connectivity(20)),
        ("straight_40_inlet", lambda: TestStraightChannelAxis().test_inlet_has_fluid(40)),
        ("straight_40_outlet", lambda: TestStraightChannelAxis().test_outlet_has_fluid(40)),
        ("straight_40_connected", lambda: TestStraightChannelAxis().test_flow_connectivity(40)),
        ("straight_span_flow_axis", lambda: TestStraightChannelAxis().test_channels_span_flow_axis()),
        ("straight_porosity", lambda: TestStraightChannelAxis().test_porosity_reasonable()),
        ("straight_mesh_convention", lambda: TestStraightChannelAxis().test_consistent_with_mesh_or_grid_convention()),
        ("serpentine_inlet_outlet", lambda: TestSerpentineChannelAxis().test_inlet_outlet_have_fluid()),
        ("serpentine_connected", lambda: TestSerpentineChannelAxis().test_flow_connectivity()),
        ("pin_fin_inlet_outlet", lambda: TestPinFinAxis().test_inlet_outlet_have_fluid()),
        ("pin_fin_connected", lambda: TestPinFinAxis().test_flow_connectivity()),
    ]
    
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR {name}: {type(e).__name__}: {e}")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")
    sys.exit(1 if failed > 0 else 0)
