"""
Comparison logic for Stage 6 structural screening.

Compares candidates under matched structural assumptions and
identifies best candidates by combined thermal-structural performance.
"""

from typing import List, Dict, Any
import numpy as np


def verify_matched_conditions(candidates_metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Verify that candidates are compared under matched conditions.
    
    For structural screening, matched conditions include:
    - Same material properties
    - Same load case definitions
    - Same manufacturability requirements
    - Same structural screening methods
    
    Args:
        candidates_metrics: List of candidate metrics dictionaries
        
    Returns:
        Verification results
    """
    if not candidates_metrics:
        return {'matched': True, 'issues': []}
    
    issues = []
    
    # Check material consistency
    materials = [m['material_properties']['material_name'] for m in candidates_metrics]
    if len(set(materials)) > 1:
        issues.append(f"Multiple materials used: {set(materials)}")
    
    # Check safety factor consistency
    safety_factors = [m['material_properties']['safety_factor'] for m in candidates_metrics]
    if len(set(safety_factors)) > 1:
        issues.append(f"Multiple safety factors used: {set(safety_factors)}")
    
    # Note: Load cases vary per candidate based on their flow/thermal results
    # This is EXPECTED and correct for comparing actual performance
    
    matched = len(issues) == 0
    
    return {
        'matched': matched,
        'issues': issues,
        'note': 'Load cases vary per candidate based on flow/thermal results (expected)'
    }


def rank_candidates_by_combined_performance(
    candidates_metrics: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Rank candidates by combined thermal-structural performance.
    
    Ranking criteria (in priority order):
    1. Must pass structural screening
    2. Must pass manufacturability screening
    3. Lower thermal resistance (better cooling)
    4. Higher structural margin (more robust)
    5. Lower pressure drop (easier to pump)
    
    Args:
        candidates_metrics: List of candidate metrics dictionaries
        
    Returns:
        Ranked list of candidates with scores
    """
    ranked = []
    
    for metrics in candidates_metrics:
        summary = {
            'candidate_id': metrics['candidate_id'],
            'overall_pass': metrics['stage6_verdict']['overall_pass'],
            'structural_pass': metrics['stage6_verdict']['structural_pass'],
            'manufacturability_pass': metrics['stage6_verdict']['manufacturability_pass']
        }
        
        # Extract key metrics
        struct = metrics['structural_screened_quantities']
        thermal = metrics['thermal_simulated_quantities']
        flow = metrics['flow_simulated_quantities']
        
        summary['thermal_resistance_k_w'] = thermal['thermal_resistance']['thermal_resistance_k_w']
        summary['structural_margin'] = struct['combined_stress']['margin_of_safety']
        summary['pressure_drop_pa'] = flow['pressure_drop']['pressure_drop_pa']
        summary['T_max_c'] = thermal['temperature_statistics']['T_max_c']
        
        # Compute composite score (lower is better)
        # Only valid candidates get scored
        if summary['overall_pass']:
            # Normalize metrics to comparable scales
            R_th_normalized = summary['thermal_resistance_k_w'] / 1.0  # ~1 K/W typical
            dP_normalized = summary['pressure_drop_pa'] / 1000.0  # ~1000 Pa typical
            margin_penalty = 1.0 / max(summary['structural_margin'], 0.1)  # Penalize low margin
            
            # Weighted score (thermal dominant, structural as constraint)
            score = (
                1.0 * R_th_normalized +  # Primary: thermal performance
                0.2 * dP_normalized +     # Secondary: hydraulic cost
                0.1 * margin_penalty      # Tertiary: structural robustness
            )
        else:
            score = float('inf')  # Failed candidates ranked last
        
        summary['composite_score'] = score
        ranked.append(summary)
    
    # Sort by score (lower is better)
    ranked.sort(key=lambda x: (not x['overall_pass'], x['composite_score']))
    
    # Add ranks
    for i, item in enumerate(ranked, 1):
        item['rank'] = i
    
    return ranked


def generate_comparison_summary(
    candidates_metrics: List[Dict[str, Any]],
    ranked_candidates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate comparison summary across all candidates.
    
    Args:
        candidates_metrics: List of full candidate metrics
        ranked_candidates: Ranked candidate summaries
        
    Returns:
        Comparison summary dictionary
    """
    n_total = len(candidates_metrics)
    n_pass_structural = sum(1 for m in candidates_metrics if m['stage6_verdict']['structural_pass'])
    n_pass_manufacturability = sum(1 for m in candidates_metrics if m['stage6_verdict']['manufacturability_pass'])
    n_pass_overall = sum(1 for m in candidates_metrics if m['stage6_verdict']['overall_pass'])
    
    # Collect all failure modes
    all_failures = {}
    for metrics in candidates_metrics:
        for mode in metrics['stage6_verdict']['all_failure_modes']:
            all_failures[mode] = all_failures.get(mode, 0) + 1
    
    # Best candidate (if any pass)
    best_candidate = None
    if n_pass_overall > 0:
        best_candidate = ranked_candidates[0]['candidate_id']
    
    # Statistics on passing candidates
    passing_metrics = [r for r in ranked_candidates if r['overall_pass']]
    
    if passing_metrics:
        thermal_resistances = [m['thermal_resistance_k_w'] for m in passing_metrics]
        structural_margins = [m['structural_margin'] for m in passing_metrics]
        
        stats = {
            'thermal_resistance_range_k_w': [min(thermal_resistances), max(thermal_resistances)],
            'structural_margin_range': [min(structural_margins), max(structural_margins)],
            'best_thermal_resistance_k_w': min(thermal_resistances),
            'best_structural_margin': max(structural_margins)
        }
    else:
        stats = None
    
    return {
        'n_candidates': n_total,
        'n_pass_structural': n_pass_structural,
        'n_pass_manufacturability': n_pass_manufacturability,
        'n_pass_overall': n_pass_overall,
        'pass_rate': n_pass_overall / n_total if n_total > 0 else 0.0,
        'best_candidate': best_candidate,
        'failure_mode_counts': all_failures,
        'statistics': stats,
        'ranking': ranked_candidates
    }


def format_comparison_table_markdown(comparison_summary: Dict[str, Any]) -> str:
    """
    Format comparison results as Markdown table.
    
    Args:
        comparison_summary: Comparison summary dictionary
        
    Returns:
        Markdown formatted table string
    """
    lines = []
    lines.append("# Stage 6 Structural Screening Comparison")
    lines.append("")
    lines.append(f"**Total candidates:** {comparison_summary['n_candidates']}")
    lines.append(f"**Pass structural:** {comparison_summary['n_pass_structural']}")
    lines.append(f"**Pass manufacturability:** {comparison_summary['n_pass_manufacturability']}")
    lines.append(f"**Pass overall:** {comparison_summary['n_pass_overall']}")
    lines.append(f"**Pass rate:** {comparison_summary['pass_rate']:.1%}")
    lines.append("")
    
    if comparison_summary['best_candidate']:
        lines.append(f"**Best candidate:** {comparison_summary['best_candidate']}")
        lines.append("")
    
    if comparison_summary['failure_mode_counts']:
        lines.append("## Failure Modes")
        for mode, count in sorted(comparison_summary['failure_mode_counts'].items()):
            lines.append(f"- {mode}: {count}")
        lines.append("")
    
    lines.append("## Ranked Candidates")
    lines.append("")
    lines.append("| Rank | Candidate | Pass | R_th (K/W) | Margin | ΔP (Pa) | T_max (°C) | Score |")
    lines.append("|------|-----------|------|------------|--------|---------|------------|-------|")
    
    for item in comparison_summary['ranking']:
        status = "✓" if item['overall_pass'] else "✗"
        score_str = f"{item['composite_score']:.3f}" if item['composite_score'] != float('inf') else "FAIL"
        lines.append(
            f"| {item['rank']} | {item['candidate_id']} | {status} | "
            f"{item['thermal_resistance_k_w']:.4f} | {item['structural_margin']:.2f} | "
            f"{item['pressure_drop_pa']:.1f} | {item['T_max_c']:.2f} | {score_str} |"
        )
    
    lines.append("")
    lines.append("**Note:** Screening-level analysis only. Full FEA and fabrication validation required before production.")
    
    return "\n".join(lines)
