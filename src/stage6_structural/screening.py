"""
Structural screening for Stage 6.

Implements SIMPLIFIED structural analysis using analytical approximations
and reduced-order methods. This is NOT full FEA, but provides screening-level
estimates to identify obvious mechanical failures.
"""

import numpy as np
from typing import Dict, Any


def estimate_pressure_stress(
    pressure_pa: float,
    geometry_info: Dict[str, Any],
    material: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Estimate stress from internal pressure loading.
    
    LABEL: ANALYTICAL (simplified stress estimate)
    
    Uses simplified thin-wall pressure vessel theory as an UPPER BOUND
    for screening purposes. This is CONSERVATIVE.
    
    σ_hoop ≈ p * r / t  (for thin-walled cylinder/sphere)
    
    For TPMS structures, we approximate using:
    - Effective radius from domain size
    - Effective thickness from wall thickness
    
    Args:
        pressure_pa: Internal pressure (Pa)
        geometry_info: Geometry metadata
        material: Material properties
        
    Returns:
        Pressure stress estimate
    """
    # Extract geometry info
    domain_mm = geometry_info.get('domain_size_mm', [5.0, 5.0, 5.0])
    wall_thickness_mm = geometry_info.get('min_wall_thickness_mm', 0.5)
    
    # Characteristic dimension (effective radius)
    r_eff_mm = np.mean(domain_mm) / 2.0
    t_mm = max(wall_thickness_mm, 0.1)  # Avoid division by zero
    
    # Convert to meters
    r_m = r_eff_mm / 1000.0
    t_m = t_mm / 1000.0
    
    # Thin-wall hoop stress (UPPER BOUND)
    # For TPMS, this is very conservative as structure is cellular
    sigma_hoop_pa = pressure_pa * r_m / t_m
    sigma_hoop_mpa = sigma_hoop_pa / 1e6
    
    # Stress concentration factor for cellular structures (simplified)
    # TPMS structures have lower stress concentration than holes
    # Use factor of 2 as reasonable estimate
    k_t = 2.0
    sigma_max_mpa = k_t * sigma_hoop_mpa
    
    # Check against allowable
    allowable_mpa = material.get('allowable_stress_mpa', 90.0)
    passes = sigma_max_mpa < allowable_mpa
    margin = (allowable_mpa / sigma_max_mpa - 1.0) if sigma_max_mpa > 0 else float('inf')
    
    return {
        'sigma_nominal_mpa': float(sigma_hoop_mpa),
        'sigma_max_mpa': float(sigma_max_mpa),
        'stress_concentration_factor': k_t,
        'allowable_stress_mpa': allowable_mpa,
        'margin_of_safety': float(margin),
        'passes': bool(passes),
        'failure_mode': None if passes else 'pressure_overstress',
        'label': 'ANALYTICAL',
        'method': 'thin_wall_pressure_vessel_approximation',
        'note': 'Conservative upper bound for screening'
    }


def estimate_thermal_stress(
    delta_T_c: float,
    geometry_info: Dict[str, Any],
    material: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Estimate stress from thermal expansion.
    
    LABEL: ANALYTICAL (simplified stress estimate)
    
    Uses simplified thermal stress theory:
    σ_thermal = E * α * ΔT / (1 - ν)  (for fully constrained expansion)
    
    This is an UPPER BOUND assuming full constraint.
    
    Args:
        delta_T_c: Temperature difference (°C)
        geometry_info: Geometry metadata
        material: Material properties
        
    Returns:
        Thermal stress estimate
    """
    # Material properties
    E_gpa = material.get('E_gpa', 68.9)
    alpha_1_k = material.get('alpha_1_k', 23.6e-6)
    nu = material.get('nu', 0.33)
    
    # Convert to consistent units
    E_mpa = E_gpa * 1000.0
    
    # Thermal stress coefficient
    # Assumes plane strain condition (conservative)
    coeff = E_mpa * alpha_1_k / (1.0 - nu)
    
    # Thermal stress (UPPER BOUND for full constraint)
    sigma_thermal_mpa = coeff * delta_T_c
    
    # For TPMS structures, constraint is NOT full
    # Apply reduction factor (engineering judgment)
    # Cellular structures can accommodate thermal expansion
    constraint_factor = 0.5  # Reduced constraint for cellular structure
    sigma_effective_mpa = constraint_factor * sigma_thermal_mpa
    
    # Check against allowable
    allowable_mpa = material.get('allowable_stress_mpa', 90.0)
    passes = sigma_effective_mpa < allowable_mpa
    margin = (allowable_mpa / sigma_effective_mpa - 1.0) if sigma_effective_mpa > 0 else float('inf')
    
    return {
        'sigma_thermal_unconstrained_mpa': float(sigma_thermal_mpa),
        'sigma_thermal_effective_mpa': float(sigma_effective_mpa),
        'constraint_factor': constraint_factor,
        'delta_T_c': delta_T_c,
        'allowable_stress_mpa': allowable_mpa,
        'margin_of_safety': float(margin),
        'passes': bool(passes),
        'failure_mode': None if passes else 'thermal_overstress',
        'label': 'ANALYTICAL',
        'method': 'thermal_expansion_stress_approximation',
        'note': 'Reduced constraint factor for cellular structure'
    }


def estimate_deflection(
    pressure_pa: float,
    geometry_info: Dict[str, Any],
    material: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Estimate deflection from pressure loading.
    
    LABEL: ANALYTICAL (simplified deflection estimate)
    
    Uses simplified plate bending theory as screening estimate:
    δ ≈ (p * L^4) / (E * t^3)  (for simply supported plate)
    
    Args:
        pressure_pa: Internal pressure (Pa)
        geometry_info: Geometry metadata
        material: Material properties
        
    Returns:
        Deflection estimate
    """
    # Extract geometry info
    domain_mm = geometry_info.get('domain_size_mm', [5.0, 5.0, 5.0])
    wall_thickness_mm = geometry_info.get('min_wall_thickness_mm', 0.5)
    
    # Characteristic length (span)
    L_mm = max(domain_mm)
    t_mm = max(wall_thickness_mm, 0.1)
    
    # Convert to meters
    L_m = L_mm / 1000.0
    t_m = t_mm / 1000.0
    
    # Material properties
    E_gpa = material.get('E_gpa', 68.9)
    E_pa = E_gpa * 1e9
    
    # Simplified deflection (plate bending)
    # For cellular structures, this is very conservative
    # Use coefficient for simply supported plate
    C = 0.0026  # Coefficient for rectangular plate
    delta_m = C * pressure_pa * (L_m ** 4) / (E_pa * (t_m ** 3))
    delta_mm = delta_m * 1000.0
    
    # Allowable deflection (typically L/360 for serviceability)
    allowable_delta_mm = L_mm / 360.0
    
    passes = delta_mm < allowable_delta_mm
    margin = (allowable_delta_mm / delta_mm - 1.0) if delta_mm > 0 else float('inf')
    
    return {
        'deflection_mm': float(delta_mm),
        'allowable_deflection_mm': float(allowable_delta_mm),
        'deflection_to_span_ratio': float(delta_mm / L_mm) if L_mm > 0 else 0.0,
        'margin_of_safety': float(margin),
        'passes': bool(passes),
        'failure_mode': None if passes else 'excessive_deflection',
        'label': 'ANALYTICAL',
        'method': 'plate_bending_approximation',
        'note': 'Conservative estimate for screening'
    }


def run_structural_screening(
    pressure_load: Dict[str, Any],
    thermal_load: Dict[str, Any],
    geometry_info: Dict[str, Any],
    material: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Run complete structural screening analysis.
    
    Combines pressure and thermal load effects using simplified
    superposition. This is SCREENING-LEVEL only.
    
    Args:
        pressure_load: Pressure load case
        thermal_load: Thermal load case
        geometry_info: Geometry metadata
        material: Material properties
        
    Returns:
        Structural screening results
    """
    # Pressure stress
    pressure_stress = estimate_pressure_stress(
        pressure_load['pressure_pa'],
        geometry_info,
        material
    )
    
    # Thermal stress
    thermal_stress = estimate_thermal_stress(
        thermal_load['delta_T_c'],
        geometry_info,
        material
    )
    
    # Deflection (from pressure only, thermal deflection typically small)
    deflection = estimate_deflection(
        pressure_load['pressure_pa'],
        geometry_info,
        material
    )
    
    # Combined stress (simple addition - CONSERVATIVE)
    sigma_combined_mpa = (
        pressure_stress['sigma_max_mpa'] +
        thermal_stress['sigma_thermal_effective_mpa']
    )
    
    allowable_mpa = material.get('allowable_stress_mpa', 90.0)
    combined_passes = sigma_combined_mpa < allowable_mpa
    combined_margin = (allowable_mpa / sigma_combined_mpa - 1.0) if sigma_combined_mpa > 0 else float('inf')
    
    # Overall pass/fail
    all_checks = [
        pressure_stress['passes'],
        thermal_stress['passes'],
        deflection['passes'],
        combined_passes
    ]
    overall_pass = all(all_checks)
    
    # Collect failure modes
    failure_modes = []
    if not pressure_stress['passes']:
        failure_modes.append('pressure_overstress')
    if not thermal_stress['passes']:
        failure_modes.append('thermal_overstress')
    if not deflection['passes']:
        failure_modes.append('excessive_deflection')
    if not combined_passes:
        failure_modes.append('combined_overstress')
    
    return {
        'pressure_stress': pressure_stress,
        'thermal_stress': thermal_stress,
        'deflection': deflection,
        'combined_stress': {
            'sigma_combined_mpa': float(sigma_combined_mpa),
            'allowable_stress_mpa': allowable_mpa,
            'margin_of_safety': float(combined_margin),
            'passes': bool(combined_passes),
            'label': 'ANALYTICAL',
            'method': 'linear_superposition'
        },
        'overall_pass': overall_pass,
        'failure_modes': failure_modes,
        'label': 'STRUCTURAL_SCREENED',
        'note': 'Screening-level analysis only; not certified structural validation'
    }
