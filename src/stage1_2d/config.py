"""Configuration loading and validation."""

import yaml
from pathlib import Path
from typing import Dict, Any, List
from .schemas import SweepConfig, GridConfig, BaselineFamily


def load_config(config_path: str) -> SweepConfig:
    """Load sweep configuration from YAML file.
    
    Args:
        config_path: Path to YAML config file
        
    Returns:
        SweepConfig object
        
    Raises:
        ValueError: If config is invalid
    """
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    return parse_config(config_dict)


def parse_config(config_dict: Dict[str, Any]) -> SweepConfig:
    """Parse configuration dictionary into SweepConfig.
    
    Args:
        config_dict: Configuration dictionary
        
    Returns:
        SweepConfig object
        
    Raises:
        ValueError: If config is invalid
    """
    # Parse grid
    grid_dict = config_dict.get("grid", {})
    grid = GridConfig(
        nx=grid_dict["nx"],
        ny=grid_dict["ny"],
        dx=grid_dict["dx"],
        dy=grid_dict["dy"]
    )
    
    # Parse families
    family_strs = config_dict.get("families", [])
    families = [BaselineFamily(f) for f in family_strs]
    
    # Parse param ranges
    param_ranges = config_dict.get("param_ranges", {})
    
    # Parse other settings
    output_dir = config_dict.get("output_dir", "results/stage1_2d")
    seed_start = config_dict.get("seed_start", 0)
    num_samples = config_dict.get("num_samples_per_config", 1)
    
    return SweepConfig(
        output_dir=output_dir,
        grid=grid,
        families=families,
        param_ranges=param_ranges,
        seed_start=seed_start,
        num_samples_per_config=num_samples
    )


def get_default_param_ranges() -> Dict[str, List[Any]]:
    """Get default parameter ranges for baseline families.
    
    Returns:
        Dictionary of parameter ranges
    """
    return {
        "straight_channel": {
            "num_channels": [2, 4, 8, 16],
            "channel_width_fraction": [0.4, 0.5, 0.6],
        },
        "serpentine_channel": {
            "channel_width_px": [5, 10, 15],
            "turn_radius_px": [10, 20],
            "num_passes": [3, 5, 7],
        },
        "pin_fin": {
            "pin_diameter_px": [5, 10, 15],
            "pin_spacing_px": [20, 30, 40],
            "offset_rows": [True, False],
        },
        "gyroid_2d": {
            "wavelength_px": [20, 30, 40],
            "threshold": [-0.1, 0.0, 0.1],
        },
        "diamond_2d": {
            "wavelength_px": [20, 30, 40],
            "threshold": [-0.1, 0.0, 0.1],
        },
        "primitive_2d": {
            "wavelength_px": [20, 30, 40],
            "threshold": [-0.1, 0.0, 0.1],
        },
    }
