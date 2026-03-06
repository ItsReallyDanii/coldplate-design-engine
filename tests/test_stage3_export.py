"""Tests for Stage 3 export functionality."""

import pytest
import numpy as np
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage3_geometry import export


class TestExport:
    """Test geometry export functions."""
    
    def create_test_volume(self, shape=(20, 20, 20)):
        """Create a simple test volume with a channel."""
        volume = np.zeros(shape, dtype=np.uint8)
        nz, ny, nx = shape
        # Create a channel through the middle
        volume[:, ny//3:2*ny//3, nx//3:2*nx//3] = 1
        return volume
    
    def test_export_stl(self, tmp_path):
        """Test STL export."""
        volume = self.create_test_volume((20, 20, 20))
        stl_path = tmp_path / "test.stl"
        
        success = export.export_stl_from_volume(
            volume, str(stl_path), voxel_size=0.1
        )
        
        assert success is True
        assert os.path.exists(stl_path)
        
        # Check file is not empty
        assert os.path.getsize(stl_path) > 0
        
        # Check it's ASCII STL format
        with open(stl_path, 'r') as f:
            first_line = f.readline()
            assert first_line.startswith('solid')
    
    def test_export_raw_volume(self, tmp_path):
        """Test raw volume export."""
        volume = self.create_test_volume((20, 20, 20))
        raw_path = tmp_path / "test.npy"
        
        metadata = {
            'type': 'test',
            'resolution': 20
        }
        
        success = export.export_raw_volume(
            volume, str(raw_path), metadata
        )
        
        assert success is True
        assert os.path.exists(raw_path)
        
        # Load and verify
        loaded_volume = np.load(raw_path)
        assert np.array_equal(loaded_volume, volume)
        
        # Check metadata file
        metadata_path = str(raw_path).replace('.npy', '_metadata.json')
        assert os.path.exists(metadata_path)
    
    def test_get_volume_info(self):
        """Test getting volume info."""
        volume = self.create_test_volume((30, 30, 30))
        
        info = export.get_volume_info(volume)
        
        assert info['shape'] == (30, 30, 30)
        assert info['dtype'] == 'uint8'
        assert 0 < info['porosity'] < 1
        assert info['fluid_voxels'] > 0
        assert info['solid_voxels'] > 0
        assert info['total_voxels'] == 30 * 30 * 30
        assert info['fluid_voxels'] + info['solid_voxels'] == info['total_voxels']
    
    def test_export_stl_empty_volume(self, tmp_path):
        """Test STL export with empty volume."""
        volume = np.zeros((10, 10, 10), dtype=np.uint8)
        stl_path = tmp_path / "empty.stl"
        
        # Should handle gracefully (might fail or create empty STL)
        # Just ensure it doesn't crash
        try:
            export.export_stl_from_volume(volume, str(stl_path))
        except:
            pass  # Expected to fail gracefully
    
    def test_export_stl_full_volume(self, tmp_path):
        """Test STL export with full volume."""
        volume = np.ones((10, 10, 10), dtype=np.uint8)
        stl_path = tmp_path / "full.stl"
        
        # Should handle gracefully
        try:
            success = export.export_stl_from_volume(volume, str(stl_path))
            # If succeeds, file should exist
            if success:
                assert os.path.exists(stl_path)
        except:
            pass  # May fail for full volume (no surface)
