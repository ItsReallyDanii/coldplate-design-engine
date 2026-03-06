"""Tests for Stage 2 sampler and optimization."""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage1_2d.schemas import GridConfig
from stage2_inverse.search_space import create_default_search_space
from stage2_inverse.objectives import create_default_objective
from stage2_inverse.sampler import RandomSearchSampler
from stage2_inverse.optimize import GeneticOptimizer


class TestRandomSearchSampler:
    """Test random search baseline."""
    
    def test_sampler_creation(self):
        """Test sampler can be created."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        sampler = RandomSearchSampler(search_space, objective, seed=42)
        assert sampler is not None
        assert sampler.seed == 42
    
    def test_sample_candidate_deterministic(self):
        """Test deterministic sampling with seed."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        sampler1 = RandomSearchSampler(search_space, objective, seed=42)
        family1, params1, seed1 = sampler1.sample_candidate()
        
        sampler2 = RandomSearchSampler(search_space, objective, seed=42)
        family2, params2, seed2 = sampler2.sample_candidate()
        
        assert family1 == family2
        assert seed1 == seed2
        # Params should be the same
        for key in params1.keys():
            assert key in params2
    
    def test_run_smoke(self):
        """Test running sampler with small budget."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        sampler = RandomSearchSampler(search_space, objective, seed=42)
        results = sampler.run(budget=3)
        
        assert len(results) == 3
        assert sampler.evaluation_count == 3
    
    def test_get_best(self):
        """Test getting best candidates."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        sampler = RandomSearchSampler(search_space, objective, seed=42)
        results = sampler.run(budget=5)
        
        best = sampler.get_best(k=3)
        
        assert len(best) <= 3
        # Check sorted descending
        if len(best) >= 2:
            for i in range(len(best) - 1):
                assert best[i]["total_score"] >= best[i+1]["total_score"]
    
    def test_evaluation_result_structure(self):
        """Test that evaluation results have expected structure."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        sampler = RandomSearchSampler(search_space, objective, seed=42)
        results = sampler.run(budget=1)
        
        result = results[0]
        
        # Check expected fields
        assert "family" in result
        assert "params" in result
        assert "seed" in result
        assert "evaluation_num" in result
        assert "total_score" in result
        assert "is_valid" in result
        assert "objective_breakdown" in result
        assert "metrics" in result


class TestGeneticOptimizer:
    """Test genetic algorithm optimizer."""
    
    def test_optimizer_creation(self):
        """Test optimizer can be created."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        optimizer = GeneticOptimizer(
            search_space, objective, seed=42,
            population_size=5
        )
        
        assert optimizer is not None
        assert optimizer.seed == 42
        assert optimizer.population_size == 5
    
    def test_create_individual(self):
        """Test creating random individual."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        optimizer = GeneticOptimizer(search_space, objective, seed=42, population_size=5)
        individual = optimizer.create_individual()
        
        assert "family" in individual
        assert "params" in individual
        assert "score" in individual
        assert "evaluated" in individual
    
    def test_run_smoke(self):
        """Test running optimizer with small budget."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        optimizer = GeneticOptimizer(
            search_space, objective, seed=42,
            population_size=3
        )
        
        results = optimizer.run(budget=5)
        
        assert len(results) == 5
        assert optimizer.evaluation_count == 5
    
    def test_get_best(self):
        """Test getting best candidates from optimizer."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        optimizer = GeneticOptimizer(
            search_space, objective, seed=42,
            population_size=3
        )
        
        results = optimizer.run(budget=5)
        best = optimizer.get_best(k=3)
        
        assert len(best) <= 3
        # Check sorted
        if len(best) >= 2:
            for i in range(len(best) - 1):
                assert best[i]["total_score"] >= best[i+1]["total_score"]
    
    def test_crossover(self):
        """Test crossover operation."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        optimizer = GeneticOptimizer(search_space, objective, seed=42, population_size=5)
        
        parent1 = optimizer.create_individual()
        parent2 = optimizer.create_individual()
        
        child = optimizer.crossover(parent1, parent2)
        
        assert "family" in child
        assert "params" in child
    
    def test_mutate(self):
        """Test mutation operation."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        optimizer = GeneticOptimizer(search_space, objective, seed=42, population_size=5)
        
        individual = optimizer.create_individual()
        original_params = individual["params"].copy()
        
        mutated = optimizer.mutate(individual)
        
        assert mutated["evaluated"] is False
        # At least one param might have changed (probabilistic)
    
    def test_deterministic_with_seed(self):
        """Test deterministic behavior with same seed."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        optimizer1 = GeneticOptimizer(search_space, objective, seed=42, population_size=3)
        results1 = optimizer1.run(budget=3)
        
        optimizer2 = GeneticOptimizer(search_space, objective, seed=42, population_size=3)
        results2 = optimizer2.run(budget=3)
        
        # Should produce same results with same seed
        assert len(results1) == len(results2)
        for r1, r2 in zip(results1, results2):
            assert r1["family"] == r2["family"]
            assert r1["seed"] == r2["seed"]


class TestComparisonFairness:
    """Test that comparison between methods is fair."""
    
    def test_equal_budgets(self):
        """Test that both methods use equal budgets."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        budget = 10
        
        # Run random search
        random_sampler = RandomSearchSampler(search_space, objective, seed=42)
        random_results = random_sampler.run(budget)
        
        # Run genetic algorithm
        genetic_opt = GeneticOptimizer(search_space, objective, seed=43, population_size=5)
        genetic_results = genetic_opt.run(budget)
        
        # Check equal budgets
        assert len(random_results) == budget
        assert len(genetic_results) == budget
    
    def test_both_methods_runnable(self):
        """Test that both methods can run successfully."""
        grid = GridConfig(50, 50, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        objective = create_default_objective()
        
        budget = 5
        
        # Both should complete without errors
        random_sampler = RandomSearchSampler(search_space, objective, seed=42)
        random_results = random_sampler.run(budget)
        
        genetic_opt = GeneticOptimizer(search_space, objective, seed=43, population_size=3)
        genetic_results = genetic_opt.run(budget)
        
        assert len(random_results) > 0
        assert len(genetic_results) > 0
