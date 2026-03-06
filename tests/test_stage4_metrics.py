"""Tests for Stage 4 metrics and comparison."""

import pytest
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage4_sim import mesh_or_grid, solver, boundary_conditions, metrics, compare


class TestMetrics:
    """Test metrics computation."""
    
    def create_mock_simulation_result(self):
        """Create mock simulation result for testing."""
        shape = (10, 10, 20)
        
        # Mock pressure field (linear gradient in z)
        pressure = np.zeros(shape)
        for k in range(shape[2]):
            pressure[:, :, k] = 101325.0 + 1000.0 * (1.0 - k / (shape[2] - 1))
        
        # Mock velocity field
        velocity = {
            'vx': np.zeros(shape),
            'vy': np.zeros(shape),
            'vz': np.ones(shape) * 0.01  # 1 cm/s in z-direction
        }
        
        return {
            'pressure': pressure,
            'velocity': velocity,
            'converged': True,
            'iterations': 100,
            'solve_time_s': 0.5,
            'tolerance': 1e-6
        }
    
    def create_mock_grid(self):
        """Create mock grid."""
        fluid_mask = np.ones((10, 10, 20), dtype=bool)
        return {
            'fluid_mask': fluid_mask,
            'shape': (10, 10, 20),
            'voxel_size_mm': 0.1,
            'domain_size_mm': (1.0, 1.0, 2.0),
            'porosity': 1.0
        }
    
    def test_compute_pressure_drop(self):
        """Test pressure drop computation."""
        sim_result = self.create_mock_simulation_result()
        grid = self.create_mock_grid()
        
        faces = mesh_or_grid.get_inlet_outlet_faces(grid['shape'])
        
        pd = metrics.compute_pressure_drop(
            sim_result['pressure'],
            faces['inlet_mask'],
            faces['outlet_mask']
        )
        
        assert 'pressure_drop_pa' in pd
        assert pd['label'] == 'SIMULATED'
        assert pd['pressure_drop_pa'] > 0
    
    def test_compute_all_metrics(self):
        """Test computing all metrics."""
        sim_result = self.create_mock_simulation_result()
        grid = self.create_mock_grid()
        bc = boundary_conditions.get_matched_boundary_conditions()
        
        all_metrics = metrics.compute_all_metrics(sim_result, grid, bc)
        
        # Check structure
        assert 'simulated_quantities' in all_metrics
        assert 'geometric_quantities' in all_metrics
        assert 'proxy_quantities' in all_metrics
        assert 'solver_info' in all_metrics
        
        # Check simulated quantities
        sim_q = all_metrics['simulated_quantities']
        assert 'pressure_drop' in sim_q
        assert 'flow_rate' in sim_q
        assert 'velocity_statistics' in sim_q
        assert 'flow_uniformity' in sim_q
        assert 'hydraulic_resistance' in sim_q
        
        # Check all simulated quantities are labeled
        assert sim_q['pressure_drop']['label'] == 'SIMULATED'
        assert sim_q['flow_rate']['label'] == 'SIMULATED'
        assert sim_q['velocity_statistics']['label'] == 'SIMULATED'
        
        # Check geometric quantities
        assert 'porosity' in all_metrics['geometric_quantities']
        assert all_metrics['geometric_quantities']['label'] == 'GEOMETRIC'
        
        # Check proxy quantities note
        assert all_metrics['proxy_quantities']['label'] == 'NOT_COMPUTED'
    
    def test_metric_labeling_honesty(self):
        """Test that all metrics are honestly labeled."""
        sim_result = self.create_mock_simulation_result()
        grid = self.create_mock_grid()
        bc = boundary_conditions.get_matched_boundary_conditions()
        
        all_metrics = metrics.compute_all_metrics(sim_result, grid, bc)
        
        # Every metric should have a label
        for category in ['simulated_quantities', 'geometric_quantities', 'proxy_quantities']:
            if category == 'simulated_quantities':
                for key, val in all_metrics[category].items():
                    assert 'label' in val
                    assert val['label'] in ['SIMULATED', 'GEOMETRIC', 'PROXY', 'NOT_COMPUTED']
            elif category == 'geometric_quantities':
                assert 'label' in all_metrics[category]
            elif category == 'proxy_quantities':
                assert 'label' in all_metrics[category]


