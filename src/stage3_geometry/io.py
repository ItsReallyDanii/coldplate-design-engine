"""I/O utilities for Stage 3 geometry promotion.

Handles loading Stage 2 candidates and saving Stage 3 outputs.
"""

import csv
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timezone


def load_stage2_candidates(filepath: str) -> List[Dict[str, Any]]:
    """Load Stage 2 candidates from CSV file.
    
    Args:
        filepath: Path to best_candidates.csv or similar
        
    Returns:
        List of candidate dictionaries with parsed parameters
    """
    candidates = []
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse candidate
            candidate = {
                'rank': int(row['rank']),
                'method': row['method'],
                'family': row['family'],
                'total_score': float(row['total_score']),
                'total_objective': float(row['total_objective']),
                'total_penalty': float(row['total_penalty']),
                'is_valid': row['is_valid'] == 'True',
                'evaluation_num': int(row['evaluation_num']),
                'seed': int(row['seed']),
                'mask_id': row['mask_id'],
            }
            
            # Extract parameters (param_* columns)
            params = {}
            for key, value in row.items():
                if key.startswith('param_'):
                    param_name = key[6:]  # Remove 'param_' prefix
                    if value:
                        params[param_name] = float(value)
            candidate['params'] = params
            
            # Extract metrics
            metrics = {}
            metric_keys = [
                'porosity', 'heat_exchange_area_proxy',
                'hydraulic_resistance_proxy', 'flow_connectivity_score',
                'dead_zone_fraction'
            ]
            for key in metric_keys:
                if key in row and row[key]:
                    metrics[key] = float(row[key])
            candidate['metrics'] = metrics
            
            candidates.append(candidate)
    
    return candidates


def select_top_k_candidates(
    candidates: List[Dict[str, Any]],
    k: int = 5,
    family_filter: Optional[str] = None,
    valid_only: bool = True
) -> List[Dict[str, Any]]:
    """Select top-k candidates from loaded candidates.
    
    Args:
        candidates: List of candidates from load_stage2_candidates
        k: Number of candidates to select
        family_filter: Optional family filter (e.g., 'diamond_2d')
        valid_only: Only select valid candidates
        
    Returns:
        Top-k candidates
    """
    filtered = candidates
    
    if valid_only:
        filtered = [c for c in filtered if c['is_valid']]
    
    if family_filter:
        filtered = [c for c in filtered if c['family'] == family_filter]
    
    # Already ranked by Stage 2, take first k
    return filtered[:k]


def save_json(data: Dict[str, Any], filepath: str):
    """Save dictionary as JSON.
    
    Args:
        data: Dictionary to save
        filepath: Output file path
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved JSON to {filepath}")


def save_text(text: str, filepath: str):
    """Save text to file.
    
    Args:
        text: Text content
        filepath: Output file path
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        f.write(text)
    
    print(f"Saved text to {filepath}")


def ensure_output_dir(output_dir: str):
    """Ensure output directory exists.
    
    Args:
        output_dir: Output directory path
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)


def create_candidate_output_dir(base_dir: str, rank: int, family: str, seed: int) -> str:
    """Create output directory for a specific candidate.
    
    Args:
        base_dir: Base output directory
        rank: Candidate rank
        family: Family name
        seed: Seed value
        
    Returns:
        Path to candidate-specific directory
    """
    candidate_dir = os.path.join(base_dir, f"candidate_{rank:02d}_{family}_s{seed}")
    ensure_output_dir(candidate_dir)
    ensure_output_dir(os.path.join(candidate_dir, "geometry"))
    ensure_output_dir(os.path.join(candidate_dir, "validation"))
    return candidate_dir
