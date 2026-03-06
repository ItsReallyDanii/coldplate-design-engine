"""Tests for Stage 3 validation."""

import pytest
import numpy as np
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage3_geometry import validate


class TestGeometryValidation:
    """Test geometry validation functions."""
    
    def create_test_volume(self, shape=(50, 50, 50), porosity=0.5):
        """Create a simple test volume."""
        np.random.seed(42)
        volume = (np.random.random(shape) < porosity).astype(np.uint8)
        return volume
    
    def create_connected_volume(self, shape=(50, 50, 50)):
        """Create a volume with guaranteed connected fluid region."""
        volume = np.zeros(shape, dtype=np.uint8)
        # Create a single channel through the middle
        nz, ny, nx = shape
        volume[:, ny//4:3*ny//4, nx//4:3*nx//4] = 1
        return volume
    
    def test_check_connectivity_single_component(self):
        """Test connectivity check with single component."""
        volume = self.create_connected_volume((30, 30, 30))
        
        result = validate.check_connectivity(volume)
        
        assert result['is_connected'] is True
        assert result['num_fluid_components'] == 1
        assert result['largest_component_fraction'] == 1.0
    
    def test_check_connectivity_multiple_components(self):
        """Test connectivity check with multiple components."""
        volume = np.zeros((30, 30, 30), dtype=np.uint8)
        # Create two disconnected regions
        volume[5:15, 5:15, 5:15] = 1
        volume[20:25, 20:25, 20:25] = 1
        
        result = validate.check_connectivity(volume)
        
        assert result['is_connected'] is False
        assert result['num_fluid_components'] == 2
    
    def test_check_solid_connectivity(self):
        """Test solid connectivity check."""
        volume = self.create_connected_volume((30, 30, 30))
        
        result = validate.check_solid_connectivity(volume)
        
        assert 'num_solid_components' in result
        assert 'solid_is_connected' in result
    
    def test_estimate_minimum_feature_size(self):
        """Test minimum feature size estimation."""
        volume = self.create_connected_volume((30, 30, 30))
        
        result = validate.estimate_minimum_feature_size(volume, voxel_size=0.1)
        
        assert 'min_channel_diameter_mm' in result
        assert 'min_wall_thickness_mm' in result
        assert result['min_channel_diameter_mm'] > 0
    
    def test_check_bounding_box(self):
        """Test bounding box check."""
        volume = np.zeros((50, 40, 30), dtype=np.uint8)
        
        result = validate.check_bounding_box(volume, voxel_size=0.1)
        
        assert result['dimensions_voxels']['nx'] == 30
        assert result['dimensions_voxels']['ny'] == 40
        assert result['dimensions_voxels']['nz'] == 50
        assert result['dimensions_mm']['x'] == 3.0
        assert result['dimensions_mm']['y'] == 4.0
        assert result['dimensions_mm']['z'] == 5.0
    
    def test_validate_geometry_pass(self):
        """Test geometry validation that should pass."""
        volume = self.create_connected_volume((50, 50, 50))
        
        is_valid, results, errors = validate.validate_geometry(
            volume, voxel_size=0.1, min_feature_size_mm=0.1, require_connected=True
        )
        
        assert is_valid is True
        assert len(errors) == 0
        assert 'porosity' in results
        assert 'connectivity' in results
        assert 'feature_sizes' in results
    
    def test_validate_geometry_fail_connectivity(self):
        """Test geometry validation that fails connectivity."""
        volume = np.zeros((30, 30, 30), dtype=np.uint8)
        # Create two disconnected regions
        volume[5:10, 5:10, 5:10] = 1
        volume[20:25, 20:25, 20:25] = 1
        
        is_valid, results, errors = validate.validate_geometry(
            volume, voxel_size=0.1, require_connected=True
        )
        
        assert is_valid is False
        assert len(errors) > 0
        assert any('not connected' in err for err in errors)
    
    def test_validate_geometry_fail_porosity(self):
        """Test geometry validation that fails porosity check."""
        # All solid
        volume = np.zeros((30, 30, 30), dtype=np.uint8)
        
        is_valid, results, errors = validate.validate_geometry(volume)
        
        assert is_valid is False
        assert any('porosity' in err for err in errors)
    
    def test_check_stl_export_feasible_small(self):
        """Test STL export feasibility for small volume."""
        volume = self.create_connected_volume((20, 20, 20))
        
        is_feasible, message = validate.check_stl_export_feasible(
            volume, max_triangles=100000
        )
        
        assert is_feasible is True
        assert 'triangles' in message.lower()
    
    def test_check_stl_export_feasible_large(self):
        """Test STL export feasibility for large volume."""
        volume = self.create_connected_volume((100, 100, 100))
        
        is_feasible, message = validate.check_stl_export_feasible(
            volume, max_triangles=1000
        )
        
        # Should fail due to too many triangles
        assert is_feasible is False
        assert 'Too many' in message
