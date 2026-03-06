"""Command-line interface for Stage 2 inverse design."""

import sys
import os
import argparse
import yaml

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from stage1_2d.schemas import GridConfig
from stage2_inverse.search_space import create_default_search_space
from stage2_inverse.objectives import create_default_objective
from stage2_inverse.sampler import RandomSearchSampler
from stage2_inverse.optimize import GeneticOptimizer
from stage2_inverse.compare import compare_methods
from stage2_inverse import io
from stage2_inverse.provenance import get_git_sha, get_git_status


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def run_smoke_test():
    """Run quick smoke test of Stage 2 system."""
    print("=" * 60)
    print("STAGE 2 SMOKE TEST")
    print("=" * 60)
    
    # Minimal configuration
    grid = GridConfig(nx=50, ny=50, dx=0.0001, dy=0.0001)
    search_space = create_default_search_space(grid)
    objective = create_default_objective()
    
    budget = 10  # Very small for smoke test
    seed = 42
    output_dir = "results/stage2_inverse_smoke"
    
    io.ensure_output_dir(output_dir)
    
    print(f"\nRunning smoke test with budget={budget}")
    print(f"Output: {output_dir}\n")
    
    # Run random search
    print("--- Random Search Baseline ---")
    random_sampler = RandomSearchSampler(search_space, objective, seed=seed)
    random_results = random_sampler.run(budget)
    random_best = random_sampler.get_best(k=3)
    
    # Run genetic optimizer
    print("\n--- Genetic Optimizer ---")
    genetic_opt = GeneticOptimizer(
        search_space, objective, seed=seed + 1,
        population_size=5  # Small for smoke test
    )
    genetic_results = genetic_opt.run(budget)
    genetic_best = genetic_opt.get_best(k=3)
    
    # Compare
    print("\n--- Comparison ---")
    comparison = compare_methods(
        [random_results, genetic_results],
        ["random_search", "genetic_algorithm"]
    )
    
    # Save results
    io.save_jsonl(random_results, f"{output_dir}/random_search.jsonl")
    io.save_jsonl(genetic_results, f"{output_dir}/genetic_algorithm.jsonl")
    io.save_best_candidates_csv(random_best, f"{output_dir}/random_best.csv", "random_search")
    io.save_best_candidates_csv(genetic_best, f"{output_dir}/genetic_best.csv", "genetic_algorithm")
    io.save_json(comparison.to_dict(), f"{output_dir}/comparison.json")
    io.save_text(comparison.generate_summary(), f"{output_dir}/comparison_summary.md")
    
    # Manifest
    manifest = io.create_run_manifest(
        method_name="smoke_test",
        search_space_dict=search_space.to_dict(),
        objective_dict=objective.to_dict(),
        budget=budget,
        seed=seed,
        num_evaluations=len(random_results) + len(genetic_results),
        git_sha=get_git_sha()
    )
    io.save_json(manifest, f"{output_dir}/run_manifest.json")
    
    print("\n" + "=" * 60)
    print(f"SMOKE TEST COMPLETE")
    print(f"Random best: {random_best[0]['total_score']:.4f}" if random_best else "No valid candidates")
    print(f"Genetic best: {genetic_best[0]['total_score']:.4f}" if genetic_best else "No valid candidates")
    print(f"Output: {output_dir}")
    print("=" * 60)


def run_optimize(config_path: str):
    """Run optimization with configuration file.
    
    Args:
        config_path: Path to YAML configuration file
    """
    config = load_config(config_path)
    
    print("=" * 60)
    print("STAGE 2 OPTIMIZATION")
    print("=" * 60)
    print(f"Config: {config_path}")
    
    # Parse configuration
    grid_config = config.get('grid', {})
    grid = GridConfig(
        nx=grid_config.get('nx', 100),
        ny=grid_config.get('ny', 100),
        dx=grid_config.get('dx', 0.0001),
        dy=grid_config.get('dy', 0.0001)
    )
    
    budget = config.get('budget', 100)
    seed = config.get('seed', 42)
    output_dir = config.get('output_dir', 'results/stage2_inverse')
    method = config.get('method', 'genetic')
    
    # GA-specific params
    population_size = config.get('population_size', 20)
    
    io.ensure_output_dir(output_dir)
    
    print(f"Grid: {grid.nx}x{grid.ny}")
    print(f"Budget: {budget}")
    print(f"Method: {method}")
    print(f"Seed: {seed}")
    print(f"Output: {output_dir}\n")
    
    # Setup
    search_space = create_default_search_space(grid)
    objective = create_default_objective()
    
    # Run optimization
    if method == "random":
        print("Running Random Search...")
        sampler = RandomSearchSampler(search_space, objective, seed=seed)
        results = sampler.run(budget)
        best = sampler.get_best(k=10)
        method_name = "random_search"
    
    elif method == "genetic":
        print("Running Genetic Algorithm...")
        optimizer = GeneticOptimizer(
            search_space, objective, seed=seed,
            population_size=population_size
        )
        results = optimizer.run(budget)
        best = optimizer.get_best(k=10)
        method_name = "genetic_algorithm"
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # Save results
    print("\nSaving results...")
    io.save_jsonl(results, f"{output_dir}/{method_name}_results.jsonl")
    io.save_best_candidates_csv(best, f"{output_dir}/{method_name}_best.csv", method_name)
    
    manifest = io.create_run_manifest(
        method_name=method_name,
        search_space_dict=search_space.to_dict(),
        objective_dict=objective.to_dict(),
        budget=budget,
        seed=seed,
        num_evaluations=len(results),
        git_sha=get_git_sha()
    )
    io.save_json(manifest, f"{output_dir}/run_manifest.json")
    
    print("\n" + "=" * 60)
    print(f"OPTIMIZATION COMPLETE")
    print(f"Valid candidates: {len(best)}")
    if best:
        print(f"Best score: {best[0]['total_score']:.4f}")
        print(f"Best family: {best[0]['family']}")
    print(f"Output: {output_dir}")
    print("=" * 60)


