#!/usr/bin/env python3
"""Command-line interface for Stage 1 2D evaluation."""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from stage1_2d.config import load_config
from stage1_2d.sweep import run_sweep, run_smoke_test


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Stage 1: 2D cold-plate evaluation engine"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Smoke test command
    smoke_parser = subparsers.add_parser(
        "smoke",
        help="Run smoke test with minimal parameters"
    )
    smoke_parser.add_argument(
        "--output-dir",
        default="results/stage1_2d_smoke",
        help="Output directory (default: results/stage1_2d_smoke)"
    )
    
    # Sweep command
    sweep_parser = subparsers.add_parser(
        "sweep",
        help="Run parameter sweep from config file"
    )
    sweep_parser.add_argument(
        "config",
        help="Path to YAML configuration file"
    )
    sweep_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output"
    )
    
    args = parser.parse_args()
    
    if args.command == "smoke":
        print("\n" + "=" * 60)
        print("STAGE 1 SMOKE TEST")
        print("=" * 60 + "\n")
        results = run_smoke_test(args.output_dir)
        print(f"\nSmoke test completed: {len(results)} evaluations")
        return 0
    
    elif args.command == "sweep":
        config = load_config(args.config)
        results = run_sweep(config, verbose=not args.quiet)
        print(f"\nSweep completed: {len(results)} evaluations")
        return 0
    
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
