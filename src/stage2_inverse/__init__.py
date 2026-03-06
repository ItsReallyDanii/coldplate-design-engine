"""Stage 2: Inverse-Design Optimization.

Stage 2 builds on Stage 1's 2D evaluation engine to implement formal
inverse-design optimization. This stage:
- Uses Stage 1 proxy metrics as objectives
- Implements parameterized search over baseline families
- Compares inverse-design methods against random search baseline
- Reports honest results (proxy-based, not real thermal claims)
"""

__version__ = "2.0.0"
