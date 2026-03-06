"""Tests for Stage 1 baseline generators."""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stage1_2d.generators import (
    generate_straight_channel,
    generate_serpentine_channel,
    generate_pin_fin,
    generate_gyroid_2d_proxy,
    generate_diamond_2d_proxy,
    generate_primitive_2d_proxy,
    generate_baseline_mask,
)
from stage1_2d.schemas import GridConfig, BaselineFamily


@pytest.fixture
def test_grid():
    """Standard test grid."""
    return GridConfig(nx=100, ny=100, dx=1e-4, dy=1e-4)


class TestStraightChannel:
    """Tests for straight channel generator."""
    
    def test_deterministic(self, test_grid):
        """Test deterministic generation with same seed."""
        mask1, _ = generate_straight_channel(test_grid, 4, 0.5, seed=42)
        mask2, _ = generate_straight_channel(test_grid, 4, 0.5, seed=42)
        assert np.array_equal(mask1, mask2), "Same seed should produce same mask"
    
    def test_different_seeds(self, test_grid):
        """Test different seeds can produce different masks."""
        mask1, _ = generate_straight_channel(test_grid, 4, 0.5, seed=42)
        mask2, _ = generate_straight_channel(test_grid, 4, 0.5, seed=43)
        # Masks might be identical for simple straight channels, so just check they're valid
        assert mask1.shape == mask2.shape
    
    def test_output_shape(self, test_grid):
        """Test output has correct shape."""
        mask, _ = generate_straight_channel(test_grid, 4, 0.5, seed=42)
        assert mask.shape == (test_grid.ny, test_grid.nx)
    
    def test_binary_values(self, test_grid):
        """Test mask contains only binary values."""
        mask, _ = generate_straight_channel(test_grid, 4, 0.5, seed=42)
        assert set(np.unique(mask)) <= {0, 1}, "Mask should be binary"
    
    def test_porosity_range(self, test_grid):
        """Test porosity is in reasonable range."""
        mask, _ = generate_straight_channel(test_grid, 4, 0.5, seed=42)
        porosity = mask.mean()
        assert 0.0 <= porosity <= 1.0, "Porosity should be in [0, 1]"
        assert porosity > 0.1, "Should have some open area"


class TestSerpentineChannel:
    """Tests for serpentine channel generator."""
    
    def test_deterministic(self, test_grid):
        """Test deterministic generation."""
        mask1, _ = generate_serpentine_channel(test_grid, 10, 15, 3, seed=42)
        mask2, _ = generate_serpentine_channel(test_grid, 10, 15, 3, seed=42)
        assert np.array_equal(mask1, mask2)
    
    def test_output_shape(self, test_grid):
        """Test output has correct shape."""
        mask, _ = generate_serpentine_channel(test_grid, 10, 15, 3, seed=42)
        assert mask.shape == (test_grid.ny, test_grid.nx)
    
    def test_binary_values(self, test_grid):
        """Test binary values."""
        mask, _ = generate_serpentine_channel(test_grid, 10, 15, 3, seed=42)
        assert set(np.unique(mask)) <= {0, 1}


class TestPinFin:
    """Tests for pin-fin generator."""
    
    def test_deterministic(self, test_grid):
        """Test deterministic generation."""
        mask1, _ = generate_pin_fin(test_grid, 8, 25, False, seed=42)
        mask2, _ = generate_pin_fin(test_grid, 8, 25, False, seed=42)
        assert np.array_equal(mask1, mask2)
    
    def test_output_shape(self, test_grid):
        """Test output has correct shape."""
        mask, _ = generate_pin_fin(test_grid, 8, 25, False, seed=42)
        assert mask.shape == (test_grid.ny, test_grid.nx)
    
    def test_binary_values(self, test_grid):
        """Test binary values."""
        mask, _ = generate_pin_fin(test_grid, 8, 25, False, seed=42)
        assert set(np.unique(mask)) <= {0, 1}
    
    def test_offset_vs_aligned(self, test_grid):
        """Test offset vs aligned patterns."""
        mask_aligned, meta_aligned = generate_pin_fin(test_grid, 8, 25, False, seed=42)
        mask_offset, meta_offset = generate_pin_fin(test_grid, 8, 25, True, seed=42)
        
        # Should produce different patterns
        assert not np.array_equal(mask_aligned, mask_offset)