class TestComparison:
    """Test comparison framework."""
    
    def create_mock_results(self, n=3):
        """Create mock simulation results for comparison."""
        results = []
        for i in range(n):
            result = {
                'candidate_id': f'candidate_{i:02d}_test_s{1000+i}',
                'grid': {
                    'voxel_size_mm': 0.1,
                    'porosity': 0.6 + i * 0.05
                },
                'boundary_conditions': {
                    'inlet_pressure_pa': 102325.0,
                    'outlet_pressure_pa': 101325.0,
                    'fluid_viscosity_pa_s': 0.001
                },
                'metrics': {
                    'simulated_quantities': {
                        'pressure_drop': {
                            'pressure_drop_pa': 1000.0 - i * 100.0,
                            'label': 'SIMULATED'
                        },
                        'flow_rate': {
                            'flow_rate_m3_s': 1e-6 + i * 1e-7,
                            'label': 'SIMULATED'
                        },
                        'hydraulic_resistance': {
                            'hydraulic_resistance_pa_s_m3': 1e9 / (1.0 + i * 0.1),
                            'label': 'SIMULATED'
                        }
                    },
                    'geometric_quantities': {
                        'porosity': 0.6 + i * 0.05,
                        'label': 'GEOMETRIC'
                    }
                }
            }
            results.append(result)
        
        return results
    
    def test_verify_matched_conditions(self):
        """Test matched conditions verification."""
        results = self.create_mock_results(n=3)
        
        matched = compare.verify_matched_conditions(results)
        
        assert matched['matched'] is True
        assert matched['verification'] == 'PASS'
    
    def test_verify_mismatched_conditions(self):
        """Test detection of mismatched conditions."""
        results = self.create_mock_results(n=3)
        
        # Introduce mismatch
        results[1]['boundary_conditions']['inlet_pressure_pa'] = 105000.0
        
        matched = compare.verify_matched_conditions(results)
        
        assert matched['matched'] is False
        assert 'inlet_pressure_pa' in matched['mismatches']
    
    def test_compute_comparison_metrics(self):
        """Test comparison metrics computation."""
        results = self.create_mock_results(n=3)
        
        comp = compare.compute_comparison_metrics(results)
        
        # Check structure
        assert 'n_candidates' in comp
        assert comp['n_candidates'] == 3
        
        assert 'pressure_drop_pa' in comp
        assert 'flow_rate_m3_s' in comp
        assert 'hydraulic_resistance_pa_s_m3' in comp
        assert 'porosity' in comp
        
        # Check labeling
        assert comp['pressure_drop_pa']['label'] == 'SIMULATED'
        assert comp['porosity']['label'] == 'GEOMETRIC'
        
        # Check rankings
        assert len(comp['pressure_drop_pa']['ranking']) == 3
        assert 'best_candidate' in comp['pressure_drop_pa']
    
    def test_generate_comparison_summary(self):
        """Test summary generation."""
        results = self.create_mock_results(n=3)
        matched = compare.verify_matched_conditions(results)
        comp = compare.compute_comparison_metrics(results)
        
        summary = compare.generate_comparison_summary(results, comp, matched)
        
        # Check it's a string
        assert isinstance(summary, str)
        
        # Check key sections are present
        assert 'Stage 4 Simulation Comparison' in summary
        assert 'Matched Conditions' in summary
        assert 'Pressure Drop' in summary
        assert 'SIMULATED' in summary
        assert 'GEOMETRIC' in summary
    
    def test_ranking_consistency(self):
        """Test that ranking is consistent."""
        results = self.create_mock_results(n=5)
        
        comp = compare.compute_comparison_metrics(results)
        
        # Best candidate should have lowest pressure drop
        best_idx = comp['pressure_drop_pa']['ranking'][0]
        best_dp = comp['pressure_drop_pa']['values'][best_idx]
        
        # All other candidates should have higher or equal pressure drop
        for val in comp['pressure_drop_pa']['values']:
            assert val >= best_dp


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
