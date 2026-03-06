"""Tests for Stage 3 3D promotion."""

import pytest
import numpy as np
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage3_geometry import promote, channels3d, tpms3d


class TestChannelPromotion:
    """Test 3D promotion for channel families."""
    
    def test_straight_channel_3d(self):
        """Test straight channel 3D generation."""
        params = {
            'num_channels': 3,
            'channel_width_fraction': 0.3
        }
        grid_config = {'nx': 100, 'ny': 100, 'dx': 0.0001, 'dy': 0.0001}
        
        volume, metadata = channels3d.generate_straight_channel_3d(
            params, grid_config, height_mm=2.0, resolution=50
        )
        
        assert volume.shape == (50, 50, 50)
        assert volume.dtype == np.uint8
        assert np.any(volume == 1)  # Has fluid regions
        assert np.any(volume == 0)  # Has solid regions
        assert metadata['type'] == '3d_straight_channel'
        assert metadata['num_channels'] == 3
    
    def test_serpentine_channel_3d(self):
        """Test serpentine channel 3D generation."""
        params = {
            'channel_width_px': 10,
            'num_passes': 3
        }
        grid_config = {'nx': 100, 'ny': 100, 'dx': 0.0001, 'dy': 0.0001}
        
        volume, metadata = channels3d.generate_serpentine_channel_3d(
            params, grid_config, height_mm=2.0, resolution=50
        )
        
        assert volume.shape == (50, 50, 50)
        assert np.any(volume == 1)
        assert metadata['type'] == '3d_serpentine_channel'
    
    def test_pin_fin_3d(self):
        """Test pin-fin 3D generation."""
        params = {
            'pin_diameter_px': 8,
            'nx_pins': 4,
            'ny_pins': 4
        }
        grid_config = {'nx': 100, 'ny': 100, 'dx': 0.0001, 'dy': 0.0001}
        
        volume, metadata = channels3d.generate_pin_fin_3d(
            params, grid_config, height_mm=2.0, resolution=50
        )
        
        assert volume.shape == (50, 50, 50)
        assert np.any(volume == 1)
        assert np.any(volume == 0)
        assert metadata['type'] == '3d_pin_fin'


class TestTPMSPromotion:
    """Test 3D promotion for TPMS families."""
    
    def test_gyroid_3d(self):
        """Test gyroid TPMS 3D generation."""
        params = {
            'threshold': 0.0,
            'wavelength_px': 20.0
        }
        grid_config = {'nx': 100, 'ny': 100, 'dx': 0.0001, 'dy': 0.0001}
        
        volume, metadata = tpms3d.generate_gyroid_3d(
            params, grid_config, height_mm=2.0, resolution=50
        )
        
        assert volume.shape == (50, 50, 50)
        assert volume.dtype == np.uint8
        assert np.any(volume == 1)
        assert np.any(volume == 0)
        assert metadata['type'] == '3d_gyroid_tpms'
        assert 'porosity' in metadata
        assert 0 < metadata['porosity'] < 1
    
    def test_diamond_3d(self):
        """Test diamond TPMS 3D generation."""
        params = {
            'threshold': -0.15,
            'wavelength_px': 15.5
        }
        grid_config = {'nx': 100, 'ny': 100, 'dx': 0.0001, 'dy': 0.0001}
        
        volume, metadata = tpms3d.generate_diamond_3d(
            params, grid_config, height_mm=2.0, resolution=50
        )
        
        assert volume.shape == (50, 50, 50)
        assert np.any(volume == 1)
        assert metadata['type'] == '3d_diamond_tpms'
        assert 'porosity' in metadata
    
    def test_primitive_3d(self):
        """Test primitive TPMS 3D generation."""
        params = {
            'threshold': 0.0,
            'wavelength_px': 20.0
        }
        grid_config = {'nx': 100, 'ny': 100, 'dx': 0.0001, 'dy': 0.0001}
        
        volume, metadata = tpms3d.generate_primitive_3d(
            params, grid_config, height_mm=2.0, resolution=50
        )
        
        assert volume.shape == (50, 50, 50)
        assert np.any(volume == 1)
        assert metadata['type'] == '3d_primitive_tpms'
        assert 'porosity' in metadata


class TestCandidatePromotion:
    """Test full candidate promotion."""
    
    def test_promote_diamond_candidate(self):
        """Test promoting a diamond_2d candidate."""
        candidate = {
            'rank': 1,
            'family': 'diamond_2d',
            'seed': 1000,
            'total_score': 2000.0,
            'params': {
                'threshold': -0.15,
                'wavelength_px': 15.5
            }
        }
        
        volume, metadata, error = promote.promote_candidate_to_3d(
            candidate, height_mm=2.0, resolution=30
        )
        
        assert error is None
        assert volume is not None
        assert volume.shape == (30, 30, 30)
        assert metadata['candidate_rank'] == 1
        assert metadata['candidate_family'] == 'diamond_2d'
    
    def test_promote_unsupported_family(self):
        """Test promoting unsupported family fails cleanly."""
        candidate = {
            'rank': 1,
            'family': 'unknown_family',
            'seed': 1000,
            'total_score': 2000.0,
            'params': {}
        }
        
        volume, metadata, error = promote.promote_candidate_to_3d(candidate)
        
        assert volume is None
        assert error is not None
        assert 'Unsupported family' in error
    
    def test_get_family_promotion_status(self):
        """Test getting promotion status for all families."""
        status = promote.get_family_promotion_status()
        
        assert 'diamond_2d' in status
        assert 'gyroid_2d' in status
        assert 'primitive_2d' in status
        assert 'straight_channel' in status
        
        assert status['diamond_2d']['supported'] is True
        assert status['diamond_2d']['method'] == '3d_implicit_tpms'
    
    def test_deterministic_promotion(self):
        """Test that promotion is deterministic."""
        candidate = {
            'rank': 1,
            'family': 'diamond_2d',
            'seed': 1000,
            'total_score': 2000.0,
            'params': {
                'threshold': -0.15,
                'wavelength_px': 15.5
            }
        }
        
        volume1, _, _ = promote.promote_candidate_to_3d(candidate, resolution=30)
        volume2, _, _ = promote.promote_candidate_to_3d(candidate, resolution=30)
        
        assert np.array_equal(volume1, volume2)
