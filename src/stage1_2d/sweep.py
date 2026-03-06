"""Parameter sweep runner for Stage 1 evaluation.

Generates baseline geometries across parameter ranges and evaluates them.
"""

import itertools
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any
from .schemas import (
    SweepConfig, BaselineParams, BaselineFamily,
    EvaluationResult, SweepManifest
)
from .generators import generate_baseline_mask
from .evaluate import evaluate_mask
from .provenance import get_git_sha, get_git_status
from .metrics import get_metric_schema_version
from .io import (
    ensure_output_dir, save_mask, save_evaluation_result,
    save_metrics_csv, save_metrics_jsonl, save_sweep_manifest
)


def generate_param_combinations(
    family: BaselineFamily,
    param_ranges: Dict[str, List[Any]]
) -> List[Dict[str, Any]]:
    """Generate all combinations of parameters for a family.
    
    Args:
        family: Baseline family
        param_ranges: Parameter ranges for this family
        
    Returns:
        List of parameter dictionaries
    """
    family_key = family.value
    
    if family_key not in param_ranges:
        return [{}]
    
    family_params = param_ranges[family_key]
    
    # Get all parameter names and their ranges
    param_names = list(family_params.keys())
    param_values = [family_params[name] for name in param_names]
    
    # Generate all combinations
    combinations = []
    for combo in itertools.product(*param_values):
        param_dict = dict(zip(param_names, combo))
        combinations.append(param_dict)
    
    return combinations


def run_sweep(config: SweepConfig, verbose: bool = True) -> List[EvaluationResult]:
    """Run parameter sweep.
    
    Args:
        config: Sweep configuration
        verbose: Whether to print progress
        
    Returns:
        List of evaluation results
    """
    # Ensure output directory exists
    output_path = ensure_output_dir(config.output_dir)
    masks_dir = output_path / "masks"
    masks_dir.mkdir(exist_ok=True)
    results_dir = output_path / "results"
    results_dir.mkdir(exist_ok=True)
    
    if verbose:
        print(f"Running Stage 1 sweep")
        print(f"Output directory: {config.output_dir}")
        print(f"Grid: {config.grid.nx}x{config.grid.ny}")
        print(f"Families: {[f.value for f in config.families]}")
    
    # Track all results
    all_results = []
    seed = config.seed_start
    eval_count = 0
    
    # Iterate over families
    for family in config.families:
        if verbose:
            print(f"\nGenerating {family.value} baselines...")
        
        # Get parameter combinations
        param_combos = generate_param_combinations(family, config.param_ranges)
        
        if verbose:
            print(f"  {len(param_combos)} parameter combinations")
        
        # Generate and evaluate each combination
        for combo in param_combos:
            for sample_idx in range(config.num_samples_per_config):
                # Create baseline parameters
                baseline_params = BaselineParams(
                    family=family,
                    grid=config.grid,
                    seed=seed,
                    params=combo
                )
                
                # Generate mask
                try:
                    mask, gen_metadata = generate_baseline_mask(
                        family,
                        config.grid,
                        combo,
                        seed
                    )
                    
                    # Create mask ID
                    mask_id = f"{family.value}_s{seed}"
                    
                    # Save mask
                    mask_path = masks_dir / f"{mask_id}.npy"
                    save_mask(mask, str(mask_path))
                    
                    # Evaluate mask
                    result = evaluate_mask(
                        mask,
                        mask_id,
                        baseline_params
                    )
                    
                    # Save individual result
                    result_path = results_dir / f"{mask_id}.json"
                    save_evaluation_result(result, str(result_path))
                    
                    all_results.append(result)
                    eval_count += 1
                    
                    if verbose and eval_count % 10 == 0:
                        print(f"  Evaluated {eval_count} masks...")
                
                except Exception as e:
                    if verbose:
                        print(f"  Error generating {family.value} with seed {seed}: {e}")
                
                seed += 1
    
    if verbose:
        print(f"\nCompleted {eval_count} evaluations")
    
    # Save aggregate outputs
    if all_results:
        # Save CSV
        csv_path = output_path / "metrics.csv"
        save_metrics_csv(all_results, str(csv_path))
        if verbose:
            print(f"Saved metrics CSV: {csv_path}")
        
        # Save JSONL
        jsonl_path = output_path / "metrics.jsonl"
        save_metrics_jsonl(all_results, str(jsonl_path))
        if verbose:
            print(f"Saved metrics JSONL: {jsonl_path}")
    
    # Create and save manifest
    manifest = SweepManifest(
        timestamp=datetime.now(timezone.utc).isoformat(),
        git_sha=get_git_sha(),
        config=config,
        num_evaluations=eval_count,
        metric_schema_version=get_metric_schema_version()
    )
    
    manifest_path = output_path / "run_manifest.json"
    save_sweep_manifest(manifest, str(manifest_path))
    if verbose:
        print(f"Saved manifest: {manifest_path}")
        git_status = get_git_status()
        if git_status:
            print(f"Git status: {git_status}")
    
    return all_results


def run_smoke_test(output_dir: str = "results/stage1_2d_smoke") -> List[EvaluationResult]:
    """Run a quick smoke test with minimal parameters.
    
    Args:
        output_dir: Output directory for smoke test
        
    Returns:
        List of evaluation results
    """
    from .schemas import GridConfig
    
    # Minimal grid
    grid = GridConfig(nx=100, ny=100, dx=1e-4, dy=1e-4)
    
    # Minimal param ranges (one configuration per family)
    param_ranges = {
        "straight_channel": {
            "num_channels": [4],
            "channel_width_fraction": [0.5],
        },
        "serpentine_channel": {
            "channel_width_px": [10],
            "turn_radius_px": [15],
            "num_passes": [3],
        },
        "pin_fin": {
            "pin_diameter_px": [8],
            "pin_spacing_px": [25],
            "offset_rows": [True],
        },
        "gyroid_2d": {
            "wavelength_px": [25],
            "threshold": [0.0],
        },
        "diamond_2d": {
            "wavelength_px": [25],
            "threshold": [0.0],
        },
        "primitive_2d": {
            "wavelength_px": [25],
            "threshold": [0.0],
        },
    }
    
    # All families
    families = [
        BaselineFamily.STRAIGHT_CHANNEL,
        BaselineFamily.SERPENTINE_CHANNEL,
        BaselineFamily.PIN_FIN,
        BaselineFamily.GYROID_2D,
        BaselineFamily.DIAMOND_2D,
        BaselineFamily.PRIMITIVE_2D,
    ]
    
    config = SweepConfig(
        output_dir=output_dir,
        grid=grid,
        families=families,
        param_ranges=param_ranges,
        seed_start=42,
        num_samples_per_config=1
    )
    
    print("=" * 60)
    print("STAGE 1 SMOKE TEST")
    print("=" * 60)
    
    results = run_sweep(config, verbose=True)
    
    print("=" * 60)
    print(f"SMOKE TEST COMPLETE: {len(results)} evaluations")
    print("=" * 60)
    
    return results
