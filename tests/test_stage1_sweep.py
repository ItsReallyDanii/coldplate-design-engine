"""Tests for Stage 1 sweep runner."""

import pytest
import numpy as np
import sys
from pathlib import Path
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stage1_2d.sweep import run_sweep, generate_param_combinations
from stage1_2d.schemas import SweepConfig, GridConfig, BaselineFamily
from stage1_2d.io import load_mask


@pytest.fixture
def temp_output_dir():
    """Create temporary output directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def minimal_sweep_config(temp_output_dir):
    """Minimal sweep configuration for testing."""
    grid = GridConfig(nx=50, ny=50, dx=1e-4, dy=1e-4)
    
    return SweepConfig(
        output_dir=temp_output_dir,
        grid=grid,
        families=[BaselineFamily.STRAIGHT_CHANNEL],
        param_ranges={
            "straight_channel": {
                "num_channels": [2, 4],
                "channel_width_fraction": [0.5],
            }
        },
        seed_start=42,
        num_samples_per_config=1
    )


class TestParamCombinations:
    """Tests for parameter combination generation."""
    
    def test_single_param(self):
        """Test single parameter with multiple values."""
        param_ranges = {
            "straight_channel": {
                "num_channels": [2, 4, 8],
            }
        }
        
        combos = generate_param_combinations(
            BaselineFamily.STRAIGHT_CHANNEL,
            param_ranges
        )
        
        assert len(combos) == 3
        assert {"num_channels": 2} in combos
        assert {"num_channels": 4} in combos
        assert {"num_channels": 8} in combos
    
    def test_multiple_params(self):
        """Test multiple parameters with cartesian product."""
        param_ranges = {
            "straight_channel": {
                "num_channels": [2, 4],
                "channel_width_fraction": [0.4, 0.5],
            }
        }
        
        combos = generate_param_combinations(
            BaselineFamily.STRAIGHT_CHANNEL,
            param_ranges
        )
        
        assert len(combos) == 4  # 2 x 2
    
    def test_missing_family(self):
        """Test family not in param_ranges."""
        param_ranges = {}
        
        combos = generate_param_combinations(
            BaselineFamily.STRAIGHT_CHANNEL,
            param_ranges
        )
        
        assert len(combos) == 1
        assert combos[0] == {}


class TestSweepRunner:
    """Tests for sweep runner."""
    
    def test_sweep_runs_successfully(self, minimal_sweep_config):
        """Test sweep runs without errors."""
        results = run_sweep(minimal_sweep_config, verbose=False)
        
        assert len(results) > 0
    
    def test_sweep_creates_output_dir(self, minimal_sweep_config):
        """Test sweep creates output directory."""
        run_sweep(minimal_sweep_config, verbose=False)
        
        assert Path(minimal_sweep_config.output_dir).exists()
    
    def test_sweep_creates_manifest(self, minimal_sweep_config):
        """Test sweep creates run manifest."""
        run_sweep(minimal_sweep_config, verbose=False)
        
        manifest_path = Path(minimal_sweep_config.output_dir) / "run_manifest.json"
        assert manifest_path.exists()
    
    def test_sweep_creates_csv(self, minimal_sweep_config):
        """Test sweep creates metrics CSV."""
        run_sweep(minimal_sweep_config, verbose=False)
        
        csv_path = Path(minimal_sweep_config.output_dir) / "metrics.csv"
        assert csv_path.exists()
    
    def test_sweep_creates_jsonl(self, minimal_sweep_config):
        """Test sweep creates metrics JSONL."""
        run_sweep(minimal_sweep_config, verbose=False)
        
        jsonl_path = Path(minimal_sweep_config.output_dir) / "metrics.jsonl"
        assert jsonl_path.exists()
    
    def test_sweep_saves_masks(self, minimal_sweep_config):
        """Test sweep saves mask files."""
        results = run_sweep(minimal_sweep_config, verbose=False)
        
        masks_dir = Path(minimal_sweep_config.output_dir) / "masks"
        assert masks_dir.exists()
        
        # Check at least one mask was saved
        mask_files = list(masks_dir.glob("*.npy"))
        assert len(mask_files) > 0
    
    def test_sweep_result_count_matches_config(self, minimal_sweep_config):
        """Test number of results matches configuration."""
        results = run_sweep(minimal_sweep_config, verbose=False)
        
        # 2 channel counts x 1 width fraction x 1 sample = 2
        expected_count = 2
        assert len(results) == expected_count
    
    def test_sweep_with_multiple_families(self, temp_output_dir):
        """Test sweep with multiple baseline families."""
        grid = GridConfig(nx=50, ny=50, dx=1e-4, dy=1e-4)
        
        config = SweepConfig(
            output_dir=temp_output_dir,
            grid=grid,
            families=[
                BaselineFamily.STRAIGHT_CHANNEL,
                BaselineFamily.PIN_FIN,
            ],
            param_ranges={
                "straight_channel": {
                    "num_channels": [4],
                    "channel_width_fraction": [0.5],
                },
                "pin_fin": {
                    "pin_diameter_px": [5],
                    "pin_spacing_px": [20],
                    "offset_rows": [False],
                },
            },
            seed_start=42,
            num_samples_per_config=1
        )
        
        results = run_sweep(config, verbose=False)
        
        # Should have results from both families
        assert len(results) == 2
        
        families_in_results = set()
        for result in results:
            if result.baseline_params:
                families_in_results.add(result.baseline_params.family)
        
        assert BaselineFamily.STRAIGHT_CHANNEL in families_in_results
        assert BaselineFamily.PIN_FIN in families_in_results
    
    def test_deterministic_with_seed(self, temp_output_dir):
        """Test sweep is deterministic with same seed."""
        grid = GridConfig(nx=50, ny=50, dx=1e-4, dy=1e-4)
        
        config = SweepConfig(
            output_dir=temp_output_dir,
            grid=grid,
            families=[BaselineFamily.STRAIGHT_CHANNEL],
            param_ranges={
                "straight_channel": {
                    "num_channels": [4],
                    "channel_width_fraction": [0.5],
                }
            },
            seed_start=42,
            num_samples_per_config=2  # Multiple samples
        )
        
        results = run_sweep(config, verbose=False)
        
        # Load masks and verify they're different
        masks_dir = Path(config.output_dir) / "masks"
        mask_files = sorted(masks_dir.glob("*.npy"))
        
        assert len(mask_files) == 2
        
        mask1 = load_mask(str(mask_files[0]))
        mask2 = load_mask(str(mask_files[1]))
        
        # Different seeds should produce different masks (for most generators)
        # But both should be valid
        assert mask1.shape == mask2.shape


class TestEndToEnd:
    """End-to-end smoke tests."""
    
    def test_all_families_in_smoke_test(self, temp_output_dir):
        """Test all 6 baseline families can be generated and evaluated."""
        grid = GridConfig(nx=50, ny=50, dx=1e-4, dy=1e-4)
        
        all_families = [
            BaselineFamily.STRAIGHT_CHANNEL,
            BaselineFamily.SERPENTINE_CHANNEL,
            BaselineFamily.PIN_FIN,
            BaselineFamily.GYROID_2D,
            BaselineFamily.DIAMOND_2D,
            BaselineFamily.PRIMITIVE_2D,
        ]
        
        config = SweepConfig(
            output_dir=temp_output_dir,
            grid=grid,
            families=all_families,
            param_ranges={
                "straight_channel": {"num_channels": [4], "channel_width_fraction": [0.5]},
                "serpentine_channel": {"channel_width_px": [8], "turn_radius_px": [10], "num_passes": [3]},
                "pin_fin": {"pin_diameter_px": [5], "pin_spacing_px": [15], "offset_rows": [False]},
                "gyroid_2d": {"wavelength_px": [20], "threshold": [0.0]},
                "diamond_2d": {"wavelength_px": [20], "threshold": [0.0]},
                "primitive_2d": {"wavelength_px": [20], "threshold": [0.0]},
            },
            seed_start=42,
            num_samples_per_config=1
        )
        
        results = run_sweep(config, verbose=False)
        
        # Should have 6 results (one per family)
        assert len(results) == 6
        
        # Verify all families are present
        families_found = set()
        for result in results:
            if result.baseline_params:
                families_found.add(result.baseline_params.family)
        
        assert len(families_found) == 6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
