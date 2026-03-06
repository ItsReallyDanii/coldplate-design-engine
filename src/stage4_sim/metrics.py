"""
Metrics computation for Stage 4 simulation results.

All metrics are HONESTLY LABELED as:
- SIMULATED: Computed from actual flow solver
- GEOMETRIC: Derived from geometry only
- PROXY: Simplified estimate, not validated
"""

import numpy as np
from typing import Dict, Any


def compute_pressure_drop(
    pressure: np.ndarray,
    inlet_mask: np.ndarray,
    outlet_mask: np.ndarray
) -> Dict[str, Any]:
    """
    Compute pressure drop from simulated pressure field.
    
    LABEL: SIMULATED
    
    Args:
        pressure: Pressure field from solver (Pa)
        inlet_mask: Inlet boundary mask
        outlet_mask: Outlet boundary mask
        
    Returns:
        Dictionary with pressure drop metrics
    """
    # Average pressure at inlet and outlet
    p_inlet = np.mean(pressure[inlet_mask])
    p_outlet = np.mean(pressure[outlet_mask])
    
    # Pressure drop
    delta_p = p_inlet - p_outlet
    
    return {
        'pressure_drop_pa': float(delta_p),
        'inlet_pressure_pa': float(p_inlet),
        'outlet_pressure_pa': float(p_outlet),
        'label': 'SIMULATED',
        'method': 'pressure_poisson_solver'
    }


def compute_flow_rate(
    velocity: Dict[str, np.ndarray],
    fluid_mask: np.ndarray,
    outlet_mask: np.ndarray,
    voxel_size_mm: float
) -> Dict[str, Any]:
    """
    Compute volumetric flow rate from velocity field.
    
    LABEL: SIMULATED
    
    Args:
        velocity: Velocity components (vx, vy, vz) from solver
        fluid_mask: Boolean array (True=fluid)
        outlet_mask: Outlet boundary mask
        voxel_size_mm: Physical voxel size in mm
        
    Returns:
        Dictionary with flow rate metrics
    """
    # Convert voxel size to meters
    dx = voxel_size_mm / 1000.0
    dA = dx * dx  # Face area
    
    # Flow rate through outlet (z-direction)
    vz = velocity['vz']
    
    # Mask for outlet fluid cells
    outlet_fluid = outlet_mask & fluid_mask
    
    # Volumetric flow rate (m^3/s)
    Q = np.sum(np.abs(vz[outlet_fluid])) * dA
    
    # Convert to L/min
    Q_lpm = Q * 1000.0 * 60.0
    
    return {
        'flow_rate_m3_s': float(Q),
        'flow_rate_lpm': float(Q_lpm),
        'label': 'SIMULATED',
        'method': 'velocity_integration'
    }


def compute_velocity_statistics(
    velocity: Dict[str, np.ndarray],
    fluid_mask: np.ndarray
) -> Dict[str, Any]:
    """
    Compute velocity field statistics.
    
    LABEL: SIMULATED
    
    Args:
        velocity: Velocity components (vx, vy, vz)
        fluid_mask: Boolean array (True=fluid)
        
    Returns:
        Dictionary with velocity statistics
    """
    vx = velocity['vx'][fluid_mask]
    vy = velocity['vy'][fluid_mask]
    vz = velocity['vz'][fluid_mask]
    
    # Velocity magnitude
    v_mag = np.sqrt(vx**2 + vy**2 + vz**2)
    
    return {
        'v_mean_m_s': float(np.mean(v_mag)),
        'v_max_m_s': float(np.max(v_mag)),
        'v_min_m_s': float(np.min(v_mag)),
        'v_std_m_s': float(np.std(v_mag)),
        'vz_mean_m_s': float(np.mean(vz)),  # Primary flow direction
        'label': 'SIMULATED',
        'method': 'velocity_field_statistics'
    }


def compute_flow_uniformity(
    velocity: Dict[str, np.ndarray],
    fluid_mask: np.ndarray
) -> Dict[str, Any]:
    """
    Compute flow uniformity metrics.
    
    LABEL: SIMULATED
    
    Args:
        velocity: Velocity components (vx, vy, vz)
        fluid_mask: Boolean array (True=fluid)
        
    Returns:
        Dictionary with uniformity metrics
    """
    vz = velocity['vz'][fluid_mask]
    
    # Coefficient of variation (std/mean)
    vz_mean = np.mean(vz)
    vz_std = np.std(vz)
    
    if vz_mean > 0:
        cv = vz_std / vz_mean
    else:
        cv = 999.0  # Invalid flow
    
    # Maldistribution factor (max/min ratio in positive flow regions)
    vz_positive = vz[vz > 0]
    if len(vz_positive) > 0:
        maldist = np.max(vz_positive) / np.mean(vz_positive)
    else:
        maldist = 999.0
    
    return {
        'coefficient_of_variation': float(cv),
        'maldistribution_factor': float(maldist),
        'label': 'SIMULATED',
        'method': 'velocity_distribution_analysis'
    }


