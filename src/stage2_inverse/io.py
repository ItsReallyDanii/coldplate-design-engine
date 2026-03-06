"""I/O utilities for Stage 2 inverse design.

Handles saving/loading results, manifests, and comparisons.
"""

import json
import csv
import os
from typing import List, Dict, Any
from datetime import datetime, timezone
from pathlib import Path


def save_jsonl(results: List[Dict[str, Any]], filepath: str):
    """Save results as JSONL (one JSON object per line).
    
    Args:
        results: List of result dictionaries
        filepath: Output file path
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        for result in results:
            json.dump(result, f)
            f.write('\n')
    
    print(f"Saved {len(results)} results to {filepath}")


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


def save_best_candidates_csv(
    candidates: List[Dict[str, Any]],
    filepath: str,
    method_name: str = ""
):
    """Save best candidates to CSV.
    
    Args:
        candidates: List of candidate result dictionaries
        filepath: Output CSV path
        method_name: Name of method (for column)
    """
    if not candidates:
        print(f"No candidates to save to {filepath}")
        return
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', newline='') as f:
        # Determine columns
        fieldnames = [
            "rank",
            "method",
            "family",
            "total_score",
            "total_objective",
            "total_penalty",
            "is_valid",
            "evaluation_num",
            "seed",
            "mask_id",
        ]
        
        # Add parameter columns (collect all unique param names)
        all_param_names = set()
        for cand in candidates:
            if "params" in cand:
                all_param_names.update(cand["params"].keys())
        param_names = sorted(all_param_names)
        fieldnames.extend([f"param_{p}" for p in param_names])
        
        # Add key metrics
        key_metrics = [
            "porosity",
            "heat_exchange_area_proxy",
            "hydraulic_resistance_proxy",
            "flow_connectivity_score",
            "dead_zone_fraction",
        ]
        fieldnames.extend(key_metrics)
        
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for i, cand in enumerate(candidates):
            row = {
                "rank": i + 1,
                "method": method_name,
                "family": cand.get("family", ""),
                "total_score": cand.get("total_score", ""),
                "total_objective": cand.get("total_objective", ""),
                "total_penalty": cand.get("total_penalty", ""),
                "is_valid": cand.get("is_valid", ""),
                "evaluation_num": cand.get("evaluation_num", ""),
                "seed": cand.get("seed", ""),
                "mask_id": cand.get("mask_id", ""),
            }
            
            # Add parameters
            if "params" in cand:
                for param_name in param_names:
                    row[f"param_{param_name}"] = cand["params"].get(param_name, "")
            
            # Add metrics
            if "metrics" in cand:
                for metric in key_metrics:
                    row[metric] = cand["metrics"].get(metric, "")
            
            writer.writerow(row)
    
    print(f"Saved {len(candidates)} candidates to {filepath}")


def create_run_manifest(
    method_name: str,
    search_space_dict: Dict[str, Any],
    objective_dict: Dict[str, Any],
    budget: int,
    seed: int,
    num_evaluations: int,
    git_sha: str = None
) -> Dict[str, Any]:
    """Create run manifest.
    
    Args:
        method_name: Name of optimization method
        search_space_dict: Search space configuration
        objective_dict: Objective function configuration
        budget: Evaluation budget
        seed: Random seed
        num_evaluations: Actual number of evaluations performed
        git_sha: Git commit SHA
        
    Returns:
        Manifest dictionary
    """
    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_sha": git_sha,
        "stage": "stage2_inverse",
        "method": method_name,
        "budget": budget,
        "seed": seed,
        "num_evaluations": num_evaluations,
        "search_space": search_space_dict,
        "objective": objective_dict,
    }
    
    return manifest


def load_jsonl(filepath: str) -> List[Dict[str, Any]]:
    """Load JSONL file.
    
    Args:
        filepath: Path to JSONL file
        
    Returns:
        List of dictionaries
    """
    results = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    return results


def ensure_output_dir(output_dir: str):
    """Ensure output directory exists.
    
    Args:
        output_dir: Output directory path
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
