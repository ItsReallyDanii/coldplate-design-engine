"""
I/O functions for Stage 6 structural screening.
"""

import os
import json
from typing import Dict, Any


def save_candidate_metrics(
    output_dir: str,
    candidate_id: str,
    metrics: Dict[str, Any]
) -> None:
    """
    Save candidate metrics to JSON file.
    
    Args:
        output_dir: Output directory path
        candidate_id: Candidate identifier
        metrics: Metrics dictionary
    """
    cand_dir = os.path.join(output_dir, candidate_id)
    os.makedirs(cand_dir, exist_ok=True)
    
    filepath = os.path.join(cand_dir, 'structural_metrics.json')
    
    with open(filepath, 'w') as f:
        json.dump(metrics, f, indent=2)


def save_comparison_summary(
    output_dir: str,
    comparison: Dict[str, Any]
) -> None:
    """
    Save comparison summary to JSON file.
    
    Args:
        output_dir: Output directory path
        comparison: Comparison summary dictionary
    """
    filepath = os.path.join(output_dir, 'structural_comparison.json')
    
    with open(filepath, 'w') as f:
        json.dump(comparison, f, indent=2)


def save_comparison_markdown(
    output_dir: str,
    markdown_text: str
) -> None:
    """
    Save comparison summary as Markdown file.
    
    Args:
        output_dir: Output directory path
        markdown_text: Markdown formatted text
    """
    filepath = os.path.join(output_dir, 'structural_comparison_summary.md')
    
    with open(filepath, 'w') as f:
        f.write(markdown_text)


def save_stage6_summary(
    output_dir: str,
    summary: Dict[str, Any]
) -> None:
    """
    Save Stage 6 overall summary.
    
    Args:
        output_dir: Output directory path
        summary: Summary dictionary
    """
    filepath = os.path.join(output_dir, 'stage6_summary.json')
    
    with open(filepath, 'w') as f:
        json.dump(summary, f, indent=2)


def save_run_manifest(
    output_dir: str,
    manifest: Dict[str, Any]
) -> None:
    """
    Save run manifest with execution metadata.
    
    Args:
        output_dir: Output directory path
        manifest: Manifest dictionary
    """
    filepath = os.path.join(output_dir, 'run_manifest.json')
    
    with open(filepath, 'w') as f:
        json.dump(manifest, f, indent=2)
