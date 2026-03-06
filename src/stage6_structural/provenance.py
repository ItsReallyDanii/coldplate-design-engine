"""
Provenance tracking for Stage 6 structural screening.
"""

from datetime import datetime, timezone
from typing import Dict, Any
import subprocess


def get_git_sha() -> str:
    """
    Get current git commit SHA.
    
    Returns:
        Git SHA string or 'unknown'
    """
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


def create_provenance_record(
    candidate_id: str,
    stage5_provenance: Dict[str, Any],
    material: Dict[str, Any],
    load_cases: Dict[str, Any],
    requirements: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create provenance record for Stage 6 screening.
    
    Args:
        candidate_id: Candidate identifier
        stage5_provenance: Provenance from Stage 5
        material: Material properties
        load_cases: Load case definitions
        requirements: Manufacturability requirements
        
    Returns:
        Provenance dictionary
    """
    return {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'stage': 'stage6_structural',
        'schema_version': '1.0',
        'candidate_id': candidate_id,
        'git_sha': get_git_sha(),
        
        'stage5_source': {
            'candidate_id': candidate_id,
            'thermal_converged': stage5_provenance.get('thermal_simulation', {}).get('converged', False),
            'thermal_solve_time_s': stage5_provenance.get('thermal_simulation', {}).get('solve_time_s', 0.0)
        },
        
        'material': {
            'name': material['name'],
            'label': material['label'],
            'source': material['source']
        },
        
        'load_cases': {
            'pressure': {
                'type': load_cases['pressure']['type'],
                'pressure_pa': load_cases['pressure']['pressure_pa'],
                'label': load_cases['pressure']['label']
            },
            'thermal': {
                'type': load_cases['thermal']['type'],
                'delta_T_c': load_cases['thermal']['delta_T_c'],
                'label': load_cases['thermal']['label']
            }
        },
        
        'screening_parameters': {
            'structural_method': 'analytical_approximation',
            'manufacturability_method': 'geometric_analysis',
            'screening_level': 'PRELIMINARY'
        },
        
        'manufacturability_requirements': requirements
    }


def create_run_manifest(
    stage5_dir: str,
    output_dir: str,
    n_candidates: int,
    n_pass: int,
    mode: str = 'full'
) -> Dict[str, Any]:
    """
    Create run manifest for Stage 6 execution.
    
    Args:
        stage5_dir: Stage 5 input directory
        output_dir: Output directory
        n_candidates: Number of candidates processed
        n_pass: Number of candidates passing screening
        mode: Execution mode
        
    Returns:
        Run manifest dictionary
    """
    return {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'stage': 'stage6_structural',
        'git_sha': get_git_sha(),
        'mode': mode,
        
        'input': {
            'stage5_dir': stage5_dir
        },
        
        'output': {
            'output_dir': output_dir
        },
        
        'execution': {
            'n_candidates_processed': n_candidates,
            'n_candidates_pass': n_pass,
            'pass_rate': n_pass / n_candidates if n_candidates > 0 else 0.0
        }
    }
