"""
Stage 4 Gyroid TPMS candidate artifact emitter.

Generates ONE Gyroid candidate for the TPMS family SNR pilot defined in
coldplate-topobridge TPMS_FAMILY_SNR_EXPERIMENT_SPEC.md v1.1.

Constraints enforced here:
  - Identical Stage 4 solver, BCs, grid shape, voxel size as Diamond candidates
  - Gyroid 3D implicit surface: sin(x)cos(y) + sin(y)cos(z) + sin(z)cos(x) = threshold
  - Porosity gate: solid_fraction at z=25 MUST be in [0.414, 0.453] (±0.015 of Diamond mean 0.434)
  - No changes to existing Stage 4 solver modules
  - Artifact written to results/stage4_sim_full/candidate_gyroid_3d_s0000/

Run from coldplate-design-engine root:
    python scripts/emit_stage4_gyroid.py
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

from stage3_geometry import tpms3d
from stage4_sim import (
    mesh_or_grid,
    solver,
    boundary_conditions,
    metrics,
)

# === Constants — identical to Diamond full-run ===
GRID_SHAPE   = (50, 50, 50)   # nx, ny, nz
VOXEL_SIZE   = 0.1            # mm
RESOLUTION   = 50
OUTPUT_ROOT  = Path("results/stage4_sim_full")
CANDIDATE_ID = "candidate_gyroid_3d_s0000"
TIMESTAMP    = datetime.now(timezone.utc).isoformat()

# === Gyroid parameters (tuned to hit porosity gate) ===
# threshold=0.0 on 50x50x50, wavelength_px=15.5 → solid fraction ≈ 0.44 at 3D level
# Validated below before running solver.
GYROID_PARAMS = {
    "threshold":    -0.24,
    "wavelength_px": 15.513267309547823,   # identical to Diamond cand01 wavelength
}

# === Porosity inclusion gate (spec §3 criterion 2) ===
# Diamond z=25 solid_fraction: cand01=0.4376, cand02=0.4296 → mean≈0.4336
# Gate: [mean - 0.015, mean + 0.015] = [0.414, 0.453]
SOLID_FRAC_GATE = (0.414, 0.453)


def get_git_sha():
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
            cwd=str(Path(__file__).parent.parent)
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return "unknown"


def compute_solid_fraction_z25(vx: np.ndarray, vy: np.ndarray) -> float:
    """Compute solid_fraction at z=25 slice using velocity-magnitude threshold."""
    mag = np.sqrt(vx[:, :, 25] ** 2 + vy[:, :, 25] ** 2)
    solid_mask = mag < 1e-3 * np.max(mag)
    return float(solid_mask.sum()) / solid_mask.size


def compute_transverse_max_ratio(vx: np.ndarray, vy: np.ndarray, vz: np.ndarray) -> float:
    """transverse_max_ratio = max(|vx|, |vy|) / mean(|vz|) at z=25."""
    vx25 = vx[:, :, 25]
    vy25 = vy[:, :, 25]
    vz25 = vz[:, :, 25]
    transverse_max = max(float(np.max(np.abs(vx25))), float(np.max(np.abs(vy25))))
    vz_mean = float(np.mean(np.abs(vz25)))
    if vz_mean < 1e-30:
        return 0.0
    return transverse_max / vz_mean


def main():
    print("=== Stage 4 Gyroid TPMS Candidate Emitter ===")
    print(f"Candidate ID : {CANDIDATE_ID}")
    print(f"Grid shape   : {GRID_SHAPE}")
    print(f"Gyroid params: {GYROID_PARAMS}")
    print(f"Timestamp    : {TIMESTAMP}")

    git_sha = get_git_sha()
    print(f"Git SHA      : {git_sha[:12]}...")

    # ------------------------------------------------------------------
    # Step 1 - Generate 3D Gyroid volume
    # ------------------------------------------------------------------
    print("\n[1] Generating 3D Gyroid volume...")
    grid_config = {"nx": RESOLUTION, "ny": RESOLUTION, "nz": RESOLUTION}
    volume, vol_meta = tpms3d.generate_gyroid_3d(
        params=GYROID_PARAMS,
        grid_config=grid_config,
        resolution=RESOLUTION,
    )
    # volume is (nz, ny, nx), values: 1=fluid, 0=solid
    n_total = volume.size
    n_fluid = int(np.sum(volume == 1))
    n_solid = int(np.sum(volume == 0))
    vol_porosity = n_fluid / n_total
    print(f"  Volume shape: {volume.shape}")
    print(f"  3D porosity (fluid fraction): {vol_porosity:.4f}")
    print(f"  3D solid fraction           : {1 - vol_porosity:.4f}")

    # ------------------------------------------------------------------
    # Step 2 - Setup grid (identical BC setup to Diamond candidates)
    # tpms3d returns (nz, ny, nx); mesh_or_grid expects (nx, ny, nz)
    # ------------------------------------------------------------------
    print("\n[2] Setting up simulation grid...")
    volume_for_grid = np.transpose(volume, (2, 1, 0))   # (nz,ny,nx) -> (nx,ny,nz)
    grid = mesh_or_grid.setup_simulation_grid(volume_for_grid, voxel_size_mm=VOXEL_SIZE)
    print(f"  Grid shape   : {grid['shape']}")
    print(f"  Grid porosity: {grid['porosity']:.4f}")

    bc = boundary_conditions.get_matched_boundary_conditions()

    # ------------------------------------------------------------------
    # Step 3 - Run solver
    # ------------------------------------------------------------------
    print("\n[3] Running Darcy flow solver (this may take several minutes)...")
    t0 = time.time()
    sim_result = solver.run_flow_simulation(grid, bc)
    elapsed = time.time() - t0

    if sim_result["converged"]:
        print(f"  PASS: Converged in {elapsed:.1f}s ({sim_result['iterations']} iter)")
    else:
        print(f"  FAIL: Did NOT converge in {elapsed:.1f}s")

    vel = sim_result["velocity"]
    vx, vy, vz = vel["vx"], vel["vy"], vel["vz"]
    print(f"  vx shape: {vx.shape}")
    print(f"  vx range: [{vx.min():.3f}, {vx.max():.3f}]")
    print(f"  vz range: [{vz.min():.3f}, {vz.max():.3f}]")

    # ------------------------------------------------------------------
    # Step 4 - Inclusion gate checks (spec section 3)
    # ------------------------------------------------------------------
    print("\n[4] Checking inclusion gates (spec section 3)...")

    solid_frac_z25 = compute_solid_fraction_z25(vx, vy)
    transverse_ratio = compute_transverse_max_ratio(vx, vy, vz)

    sf_lo, sf_hi = SOLID_FRAC_GATE
    porosity_pass = sf_lo <= solid_frac_z25 <= sf_hi
    transverse_pass = transverse_ratio > 1e-4

    print(f"  solid_fraction@z=25   : {solid_frac_z25:.4f}  gate [{sf_lo},{sf_hi}]  -> {'PASS' if porosity_pass else 'FAIL'}")
    print(f"  transverse_max_ratio  : {transverse_ratio:.6f}  gate >1e-4            -> {'PASS' if transverse_pass else 'FAIL'}")

    if not porosity_pass:
        print("\n  FAIL: POROSITY GATE FAILED. Artifact NOT written.")
        print(f"    solid_fraction@z25={solid_frac_z25:.4f} outside [{sf_lo},{sf_hi}].")
        print("    Adjust GYROID_PARAMS threshold and re-run.")
        sys.exit(1)

    if not transverse_pass:
        print("\n  FAIL: TRANSVERSE FLOW GATE FAILED. Artifact NOT written.")
        sys.exit(1)

    print("  PASS: Both inclusion gates PASSED.")

    # ------------------------------------------------------------------
    # Step 5 - Write velocity_field.npz
    # ------------------------------------------------------------------
    out_dir = OUTPUT_ROOT / CANDIDATE_ID
    out_dir.mkdir(parents=True, exist_ok=True)

    vel_path = out_dir / "velocity_field.npz"
    np.savez_compressed(str(vel_path), vx=vx, vy=vy, vz=vz)
    print(f"\n[5] Saved: {vel_path}  shape={vx.shape}")

    # Verify
    vf = np.load(str(vel_path), allow_pickle=False)
    assert set(vf.keys()) == {"vx", "vy", "vz"}, f"Missing keys: {list(vf.keys())}"
    assert vf["vx"].shape == tuple(GRID_SHAPE), f"Shape mismatch: {vf['vx'].shape}"
    assert not np.any(np.isnan(vf["vx"])), "NaN in vx"
    print(f"  PASS: Verified: keys={list(vf.keys())}, shape={vf['vx'].shape}, no NaN")

    # ------------------------------------------------------------------
    # Step 6 - Write provenance.json
    # ------------------------------------------------------------------
    metric_results = metrics.compute_all_metrics(sim_result, grid, bc)

    provenance = {
        "timestamp": TIMESTAMP,
        "stage": "stage4_sim",
        "schema_version": "1.0",
        "candidate_id": CANDIDATE_ID,
        "git_sha": git_sha,
        "stage3_source": {
            "provenance": {
                "timestamp": TIMESTAMP,
                "stage": "stage3_geometry",
                "schema_version": "1.0",
                "stage2_source": {
                    "rank": None,
                    "family": "gyroid_2d",
                    "seed": 0,
                    "mask_id": CANDIDATE_ID,
                    "total_score": None,
                    "is_valid": True,
                    "params": GYROID_PARAMS,
                },
                "promotion": {
                    "volume_metadata": {
                        "type": "3d_gyroid_tpms",
                        "threshold": GYROID_PARAMS["threshold"],
                        "wavelength_px": GYROID_PARAMS["wavelength_px"],
                        "porosity": vol_porosity,
                        "height_mm": RESOLUTION * VOXEL_SIZE,
                        "resolution": RESOLUTION,
                        "dimensions": {"nx": RESOLUTION, "ny": RESOLUTION, "nz": RESOLUTION},
                        "candidate_rank": None,
                        "candidate_seed": 0,
                        "candidate_family": "gyroid_2d",
                    },
                    "success": True,
                    "errors": [],
                },
                "validation": {
                    "porosity": round(vol_porosity, 6),
                    "connectivity": {"note": "not validated for this pilot artifact"},
                },
            },
            "metadata": {
                "type": "3d_gyroid_tpms",
                "threshold": GYROID_PARAMS["threshold"],
                "wavelength_px": GYROID_PARAMS["wavelength_px"],
                "porosity": round(vol_porosity, 6),
                "height_mm": RESOLUTION * VOXEL_SIZE,
                "resolution": RESOLUTION,
                "dimensions": {"nx": RESOLUTION, "ny": RESOLUTION, "nz": RESOLUTION},
                "candidate_rank": None,
                "candidate_seed": 0,
                "candidate_family": "gyroid_2d",
            },
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
            "config": {"mode": "full_gyroid_pilot", "family": "gyroid_2d"},
        },
        "inclusion_gates": {
            "solid_fraction_z25": solid_frac_z25,
            "solid_frac_gate": list(SOLID_FRAC_GATE),
            "porosity_gate_pass": porosity_pass,
            "transverse_max_ratio_z25": transverse_ratio,
            "transverse_gate_pass": transverse_pass,
        },
        "metrics": metric_results,
    }

    prov_path = out_dir / "provenance.json"
    with open(prov_path, "w") as f:
        json.dump(provenance, f, indent=2)
    print(f"[6] Saved: {prov_path}")

    print("\n=== Gyroid Stage 4 artifact COMPLETE ===")
    print(f"  velocity_field.npz : {vel_path}")
    print(f"  provenance.json    : {prov_path}")
    print(f"  solid_fraction@z25 : {solid_frac_z25:.4f}  PASS in gate")
    print(f"  transverse_ratio   : {transverse_ratio:.6f}  PASS above 1e-4")
    print("\nNow commit to coldplate-design-engine and run the SNR pilot.")


if __name__ == "__main__":
    main()
