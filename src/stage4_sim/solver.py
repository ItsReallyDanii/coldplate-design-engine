"""
Flow solver for Stage 4 simulation.

Implements a simplified steady-state incompressible flow solver using:
- Pressure Poisson equation with Darcy-like resistance
- Finite-difference discretization on voxel grid
- Iterative solution (Jacobi or conjugate gradient)

This is an HONEST, SIMPLIFIED solver suitable for:
- Comparative pressure drop estimation
- Flow distribution analysis
- Relative performance ranking

This is NOT:
- A full Navier-Stokes CFD solver
- Validated for absolute quantitative predictions
- Including turbulence, compressibility, or thermal coupling
"""

import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg
from typing import Dict, Any, Tuple, Optional
import time


def build_pressure_poisson_operator(
    fluid_mask: np.ndarray,
    permeability: np.ndarray,
    voxel_size_mm: float,
    inlet_mask: np.ndarray,
    outlet_mask: np.ndarray
) -> Tuple[sparse.csr_matrix, np.ndarray]:
    """
    Build sparse linear operator for pressure Poisson equation.
    
    Solves: ∇·(k ∇p) = 0 (incompressible steady flow)
    where k is permeability field
    
    Args:
        fluid_mask: Boolean array (True=fluid, False=solid)
        permeability: Permeability field (m^2)
        voxel_size_mm: Physical voxel size in mm
        inlet_mask: Inlet boundary mask
        outlet_mask: Outlet boundary mask
        
    Returns:
        (A, rhs) where A @ p_flat = rhs
        A: Sparse matrix operator
        rhs: Right-hand side vector (modified for BCs)
    """
    nx, ny, nz = fluid_mask.shape
    n_total = nx * ny * nz
    
    # Convert voxel size to meters
    dx = voxel_size_mm / 1000.0
    
    # Flatten arrays
    flat_mask = fluid_mask.ravel()
    flat_perm = permeability.ravel()
    flat_inlet = inlet_mask.ravel()
    flat_outlet = outlet_mask.ravel()
    
    # Build sparse matrix using COO format
    rows = []
    cols = []
    data = []
    
    # Right-hand side
    rhs = np.zeros(n_total)
    
    # Helper to convert 3D indices to flat index
    def idx(i, j, k):
        return i + j * nx + k * nx * ny
    
    # Build finite-difference stencil for each cell
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                flat_i = idx(i, j, k)
                
                # If inlet or outlet, use Dirichlet BC
                if flat_inlet[flat_i] or flat_outlet[flat_i]:
                    # Identity: p[flat_i] = boundary value
                    rows.append(flat_i)
                    cols.append(flat_i)
                    data.append(1.0)
                    # RHS will be set later based on BC values
                    continue
                
                # Central cell coefficient
                center_coeff = 0.0
                
                # x-direction neighbors
                if i > 0:
                    neighbor_i = idx(i-1, j, k)
                    k_face = 0.5 * (flat_perm[flat_i] + flat_perm[neighbor_i])
                    coeff = k_face / (dx * dx)
                    rows.append(flat_i)
                    cols.append(neighbor_i)
                    data.append(coeff)
                    center_coeff -= coeff
                
                if i < nx - 1:
                    neighbor_i = idx(i+1, j, k)
                    k_face = 0.5 * (flat_perm[flat_i] + flat_perm[neighbor_i])
                    coeff = k_face / (dx * dx)
                    rows.append(flat_i)
                    cols.append(neighbor_i)
                    data.append(coeff)
                    center_coeff -= coeff
                
                # y-direction neighbors
                if j > 0:
                    neighbor_i = idx(i, j-1, k)
                    k_face = 0.5 * (flat_perm[flat_i] + flat_perm[neighbor_i])
                    coeff = k_face / (dx * dx)
                    rows.append(flat_i)
                    cols.append(neighbor_i)
                    data.append(coeff)
                    center_coeff -= coeff
                
                if j < ny - 1:
                    neighbor_i = idx(i, j+1, k)
                    k_face = 0.5 * (flat_perm[flat_i] + flat_perm[neighbor_i])
                    coeff = k_face / (dx * dx)
                    rows.append(flat_i)
                    cols.append(neighbor_i)
                    data.append(coeff)
                    center_coeff -= coeff
                
                # z-direction neighbors
                if k > 0:
                    neighbor_i = idx(i, j, k-1)
                    k_face = 0.5 * (flat_perm[flat_i] + flat_perm[neighbor_i])
                    coeff = k_face / (dx * dx)
                    rows.append(flat_i)
                    cols.append(neighbor_i)
                    data.append(coeff)
                    center_coeff -= coeff
                
                if k < nz - 1:
                    neighbor_i = idx(i, j, k+1)
                    k_face = 0.5 * (flat_perm[flat_i] + flat_perm[neighbor_i])
                    coeff = k_face / (dx * dx)
                    rows.append(flat_i)
                    cols.append(neighbor_i)
                    data.append(coeff)
                    center_coeff -= coeff
                
                # Add center coefficient
                rows.append(flat_i)
                cols.append(flat_i)
                data.append(center_coeff)
    
    # Build sparse matrix
    A = sparse.coo_matrix((data, (rows, cols)), shape=(n_total, n_total))
    A = A.tocsr()
    
    return A, rhs


