"""Tests for Stage 6 structural screening."""

import pytest
import os
import sys
import numpy as np
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage6_structural import (
    load_cases,
    material_models,
    manufacturability,
    screening,
    metrics as metrics_module,
    compare as compare_module
)


class TestLoadCases:
    """Test load case loading and definition."""
    
    def test_load_stage5_summary(self):
        """Test loading Stage 5 summary file."""
        stage5_dir = 'results/stage5_thermal_smoke'
        
        if not os.path.exists(stage5_dir):
            pytest.skip("Stage 5 smoke outputs not available")
        
        summary = load_cases.load_stage5_summary(stage5_dir)
        
        assert 'n_candidates' in summary
        assert 'candidates' in summary
        assert summary['n_candidates'] > 0
    
    def test_load_stage5_candidate(self):
        """Test loading a single Stage 5 candidate."""
        stage5_dir = 'results/stage5_thermal_smoke'
        
        if not os.path.exists(stage5_dir):
            pytest.skip("Stage 5 smoke outputs not available")
        
        summary = load_cases.load_stage5_summary(stage5_dir)
        candidate_id = summary['candidates'][0]['candidate_id']
        
        candidate = load_cases.load_stage5_candidate(stage5_dir, candidate_id)
        
        assert 'candidate_id' in candidate
        assert 'metrics' in candidate
        assert 'provenance' in candidate
        assert 'boundary_conditions' in candidate
    
    def test_define_pressure_load_case(self):
        """Test pressure load case definition."""
        bc = {'inlet_pressure_pa': 102325.0}
        load_case = load_cases.define_pressure_load_case(1000.0, bc)
        
        assert load_case['type'] == 'internal_pressure'
        assert load_case['pressure_pa'] == 102325.0
        assert load_case['label'] == 'ANALYTICAL'
    
    def test_define_thermal_load_case(self):
        """Test thermal load case definition."""
        bc = {'ambient_temperature_c': 25.0}
        load_case = load_cases.define_thermal_load_case(50.0, 25.0, bc)
        
        assert load_case['type'] == 'thermal_expansion'
        assert load_case['delta_T_c'] == 25.0
        assert load_case['label'] == 'ANALYTICAL'


class TestMaterialModels:
    """Test material property definitions."""
    
    def test_get_aluminum_6061_properties(self):
        """Test aluminum 6061 material properties."""
        props = material_models.get_aluminum_6061_properties()
        
        assert props['name'] == 'Aluminum 6061-T6'
        assert props['E_gpa'] > 0
        assert props['yield_strength_mpa'] > 0
        assert props['label'] == 'LITERATURE'
        assert 'safety_factor' in props
    
    def test_get_material_properties(self):
        """Test material lookup by name."""
        props = material_models.get_material_properties('aluminum_6061')
        
        assert props['name'] == 'Aluminum 6061-T6'
    
    def test_compute_thermal_stress_coefficient(self):
        """Test thermal stress coefficient computation."""
        material = material_models.get_aluminum_6061_properties()
        coeff = material_models.compute_thermal_stress_coefficient(material)
        
        assert coeff > 0
        assert isinstance(coeff, float)


class TestManufacturability:
    """Test manufacturability checks."""
    
    def setup_method(self):
        """Create test geometry."""
        # Create simple test volume with known characteristics
        nx, ny, nz = 20, 20, 20
        self.volume = np.zeros((nx, ny, nz), dtype=bool)
        
        # Create channels (fluid regions)
        self.volume[5:15, 5:15, :] = True  # Vertical channel
        self.voxel_size_mm = 0.25
    
    def test_check_minimum_wall_thickness(self):
        """Test wall thickness check."""
        result = manufacturability.check_minimum_wall_thickness(
            self.volume, self.voxel_size_mm, min_thickness_mm=0.5
        )
        
        assert 'min_wall_thickness_mm' in result
        assert 'passes' in result
        assert result['label'] == 'GEOMETRIC'
        assert isinstance(result['passes'], bool)
    
    def test_check_minimum_feature_size(self):
        """Test feature size check."""
        result = manufacturability.check_minimum_feature_size(
            self.volume, self.voxel_size_mm, min_feature_mm=0.5
        )
        
        assert 'min_channel_diameter_mm' in result
        assert 'passes' in result
        assert result['label'] == 'GEOMETRIC'
    
    def test_check_trapped_volumes(self):
        """Test trapped volume detection."""
        result = manufacturability.check_trapped_volumes(
            self.volume, self.voxel_size_mm
        )
        
        assert 'num_fluid_components' in result
        assert 'has_trapped_volumes' in result
        assert result['label'] == 'GEOMETRIC'
    
    def test_run_all_manufacturability_checks(self):
        """Test running all manufacturability checks."""
        requirements = {
            'min_wall_thickness_mm': 0.5,
            'min_feature_size_mm': 0.5,
            'max_unsupported_mm': 10.0
        }
        
        result = manufacturability.run_all_manufacturability_checks(
            self.volume, self.voxel_size_mm, requirements
        )
        
        assert 'wall_thickness' in result
        assert 'feature_size' in result
        assert 'overall_pass' in result
        assert result['label'] == 'MANUFACTURABILITY_SCREENED'


