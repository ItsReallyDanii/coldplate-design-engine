"""Tests for Stage 4 geometry loading."""

import pytest
import tempfile
import os
import sys
import json
import numpy as np
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage4_sim import load_geometry


class TestGeometryLoading:
    """Test loading Stage 3 outputs."""
    
    def create_mock_stage3_output(self, tmpdir):
        """Create mock Stage 3 output structure."""
        stage3_dir = Path(tmpdir) / "stage3_test"
        stage3_dir.mkdir()
        
        # Create summary.json
        summary = {
            'provenance_records': [
                {
                    'timestamp': '2026-03-06T10:00:00+00:00',
                    'stage': 'stage3_geometry',
                    'schema_version': '1.0',
                    'stage2_source': {
                        'rank': 1,
                        'family': 'diamond_2d',
                        'seed': 1001,
                        'mask_id': 'diamond_2d_s1001_eval1',
                        'total_score': 2000.0,
                        'is_valid': True,
                        'params': {'threshold': -0.15, 'wavelength_px': 15.5},
                        'metrics': {
                            'porosity': 0.65,
                            'heat_exchange_area_proxy': 2000.0,
                            'hydraulic_resistance_proxy': 0.5,
                            'flow_connectivity_score': 1.0,
                            'dead_zone_fraction': 0.0
                        }
                    },
                    'promotion': {
                        'volume_metadata': {
                            'type': '3d_diamond_tpms',
                            'threshold': -0.15,
                            'wavelength_px': 15.5,
                            'porosity': 0.60,
                            'height_mm': 2.0,
                            'resolution': 20,
                            'dimensions': {'nx': 20, 'ny': 20, 'nz': 20}
                        },
                        'success': True,
                        'errors': []
                    },
                    'validation': {
                        'porosity': 0.60,
                        'connectivity': {'is_connected': True}
                    },
                    'exports': {
                        'stl': str(stage3_dir / 'candidate_01_diamond_2d_s1001/geometry/geometry.stl'),
                        'raw': str(stage3_dir / 'candidate_01_diamond_2d_s1001/geometry/volume.npy')
                    }
                },
                {
                    'timestamp': '2026-03-06T10:01:00+00:00',
                    'stage': 'stage3_geometry',
                    'schema_version': '1.0',
                    'stage2_source': {
                        'rank': 2,
                        'family': 'gyroid_2d',
                        'seed': 1002,
                        'mask_id': 'gyroid_2d_s1002_eval2',
                        'total_score': 1900.0,
                        'is_valid': True,
                        'params': {'threshold': -0.10, 'wavelength_px': 16.0},
                        'metrics': {
                            'porosity': 0.70,
                            'heat_exchange_area_proxy': 1900.0,
                            'hydraulic_resistance_proxy': 0.45,
                            'flow_connectivity_score': 1.0,
                            'dead_zone_fraction': 0.0
                        }
                    },
                    'promotion': {
                        'volume_metadata': {
                            'type': '3d_gyroid_tpms',
                            'threshold': -0.10,
                            'wavelength_px': 16.0,
                            'porosity': 0.65,
                            'height_mm': 2.0,
                            'resolution': 20,
                            'dimensions': {'nx': 20, 'ny': 20, 'nz': 20}
                        },
                        'success': True,
                        'errors': []
                    },
                    'validation': {
                        'porosity': 0.65,
                        'connectivity': {'is_connected': True}
                    },
                    'exports': {
                        'stl': str(stage3_dir / 'candidate_02_gyroid_2d_s1002/geometry/geometry.stl'),
                        'raw': str(stage3_dir / 'candidate_02_gyroid_2d_s1002/geometry/volume.npy')
                    }
                }
            ]
        }
        
        with open(stage3_dir / 'summary.json', 'w') as f:
            json.dump(summary, f)
        
        # Create candidate directories and volume files
        for i, prov in enumerate(summary['provenance_records']):
            candidate_dir = Path(prov['exports']['raw']).parent.parent
            candidate_dir.mkdir(parents=True, exist_ok=True)
            geometry_dir = candidate_dir / 'geometry'
            geometry_dir.mkdir(parents=True, exist_ok=True)
            
            # Create mock volume (20x20x20 with ~60% porosity)
            volume = np.random.rand(20, 20, 20) < 0.6
            volume = volume.astype(np.uint8)
            np.save(geometry_dir / 'volume.npy', volume)
            
            # Create provenance.json
            with open(candidate_dir / 'provenance.json', 'w') as f:
                json.dump(prov, f)
        
        return stage3_dir
    
    def test_load_stage3_summary(self, tmpdir):
        """Test loading Stage 3 summary file."""
        stage3_dir = self.create_mock_stage3_output(tmpdir)
        
        summary = load_geometry.load_stage3_summary(stage3_dir)
        
        assert 'provenance_records' in summary
        assert len(summary['provenance_records']) == 2
    
    def test_load_stage3_summary_missing(self, tmpdir):
        """Test error when summary.json is missing."""
        stage3_dir = Path(tmpdir) / "empty"
        stage3_dir.mkdir()
        
        with pytest.raises(FileNotFoundError):
            load_geometry.load_stage3_summary(stage3_dir)
    
    def test_select_top_k_candidates(self, tmpdir):
        """Test selecting top k candidates."""
        stage3_dir = self.create_mock_stage3_output(tmpdir)
        summary = load_geometry.load_stage3_summary(stage3_dir)
        
        top_1 = load_geometry.select_top_k_candidates(summary, k=1)
        assert len(top_1) == 1
        assert top_1[0]['stage2_source']['rank'] == 1
        
        top_2 = load_geometry.select_top_k_candidates(summary, k=2)
        assert len(top_2) == 2
    
    def test_load_candidate_geometry(self, tmpdir):
        """Test loading a single candidate's geometry."""
        stage3_dir = self.create_mock_stage3_output(tmpdir)
        
        candidate_dir = stage3_dir / 'candidate_01_diamond_2d_s1001'
        
        candidate = load_geometry.load_candidate_geometry(candidate_dir)
        
        assert 'volume' in candidate
        assert 'provenance' in candidate
        assert 'metadata' in candidate
        assert isinstance(candidate['volume'], np.ndarray)
        assert candidate['volume'].shape == (20, 20, 20)
    
    def test_load_candidates_for_simulation(self, tmpdir):
        """Test loading all candidates for simulation."""
        stage3_dir = self.create_mock_stage3_output(tmpdir)
        
        # Load all
        candidates = load_geometry.load_candidates_for_simulation(stage3_dir)
        assert len(candidates) == 2
        
        # Load top 1
        candidates = load_geometry.load_candidates_for_simulation(stage3_dir, top_k=1)
        assert len(candidates) == 1
    
    def test_get_candidate_identifier(self, tmpdir):
        """Test getting candidate identifier."""
        stage3_dir = self.create_mock_stage3_output(tmpdir)
        candidates = load_geometry.load_candidates_for_simulation(stage3_dir, top_k=1)
        
        candidate_id = load_geometry.get_candidate_identifier(candidates[0])
        assert candidate_id == 'candidate_01_diamond_2d_s1001'
    
    def test_get_candidate_score(self, tmpdir):
        """Test getting candidate score."""
        stage3_dir = self.create_mock_stage3_output(tmpdir)
        candidates = load_geometry.load_candidates_for_simulation(stage3_dir, top_k=1)
        
        score = load_geometry.get_candidate_score(candidates[0])
        assert score == 2000.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
