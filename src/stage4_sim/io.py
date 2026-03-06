"""
I/O utilities for Stage 4 simulation results.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


def save_candidate_results(
    result: Dict[str, Any],
    output_dir: Path,
    candidate_id: str
) -> Dict[str, str]:
    """
    Save simulation results for a single candidate.
    
    Args:
        result: Simulation result dictionary
        output_dir: Output directory
        candidate_id: Candidate identifier
        
    Returns:
        Dictionary with paths to saved files
    """
    # Create candidate directory
    candidate_dir = output_dir / candidate_id
    candidate_dir.mkdir(parents=True, exist_ok=True)
    
    # Save metrics as JSON
    metrics_path = candidate_dir / "metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(result['metrics'], f, indent=2)
    
    # Save solver info
    solver_info = {
        'converged': result['simulation_result']['converged'],
        'iterations': result['simulation_result']['iterations'],
        'solve_time_s': result['simulation_result']['solve_time_s'],
        'tolerance': result['simulation_result']['tolerance']
    }
    solver_path = candidate_dir / "solver_info.json"
    with open(solver_path, 'w') as f:
        json.dump(solver_info, f, indent=2)
    
    # Save pressure field (optional, can be large)
    pressure = result['simulation_result']['pressure']
    pressure_path = candidate_dir / "pressure_field.npy"
    np.save(pressure_path, pressure)
    
    # Save velocity field (optional)
    velocity = result['simulation_result']['velocity']
    velocity_path = candidate_dir / "velocity_field.npz"
    np.savez_compressed(velocity_path, 
                        vx=velocity['vx'], 
                        vy=velocity['vy'], 
                        vz=velocity['vz'])
    
    return {
        'metrics': str(metrics_path),
        'solver_info': str(solver_path),
        'pressure_field': str(pressure_path),
        'velocity_field': str(velocity_path)
    }


def save_run_manifest(
    output_dir: Path,
    config: Dict[str, Any],
    candidate_ids: List[str],
    git_sha: str = "unknown"
) -> Path:
    """
    Save run manifest for reproducibility.
    
    Args:
        output_dir: Output directory
        config: Configuration dictionary
        candidate_ids: List of candidate identifiers
        git_sha: Git commit SHA
        
    Returns:
        Path to manifest file
    """
    manifest = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'stage': 'stage4_sim',
        'git_sha': git_sha,
        'config': config,
        'n_candidates': len(candidate_ids),
        'candidate_ids': candidate_ids
    }
    
    manifest_path = output_dir / "run_manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    return manifest_path


def save_comparison_results(
    output_dir: Path,
    comparison_metrics: Dict[str, Any],
    matched_conditions: Dict[str, Any],
    summary_text: str
) -> Dict[str, str]:
    """
    Save comparison results.
    
    Args:
        output_dir: Output directory
        comparison_metrics: Comparison metrics dictionary
        matched_conditions: Matched conditions verification
        summary_text: Markdown summary text
        
    Returns:
        Dictionary with paths to saved files
    """
    # Save comparison JSON
    comparison_data = {
        'comparison_metrics': comparison_metrics,
        'matched_conditions': matched_conditions
    }
    comparison_path = output_dir / "comparison.json"
    with open(comparison_path, 'w') as f:
        json.dump(comparison_data, f, indent=2)
    
    # Save summary markdown
    summary_path = output_dir / "comparison_summary.md"
    with open(summary_path, 'w') as f:
        f.write(summary_text)
    
    return {
        'comparison_json': str(comparison_path),
        'summary_md': str(summary_path)
    }


def save_stage4_summary(
    output_dir: Path,
    results: List[Dict[str, Any]]
) -> Path:
    """
    Save overall Stage 4 summary.
    
    Args:
        output_dir: Output directory
        results: List of all candidate results
        
    Returns:
        Path to summary file
    """
    summary = {
        'n_candidates': len(results),
        'candidates': []
    }
    
    for r in results:
        candidate_summary = {
            'candidate_id': r['candidate_id'],
            'converged': r['simulation_result']['converged'],
            'solve_time_s': r['simulation_result']['solve_time_s'],
            'pressure_drop_pa': r['metrics']['simulated_quantities']['pressure_drop']['pressure_drop_pa'],
            'flow_rate_m3_s': r['metrics']['simulated_quantities']['flow_rate']['flow_rate_m3_s'],
            'hydraulic_resistance': r['metrics']['simulated_quantities']['hydraulic_resistance']['hydraulic_resistance_pa_s_m3'],
            'porosity': r['metrics']['geometric_quantities']['porosity']
        }
        summary['candidates'].append(candidate_summary)
    
    summary_path = output_dir / "stage4_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    return summary_path