class TestTPMSProxies:
    """Tests for TPMS-adjacent 2D proxy generators."""
    
    def test_gyroid_deterministic(self, test_grid):
        """Test gyroid proxy deterministic generation."""
        mask1, _ = generate_gyroid_2d_proxy(test_grid, 25, 0.0, seed=42)
        mask2, _ = generate_gyroid_2d_proxy(test_grid, 25, 0.0, seed=42)
        assert np.array_equal(mask1, mask2)
    
    def test_diamond_deterministic(self, test_grid):
        """Test diamond proxy deterministic generation."""
        mask1, _ = generate_diamond_2d_proxy(test_grid, 25, 0.0, seed=42)
        mask2, _ = generate_diamond_2d_proxy(test_grid, 25, 0.0, seed=42)
        assert np.array_equal(mask1, mask2)
    
    def test_primitive_deterministic(self, test_grid):
        """Test primitive proxy deterministic generation."""
        mask1, _ = generate_primitive_2d_proxy(test_grid, 25, 0.0, seed=42)
        mask2, _ = generate_primitive_2d_proxy(test_grid, 25, 0.0, seed=42)
        assert np.array_equal(mask1, mask2)
    
    def test_all_proxies_labeled(self, test_grid):
        """Test all TPMS proxies are honestly labeled."""
        _, meta_g = generate_gyroid_2d_proxy(test_grid, 25, 0.0, seed=42)
        _, meta_d = generate_diamond_2d_proxy(test_grid, 25, 0.0, seed=42)
        _, meta_p = generate_primitive_2d_proxy(test_grid, 25, 0.0, seed=42)
        
        assert meta_g["is_2d_proxy"] is True
        assert meta_g["not_true_3d_gyroid"] is True
        
        assert meta_d["is_2d_proxy"] is True
        assert meta_d["not_true_3d_diamond"] is True
        
        assert meta_p["is_2d_proxy"] is True
        assert meta_p["not_true_3d_primitive"] is True
    
    def test_threshold_effect(self, test_grid):
        """Test threshold changes porosity."""
        mask_low, _ = generate_gyroid_2d_proxy(test_grid, 25, -0.2, seed=42)
        mask_mid, _ = generate_gyroid_2d_proxy(test_grid, 25, 0.0, seed=42)
        mask_high, _ = generate_gyroid_2d_proxy(test_grid, 25, 0.2, seed=42)
        
        # Different thresholds should give different porosities
        assert mask_low.mean() != mask_mid.mean() or mask_mid.mean() != mask_high.mean()


class TestBaselineMaskInterface:
    """Tests for unified baseline mask interface."""
    
    def test_all_families_supported(self, test_grid):
        """Test all baseline families can be generated."""
        families_and_params = [
            (BaselineFamily.STRAIGHT_CHANNEL, {"num_channels": 4, "channel_width_fraction": 0.5}),
            (BaselineFamily.SERPENTINE_CHANNEL, {"channel_width_px": 10, "turn_radius_px": 15, "num_passes": 3}),
            (BaselineFamily.PIN_FIN, {"pin_diameter_px": 8, "pin_spacing_px": 25, "offset_rows": False}),
            (BaselineFamily.GYROID_2D, {"wavelength_px": 25, "threshold": 0.0}),
            (BaselineFamily.DIAMOND_2D, {"wavelength_px": 25, "threshold": 0.0}),
            (BaselineFamily.PRIMITIVE_2D, {"wavelength_px": 25, "threshold": 0.0}),
        ]
        
        for family, params in families_and_params:
            mask, metadata = generate_baseline_mask(family, test_grid, params, seed=42)
            assert mask.shape == (test_grid.ny, test_grid.nx)
            assert set(np.unique(mask)) <= {0, 1}
            assert isinstance(metadata, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
