"""
Command-line interface for Stage 5 thermal validation.
"""

import os
import sys
import json
import argparse
from typing import Optional, Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from stage5_thermal import (
    load_cases,
    boundary_conditions as bc_module,
    coupling,
    metrics as metrics_module,
    compare as compare_module,
    io as io_module,
    provenance as prov_module
)


def run_thermal_validation(
    stage4_dir: str,
    output_dir: str,
    top_k: Optional[int] = None,
    family_filter: Optional[str] = None,
    mode: str = 'full'
) -> Dict[str, Any]:
    """
    Run thermal validation on Stage 4 candidates.
    
    Args:
        stage4_dir: Path to Stage 4 results directory
        output_dir: Path to output directory
        top_k: Number of top candidates to evaluate
        family_filter: Filter by family name
        mode: Execution mode
        
    Returns:
        Summary dictionary
    """
    print(f"=== Stage 5 Thermal Validation ===")
    print(f"Stage 4 directory: {stage4_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Mode: {mode}")
    print()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load candidates
    print("Loading Stage 4 candidates...")
    candidates = load_cases.load_candidates_for_thermal(
        stage4_dir, top_k, family_filter
    )
    print(f"Loaded {len(candidates)} candidates")
    print()
    
    if not candidates:
        print("ERROR: No candidates loaded!")
        return {'status': 'failed', 'reason': 'no_candidates'}
    
    # Get matched boundary conditions
    bc = bc_module.get_matched_thermal_boundary_conditions()
    
    # Solver parameters
    solver_params = {'tol': 1e-6}
    
    # Process each candidate
    results = []
    
    for i, candidate in enumerate(candidates, 1):
        cand_id = candidate['candidate_id']
        print(f"[{i}/{len(candidates)}] Processing {cand_id}...")
        
        try:
            # Run coupled thermal simulation
            thermal_result = coupling.run_coupled_thermal_simulation(
                candidate, bc, solver_params
            )
            
            print(f"  Thermal solver: {'CONVERGED' if thermal_result['converged'] else 'FAILED'}")
            print(f"  Solve time: {thermal_result['solve_time_s']:.2f}s")
            
            if not thermal_result['converged']:
                print(f"  WARNING: Solver did not converge!")
            
            # Compute metrics
            cand_metrics = metrics_module.compute_all_thermal_metrics(
                thermal_result, candidate, bc
            )
            
            # Extract key metrics for display
            thermal_sim = cand_metrics['thermal_simulated_quantities']
            T_max = thermal_sim['temperature_statistics']['T_max_c']
            R_th = thermal_sim['thermal_resistance']['thermal_resistance_k_w']
            
            print(f"  Peak temperature: {T_max:.2f} °C")
            print(f"  Thermal resistance: {R_th:.6f} K/W")
            
            # Create provenance
            prov = prov_module.create_stage5_provenance(
                candidate, bc, solver_params, thermal_result
            )
            
            # Save results
            io_module.save_candidate_results(
                output_dir, cand_id, thermal_result, cand_metrics, prov, bc
            )
            
            # Store for comparison
            results.append({
                'candidate_id': cand_id,
                'thermal_result': thermal_result,
                'metrics': cand_metrics,
                'provenance': prov,
                'boundary_conditions': bc
            })
            
            print()
            
        except Exception as e:
            import traceback
            print(f"  ERROR: {e}")
            print(f"  Traceback:")
            traceback.print_exc()
            print()
            continue
    
    if not results:
        print("ERROR: No successful results!")
        return {'status': 'failed', 'reason': 'no_successful_results'}
    
    # Compare candidates
    print("Comparing candidates...")
    comparison = compare_module.compute_comparison_metrics(results)
    summary_text = compare_module.generate_comparison_summary(results, comparison)
    
    # Save comparison
    io_module.save_comparison_results(output_dir, comparison, summary_text)
    
    # Save Stage 5 summary
    io_module.save_stage5_summary(output_dir, results)
    
    # Save run manifest
    manifest = prov_module.create_run_manifest(
        mode, len(results),
        [r['candidate_id'] for r in results],
        {'top_k': top_k, 'family_filter': family_filter}
    )
    
    manifest_path = os.path.join(output_dir, 'run_manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Results saved to: {output_dir}")
    print()
    print("=== Summary ===")
    print(f"Candidates processed: {len(results)}")
    print(f"Best thermal resistance: {comparison['thermal_resistance']['best_k_w']:.6f} K/W")
    print(f"Best candidate: {comparison['thermal_resistance']['best_candidate']}")
    print()
    
    return {
        'status': 'success',
        'n_candidates': len(results),
        'comparison': comparison
    }


def smoke_test():
    """Run smoke test on Stage 4 smoke outputs."""
    print("Running Stage 5 smoke test...")
    print()
    
    # Use Stage 4 smoke outputs
    stage4_dir = 'results/stage4_sim_smoke'
    output_dir = 'results/stage5_thermal_smoke'
    
    if not os.path.exists(stage4_dir):
        print(f"ERROR: Stage 4 smoke outputs not found: {stage4_dir}")
        print("Please run Stage 4 smoke test first:")
        print("  python src/stage4_sim/cli.py smoke")
        sys.exit(1)
    
    result = run_thermal_validation(
        stage4_dir, output_dir, top_k=2, mode='smoke'
    )
    
    if result['status'] == 'success':
        print("Smoke test PASSED!")
        sys.exit(0)
    else:
        print("Smoke test FAILED!")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Stage 5: Thermal Validation'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Smoke test
    subparsers.add_parser('smoke', help='Run smoke test')
    
    # Full run
    run_parser = subparsers.add_parser('run', help='Run thermal validation')
    run_parser.add_argument('stage4_dir', help='Stage 4 results directory')
    run_parser.add_argument('--output', '-o', default='results/stage5_thermal',
                          help='Output directory')
    run_parser.add_argument('--top-k', type=int, default=None,
                          help='Number of top candidates to evaluate')
    run_parser.add_argument('--family', default=None,
                          help='Filter by family name')
    
    args = parser.parse_args()
    
    if args.command == 'smoke':
        smoke_test()
    elif args.command == 'run':
        result = run_thermal_validation(
            args.stage4_dir,
            args.output,
            args.top_k,
            args.family,
            'full'
        )
        sys.exit(0 if result['status'] == 'success' else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
