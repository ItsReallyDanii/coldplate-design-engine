"""
Command-line interface for Stage 6 structural screening.
"""

import os
import sys
import json
import argparse
import numpy as np
from typing import Optional, Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from stage6_structural import (
    load_cases,
    material_models,
    manufacturability,
    screening,
    metrics as metrics_module,
    compare as compare_module,
    io as io_module,
    provenance as prov_module
)


def reconstruct_volume_from_stage3(stage3_metadata: Dict[str, Any]) -> np.ndarray:
    """
    Load actual volume array from Stage 3 geometry.
    
    Args:
        stage3_metadata: Stage 3 geometry metadata
        
    Returns:
        Volume array (True=fluid, False=solid)
    """
    # Try to load actual geometry from Stage 3 exports
    provenance = stage3_metadata.get('provenance', {})
    exports = provenance.get('exports', {})
    raw_path = exports.get('raw', None)
    
    if raw_path and os.path.exists(raw_path):
        # Load actual geometry
        print(f"  Loading actual geometry from: {raw_path}")
        volume = np.load(raw_path)
        # Convert to boolean (fluid=True, solid=False)
        # Stage 3 exports use 1=fluid, 0=solid
        volume = volume.astype(bool)
        print(f"  Loaded geometry: shape={volume.shape}, porosity={volume.sum()/volume.size:.3f}")
        return volume
    
    # Fallback: if path not found, create synthetic volume
    # This maintains backward compatibility for old results
    validation = stage3_metadata.get('validation', {})
    bbox = validation.get('bounding_box', {})
    dims_voxels = bbox.get('dimensions_voxels', {})
    
    nx = dims_voxels.get('nx', 50)
    ny = dims_voxels.get('ny', 50)
    nz = dims_voxels.get('nz', 50)
    
    porosity = validation.get('porosity', 0.5)
    
    if raw_path:
        print(f"  WARNING: Actual geometry file not found at {raw_path}, using synthetic volume")
    else:
        print(f"  WARNING: Actual geometry path not found in metadata, using synthetic volume")
    volume = np.random.random((nx, ny, nz)) < porosity
    
    return volume


