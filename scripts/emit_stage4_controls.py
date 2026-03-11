"""
Stage 4 control artifact emitter for coldplate-topobridge G5/G6 gate.

Generates TWO control artifacts by running the existing Stage 4 solver on
synthetic geometry volumes, using identical boundary conditions and solver
settings as the existing diamond TPMS candidates.

Control geometries:
  1. Uniform channel (G5 negative control) — all fluid, no obstructions
  2. Single central obstruction (G6 positive control) — fluid except one
     central solid block occupying ~10% of the volume

Both artifacts are written to results/stage4_sim_full/:
  baseline_uniform_channel_ctrl/
    velocity_field.npz
    provenance.json
  baseline_single_obstruction_ctrl/
    velocity_field.npz
    provenance.json

Hard constraints:
  - No changes to existing solver, io, provenance, boundary_conditions, or mesh_or_grid
  - Identical boundary conditions, grid shape, voxel size as existing candidates
  - No new solver semantics
  - No scientific claims
"""

import sys
import json
import time
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# Add src to import path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stage4_sim import (
    mesh_or_grid,
    solver,
    boundary_conditions,
    metrics,
    io,
    provenance as prov_mod,
)

# Grid settings: identical to existing full-run candidates
GRID_SHAPE = (50, 50, 50)        # nx, ny, nz
VOXEL_SIZE_MM = 0.1              # matches existing full-run artifacts
OUTPUT_DIR = Path("results/stage4_sim_full")
TIMESTAMP = datetime.now(timezone.utc).isoformat()


def get_git_sha():
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return "unknown"


# ======================================================================
# Geometry constructors
# ======================================================================

def make_uniform_channel(nx=50, ny=50, nz=50) -> np.ndarray:
    """All-fluid volume. Flow is unobstructed in every voxel. (1=fluid, 0=solid)"""
    return np.ones((nx, ny, nz), dtype=np.uint8)


def make_single_obstruction(nx=50, ny=50, nz=50) -> np.ndarray:
    """
    Fluid volume with ONE central rectangular solid obstruction.

    Obstruction: central 20% of x, 20% of y, 60% of z (centred).
    Occupies ~2.4% of total volume as a single monolithic solid block.
    Flow must route around it in both x and y, creating transverse velocity components.
    (1=fluid, 0=solid)
    """
    vol = np.ones((nx, ny, nz), dtype=np.uint8)

    # Central block dimensions: 20% of x/y, 60% of z
    x_start = int(nx * 0.40)
    x_end   = int(nx * 0.60)
    y_start = int(ny * 0.40)
    y_end   = int(ny * 0.60)
    z_start = int(nz * 0.20)
    z_end   = int(nz * 0.80)

    vol[x_start:x_end, y_start:y_end, z_start:z_end] = 0
    return vol


# ======================================================================
# Provenance builder (bridge-compatible fields)
# ======================================================================