def solve_pressure_field(
    A: sparse.csr_matrix,
    rhs: np.ndarray,
    inlet_mask: np.ndarray,
    outlet_mask: np.ndarray,
    inlet_pressure_pa: float,
    outlet_pressure_pa: float,
    shape: Tuple[int, int, int],
    tol: float = 1e-6,
    max_iter: int = 10000
) -> Dict[str, Any]:
    """
    Solve pressure field using iterative solver.
    
    Args:
        A: Sparse matrix operator
        rhs: Right-hand side vector
        inlet_mask: Inlet boundary mask
        outlet_mask: Outlet boundary mask
        inlet_pressure_pa: Inlet pressure
        outlet_pressure_pa: Outlet pressure
        shape: Grid dimensions
        tol: Convergence tolerance
        max_iter: Maximum iterations
        
    Returns:
        Dictionary with pressure field and convergence info
    """
    # Apply boundary conditions to RHS
    flat_inlet = inlet_mask.ravel()
    flat_outlet = outlet_mask.ravel()
    
    rhs_bc = rhs.copy()
    rhs_bc[flat_inlet] = inlet_pressure_pa
    rhs_bc[flat_outlet] = outlet_pressure_pa
    
    # Solve using direct solver (more robust for small problems)
    start_time = time.time()
    
    try:
        p_flat = splinalg.spsolve(A, rhs_bc)
        converged = True
        iterations = 1
    except Exception as e:
        raise RuntimeError(f"Solver failed: {e}")
    
    solve_time = time.time() - start_time
    
    # Reshape to 3D
    pressure = p_flat.reshape(shape)
    
    return {
        'pressure': pressure,
        'converged': converged,
        'iterations': iterations,
        'solve_time_s': solve_time,
        'tolerance': tol
    }


