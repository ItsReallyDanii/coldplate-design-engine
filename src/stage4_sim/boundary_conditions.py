"""
Boundary conditions for Stage 4 flow simulation.
"""

import numpy as np
from typing import Dict, Any, Tuple


def apply_pressure_boundary_conditions(
    shape: Tuple[int, int, int],
    inlet_pressure_pa: float = 101325.0 + 1000.0,  # 1 kPa above ambient
    outlet_pressure_pa: float = 101325.0  # Ambient
) -> Dict[str, Any]:
    """
    Setup pressure boundary conditions for flow simulation.
    
    Uses Dirichlet boundary conditions:
    - Inlet (z=0): Fixed pressure at inlet_pressure_pa
    - Outlet (z=-1): Fixed pressure at outlet_pressure_pa
    - Walls (x, y boundaries): Zero gradient (Neumann)
    
    Args:
        shape: Grid dimensions (nx, ny, nz)
        inlet_pressure_pa: Inlet pressure in Pa
        outlet_pressure_pa: Outlet pressure in Pa
        
    Returns:
        Dictionary with boundary condition information
    """
    return {
        'inlet_pressure_pa': inlet_pressure_pa,
        'outlet_pressure_pa': outlet_pressure_pa,
        'pressure_drop_pa': inlet_pressure_pa - outlet_pressure_pa,
        'bc_type': 'dirichlet_inlet_outlet',
        'wall_bc': 'zero_gradient'
    }


def get_matched_boundary_conditions() -> Dict[str, Any]:
    """
    Get matched boundary conditions for fair comparison across candidates.
    
    All candidates are simulated with:
    - Same inlet/outlet pressure drop
    - Same fluid properties
    - Same domain orientation
    
    Returns:
        Dictionary with matched boundary conditions
    """
    return {
        'inlet_pressure_pa': 101325.0 + 1000.0,  # 1 kPa pressure drop
        'outlet_pressure_pa': 101325.0,
        'pressure_drop_pa': 1000.0,
        'fluid_density_kg_m3': 1000.0,  # Water
        'fluid_viscosity_pa_s': 0.001,  # Water at 20°C
        'flow_direction': 'z',  # Flow in z-direction
        'matched_conditions': True
    }
