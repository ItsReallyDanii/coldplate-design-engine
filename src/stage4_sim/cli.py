"""
Command-line interface for Stage 4 simulation.

Usage:
    python src/stage4_sim/cli.py smoke
    python src/stage4_sim/cli.py run <stage3_dir> <output_dir> [--top-k K]
"""

import sys
import argparse
from pathlib import Path
import time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from stage4_sim import (
    load_geometry,
    mesh_or_grid,
    solver,
    boundary_conditions,
    metrics,
    compare,
    io,
    provenance
)


def run_smoke_test():
    """
    Run smoke test using Stage 3 smoke outputs.
    """
    print("=== Stage 4 Smoke Test ===\n")
    
    # Find Stage 3 smoke results
    stage3_dir = Path("results/stage3_geometry_smoke")
    if not stage3_dir.exists():
        print("ERROR: Stage 3 smoke results not found. Run Stage 3 smoke test first:")
        print("  python src/stage3_geometry/cli.py smoke")
        return False
    
    # Output directory
    output_dir = Path("results/stage4_sim_smoke")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load top 2 candidates
    print(f"Loading candidates from {stage3_dir}...")
    candidates = load_geometry.load_candidates_for_simulation(stage3_dir, top_k=2)
    print(f"Loaded {len(candidates)} candidates\n")
    
    # Get matched boundary conditions
    bc = boundary_conditions.get_matched_boundary_conditions()
    
    # Run simulation for each candidate
    results = []
    for i, candidate in enumerate(candidates):
        candidate_id = load_geometry.get_candidate_identifier(candidate)
        print(f"--- {candidate_id} ---")
        
        # Setup grid
        grid = mesh_or_grid.setup_simulation_grid(candidate['volume'])
        print(f"Grid: {grid['shape']}, porosity: {grid['porosity']:.3f}")
        
        # Run simulation
        print("Running flow simulation...")
        start_time = time.time()
        sim_result = solver.run_flow_simulation(grid, bc)
        elapsed = time.time() - start_time
        
        if sim_result['converged']:
            print(f"✓ Converged in {sim_result['iterations']} iterations ({elapsed:.2f}s)")
        else:
            print(f"✗ Did not converge ({elapsed:.2f}s)")
        
        # Compute metrics
        print("Computing metrics...")
        metric_results = metrics.compute_all_metrics(sim_result, grid, bc)
        
        # Display key results
        dp = metric_results['simulated_quantities']['pressure_drop']['pressure_drop_pa']
        Q = metric_results['simulated_quantities']['flow_rate']['flow_rate_lpm']
        print(f"Pressure drop: {dp:.2f} Pa (SIMULATED)")
        print(f"Flow rate: {Q:.4f} L/min (SIMULATED)")
        
        # Save results
        result = {
            'candidate_id': candidate_id,
            'candidate_data': candidate,
            'grid': grid,
            'boundary_conditions': bc,
            'simulation_result': sim_result,
            'metrics': metric_results
        }
        results.append(result)
        
        # Save candidate results
        io.save_candidate_results(result, output_dir, candidate_id)
        
        # Save provenance
        prov = provenance.create_provenance_record(
            candidate_id, candidate, sim_result, metric_results,
            bc, grid, {'mode': 'smoke'}
        )
        provenance.save_provenance(prov, output_dir / candidate_id / "provenance.json")
        
        print()
    
    # Comparison
    print("=== Comparison ===")
    matched = compare.verify_matched_conditions(results)
    if matched['matched']:
        print("✓ All candidates simulated under matched conditions")
    else:
        print(f"✗ Mismatches: {matched['mismatches']}")
    
    comp_metrics = compare.compute_comparison_metrics(results)
    summary_text = compare.generate_comparison_summary(results, comp_metrics, matched)
    
    # Save comparison
    io.save_comparison_results(output_dir, comp_metrics, matched, summary_text)
    io.save_stage4_summary(output_dir, results)
    
    # Save manifest
    candidate_ids = [r['candidate_id'] for r in results]
    io.save_run_manifest(output_dir, {'mode': 'smoke', 'top_k': 2}, candidate_ids)
    
    print(f"\n=== Smoke Test Complete ===")
    print(f"Results saved to {output_dir}")
    print(f"Summary: {output_dir / 'comparison_summary.md'}")
    
    return True


