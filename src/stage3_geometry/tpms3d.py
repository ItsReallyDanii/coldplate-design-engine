"""3D TPMS geometry generators.

Generates true 3D triply periodic minimal surface volumes
using implicit field equations.
"""

import numpy as np
from typing import Tuple, Dict, Any


def generate_gyroid_3d(
    params: Dict[str, Any],
    grid_config: Dict[str, Any],
    height_mm: float = 2.0,
    resolution: int = 100
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Generate 3D gyroid TPMS geometry.
    
    Uses gyroid implicit surface equation:
    sin(x)cos(y) + sin(y)cos(z) + sin(z)cos(x) = threshold
    
    Args:
        params: Parameters dict (must have 'threshold', 'wavelength_px')
        grid_config: Grid configuration
        height_mm: Height in mm
        resolution: Grid resolution
        
    Returns:
        3D binary volume (nz, ny, nx) where 1=fluid, 0=solid
        Metadata dictionary
    """
    nx = ny = nz = resolution
    
    # Get parameters
    threshold = params.get('threshold', 0.0)
    wavelength_px = params.get('wavelength_px', 20.0)
    
    # Create coordinate grids
    x = np.linspace(0, 2*np.pi*nx/wavelength_px, nx)
    y = np.linspace(0, 2*np.pi*ny/wavelength_px, ny)
    z = np.linspace(0, 2*np.pi*nz/wavelength_px, nz)
    
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    # Gyroid equation
    field = np.sin(X)*np.cos(Y) + np.sin(Y)*np.cos(Z) + np.sin(Z)*np.cos(X)
    
    # Threshold to binary (1=fluid, 0=solid)
    volume = (field > threshold).astype(np.uint8)
    
    # Transpose to (nz, ny, nx) format
    volume = np.transpose(volume, (2, 1, 0))
    
    metadata = {
        'type': '3d_gyroid_tpms',
        'threshold': threshold,
        'wavelength_px': wavelength_px,
        'porosity': float(np.mean(volume)),
        'height_mm': height_mm,
        'resolution': resolution,
        'dimensions': {'nx': nx, 'ny': ny, 'nz': nz}
    }
    
    return volume, metadata


def generate_diamond_3d(
    params: Dict[str, Any],
    grid_config: Dict[str, Any],
    height_mm: float = 2.0,
    resolution: int = 100
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Generate 3D diamond (Schwarz-D) TPMS geometry.
    
    Uses diamond implicit surface equation:
    sin(x)sin(y)sin(z) + sin(x)cos(y)cos(z) + 
    cos(x)sin(y)cos(z) + cos(x)cos(y)sin(z) = threshold
    
    Args:
        params: Parameters dict (must have 'threshold', 'wavelength_px')
        grid_config: Grid configuration
        height_mm: Height in mm
        resolution: Grid resolution
        
    Returns:
        3D binary volume (nz, ny, nx) where 1=fluid, 0=solid
        Metadata dictionary
    """
    nx = ny = nz = resolution
    
    # Get parameters
    threshold = params.get('threshold', 0.0)
    wavelength_px = params.get('wavelength_px', 20.0)
    
    # Create coordinate grids
    x = np.linspace(0, 2*np.pi*nx/wavelength_px, nx)
    y = np.linspace(0, 2*np.pi*ny/wavelength_px, ny)
    z = np.linspace(0, 2*np.pi*nz/wavelength_px, nz)
    
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    # Diamond (Schwarz-D) equation
    field = (np.sin(X)*np.sin(Y)*np.sin(Z) + 
             np.sin(X)*np.cos(Y)*np.cos(Z) + 
             np.cos(X)*np.sin(Y)*np.cos(Z) + 
             np.cos(X)*np.cos(Y)*np.sin(Z))
    
    # Threshold to binary (1=fluid, 0=solid)
    volume = (field > threshold).astype(np.uint8)
    
    # Transpose to (nz, ny, nx) format
    volume = np.transpose(volume, (2, 1, 0))
    
    metadata = {
        'type': '3d_diamond_tpms',
        'threshold': threshold,
        'wavelength_px': wavelength_px,
        'porosity': float(np.mean(volume)),
        'height_mm': height_mm,
        'resolution': resolution,
        'dimensions': {'nx': nx, 'ny': ny, 'nz': nz}
    }
    
    return volume, metadata


def generate_primitive_3d(
    params: Dict[str, Any],
    grid_config: Dict[str, Any],
    height_mm: float = 2.0,
    resolution: int = 100
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Generate 3D primitive (Schwarz-P) TPMS geometry.
    
    Uses primitive implicit surface equation:
    cos(x) + cos(y) + cos(z) = threshold
    
    Args:
        params: Parameters dict (must have 'threshold', 'wavelength_px')
        grid_config: Grid configuration
        height_mm: Height in mm
        resolution: Grid resolution
        
    Returns:
        3D binary volume (nz, ny, nx) where 1=fluid, 0=solid
        Metadata dictionary
    """
    nx = ny = nz = resolution
    
    # Get parameters
    threshold = params.get('threshold', 0.0)
    wavelength_px = params.get('wavelength_px', 20.0)
    
    # Create coordinate grids
    x = np.linspace(0, 2*np.pi*nx/wavelength_px, nx)
    y = np.linspace(0, 2*np.pi*ny/wavelength_px, ny)
    z = np.linspace(0, 2*np.pi*nz/wavelength_px, nz)
    
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    # Primitive (Schwarz-P) equation
    field = np.cos(X) + np.cos(Y) + np.cos(Z)
    
    # Threshold to binary (1=fluid, 0=solid)
    volume = (field > threshold).astype(np.uint8)
    
    # Transpose to (nz, ny, nx) format
    volume = np.transpose(volume, (2, 1, 0))
    
    metadata = {
        'type': '3d_primitive_tpms',
        'threshold': threshold,
        'wavelength_px': wavelength_px,
        'porosity': float(np.mean(volume)),
        'height_mm': height_mm,
        'resolution': resolution,
        'dimensions': {'nx': nx, 'ny': ny, 'nz': nz}
    }
    
    return volume, metadata
