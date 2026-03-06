"""Single-mask evaluation module."""

import numpy as np
from datetime import datetime, timezone
from typing import Optional, List
from .schemas import BaselineParams, EvaluationResult
from .masks import load_and_validate_mask
from .metrics import compute_all_metrics, get_metric_schema_version


def evaluate_mask(
    mask: np.ndarray,
    mask_id: str,
    baseline_params: Optional[BaselineParams] = None,
    inlet_side: str = "left",
    outlet_side: str = "right",
    enforce_binary_threshold: float = 0.5,
    check_connectivity: bool = True
) -> EvaluationResult:
    """Evaluate a single mask.
    
    Args:
        mask: Binary mask (1 = fluid, 0 = solid)
        mask_id: Identifier for this mask
        baseline_params: Baseline parameters if generated, None if external
        inlet_side: Inlet side
        outlet_side: Outlet side
        enforce_binary_threshold: Threshold for binary enforcement
        check_connectivity: Whether to check connectivity
        
    Returns:
        EvaluationResult with all metrics and warnings
    """
    # Validate mask
    grid = baseline_params.grid if baseline_params else None
    
    if grid is not None:
        validated_mask, warnings = load_and_validate_mask(
            mask, grid, enforce_binary_threshold, check_connectivity,
            inlet_side, outlet_side
        )
    else:
        # External mask without known grid - just enforce binary
        from .masks import enforce_binary
        validated_mask = enforce_binary(mask, enforce_binary_threshold)
        warnings = ["External mask - grid validation skipped"]
    
    # Compute all metrics
    metrics = compute_all_metrics(validated_mask, inlet_side, outlet_side)
    
    # Create result
    result = EvaluationResult(
        mask_id=mask_id,
        baseline_params=baseline_params,
        metrics=metrics,
        timestamp=datetime.now(timezone.utc).isoformat(),
        warnings=warnings
    )
    
    return result
