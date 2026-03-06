"""Input/output utilities for Stage 1."""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from .schemas import EvaluationResult, SweepManifest


def save_mask(mask: np.ndarray, output_path: str) -> None:
    """Save binary mask to file.
    
    Args:
        mask: Binary mask
        output_path: Output file path (.npy)
    """
    np.save(output_path, mask)


def load_mask(input_path: str) -> np.ndarray:
    """Load binary mask from file.
    
    Args:
        input_path: Input file path (.npy)
        
    Returns:
        Binary mask
    """
    return np.load(input_path)


def save_evaluation_result(result: EvaluationResult, output_path: str) -> None:
    """Save evaluation result to JSON file.
    
    Args:
        result: Evaluation result
        output_path: Output file path (.json)
    """
    with open(output_path, 'w') as f:
        json.dump(result.to_dict(), f, indent=2)


def load_evaluation_result(input_path: str) -> Dict[str, Any]:
    """Load evaluation result from JSON file.
    
    Args:
        input_path: Input file path (.json)
        
    Returns:
        Evaluation result dictionary
    """
    with open(input_path, 'r') as f:
        return json.load(f)


def save_metrics_csv(results: List[EvaluationResult], output_path: str) -> None:
    """Save metrics to CSV file.
    
    Args:
        results: List of evaluation results
        output_path: Output file path (.csv)
    """
    records = []
    
    for result in results:
        record = {
            "mask_id": result.mask_id,
            "timestamp": result.timestamp,
        }
        
        # Add baseline params if available
        if result.baseline_params:
            record["family"] = result.baseline_params.family.value
            record["seed"] = result.baseline_params.seed
            for key, value in result.baseline_params.params.items():
                record[f"param_{key}"] = value
        
        # Add all metrics
        for metric_name, metric_result in result.metrics.items():
            record[metric_name] = metric_result.value
            record[f"{metric_name}_is_proxy"] = metric_result.definition.is_proxy
        
        # Add warning count
        record["num_warnings"] = len(result.warnings)
        
        records.append(record)
    
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)


def save_metrics_jsonl(results: List[EvaluationResult], output_path: str) -> None:
    """Save metrics to JSONL file (one JSON object per line).
    
    Args:
        results: List of evaluation results
        output_path: Output file path (.jsonl)
    """
    with open(output_path, 'w') as f:
        for result in results:
            json.dump(result.to_dict(), f)
            f.write('\n')


def save_sweep_manifest(manifest: SweepManifest, output_path: str) -> None:
    """Save sweep manifest to JSON file.
    
    Args:
        manifest: Sweep manifest
        output_path: Output file path (.json)
    """
    with open(output_path, 'w') as f:
        json.dump(manifest.to_dict(), f, indent=2)


def ensure_output_dir(output_dir: str) -> Path:
    """Ensure output directory exists.
    
    Args:
        output_dir: Output directory path
        
    Returns:
        Path object for output directory
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path