def compute_hydraulic_resistance(
    pressure_drop_pa: float,
    flow_rate_m3_s: float
) -> Dict[str, Any]:
    """
    Compute hydraulic resistance from pressure drop and flow rate.
    
    LABEL: SIMULATED
    
    R_h = ΔP / Q
    
    Args:
        pressure_drop_pa: Pressure drop (Pa)
        flow_rate_m3_s: Volumetric flow rate (m^3/s)
        
    Returns:
        Dictionary with hydraulic resistance
    """
    if flow_rate_m3_s > 0:
        R_h = pressure_drop_pa / flow_rate_m3_s
    else:
        R_h = 999999.0  # Very high resistance (blocked)
    
    return {
        'hydraulic_resistance_pa_s_m3': float(R_h),
        'label': 'SIMULATED',
        'method': 'resistance_from_dp_and_q'
    }


def compute_geometric_metrics(
    grid: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compute geometric metrics from grid.
    
    LABEL: GEOMETRIC
    
    Args:
        grid: Grid dictionary from setup_simulation_grid
        
    Returns:
        Dictionary with geometric metrics
    """
    return {
        'porosity': float(grid['porosity']),
        'domain_volume_mm3': float(np.prod(grid['domain_size_mm'])),
        'fluid_volume_mm3': float(grid['porosity'] * np.prod(grid['domain_size_mm'])),
        'label': 'GEOMETRIC',
        'method': 'geometry_analysis'
    }


def compute_all_metrics(
    simulation_result: Dict[str, Any],
    grid: Dict[str, Any],
    boundary_conditions: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compute all metrics from simulation results.
    
    Args:
        simulation_result: Output from run_flow_simulation
        grid: Grid dictionary
        boundary_conditions: BC dictionary
        
    Returns:
        Dictionary with all metrics, each labeled appropriately
    """
    from . import mesh_or_grid
    
    # Get inlet/outlet masks
    faces = mesh_or_grid.get_inlet_outlet_faces(grid['shape'])
    inlet_mask = faces['inlet_mask']
    outlet_mask = faces['outlet_mask']
    
    # Pressure drop (SIMULATED)
    pressure_metrics = compute_pressure_drop(
        simulation_result['pressure'],
        inlet_mask,
        outlet_mask
    )
    
    # Flow rate (SIMULATED)
    flow_metrics = compute_flow_rate(
        simulation_result['velocity'],
        grid['fluid_mask'],
        outlet_mask,
        grid['voxel_size_mm']
    )
    
    # Velocity statistics (SIMULATED)
    velocity_stats = compute_velocity_statistics(
        simulation_result['velocity'],
        grid['fluid_mask']
    )
    
    # Flow uniformity (SIMULATED)
    uniformity = compute_flow_uniformity(
        simulation_result['velocity'],
        grid['fluid_mask']
    )
    
    # Hydraulic resistance (SIMULATED)
    resistance = compute_hydraulic_resistance(
        pressure_metrics['pressure_drop_pa'],
        flow_metrics['flow_rate_m3_s']
    )
    
    # Geometric metrics (GEOMETRIC)
    geometric = compute_geometric_metrics(grid)
    
    # Combine all metrics
    metrics = {
        'simulated_quantities': {
            'pressure_drop': pressure_metrics,
            'flow_rate': flow_metrics,
            'velocity_statistics': velocity_stats,
            'flow_uniformity': uniformity,
            'hydraulic_resistance': resistance
        },
        'geometric_quantities': geometric,
        'proxy_quantities': {
            # Note: We don't compute thermal metrics yet
            # This is explicitly empty to show honesty
            'note': 'Thermal simulation not yet implemented in Stage 4',
            'label': 'NOT_COMPUTED'
        },
        'solver_info': {
            'converged': simulation_result['converged'],
            'iterations': simulation_result['iterations'],
            'solve_time_s': simulation_result['solve_time_s']
        }
    }
    
    return metrics
