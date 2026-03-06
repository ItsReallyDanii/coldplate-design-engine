"""
Load case definitions and candidate loading for Stage 6.

Loads candidates from Stage 5 thermal validation outputs and defines
mechanical load cases for structural screening.
"""

import os
import json
import numpy as np
from typing import Dict, Any, List, Optional


def load_stage5_summary(stage5_dir: str) -> Dict[str, Any]:
    """
    Load Stage 5 summary file.
    
    Args:
        stage5_dir: Path to Stage 5 results directory
        
    Returns:
        Summary dictionary
    """
    summary_path = os.path.join(stage5_dir, 'stage5_summary.json')
    
    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"Stage 5 summary not found: {summary_path}")
    
    with open(summary_path, 'r') as f:
        return json.load(f)


def load_stage5_candidate(stage5_dir: str, candidate_id: str) -> Dict[str, Any]:
    """
    Load a single Stage 5 candidate with all data.
    
    Args:
        stage5_dir: Path to Stage 5 results directory
        candidate_id: Candidate identifier
        
    Returns:
        Dictionary with candidate data
    """
    cand_dir = os.path.join(stage5_dir, candidate_id)
    
    if not os.path.exists(cand_dir):
        raise FileNotFoundError(f"Candidate directory not found: {cand_dir}")
    
    # Load thermal metrics (includes geometry and flow data)
    metrics_path = os.path.join(cand_dir, 'thermal_metrics.json')
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    
    # Load provenance (contains Stage 3 geometry metadata)
    prov_path = os.path.join(cand_dir, 'provenance.json')
    with open(prov_path, 'r') as f:
        provenance = json.load(f)
    
    # Load boundary conditions
    bc_path = os.path.join(cand_dir, 'boundary_conditions.json')
    with open(bc_path, 'r') as f:
        boundary_conditions = json.load(f)
    
    return {
        'candidate_id': candidate_id,
        'metrics': metrics,
        'provenance': provenance,
        'boundary_conditions': boundary_conditions
    }


def load_candidates_for_structural(
    stage5_dir: str,
    top_k: Optional[int] = None,
    family_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Load Stage 5 candidates for structural screening.
    
    Args:
        stage5_dir: Path to Stage 5 results directory
        top_k: Number of top candidates to load (by thermal performance)
        family_filter: Filter by family name
        
    Returns:
        List of candidate dictionaries
    """
    summary = load_stage5_summary(stage5_dir)
    
    # Get candidate list
    candidates_list = summary['candidates']
    
    # Filter by family if requested
    if family_filter:
        candidates_list = [
            c for c in candidates_list
            if family_filter in c['candidate_id']
        ]
    
    # Sort by thermal resistance (lower is better)
    candidates_list = sorted(
        candidates_list,
        key=lambda c: c['thermal_resistance_k_w']
    )
    
    # Apply top-k limit
    if top_k:
        candidates_list = candidates_list[:top_k]
    
    # Load full candidate data
    candidates = []
    for cand_summary in candidates_list:
        cand_id = cand_summary['candidate_id']
        try:
            cand_data = load_stage5_candidate(stage5_dir, cand_id)
            candidates.append(cand_data)
        except Exception as e:
            print(f"WARNING: Failed to load {cand_id}: {e}")
            continue
    
    return candidates


def define_pressure_load_case(
    pressure_drop_pa: float,
    boundary_conditions: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Define pressure load case for structural screening.
    
    LABEL: ANALYTICAL (simplified load approximation)
    
    Args:
        pressure_drop_pa: Pressure drop from flow simulation (Pa)
        boundary_conditions: Boundary conditions from Stage 5
        
    Returns:
        Pressure load case dictionary
    """
    # Simplified: assume uniform internal pressure equal to inlet pressure
    # This is CONSERVATIVE for screening purposes
    inlet_pressure_pa = boundary_conditions.get('inlet_pressure_pa', 101325.0 + pressure_drop_pa)
    
    return {
        'type': 'internal_pressure',
        'pressure_pa': inlet_pressure_pa,
        'pressure_drop_pa': pressure_drop_pa,
        'description': 'Internal pressure load from flow',
        'label': 'ANALYTICAL',
        'method': 'uniform_pressure_approximation'
    }


def define_thermal_load_case(
    T_max_c: float,
    T_min_c: float,
    boundary_conditions: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Define thermal load case for structural screening.
    
    LABEL: ANALYTICAL (simplified from thermal simulation)
    
    Args:
        T_max_c: Maximum temperature (°C)
        T_min_c: Minimum temperature (°C)
        boundary_conditions: Boundary conditions from Stage 5
        
    Returns:
        Thermal load case dictionary
    """
    # Simplified: assume uniform temperature gradient causes thermal strain
    delta_T_c = T_max_c - T_min_c
    T_ref_c = boundary_conditions.get('ambient_temperature_c', 25.0)
    
    return {
        'type': 'thermal_expansion',
        'T_max_c': T_max_c,
        'T_min_c': T_min_c,
        'delta_T_c': delta_T_c,
        'T_ref_c': T_ref_c,
        'description': 'Thermal expansion from temperature field',
        'label': 'ANALYTICAL',
        'method': 'simplified_thermal_strain'
    }


def define_combined_load_case(
    pressure_load: Dict[str, Any],
    thermal_load: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Define combined pressure + thermal load case.
    
    LABEL: ANALYTICAL (superposition approximation)
    
    Args:
        pressure_load: Pressure load case
        thermal_load: Thermal load case
        
    Returns:
        Combined load case dictionary
    """
    return {
        'type': 'combined_pressure_thermal',
        'pressure_load': pressure_load,
        'thermal_load': thermal_load,
        'description': 'Combined pressure and thermal loading',
        'label': 'ANALYTICAL',
        'method': 'linear_superposition_approximation'
    }
