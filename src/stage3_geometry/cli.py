"""Command-line interface for Stage 3 geometry promotion."""

import sys
import os
import argparse
import yaml
import subprocess
from pathlib import Path

# Handle both direct execution and package import
if __name__ == '__main__' and __package__ is None:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from stage3_geometry import io, promote, export, validate, provenance, config as geom_config
else:
    from . import io, promote, export, validate, provenance, config as geom_config


def get_git_sha():
    """Get current git SHA if available."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return 'unknown'


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def run_smoke(args):
    """Run smoke test with minimal candidates."""
    print("=== Stage 3 Smoke Test ===")
    
    # Load top 2 candidates from Stage 2
    stage2_results = "results/stage2_inverse/best_candidates.csv"
    
    if not Path(stage2_results).exists():
        print(f"ERROR: Stage 2 results not found at {stage2_results}")
        print("Run Stage 2 first: python src/stage2_inverse/cli.py smoke")
        return 1
    
    print(f"Loading candidates from {stage2_results}...")
    candidates = io.load_stage2_candidates(stage2_results)
    
    # Select top 2
    selected = io.select_top_k_candidates(candidates, k=2)
    print(f"Selected {len(selected)} candidates")
    
    # Promote to 3D
    output_dir = "results/stage3_geometry_smoke"
    io.ensure_output_dir(output_dir)
    
    # Get remediation configuration (v1: 0.25mm voxels, resolution=20)
    smoke_cfg = geom_config.get_smoke_config()
    
    config = {
        'resolution': smoke_cfg['resolution'],  # Remediation: 20 (was 50)
        'height_mm': smoke_cfg['height_mm'],
        'voxel_size_mm': smoke_cfg['voxel_size_mm'],  # Remediation: 0.25mm (was 0.1mm)
        'top_k': 2,
        'source_file': stage2_results,
        'remediation': geom_config.get_remediation_info(),  # Provenance tracking
    }
    
    git_sha = get_git_sha()
    manifest = provenance.create_promotion_manifest(selected, config, git_sha)
    io.save_json(manifest, f"{output_dir}/run_manifest.json")
    
    provenance_records = []
    
    for candidate in selected:
        print(f"\n--- Candidate {candidate['rank']}: {candidate['family']} ---")
        
        # Promote to 3D
        volume, metadata, error = promote.promote_candidate_to_3d(
            candidate,
            height_mm=config['height_mm'],
            resolution=config['resolution']
        )
        
        if volume is None:
            print(f"FAILED: {error}")
            prov = provenance.create_candidate_provenance(
                candidate, {}, {}, {}, [error]
            )
            provenance_records.append(prov)
            continue
        
        print(f"Generated 3D volume: {volume.shape}")
        print(f"Porosity: {metadata.get('porosity', 'N/A')}")
        
        # Create output directory
        cand_dir = io.create_candidate_output_dir(
            output_dir, candidate['rank'], candidate['family'], candidate['seed']
        )
        
        # Validate (use config voxel size)
        voxel_size = config['voxel_size_mm']
        is_valid, val_results, errors = validate.validate_geometry(
            volume, voxel_size=voxel_size, require_connected=False
        )
        
        print(f"Validation: {'PASS' if is_valid else 'FAIL'}")
        if errors:
            for err in errors:
                print(f"  - {err}")
        
        # Export
        export_paths = {}
        
        stl_path = f"{cand_dir}/geometry/geometry.stl"
        if export.export_stl_from_volume(volume, stl_path, voxel_size=voxel_size):
            export_paths['stl'] = stl_path
        
        raw_path = f"{cand_dir}/geometry/volume.npy"
        if export.export_raw_volume(volume, raw_path, metadata):
            export_paths['raw'] = raw_path
        
        # Save provenance
        prov = provenance.create_candidate_provenance(
            candidate, metadata, val_results, export_paths, errors if not is_valid else None
        )
        provenance_records.append(prov)
        
        prov_path = f"{cand_dir}/provenance.json"
        provenance.save_provenance(prov, prov_path)
    
    # Generate summary
    summary_text = provenance.create_summary_report(manifest, provenance_records)
    io.save_text(summary_text, f"{output_dir}/summary.md")
    io.save_json({'provenance_records': provenance_records}, f"{output_dir}/summary.json")
    
    print(f"\n=== Smoke Test Complete ===")
    print(f"Results saved to {output_dir}")
    print(f"Summary: {output_dir}/summary.md")
    
    return 0


def run_promote(args):
    """Run full promotion from config file."""
    print("=== Stage 3 Full Promotion ===")
    
    config = load_config(args.config)
    
    # Load candidates
    stage2_results = config.get('stage2_results', 'results/stage2_inverse/best_candidates.csv')
    
    if not Path(stage2_results).exists():
        print(f"ERROR: Stage 2 results not found at {stage2_results}")
        return 1
    
    print(f"Loading candidates from {stage2_results}...")
    candidates = io.load_stage2_candidates(stage2_results)
    
    # Select top-k
    top_k = config.get('top_k', 5)
    family_filter = config.get('family_filter', None)
    selected = io.select_top_k_candidates(candidates, k=top_k, family_filter=family_filter)
    print(f"Selected {len(selected)} candidates")
    
    # Promote
    output_dir = config.get('output_dir', 'results/stage3_geometry')
    io.ensure_output_dir(output_dir)
    
    # Use remediation config defaults if not specified in config file
    full_cfg = geom_config.get_full_config()
    resolution = config.get('resolution', full_cfg['resolution'])
    height_mm = config.get('height_mm', full_cfg['height_mm'])
    voxel_size_mm = config.get('voxel_size_mm', full_cfg['voxel_size_mm'])
    
    # Add remediation info to config for provenance
    if 'remediation' not in config:
        config['remediation'] = geom_config.get_remediation_info()
        config['voxel_size_mm'] = voxel_size_mm
    
    git_sha = get_git_sha()
    manifest = provenance.create_promotion_manifest(selected, config, git_sha)
    io.save_json(manifest, f"{output_dir}/run_manifest.json")
    
    provenance_records = []
    
    for candidate in selected:
        print(f"\n--- Candidate {candidate['rank']}: {candidate['family']} ---")
        
        # Promote to 3D
        volume, metadata, error = promote.promote_candidate_to_3d(
            candidate,
            height_mm=height_mm,
            resolution=resolution
        )
        
        if volume is None:
            print(f"FAILED: {error}")
            prov = provenance.create_candidate_provenance(
                candidate, {}, {}, {}, [error]
            )
            provenance_records.append(prov)
            continue
        
        print(f"Generated 3D volume: {volume.shape}")
        
        # Create output directory
        cand_dir = io.create_candidate_output_dir(
            output_dir, candidate['rank'], candidate['family'], candidate['seed']
        )
        
        # Validate (use config voxel size)
        is_valid, val_results, errors = validate.validate_geometry(
            volume, voxel_size=voxel_size_mm, require_connected=False
        )
        
        print(f"Validation: {'PASS' if is_valid else 'FAIL'}")
        
        # Export
        export_paths = {}
        
        stl_path = f"{cand_dir}/geometry/geometry.stl"
        if export.export_stl_from_volume(volume, stl_path, voxel_size=voxel_size_mm):
            export_paths['stl'] = stl_path
        
        raw_path = f"{cand_dir}/geometry/volume.npy"
        if export.export_raw_volume(volume, raw_path, metadata):
            export_paths['raw'] = raw_path
        
        # Save validation report
        val_report_path = f"{cand_dir}/validation/validation_report.json"
        io.save_json({'results': val_results, 'errors': errors}, val_report_path)
        
        # Save provenance
        prov = provenance.create_candidate_provenance(
            candidate, metadata, val_results, export_paths, errors if not is_valid else None
        )
        provenance_records.append(prov)
        
        prov_path = f"{cand_dir}/provenance.json"
        provenance.save_provenance(prov, prov_path)
    
    # Generate summary
    summary_text = provenance.create_summary_report(manifest, provenance_records)
    io.save_text(summary_text, f"{output_dir}/summary.md")
    io.save_json({'provenance_records': provenance_records}, f"{output_dir}/summary.json")
    
    print(f"\n=== Promotion Complete ===")
    print(f"Results saved to {output_dir}")
    
    return 0


def run_validate(args):
    """Validate existing Stage 3 outputs."""
    print("=== Stage 3 Validation ===")
    
    config = load_config(args.config)
    output_dir = config.get('output_dir', 'results/stage3_geometry')
    
    # Load summary
    summary_path = f"{output_dir}/summary.json"
    if not Path(summary_path).exists():
        print(f"ERROR: No summary found at {summary_path}")
        return 1
    
    import json
    with open(summary_path, 'r') as f:
        summary = json.load(f)
    
    provenance_records = summary['provenance_records']
    
    print(f"Found {len(provenance_records)} candidates")
    
    passed = 0
    failed = 0
    
    for prov in provenance_records:
        if prov['promotion']['success']:
            passed += 1
        else:
            failed += 1
    
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Stage 3 Geometry Promotion')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Smoke test
    smoke_parser = subparsers.add_parser('smoke', help='Run smoke test')
    
    # Full promotion
    promote_parser = subparsers.add_parser('promote', help='Run full promotion')
    promote_parser.add_argument('config', help='Configuration YAML file')
    
    # Validation
    validate_parser = subparsers.add_parser('validate', help='Validate existing outputs')
    validate_parser.add_argument('config', help='Configuration YAML file')
    
    args = parser.parse_args()
    
    if args.command == 'smoke':
        return run_smoke(args)
    elif args.command == 'promote':
        return run_promote(args)
    elif args.command == 'validate':
        return run_validate(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
