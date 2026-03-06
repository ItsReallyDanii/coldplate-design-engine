"""Random baseline sampler for Stage 2 inverse design.

Provides random search baseline for fair comparison.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from stage1_2d.schemas import BaselineFamily, BaselineParams, GridConfig, EvaluationResult
from stage1_2d.generators import generate_baseline_mask
from stage1_2d.evaluate import evaluate_mask
from .search_space import Stage2SearchSpace
from .objectives import ObjectiveFunction


class RandomSearchSampler:
    """Random search baseline sampler."""
    
    def __init__(
        self,
        search_space: Stage2SearchSpace,
        objective_func: ObjectiveFunction,
        seed: int = 42
    ):
        """Initialize random sampler.
        
        Args:
            search_space: Stage 2 search space definition
            objective_func: Objective function for scoring
            seed: Random seed for reproducibility
        """
        self.search_space = search_space
        self.objective_func = objective_func
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        
        self.evaluation_count = 0
        self.history = []
    
    def sample_candidate(self) -> Tuple[BaselineFamily, Dict[str, Any], int]:
        """Sample a random candidate from search space.
        
        Returns:
            (family, params, seed)
        """
        # Random family selection from allowed families
        family = self.rng.choice(self.search_space.allowed_families)
        
        # Get family-specific search space
        family_space = self.search_space.get_family_space(family)
        
        # Sample random parameters
        params = family_space.sample_random_params(self.rng)
        
        # Handle discrete boolean parameters
        if "offset_rows" in params:
            params["offset_rows"] = bool(int(params["offset_rows"]))
        
        # Generate unique seed for this sample
        sample_seed = self.seed + self.evaluation_count
        
        return family, params, sample_seed
    
    def evaluate_candidate(
        self,
        family: BaselineFamily,
        params: Dict[str, Any],
        sample_seed: int
    ) -> Dict[str, Any]:
        """Evaluate a candidate design.
        
        Args:
            family: Baseline family
            params: Parameters for the family
            sample_seed: Seed for generation
            
        Returns:
            Evaluation result dictionary
        """
        # Create BaselineParams
        baseline_params = BaselineParams(
            family=family,
            grid=self.search_space.grid,
            seed=sample_seed,
            params=params
        )
        
        # Generate mask
        evaluation_num = self.evaluation_count
        self.evaluation_count += 1
        
        try:
            mask, metadata = generate_baseline_mask(
                family, self.search_space.grid, params, sample_seed
            )
        except Exception as e:
            result = {
                "family": family.value,
                "params": params,
                "seed": sample_seed,
                "evaluation_num": evaluation_num,
                "is_valid": False,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self.history.append(result)
            return result
        
        # Evaluate mask
        mask_id = f"{family.value}_s{sample_seed}_eval{evaluation_num}"
        eval_result = evaluate_mask(mask, mask_id, baseline_params)
        
        # Score with objective function
        obj_result = self.objective_func.evaluate(eval_result.metrics)
        
        # Combine results
        result = {
            "family": family.value,
            "params": params,
            "seed": sample_seed,
            "evaluation_num": evaluation_num,
            "mask_id": mask_id,
            "total_score": obj_result["total_score"],
            "total_objective": obj_result["total_objective"],
            "total_penalty": obj_result["total_penalty"],
            "is_valid": obj_result["is_valid"],
            "objective_breakdown": obj_result["objective_breakdown"],
            "constraint_violations": obj_result["constraint_violations"],
            "metrics": {k: v.value for k, v in eval_result.metrics.items()},
            "warnings": eval_result.warnings,
            "timestamp": eval_result.timestamp,
        }
        
        self.history.append(result)
        
        return result
    
    def run(self, budget: int) -> List[Dict[str, Any]]:
        """Run random search with given budget.
        
        Args:
            budget: Number of evaluations to perform
            
        Returns:
            List of all evaluation results
        """
        results = []
        
        for i in range(budget):
            family, params, sample_seed = self.sample_candidate()
            result = self.evaluate_candidate(family, params, sample_seed)
            results.append(result)
            
            # Progress logging
            if (i + 1) % 10 == 0 or (i + 1) == budget:
                valid_count = sum(1 for r in results if r["is_valid"])
                print(f"Random search: {i+1}/{budget} evaluations, "
                      f"{valid_count} valid candidates")
        
        return results
    
    def get_best(self, k: int = 1, valid_only: bool = True) -> List[Dict[str, Any]]:
        """Get best k candidates.
        
        Args:
            k: Number of top candidates to return
            valid_only: Only consider valid candidates
            
        Returns:
            List of top k candidates sorted by score (descending)
        """
        candidates = self.history
        if valid_only:
            candidates = [c for c in candidates if c["is_valid"]]
        
        if not candidates:
            return []
        
        # Sort by total score (descending)
        sorted_candidates = sorted(
            candidates,
            key=lambda x: x["total_score"],
            reverse=True
        )
        
        return sorted_candidates[:k]
