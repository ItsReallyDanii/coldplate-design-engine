"""Tests for Stage 3 I/O and candidate loading."""

import pytest
import tempfile
import os
import sys
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage3_geometry import io


class TestCandidateLoading:
    """Test loading Stage 2 candidates."""
    
    def create_mock_csv(self, filepath, num_candidates=5):
        """Create mock best_candidates.csv."""
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'rank', 'method', 'family', 'total_score', 'total_objective',
                'total_penalty', 'is_valid', 'evaluation_num', 'seed', 'mask_id',
                'param_threshold', 'param_wavelength_px',
                'porosity', 'heat_exchange_area_proxy',
                'hydraulic_resistance_proxy', 'flow_connectivity_score',
                'dead_zone_fraction'
            ])
            
            # Data rows
            for i in range(num_candidates):
                writer.writerow([
                    i + 1, 'combined', 'diamond_2d', 2000 - i*100, 2000 - i*100,
                    0.0, 'True', i, 1000 + i, f'diamond_2d_s{1000+i}_eval{i}',
                    -0.15, 15.5,
                    0.65, 2000 - i*100, 0.5, 1.0, 0.0
                ])
    
    def test_load_candidates(self, tmp_path):
        """Test loading candidates from CSV."""
        csv_path = tmp_path / "test_candidates.csv"
        self.create_mock_csv(csv_path, num_candidates=5)
        
        candidates = io.load_stage2_candidates(str(csv_path))
        
        assert len(candidates) == 5
        assert candidates[0]['rank'] == 1
        assert candidates[0]['family'] == 'diamond_2d'
        assert candidates[0]['seed'] == 1000
        assert 'params' in candidates[0]
        assert 'threshold' in candidates[0]['params']
        assert 'metrics' in candidates[0]
    
    def test_select_top_k(self, tmp_path):
        """Test top-k selection."""
        csv_path = tmp_path / "test_candidates.csv"
        self.create_mock_csv(csv_path, num_candidates=10)
        
        candidates = io.load_stage2_candidates(str(csv_path))
        selected = io.select_top_k_candidates(candidates, k=3)
        
        assert len(selected) == 3
        assert selected[0]['rank'] == 1
        assert selected[1]['rank'] == 2
        assert selected[2]['rank'] == 3
    
    def test_select_top_k_with_family_filter(self, tmp_path):
        """Test top-k selection with family filter."""
        csv_path = tmp_path / "test_candidates.csv"
        
        # Create mixed families
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'rank', 'method', 'family', 'total_score', 'total_objective',
                'total_penalty', 'is_valid', 'evaluation_num', 'seed', 'mask_id',
                'param_threshold', 'param_wavelength_px',
                'porosity', 'heat_exchange_area_proxy',
                'hydraulic_resistance_proxy', 'flow_connectivity_score',
                'dead_zone_fraction'
            ])
            
            writer.writerow([1, 'combined', 'diamond_2d', 2000, 2000, 0.0, 'True', 0, 1000, 'id1', -0.15, 15.5, 0.65, 2000, 0.5, 1.0, 0.0])
            writer.writerow([2, 'combined', 'primitive_2d', 1900, 1900, 0.0, 'True', 1, 1001, 'id2', -0.15, 15.5, 0.65, 1900, 0.5, 1.0, 0.0])
            writer.writerow([3, 'combined', 'diamond_2d', 1800, 1800, 0.0, 'True', 2, 1002, 'id3', -0.15, 15.5, 0.65, 1800, 0.5, 1.0, 0.0])
        
        candidates = io.load_stage2_candidates(str(csv_path))
        selected = io.select_top_k_candidates(candidates, k=5, family_filter='diamond_2d')
        
        assert len(selected) == 2
        assert all(c['family'] == 'diamond_2d' for c in selected)
    
    def test_create_candidate_output_dir(self, tmp_path):
        """Test creating candidate output directory."""
        base_dir = str(tmp_path / "output")
        
        cand_dir = io.create_candidate_output_dir(base_dir, rank=1, family='diamond_2d', seed=1000)
        
        assert os.path.exists(cand_dir)
        assert os.path.exists(os.path.join(cand_dir, 'geometry'))
        assert os.path.exists(os.path.join(cand_dir, 'validation'))