def compute_velocity_field(
    pressure: np.ndarray,
    permeability: np.ndarray,
    voxel_size_mm: float,
    fluid_viscosity_pa_s: float
) -> Dict[str, np.ndarray]:
    """
    Compute velocity field from pressure gradient using Darcy's law.
    
    v = -(k/μ) ∇p
    
    Args:
        pressure: Pressure field (Pa)
        permeability: Permeability field (m^2)
        voxel_size_mm: Physical voxel size in mm
        fluid_viscosity_pa_s: Fluid dynamic viscosity (Pa·s)
        
    Returns:
        Dictionary with velocity components (vx, vy, vz) in m/s
    """
    # Convert voxel size to meters
    dx = voxel_size_mm / 1000.0
    
    # Compute pressure gradients using central differences
    grad_px = np.zeros_like(pressure)
    grad_py = np.zeros_like(pressure)
    grad_pz = np.zeros_like(pressure)
    
    # x-direction
    grad_px[1:-1, :, :] = (pressure[2:, :, :] - pressure[:-2, :, :]) / (2 * dx)
    grad_px[0, :, :] = (pressure[1, :, :] - pressure[0, :, :]) / dx
    grad_px[-1, :, :] = (pressure[-1, :, :] - pressure[-2, :, :]) / dx
    
    # y-direction
    grad_py[:, 1:-1, :] = (pressure[:, 2:, :] - pressure[:, :-2, :]) / (2 * dx)
    grad_py[:, 0, :] = (pressure[:, 1, :] - pressure[:, 0, :]) / dx
    grad_py[:, -1, :] = (pressure[:, -1, :] - pressure[:, -2, :]) / dx
    
    # z-direction
    grad_pz[:, :, 1:-1] = (pressure[:, :, 2:] - pressure[:, :, :-2]) / (2 * dx)
    grad_pz[:, :, 0] = (pressure[:, :, 1] - pressure[:, :, 0]) / dx
    grad_pz[:, :, -1] = (pressure[:, :, -1] - pressure[:, :, -2]) / dx
    
    # Apply Darcy's law: v = -(k/μ) ∇p
    vx = -(permeability / fluid_viscosity_pa_s) * grad_px
    vy = -(permeability / fluid_viscosity_pa_s) * grad_py
    vz = -(permeability / fluid_viscosity_pa_s) * grad_pz
    
    return {
        'vx': vx,
        'vy': vy,
        'vz': vz
    }


def run_flow_simulation(
    grid: Dict[str, Any],
    boundary_conditions: Dict[str, Any],
    solver_params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Run complete flow simulation on a grid.
    
    Args:
        grid: Grid dictionary from setup_simulation_grid
        boundary_conditions: BC dictionary from apply_pressure_boundary_conditions
        solver_params: Optional solver parameters (tol, max_iter)
        
    Returns:
        Dictionary with simulation results:
        - pressure: Pressure field (Pa)
        - velocity: Velocity components (vx, vy, vz) in m/s
        - converged: Whether solver converged
        - solve_time_s: Solution time
    """
    if solver_params is None:
        solver_params = {'tol': 1e-6, 'max_iter': 10000}
    
    # Extract grid data
    fluid_mask = grid['fluid_mask']
    shape = grid['shape']
    voxel_size_mm = grid['voxel_size_mm']
    
    # Setup inlet/outlet
    from . import mesh_or_grid
    faces = mesh_or_grid.get_inlet_outlet_faces(shape)
    inlet_mask = faces['inlet_mask']
    outlet_mask = faces['outlet_mask']
    
    # Compute permeability field
    permeability = mesh_or_grid.compute_permeability_field(fluid_mask)
    
    # Build operator
    A, rhs = build_pressure_poisson_operator(
        fluid_mask, permeability, voxel_size_mm,
        inlet_mask, outlet_mask
    )
    
    # Solve pressure field
    pressure_result = solve_pressure_field(
        A, rhs, inlet_mask, outlet_mask,
        boundary_conditions['inlet_pressure_pa'],
        boundary_conditions['outlet_pressure_pa'],
        shape,
        tol=solver_params['tol'],
        max_iter=solver_params['max_iter']
    )
    
    # Compute velocity field
    velocity = compute_velocity_field(
        pressure_result['pressure'],
        permeability,
        voxel_size_mm,
        boundary_conditions['fluid_viscosity_pa_s']
    )
    
    return {
        'pressure': pressure_result['pressure'],
        'velocity': velocity,
        'converged': pressure_result['converged'],
        'iterations': pressure_result['iterations'],
        'solve_time_s': pressure_result['solve_time_s'],
        'tolerance': pressure_result['tolerance']
    }
