"""Data schemas for Stage 1 evaluation.

Defines data structures for configuration, geometry parameters,
metric results, and sweep outputs.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from enum import Enum


class BaselineFamily(Enum):
    """Baseline geometry families."""
    STRAIGHT_CHANNEL = "straight_channel"
    SERPENTINE_CHANNEL = "serpentine_channel"
    PIN_FIN = "pin_fin"
    GYROID_2D = "gyroid_2d"
    DIAMOND_2D = "diamond_2d"
    PRIMITIVE_2D = "primitive_2d"


class MetricCategory(Enum):
    """Metric categories for honest labeling."""
    GEOMETRIC = "geometric"
    FLOW_PROXY = "flow_proxy"
    HEAT_PROXY = "heat_proxy"


@dataclass
class GridConfig:
    """Grid configuration for 2D mask generation."""
    nx: int
    ny: int
    dx: float  # meters
    dy: float  # meters
    
    @property
    def width(self) -> float:
        """Grid width in meters."""
        return self.nx * self.dx
    
    @property
    def height(self) -> float:
        """Grid height in meters."""
        return self.ny * self.dy


@dataclass
class BaselineParams:
    """Parameters for baseline geometry generation."""
    family: BaselineFamily
    grid: GridConfig
    seed: int
    params: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "family": self.family.value,
            "grid": {
                "nx": self.grid.nx,
                "ny": self.grid.ny,
                "dx": self.grid.dx,
                "dy": self.grid.dy,
            },
            "seed": self.seed,
            "params": self.params,
        }
        return result


@dataclass
class MetricDefinition:
    """Definition of a single metric."""
    name: str
    category: MetricCategory
    units: Optional[str]
    description: str
    is_proxy: bool
    assumptions: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "category": self.category.value,
            "units": self.units,
            "description": self.description,
            "is_proxy": self.is_proxy,
            "assumptions": self.assumptions,
            "limitations": self.limitations,
        }


@dataclass
class MetricResult:
    """Result for a single metric."""
    value: float
    definition: MetricDefinition
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "value": self.value,
            "name": self.definition.name,
            "category": self.definition.category.value,
            "units": self.definition.units,
            "is_proxy": self.definition.is_proxy,
        }


@dataclass
class EvaluationResult:
    """Complete evaluation result for a single mask."""
    mask_id: str
    baseline_params: Optional[BaselineParams]
    metrics: Dict[str, MetricResult]
    timestamp: str
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "mask_id": self.mask_id,
            "baseline_params": self.baseline_params.to_dict() if self.baseline_params else None,
            "metrics": {k: v.to_dict() for k, v in self.metrics.items()},
            "timestamp": self.timestamp,
            "warnings": self.warnings,
        }


@dataclass
class SweepConfig:
    """Configuration for a parameter sweep."""
    output_dir: str
    grid: GridConfig
    families: List[BaselineFamily]
    param_ranges: Dict[str, List[Any]]
    seed_start: int = 0
    num_samples_per_config: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "output_dir": self.output_dir,
            "grid": {
                "nx": self.grid.nx,
                "ny": self.grid.ny,
                "dx": self.grid.dx,
                "dy": self.grid.dy,
            },
            "families": [f.value for f in self.families],
            "param_ranges": self.param_ranges,
            "seed_start": self.seed_start,
            "num_samples_per_config": self.num_samples_per_config,
        }


@dataclass
class SweepManifest:
    """Manifest for a completed sweep run."""
    timestamp: str
    git_sha: Optional[str]
    config: SweepConfig
    num_evaluations: int
    metric_schema_version: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp,
            "git_sha": self.git_sha,
            "config": self.config.to_dict(),
            "num_evaluations": self.num_evaluations,
            "metric_schema_version": self.metric_schema_version,
        }
