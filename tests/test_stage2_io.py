"""Tests for Stage 2 comparison and I/O."""

import pytest
import json
import os
import tempfile
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage2_inverse.compare import compare_methods, ComparisonResult
from stage2_inverse import io


class TestCompare:
    """Test comparison framework."""
    
    def create_mock_results(self, num_results=10, score_range=(0, 100), valid_rate=0.8):
        """Create mock results for testing."""
        import numpy as np
        results = []
        rng = np.random.default_rng(42)
        
        for i in range(num_results):
            result = {
                "family": "straight_channel",
                "params": {"num_channels": 4},
                "seed": i,
                "evaluation_num": i,
                "total_score": rng.uniform(score_range[0], score_range[1]),
                "total_objective": rng.uniform(score_range[0], score_range[1]),
                "total_penalty": 0.0,
                "is_valid": rng.random() < valid_rate,
                "objective_breakdown": {},
                "constraint_violations": [],
                "metrics": {
                    "porosity": 0.5,
                    "heat_exchange_area_proxy": 100.0,
                },
            }
            results.append(result)
        
        return results
    
    def test_compare_methods_basic(self):
        """Test basic comparison of two methods."""
        results_a = self.create_mock_results(10, (50, 70))
        results_b = self.create_mock_results(10, (60, 80))
        
        comparison = compare_methods(
            [results_a, results_b],
            ["method_a", "method_b"]
        )
        
        assert comparison.method_names == ["method_a", "method_b"]
        assert len(comparison.budgets) == 2
        assert len(comparison.best_scores) == 2
    
    def test_compare_equal_budgets(self):
        """Test comparison with equal budgets."""
        results_a = self.create_mock_results(20)
        results_b = self.create_mock_results(20)
        
        comparison = compare_methods(
            [results_a, results_b],
            ["method_a", "method_b"]
        )
        
        assert comparison.budgets[0] == comparison.budgets[1]
    
    def test_compare_best_scores(self):
        """Test that best scores are correctly identified."""
        results_a = self.create_mock_results(10, (0, 50))
        results_b = self.create_mock_results(10, (50, 100))
        
        comparison = compare_methods(
            [results_a, results_b],
            ["method_a", "method_b"]
        )
        
        # Method B should have higher best score
        assert comparison.best_scores[1] > comparison.best_scores[0]
    
    def test_compare_valid_counts(self):
        """Test valid/invalid counting."""
        results_a = self.create_mock_results(10, valid_rate=0.7)
        results_b = self.create_mock_results(10, valid_rate=0.9)
        
        comparison = compare_methods(
            [results_a, results_b],
            ["method_a", "method_b"]
        )
        
        assert comparison.valid_counts[0] > 0
        assert comparison.valid_counts[1] > 0
        # Method B should have more valid
        assert comparison.valid_counts[1] > comparison.valid_counts[0]
    
    def test_generate_summary(self):
        """Test summary generation."""
        results_a = self.create_mock_results(10)
        results_b = self.create_mock_results(10)
        
        comparison = compare_methods(
            [results_a, results_b],
            ["random_search", "genetic_algorithm"]
        )
        
        summary = comparison.generate_summary()
        
        assert isinstance(summary, str)
        assert "random_search" in summary
        assert "genetic_algorithm" in summary
        assert "Stage 2 Comparison" in summary
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        results_a = self.create_mock_results(5)
        results_b = self.create_mock_results(5)
        
        comparison = compare_methods(
            [results_a, results_b],
            ["method_a", "method_b"]
        )
        
        d = comparison.to_dict()
        
        assert "method_names" in d
        assert "budgets" in d
        assert "best_scores" in d
        assert isinstance(d, dict)


class TestIO:
    """Test I/O utilities."""
    
    def test_save_and_load_jsonl(self):
        """Test saving and loading JSONL."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.jsonl")
            
            data = [
                {"id": 1, "value": 10.0},
                {"id": 2, "value": 20.0},
            ]
            
            io.save_jsonl(data, filepath)
            
            assert os.path.exists(filepath)
            
            loaded = io.load_jsonl(filepath)
            assert len(loaded) == 2
            assert loaded[0]["id"] == 1
            assert loaded[1]["value"] == 20.0
    
    def test_save_json(self):
        """Test saving JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.json")
            
            data = {"key": "value", "number": 42}
            
            io.save_json(data, filepath)
            
            assert os.path.exists(filepath)
            
            with open(filepath, 'r') as f:
                loaded = json.load(f)
            
            assert loaded["key"] == "value"
            assert loaded["number"] == 42
    
    def test_save_text(self):
        """Test saving text."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.txt")
            
            text = "Hello, Stage 2!"
            
            io.save_text(text, filepath)
            
            assert os.path.exists(filepath)
            
            with open(filepath, 'r') as f:
                loaded = f.read()
            
            assert loaded == text
    
    def test_save_best_candidates_csv(self):
        """Test saving best candidates to CSV."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "best.csv")
            
            candidates = [
                {
                    "family": "straight_channel",
                    "params": {"num_channels": 4, "channel_width_fraction": 0.5},
                    "total_score": 100.0,
                    "total_objective": 100.0,
                    "total_penalty": 0.0,
                    "is_valid": True,
                    "evaluation_num": 0,
                    "seed": 42,
                    "mask_id": "test_mask",
                    "metrics": {
                        "porosity": 0.5,
                        "heat_exchange_area_proxy": 200.0,
                    }
                }
            ]
            
            io.save_best_candidates_csv(candidates, filepath, "test_method")
            
            assert os.path.exists(filepath)
            
            # Check CSV structure
            import csv
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            assert len(rows) == 1
            assert rows[0]["method"] == "test_method"
            assert rows[0]["family"] == "straight_channel"
    
    def test_create_run_manifest(self):
        """Test creating run manifest."""
        manifest = io.create_run_manifest(
            method_name="test_method",
            search_space_dict={"grid": {"nx": 100}},
            objective_dict={"name": "test_objective"},
            budget=100,
            seed=42,
            num_evaluations=95,
            git_sha="abc123"
        )
        
        assert manifest["method"] == "test_method"
        assert manifest["budget"] == 100
        assert manifest["seed"] == 42
        assert manifest["num_evaluations"] == 95
        assert manifest["git_sha"] == "abc123"
        assert "timestamp" in manifest
    
    def test_ensure_output_dir(self):
        """Test ensuring output directory exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, "subdir", "nested")
            
            io.ensure_output_dir(test_dir)
            
            assert os.path.exists(test_dir)
            assert os.path.isdir(test_dir)
