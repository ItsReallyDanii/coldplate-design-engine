"""
Metrics computation for Stage 6 structural screening.

Computes and aggregates all structural and manufacturability metrics
with HONEST labeling.
"""

import numpy as np
from typing import Dict, Any


def compute_all_structural_metrics(
    candidate_data: Dict[str, Any],
    structural_results: Dict[str, Any],
    manufacturability_results: Dict[str, Any],
    material: Dict[str, Any],
    volume: np.ndarray
) -> Dict[str, Any]:
    """
    Compute all structural metrics for a candidate.
    
    Aggregates results from structural screening and manufacturability
    checks into a single metrics dictionary with proper labeling.
    
    Args:
        candidate_data: Candidate data from Stage 5
        structural_results: Structural screening results
        manufacturability_results: Manufacturability check results
        material: Material properties
        volume: Geometry volume array
        
    Returns:
        Complete metrics dictionary
    """
    candidate_id = candidate_data['candidate_id']
    metrics_stage5 = candidate_data['metrics']
    provenance = candidate_data['provenance']
    
    # Extract Stage 5 performance data (carry forward with proper labels)
    thermal_metrics = metrics_stage5.get('thermal_simulated_quantities', {})
    flow_metrics = metrics_stage5.get('flow_simulated_quantities', {})
    geometric_metrics = metrics_stage5.get('geometric_quantities', {})
    
    # Structural screening results (STRUCTURAL_SCREENED)
    structural_screened = {
        'pressure_stress': structural_results['pressure_stress'],
        'thermal_stress': structural_results['thermal_stress'],
        'deflection': structural_results['deflection'],
        'combined_stress': structural_results['combined_stress'],
        'overall_structural_pass': structural_results['overall_pass'],
        'structural_failure_modes': structural_results['failure_modes'],
        'label': 'STRUCTURAL_SCREENED',
        'method': 'analytical_structural_screening'
    }
    
    # Manufacturability results (MANUFACTURABILITY_SCREENED)
    manufacturability_screened = {
        'wall_thickness': manufacturability_results['wall_thickness'],
        'feature_size': manufacturability_results['feature_size'],
        'unsupported_regions': manufacturability_results['unsupported_regions'],
        'trapped_volumes': manufacturability_results['trapped_volumes'],
        'overall_manufacturability_pass': manufacturability_results['overall_pass'],
        'manufacturability_failure_modes': manufacturability_results['failure_modes'],
        'label': 'MANUFACTURABILITY_SCREENED',
        'method': 'geometry_based_manufacturability_screening'
    }
    
    # Material properties (LITERATURE)
    material_info = {
        'material_name': material['name'],
        'E_gpa': material['E_gpa'],
        'yield_strength_mpa': material['yield_strength_mpa'],
        'allowable_stress_mpa': material['allowable_stress_mpa'],
        'safety_factor': material['safety_factor'],
        'label': 'LITERATURE',
        'source': material['source']
    }
    
    # Overall Stage 6 verdict
    overall_pass = (
        structural_results['overall_pass'] and
        manufacturability_results['overall_pass']
    )
    
    all_failure_modes = (
        structural_results['failure_modes'] +
        manufacturability_results['failure_modes']
    )
    
    stage6_verdict = {
        'overall_pass': overall_pass,
        'structural_pass': structural_results['overall_pass'],
        'manufacturability_pass': manufacturability_results['overall_pass'],
        'all_failure_modes': all_failure_modes,
        'screening_level': 'PRELIMINARY',
        'note': 'Screening-level analysis only; full FEA and fabrication validation required before production'
    }
    
    # Assemble complete metrics
    return {
        'candidate_id': candidate_id,
        
        # Stage 6 new quantities
        'structural_screened_quantities': structural_screened,
        'manufacturability_screened_quantities': manufacturability_screened,
        'material_properties': material_info,
        'stage6_verdict': stage6_verdict,
        
        # Carried forward from Stage 5 (with original labels)
        'thermal_simulated_quantities': thermal_metrics,
        'flow_simulated_quantities': flow_metrics,
        'geometric_quantities': geometric_metrics,
        
        # Provenance
        'provenance_summary': {
            'stage5_source': candidate_id,
            'thermal_converged': provenance.get('thermal_simulation', {}).get('converged', False),
            'flow_converged': provenance.get('stage4_source', {}).get('flow_converged', False)
        }
    }


def extract_summary_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract key summary metrics for comparison table.
    
    Args:
        metrics: Full metrics dictionary
        
    Returns:
        Summary metrics dictionary
    """
    structural = metrics['structural_screened_quantities']
    manufacturability = metrics['manufacturability_screened_quantities']
    
    return {
        'candidate_id': metrics['candidate_id'],
        
        # Structural
        'sigma_pressure_mpa': structural['pressure_stress']['sigma_max_mpa'],
        'sigma_thermal_mpa': structural['thermal_stress']['sigma_thermal_effective_mpa'],
        'sigma_combined_mpa': structural['combined_stress']['sigma_combined_mpa'],
        'combined_margin': structural['combined_stress']['margin_of_safety'],
        'deflection_mm': structural['deflection']['deflection_mm'],
        'structural_pass': structural['overall_structural_pass'],
        
        # Manufacturability
        'min_wall_thickness_mm': manufacturability['wall_thickness']['min_wall_thickness_mm'],
        'min_channel_diameter_mm': manufacturability['feature_size']['min_channel_diameter_mm'],
        'manufacturability_pass': manufacturability['overall_manufacturability_pass'],
        
        # Overall
        'overall_pass': metrics['stage6_verdict']['overall_pass'],
        'failure_modes': metrics['stage6_verdict']['all_failure_modes'],
        
        # Performance (from Stage 5)
        'thermal_resistance_k_w': metrics['thermal_simulated_quantities']['thermal_resistance']['thermal_resistance_k_w'],
        'T_max_c': metrics['thermal_simulated_quantities']['temperature_statistics']['T_max_c'],
        'pressure_drop_pa': metrics['flow_simulated_quantities']['pressure_drop']['pressure_drop_pa']
    }
