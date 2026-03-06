"""Search space definitions for Stage 2 inverse design.

Defines parameter bounds and families for optimization.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Tuple
from enum import Enum
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from stage1_2d.schemas import BaselineFamily, GridConfig


@dataclass
class ParameterBound:
    """Bounds for a single parameter."""
    name: str
    min_val: float
    max_val: float
    param_type: str = "continuous"  # "continuous" or "discrete" or "integer"
    
    def clip(self, value: float) -> float:
        """Clip value to bounds."""
        return max(self.min_val, min(self.max_val, value))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "min_val": self.min_val,
            "max_val": self.max_val,
            "param_type": self.param_type,
        }


@dataclass
class FamilySearchSpace:
    """Search space for a single baseline family."""
    family: BaselineFamily
    parameter_bounds: List[ParameterBound]
    
    def sample_random_params(self, rng) -> Dict[str, Any]:
        """Sample random parameters within bounds.
        
        Args:
            rng: numpy random generator
            
        Returns:
            Dictionary of parameter values
        """
        params = {}
        for bound in self.parameter_bounds:
            if bound.param_type == "discrete":
                # For discrete params, sample from valid discrete values
                params[bound.name] = rng.choice([bound.min_val, bound.max_val])
            elif bound.param_type == "integer":
                params[bound.name] = int(rng.integers(bound.min_val, bound.max_val + 1))
            else:
                params[bound.name] = rng.uniform(bound.min_val, bound.max_val)
        return params
    
    def validate_params(self, params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate parameters against bounds.
        
        Returns:
            (is_valid, list_of_violations)
        """
        violations = []
        for bound in self.parameter_bounds:
            if bound.name not in params:
                violations.append(f"Missing parameter: {bound.name}")
                continue
            val = params[bound.name]
            if val < bound.min_val or val > bound.max_val:
                violations.append(
                    f"{bound.name}={val} outside bounds [{bound.min_val}, {bound.max_val}]"
                )
        return len(violations) == 0, violations
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "family": self.family.value,
            "parameter_bounds": [b.to_dict() for b in self.parameter_bounds],
        }


@dataclass
class Stage2SearchSpace:
    """Complete search space for Stage 2 optimization."""
    grid: GridConfig
    family_spaces: List[FamilySearchSpace]
    allowed_families: List[BaselineFamily] = field(default_factory=list)
    
    def __post_init__(self):
        """Set allowed families if not specified."""
        if not self.allowed_families:
            self.allowed_families = [fs.family for fs in self.family_spaces]
    
    def get_family_space(self, family: BaselineFamily) -> FamilySearchSpace:
        """Get search space for a specific family."""
        for fs in self.family_spaces:
            if fs.family == family:
                return fs
        raise ValueError(f"Family {family} not in search space")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "grid": {
                "nx": self.grid.nx,
                "ny": self.grid.ny,
                "dx": self.grid.dx,
                "dy": self.grid.dy,
            },
            "family_spaces": [fs.to_dict() for fs in self.family_spaces],
            "allowed_families": [f.value for f in self.allowed_families],
        }


def create_default_search_space(grid: GridConfig) -> Stage2SearchSpace:
    """Create default search space for all families.
    
    Args:
        grid: Grid configuration
        
    Returns:
        Stage2SearchSpace with reasonable bounds for all families
    """
    family_spaces = []
    
    # Straight channel
    family_spaces.append(FamilySearchSpace(
        family=BaselineFamily.STRAIGHT_CHANNEL,
        parameter_bounds=[
            ParameterBound("num_channels", 2, 10, "integer"),
            ParameterBound("channel_width_fraction", 0.2, 0.8, "continuous"),
        ]
    ))
    
    # Serpentine channel
    family_spaces.append(FamilySearchSpace(
        family=BaselineFamily.SERPENTINE_CHANNEL,
        parameter_bounds=[
            ParameterBound("channel_width_px", 5, 20, "continuous"),
            ParameterBound("turn_radius_px", 10, 30, "continuous"),
            ParameterBound("num_passes", 2, 6, "integer"),
        ]
    ))
    
    # Pin fin
    family_spaces.append(FamilySearchSpace(
        family=BaselineFamily.PIN_FIN,
        parameter_bounds=[
            ParameterBound("pin_diameter_px", 4, 15, "continuous"),
            ParameterBound("pin_spacing_px", 15, 40, "continuous"),
            ParameterBound("offset_rows", 0, 1, "discrete"),  # Boolean as 0/1
        ]
    ))
    
    # Gyroid 2D
    family_spaces.append(FamilySearchSpace(
        family=BaselineFamily.GYROID_2D,
        parameter_bounds=[
            ParameterBound("wavelength_px", 15, 50, "continuous"),
            ParameterBound("threshold", -0.3, 0.3, "continuous"),
        ]
    ))
    
    # Diamond 2D
    family_spaces.append(FamilySearchSpace(
        family=BaselineFamily.DIAMOND_2D,
        parameter_bounds=[
            ParameterBound("wavelength_px", 15, 50, "continuous"),
            ParameterBound("threshold", -0.3, 0.3, "continuous"),
        ]
    ))
    
    # Primitive 2D
    family_spaces.append(FamilySearchSpace(
        family=BaselineFamily.PRIMITIVE_2D,
        parameter_bounds=[
            ParameterBound("wavelength_px", 15, 50, "continuous"),
            ParameterBound("threshold", -0.3, 0.3, "continuous"),
        ]
    ))
    
    return Stage2SearchSpace(grid=grid, family_spaces=family_spaces)
