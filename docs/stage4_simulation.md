# Stage 4: Flow Simulation Validation

**Status:** IMPLEMENTED AND FUNCTIONAL

Stage 4 provides the first real physics validation layer on top of Stage 3 geometry outputs.

## What Stage 4 Does

Stage 4 implements a **flow-only simulation** using a simplified steady-state incompressible flow solver:

1. Loads Stage 3 promoted 3D geometry
2. Sets up voxel-based computational grid
3. Solves pressure Poisson equation with Darcy-like resistance
4. Computes velocity field from pressure gradients
5. Calculates flow metrics (pressure drop, flow rate, hydraulic resistance)
6. Compares candidates under matched boundary conditions
7. Outputs reproducible results with honest quantity labeling

## Simulation Scope

### What Is Simulated (HONEST)

- **Pressure field**: From finite-difference Poisson solver
- **Velocity field**: From Darcy's law applied to pressure gradient
- **Pressure drop**: Inlet to outlet pressure difference
- **Volumetric flow rate**: Integrated from velocity field
- **Hydraulic resistance**: Pressure drop / flow rate
- **Flow uniformity**: Velocity distribution statistics

All simulated quantities are **labeled as SIMULATED** in outputs.

### What Is NOT Simulated (LIMITATIONS)

- **Thermal coupling**: No conjugate heat transfer yet
- **Turbulence**: Laminar flow assumption only
- **Compressibility**: Incompressible flow assumption
- **Transient dynamics**: Steady-state only
- **Full Navier-Stokes**: Simplified Darcy-like model in porous regions

Stage 4 is **NOT** a full CFD solver. It provides:
- Relative performance ranking across candidates
- Flow distribution analysis
- Comparative pressure drop estimates

Stage 4 does **NOT** provide:
- Absolute quantitative predictions validated against experiment
- Thermal performance metrics
- Complex flow phenomena (turbulence, recirculation, etc.)

## Execution

### Quick Start (Smoke Test)

```bash
# Run smoke test on Stage 3 smoke outputs
python src/stage4_sim/cli.py smoke
```

### Run on Stage 3 Outputs

```bash
# Run on all Stage 3 candidates
python src/stage4_sim/cli.py run results/stage3_geometry results/stage4_sim

# Run on top 5 candidates only
python src/stage4_sim/cli.py run results/stage3_geometry results/stage4_sim --top-k 5
```

### Run Tests

```bash
# Run all Stage 4 tests
pytest tests/test_stage4_*.py -v
```

## Outputs

Stage 4 creates a structured output directory:

```
results/stage4_sim/
├── run_manifest.json          # Reproducibility record
├── comparison.json            # Comparison metrics
├── comparison_summary.md      # Human-readable summary
├── stage4_summary.json        # Overall summary
├── candidate_01_*/
│   ├── metrics.json           # All computed metrics
│   ├── solver_info.json       # Solver convergence info
│   ├── provenance.json        # Full traceability chain
│   ├── pressure_field.npy     # Pressure field (3D array)
│   └── velocity_field.npz     # Velocity components (vx, vy, vz)
└── candidate_02_*/
    └── ...
```

### Output Schema

All outputs follow a strict schema with honest labeling:

```json
{
  "metrics": {
    "simulated_quantities": {
      "pressure_drop": {
        "pressure_drop_pa": 1000.0,
        "label": "SIMULATED",
        "method": "pressure_poisson_solver"
      },
      "flow_rate": {
        "flow_rate_m3_s": 1.8e-6,
        "label": "SIMULATED",
        "method": "velocity_integration"
      }
    },
    "geometric_quantities": {
      "porosity": 0.55,
      "label": "GEOMETRIC"
    },
    "proxy_quantities": {
      "note": "Thermal simulation not yet implemented",
      "label": "NOT_COMPUTED"
    }
  }
}
```

Every quantity is labeled as:
- **SIMULATED**: Computed from actual flow solver
- **GEOMETRIC**: Derived from geometry only  
- **PROXY**: Simplified estimate (none in Stage 4)
- **NOT_COMPUTED**: Not yet implemented

## Matched Conditions

All candidates are compared under **strictly matched conditions**:

- Same inlet/outlet pressure drop (1 kPa)
- Same fluid properties (water: ρ=1000 kg/m³, μ=0.001 Pa·s)
- Same flow direction (z-axis)
- Same voxel resolution
- Same solver settings

The comparison framework verifies matched conditions and reports any mismatches.

## Solver Details

### Method

- **Discretization**: Finite-difference on voxel grid
- **Equation**: Pressure Poisson with Darcy resistance: ∇·(k ∇p) = 0
- **Permeability**: k_fluid = 1e-6 m², k_solid = 1e-12 m²
- **Boundary Conditions**: Dirichlet (fixed pressure) at inlet/outlet, zero-gradient at walls
- **Solver**: Sparse direct solver (scipy.sparse.linalg.spsolve)

### Limitations

This is a **simplified solver** suitable for:
- Comparative analysis
- Flow distribution assessment
- Relative ranking

This is **NOT** suitable for:
- Absolute performance claims
- Detailed flow physics
- Design certification

## Stage 4 Pass Criteria

✓ Executable code exists  
✓ Smoke test runs successfully  
✓ Tests pass (24/24)  
✓ Stage 3 candidates load correctly  
✓ Solver converges  
✓ Outputs are reproducible  
✓ Quantities are labeled honestly  
✓ Comparisons use matched conditions  
✓ Documentation states limitations clearly

## What's Next (Stage 4.5+)

Stage 4 provides flow simulation only. Future stages would add:

- **Stage 4.5**: Conjugate heat transfer (thermal coupling)
- **Stage 5**: Structural FEA validation
- **Stage 6**: Manufacturing and testing

Do not overstate Stage 4 results. They provide **relative ranking** for flow characteristics only.
