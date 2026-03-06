"""
Stage 5: Thermal Validation Layer

SCOPE STATEMENT (HONEST):
This module implements the FIRST REAL THERMAL VALIDATION on top of Stage 4 flow simulation.

What Stage 5 DOES:
- Loads Stage 4 flow simulation results (pressure, velocity fields)
- Solves steady-state thermal conduction equation with convective coupling
- Computes temperature fields under defined thermal boundary conditions
- Calculates thermal metrics (peak temperature, thermal resistance, uniformity)
- Compares candidates under matched thermal boundary conditions
- Labels all quantities honestly (SIMULATED, FLOW_SIMULATED, GEOMETRIC, NOT_COMPUTED)

What Stage 5 does NOT do:
- Full conjugate heat transfer (fluid energy equation NOT solved)
- Transient thermal dynamics (steady-state only)
- Radiation heat transfer (not included)
- Complex turbulence-enhanced heat transfer (simplified convective coupling)

THERMAL SIMULATION METHOD:
- Steady-state heat conduction: ∇·(k∇T) = q'''
- Convective heat transfer using Stage 4 velocity field: q_conv = h·A·(T_solid - T_fluid)
- Finite-difference discretization on voxel grid
- Direct sparse solver for temperature field

This is an HONEST, SIMPLIFIED thermal solver suitable for:
- Comparative thermal performance ranking
- Temperature distribution analysis
- Relative thermal resistance estimation

This is NOT:
- A full conjugate heat transfer CFD solver
- Validated for absolute quantitative predictions
- Including radiation, phase change, or complex physics
"""

__version__ = "1.0.0"
__stage__ = "stage5_thermal"

from . import (
    load_cases,
    boundary_conditions,
    solver,
    coupling,
    metrics,
    compare,
    io,
    provenance,
    cli
)

__all__ = [
    'load_cases',
    'boundary_conditions',
    'solver',
    'coupling',
    'metrics',
    'compare',
    'io',
    'provenance',
    'cli'
]
