"""
Thermal metrics computation for Stage 5.

Computes and labels thermal performance metrics HONESTLY.
"""

import numpy as np
from typing import Dict, Any


def compute_temperature_statistics(
    temperature: np.ndarray,
    volume: np.ndarray
) -> Dict[str, Any]:
    """
    Compute temperature field statistics.
    
    LABEL: SIMULATED (from thermal solver)
    
    Args:
        temperature: Temperature field (°C)
        volume: Boolean array (True=fluid, False=solid)
        
    Returns:
        Dictionary with temperature statistics
    """
    # Ensure volume is boolean
    volume = volume.astype(bool)
    
    # Overall statistics
    T_mean = np.mean(temperature)
    T_max = np.max(temperature)
    T_min = np.min(temperature)
    T_std = np.std(temperature)
    
    # Solid region statistics (more relevant for cooling performance)
    if np.any(~volume):
        T_solid_mean = np.mean(temperature[~volume])
        T_solid_max = np.max(temperature[~volume])
        T_solid_min = np.min(temperature[~volume])
    else:
        T_solid_mean = T_mean
        T_solid_max = T_max
        T_solid_min = T_min
    
    # Fluid region statistics
    if np.any(volume):
        T_fluid_mean = np.mean(temperature[volume])
        T_fluid_max = np.max(temperature[volume])
        T_fluid_min = np.min(temperature[volume])
    else:
        T_fluid_mean = T_mean
        T_fluid_max = T_max
        T_fluid_min = T_min
    
    return {
        'T_mean_c': float(T_mean),
        'T_max_c': float(T_max),
        'T_min_c': float(T_min),
        'T_std_c': float(T_std),
        'T_range_c': float(T_max - T_min),
        'T_solid_mean_c': float(T_solid_mean),
        'T_solid_max_c': float(T_solid_max),
        'T_solid_min_c': float(T_solid_min),
        'T_fluid_mean_c': float(T_fluid_mean),
        'T_fluid_max_c': float(T_fluid_max),
        'T_fluid_min_c': float(T_fluid_min),
        'label': 'SIMULATED',
        'method': 'thermal_field_statistics'
    }


def compute_thermal_resistance(
    temperature: np.ndarray,
    volume: np.ndarray,
    voxel_size_mm: float,
    boundary_conditions: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compute effective thermal resistance.
    
    R_th = (T_max - T_inlet) / Q_total
    
    LABEL: SIMULATED (from thermal solver with defined BCs)
    
    Args:
        temperature: Temperature field (°C)
        volume: Boolean array (True=fluid, False=solid)
        voxel_size_mm: Voxel size in mm
        boundary_conditions: BC dictionary
        
    Returns:
        Dictionary with thermal resistance metrics
    """
    T_inlet = boundary_conditions.get('inlet_temperature_c', 25.0)
    heat_flux = boundary_conditions.get('heat_flux_w_m2', 1e6)
    
    # Maximum temperature (typically in solid, near heat source)
    T_max = np.max(temperature)
    
    # Temperature rise
    delta_T = T_max - T_inlet
    
    # Total heat input (assuming heat flux applied to bottom surface)
    # Get surface area from volume shape
    nz, ny, nx = volume.shape  # Note: volume is (nz, ny, nx)
    area_mm2 = nx * ny * (voxel_size_mm ** 2)
    area_m2 = area_mm2 / 1e6
    
    Q_total_w = heat_flux * area_m2
    
    # Thermal resistance (K/W)
    if Q_total_w > 0:
        R_th = delta_T / Q_total_w
    else:
        R_th = float('inf')
    
    return {
        'thermal_resistance_k_w': float(R_th),
        'delta_T_max_c': float(delta_T),
        'heat_input_w': float(Q_total_w),
        'label': 'SIMULATED',
        'method': 'thermal_resistance_calculation'
    }


def compute_temperature_uniformity(
    temperature: np.ndarray,
    volume: np.ndarray
) -> Dict[str, Any]:
    """
    Compute temperature uniformity metrics.
    
    LABEL: SIMULATED (from thermal solver)
    
    Args:
        temperature: Temperature field (°C)
        volume: Boolean array (True=fluid, False=solid)
        
    Returns:
        Dictionary with uniformity metrics
    """
    # Ensure volume is boolean
    volume = volume.astype(bool)
    
    # Focus on solid regions
    if np.any(~volume):
        T_solid = temperature[~volume]
    else:
        T_solid = temperature.flatten()
    
    T_mean = np.mean(T_solid)
    T_std = np.std(T_solid)
    
    # Coefficient of variation
    if T_mean > 0:
        cv = T_std / T_mean
    else:
        cv = 0.0
    
    # Temperature spread
    T_spread = np.max(T_solid) - np.min(T_solid)
    
    return {
        'coefficient_of_variation': float(cv),
        'temperature_spread_c': float(T_spread),
        'label': 'SIMULATED',
        'method': 'temperature_uniformity_analysis'
    }


def compute_all_thermal_metrics(
    thermal_result: Dict[str, Any],
    candidate: Dict[str, Any],
    boundary_conditions: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compute all thermal metrics for a candidate.
    
    Combines SIMULATED thermal quantities with FLOW_SIMULATED (from Stage 4)
    and GEOMETRIC quantities.
    
    Args:
        thermal_result: Result from thermal solver
        candidate: Candidate dictionary
        boundary_conditions: BC dictionary
        
    Returns:
        Comprehensive metrics dictionary with honest labeling
    """
    temperature = thermal_result['temperature']
    volume = candidate['geometry']
    voxel_size_mm = candidate['grid_info']['voxel_size_mm']
    
    # Thermal quantities (SIMULATED)
    temp_stats = compute_temperature_statistics(temperature, volume)
    thermal_res = compute_thermal_resistance(temperature, volume, voxel_size_mm, boundary_conditions)
    uniformity = compute_temperature_uniformity(temperature, volume)
    
    # Carry forward Stage 4 flow quantities (FLOW_SIMULATED)
    stage4_metrics = candidate['metrics']
    flow_simulated = stage4_metrics.get('simulated_quantities', {})
    
    # Carry forward geometric quantities (GEOMETRIC)
    geometric = stage4_metrics.get('geometric_quantities', {})
    
    return {
        'thermal_simulated_quantities': {
            'temperature_statistics': temp_stats,
            'thermal_resistance': thermal_res,
            'uniformity': uniformity
        },
        'flow_simulated_quantities': flow_simulated,
        'geometric_quantities': geometric,
        'solver_info': {
            'thermal_converged': thermal_result.get('converged', False),
            'thermal_solve_time_s': thermal_result.get('solve_time_s', 0.0),
            'thermal_residual': thermal_result.get('residual', float('inf')),
            'flow_converged': candidate.get('solver_info', {}).get('converged', False)
        }
    }
