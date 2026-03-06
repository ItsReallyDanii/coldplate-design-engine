"""
Stage 4: First physics validation layer on top of Stage 3 geometry.

This package provides:
- Flow simulation using pressure Poisson solver
- Pressure drop and velocity field computation
- Fair comparison across candidates under matched conditions
- Honest labeling of simulated vs proxy quantities

Limitations (clearly stated):
- Flow-only simulation; thermal coupling not yet implemented
- Simplified steady-state incompressible flow model
- Darcy-like resistance model for porous regions
- Grid-based finite-difference solver
"""

__version__ = "1.0.0"
