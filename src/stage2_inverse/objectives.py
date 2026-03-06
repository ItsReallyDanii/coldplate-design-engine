"""Objectives and constraint definitions for Stage 2 inverse design.

All objectives are based on Stage 1 proxy metrics.
Proxy metrics are clearly labeled and limitations documented.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from stage1_2d.schemas import MetricResult


@dataclass
class ObjectiveTerm:
    """Single objective term."""
    name: str
    metric_name: str
    weight: float
    goal: str  # "maximize" or "minimize"
    is_proxy: bool = True
    description: str = ""
    
    def compute_score(self, metric_value: float) -> float:
        """Compute score contribution.
        
        For maximization: score = weight * value
        For minimization: score = -weight * value
        
        Returns:
            Contribution to total score (higher is better)
        """
        if self.goal == "maximize":
            return self.weight * metric_value
        elif self.goal == "minimize":
            return -self.weight * metric_value
        else:
            raise ValueError(f"Invalid goal: {self.goal}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "metric_name": self.metric_name,
            "weight": self.weight,
            "goal": self.goal,
            "is_proxy": self.is_proxy,
            "description": self.description,
        }


@dataclass
class Constraint:
    """Single constraint definition."""
    name: str
    metric_name: str
    constraint_type: str  # "min", "max", or "range"
    threshold_min: float = None
    threshold_max: float = None
    hard: bool = True  # If True, violation means invalid; if False, apply penalty
    penalty_weight: float = 1000.0  # Penalty weight for soft constraints
    description: str = ""
    
    def check(self, metric_value: float) -> bool:
        """Check if constraint is satisfied.
        
        Returns:
            True if satisfied, False if violated
        """
        if self.constraint_type == "min":
            return metric_value >= self.threshold_min
        elif self.constraint_type == "max":
            return metric_value <= self.threshold_max
        elif self.constraint_type == "range":
            return self.threshold_min <= metric_value <= self.threshold_max
        else:
            raise ValueError(f"Invalid constraint type: {self.constraint_type}")
    
    def compute_penalty(self, metric_value: float) -> float:
        """Compute penalty for constraint violation.
        
        Returns:
            Penalty value (0 if satisfied, positive if violated)
        """
        if self.check(metric_value):
            return 0.0
        
        if self.hard:
            return float('inf')  # Hard constraint violation
        
        # Soft constraint - compute penalty based on violation magnitude
        if self.constraint_type == "min":
            violation = self.threshold_min - metric_value
        elif self.constraint_type == "max":
            violation = metric_value - self.threshold_max
        elif self.constraint_type == "range":
            if metric_value < self.threshold_min:
                violation = self.threshold_min - metric_value
            else:
                violation = metric_value - self.threshold_max
        else:
            violation = 0.0
        
        return self.penalty_weight * abs(violation)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "metric_name": self.metric_name,
            "constraint_type": self.constraint_type,
            "threshold_min": self.threshold_min,
            "threshold_max": self.threshold_max,
            "hard": self.hard,
            "penalty_weight": self.penalty_weight,
            "description": self.description,
        }


@dataclass
class ObjectiveFunction:
    """Complete objective function with terms and constraints."""
    objective_terms: List[ObjectiveTerm]
    constraints: List[Constraint] = field(default_factory=list)
    name: str = "stage2_objective"
    description: str = ""
    
    def evaluate(self, metrics: Dict[str, MetricResult]) -> Dict[str, Any]:
        """Evaluate objective function on metrics.
        
        Args:
            metrics: Dictionary of metric results from Stage 1
            
        Returns:
            Dictionary with:
                - total_score: Overall score (higher is better)
                - objective_breakdown: Contribution from each term
                - constraint_violations: List of violated constraints
                - penalties: Total penalty from constraint violations
                - is_valid: Whether all hard constraints satisfied
        """
        objective_breakdown = {}
        total_objective = 0.0
        
        # Compute objective terms
        for term in self.objective_terms:
            if term.metric_name not in metrics:
                raise ValueError(f"Metric {term.metric_name} not found in results")
            metric_value = metrics[term.metric_name].value
            score = term.compute_score(metric_value)
            objective_breakdown[term.name] = {
                "value": metric_value,
                "score": score,
                "weight": term.weight,
                "goal": term.goal,
            }
            total_objective += score
        
        # Check constraints
        constraint_violations = []
        total_penalty = 0.0
        is_valid = True
        
        for constraint in self.constraints:
            if constraint.metric_name not in metrics:
                raise ValueError(f"Metric {constraint.metric_name} not found in results")
            metric_value = metrics[constraint.metric_name].value
            penalty = constraint.compute_penalty(metric_value)
            
            if penalty > 0:
                constraint_violations.append({
                    "name": constraint.name,
                    "metric": constraint.metric_name,
                    "value": metric_value,
                    "threshold_min": constraint.threshold_min,
                    "threshold_max": constraint.threshold_max,
                    "penalty": penalty,
                    "hard": constraint.hard,
                })
                total_penalty += penalty
                if constraint.hard:
                    is_valid = False
        
        # Final score = objective - penalties
        total_score = total_objective - total_penalty
        
        return {
            "total_score": total_score,
            "total_objective": total_objective,
            "objective_breakdown": objective_breakdown,
            "constraint_violations": constraint_violations,
            "total_penalty": total_penalty,
            "is_valid": is_valid,
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "objective_terms": [t.to_dict() for t in self.objective_terms],
            "constraints": [c.to_dict() for c in self.constraints],
        }


def create_default_objective() -> ObjectiveFunction:
    """Create default objective function for Stage 2.
    
    Default objective:
    - Maximize heat_exchange_area_proxy (primary goal)
    - Minimize hydraulic_resistance_proxy (secondary goal)
    - Constrain: flow must be connected
    - Constrain: porosity in reasonable range
    - Constrain: no excessive dead zones
    - Constrain: minimum feature sizes above manufacturing threshold
    
    Returns:
        ObjectiveFunction configured with default Stage 2 goals
    """
    objective_terms = [
        ObjectiveTerm(
            name="heat_transfer",
            metric_name="heat_exchange_area_proxy",
            weight=1.0,
            goal="maximize",
            is_proxy=True,
            description="Maximize heat exchange area proxy (NOT real heat transfer)"
        ),
        ObjectiveTerm(
            name="hydraulic_performance",
            metric_name="hydraulic_resistance_proxy",
            weight=0.5,
            goal="minimize",
            is_proxy=True,
            description="Minimize hydraulic resistance proxy (NOT real pressure drop)"
        ),
    ]
    
    constraints = [
        Constraint(
            name="flow_connected",
            metric_name="flow_connectivity_score",
            constraint_type="min",
            threshold_min=0.5,
            hard=True,
            description="Flow must be reasonably connected from inlet to outlet"
        ),
        Constraint(
            name="porosity_range",
            metric_name="porosity",
            constraint_type="range",
            threshold_min=0.3,
            threshold_max=0.8,
            hard=True,
            description="Porosity must be in reasonable range for cold plate"
        ),
        Constraint(
            name="dead_zone_limit",
            metric_name="dead_zone_fraction",
            constraint_type="max",
            threshold_max=0.3,
            hard=False,
            penalty_weight=500.0,
            description="Penalize excessive dead zones (soft constraint)"
        ),
        Constraint(
            name="min_fluid_feature",
            metric_name="min_fluid_feature_px",
            constraint_type="min",
            threshold_min=2.0,
            hard=False,
            penalty_weight=200.0,
            description="Penalize features below manufacturing threshold (soft)"
        ),
    ]
    
    return ObjectiveFunction(
        objective_terms=objective_terms,
        constraints=constraints,
        name="default_stage2_objective",
        description="Default Stage 2 objective: maximize heat_exchange_area_proxy, "
                    "minimize hydraulic_resistance_proxy, enforce basic constraints"
    )
