"""
Grid setup for Stage 4 voxel-based flow simulation.
"""

import numpy as np
from typing import Dict, Any, Tuple


def setup_simulation_grid(
    volume: np.ndarray,
    voxel_size_mm: float = 0.1
) -> Dict[str, Any]:
    """
    Setup simulation grid from Stage 3 volume data.
    
    Args:
        volume: 3D numpy array (uint8, 1=fluid, 0=solid) from Stage 3
        voxel_size_mm: Physical size of each voxel in mm
        
    Returns:
        Dictionary containing:
        - fluid_mask: Boolean array (True=fluid, False=solid)
        - shape: Grid dimensions (nx, ny, nz)
        - voxel_size_mm: Physical voxel size
        - domain_size_mm: Physical domain dimensions
        - porosity: Volume fraction of fluid
    """
    # Fluid mask (1=fluid in volume array)
    fluid_mask = (volume == 1).astype(bool)
    
    # Grid dimensions
    nx, ny, nz = volume.shape
    
    # Physical domain size
    domain_size_mm = (
        nx * voxel_size_mm,
        ny * voxel_size_mm,
        nz * voxel_size_mm
    )
    
    # Porosity
    porosity = np.sum(fluid_mask) / fluid_mask.size
    
    return {
        'fluid_mask': fluid_mask,
        'shape': (nx, ny, nz),
        'voxel_size_mm': voxel_size_mm,
        'domain_size_mm': domain_size_mm,
        'porosity': porosity
    }


def get_inlet_outlet_faces(shape: Tuple[int, int, int]) -> Dict[str, np.ndarray]:
    """
    Define inlet and outlet faces for flow simulation.
    
    Uses z-direction flow convention:
    - Inlet: z=0 face (bottom)
    - Outlet: z=-1 face (top)
    
    Args:
        shape: Grid dimensions (nx, ny, nz)
        
    Returns:
        Dictionary with inlet_mask and outlet_mask (3D boolean arrays)
    """
    nx, ny, nz = shape
    
    # Initialize masks
    inlet_mask = np.zeros(shape, dtype=bool)
    outlet_mask = np.zeros(shape, dtype=bool)
    
    # Set inlet face (z=0)
    inlet_mask[:, :, 0] = True
    
    # Set outlet face (z=-1)
    outlet_mask[:, :, -1] = True
    
    return {
        'inlet_mask': inlet_mask,
        'outlet_mask': outlet_mask
    }


def compute_permeability_field(
    fluid_mask: np.ndarray,
    k_fluid: float = 1e-6,
    k_solid: float = 1e-12
) -> np.ndarray:
    """
    Compute permeability field for Darcy-like flow resistance.
    
    Args:
        fluid_mask: Boolean array (True=fluid, False=solid)
        k_fluid: Permeability in fluid regions (m^2)
        k_solid: Permeability in solid regions (m^2, very small)
        
    Returns:
        Permeability field (same shape as fluid_mask)
    """
    permeability = np.where(fluid_mask, k_fluid, k_solid)
    return permeability