def run_full_simulation(stage3_dir: Path, output_dir: Path, top_k: int = None):
    """
    Run full Stage 4 simulation on Stage 3 outputs.
    
    Args:
        stage3_dir: Path to Stage 3 results directory
        output_dir: Path to output directory
        top_k: Number of top candidates to simulate (None = all)
    """
    print("=== Stage 4 Simulation ===\n")
    
    if not stage3_dir.exists():
        print(f"ERROR: Stage 3 directory not found: {stage3_dir}")
        return False
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load candidates
    print(f"Loading candidates from {stage3_dir}...")
    candidates = load_geometry.load_candidates_for_simulation(stage3_dir, top_k=top_k)
    print(f"Loaded {len(candidates)} candidates\n")
    
    if len(candidates) == 0:
        print("ERROR: No candidates found")
        return False
    
    # Get matched boundary conditions
    bc = boundary_conditions.get_matched_boundary_conditions()
    print(f"Boundary conditions:")
    print(f"  Pressure drop: {bc['pressure_drop_pa']} Pa")
    print(f"  Fluid: water (ρ={bc['fluid_density_kg_m3']} kg/m³, μ={bc['fluid_viscosity_pa_s']} Pa·s)")
    print()
    
    # Run simulation for each candidate
    results = []
    for i, candidate in enumerate(candidates):
        candidate_id = load_geometry.get_candidate_identifier(candidate)
        print(f"[{i+1}/{len(candidates)}] {candidate_id}")
        
        # Setup grid
        grid = mesh_or_grid.setup_simulation_grid(candidate['volume'])
        print(f"  Grid: {grid['shape']}, porosity: {grid['porosity']:.3f}")
        
        # Run simulation
        print("  Running flow simulation...")
        start_time = time.time()
        sim_result = solver.run_flow_simulation(grid, bc)
        elapsed = time.time() - start_time
        
        if sim_result['converged']:
            print(f"  ✓ Converged ({elapsed:.2f}s)")
        else:
            print(f"  ✗ Did not converge ({elapsed:.2f}s)")
            continue  # Skip if not converged
        
        # Compute metrics
        metric_results = metrics.compute_all_metrics(sim_result, grid, bc)
        
        # Display key results
        dp = metric_results['simulated_quantities']['pressure_drop']['pressure_drop_pa']
        Q = metric_results['simulated_quantities']['flow_rate']['flow_rate_lpm']
        R = metric_results['simulated_quantities']['hydraulic_resistance']['hydraulic_resistance_pa_s_m3']
        print(f"  ΔP: {dp:.2f} Pa, Q: {Q:.4f} L/min, R: {R:.2e} Pa·s/m³")
        
        # Save results
        result = {
            'candidate_id': candidate_id,
            'candidate_data': candidate,
            'grid': grid,
            'boundary_conditions': bc,
            'simulation_result': sim_result,
            'metrics': metric_results
        }
        results.append(result)
        
        # Save candidate results
        io.save_candidate_results(result, output_dir, candidate_id)
        
        # Save provenance
        prov = provenance.create_provenance_record(
            candidate_id, candidate, sim_result, metric_results,
            bc, grid, {'mode': 'full', 'top_k': top_k}
        )
        provenance.save_provenance(prov, output_dir / candidate_id / "provenance.json")
        
        print()
    
    if len(results) == 0:
        print("ERROR: No candidates successfully simulated")
        return False
    
    # Comparison
    print("=== Generating Comparison ===")
    matched = compare.verify_matched_conditions(results)
    if matched['matched']:
        print("✓ All candidates simulated under matched conditions")
    else:
        print(f"✗ Mismatches: {matched['mismatches']}")
    
    comp_metrics = compare.compute_comparison_metrics(results)
    summary_text = compare.generate_comparison_summary(results, comp_metrics, matched)
    
    # Save comparison
    io.save_comparison_results(output_dir, comp_metrics, matched, summary_text)
    io.save_stage4_summary(output_dir, results)
    
    # Save manifest
    candidate_ids = [r['candidate_id'] for r in results]
    io.save_run_manifest(
        output_dir,
        {'mode': 'full', 'top_k': top_k, 'stage3_dir': str(stage3_dir)},
        candidate_ids,
        git_sha=provenance.get_git_sha()
    )
    
    print(f"\n=== Stage 4 Simulation Complete ===")
    print(f"Results saved to {output_dir}")
    print(f"Summary: {output_dir / 'comparison_summary.md'}")
    print(f"Manifest: {output_dir / 'run_manifest.json'}")
    
    return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Stage 4: Flow simulation validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run smoke test
  python src/stage4_sim/cli.py smoke
  
  # Run on Stage 3 smoke outputs
  python src/stage4_sim/cli.py run results/stage3_geometry_smoke results/stage4_sim
  
  # Run on top 5 candidates
  python src/stage4_sim/cli.py run results/stage3_geometry results/stage4_sim --top-k 5
"""
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Smoke test command
    subparsers.add_parser('smoke', help='Run smoke test')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run full simulation')
    run_parser.add_argument('stage3_dir', type=Path, help='Stage 3 results directory')
    run_parser.add_argument('output_dir', type=Path, help='Output directory')
    run_parser.add_argument('--top-k', type=int, default=None, help='Number of top candidates to simulate')
    
    args = parser.parse_args()
    
    if args.command == 'smoke':
        success = run_smoke_test()
    elif args.command == 'run':
        success = run_full_simulation(args.stage3_dir, args.output_dir, args.top_k)
    else:
        parser.print_help()
        return 1
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
