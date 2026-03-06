"""
Steady-state thermal solver for Stage 5.

Implements simplified thermal conduction with flow-informed convective coupling.

HONEST SCOPE:
- Steady-state heat conduction equation: ∇·(k∇T) = q'''
- Convective coupling using Stage 4 velocity field
- Finite-difference discretization on voxel grid
- Direct sparse solver

LIMITATIONS:
- No fluid energy equation (not full conjugate heat transfer)
- Simplified convective heat transfer coefficient estimation
- No radiation
- Uniform material properties within each phase
"""

import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg
from typing import Dict, Any, Tuple, Optional
import time


def build_thermal_operator(
    volume: np.ndarray,
    voxel_size_mm: float,
    thermal_conductivity: np.ndarray,
    convective_coefficient: Optional[np.ndarray] = None,
    boundary_conditions: Optional[Dict[str, Any]] = None
) -> Tuple[sparse.csr_matrix, np.ndarray]:
    """
    Build sparse linear operator for steady-state heat conduction.
    
    Solves: ∇·(k∇T) + h·(T - T_ref) = q'''
    
    where:
    - k is thermal conductivity field
    - h is convective heat transfer coefficient (in fluid regions)
    - T_ref is reference/coolant temperature
    - q''' is volumetric heat generation
    
    Args:
        volume: Boolean array (True=fluid, False=solid)
        voxel_size_mm: Physical voxel size in mm
        thermal_conductivity: Thermal conductivity field (W/m·K)
        convective_coefficient: Convective coefficient field (W/m²·K) or None
        boundary_conditions: BC dictionary
        
    Returns:
        (A, rhs) where A @ T_flat = rhs
        A: Sparse matrix operator
        rhs: Right-hand side vector
    """
    # Ensure volume is boolean
    volume = volume.astype(bool)
    
    nx, ny, nz = volume.shape
    n = nx * ny * nz
    
    # Convert voxel size to meters
    dx = voxel_size_mm / 1000.0
    
    # Flatten arrays for indexing
    volume_flat = volume.flatten()
    k_flat = thermal_conductivity.flatten()
    
    if convective_coefficient is not None:
        h_flat = convective_coefficient.flatten()
    else:
        h_flat = np.zeros(n)
    
    # Build coefficient matrix using finite differences
    # Using 7-point stencil for 3D Laplacian
    
    # Create index mapping
    def idx(i, j, k):
        return i + j * nx + k * nx * ny
    
    # Lists for sparse matrix construction
    rows = []
    cols = []
    vals = []
    
    # RHS vector
    rhs = np.zeros(n)
    
    # Get BC parameters
    if boundary_conditions is None:
        boundary_conditions = {}
    
    T_ref = boundary_conditions.get('inlet_temperature_c', 25.0)
    heat_flux = boundary_conditions.get('heat_flux_w_m2', 1e6)
    
    # Build operator
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                idx_c = idx(i, j, k)
                
                # Check if on boundary
                on_bottom = (k == 0)
                on_top = (k == nz - 1)
                on_inlet = (k == 0)
                on_outlet = (k == nz - 1)
                
                # Diagonal term (center)
                diag = 0.0
                
                # Off-diagonal terms (neighbors)
                # Use harmonic mean of conductivities at interfaces
                
                # X-direction
                if i > 0:
                    idx_l = idx(i-1, j, k)
                    k_interface = 2.0 * k_flat[idx_c] * k_flat[idx_l] / (k_flat[idx_c] + k_flat[idx_l] + 1e-10)
                    coeff = k_interface / (dx ** 2)
                    rows.append(idx_c)
                    cols.append(idx_l)
                    vals.append(coeff)
                    diag -= coeff
                
                if i < nx - 1:
                    idx_r = idx(i+1, j, k)
                    k_interface = 2.0 * k_flat[idx_c] * k_flat[idx_r] / (k_flat[idx_c] + k_flat[idx_r] + 1e-10)
                    coeff = k_interface / (dx ** 2)
                    rows.append(idx_c)
                    cols.append(idx_r)
                    vals.append(coeff)
                    diag -= coeff
                
                # Y-direction
                if j > 0:
                    idx_b = idx(i, j-1, k)
                    k_interface = 2.0 * k_flat[idx_c] * k_flat[idx_b] / (k_flat[idx_c] + k_flat[idx_b] + 1e-10)
                    coeff = k_interface / (dx ** 2)
                    rows.append(idx_c)
                    cols.append(idx_b)
                    vals.append(coeff)
                    diag -= coeff
                
                if j < ny - 1:
                    idx_f = idx(i, j+1, k)
                    k_interface = 2.0 * k_flat[idx_c] * k_flat[idx_f] / (k_flat[idx_c] + k_flat[idx_f] + 1e-10)
                    coeff = k_interface / (dx ** 2)
                    rows.append(idx_c)
                    cols.append(idx_f)
                    vals.append(coeff)
                    diag -= coeff
                
                # Z-direction
                if k > 0:
                    idx_d = idx(i, j, k-1)
                    k_interface = 2.0 * k_flat[idx_c] * k_flat[idx_d] / (k_flat[idx_c] + k_flat[idx_d] + 1e-10)
                    coeff = k_interface / (dx ** 2)
                    rows.append(idx_c)
                    cols.append(idx_d)
                    vals.append(coeff)
                    diag -= coeff
                else:
                    # Bottom boundary - heat flux BC
                    # Heat flux: q = -k dT/dz => dT/dz = -q/k
                    # Modify RHS
                    rhs[idx_c] -= heat_flux / dx
                
                if k < nz - 1:
                    idx_u = idx(i, j, k+1)
                    k_interface = 2.0 * k_flat[idx_c] * k_flat[idx_u] / (k_flat[idx_c] + k_flat[idx_u] + 1e-10)
                    coeff = k_interface / (dx ** 2)
                    rows.append(idx_c)
                    cols.append(idx_u)
                    vals.append(coeff)
                    diag -= coeff
                
                # Convective term in fluid regions
                if volume_flat[idx_c]:  # Fluid region
                    # Convective heat transfer: q = h·A·(T - T_ref)
                    # In volumetric form: q''' = h·a·(T - T_ref)
                    # where a is surface area per unit volume
                    # For voxel grid, approximate a ≈ 1/dx
                    a_vol = 1.0 / dx
                    conv_coeff = h_flat[idx_c] * a_vol
                    
                    diag -= conv_coeff
                    rhs[idx_c] -= conv_coeff * T_ref
                
                # Add diagonal term
                rows.append(idx_c)
                cols.append(idx_c)
                vals.append(diag)
    
    # Build sparse matrix
    A = sparse.csr_matrix((vals, (rows, cols)), shape=(n, n))
    
    return A, rhs


