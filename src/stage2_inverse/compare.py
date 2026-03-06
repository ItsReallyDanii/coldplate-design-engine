"""Comparison framework for Stage 2 inverse design.

Compares inverse-design method against random search baseline
under equal evaluation budget.
"""

import numpy as np
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class ComparisonResult:
    """Results from comparing two methods."""
    method_names: List[str]
    budgets: List[int]
    best_scores: List[float]
    top_k_scores: List[List[float]]
    valid_counts: List[int]
    invalid_counts: List[int]
    family_distributions: List[Dict[str, int]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "method_names": self.method_names,
            "budgets": self.budgets,
            "best_scores": self.best_scores,
            "top_k_scores": self.top_k_scores,
            "valid_counts": self.valid_counts,
            "invalid_counts": self.invalid_counts,
            "family_distributions": self.family_distributions,
        }
    
    def generate_summary(self) -> str:
        """Generate human-readable summary.
        
        Returns:
            Markdown formatted summary
        """
        lines = []
        lines.append("# Stage 2 Comparison Summary\n")
        lines.append("## Methods Compared\n")
        
        for i, method in enumerate(self.method_names):
            lines.append(f"### {method}\n")
            lines.append(f"- Budget: {self.budgets[i]} evaluations")
            lines.append(f"- Valid candidates: {self.valid_counts[i]}")
            lines.append(f"- Invalid candidates: {self.invalid_counts[i]}")
            lines.append(f"- Best score: {self.best_scores[i]:.4f}")
            
            if i < len(self.top_k_scores) and self.top_k_scores[i]:
                top_k = self.top_k_scores[i]
                lines.append(f"- Top-{len(top_k)} mean: {np.mean(top_k):.4f} ± {np.std(top_k):.4f}")
            
            if i < len(self.family_distributions):
                lines.append(f"- Family distribution:")
                for family, count in sorted(self.family_distributions[i].items()):
                    lines.append(f"  - {family}: {count}")
            lines.append("")
        
        # Winner determination
        lines.append("## Comparison\n")
        
        if len(self.method_names) >= 2:
            method_a = self.method_names[0]
            method_b = self.method_names[1]
            score_a = self.best_scores[0]
            score_b = self.best_scores[1]
            
            improvement = ((score_b - score_a) / abs(score_a) * 100) if score_a != 0 else float('inf')
            
            if score_b > score_a:
                lines.append(f"✓ **{method_b}** outperforms **{method_a}**")
                lines.append(f"  - Best score: {score_b:.4f} vs {score_a:.4f}")
                lines.append(f"  - Improvement: {improvement:.2f}%")
                lines.append(f"  - **Stage 2 PASS candidate** (pending full validation)")
            elif score_a > score_b:
                lines.append(f"✗ **{method_a}** outperforms **{method_b}**")
                lines.append(f"  - This suggests inverse-design did NOT beat random search")
                lines.append(f"  - Best score: {score_a:.4f} vs {score_b:.4f}")
                lines.append(f"  - **Stage 2 FAIL** - inverse design did not beat baseline")
            else:
                lines.append(f"→ Methods tied with score {score_a:.4f}")
                lines.append(f"  - **Stage 2 INCONCLUSIVE** - no clear winner")
            lines.append("")
        
        # Budget fairness check
        lines.append("## Budget Fairness\n")
        if len(set(self.budgets)) == 1:
            lines.append(f"✓ All methods used equal budget: {self.budgets[0]} evaluations")
        else:
            lines.append(f"✗ WARNING: Unequal budgets detected!")
            for i, method in enumerate(self.method_names):
                lines.append(f"  - {method}: {self.budgets[i]} evaluations")
        lines.append("")
        
        # Validity check
        lines.append("## Validity Rates\n")
        for i, method in enumerate(self.method_names):
            total = self.valid_counts[i] + self.invalid_counts[i]
            if total > 0:
                rate = self.valid_counts[i] / total * 100
                lines.append(f"- {method}: {rate:.1f}% valid ({self.valid_counts[i]}/{total})")
        lines.append("")
        
        lines.append("---\n")
        lines.append("**Important Note**: All scores are based on Stage 1 proxy metrics.")
        lines.append("These results do NOT establish real thermal or hydraulic superiority.")
        lines.append("CFD and conjugate heat transfer analysis (Stages 3-4) are required for physical claims.\n")
        
        return "\n".join(lines)


def compare_methods(
    method_results: List[Dict[str, Any]],
    method_names: List[str],
    top_k: int = 10
) -> ComparisonResult:
    """Compare results from multiple methods.
    
    Args:
        method_results: List of result lists from each method
        method_names: Names of methods
        top_k: Number of top candidates to compare
        
    Returns:
        ComparisonResult with comparison statistics
    """
    budgets = []
    best_scores = []
    top_k_scores = []
    valid_counts = []
    invalid_counts = []
    family_distributions = []
    
    for results in method_results:
        # Budget
        budgets.append(len(results))
        
        # Valid/invalid counts
        valid = [r for r in results if r.get("is_valid", False)]
        invalid = [r for r in results if not r.get("is_valid", False)]
        valid_counts.append(len(valid))
        invalid_counts.append(len(invalid))
        
        # Best score
        if valid:
            best_score = max(r.get("total_score", float('-inf')) for r in valid)
            best_scores.append(best_score)
            
            # Top-k scores
            sorted_valid = sorted(valid, key=lambda x: x.get("total_score", float('-inf')), reverse=True)
            top_k_list = [r.get("total_score", float('-inf')) for r in sorted_valid[:top_k]]
            top_k_scores.append(top_k_list)
        else:
            best_scores.append(float('-inf'))
            top_k_scores.append([])
        
        # Family distribution (all candidates, valid or not)
        family_dist = {}
        for r in results:
            family = r.get("family", "unknown")
            family_dist[family] = family_dist.get(family, 0) + 1
        family_distributions.append(family_dist)
    
    return ComparisonResult(
        method_names=method_names,
        budgets=budgets,
        best_scores=best_scores,
        top_k_scores=top_k_scores,
        valid_counts=valid_counts,
        invalid_counts=invalid_counts,
        family_distributions=family_distributions,
    )
