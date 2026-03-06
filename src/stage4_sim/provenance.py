"""
Provenance tracking for Stage 4 simulation.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


def get_git_sha() -> str:
    """
    Get current git commit SHA.
    
    Returns:
        Git SHA string or 'unknown' if not available
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
    return "unknown"


def create_provenance_record(
    candidate_id: str,
    candidate_data: Dict[str, Any],
    simulation_result: Dict[str, Any],
    metrics: Dict[str, Any],
    boundary_conditions: Dict[str, Any],
    grid: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create comprehensive provenance record for Stage 4 simulation.
    
    Args:
        candidate_id: Candidate identifier
        candidate_data: Loaded candidate data from Stage 3
        simulation_result: Simulation result from solver
        metrics: Computed metrics
        boundary_conditions: Boundary conditions used
        grid: Grid setup used
        config: Configuration parameters
        
    Returns:
        Provenance record dictionary
    """
    return {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'stage': 'stage4_sim',
        'schema_version': '1.0',
        'candidate_id': candidate_id,
        'git_sha': get_git_sha(),
        'stage3_source': {
            'provenance': candidate_data['provenance'],
            'metadata': candidate_data['metadata']
        },
        'simulation': {
            'grid': {
                'shape': grid['shape'],
                'voxel_size_mm': grid['voxel_size_mm'],
                'domain_size_mm': grid['domain_size_mm'],
                'porosity': grid['porosity']
            },
            'boundary_conditions': boundary_conditions,
            'solver': {
                'type': 'pressure_poisson',
                'method': 'finite_difference',
                'converged': simulation_result['converged'],
                'iterations': simulation_result['iterations'],
                'solve_time_s': simulation_result['solve_time_s'],
                'tolerance': simulation_result['tolerance']
            },
            'config': config
        },
        'metrics': metrics
    }


def save_provenance(
    provenance_record: Dict[str, Any],
    output_path: Path
) -> None:
    """
    Save provenance record to JSON file.
    
    Args:
        provenance_record: Provenance dictionary
        output_path: Path to output file
    """
    with open(output_path, 'w') as f:
        json.dump(provenance_record, f, indent=2)