class TestScreening:
    """Test structural screening."""
    
    def setup_method(self):
        """Set up test data."""
        self.material = material_models.get_aluminum_6061_properties()
        self.geometry_info = {
            'domain_size_mm': [5.0, 5.0, 5.0],
            'min_wall_thickness_mm': 0.5,
            'porosity': 0.5
        }
    
    def test_estimate_pressure_stress(self):
        """Test pressure stress estimation."""
        result = screening.estimate_pressure_stress(
            100000.0, self.geometry_info, self.material
        )
        
        assert 'sigma_max_mpa' in result
        assert 'margin_of_safety' in result
        assert 'passes' in result
        assert result['label'] == 'ANALYTICAL'
    
    def test_estimate_thermal_stress(self):
        """Test thermal stress estimation."""
        result = screening.estimate_thermal_stress(
            25.0, self.geometry_info, self.material
        )
        
        assert 'sigma_thermal_effective_mpa' in result
        assert 'margin_of_safety' in result
        assert 'passes' in result
        assert result['label'] == 'ANALYTICAL'
    
    def test_estimate_deflection(self):
        """Test deflection estimation."""
        result = screening.estimate_deflection(
            100000.0, self.geometry_info, self.material
        )
        
        assert 'deflection_mm' in result
        assert 'passes' in result
        assert result['label'] == 'ANALYTICAL'
    
    def test_run_structural_screening(self):
        """Test complete structural screening."""
        pressure_load = {
            'type': 'internal_pressure',
            'pressure_pa': 102325.0,
            'label': 'ANALYTICAL'
        }
        thermal_load = {
            'type': 'thermal_expansion',
            'delta_T_c': 25.0,
            'label': 'ANALYTICAL'
        }
        
        result = screening.run_structural_screening(
            pressure_load, thermal_load, self.geometry_info, self.material
        )
        
        assert 'pressure_stress' in result
        assert 'thermal_stress' in result
        assert 'deflection' in result
        assert 'combined_stress' in result
        assert 'overall_pass' in result
        assert result['label'] == 'STRUCTURAL_SCREENED'


class TestCompare:
    """Test comparison logic."""
    
    def setup_method(self):
        """Create test candidate metrics."""
        self.candidates_metrics = [
            {
                'candidate_id': 'test_candidate_01',
                'stage6_verdict': {
                    'overall_pass': True,
                    'structural_pass': True,
                    'manufacturability_pass': True,
                    'all_failure_modes': []
                },
                'structural_screened_quantities': {
                    'combined_stress': {
                        'sigma_combined_mpa': 50.0,
                        'margin_of_safety': 0.8
                    }
                },
                'thermal_simulated_quantities': {
                    'thermal_resistance': {'thermal_resistance_k_w': 1.03},
                    'temperature_statistics': {'T_max_c': 50.5}
                },
                'flow_simulated_quantities': {
                    'pressure_drop': {'pressure_drop_pa': 1000.0}
                },
                'material_properties': {
                    'material_name': 'Aluminum 6061-T6',
                    'safety_factor': 3.0
                }
            }
        ]
    
    def test_verify_matched_conditions(self):
        """Test matched conditions verification."""
        result = compare_module.verify_matched_conditions(self.candidates_metrics)
        
        assert 'matched' in result
        assert 'issues' in result
        assert isinstance(result['matched'], bool)
    
    def test_rank_candidates_by_combined_performance(self):
        """Test candidate ranking."""
        ranked = compare_module.rank_candidates_by_combined_performance(
            self.candidates_metrics
        )
        
        assert len(ranked) == 1
        assert 'rank' in ranked[0]
        assert 'composite_score' in ranked[0]
        assert ranked[0]['rank'] == 1
    
    def test_generate_comparison_summary(self):
        """Test comparison summary generation."""
        ranked = compare_module.rank_candidates_by_combined_performance(
            self.candidates_metrics
        )
        summary = compare_module.generate_comparison_summary(
            self.candidates_metrics, ranked
        )
        
        assert 'n_candidates' in summary
        assert 'n_pass_overall' in summary
        assert 'best_candidate' in summary
        assert 'ranking' in summary


