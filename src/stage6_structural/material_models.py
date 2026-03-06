"""
Material models for structural screening.

Provides simplified material property definitions for aluminum alloys
commonly used in cold plate fabrication.
"""

from typing import Dict, Any


def get_aluminum_6061_properties() -> Dict[str, Any]:
    """
    Get material properties for Aluminum 6061-T6.
    
    This is a STANDARD aluminum alloy commonly used for liquid cooling
    cold plates due to good thermal conductivity, machinability, and
    corrosion resistance.
    
    LABEL: LITERATURE (from materials handbooks)
    
    Returns:
        Material properties dictionary
    """
    return {
        'name': 'Aluminum 6061-T6',
        'description': 'Common cold plate aluminum alloy',
        
        # Mechanical properties at room temperature
        'E_gpa': 68.9,  # Young's modulus (GPa)
        'nu': 0.33,  # Poisson's ratio
        'rho_kg_m3': 2700.0,  # Density (kg/m³)
        'yield_strength_mpa': 276.0,  # Yield strength (MPa)
        'ultimate_strength_mpa': 310.0,  # Ultimate tensile strength (MPa)
        
        # Thermal properties
        'k_w_m_k': 167.0,  # Thermal conductivity (W/m·K)
        'cp_j_kg_k': 896.0,  # Specific heat (J/kg·K)
        'alpha_1_k': 23.6e-6,  # Coefficient of thermal expansion (1/K)
        
        # Screening margins (conservative for prototype screening)
        'safety_factor': 3.0,  # Safety factor for screening
        'allowable_stress_mpa': 276.0 / 3.0,  # Conservative allowable = yield / 3
        
        'label': 'LITERATURE',
        'source': 'ASM_Metals_Handbook',
        'method': 'material_database_lookup'
    }


def get_material_properties(material_name: str = 'aluminum_6061') -> Dict[str, Any]:
    """
    Get material properties by name.
    
    Args:
        material_name: Material identifier
        
    Returns:
        Material properties dictionary
    """
    materials = {
        'aluminum_6061': get_aluminum_6061_properties,
    }
    
    if material_name not in materials:
        raise ValueError(f"Unknown material: {material_name}")
    
    return materials[material_name]()


def compute_thermal_stress_coefficient(material: Dict[str, Any]) -> float:
    """
    Compute thermal stress coefficient for constrained thermal expansion.
    
    For a fully constrained thermal expansion:
    σ_thermal = E * α * ΔT / (1 - ν)
    
    This is an UPPER BOUND assuming full constraint.
    
    LABEL: ANALYTICAL
    
    Args:
        material: Material properties dictionary
        
    Returns:
        Thermal stress coefficient (MPa/K)
    """
    E_gpa = material['E_gpa']
    alpha_1_k = material['alpha_1_k']
    nu = material['nu']
    
    # Convert to consistent units
    E_mpa = E_gpa * 1000.0  # GPa to MPa
    
    # Thermal stress coefficient for plane strain
    # This is CONSERVATIVE (assumes full constraint)
    coeff = E_mpa * alpha_1_k / (1.0 - nu)
    
    return coeff