def run_compare(config_path: str):
    """Run comparison of random search vs inverse design.
    
    Args:
        config_path: Path to YAML configuration file
    """
    config = load_config(config_path)
    
    print("=" * 60)
    print("STAGE 2 COMPARISON")
    print("=" * 60)
    print(f"Config: {config_path}")
    
    # Parse configuration
    grid_config = config.get('grid', {})
    grid = GridConfig(
        nx=grid_config.get('nx', 100),
        ny=grid_config.get('ny', 100),
        dx=grid_config.get('dx', 0.0001),
        dy=grid_config.get('dy', 0.0001)
    )
    
    budget = config.get('budget', 100)
    seed = config.get('seed', 42)
    output_dir = config.get('output_dir', 'results/stage2_inverse_comparison')
    population_size = config.get('population_size', 20)
    
    io.ensure_output_dir(output_dir)
    
    print(f"Grid: {grid.nx}x{grid.ny}")
    print(f"Budget per method: {budget}")
    print(f"Output: {output_dir}\n")
    
    # Setup
    search_space = create_default_search_space(grid)
    objective = create_default_objective()
    
    # Run random search
    print("--- Random Search Baseline ---")
    random_sampler = RandomSearchSampler(search_space, objective, seed=seed)
    random_results = random_sampler.run(budget)
    random_best = random_sampler.get_best(k=10)
    
    # Run genetic algorithm
    print("\n--- Genetic Algorithm ---")
    genetic_opt = GeneticOptimizer(
        search_space, objective, seed=seed + 1000,
        population_size=population_size
    )
    genetic_results = genetic_opt.run(budget)
    genetic_best = genetic_opt.get_best(k=10)
    
    # Compare
    print("\n--- Comparison ---")
    comparison = compare_methods(
        [random_results, genetic_results],
        ["random_search", "genetic_algorithm"],
        top_k=10
    )
    
    # Save results
    print("\nSaving results...")
    io.save_jsonl(random_results, f"{output_dir}/random_search_results.jsonl")
    io.save_jsonl(genetic_results, f"{output_dir}/genetic_algorithm_results.jsonl")
    io.save_best_candidates_csv(random_best, f"{output_dir}/random_best.csv", "random_search")
    io.save_best_candidates_csv(genetic_best, f"{output_dir}/genetic_best.csv", "genetic_algorithm")
    io.save_json(comparison.to_dict(), f"{output_dir}/comparison.json")
    io.save_text(comparison.generate_summary(), f"{output_dir}/comparison_summary.md")
    
    # Combined best candidates
    combined_best = random_best + genetic_best
    combined_best = sorted(combined_best, key=lambda x: x.get("total_score", float('-inf')), reverse=True)[:20]
    io.save_best_candidates_csv(combined_best, f"{output_dir}/best_candidates.csv", "combined")
    
    # Manifest
    manifest = io.create_run_manifest(
        method_name="comparison",
        search_space_dict=search_space.to_dict(),
        objective_dict=objective.to_dict(),
        budget=budget * 2,  # Total budget across both methods
        seed=seed,
        num_evaluations=len(random_results) + len(genetic_results),
        git_sha=get_git_sha()
    )
    manifest["methods"] = ["random_search", "genetic_algorithm"]
    manifest["budget_per_method"] = budget
    io.save_json(manifest, f"{output_dir}/run_manifest.json")
    
    print("\n" + comparison.generate_summary())
    
    print("\n" + "=" * 60)
    print(f"COMPARISON COMPLETE")
    print(f"Output: {output_dir}")
    print("=" * 60)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Stage 2 Inverse Design - Cold Plate Optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick smoke test
  python src/stage2_inverse/cli.py smoke
  
  # Run optimization with config
  python src/stage2_inverse/cli.py optimize configs/stage2_default.yaml
  
  # Run comparison
  python src/stage2_inverse/cli.py compare configs/stage2_default.yaml
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Smoke test command
    subparsers.add_parser('smoke', help='Run quick smoke test')
    
    # Optimize command
    optimize_parser = subparsers.add_parser('optimize', help='Run optimization')
    optimize_parser.add_argument('config', help='Path to config YAML file')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare methods')
    compare_parser.add_argument('config', help='Path to config YAML file')
    
    args = parser.parse_args()
    
    if args.command == 'smoke':
        run_smoke_test()
    elif args.command == 'optimize':
        run_optimize(args.config)
    elif args.command == 'compare':
        run_compare(args.config)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
