"""
I/O utilities for Stage 5 thermal validation.
"""

import os
import json
import numpy as np
from typing import Dict, Any, List


def create_output_directory(base_dir: str, candidate_id: str) -> str:
    """
    Create output directory for a candidate.
    
    Args:
        base_dir: Base output directory
        candidate_id: Candidate identifier
        
    Returns:
        Path to candidate output directory
    """
    cand_dir = os.path.join(base_dir, candidate_id)
    os.makedirs(cand_dir, exist_ok=True)
    return cand_dir


def save_candidate_results(
    output_dir: str,
    candidate_id: str,
    thermal_result: Dict[str, Any],
    metrics: Dict[str, Any],
    provenance: Dict[str, Any],
    boundary_conditions: Dict[str, Any]
) -> None:
    """
    Save candidate results to disk.
    
    Args:
        output_dir: Output directory path
        candidate_id: Candidate identifier
        thermal_result: Thermal simulation result
        metrics: Metrics dictionary
        provenance: Provenance dictionary
        boundary_conditions: BC dictionary
    """
    cand_dir = create_output_directory(output_dir, candidate_id)
    
    # Save temperature field
    temp_path = os.path.join(cand_dir, 'temperature_field.npy')
    np.save(temp_path, thermal_result['temperature'])
    
    # Save metrics
    metrics_path = os.path.join(cand_dir, 'thermal_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Save provenance
    prov_path = os.path.join(cand_dir, 'provenance.json')
    with open(prov_path, 'w') as f:
        json.dump(provenance, f, indent=2)
    
    # Save boundary conditions
    bc_path = os.path.join(cand_dir, 'boundary_conditions.json')
    with open(bc_path, 'w') as f:
        json.dump(boundary_conditions, f, indent=2)
    
    # Save solver info
    solver_info = {
        'converged': thermal_result.get('converged', False),
        'solve_time_s': thermal_result.get('solve_time_s', 0.0),
        'residual': thermal_result.get('residual', float('inf')),
        'solver': thermal_result.get('solver', 'unknown'),
        'matrix_shape': thermal_result.get('matrix_shape', None),
        'matrix_nnz': thermal_result.get('matrix_nnz', None)
    }
    
    solver_path = os.path.join(cand_dir, 'solver_info.json')
    with open(solver_path, 'w') as f:
        json.dump(solver_info, f, indent=2)


def save_comparison_results(
    output_dir: str,
    comparison: Dict[str, Any],
    summary_text: str
) -> None:
    """
    Save comparison results.
    
    Args:
        output_dir: Output directory path
        comparison: Comparison metrics dictionary
        summary_text: Summary text (markdown)
    """
    # Save comparison JSON
    comp_path = os.path.join(output_dir, 'thermal_comparison.json')
    with open(comp_path, 'w') as f:
        json.dump(comparison, f, indent=2)
    
    # Save summary markdown
    summary_path = os.path.join(output_dir, 'thermal_comparison_summary.md')
    with open(summary_path, 'w') as f:
        f.write(summary_text)


def save_stage5_summary(
    output_dir: str,
    results: List[Dict[str, Any]]
) -> None:
    """
    Save Stage 5 summary file.
    
    Args:
        output_dir: Output directory path
        results: List of candidate results
    """
    summary = {
        'n_candidates': len(results),
        'candidates': []
    }
    
    for result in results:
        metrics = result['metrics']
        thermal_sim = metrics['thermal_simulated_quantities']
        
        summary['candidates'].append({
            'candidate_id': result['candidate_id'],
            'thermal_converged': result.get('thermal_result', {}).get('converged', False),
            'thermal_solve_time_s': result.get('thermal_result', {}).get('solve_time_s', 0.0),
            'thermal_resistance_k_w': thermal_sim['thermal_resistance']['thermal_resistance_k_w'],
            'T_max_c': thermal_sim['temperature_statistics']['T_max_c'],
            'T_mean_c': thermal_sim['temperature_statistics']['T_mean_c'],
            'T_spread_c': thermal_sim['uniformity']['temperature_spread_c']
        })
    
    summary_path = os.path.join(output_dir, 'stage5_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