def build_control_provenance(
    candidate_id: str,
    geometry_type: str,
    geometry_description: str,
    volume: np.ndarray,
    grid: dict,
    bc: dict,
    sim_result: dict,
    metric_results: dict,
    git_sha: str,
) -> dict:
    """
    Build a provenance.json record that is compatible with the bridge adapter.

    The bridge adapter reads:
      - prov["git_sha"]
      - prov["timestamp"]
      - prov["stage"]
      - prov["stage3_source"]["provenance"]["stage2_source"]["family"]
      - prov["stage3_source"]["provenance"]["stage2_source"]["seed"]
      - prov["simulation"]["grid"]["porosity"]
      - prov["simulation"]["grid"]["shape"]
      - prov["simulation"]["boundary_conditions"]["flow_direction"]
      - prov["simulation"]["solver"]["converged"]
    """
    nx, ny, nz = volume.shape
    n_solid = int(np.sum(volume == 0))
    n_fluid = int(np.sum(volume == 1))
    total = nx * ny * nz
    porosity = n_fluid / total

    return {
        "timestamp": TIMESTAMP,
        "stage": "stage4_sim",
        "schema_version": "1.0",
        "candidate_id": candidate_id,
        "git_sha": git_sha,
        "control_type": geometry_type,   # extra field for bridge audits
        "stage3_source": {
            # Control geometries have no real Stage 3 predecessor.
            # Bridge-required fields are filled with control metadata.
            "provenance": {
                "timestamp": TIMESTAMP,
                "stage": "stage4_control_geometry",
                "schema_version": "1.0",
                "stage2_source": {
                    "rank": None,
                    "family": geometry_type,      # e.g. "uniform_channel"
                    "seed": None,
                    "mask_id": candidate_id,
                    "total_score": None,
                    "is_valid": True,
                    "description": geometry_description,
                    "params": {
                        "nx": nx,
                        "ny": ny,
                        "nz": nz,
                        "n_solid": n_solid,
                        "n_fluid": n_fluid,
                        "porosity": round(porosity, 6),
                    }
                },
                "promotion": {
                    "volume_metadata": {
                        "type": geometry_type,
                        "porosity": round(porosity, 6),
                        "height_mm": nz * VOXEL_SIZE_MM,
                        "resolution": max(nx, ny, nz),
                        "dimensions": {"nx": nx, "ny": ny, "nz": nz},
                        "candidate_rank": None,
                        "candidate_seed": None,
                        "candidate_family": geometry_type,
                    },
                    "success": True,
                    "errors": [],
                },
                "validation": {
                    "porosity": round(porosity, 6),
                    "connectivity": {
                        "num_fluid_components": 1,
                        "note": "control geometry — connectivity not validated"
                    }
                }
            },
            "metadata": {
                "candidate_id": candidate_id,
                "control": True,
                "geometry_type": geometry_type,
                "description": geometry_description,
            }
        },
        "simulation": {
            "grid": {
                "shape": list(grid["shape"]),
                "voxel_size_mm": grid["voxel_size_mm"],
                "domain_size_mm": list(grid["domain_size_mm"]),
                "porosity": float(grid["porosity"]),
            },
            "boundary_conditions": bc,
            "solver": {
                "type": "pressure_poisson",
                "method": "finite_difference",
                "converged": sim_result["converged"],
                "iterations": sim_result["iterations"],
                "solve_time_s": sim_result["solve_time_s"],
                "tolerance": sim_result["tolerance"],
            },
            "config": {"mode": "control", "geometry_type": geometry_type},
        },
        "metrics": metric_results,
    }


# ======================================================================
# Runner
# ======================================================================

def run_control(
    name: str,
    volume: np.ndarray,
    geometry_type: str,
    description: str,
    git_sha: str,
) -> dict:
    print(f"\n--- {name} ---")
    print(f"  Geometry: {description}")
    print(f"  Shape: {volume.shape}, porosity={volume.mean():.4f}")

    # Grid
    grid = mesh_or_grid.setup_simulation_grid(volume, voxel_size_mm=VOXEL_SIZE_MM)
    print(f"  Grid: {grid['shape']}, porosity: {grid['porosity']:.4f}")

    # Boundary conditions
    bc = boundary_conditions.get_matched_boundary_conditions()

    # Solve
    print("  Running solver...")
    t0 = time.time()
    sim_result = solver.run_flow_simulation(grid, bc)
    elapsed = time.time() - t0

    if sim_result["converged"]:
        print(f"  ✓ Converged ({elapsed:.2f}s)")
    else:
        print(f"  ✗ Did not converge ({elapsed:.2f}s)")

    # Metrics
    metric_results = metrics.compute_all_metrics(sim_result, grid, bc)
    dp = metric_results["simulated_quantities"]["pressure_drop"]["pressure_drop_pa"]
    Q = metric_results["simulated_quantities"]["flow_rate"]["flow_rate_lpm"]
    print(f"  ΔP: {dp:.2f} Pa, Q: {Q:.4f} L/min")

    # Output dir
    out_dir = OUTPUT_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save velocity_field.npz (same format as existing candidates)
    vel = sim_result["velocity"]
    vel_path = out_dir / "velocity_field.npz"
    np.savez_compressed(str(vel_path), vx=vel["vx"], vy=vel["vy"], vz=vel["vz"])
    print(f"  Saved: {vel_path}  shape={vel['vx'].shape}")

    # Build and save provenance.json
    prov_record = build_control_provenance(
        candidate_id=name,
        geometry_type=geometry_type,
        geometry_description=description,
        volume=volume,
        grid=grid,
        bc=bc,
        sim_result=sim_result,
        metric_results=metric_results,
        git_sha=git_sha,
    )
    prov_path = out_dir / "provenance.json"
    with open(prov_path, "w") as f:
        json.dump(prov_record, f, indent=2)
    print(f"  Saved: {prov_path}")

    # Verify both files exist
    assert vel_path.exists(), f"MISSING: {vel_path}"
    assert prov_path.exists(), f"MISSING: {prov_path}"

    # Quick verification
    vf = np.load(str(vel_path), allow_pickle=False)
    assert "vx" in vf and "vy" in vf and "vz" in vf, "velocity_field.npz missing keys"
    assert vf["vx"].shape == GRID_SHAPE, f"Shape mismatch: {vf['vx'].shape}"
    assert not np.any(np.isnan(vf["vx"])), "NaN in vx"

    return {
        "name": name,
        "vel_path": str(vel_path),
        "prov_path": str(prov_path),
        "shape": vf["vx"].shape,
        "porosity": float(grid["porosity"]),
        "converged": sim_result["converged"],
        "pressure_drop_pa": dp,
        "flow_rate_lpm": Q,
    }


