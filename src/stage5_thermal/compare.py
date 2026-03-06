"""
Comparison framework for Stage 5 thermal validation.

Compares candidates under matched thermal boundary conditions.
"""

import numpy as np
from typing import Dict, List, Any


def verify_matched_thermal_conditions(
    results: List[Dict[str, Any]]
) -> bool:
    """
    Verify all candidates use matched thermal boundary conditions.
    
    Args:
        results: List of candidate result dictionaries
        
    Returns:
        True if all conditions match
    """
    if len(results) < 2:
        return True
    
    from . import boundary_conditions
    
    # Extract BCs from first candidate
    bc_ref = results[0].get('boundary_conditions', {})
    
    # Check all others match
    for result in results[1:]:
        bc = result.get('boundary_conditions', {})
        if not boundary_conditions.verify_matched_thermal_conditions(bc_ref, bc):
            return False
    
    return True


def rank_candidates_by_thermal_performance(
    results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Rank candidates by thermal performance.
    
    Primary metric: Thermal resistance (lower is better)
    Secondary metric: Peak temperature (lower is better)
    
    Args:
        results: List of candidate result dictionaries
        
    Returns:
        Sorted list (best to worst)
    """
    def get_thermal_resistance(result):
        metrics = result.get('metrics', {})
        thermal_sim = metrics.get('thermal_simulated_quantities', {})
        R_th_dict = thermal_sim.get('thermal_resistance', {})
        return R_th_dict.get('thermal_resistance_k_w', float('inf'))
    
    def get_peak_temperature(result):
        metrics = result.get('metrics', {})
        thermal_sim = metrics.get('thermal_simulated_quantities', {})
        temp_stats = thermal_sim.get('temperature_statistics', {})
        return temp_stats.get('T_max_c', float('inf'))
    
    # Sort by thermal resistance, then by peak temperature
    sorted_results = sorted(
        results,
        key=lambda r: (get_thermal_resistance(r), get_peak_temperature(r))
    )
    
    return sorted_results


def compute_comparison_metrics(
    results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Compute comparison metrics across candidates.
    
    Args:
        results: List of candidate result dictionaries
        
    Returns:
        Comparison metrics dictionary
    """
    if not results:
        return {}
    
    # Extract thermal resistances
    R_th_list = []
    T_max_list = []
    candidate_ids = []
    
    for result in results:
        candidate_ids.append(result['candidate_id'])
        
        metrics = result.get('metrics', {})
        thermal_sim = metrics.get('thermal_simulated_quantities', {})
        
        R_th_dict = thermal_sim.get('thermal_resistance', {})
        R_th_list.append(R_th_dict.get('thermal_resistance_k_w', float('inf')))
        
        temp_stats = thermal_sim.get('temperature_statistics', {})
        T_max_list.append(temp_stats.get('T_max_c', float('inf')))
    
    R_th_arr = np.array(R_th_list)
    T_max_arr = np.array(T_max_list)
    
    # Compute statistics
    comparison = {
        'n_candidates': len(results),
        'candidate_ids': candidate_ids,
        'thermal_resistance': {
            'values_k_w': R_th_list,
            'best_k_w': float(np.min(R_th_arr)),
            'worst_k_w': float(np.max(R_th_arr)),
            'mean_k_w': float(np.mean(R_th_arr)),
            'std_k_w': float(np.std(R_th_arr)),
            'range_k_w': float(np.max(R_th_arr) - np.min(R_th_arr)),
            'best_candidate': candidate_ids[int(np.argmin(R_th_arr))]
        },
        'peak_temperature': {
            'values_c': T_max_list,
            'lowest_c': float(np.min(T_max_arr)),
            'highest_c': float(np.max(T_max_arr)),
            'mean_c': float(np.mean(T_max_arr)),
            'std_c': float(np.std(T_max_arr)),
            'range_c': float(np.max(T_max_arr) - np.min(T_max_arr)),
            'best_candidate': candidate_ids[int(np.argmin(T_max_arr))]
        }
    }
    
    return comparison


def generate_comparison_summary(
    results: List[Dict[str, Any]],
    comparison: Dict[str, Any]
) -> str:
    """
    Generate human-readable comparison summary.
    
    Args:
        results: List of candidate result dictionaries
        comparison: Comparison metrics
        
    Returns:
        Markdown-formatted summary string
    """
    lines = []
    lines.append("# Stage 5 Thermal Validation Comparison\n")
    lines.append(f"**Candidates evaluated:** {comparison['n_candidates']}\n")
    lines.append("")
    
    # Thermal resistance summary
    R_th = comparison['thermal_resistance']
    lines.append("## Thermal Resistance (lower is better)\n")
    lines.append(f"- **Best:** {R_th['best_k_w']:.6f} K/W ({R_th['best_candidate']})")
    lines.append(f"- **Worst:** {R_th['worst_k_w']:.6f} K/W")
    lines.append(f"- **Mean:** {R_th['mean_k_w']:.6f} K/W")
    lines.append(f"- **Range:** {R_th['range_k_w']:.6f} K/W")
    lines.append("")
    
    # Peak temperature summary
    T_max = comparison['peak_temperature']
    lines.append("## Peak Temperature (lower is better)\n")
    lines.append(f"- **Lowest:** {T_max['lowest_c']:.2f} °C ({T_max['best_candidate']})")
    lines.append(f"- **Highest:** {T_max['highest_c']:.2f} °C")
    lines.append(f"- **Mean:** {T_max['mean_c']:.2f} °C")
    lines.append(f"- **Range:** {T_max['range_c']:.2f} °C")
    lines.append("")
    
    # Ranking table
    ranked = rank_candidates_by_thermal_performance(results)
    lines.append("## Thermal Performance Ranking\n")
    lines.append("| Rank | Candidate | R_th (K/W) | T_max (°C) | T_mean (°C) |")
    lines.append("|------|-----------|------------|------------|-------------|")
    
    for i, result in enumerate(ranked, 1):
        cand_id = result['candidate_id']
        metrics = result['metrics']
        thermal_sim = metrics['thermal_simulated_quantities']
        
        R_th_val = thermal_sim['thermal_resistance']['thermal_resistance_k_w']
        T_max_val = thermal_sim['temperature_statistics']['T_max_c']
        T_mean_val = thermal_sim['temperature_statistics']['T_mean_c']
        
        lines.append(f"| {i} | {cand_id} | {R_th_val:.6f} | {T_max_val:.2f} | {T_mean_val:.2f} |")
    
    lines.append("")
    lines.append("## Quantity Labeling\n")
    lines.append("- **SIMULATED**: Thermal quantities from Stage 5 thermal solver")
    lines.append("- **FLOW_SIMULATED**: Flow quantities from Stage 4 flow solver")
    lines.append("- **GEOMETRIC**: Geometric quantities from Stage 3 geometry")
    lines.append("")
    
    return "\n".join(lines)
