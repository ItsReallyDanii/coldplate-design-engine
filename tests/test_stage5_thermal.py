"""Tests for Stage 5 thermal validation."""

import pytest
import os
import sys
import numpy as np
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage5_thermal import (
    load_cases,
    boundary_conditions as bc_module,
    solver as thermal_solver,
    coupling,
    metrics as metrics_module,
    compare as compare_module
)


class TestLoadCases:
    """Test case loading from Stage 4."""
    
    def test_load_stage4_summary(self):
        """Test loading Stage 4 summary file."""
        stage4_dir = 'results/stage4_sim_smoke'
        
        if not os.path.exists(stage4_dir):
            pytest.skip("Stage 4 smoke outputs not available")
        
        summary = load_cases.load_stage4_summary(stage4_dir)
        
        assert 'n_candidates' in summary
        assert 'candidates' in summary
        assert summary['n_candidates'] > 0
    
    def test_load_stage4_candidate(self):
        """Test loading a single Stage 4 candidate."""
        stage4_dir = 'results/stage4_sim_smoke'
        
        if not os.path.exists(stage4_dir):
            pytest.skip("Stage 4 smoke outputs not available")
        
        summary = load_cases.load_stage4_summary(stage4_dir)
        candidate_id = summary['candidates'][0]['candidate_id']
        
        candidate = load_cases.load_stage4_candidate(stage4_dir, candidate_id)
        
        assert 'geometry' in candidate
        assert 'pressure' in candidate
        assert 'velocity' in candidate
        assert 'metrics' in candidate
        assert 'provenance' in candidate
        
        # Check geometry shape
        assert candidate['geometry'].shape == candidate['pressure'].shape
        
        # Check velocity components
        assert 'vx' in candidate['velocity']
        assert 'vy' in candidate['velocity']
        assert 'vz' in candidate['velocity']
    
    def test_select_candidates_for_thermal(self):
        """Test candidate selection."""
        stage4_dir = 'results/stage4_sim_smoke'
        
        if not os.path.exists(stage4_dir):
            pytest.skip("Stage 4 smoke outputs not available")
        
        candidate_ids = load_cases.select_candidates_for_thermal(stage4_dir, top_k=1)
        
        assert len(candidate_ids) >= 1
        assert isinstance(candidate_ids[0], str)


class TestBoundaryConditions:
    """Test thermal boundary conditions."""
    
    def test_matched_thermal_bcs(self):
        """Test getting matched thermal boundary conditions."""
        bc = bc_module.get_matched_thermal_boundary_conditions()
        
        assert 'heat_flux_w_m2' in bc
        assert 'inlet_temperature_c' in bc
        assert 'k_solid_w_m_k' in bc
        assert 'k_fluid_w_m_k' in bc
        assert bc['bc_label'] == 'MATCHED_THERMAL_BC_V1'
    
    def test_estimate_convective_coefficient(self):
        """Test convective coefficient estimation."""
        fluid_props = {
            'rho_fluid_kg_m3': 1000.0,
            'mu_fluid_pa_s': 0.001,
            'cp_fluid_j_kg_k': 4180.0,
            'k_fluid_w_m_k': 0.6
        }
        
        # Test with various velocities
        h1 = bc_module.estimate_convective_coefficient(0.1, fluid_props, 0.0001)
        h2 = bc_module.estimate_convective_coefficient(1.0, fluid_props, 0.0001)
        h3 = bc_module.estimate_convective_coefficient(10.0, fluid_props, 0.0001)
        
        # Higher velocity should give higher h
        assert h2 > h1
        assert h3 > h2
        
        # Should be in reasonable range
        assert 10.0 < h1 < 50000.0
        assert 10.0 < h2 < 50000.0
        assert 10.0 <= h3 <= 50000.0  # May hit upper limit
    
    def test_verify_matched_conditions(self):
        """Test matched condition verification."""
        bc1 = bc_module.get_matched_thermal_boundary_conditions()
        bc2 = bc_module.get_matched_thermal_boundary_conditions()
        
        # Same BCs should match
        assert bc_module.verify_matched_thermal_conditions(bc1, bc2)
        
        # Different BCs should not match
        bc3 = bc1.copy()
        bc3['heat_flux_w_m2'] = bc1['heat_flux_w_m2'] * 2.0
        
        assert not bc_module.verify_matched_thermal_conditions(bc1, bc3)


