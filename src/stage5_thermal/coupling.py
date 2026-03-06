"""
Flow-thermal coupling for Stage 5.

Couples Stage 4 flow field with thermal solver through convective heat transfer.
"""

import numpy as np
from typing import Dict, Any, Optional
from . import boundary_conditions as bc_module


def prepare_thermal_conductivity_field(
    volume: np.ndarray,
    k_solid: float,
    k_fluid: float
) -> np.ndarray:
    """
    Prepare thermal conductivity field from geometry.
    
    Args:
        volume: Boolean array (True=fluid, False=solid)
        k_solid: Solid thermal conductivity (W/m·K)
        k_fluid: Fluid thermal conductivity (W/m·K)
        
    Returns:
        Thermal conductivity field (W/m·K)
    """
    # Ensure volume is boolean
    volume = volume.astype(bool)
    k = np.where(volume, k_fluid, k_solid)
    return k


def compute_convective_field(
    velocity: Dict[str, np.ndarray],
    volume: np.ndarray,
    voxel_size_mm: float,
    boundary_conditions: Dict[str, Any]
) -> np.ndarray:
    """
    Compute convective heat transfer coefficient field from velocity.
    
    Uses Stage 4 velocity field to estimate local convective coefficients.
    
    Args:
        velocity: Velocity field dict (vx, vy, vz)
        volume: Boolean array (True=fluid, False=solid)
        voxel_size_mm: Physical voxel size in mm
        boundary_conditions: BC dictionary with fluid properties
        
    Returns:
        Convective coefficient field (W/m²·K)
    """
    # Ensure volume is boolean
    volume = volume.astype(bool)
    
    # Compute velocity magnitude
    vx = velocity['vx']
    vy = velocity['vy']
    vz = velocity['vz']
    
    v_mag = np.sqrt(vx**2 + vy**2 + vz**2)
    
    # Length scale in meters
    length_scale_m = voxel_size_mm / 1000.0
    
    # Get fluid properties
    fluid_props = {
        'rho_fluid_kg_m3': boundary_conditions.get('rho_fluid_kg_m3', 1000.0),
        'mu_fluid_pa_s': boundary_conditions.get('mu_fluid_pa_s', 0.001),
        'cp_fluid_j_kg_k': boundary_conditions.get('cp_fluid_j_kg_k', 4180.0),
        'k_fluid_w_m_k': boundary_conditions.get('k_fluid_w_m_k', 0.6)
    }
    
    # Vectorized convective coefficient estimation
    h_field = np.zeros_like(v_mag)
    
    for i in range(v_mag.shape[0]):
        for j in range(v_mag.shape[1]):
            for k in range(v_mag.shape[2]):
                if volume[i, j, k]:  # Fluid region
                    h_field[i, j, k] = bc_module.estimate_convective_coefficient(
                        v_mag[i, j, k],
                        fluid_props,
                        length_scale_m
                    )
    
    return h_field


def run_coupled_thermal_simulation(
    candidate: Dict[str, Any],
    boundary_conditions: Dict[str, Any],
    solver_params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Run coupled flow-thermal simulation for a candidate.
    
    Uses Stage 4 flow results to inform thermal simulation.
    
    Args:
        candidate: Candidate dictionary from load_cases
        boundary_conditions: Thermal BC dictionary
        solver_params: Solver parameters
        
    Returns:
        Dictionary with thermal results
    """
    from . import solver as thermal_solver
    
    if solver_params is None:
        solver_params = {}
    
    # Extract data
    volume = candidate['geometry']
    velocity = candidate['velocity']
    voxel_size_mm = candidate['grid_info']['voxel_size_mm']
    
    # Prepare thermal conductivity field
    k_solid = boundary_conditions.get('k_solid_w_m_k', 200.0)
    k_fluid = boundary_conditions.get('k_fluid_w_m_k', 0.6)
    
    k_field = prepare_thermal_conductivity_field(volume, k_solid, k_fluid)
    
    # Compute convective coefficient field from velocity
    h_field = None
    if boundary_conditions.get('use_flow_informed_h', True):
        h_field = compute_convective_field(
            velocity, volume, voxel_size_mm, boundary_conditions
        )
    
    # Solve thermal field
    thermal_result = thermal_solver.solve_thermal_field(
        volume,
        k_field,
        voxel_size_mm,
        boundary_conditions,
        h_field,
        solver_params
    )
    
    return thermal_result