def run_structural_screening(
    stage5_dir: str,
    output_dir: str,
    top_k: Optional[int] = None,
    family_filter: Optional[str] = None,
    material_name: str = 'aluminum_6061',
    mode: str = 'full'
) -> Dict[str, Any]:
    """
    Run structural screening on Stage 5 candidates.
    
    Args:
        stage5_dir: Path to Stage 5 results directory
        output_dir: Path to output directory
        top_k: Number of top candidates to evaluate
        family_filter: Filter by family name
        material_name: Material to use
        mode: Execution mode
        
    Returns:
        Summary dictionary
    """
    print(f"=== Stage 6 Structural Screening ===")
    print(f"Stage 5 directory: {stage5_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Material: {material_name}")
    print(f"Mode: {mode}")
    print()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load candidates
    print("Loading Stage 5 candidates...")
    candidates = load_cases.load_candidates_for_structural(
        stage5_dir, top_k, family_filter
    )
    print(f"Loaded {len(candidates)} candidates")
    print()
    
    if not candidates:
        print("ERROR: No candidates loaded!")
        return {'status': 'failed', 'reason': 'no_candidates'}
    
    # Get material properties
    material = material_models.get_material_properties(material_name)
    
    # Manufacturability requirements
    requirements = {
        'min_wall_thickness_mm': 0.5,
        'min_feature_size_mm': 0.5,
        'max_unsupported_mm': 10.0
    }
    
    # Process each candidate
    all_metrics = []
    
    for i, candidate in enumerate(candidates, 1):
        cand_id = candidate['candidate_id']
        print(f"[{i}/{len(candidates)}] Screening {cand_id}...")
        
        try:
            # Extract data
            metrics_stage5 = candidate['metrics']
            provenance = candidate['provenance']
            bc = candidate['boundary_conditions']
            
            # Get Stage 3 geometry metadata
            stage3_metadata = provenance['stage4_source']['provenance']['stage3_source']
            
            # Reconstruct volume (simplified for screening)
            volume = reconstruct_volume_from_stage3(stage3_metadata)
            
            # Extract validation data from nested provenance structure
            # Stage 3 stores validation at stage3_metadata['provenance']['validation']
            stage3_prov = stage3_metadata.get('provenance', {})
            validation = stage3_prov.get('validation', {})
            feature_sizes = validation.get('feature_sizes', {})
            
            # Calculate voxel size from feature sizes
            # min_channel_diameter_mm = 2 voxels × voxel_size_mm
            min_channel = feature_sizes.get('min_channel_diameter_mm', 0.0)
            if min_channel > 0:
                voxel_size_mm = min_channel / 2.0
            else:
                voxel_size_mm = 0.1  # Fallback default
            
            # Extract geometry info for structural analysis
            bbox = validation.get('bounding_box', {})
            dims_mm = bbox.get('dimensions_mm', {})
            
            geometry_info = {
                'domain_size_mm': [
                    dims_mm.get('x', 5.0),
                    dims_mm.get('y', 5.0),
                    dims_mm.get('z', 5.0)
                ],
                'min_wall_thickness_mm': feature_sizes.get('min_wall_thickness_mm', 0.5),
                'porosity': validation.get('porosity', 0.5)
            }
            
            # Define load cases
            pressure_drop_pa = metrics_stage5['flow_simulated_quantities']['pressure_drop']['pressure_drop_pa']
            T_max_c = metrics_stage5['thermal_simulated_quantities']['temperature_statistics']['T_max_c']
            T_min_c = metrics_stage5['thermal_simulated_quantities']['temperature_statistics']['T_min_c']
            
            pressure_load = load_cases.define_pressure_load_case(pressure_drop_pa, bc)
            thermal_load = load_cases.define_thermal_load_case(T_max_c, T_min_c, bc)
            
            # Run manufacturability checks
            manuf_results = manufacturability.run_all_manufacturability_checks(
                volume, voxel_size_mm, requirements
            )
            
            # Run structural screening
            struct_results = screening.run_structural_screening(
                pressure_load, thermal_load, geometry_info, material
            )
            
            # Compute metrics
            candidate_metrics = metrics_module.compute_all_structural_metrics(
                candidate, struct_results, manuf_results, material, volume
            )
            
            # Add provenance
            candidate_metrics['provenance'] = prov_module.create_provenance_record(
                cand_id, provenance, material,
                {'pressure': pressure_load, 'thermal': thermal_load},
                requirements
            )
            
            # Save candidate results
            io_module.save_candidate_metrics(output_dir, cand_id, candidate_metrics)
            
            all_metrics.append(candidate_metrics)
            
            # Print summary
            overall_pass = candidate_metrics['stage6_verdict']['overall_pass']
            status = "PASS" if overall_pass else "FAIL"
            print(f"  Status: {status}")
            if not overall_pass:
                failures = candidate_metrics['stage6_verdict']['all_failure_modes']
                print(f"  Failures: {', '.join(failures)}")
            else:
                margin = candidate_metrics['structural_screened_quantities']['combined_stress']['margin_of_safety']
                print(f"  Structural margin: {margin:.2f}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print()
    
    # Compare candidates
    print("Comparing candidates...")
    matched_check = compare_module.verify_matched_conditions(all_metrics)
    ranked_candidates = compare_module.rank_candidates_by_combined_performance(all_metrics)
    comparison_summary = compare_module.generate_comparison_summary(all_metrics, ranked_candidates)
    
    # Generate markdown summary
    markdown = compare_module.format_comparison_table_markdown(comparison_summary)
    
    # Save comparison results
    io_module.save_comparison_summary(output_dir, comparison_summary)
    io_module.save_comparison_markdown(output_dir, markdown)
    
    # Create Stage 6 summary
    n_pass = sum(1 for m in all_metrics if m['stage6_verdict']['overall_pass'])
    stage6_summary = {
        'n_candidates': len(all_metrics),
        'n_pass': n_pass,
        'pass_rate': n_pass / len(all_metrics) if all_metrics else 0.0,
        'best_candidate': comparison_summary.get('best_candidate'),
        'matched_conditions': matched_check
    }
    
    io_module.save_stage6_summary(output_dir, stage6_summary)
    
    # Save run manifest
    manifest = prov_module.create_run_manifest(
        stage5_dir, output_dir, len(all_metrics), n_pass, mode
    )
    io_module.save_run_manifest(output_dir, manifest)
    
    # Print summary
    print()
    print("=== Summary ===")
    print(f"Candidates processed: {len(all_metrics)}")
    print(f"Candidates PASS: {n_pass}")
    print(f"Pass rate: {stage6_summary['pass_rate']:.1%}")
    if stage6_summary['best_candidate']:
        print(f"Best candidate: {stage6_summary['best_candidate']}")
    print()
    
    return stage6_summary


def smoke_test() -> int:
    """
    Run smoke test on Stage 5 smoke outputs.
    
    Returns:
        Exit code (0 = success)
    """
    stage5_dir = 'results/stage5_thermal_smoke'
    output_dir = 'results/stage6_structural_smoke'
    
    if not os.path.exists(stage5_dir):
        print(f"ERROR: Stage 5 smoke outputs not found: {stage5_dir}")
        print("Run Stage 5 smoke test first:")
        print("  python src/stage5_thermal/cli.py smoke")
        return 1
    
    try:
        summary = run_structural_screening(
            stage5_dir, output_dir, mode='smoke'
        )
        
        if summary.get('status') == 'failed':
            print("Smoke test FAILED!")
            return 1
        
        print("Smoke test PASSED!")
        return 0
        
    except Exception as e:
        print(f"Smoke test FAILED with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Stage 6: Structural and Manufacturability Screening'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Smoke test command
    subparsers.add_parser('smoke', help='Run smoke test on Stage 5 smoke outputs')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run structural screening')
    run_parser.add_argument('stage5_dir', help='Stage 5 results directory')
    run_parser.add_argument('--output', required=True, help='Output directory')
    run_parser.add_argument('--top-k', type=int, help='Number of top candidates')
    run_parser.add_argument('--family', help='Filter by family name')
    run_parser.add_argument('--material', default='aluminum_6061', help='Material name')
    
    args = parser.parse_args()
    
    if args.command == 'smoke':
        return smoke_test()
    
    elif args.command == 'run':
        summary = run_structural_screening(
            args.stage5_dir,
            args.output,
            args.top_k,
            args.family,
            args.material,
            mode='full'
        )
        return 0 if summary.get('n_pass', 0) > 0 else 1
    
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