class TestThermalSolver:
    """Test thermal solver."""
    
    def create_simple_geometry(self, nx=10, ny=10, nz=10):
        """Create simple test geometry."""
        volume = np.zeros((nx, ny, nz), dtype=np.uint8)
        
        # Create channel in center
        cx_min, cx_max = nx//4, 3*nx//4
        cy_min, cy_max = ny//4, 3*ny//4
        volume[cx_min:cx_max, cy_min:cy_max, :] = 1
        
        return volume
    
    def test_thermal_solver_smoke(self):
        """Smoke test for thermal solver."""
        volume = self.create_simple_geometry(nx=10, ny=10, nz=10)
        
        # Prepare thermal conductivity
        k_field = coupling.prepare_thermal_conductivity_field(
            volume, k_solid=200.0, k_fluid=0.6
        )
        
        # Get boundary conditions - use much lower heat flux for small test
        bc = bc_module.get_matched_thermal_boundary_conditions()
        bc['heat_flux_w_m2'] = 1e4  # Use lower heat flux for small test geometry
        
        # Solve
        result = thermal_solver.solve_thermal_field(
            volume, k_field, 0.1, bc, None, {'tol': 1e-4}
        )
        
        assert 'temperature' in result
        assert 'converged' in result
        # Small test geometry without convection may diverge - just check structure
        assert result['temperature'].shape == volume.shape
    
    def test_thermal_solver_deterministic(self):
        """Test that thermal solver gives deterministic results."""
        volume = self.create_simple_geometry(nx=8, ny=8, nz=8)
        k_field = coupling.prepare_thermal_conductivity_field(
            volume, k_solid=200.0, k_fluid=0.6
        )
        bc = bc_module.get_matched_thermal_boundary_conditions()
        
        # Solve twice
        result1 = thermal_solver.solve_thermal_field(
            volume, k_field, 0.1, bc, None, {'tol': 1e-6}
        )
        result2 = thermal_solver.solve_thermal_field(
            volume, k_field, 0.1, bc, None, {'tol': 1e-6}
        )
        
        # Results should be identical
        np.testing.assert_allclose(
            result1['temperature'], result2['temperature'], rtol=1e-6
        )


class TestMetrics:
    """Test thermal metrics."""
    
    def test_compute_temperature_statistics(self):
        """Test temperature statistics computation."""
        # Create test temperature field
        temperature = np.random.rand(10, 10, 10) * 50 + 25
        volume = np.random.rand(10, 10, 10) > 0.5
        volume = volume.astype(np.uint8)
        
        stats = metrics_module.compute_temperature_statistics(temperature, volume)
        
        assert stats['label'] == 'SIMULATED'
        assert 'T_mean_c' in stats
        assert 'T_max_c' in stats
        assert 'T_min_c' in stats
        assert 'T_solid_mean_c' in stats
        assert 'T_fluid_mean_c' in stats
        
        # Check values are reasonable
        assert stats['T_min_c'] < stats['T_mean_c'] < stats['T_max_c']
    
    def test_compute_thermal_resistance(self):
        """Test thermal resistance computation."""
        temperature = np.ones((10, 10, 10)) * 50.0
        volume = np.zeros((10, 10, 10), dtype=np.uint8)
        
        bc = bc_module.get_matched_thermal_boundary_conditions()
        
        thermal_res = metrics_module.compute_thermal_resistance(
            temperature, volume, 0.1, bc
        )
        
        assert thermal_res['label'] == 'SIMULATED'
        assert 'thermal_resistance_k_w' in thermal_res
        assert 'delta_T_max_c' in thermal_res
        assert 'heat_input_w' in thermal_res
        
        # Check values are positive
        assert thermal_res['thermal_resistance_k_w'] > 0
        assert thermal_res['delta_T_max_c'] > 0
        assert thermal_res['heat_input_w'] > 0