# ======================================================================
# Main
# ======================================================================

def main():
    print("=== Stage 4 Control Artifact Emitter ===")
    print(f"Output dir: {OUTPUT_DIR.resolve()}")
    print(f"Grid shape: {GRID_SHAPE}, voxel_size: {VOXEL_SIZE_MM} mm")
    print(f"Timestamp: {TIMESTAMP}")

    git_sha = get_git_sha()
    print(f"Git SHA: {git_sha[:12]}...")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # G5: Negative control — uniform channel
    vol_uniform = make_uniform_channel(*GRID_SHAPE)
    r1 = run_control(
        name="baseline_uniform_channel_ctrl",
        volume=vol_uniform,
        geometry_type="uniform_channel",
        description=(
            "All-fluid column. No obstructions. Primary axis=z. "
            "Expected: near-zero transverse velocity (vx,vy≈0), uniform vz. "
            "Bridge expected behavior: theta_std ≈ 0 (G5 negative control)."
        ),
        git_sha=git_sha,
    )

    # G6: Positive control — single central obstruction
    vol_obs = make_single_obstruction(*GRID_SHAPE)
    r2 = run_control(
        name="baseline_single_obstruction_ctrl",
        volume=vol_obs,
        geometry_type="single_obstruction",
        description=(
            "Uniform-channel with one central rectangular solid block "
            "(x=[40%,60%], y=[40%,60%], z=[20%,80%]). "
            "Flow must detour around obstruction, generating transverse vx/vy. "
            "Bridge expected behavior: theta_std clearly > 0 (G6 positive control)."
        ),
        git_sha=git_sha,
    )

    # Summary
    print("\n=== Control Artifact Summary ===")
    for r in [r1, r2]:
        print(f"\n  {r['name']}")
        print(f"    velocity_field.npz: shape={r['shape']}, converged={r['converged']}")
        print(f"    porosity: {r['porosity']:.4f}")
        print(f"    ΔP: {r['pressure_drop_pa']:.2f} Pa, Q: {r['flow_rate_lpm']:.4f} L/min")
        print(f"    vel: {r['vel_path']}")
        print(f"    prov: {r['prov_path']}")

    print("\n=== Bridge Consumption Check ===")
    print("Both artifacts are in results/stage4_sim_full/")
    print("Both contain velocity_field.npz (keys: vx, vy, vz) and provenance.json")
    print("No bridge schema changes required.")
    print("G5 test: run bridge on baseline_uniform_channel_ctrl, verify theta_std ≈ 0")
    print("G6 test: run bridge on baseline_single_obstruction_ctrl, verify theta_std > 0")
    print("\nDone.")


if __name__ == "__main__":
    main()
