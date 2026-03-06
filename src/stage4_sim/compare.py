"""
Fair comparison of Stage 4 simulation results across candidates.

Ensures matched conditions and honest relative ranking.
"""

import numpy as np
from typing import List, Dict, Any


def verify_matched_conditions(
    results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Verify that all candidates were simulated under matched conditions.
    
    Args:
        results: List of simulation result dictionaries
        
    Returns:
        Dictionary with verification status and any mismatches
    """
    if len(results) < 2:
        return {
            'matched': True,
            'note': 'Less than 2 candidates, no comparison needed'
        }
    
    # Check boundary conditions
    bc_keys = ['inlet_pressure_pa', 'outlet_pressure_pa', 'fluid_viscosity_pa_s']
    mismatches = []
    
    for key in bc_keys:
        values = [r['boundary_conditions'].get(key) for r in results]
        if not all(v == values[0] for v in values):
            mismatches.append(key)
    
    # Check grid resolution matching
    voxel_sizes = [r['grid']['voxel_size_mm'] for r in results]
    if not all(v == voxel_sizes[0] for v in voxel_sizes):
        mismatches.append('voxel_size_mm')
    
    return {
        'matched': len(mismatches) == 0,
        'mismatches': mismatches,
        'verification': 'PASS' if len(mismatches) == 0 else 'FAIL'
    }


def rank_candidates_by_metric(
    results: List[Dict[str, Any]],
    metric_path: str,
    lower_is_better: bool = True
) -> List[Dict[str, Any]]:
    """
    Rank candidates by a specific metric.
    
    Args:
        results: List of simulation result dictionaries
        metric_path: Dot-separated path to metric (e.g., 'metrics.simulated_quantities.pressure_drop.pressure_drop_pa')
        lower_is_better: Whether lower values are better (True for pressure drop, False for flow rate)
        
    Returns:
        List of results sorted by metric, best first
    """
    def get_nested_value(d, path):
        keys = path.split('.')
        val = d
        for key in keys:
            val = val[key]
        return val
    
    # Extract metric values
    ranked = []
    for r in results:
        try:
            metric_val = get_nested_value(r, metric_path)
            ranked.append((r, metric_val))
        except (KeyError, TypeError):
            # Metric not available, put at end
            ranked.append((r, float('inf') if lower_is_better else float('-inf')))
    
    # Sort
    ranked.sort(key=lambda x: x[1], reverse=not lower_is_better)
    
    return [r[0] for r in ranked]


def compute_comparison_metrics(
    results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Compute comparison metrics across all candidates.
    
    Args:
        results: List of simulation result dictionaries
        
    Returns:
        Dictionary with comparison results
    """
    # Extract key metrics
    candidate_ids = [r['candidate_id'] for r in results]
    pressure_drops = [r['metrics']['simulated_quantities']['pressure_drop']['pressure_drop_pa'] for r in results]
    flow_rates = [r['metrics']['simulated_quantities']['flow_rate']['flow_rate_m3_s'] for r in results]
    hydraulic_resistances = [r['metrics']['simulated_quantities']['hydraulic_resistance']['hydraulic_resistance_pa_s_m3'] for r in results]
    porosities = [r['metrics']['geometric_quantities']['porosity'] for r in results]
    
    # Rankings (lower pressure drop is better)
    pressure_drop_ranking = np.argsort(pressure_drops).tolist()
    flow_rate_ranking = np.argsort(flow_rates)[::-1].tolist()  # Higher flow is better
    resistance_ranking = np.argsort(hydraulic_resistances).tolist()  # Lower resistance is better
    
    return {
        'n_candidates': len(results),
        'candidate_ids': candidate_ids,
        'pressure_drop_pa': {
            'values': pressure_drops,
            'ranking': pressure_drop_ranking,
            'best_candidate': candidate_ids[pressure_drop_ranking[0]],
            'best_value': pressure_drops[pressure_drop_ranking[0]],
            'worst_value': pressure_drops[pressure_drop_ranking[-1]],
            'mean': float(np.mean(pressure_drops)),
            'std': float(np.std(pressure_drops)),
            'label': 'SIMULATED'
        },
        'flow_rate_m3_s': {
            'values': flow_rates,
            'ranking': flow_rate_ranking,
            'best_candidate': candidate_ids[flow_rate_ranking[0]],
            'best_value': flow_rates[flow_rate_ranking[0]],
            'worst_value': flow_rates[flow_rate_ranking[-1]],
            'mean': float(np.mean(flow_rates)),
            'std': float(np.std(flow_rates)),
            'label': 'SIMULATED'
        },
        'hydraulic_resistance_pa_s_m3': {
            'values': hydraulic_resistances,
            'ranking': resistance_ranking,
            'best_candidate': candidate_ids[resistance_ranking[0]],
            'best_value': hydraulic_resistances[resistance_ranking[0]],
            'worst_value': hydraulic_resistances[resistance_ranking[-1]],
            'mean': float(np.mean(hydraulic_resistances)),
            'std': float(np.std(hydraulic_resistances)),
            'label': 'SIMULATED'
        },
        'porosity': {
            'values': porosities,
            'mean': float(np.mean(porosities)),
            'std': float(np.std(porosities)),
            'label': 'GEOMETRIC'
        }
    }


def generate_comparison_summary(
    results: List[Dict[str, Any]],
    comparison_metrics: Dict[str, Any],
    matched_conditions: Dict[str, Any]
) -> str:
    """
    Generate human-readable comparison summary.
    
    Args:
        results: List of simulation result dictionaries
        comparison_metrics: Output from compute_comparison_metrics
        matched_conditions: Output from verify_matched_conditions
        
    Returns:
        Markdown-formatted summary string
    """
    lines = ["# Stage 4 Simulation Comparison", ""]
    
    # Matched conditions check
    lines.append("## Matched Conditions Verification")
    if matched_conditions['matched']:
        lines.append("✓ All candidates simulated under matched conditions")
    else:
        lines.append("✗ MISMATCH DETECTED: " + ", ".join(matched_conditions['mismatches']))
    lines.append("")
    
    # Number of candidates
    lines.append(f"## Candidates Compared: {comparison_metrics['n_candidates']}")
    lines.append("")
    for cid in comparison_metrics['candidate_ids']:
        lines.append(f"- {cid}")
    lines.append("")
    
    # Pressure drop comparison
    lines.append("## Pressure Drop (SIMULATED)")
    pd = comparison_metrics['pressure_drop_pa']
    lines.append(f"- Best: {pd['best_candidate']} = {pd['best_value']:.2f} Pa")
    lines.append(f"- Worst: {pd['worst_value']:.2f} Pa")
    lines.append(f"- Mean: {pd['mean']:.2f} Pa")
    lines.append(f"- Std: {pd['std']:.2f} Pa")
    lines.append("")
    
    # Flow rate comparison
    lines.append("## Flow Rate (SIMULATED)")
    fr = comparison_metrics['flow_rate_m3_s']
    lines.append(f"- Best: {fr['best_candidate']} = {fr['best_value']*1e6:.4f} mL/s")
    lines.append(f"- Worst: {fr['worst_value']*1e6:.4f} mL/s")
    lines.append(f"- Mean: {fr['mean']*1e6:.4f} mL/s")
    lines.append(f"- Std: {fr['std']*1e6:.4f} mL/s")
    lines.append("")
    
    # Hydraulic resistance comparison
    lines.append("## Hydraulic Resistance (SIMULATED)")
    hr = comparison_metrics['hydraulic_resistance_pa_s_m3']
    lines.append(f"- Best: {hr['best_candidate']} = {hr['best_value']:.2e} Pa·s/m³")
    lines.append(f"- Worst: {hr['worst_value']:.2e} Pa·s/m³")
    lines.append(f"- Mean: {hr['mean']:.2e} Pa·s/m³")
    lines.append(f"- Std: {hr['std']:.2e} Pa·s/m³")
    lines.append("")
    
    # Porosity (geometric)
    lines.append("## Porosity (GEOMETRIC)")
    por = comparison_metrics['porosity']
    lines.append(f"- Mean: {por['mean']:.3f}")
    lines.append(f"- Std: {por['std']:.3f}")
    lines.append("")
    
    # Labels reminder
    lines.append("## Quantity Labels")
    lines.append("- **SIMULATED**: Computed from actual flow solver")
    lines.append("- **GEOMETRIC**: Derived from geometry only")
    lines.append("- **NOT COMPUTED**: Thermal simulation not yet implemented")
    lines.append("")
    
    return "\n".join(lines)