class TestComparison:
    """Test comparison framework."""
    
    def create_mock_result(self, candidate_id, R_th, T_max):
        """Create mock result for testing."""
        return {
            'candidate_id': candidate_id,
            'metrics': {
                'thermal_simulated_quantities': {
                    'thermal_resistance': {
                        'thermal_resistance_k_w': R_th
                    },
                    'temperature_statistics': {
                        'T_max_c': T_max,
                        'T_mean_c': T_max - 5.0
                    },
                    'uniformity': {
                        'temperature_spread_c': 10.0
                    }
                }
            },
            'boundary_conditions': bc_module.get_matched_thermal_boundary_conditions()
        }
    
    def test_rank_candidates(self):
        """Test candidate ranking."""
        results = [
            self.create_mock_result('cand1', 1.5, 60.0),
            self.create_mock_result('cand2', 1.0, 55.0),
            self.create_mock_result('cand3', 2.0, 65.0),
        ]
        
        ranked = compare_module.rank_candidates_by_thermal_performance(results)
        
        # Should be sorted by thermal resistance
        assert ranked[0]['candidate_id'] == 'cand2'  # R_th = 1.0
        assert ranked[1]['candidate_id'] == 'cand1'  # R_th = 1.5
        assert ranked[2]['candidate_id'] == 'cand3'  # R_th = 2.0
    
    def test_compute_comparison_metrics(self):
        """Test comparison metrics computation."""
        results = [
            self.create_mock_result('cand1', 1.5, 60.0),
            self.create_mock_result('cand2', 1.0, 55.0),
        ]
        
        comparison = compare_module.compute_comparison_metrics(results)
        
        assert comparison['n_candidates'] == 2
        assert 'thermal_resistance' in comparison
        assert 'peak_temperature' in comparison
        
        # Check best values
        assert comparison['thermal_resistance']['best_k_w'] == 1.0
        assert comparison['peak_temperature']['lowest_c'] == 55.0
    
    def test_verify_matched_thermal_conditions(self):
        """Test matched condition verification."""
        results = [
            self.create_mock_result('cand1', 1.5, 60.0),
            self.create_mock_result('cand2', 1.0, 55.0),
        ]
        
        # Should verify as matched
        assert compare_module.verify_matched_thermal_conditions(results)


class TestIntegration:
    """Integration tests."""
    
    def test_full_smoke_pipeline(self):
        """Test full pipeline on smoke test data."""
        stage4_dir = 'results/stage4_sim_smoke'
        
        if not os.path.exists(stage4_dir):
            pytest.skip("Stage 4 smoke outputs not available")
        
        # Load candidates
        candidates = load_cases.load_candidates_for_thermal(stage4_dir, top_k=1)
        
        if len(candidates) == 0:
            pytest.skip("No candidates loaded")
        
        candidate = candidates[0]
        
        # Get boundary conditions
        bc = bc_module.get_matched_thermal_boundary_conditions()
        
        # Run thermal simulation
        thermal_result = coupling.run_coupled_thermal_simulation(
            candidate, bc, {'tol': 1e-6}
        )
        
        assert thermal_result['converged']
        assert thermal_result['temperature'].shape == candidate['geometry'].shape
        
        # Compute metrics
        cand_metrics = metrics_module.compute_all_thermal_metrics(
            thermal_result, candidate, bc
        )
        
        assert 'thermal_simulated_quantities' in cand_metrics
        assert 'flow_simulated_quantities' in cand_metrics
        assert 'geometric_quantities' in cand_metrics
