"""Baseline geometry generators for Stage 1.

Generates 2D binary masks for baseline families:
- Straight channels
- Serpentine channels
- Pin-fin arrays
- TPMS-adjacent 2D proxy families (gyroid-like, diamond-like, primitive-like)

All generators produce binary masks where:
- 0 = solid material
- 1 = fluid/open region
"""

import numpy as np
from typing import Tuple
from .schemas import BaselineFamily, GridConfig


def generate_straight_channel(
    grid: GridConfig,
    num_channels: int,
    channel_width_fraction: float,
    seed: int
) -> Tuple[np.ndarray, dict]:
    """Generate straight parallel channels.
    
    Args:
        grid: Grid configuration
        num_channels: Number of parallel channels
        channel_width_fraction: Channel width as fraction of pitch
        seed: Random seed for reproducibility
        
    Returns:
        Binary mask (ny, nx) and generation metadata
    """
    np.random.seed(seed)
    
    mask = np.zeros((grid.ny, grid.nx), dtype=np.uint8)
    
    # Calculate channel pitch
    pitch = grid.nx / num_channels
    channel_width_px = int(pitch * channel_width_fraction)
    
    # Generate channels
    for i in range(num_channels):
        center = int((i + 0.5) * pitch)
        half_width = channel_width_px // 2
        x_start = max(0, center - half_width)
        x_end = min(grid.nx, center + half_width)
        mask[:, x_start:x_end] = 1
    
    metadata = {
        "num_channels": num_channels,
        "channel_width_fraction": channel_width_fraction,
        "actual_channel_width_px": channel_width_px,
        "pitch_px": pitch,
    }
    
    return mask, metadata


