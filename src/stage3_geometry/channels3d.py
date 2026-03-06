"""3D channel geometry generators.

Promotes 2D channel families to 3D extruded geometry.
"""

import numpy as np
from typing import Tuple, Dict, Any


def generate_straight_channel_3d(
    params: Dict[str, Any],
    grid_config: Dict[str, Any],
    height_mm: float = 2.0,
    resolution: int = 100
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Generate 3D straight channel geometry.
    
    Extrudes 2D straight channel pattern in Z direction.
    
    Args:
        params: Parameters dict (must have 'num_channels', 'channel_width_fraction')
        grid_config: Grid configuration
        height_mm: Height of extrusion in mm
        resolution: Grid resolution (nx=ny=nz=resolution)
        
    Returns:
        3D binary volume (nz, ny, nx) where 1=fluid, 0=solid
        Metadata dictionary
    """
    nx = ny = nz = resolution
    
    # Get parameters
    num_channels = int(params.get('num_channels', 3))
    channel_width_fraction = params.get('channel_width_fraction', 0.3)
    
    # Create 3D volume
    volume = np.zeros((nz, ny, nx), dtype=np.uint8)
    
    # Calculate channel pitch
    pitch = nx / num_channels
    channel_width_px = int(pitch * channel_width_fraction)
    
    # Generate channels in X direction, extruded through Z
    for i in range(num_channels):
        center = int((i + 0.5) * pitch)
        half_width = channel_width_px // 2
        x_start = max(0, center - half_width)
        x_end = min(nx, center + half_width)
        
        # Extrude through all Z layers
        volume[:, :, x_start:x_end] = 1
    
    metadata = {
        'type': '3d_straight_channel',
        'num_channels': num_channels,
        'channel_width_fraction': channel_width_fraction,
        'height_mm': height_mm,
        'resolution': resolution,
        'dimensions': {'nx': nx, 'ny': ny, 'nz': nz}
    }
    
    return volume, metadata


def generate_serpentine_channel_3d(
    params: Dict[str, Any],
    grid_config: Dict[str, Any],
    height_mm: float = 2.0,
    resolution: int = 100
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Generate 3D serpentine channel geometry.
    
    Extrudes 2D serpentine channel pattern in Z direction.
    
    Args:
        params: Parameters dict (must have channel width, num_passes)
        grid_config: Grid configuration
        height_mm: Height of extrusion in mm
        resolution: Grid resolution
        
    Returns:
        3D binary volume (nz, ny, nx) where 1=fluid, 0=solid
        Metadata dictionary
    """
    nx = ny = nz = resolution
    
    # Get parameters
    channel_width_px = int(params.get('channel_width_px', 10))
    num_passes = int(params.get('num_passes', 3))
    
    # Create 3D volume
    volume = np.zeros((nz, ny, nx), dtype=np.uint8)
    
    # Calculate pass spacing
    pass_spacing = ny // num_passes
    
    # Draw horizontal segments (extruded in Z)
    for i in range(num_passes):
        y_center = int((i + 0.5) * pass_spacing)
        y_start = max(0, y_center - channel_width_px // 2)
        y_end = min(ny, y_center + channel_width_px // 2)
        
        # Extrude through all Z layers
        volume[:, y_start:y_end, :] = 1
    
    metadata = {
        'type': '3d_serpentine_channel',
        'channel_width_px': channel_width_px,
        'num_passes': num_passes,
        'height_mm': height_mm,
        'resolution': resolution,
        'dimensions': {'nx': nx, 'ny': ny, 'nz': nz}
    }
    
    return volume, metadata


def generate_pin_fin_3d(
    params: Dict[str, Any],
    grid_config: Dict[str, Any],
    height_mm: float = 2.0,
    resolution: int = 100
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Generate 3D pin-fin array geometry.
    
    Creates cylindrical obstacles in a regular array.
    
    Args:
        params: Parameters dict (must have pin_diameter, spacing)
        grid_config: Grid configuration
        height_mm: Height of pins in mm
        resolution: Grid resolution
        
    Returns:
        3D binary volume (nz, ny, nx) where 1=fluid, 0=solid
        Metadata dictionary
    """
    nx = ny = nz = resolution
    
    # Get parameters
    pin_diameter_px = int(params.get('pin_diameter_px', 8))
    nx_pins = int(params.get('nx_pins', 5))
    ny_pins = int(params.get('ny_pins', 5))
    
    # Create 3D volume (start with all fluid)
    volume = np.ones((nz, ny, nx), dtype=np.uint8)
    
    # Calculate pin spacing
    x_pitch = nx / (nx_pins + 1)
    y_pitch = ny / (ny_pins + 1)
    radius_sq = (pin_diameter_px / 2.0) ** 2
    
    # Place pins
    for i in range(nx_pins):
        for j in range(ny_pins):
            pin_x = int((i + 1) * x_pitch)
            pin_y = int((j + 1) * y_pitch)
            
            # Create cylindrical pin (same cross-section through all Z)
            for z in range(nz):
                for y in range(max(0, pin_y - pin_diameter_px), 
                              min(ny, pin_y + pin_diameter_px)):
                    for x in range(max(0, pin_x - pin_diameter_px), 
                                  min(nx, pin_x + pin_diameter_px)):
                        dx = x - pin_x
                        dy = y - pin_y
                        if dx*dx + dy*dy <= radius_sq:
                            volume[z, y, x] = 0  # Solid
    
    metadata = {
        'type': '3d_pin_fin',
        'pin_diameter_px': pin_diameter_px,
        'nx_pins': nx_pins,
        'ny_pins': ny_pins,
        'height_mm': height_mm,
        'resolution': resolution,
        'dimensions': {'nx': nx, 'ny': ny, 'nz': nz}
    }
    
    return volume, metadata
