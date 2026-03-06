"""
Thermal boundary conditions for Stage 5.

Defines matched thermal boundary conditions for fair candidate comparison.
"""

from typing import Dict, Any


def get_matched_thermal_boundary_conditions() -> Dict[str, Any]:
    """
    Get standard matched thermal boundary conditions for fair comparison.
    
    All candidates must be simulated with these BCs for valid comparison.
    
    Boundary conditions:
    - Heat source: Uniform heat flux applied to bottom surface (chip side)
    - Coolant inlet temperature: Fixed temperature at inlet
    - Adiabatic walls: Side walls assumed adiabatic
    - Outlet: Pressure outlet (zero gradient for temperature)
    
    Returns:
        Dictionary with thermal BC parameters
    """
    return {
        'heat_flux_w_m2': 1e6,  # 1 MW/m² typical for high-performance chips
        'inlet_temperature_c': 25.0,  # 25°C coolant inlet
        'ambient_temperature_c': 25.0,  # Reference temperature
        'wall_bc_type': 'adiabatic',  # Side walls adiabatic
        'bottom_bc_type': 'heat_flux',  # Heat source at bottom
        'top_bc_type': 'adiabatic',  # Top adiabatic
        'outlet_bc_type': 'convective',  # Outlet convective
        
        # Material properties (simplified, uniform)
        'k_solid_w_m_k': 200.0,  # Aluminum thermal conductivity
        'k_fluid_w_m_k': 0.6,  # Water thermal conductivity
        'rho_fluid_kg_m3': 1000.0,  # Water density
        'cp_fluid_j_kg_k': 4180.0,  # Water specific heat
        'mu_fluid_pa_s': 0.001,  # Water viscosity
        
        # Convective heat transfer
        'use_flow_informed_h': True,  # Use Stage 4 velocity for h estimation
        'h_base_w_m2_k': 1000.0,  # Base heat transfer coefficient if flow not available
        
        # Label
        'bc_label': 'MATCHED_THERMAL_BC_V1',
        'description': 'Matched thermal boundary conditions for Stage 5'
    }


def estimate_convective_coefficient(
    velocity_magnitude: float,
    fluid_props: Dict[str, float],
    length_scale_m: float
) -> float:
    """
    Estimate convective heat transfer coefficient from velocity.
    
    Uses simplified correlation: h ~ (k/L) * Re^0.8 * Pr^0.4
    where Re = ρVL/μ, Pr = μcp/k
    
    Args:
        velocity_magnitude: Local velocity magnitude (m/s)
        fluid_props: Fluid properties dict
        length_scale_m: Characteristic length scale (m)
        
    Returns:
        Convective heat transfer coefficient (W/m²·K)
    """
    rho = fluid_props.get('rho_fluid_kg_m3', 1000.0)
    mu = fluid_props.get('mu_fluid_pa_s', 0.001)
    cp = fluid_props.get('cp_fluid_j_kg_k', 4180.0)
    k = fluid_props.get('k_fluid_w_m_k', 0.6)
    
    # Reynolds number
    Re = rho * velocity_magnitude * length_scale_m / mu
    
    # Prandtl number
    Pr = mu * cp / k
    
    # Simplified Nusselt correlation (turbulent flow assumption)
    # Nu = 0.023 * Re^0.8 * Pr^0.4 (Dittus-Boelter correlation)
    if Re < 1.0:
        # Laminar/very low flow - use minimum h
        Nu = 3.66  # Fully developed laminar flow in circular tube
    else:
        Nu = 0.023 * (Re ** 0.8) * (Pr ** 0.4)
    
    # Convective coefficient
    h = Nu * k / length_scale_m
    
    # Clamp to reasonable range
    h_min = 10.0  # W/m²·K minimum
    h_max = 50000.0  # W/m²·K maximum
    h = max(h_min, min(h_max, h))
    
    return h


def verify_matched_thermal_conditions(bc1: Dict[str, Any], bc2: Dict[str, Any]) -> bool:
    """
    Verify that two candidates use matched thermal boundary conditions.
    
    Args:
        bc1: Boundary conditions dict for candidate 1
        bc2: Boundary conditions dict for candidate 2
        
    Returns:
        True if conditions match within tolerance
    """
    # Check critical parameters
    critical_params = [
        'heat_flux_w_m2',
        'inlet_temperature_c',
        'k_solid_w_m_k',
        'k_fluid_w_m_k'
    ]
    
    for param in critical_params:
        val1 = bc1.get(param)
        val2 = bc2.get(param)
        
        if val1 is None or val2 is None:
            return False
        
        # Check relative difference
        if abs(val1 - val2) / max(abs(val1), abs(val2), 1e-10) > 0.01:
            return False
    
    return True
