"""
Provenance tracking for Stage 5 thermal validation.
"""

import os
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any, Optional


def get_git_sha() -> str:
    """
    Get current git SHA.
    
    Returns:
        Git SHA string or 'unknown'
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    
    return 'unknown'


def create_stage5_provenance(
    candidate: Dict[str, Any],
    boundary_conditions: Dict[str, Any],
    solver_params: Dict[str, Any],
    thermal_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create provenance record for Stage 5 thermal validation.
    
    Args:
        candidate: Candidate dictionary from load_cases
        boundary_conditions: BC dictionary
        solver_params: Solver parameters
        thermal_result: Thermal simulation result
        
    Returns:
        Provenance dictionary
    """
    return {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'stage': 'stage5_thermal',
        'schema_version': '1.0',
        'candidate_id': candidate['candidate_id'],
        'git_sha': get_git_sha(),
        'stage4_source': {
            'candidate_id': candidate['candidate_id'],
            'provenance': candidate.get('provenance', {}),
            'flow_converged': candidate.get('solver_info', {}).get('converged', False),
            'stage4_metrics': candidate.get('metrics', {})
        },
        'thermal_simulation': {
            'converged': thermal_result.get('converged', False),
            'solve_time_s': thermal_result.get('solve_time_s', 0.0),
            'residual': float(thermal_result.get('residual', float('inf'))),
            'solver': thermal_result.get('solver', 'unknown')
        },
        'boundary_conditions': boundary_conditions,
        'solver_params': solver_params,
        'grid_info': candidate.get('grid_info', {})
    }


def create_run_manifest(
    mode: str,
    n_candidates: int,
    candidate_ids: list,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create run manifest for Stage 5 execution.
    
    Args:
        mode: Execution mode ('smoke', 'full', etc.)
        n_candidates: Number of candidates
        candidate_ids: List of candidate IDs
        config: Optional configuration dict
        
    Returns:
        Run manifest dictionary
    """
    return {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'stage': 'stage5_thermal',
        'git_sha': get_git_sha(),
        'config': config or {'mode': mode},
        'n_candidates': n_candidates,
        'candidate_ids': candidate_ids
    }
