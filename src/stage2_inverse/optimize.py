"""Inverse-design optimizer for Stage 2.

Implements genetic algorithm for parameterized family optimization.
Chosen for simplicity and effectiveness with structured parameter spaces.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone
import copy
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from stage1_2d.schemas import BaselineFamily, BaselineParams, GridConfig
from stage1_2d.generators import generate_baseline_mask
from stage1_2d.evaluate import evaluate_mask
from .search_space import Stage2SearchSpace, FamilySearchSpace
from .objectives import ObjectiveFunction


class GeneticOptimizer:
    """Genetic algorithm optimizer for parameterized cold plate design.
    
    Chosen for Stage 2 because:
    - Works naturally with parameterized families
    - Can explore multiple families simultaneously
    - Simple to implement and understand
    - Effective for mixed continuous/discrete parameters
    """
    
    def __init__(
        self,
        search_space: Stage2SearchSpace,
        objective_func: ObjectiveFunction,
        seed: int = 42,
        population_size: int = 20,
        elite_fraction: float = 0.2,
        mutation_rate: float = 0.2,
        crossover_rate: float = 0.6,
    ):
        """Initialize genetic optimizer.
        
        Args:
            search_space: Stage 2 search space
            objective_func: Objective function
            seed: Random seed
            population_size: Size of population
            elite_fraction: Fraction of population to keep as elites
            mutation_rate: Probability of mutation per parameter
            crossover_rate: Probability of crossover
        """
        self.search_space = search_space
        self.objective_func = objective_func
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        
        self.population_size = population_size
        self.elite_count = max(1, int(population_size * elite_fraction))
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        
        self.evaluation_count = 0
        self.generation = 0
        self.population = []
        self.history = []
    
    def create_individual(self) -> Dict[str, Any]:
        """Create a random individual (candidate design).
        
        Returns:
            Individual dict with family and params
        """
        family = self.rng.choice(self.search_space.allowed_families)
        family_space = self.search_space.get_family_space(family)
        params = family_space.sample_random_params(self.rng)
        
        # Handle discrete boolean
        if "offset_rows" in params:
            params["offset_rows"] = bool(int(params["offset_rows"]))
        
        return {
            "family": family,
            "params": params,
            "score": None,
            "is_valid": None,
            "evaluated": False,
        }
    
    def evaluate_individual(self, individual: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate an individual.
        
        Args:
            individual: Individual to evaluate
            
        Returns:
            Evaluation result (updates individual in-place and returns full result)
        """
        family = individual["family"]
        params = individual["params"]
        sample_seed = self.seed + self.evaluation_count
        
        # Create BaselineParams
        baseline_params = BaselineParams(
            family=family,
            grid=self.search_space.grid,
            seed=sample_seed,
            params=params
        )
        
        # Generate and evaluate
        try:
            mask = generate_baseline_mask(baseline_params)
            mask_id = f"{family.value}_s{sample_seed}_eval{self.evaluation_count}_gen{self.generation}"
            eval_result = evaluate_mask(mask, mask_id, baseline_params)
            obj_result = self.objective_func.evaluate(eval_result.metrics)
            
            individual["score"] = obj_result["total_score"]
            individual["is_valid"] = obj_result["is_valid"]
            individual["evaluated"] = True
            
            result = {
                "family": family.value,
                "params": params,
                "seed": sample_seed,
                "evaluation_num": self.evaluation_count,
                "generation": self.generation,
                "mask_id": mask_id,
                "total_score": obj_result["total_score"],
                "total_objective": obj_result["total_objective"],
                "total_penalty": obj_result["total_penalty"],
                "is_valid": obj_result["is_valid"],
                "objective_breakdown": obj_result["objective_breakdown"],
                "constraint_violations": obj_result["constraint_violations"],
                "metrics": {k: v.value for k, v in eval_result.metrics.items()},
                "warnings": eval_result.warnings,
                "timestamp": eval_result.timestamp,
            }
            
        except Exception as e:
            individual["score"] = float('-inf')
            individual["is_valid"] = False
            individual["evaluated"] = True
            
            result = {
                "family": family.value,
                "params": params,
                "seed": sample_seed,
                "evaluation_num": self.evaluation_count,
                "generation": self.generation,
                "is_valid": False,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        
        self.evaluation_count += 1
        self.history.append(result)
        
        return result
    
    def crossover(self, parent1: Dict[str, Any], parent2: Dict[str, Any]) -> Dict[str, Any]:
        """Create offspring via crossover.
        
        If parents are same family: mix parameters
        If different families: randomly choose one parent's family
        """
        if self.rng.random() > self.crossover_rate:
            # No crossover, return copy of parent1
            return copy.deepcopy(parent1)
        
        # If same family, do parameter crossover
        if parent1["family"] == parent2["family"]:
            child = {
                "family": parent1["family"],
                "params": {},
                "score": None,
                "is_valid": None,
                "evaluated": False,
            }
            
            # Mix parameters
            for key in parent1["params"].keys():
                if self.rng.random() < 0.5:
                    child["params"][key] = parent1["params"][key]
                else:
                    child["params"][key] = parent2["params"][key]
            
            return child
        else:
            # Different families - pick one randomly
            parent = parent1 if self.rng.random() < 0.5 else parent2
            return copy.deepcopy(parent)
    
    def mutate(self, individual: Dict[str, Any]) -> Dict[str, Any]:
        """Mutate an individual.
        
        Args:
            individual: Individual to mutate (modified in-place)
            
        Returns:
            Mutated individual (same object)
        """
        family_space = self.search_space.get_family_space(individual["family"])
        
        for bound in family_space.parameter_bounds:
            if self.rng.random() < self.mutation_rate:
                param_name = bound.name
                
                if bound.param_type == "discrete":
                    # Flip discrete value
                    individual["params"][param_name] = self.rng.choice([bound.min_val, bound.max_val])
                    if param_name == "offset_rows":
                        individual["params"][param_name] = bool(int(individual["params"][param_name]))
                
                elif bound.param_type == "integer":
                    # Mutate integer with Gaussian noise
                    current = individual["params"][param_name]
                    delta = int(self.rng.normal(0, (bound.max_val - bound.min_val) * 0.2))
                    new_val = current + delta
                    individual["params"][param_name] = int(np.clip(new_val, bound.min_val, bound.max_val))
                
                else:  # continuous
                    # Mutate continuous with Gaussian noise
                    current = individual["params"][param_name]
                    delta = self.rng.normal(0, (bound.max_val - bound.min_val) * 0.1)
                    new_val = current + delta
                    individual["params"][param_name] = np.clip(new_val, bound.min_val, bound.max_val)
        
        individual["evaluated"] = False
        individual["score"] = None
        individual["is_valid"] = None
        
        return individual
    
    def select_parents(self, population: List[Dict[str, Any]], k: int) -> List[Dict[str, Any]]:
        """Select k parents via tournament selection.
        
        Args:
            population: Current population
            k: Number of parents to select
            
        Returns:
            List of selected parents
        """
        parents = []
        for _ in range(k):
            # Tournament selection with size 3
            tournament = self.rng.choice(population, size=min(3, len(population)), replace=False)
            winner = max(tournament, key=lambda x: x["score"] if x["score"] is not None else float('-inf'))
            parents.append(winner)
        return parents
    
    def evolve_generation(self):
        """Evolve one generation."""
        # Sort population by score
        self.population.sort(key=lambda x: x["score"] if x["score"] is not None else float('-inf'), reverse=True)
        
        # Keep elites
        next_population = copy.deepcopy(self.population[:self.elite_count])
        
        # Generate offspring to fill rest of population
        while len(next_population) < self.population_size:
            # Select parents
            parents = self.select_parents(self.population, 2)
            
            # Crossover
            child = self.crossover(parents[0], parents[1])
            
            # Mutate
            child = self.mutate(child)
            
            next_population.append(child)
        
        self.population = next_population
        self.generation += 1
    
    def run(self, budget: int) -> List[Dict[str, Any]]:
        """Run genetic algorithm with evaluation budget.
        
        Args:
            budget: Total number of evaluations allowed
            
        Returns:
            List of all evaluation results
        """
        # Initialize population
        print(f"Initializing population of {self.population_size}...")
        self.population = [self.create_individual() for _ in range(self.population_size)]
        
        # Evaluate initial population
        for individual in self.population:
            if self.evaluation_count >= budget:
                break
            self.evaluate_individual(individual)
        
        valid_count = sum(1 for ind in self.population if ind.get("is_valid", False))
        print(f"Generation 0: {len(self.population)} individuals, {valid_count} valid")
        
        # Evolution loop
        while self.evaluation_count < budget:
            self.evolve_generation()
            
            # Evaluate new individuals
            for individual in self.population:
                if self.evaluation_count >= budget:
                    break
                if not individual.get("evaluated", False):
                    self.evaluate_individual(individual)
            
            # Progress report
            valid_count = sum(1 for ind in self.population if ind.get("is_valid", False))
            best_score = max((ind["score"] for ind in self.population if ind["score"] is not None), default=float('-inf'))
            print(f"Generation {self.generation}: {self.evaluation_count}/{budget} evals, "
                  f"{valid_count} valid, best score: {best_score:.3f}")
        
        return self.history
    
    def get_best(self, k: int = 1, valid_only: bool = True) -> List[Dict[str, Any]]:
        """Get best k candidates.
        
        Args:
            k: Number of top candidates
            valid_only: Only consider valid candidates
            
        Returns:
            Top k candidates sorted by score
        """
        candidates = self.history
        if valid_only:
            candidates = [c for c in candidates if c.get("is_valid", False)]
        
        if not candidates:
            return []
        
        sorted_candidates = sorted(
            candidates,
            key=lambda x: x.get("total_score", float('-inf')),
            reverse=True
        )
        
        return sorted_candidates[:k]
