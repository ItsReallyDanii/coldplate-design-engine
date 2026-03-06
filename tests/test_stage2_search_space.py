"""Tests for Stage 2 search space."""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage1_2d.schemas import BaselineFamily, GridConfig
from stage2_inverse.search_space import (
    ParameterBound,
    FamilySearchSpace,
    Stage2SearchSpace,
    create_default_search_space
)


class TestParameterBound:
    """Test ParameterBound class."""
    
    def test_clip_within_bounds(self):
        """Test clipping value within bounds."""
        bound = ParameterBound("test", 0.0, 10.0)
        assert bound.clip(5.0) == 5.0
    
    def test_clip_below_min(self):
        """Test clipping value below minimum."""
        bound = ParameterBound("test", 0.0, 10.0)
        assert bound.clip(-5.0) == 0.0
    
    def test_clip_above_max(self):
        """Test clipping value above maximum."""
        bound = ParameterBound("test", 0.0, 10.0)
        assert bound.clip(15.0) == 10.0
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        bound = ParameterBound("test", 0.0, 10.0, "continuous")
        d = bound.to_dict()
        
        assert d["name"] == "test"
        assert d["min_val"] == 0.0
        assert d["max_val"] == 10.0
        assert d["param_type"] == "continuous"


class TestFamilySearchSpace:
    """Test FamilySearchSpace class."""
    
    def test_sample_random_params_continuous(self):
        """Test sampling continuous parameters."""
        family_space = FamilySearchSpace(
            family=BaselineFamily.STRAIGHT_CHANNEL,
            parameter_bounds=[
                ParameterBound("num_channels", 2, 10, "integer"),
                ParameterBound("channel_width_fraction", 0.2, 0.8, "continuous"),
            ]
        )
        
        rng = np.random.default_rng(42)
        params = family_space.sample_random_params(rng)
        
        assert "num_channels" in params
        assert "channel_width_fraction" in params
        assert 2 <= params["num_channels"] <= 10
        assert 0.2 <= params["channel_width_fraction"] <= 0.8
    
    def test_sample_deterministic_with_seed(self):
        """Test deterministic sampling with seed."""
        family_space = FamilySearchSpace(
            family=BaselineFamily.STRAIGHT_CHANNEL,
            parameter_bounds=[
                ParameterBound("num_channels", 2, 10, "integer"),
            ]
        )
        
        rng1 = np.random.default_rng(42)
        params1 = family_space.sample_random_params(rng1)
        
        rng2 = np.random.default_rng(42)
        params2 = family_space.sample_random_params(rng2)
        
        assert params1["num_channels"] == params2["num_channels"]
    
    def test_validate_params_valid(self):
        """Test parameter validation for valid params."""
        family_space = FamilySearchSpace(
            family=BaselineFamily.STRAIGHT_CHANNEL,
            parameter_bounds=[
                ParameterBound("num_channels", 2, 10, "integer"),
            ]
        )
        
        is_valid, violations = family_space.validate_params({"num_channels": 5})
        assert is_valid is True
        assert len(violations) == 0
    
    def test_validate_params_out_of_bounds(self):
        """Test parameter validation for out-of-bounds params."""
        family_space = FamilySearchSpace(
            family=BaselineFamily.STRAIGHT_CHANNEL,
            parameter_bounds=[
                ParameterBound("num_channels", 2, 10, "integer"),
            ]
        )
        
        is_valid, violations = family_space.validate_params({"num_channels": 15})
        assert is_valid is False
        assert len(violations) > 0
    
    def test_validate_params_missing(self):
        """Test parameter validation for missing params."""
        family_space = FamilySearchSpace(
            family=BaselineFamily.STRAIGHT_CHANNEL,
            parameter_bounds=[
                ParameterBound("num_channels", 2, 10, "integer"),
            ]
        )
        
        is_valid, violations = family_space.validate_params({})
        assert is_valid is False
        assert len(violations) > 0


class TestStage2SearchSpace:
    """Test Stage2SearchSpace class."""
    
    def test_get_family_space(self):
        """Test getting family space."""
        grid = GridConfig(100, 100, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        
        straight_space = search_space.get_family_space(BaselineFamily.STRAIGHT_CHANNEL)
        assert straight_space.family == BaselineFamily.STRAIGHT_CHANNEL
        assert len(straight_space.parameter_bounds) > 0
    
    def test_get_family_space_not_found(self):
        """Test getting non-existent family space."""
        grid = GridConfig(100, 100, 0.0001, 0.0001)
        family_spaces = [
            FamilySearchSpace(
                family=BaselineFamily.STRAIGHT_CHANNEL,
                parameter_bounds=[ParameterBound("test", 0, 10)]
            )
        ]
        search_space = Stage2SearchSpace(grid, family_spaces)
        
        with pytest.raises(ValueError):
            search_space.get_family_space(BaselineFamily.PIN_FIN)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        grid = GridConfig(100, 100, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        
        d = search_space.to_dict()
        
        assert "grid" in d
        assert "family_spaces" in d
        assert "allowed_families" in d
        assert d["grid"]["nx"] == 100
        assert d["grid"]["ny"] == 100


class TestDefaultSearchSpace:
    """Test default search space creation."""
    
    def test_create_default_search_space(self):
        """Test that default search space can be created."""
        grid = GridConfig(100, 100, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        
        assert search_space is not None
        assert search_space.grid == grid
        assert len(search_space.family_spaces) == 6  # All 6 families
    
    def test_all_families_present(self):
        """Test that all families are in default search space."""
        grid = GridConfig(100, 100, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        
        families = [fs.family for fs in search_space.family_spaces]
        
        assert BaselineFamily.STRAIGHT_CHANNEL in families
        assert BaselineFamily.SERPENTINE_CHANNEL in families
        assert BaselineFamily.PIN_FIN in families
        assert BaselineFamily.GYROID_2D in families
        assert BaselineFamily.DIAMOND_2D in families
        assert BaselineFamily.PRIMITIVE_2D in families
    
    def test_parameter_bounds_reasonable(self):
        """Test that parameter bounds are reasonable."""
        grid = GridConfig(100, 100, 0.0001, 0.0001)
        search_space = create_default_search_space(grid)
        
        # Check straight channel
        straight_space = search_space.get_family_space(BaselineFamily.STRAIGHT_CHANNEL)
        param_names = [b.name for b in straight_space.parameter_bounds]
        
        assert "num_channels" in param_names
        assert "channel_width_fraction" in param_names
        
        # Check bounds are non-empty
        for bound in straight_space.parameter_bounds:
            assert bound.min_val < bound.max_val