def generate_serpentine_channel(
    grid: GridConfig,
    channel_width_px: int,
    turn_radius_px: int,
    num_passes: int,
    seed: int
) -> Tuple[np.ndarray, dict]:
    """Generate serpentine (meandering) channel.
    
    Args:
        grid: Grid configuration
        channel_width_px: Channel width in pixels
        turn_radius_px: Turning radius in pixels
        num_passes: Number of horizontal passes
        seed: Random seed
        
    Returns:
        Binary mask (ny, nx) and generation metadata
    """
    np.random.seed(seed)
    
    mask = np.zeros((grid.ny, grid.nx), dtype=np.uint8)
    
    # Calculate pass spacing
    pass_spacing = grid.ny // num_passes
    
    # Draw horizontal segments and turns
    for i in range(num_passes):
        y_center = int((i + 0.5) * pass_spacing)
        y_start = max(0, y_center - channel_width_px // 2)
        y_end = min(grid.ny, y_center + channel_width_px // 2)
        
        if i % 2 == 0:
            # Left to right
            mask[y_start:y_end, :] = 1
        else:
            # Right to left
            mask[y_start:y_end, :] = 1
        
        # Add turn if not last pass
        if i < num_passes - 1:
            # Simple vertical connector (real serpentine would have curved turns)
            y_next = int((i + 1.5) * pass_spacing)
            y_turn_start = min(y_end, y_next - channel_width_px // 2)
            y_turn_end = max(y_start, y_next + channel_width_px // 2)
            
            if i % 2 == 0:
                # Connect on right side
                x_turn = grid.nx - turn_radius_px
                mask[y_turn_start:y_turn_end, x_turn:] = 1
            else:
                # Connect on left side
                mask[y_turn_start:y_turn_end, :turn_radius_px] = 1
    
    metadata = {
        "channel_width_px": channel_width_px,
        "turn_radius_px": turn_radius_px,
        "num_passes": num_passes,
        "pass_spacing_px": pass_spacing,
    }
    
    return mask, metadata


def generate_pin_fin(
    grid: GridConfig,
    pin_diameter_px: int,
    pin_spacing_px: int,
    offset_rows: bool,
    seed: int
) -> Tuple[np.ndarray, dict]:
    """Generate pin-fin or obstacle array pattern.
    
    Args:
        grid: Grid configuration
        pin_diameter_px: Pin diameter in pixels
        pin_spacing_px: Center-to-center pin spacing
        offset_rows: Whether to offset alternate rows (staggered pattern)
        seed: Random seed
        
    Returns:
        Binary mask (ny, nx) and generation metadata
    """
    np.random.seed(seed)
    
    # Start with all fluid
    mask = np.ones((grid.ny, grid.nx), dtype=np.uint8)
    
    # Create coordinate grids
    y, x = np.ogrid[:grid.ny, :grid.nx]
    
    # Place pins
    pin_radius = pin_diameter_px / 2.0
    num_pins = 0
    
    for i, y_center in enumerate(range(pin_spacing_px // 2, grid.ny, pin_spacing_px)):
        x_offset = (pin_spacing_px // 2) if (offset_rows and i % 2 == 1) else 0
        for x_center in range(pin_spacing_px // 2 + x_offset, grid.nx, pin_spacing_px):
            # Create circular pin
            dist = np.sqrt((x - x_center)**2 + (y - y_center)**2)
            mask[dist <= pin_radius] = 0
            num_pins += 1
    
    metadata = {
        "pin_diameter_px": pin_diameter_px,
        "pin_spacing_px": pin_spacing_px,
        "offset_rows": offset_rows,
        "num_pins": num_pins,
    }
    
    return mask, metadata


def generate_gyroid_2d_proxy(
    grid: GridConfig,
    wavelength_px: float,
    threshold: float,
    seed: int
) -> Tuple[np.ndarray, dict]:
    """Generate 2D gyroid-like pattern (HONEST PROXY).
    
    This is a 2D approximation using an implicit function that mimics
    gyroid topology. It is NOT a true 3D gyroid cross-section.
    
    Args:
        grid: Grid configuration
        wavelength_px: Characteristic wavelength in pixels
        threshold: Threshold for binary conversion (0.0 = 50% porosity)
        seed: Random seed
        
    Returns:
        Binary mask (ny, nx) and generation metadata
    """
    np.random.seed(seed)
    
    # Create coordinate grids
    y, x = np.ogrid[:grid.ny, :grid.nx]
    
    # Gyroid-like implicit function: sin(x)cos(y) + sin(y)cos(z) + sin(z)cos(x)
    # For 2D, approximate with: sin(kx)cos(ky) + sin(ky)cos(kx)
    k = 2 * np.pi / wavelength_px
    
    field = (
        np.sin(k * x) * np.cos(k * y) +
        np.sin(k * y) * np.cos(k * x)
    )
    
    # Normalize and threshold
    field_normalized = (field - field.min()) / (field.max() - field.min())
    mask = (field_normalized > (0.5 + threshold)).astype(np.uint8)
    
    metadata = {
        "wavelength_px": wavelength_px,
        "threshold": threshold,
        "implicit_function": "sin(kx)cos(ky) + sin(ky)cos(kx)",
        "is_2d_proxy": True,
        "not_true_3d_gyroid": True,
    }
    
    return mask, metadata


def generate_diamond_2d_proxy(
    grid: GridConfig,
    wavelength_px: float,
    threshold: float,
    seed: int
) -> Tuple[np.ndarray, dict]:
    """Generate 2D diamond-like pattern (HONEST PROXY).
    
    This is a 2D approximation using an implicit function that mimics
    diamond topology. It is NOT a true 3D diamond cross-section.
    
    Args:
        grid: Grid configuration
        wavelength_px: Characteristic wavelength in pixels
        threshold: Threshold for binary conversion
        seed: Random seed
        
    Returns:
        Binary mask (ny, nx) and generation metadata
    """
    np.random.seed(seed)
    
    # Create coordinate grids
    y, x = np.ogrid[:grid.ny, :grid.nx]
    
    # Diamond-like implicit function
    k = 2 * np.pi / wavelength_px
    
    field = (
        np.sin(k * x) * np.sin(k * y) * np.cos(k * (x + y) / 2) +
        np.cos(k * x) * np.cos(k * y)
    )
    
    # Normalize and threshold
    field_normalized = (field - field.min()) / (field.max() - field.min())
    mask = (field_normalized > (0.5 + threshold)).astype(np.uint8)
    
    metadata = {
        "wavelength_px": wavelength_px,
        "threshold": threshold,
        "implicit_function": "sin(kx)sin(ky)cos(k(x+y)/2) + cos(kx)cos(ky)",
        "is_2d_proxy": True,
        "not_true_3d_diamond": True,
    }
    
    return mask, metadata


def generate_primitive_2d_proxy(
    grid: GridConfig,
    wavelength_px: float,
    threshold: float,
    seed: int
) -> Tuple[np.ndarray, dict]:
    """Generate 2D primitive-like pattern (HONEST PROXY).
    
    This is a 2D approximation using an implicit function that mimics
    primitive (Schwarz P) topology. It is NOT a true 3D primitive cross-section.
    
    Args:
        grid: Grid configuration
        wavelength_px: Characteristic wavelength in pixels
        threshold: Threshold for binary conversion
        seed: Random seed
        
    Returns:
        Binary mask (ny, nx) and generation metadata
    """
    np.random.seed(seed)
    
    # Create coordinate grids
    y, x = np.ogrid[:grid.ny, :grid.nx]
    
    # Primitive-like implicit function: cos(x) + cos(y) + cos(z)
    # For 2D: cos(kx) + cos(ky)
    k = 2 * np.pi / wavelength_px
    
    field = np.cos(k * x) + np.cos(k * y)
    
    # Normalize and threshold
    field_normalized = (field - field.min()) / (field.max() - field.min())
    mask = (field_normalized > (0.5 + threshold)).astype(np.uint8)
    
    metadata = {
        "wavelength_px": wavelength_px,
        "threshold": threshold,
        "implicit_function": "cos(kx) + cos(ky)",
        "is_2d_proxy": True,
        "not_true_3d_primitive": True,
    }
    
    return mask, metadata


def generate_baseline_mask(
    family: BaselineFamily,
    grid: GridConfig,
    params: dict,
    seed: int
) -> Tuple[np.ndarray, dict]:
    """Generate baseline mask for given family and parameters.
    
    Args:
        family: Baseline family
        grid: Grid configuration
        params: Family-specific parameters
        seed: Random seed
        
    Returns:
        Binary mask (ny, nx) and generation metadata
        
    Raises:
        ValueError: If family is unknown or parameters are invalid
    """
    if family == BaselineFamily.STRAIGHT_CHANNEL:
        return generate_straight_channel(
            grid,
            params["num_channels"],
            params["channel_width_fraction"],
            seed
        )
    elif family == BaselineFamily.SERPENTINE_CHANNEL:
        return generate_serpentine_channel(
            grid,
            params["channel_width_px"],
            params["turn_radius_px"],
            params["num_passes"],
            seed
        )
    elif family == BaselineFamily.PIN_FIN:
        return generate_pin_fin(
            grid,
            params["pin_diameter_px"],
            params["pin_spacing_px"],
            params.get("offset_rows", False),
            seed
        )
    elif family == BaselineFamily.GYROID_2D:
        return generate_gyroid_2d_proxy(
            grid,
            params["wavelength_px"],
            params.get("threshold", 0.0),
            seed
        )
    elif family == BaselineFamily.DIAMOND_2D:
        return generate_diamond_2d_proxy(
            grid,
            params["wavelength_px"],
            params.get("threshold", 0.0),
            seed
        )
    elif family == BaselineFamily.PRIMITIVE_2D:
        return generate_primitive_2d_proxy(
            grid,
            params["wavelength_px"],
            params.get("threshold", 0.0),
            seed
        )
    else:
        raise ValueError(f"Unknown baseline family: {family}")
