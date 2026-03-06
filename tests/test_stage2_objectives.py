"""Tests for Stage 2 objectives and constraints."""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage1_2d.schemas import MetricResult, MetricDefinition, MetricCategory
from stage2_inverse.objectives import (
    ObjectiveTerm,
    Constraint,
    ObjectiveFunction,
    create_default_objective
)


class TestObjectiveTerm:
    """Test ObjectiveTerm class."""
    
    def test_maximize_score(self):
        """Test maximization score computation."""
        term = ObjectiveTerm(
            name="test",
            metric_name="test_metric",
            weight=2.0,
            goal="maximize"
        )
        
        score = term.compute_score(10.0)
        assert score == 20.0
    
    def test_minimize_score(self):
        """Test minimization score computation."""
        term = ObjectiveTerm(
            name="test",
            metric_name="test_metric",
            weight=2.0,
            goal="minimize"
        )
        
        score = term.compute_score(10.0)
        assert score == -20.0
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        term = ObjectiveTerm(
            name="test",
            metric_name="test_metric",
            weight=1.0,
            goal="maximize",
            is_proxy=True,
            description="Test objective"
        )
        
        d = term.to_dict()
        assert d["name"] == "test"
        assert d["weight"] == 1.0
        assert d["is_proxy"] is True


class TestConstraint:
    """Test Constraint class."""
    
    def test_min_constraint_satisfied(self):
        """Test minimum constraint when satisfied."""
        constraint = Constraint(
            name="min_test",
            metric_name="test_metric",
            constraint_type="min",
            threshold_min=5.0,
            hard=True
        )
        
        assert constraint.check(10.0) is True
        assert constraint.compute_penalty(10.0) == 0.0
    
    def test_min_constraint_violated_hard(self):
        """Test hard minimum constraint violation."""
        constraint = Constraint(
            name="min_test",
            metric_name="test_metric",
            constraint_type="min",
            threshold_min=5.0,
            hard=True
        )
        
        assert constraint.check(3.0) is False
        assert constraint.compute_penalty(3.0) == float('inf')
    
    def test_min_constraint_violated_soft(self):
        """Test soft minimum constraint violation."""
        constraint = Constraint(
            name="min_test",
            metric_name="test_metric",
            constraint_type="min",
            threshold_min=5.0,
            hard=False,
            penalty_weight=100.0
        )
        
        assert constraint.check(3.0) is False
        penalty = constraint.compute_penalty(3.0)
        assert penalty > 0
        assert penalty == 100.0 * 2.0  # violation magnitude
    
    def test_max_constraint(self):
        """Test maximum constraint."""
        constraint = Constraint(
            name="max_test",
            metric_name="test_metric",
            constraint_type="max",
            threshold_max=10.0,
            hard=True
        )
        
        assert constraint.check(5.0) is True
        assert constraint.check(15.0) is False
    
    def test_range_constraint(self):
        """Test range constraint."""
        constraint = Constraint(
            name="range_test",
            metric_name="test_metric",
            constraint_type="range",
            threshold_min=5.0,
            threshold_max=10.0,
            hard=True
        )
        
        assert constraint.check(7.0) is True
        assert constraint.check(3.0) is False
        assert constraint.check(12.0) is False


class TestObjectiveFunction:
    """Test ObjectiveFunction class."""
    
    def create_mock_metrics(self):
        """Create mock metrics for testing."""
        metrics = {}
        
        # Mock metric definition
        def_proxy = MetricDefinition(
            name="metric_a",
            category=MetricCategory.HEAT_PROXY,
            units="pixels",
            description="Test metric",
            is_proxy=True
        )
        
        def_geom = MetricDefinition(
            name="metric_b",
            category=MetricCategory.GEOMETRIC,
            units="dimensionless",
            description="Test metric",
            is_proxy=False
        )
        
        metrics["metric_a"] = MetricResult(value=100.0, definition=def_proxy)
        metrics["metric_b"] = MetricResult(value=0.5, definition=def_geom)
        
        return metrics
    
    def test_evaluate_simple(self):
        """Test simple objective evaluation."""
        obj_func = ObjectiveFunction(
            objective_terms=[
                ObjectiveTerm("term1", "metric_a", 1.0, "maximize"),
                ObjectiveTerm("term2", "metric_b", 2.0, "minimize"),
            ]
        )
        
        metrics = self.create_mock_metrics()
        result = obj_func.evaluate(metrics)
        
        assert "total_score" in result
        assert "objective_breakdown" in result
        assert result["is_valid"] is True
        assert result["total_penalty"] == 0.0
        
        # Check scores
        # term1: 1.0 * 100 = 100
        # term2: -2.0 * 0.5 = -1.0
        # total: 100 - 1 = 99
        assert result["total_score"] == 99.0
    
    def test_evaluate_with_satisfied_constraint(self):
        """Test evaluation with satisfied constraint."""
        obj_func = ObjectiveFunction(
            objective_terms=[
                ObjectiveTerm("term1", "metric_a", 1.0, "maximize"),
            ],
            constraints=[
                Constraint("c1", "metric_b", "min", threshold_min=0.3, hard=True)
            ]
        )
        
        metrics = self.create_mock_metrics()
        result = obj_func.evaluate(metrics)
        
        assert result["is_valid"] is True
        assert len(result["constraint_violations"]) == 0
        assert result["total_penalty"] == 0.0
    
    def test_evaluate_with_violated_hard_constraint(self):
        """Test evaluation with violated hard constraint."""
        obj_func = ObjectiveFunction(
            objective_terms=[
                ObjectiveTerm("term1", "metric_a", 1.0, "maximize"),
            ],
            constraints=[
                Constraint("c1", "metric_b", "min", threshold_min=0.7, hard=True)
            ]
        )
        
        metrics = self.create_mock_metrics()
        result = obj_func.evaluate(metrics)
        
        assert result["is_valid"] is False
        assert len(result["constraint_violations"]) == 1
        assert result["total_penalty"] == float('inf')
        assert result["total_score"] == float('-inf')


class TestDefaultObjective:
    """Test default objective function."""
    
    def test_default_objective_created(self):
        """Test that default objective can be created."""
        obj = create_default_objective()
        
        assert obj is not None
        assert len(obj.objective_terms) > 0
        assert len(obj.constraints) > 0
    
    def test_default_has_heat_and_hydraulic_terms(self):
        """Test default objective has expected terms."""
        obj = create_default_objective()
        
        term_names = [t.name for t in obj.objective_terms]
        assert "heat_transfer" in term_names
        assert "hydraulic_performance" in term_names
    
    def test_default_has_connectivity_constraint(self):
        """Test default has connectivity constraint."""
        obj = create_default_objective()
        
        constraint_names = [c.name for c in obj.constraints]
        assert "flow_connected" in constraint_names
        assert "porosity_range" in constraint_names
    
    def test_default_to_dict(self):
        """Test default objective serialization."""
        obj = create_default_objective()
        d = obj.to_dict()
        
        assert "objective_terms" in d
        assert "constraints" in d
        assert isinstance(d["objective_terms"], list)
        assert isinstance(d["constraints"], list)