def solve_thermal_field(
    volume: np.ndarray,
    thermal_conductivity: np.ndarray,
    voxel_size_mm: float,
    boundary_conditions: Dict[str, Any],
    convective_coefficient: Optional[np.ndarray] = None,
    solver_params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Solve steady-state thermal field.
    
    Args:
        volume: Boolean array (True=fluid, False=solid)
        thermal_conductivity: Thermal conductivity field (W/m·K)
        voxel_size_mm: Physical voxel size in mm
        boundary_conditions: BC dictionary
        convective_coefficient: Convective coefficient field (W/m²·K) or None
        solver_params: Solver parameters (tol, max_iter, etc.)
        
    Returns:
        Dictionary with:
        - temperature: Temperature field (°C)
        - converged: Boolean convergence flag
        - solve_time_s: Solution time
        - residual: Final residual norm
    """
    if solver_params is None:
        solver_params = {}
    
    tol = solver_params.get('tol', 1e-6)
    
    start_time = time.time()
    
    # Build operator
    A, rhs = build_thermal_operator(
        volume, voxel_size_mm, thermal_conductivity,
        convective_coefficient, boundary_conditions
    )
    
    # Solve using direct solver
    try:
        T_flat = splinalg.spsolve(A, rhs)
        converged = True
        residual = np.linalg.norm(A @ T_flat - rhs)
    except Exception as e:
        print(f"Warning: Thermal solver failed: {e}")
        # Return zero field on failure
        T_flat = np.zeros(volume.size)
        converged = False
        residual = float('inf')
    
    solve_time = time.time() - start_time
    
    # Reshape temperature field
    temperature = T_flat.reshape(volume.shape)
    
    return {
        'temperature': temperature,
        'converged': converged,
        'solve_time_s': solve_time,
        'residual': residual,
        'solver': 'direct_sparse',
        'matrix_shape': A.shape,
        'matrix_nnz': A.nnz
    }
