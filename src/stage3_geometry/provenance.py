"""Provenance tracking for Stage 3 geometry promotion.

Records full traceability from Stage 2 candidates through 3D geometry.
"""

import json
import os
from typing import Dict, Any, List
from datetime import datetime, timezone


def create_promotion_manifest(
    candidates: List[Dict[str, Any]],
    config: Dict[str, Any],
    git_sha: str = None
) -> Dict[str, Any]:
    """Create manifest for Stage 3 promotion run.
    
    Args:
        candidates: List of candidates being promoted
        config: Configuration used for promotion
        git_sha: Git commit SHA
        
    Returns:
        Manifest dictionary
    """
    manifest = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'git_sha': git_sha or 'unknown',
        'stage': 'stage3_geometry',
        'schema_version': '1.0',
        'num_candidates': len(candidates),
        'config': config,
        'candidate_ranks': [c['rank'] for c in candidates],
        'candidate_families': [c['family'] for c in candidates],
    }
    
    return manifest


def create_candidate_provenance(
    candidate: Dict[str, Any],
    volume_metadata: Dict[str, Any],
    validation_results: Dict[str, Any],
    export_paths: Dict[str, str],
    errors: List[str] = None
) -> Dict[str, Any]:
    """Create provenance record for a single promoted candidate.
    
    Args:
        candidate: Original Stage 2 candidate
        volume_metadata: Metadata from 3D generation
        validation_results: Results from validation checks
        export_paths: Paths to exported files
        errors: List of errors if any
        
    Returns:
        Provenance dictionary
    """
    provenance = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'stage': 'stage3_geometry',
        'schema_version': '1.0',
        
        # Stage 2 source
        'stage2_source': {
            'rank': candidate['rank'],
            'family': candidate['family'],
            'seed': candidate['seed'],
            'mask_id': candidate['mask_id'],
            'total_score': candidate['total_score'],
            'is_valid': candidate['is_valid'],
            'params': candidate['params'],
            'metrics': candidate.get('metrics', {}),
        },
        
        # 3D promotion
        'promotion': {
            'volume_metadata': volume_metadata,
            'success': errors is None or len(errors) == 0,
            'errors': errors or [],
        },
        
        # Validation
        'validation': validation_results,
        
        # Exports
        'exports': export_paths,
    }
    
    return provenance


def save_provenance(provenance: Dict[str, Any], filepath: str):
    """Save provenance record to JSON file.
    
    Args:
        provenance: Provenance dictionary
        filepath: Output file path
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(provenance, f, indent=2)
    
    print(f"Saved provenance to {filepath}")


def create_summary_report(
    manifest: Dict[str, Any],
    provenance_records: List[Dict[str, Any]]
) -> str:
    """Create human-readable summary report.
    
    Args:
        manifest: Run manifest
        provenance_records: List of candidate provenance records
        
    Returns:
        Markdown-formatted summary text
    """
    lines = [
        "# Stage 3 Geometry Promotion Summary",
        "",
        f"**Timestamp:** {manifest['timestamp']}",
        f"**Git SHA:** {manifest['git_sha']}",
        f"**Candidates Processed:** {manifest['num_candidates']}",
        "",
        "## Configuration",
        "",
        f"- Resolution: {manifest['config'].get('resolution', 'N/A')}",
        f"- Height: {manifest['config'].get('height_mm', 'N/A')} mm",
        f"- Top-K: {manifest['config'].get('top_k', 'N/A')}",
        "",
        "## Promotion Results",
        "",
    ]
    
    successful = 0
    failed = 0
    
    for prov in provenance_records:
        if prov['promotion']['success']:
            successful += 1
        else:
            failed += 1
    
    lines.extend([
        f"- **Successful:** {successful}/{len(provenance_records)}",
        f"- **Failed:** {failed}/{len(provenance_records)}",
        "",
        "## Candidate Details",
        "",
        "| Rank | Family | Seed | Status | Porosity | Connected | Min Feature (mm) |",
        "|------|--------|------|--------|----------|-----------|------------------|",
    ])
    
    for prov in provenance_records:
        rank = prov['stage2_source']['rank']
        family = prov['stage2_source']['family']
        seed = prov['stage2_source']['seed']
        status = "✓" if prov['promotion']['success'] else "✗"
        
        if 'validation' in prov and 'porosity' in prov['validation']:
            porosity = f"{prov['validation']['porosity']:.3f}"
        else:
            porosity = "N/A"
        
        if 'validation' in prov and 'connectivity' in prov['validation']:
            connected = "Yes" if prov['validation']['connectivity'].get('is_connected', False) else "No"
        else:
            connected = "N/A"
        
        if 'validation' in prov and 'feature_sizes' in prov['validation']:
            min_feat = f"{prov['validation']['feature_sizes'].get('min_channel_diameter_mm', 0):.3f}"
        else:
            min_feat = "N/A"
        
        lines.append(f"| {rank} | {family} | {seed} | {status} | {porosity} | {connected} | {min_feat} |")
    
    lines.extend([
        "",
        "## Validation Summary",
        "",
    ])
    
    # Count validation results
    connected_count = sum(1 for p in provenance_records 
                         if p.get('validation', {}).get('connectivity', {}).get('is_connected', False))
    
    lines.extend([
        f"- **Connected fluid regions:** {connected_count}/{len(provenance_records)}",
        "",
        "## Stage 3 Gate Assessment",
        "",
        "Stage 3 SUCCESS if:",
        "- [ ] Top Stage 2 candidates loaded successfully",
        "- [ ] At least one channel family promoted to 3D",
        "- [ ] At least one TPMS family promoted to 3D",
        "- [ ] Geometry exports created (STL/raw)",
        "- [ ] Validation checks executed",
        "- [ ] Results reproducible from provenance",
        "",
    ])
    
    return "\n".join(lines)