class TestDeterminism:
    """Test deterministic behavior."""
    
    def test_material_properties_deterministic(self):
        """Test that material properties are deterministic."""
        props1 = material_models.get_aluminum_6061_properties()
        props2 = material_models.get_aluminum_6061_properties()
        
        assert props1['E_gpa'] == props2['E_gpa']
        assert props1['yield_strength_mpa'] == props2['yield_strength_mpa']
    
    def test_stress_calculation_deterministic(self):
        """Test that stress calculations are deterministic."""
        material = material_models.get_aluminum_6061_properties()
        geometry_info = {
            'domain_size_mm': [5.0, 5.0, 5.0],
            'min_wall_thickness_mm': 0.5,
            'porosity': 0.5
        }
        
        result1 = screening.estimate_pressure_stress(
            100000.0, geometry_info, material
        )
        result2 = screening.estimate_pressure_stress(
            100000.0, geometry_info, material
        )
        
        assert result1['sigma_max_mpa'] == result2['sigma_max_mpa']


class TestErrorHandling:
    """Test error handling."""
    
    def test_load_nonexistent_directory(self):
        """Test loading from nonexistent directory."""
        with pytest.raises(FileNotFoundError):
            load_cases.load_stage5_summary('/nonexistent/path')
    
    def test_unknown_material(self):
        """Test requesting unknown material."""
        with pytest.raises(ValueError):
            material_models.get_material_properties('unknown_material')


class TestSchemaStability:
    """Test output schema stability."""
    
    def test_structural_screening_schema(self):
        """Test structural screening output schema."""
        material = material_models.get_aluminum_6061_properties()
        geometry_info = {
            'domain_size_mm': [5.0, 5.0, 5.0],
            'min_wall_thickness_mm': 0.5,
            'porosity': 0.5
        }
        pressure_load = {
            'type': 'internal_pressure',
            'pressure_pa': 102325.0,
            'label': 'ANALYTICAL'
        }
        thermal_load = {
            'type': 'thermal_expansion',
            'delta_T_c': 25.0,
            'label': 'ANALYTICAL'
        }
        
        result = screening.run_structural_screening(
            pressure_load, thermal_load, geometry_info, material
        )
        
        # Check required keys
        required_keys = [
            'pressure_stress',
            'thermal_stress',
            'deflection',
            'combined_stress',
            'overall_pass',
            'failure_modes',
            'label'
        ]
        
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"
    
    def test_manufacturability_schema(self):
        """Test manufacturability output schema."""
        volume = np.random.random((20, 20, 20)) < 0.5
        requirements = {
            'min_wall_thickness_mm': 0.5,
            'min_feature_size_mm': 0.5,
            'max_unsupported_mm': 10.0
        }
        
        result = manufacturability.run_all_manufacturability_checks(
            volume, 0.25, requirements
        )
        
        # Check required keys
        required_keys = [
            'wall_thickness',
            'feature_size',
            'unsupported_regions',
            'trapped_volumes',
            'overall_pass',
            'failure_modes',
            'label'
        ]
        
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"


class TestSmokeRun:
    """Test smoke run if data available."""
    
    def test_smoke_run_if_available(self):
        """Test running smoke test if Stage 5 data exists."""
        stage5_dir = 'results/stage5_thermal_smoke'
        
        if not os.path.exists(stage5_dir):
            pytest.skip("Stage 5 smoke outputs not available")
        
        # Just test that we can load and process one candidate
        candidates = load_cases.load_candidates_for_structural(stage5_dir, top_k=1)
        
        assert len(candidates) > 0
        
        candidate = candidates[0]
        assert 'candidate_id' in candidate
        assert 'metrics' in candidate
