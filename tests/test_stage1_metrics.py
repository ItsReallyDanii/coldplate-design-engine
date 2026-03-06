"""Tests for Stage 1 metrics engine."""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stage1_2d.metrics import (
    compute_all_metrics,
    get_metric_definitions,
    get_metric_schema_version,
)
from stage1_2d.schemas import MetricCategory


@pytest.fixture
def simple_channel_mask():
    """Simple straight channel mask for testing."""
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[40:60, :] = 1  # Horizontal channel from left to right
    return mask


@pytest.fixture
def disconnected_mask():
    """Mask with disconnected regions."""
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[:, 20:30] = 1
    mask[:, 70:80] = 1  # Disconnected second channel
    return mask


class TestMetricDefinitions:
    """Tests for metric definitions."""
    
    def test_all_metrics_defined(self):
        """Test all metrics have definitions."""
        definitions = get_metric_definitions()
        assert len(definitions) > 0
        
        # Check all expected metrics are present
        expected_metrics = [
            "porosity",
            "wetted_perimeter_proxy",
            "flow_connectivity_score",
            "hydraulic_diameter_proxy",
            "heat_exchange_area_proxy",
        ]
        
        for metric in expected_metrics:
            assert metric in definitions
    
    def test_proxy_metrics_labeled(self):
        """Test all proxy metrics are honestly labeled."""
        definitions = get_metric_definitions()
        
        for name, definition in definitions.items():
            if "_proxy" in name:
                assert definition.is_proxy is True, f"{name} should be marked as proxy"
                assert len(definition.limitations) > 0, f"{name} should have limitations"
    
    def test_non_proxy_metrics_not_labeled(self):
        """Test non-proxy metrics are not incorrectly labeled."""
        definitions = get_metric_definitions()
        
        # Porosity should not be a proxy
        assert definitions["porosity"].is_proxy is False
    
    def test_all_categories_valid(self):
        """Test all metrics have valid categories."""
        definitions = get_metric_definitions()
        
        for name, definition in definitions.items():
            assert isinstance(definition.category, MetricCategory)
    
    def test_schema_version_exists(self):
        """Test metric schema version is defined."""
        version = get_metric_schema_version()
        assert isinstance(version, str)
        assert len(version) > 0


class TestMetricComputation:
    """Tests for metric computation."""
    
    def test_porosity_calculation(self, simple_channel_mask):
        """Test porosity calculation."""
        metrics = compute_all_metrics(simple_channel_mask)
        
        porosity = metrics["porosity"].value
        expected_porosity = simple_channel_mask.mean()
        
        assert abs(porosity - expected_porosity) < 1e-10
    
    def test_all_metrics_computed(self, simple_channel_mask):
        """Test all metrics are computed."""
        metrics = compute_all_metrics(simple_channel_mask)
        definitions = get_metric_definitions()
        
        assert set(metrics.keys()) == set(definitions.keys())
    
    def test_connectivity_score_connected(self, simple_channel_mask):
        """Test connectivity score for connected mask."""
        metrics = compute_all_metrics(simple_channel_mask)
        
        connectivity = metrics["flow_connectivity_score"].value
        assert connectivity == 1.0, "Fully connected mask should have score 1.0"
    
    def test_connectivity_score_disconnected(self, disconnected_mask):
        """Test connectivity score for disconnected mask."""
        metrics = compute_all_metrics(disconnected_mask)
        
        connectivity = metrics["flow_connectivity_score"].value
        assert connectivity < 1.0, "Disconnected mask should have score < 1.0"
    
    def test_dead_zone_fraction(self, simple_channel_mask):
        """Test dead zone fraction for simple horizontal channel."""
        metrics = compute_all_metrics(simple_channel_mask, "left", "right")
        
        dead_zone = metrics["dead_zone_fraction"].value
        # Simple vertical channel should have low/no dead zones
        assert 0.0 <= dead_zone <= 0.1
    
    def test_metric_values_finite(self, simple_channel_mask):
        """Test all metric values are finite."""
        metrics = compute_all_metrics(simple_channel_mask)
        
        for name, result in metrics.items():
            assert np.isfinite(result.value), f"{name} should be finite"
    
    def test_metric_values_non_negative(self, simple_channel_mask):
        """Test appropriate metrics are non-negative."""
        metrics = compute_all_metrics(simple_channel_mask)
        
        non_negative_metrics = [
            "porosity",
            "wetted_perimeter_proxy",
            "min_fluid_feature_px",
            "min_solid_feature_px",
            "dead_zone_fraction",
            "heat_exchange_area_proxy",
        ]
        
        for metric_name in non_negative_metrics:
            assert metrics[metric_name].value >= 0.0, f"{metric_name} should be non-negative"
    
    def test_porosity_bounds(self, simple_channel_mask):
        """Test porosity is in [0, 1]."""
        metrics = compute_all_metrics(simple_channel_mask)
        
        porosity = metrics["porosity"].value
        assert 0.0 <= porosity <= 1.0
    
    def test_empty_mask_handling(self):
        """Test handling of empty (all solid) mask."""
        empty_mask = np.zeros((100, 100), dtype=np.uint8)
        
        # Should not crash
        metrics = compute_all_metrics(empty_mask)
        
        # Porosity should be 0
        assert metrics["porosity"].value == 0.0
    
    def test_full_mask_handling(self):
        """Test handling of full (all fluid) mask."""
        full_mask = np.ones((100, 100), dtype=np.uint8)
        
        # Should not crash
        metrics = compute_all_metrics(full_mask)
        
        # Porosity should be 1
        assert metrics["porosity"].value == 1.0


class TestMetricInvariants:
    """Tests for metric invariants and monotonicity."""
    
    def test_higher_porosity_means_more_open_area(self):
        """Test porosity correlates with open area."""
        mask_low = np.zeros((100, 100), dtype=np.uint8)
        mask_low[:, 45:55] = 1  # Narrow channel
        
        mask_high = np.zeros((100, 100), dtype=np.uint8)
        mask_high[:, 30:70] = 1  # Wide channel
        
        metrics_low = compute_all_metrics(mask_low)
        metrics_high = compute_all_metrics(mask_high)
        
        assert metrics_high["porosity"].value > metrics_low["porosity"].value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
