"""
Load Stage 3 geometry outputs for Stage 4 simulation.
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional


def load_stage3_summary(stage3_dir: Path) -> Dict[str, Any]:
    """
    Load Stage 3 summary.json file.
    
    Args:
        stage3_dir: Path to Stage 3 results directory
        
    Returns:
        Dictionary containing summary data with provenance_records
    """
    summary_path = stage3_dir / "summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(f"Stage 3 summary not found: {summary_path}")
    
    with open(summary_path, 'r') as f:
        summary = json.load(f)
    
    if 'provenance_records' not in summary:
        raise ValueError("Stage 3 summary missing 'provenance_records' field")
    
    return summary


def load_candidate_geometry(candidate_dir: Path) -> Dict[str, Any]:
    """
    Load a single candidate's geometry and metadata.
    
    Args:
        candidate_dir: Path to candidate directory (e.g., candidate_01_diamond_2d_s1127)
        
    Returns:
        Dictionary with:
        - volume: 3D numpy array (uint8, 1=fluid, 0=solid)
        - provenance: Full provenance record
        - metadata: Volume metadata from promotion
    """
    # Load provenance
    prov_path = candidate_dir / "provenance.json"
    if not prov_path.exists():
        raise FileNotFoundError(f"Provenance not found: {prov_path}")
    
    with open(prov_path, 'r') as f:
        provenance = json.load(f)
    
    # Load volume
    volume_path = candidate_dir / "geometry" / "volume.npy"
    if not volume_path.exists():
        raise FileNotFoundError(f"Volume not found: {volume_path}")
    
    volume = np.load(volume_path)
    
    # Extract metadata
    metadata = provenance.get('promotion', {}).get('volume_metadata', {})
    
    return {
        'volume': volume,
        'provenance': provenance,
        'metadata': metadata
    }


def select_top_k_candidates(summary: Dict[str, Any], k: int) -> List[Dict[str, Any]]:
    """
    Select top k candidates from Stage 3 summary.
    
    Args:
        summary: Stage 3 summary dictionary
        k: Number of top candidates to select
        
    Returns:
        List of provenance records for top k candidates
    """
    provenance_records = summary['provenance_records']
    
    # Sort by Stage 2 score (already ranked in summary)
    # Records should already be in rank order from Stage 3
    top_k = provenance_records[:k]
    
    return top_k


def load_candidates_for_simulation(
    stage3_dir: Path,
    top_k: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Load Stage 3 candidates for Stage 4 simulation.
    
    Args:
        stage3_dir: Path to Stage 3 results directory
        top_k: Number of top candidates to load (None = all)
        
    Returns:
        List of candidate dictionaries with volume, provenance, metadata
    """
    # Load summary
    summary = load_stage3_summary(stage3_dir)
    
    # Select candidates
    if top_k is not None:
        provenance_records = select_top_k_candidates(summary, top_k)
    else:
        provenance_records = summary['provenance_records']
    
    # Load geometry for each candidate
    candidates = []
    for prov in provenance_records:
        # Construct candidate directory path from exports
        raw_path = Path(prov['exports']['raw'])
        candidate_dir = raw_path.parent.parent
        
        # Load candidate data
        candidate_data = load_candidate_geometry(candidate_dir)
        candidates.append(candidate_data)
    
    return candidates


def get_candidate_identifier(candidate: Dict[str, Any]) -> str:
    """
    Get human-readable identifier for a candidate.
    
    Args:
        candidate: Candidate dictionary from load_candidate_geometry
        
    Returns:
        String identifier like "candidate_01_diamond_2d_s1127"
    """
    prov = candidate['provenance']
    stage2_src = prov['stage2_source']
    
    rank = stage2_src['rank']
    family = stage2_src['family']
    seed = stage2_src['seed']
    
    return f"candidate_{rank:02d}_{family}_s{seed}"


def get_candidate_score(candidate: Dict[str, Any]) -> float:
    """
    Get Stage 2 score for a candidate.
    
    Args:
        candidate: Candidate dictionary from load_candidate_geometry
        
    Returns:
        Stage 2 total score
    """
    return candidate['provenance']['stage2_source']['total_score']
