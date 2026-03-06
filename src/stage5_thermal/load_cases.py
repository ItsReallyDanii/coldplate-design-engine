"""
Load Stage 4 simulation cases for thermal validation.

Loads:
- Stage 4 flow results (pressure, velocity fields)
- Stage 3 geometry (reconstructed from metadata)
- Metadata and parameters
"""

import os
import json
import numpy as np
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

# Import Stage 3 geometry generation for reconstruction
sys.path.insert(0, str(Path(__file__).parent.parent))
from stage3_geometry import tpms3d


def reconstruct_geometry_from_metadata(metadata: Dict[str, Any]) -> np.ndarray:
    """
    Reconstruct 3D geometry from Stage 3 metadata.
    
    Args:
        metadata: Volume metadata from Stage 3 provenance
        
    Returns:
        Reconstructed volume array (uint8, 1=fluid, 0=solid)
    """
    geom_type = metadata.get('type', '')
    params = metadata.get('stage2_params', {})
    height_mm = metadata.get('height_mm', 2.0)
    resolution = metadata.get('resolution', 50)
    
    grid_config = {}  # Not used by tpms3d functions
    
    if 'diamond' in geom_type.lower():
        # Diamond TPMS
        volume, _ = tpms3d.generate_diamond_3d(
            params, grid_config, height_mm, resolution
        )
    elif 'gyroid' in geom_type.lower():
        # Gyroid TPMS
        volume, _ = tpms3d.generate_gyroid_3d(
            params, grid_config, height_mm, resolution
        )
    elif 'primitive' in geom_type.lower():
        # Primitive TPMS
        volume, _ = tpms3d.generate_primitive_3d(
            params, grid_config, height_mm, resolution
        )
    else:
        raise ValueError(f"Unsupported geometry type: {geom_type}")
    
    return volume


def load_stage4_summary(stage4_dir: str) -> Dict[str, Any]:
    """
    Load Stage 4 summary file.
    
    Args:
        stage4_dir: Path to Stage 4 results directory
        
    Returns:
        Summary dictionary with candidate list and metadata
    """
    summary_path = os.path.join(stage4_dir, 'stage4_summary.json')
    
    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"Stage 4 summary not found: {summary_path}")
    
    with open(summary_path, 'r') as f:
        summary = json.load(f)
    
    return summary


def load_stage4_candidate(stage4_dir: str, candidate_id: str) -> Dict[str, Any]:
    """
    Load a single Stage 4 candidate with flow results.
    
    Args:
        stage4_dir: Path to Stage 4 results directory
        candidate_id: Candidate identifier
        
    Returns:
        Dictionary with:
        - geometry: Volume array
        - pressure: Pressure field
        - velocity: Velocity field dict (vx, vy, vz)
        - metrics: Stage 4 metrics
        - provenance: Traceability chain
        - grid_info: Grid metadata
    """
    cand_dir = os.path.join(stage4_dir, candidate_id)
    
    if not os.path.exists(cand_dir):
        raise FileNotFoundError(f"Candidate directory not found: {cand_dir}")
    
    # Load provenance to get Stage 3 source
    prov_path = os.path.join(cand_dir, 'provenance.json')
    with open(prov_path, 'r') as f:
        provenance = json.load(f)
    
    # Reconstruct geometry from metadata (since Stage 4 doesn't save geometry)
    metadata = provenance.get('stage3_source', {}).get('metadata', {})
    volume = reconstruct_geometry_from_metadata(metadata)
    
    # Load Stage 4 flow results
    pressure = np.load(os.path.join(cand_dir, 'pressure_field.npy'))
    velocity = np.load(os.path.join(cand_dir, 'velocity_field.npz'))
    
    # Load metrics
    with open(os.path.join(cand_dir, 'metrics.json'), 'r') as f:
        metrics = json.load(f)
    
    # Load solver info
    with open(os.path.join(cand_dir, 'solver_info.json'), 'r') as f:
        solver_info = json.load(f)
    
    return {
        'candidate_id': candidate_id,
        'geometry': volume,
        'pressure': pressure,
        'velocity': {
            'vx': velocity['vx'],
            'vy': velocity['vy'],
            'vz': velocity['vz']
        },
        'metrics': metrics,
        'provenance': provenance,
        'solver_info': solver_info,
        'grid_info': {
            'shape': volume.shape,
            'voxel_size_mm': provenance.get('stage3_source', {}).get('voxel_size_mm', 0.1),
            'porosity': metrics['geometric_quantities']['porosity']
        }
    }


def select_candidates_for_thermal(
    stage4_dir: str,
    top_k: Optional[int] = None,
    family_filter: Optional[str] = None
) -> List[str]:
    """
    Select candidates for thermal validation.
    
    Args:
        stage4_dir: Path to Stage 4 results directory
        top_k: Number of top candidates to select (None = all)
        family_filter: Filter by family name (e.g., 'diamond_2d')
        
    Returns:
        List of candidate IDs
    """
    summary = load_stage4_summary(stage4_dir)
    
    candidates = summary.get('candidates', [])
    
    # Filter by family if requested
    if family_filter:
        candidates = [
            c for c in candidates 
            if family_filter.lower() in c['candidate_id'].lower()
        ]
    
    # Filter by convergence status
    candidates = [c for c in candidates if c.get('converged', False)]
    
    # Sort by hydraulic resistance (lower is better)
    candidates.sort(key=lambda c: c.get('hydraulic_resistance', float('inf')))
    
    # Select top k
    if top_k is not None:
        candidates = candidates[:top_k]
    
    return [c['candidate_id'] for c in candidates]


def load_candidates_for_thermal(
    stage4_dir: str,
    top_k: Optional[int] = None,
    family_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Load multiple candidates for thermal validation.
    
    Args:
        stage4_dir: Path to Stage 4 results directory
        top_k: Number of top candidates to select
        family_filter: Filter by family name
        
    Returns:
        List of candidate dictionaries
    """
    candidate_ids = select_candidates_for_thermal(stage4_dir, top_k, family_filter)
    
    candidates = []
    for cand_id in candidate_ids:
        try:
            cand = load_stage4_candidate(stage4_dir, cand_id)
            candidates.append(cand)
        except Exception as e:
            print(f"Warning: Failed to load {cand_id}: {e}")
    
    return candidates
