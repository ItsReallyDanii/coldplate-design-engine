"""Tests for Stage 4 solver and simulation."""

import pytest
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stage4_sim import mesh_or_grid, solver, boundary_conditions


class TestSolver:
    """Test flow solver."""
    
    def create_simple_channel(self, nx=10, ny=10, nz=20):
        """Create simple straight channel for testing."""
        volume = np.zeros((nx, ny, nz), dtype=np.uint8)
        
        # Create channel in center
        cx_min, cx_max = nx//4, 3*nx//4
        cy_min, cy_max = ny//4, 3*ny//4
        volume[cx_min:cx_max, cy_min:cy_max, :] = 1
        
        return volume
    
    def test_solver_smoke(self):
        """Smoke test for solver on simple geometry."""
        # Create simple channel
        volume = self.create_simple_channel(nx=10, ny=10, nz=20)
        
        # Setup grid
        grid = mesh_or_grid.setup_simulation_grid(volume, voxel_size_mm=0.1)
        
        assert grid['shape'] == (10, 10, 20)
        assert grid['porosity'] > 0.0
        
        # Setup boundary conditions
        bc = boundary_conditions.get_matched_boundary_conditions()
        
        # Run simulation
        result = solver.run_flow_simulation(grid, bc, solver_params={'tol': 1e-4, 'max_iter': 1000})
        
        # Check result structure
        assert 'pressure' in result
        assert 'velocity' in result
        assert 'converged' in result
        assert result['converged'] is True
        
        # Check pressure field shape
        assert result['pressure'].shape == (10, 10, 20)
        
        # Check velocity components
        assert 'vx' in result['velocity']
        assert 'vy' in result['velocity']
        assert 'vz' in result['velocity']
        
        # Check pressure gradient exists (not all zeros)
        assert np.std(result['pressure']) > 0.0
    
    def test_solver_deterministic(self):
        """Test that solver gives deterministic results."""
        volume = self.create_simple_channel(nx=8, ny=8, nz=16)
        grid = mesh_or_grid.setup_simulation_grid(volume, voxel_size_mm=0.1)
        bc = boundary_conditions.get_matched_boundary_conditions()
        
        # Run twice
        result1 = solver.run_flow_simulation(grid, bc, solver_params={'tol': 1e-5, 'max_iter': 1000})
        result2 = solver.run_flow_simulation(grid, bc, solver_params={'tol': 1e-5, 'max_iter': 1000})
        
        # Results should be identical (or very close)
        np.testing.assert_allclose(result1['pressure'], result2['pressure'], rtol=1e-6)
    
    def test_pressure_drop_positive(self):
        """Test that pressure drop is positive (inlet > outlet)."""
        volume = self.create_simple_channel(nx=10, ny=10, nz=20)
        grid = mesh_or_grid.setup_simulation_grid(volume, voxel_size_mm=0.1)
        bc = boundary_conditions.get_matched_boundary_conditions()
        
        result = solver.run_flow_simulation(grid, bc, solver_params={'tol': 1e-4, 'max_iter': 1000})
        
        # Get inlet/outlet masks
        faces = mesh_or_grid.get_inlet_outlet_faces(grid['shape'])
        
        p_inlet = np.mean(result['pressure'][faces['inlet_mask']])
        p_outlet = np.mean(result['pressure'][faces['outlet_mask']])
        
        # Inlet pressure should be higher than outlet
        assert p_inlet > p_outlet
    
    def test_velocity_field_computation(self):
        """Test velocity field computation from pressure."""
        volume = self.create_simple_channel(nx=10, ny=10, nz=20)
        grid = mesh_or_grid.setup_simulation_grid(volume, voxel_size_mm=0.1)
        bc = boundary_conditions.get_matched_boundary_conditions()
        
        result = solver.run_flow_simulation(grid, bc, solver_params={'tol': 1e-4, 'max_iter': 1000})
        
        velocity = result['velocity']
        
        # Primary flow should be in z-direction
        vz_mean = np.mean(np.abs(velocity['vz'][grid['fluid_mask']]))
        vx_mean = np.mean(np.abs(velocity['vx'][grid['fluid_mask']]))
        vy_mean = np.mean(np.abs(velocity['vy'][grid['fluid_mask']]))
        
        # vz should dominate
        assert vz_mean > vx_mean
        assert vz_mean > vy_mean


class TestGridSetup:
    """Test grid setup functions."""
    
    def test_setup_simulation_grid(self):
        """Test grid setup from volume."""
        volume = np.ones((10, 10, 10), dtype=np.uint8)
        volume[5:, :, :] = 0  # Half fluid, half solid
        
        grid = mesh_or_grid.setup_simulation_grid(volume, voxel_size_mm=0.1)
        
        assert grid['shape'] == (10, 10, 10)
        assert grid['voxel_size_mm'] == 0.1
        assert abs(grid['porosity'] - 0.5) < 0.01  # Should be ~50%
        assert grid['domain_size_mm'] == (1.0, 1.0, 1.0)
    
    def test_inlet_outlet_faces(self):
        """Test inlet/outlet face definition."""
        shape = (10, 10, 20)
        faces = mesh_or_grid.get_inlet_outlet_faces(shape)
        
        # Check inlet face (z=0)
        assert faces['inlet_mask'][:, :, 0].all()
        assert not faces['inlet_mask'][:, :, 1:].any()
        
        # Check outlet face (z=-1)
        assert faces['outlet_mask'][:, :, -1].all()
        assert not faces['outlet_mask'][:, :, :-1].any()
    
    def test_permeability_field(self):
        """Test permeability field computation."""
        fluid_mask = np.ones((5, 5, 5), dtype=bool)
        fluid_mask[2:, :, :] = False  # Half solid
        
        k = mesh_or_grid.compute_permeability_field(
            fluid_mask,
            k_fluid=1e-6,
            k_solid=1e-12
        )
        
        # Check fluid region has high permeability
        assert np.all(k[fluid_mask] == 1e-6)
        
        # Check solid region has low permeability
        assert np.all(k[~fluid_mask] == 1e-12)


class TestBoundaryConditions:
    """Test boundary condition setup."""
    
    def test_matched_boundary_conditions(self):
        """Test that matched BCs are consistent."""
        bc1 = boundary_conditions.get_matched_boundary_conditions()
        bc2 = boundary_conditions.get_matched_boundary_conditions()
        
        # Should be identical
        assert bc1 == bc2
        
        # Check required fields
        assert 'inlet_pressure_pa' in bc1
        assert 'outlet_pressure_pa' in bc1
        assert 'pressure_drop_pa' in bc1
        assert 'fluid_viscosity_pa_s' in bc1
        assert bc1['matched_conditions'] is True
    
    def test_pressure_drop_consistency(self):
        """Test pressure drop consistency."""
        bc = boundary_conditions.get_matched_boundary_conditions()
        
        computed_dp = bc['inlet_pressure_pa'] - bc['outlet_pressure_pa']
        
        assert abs(computed_dp - bc['pressure_drop_pa']) < 1e-6


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
