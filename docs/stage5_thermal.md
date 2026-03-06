# Stage 5: Thermal Validation

**Status:** IMPLEMENTED AND FUNCTIONAL

Stage 5 provides the first real thermal validation layer on top of Stage 4 flow simulation.

## What Stage 5 Does

Stage 5 implements **flow-informed thermal simulation** using a simplified steady-state thermal solver:

1. Loads Stage 4 flow simulation results (pressure, velocity fields)
2. Reconstructs 3D geometry from Stage 3 metadata
3. Couples flow field to thermal solver through convective heat transfer
4. Solves steady-state heat conduction equation with convective coupling
5. Computes temperature fields under defined thermal boundary conditions
6. Calculates thermal metrics (peak temperature, thermal resistance, uniformity)
7. Compares candidates under matched thermal boundary conditions
8. Outputs reproducible results with honest quantity labeling

## Thermal Simulation Scope

### What IS Simulated (HONEST)

- **Temperature field**: From finite-difference thermal conduction solver
- **Convective heat transfer**: Flow-informed using Stage 4 velocity field
- **Peak temperature**: Maximum temperature in domain
- **Average temperature**: Mean solid/fluid temperatures
- **Thermal resistance**: Effective R_th = ΔT_max / Q_total
- **Temperature uniformity**: Coefficient of variation and spread

All thermal quantities are **labeled as SIMULATED** in outputs.

### What is NOT Simulated (LIMITATIONS)

- **Full conjugate heat transfer**: Fluid energy equation NOT solved
- **Transient dynamics**: Steady-state only
- **Radiation**: No radiative heat transfer
- **Complex turbulence**: Simplified convective heat transfer correlation
- **Phase change**: No boiling or condensation

Stage 5 is **NOT** a full CHT solver. It provides:
- Comparative thermal performance ranking across candidates
- Temperature distribution analysis
- Relative thermal resistance estimation

Stage 5 does **NOT** provide:
- Absolute quantitative predictions validated against experiment
- Junction-temperature realism for actual chip packaging
- Complex thermal phenomena (phase change, radiation, etc.)

## Execution

### Quick Start (Smoke Test)

```bash
# Run smoke test on Stage 4 smoke outputs
python src/stage5_thermal/cli.py smoke
```

**Expected output:**
```
=== Stage 5 Thermal Validation ===
Loading Stage 4 candidates...
Loaded 2 candidates

[1/2] Processing candidate_02_diamond_2d_s1045...
  Thermal solver: CONVERGED
  Solve time: 98.88s
  Peak temperature: 50.74 °C
  Thermal resistance: 1.029610 K/W

[2/2] Processing candidate_01_diamond_2d_s1127...
  Thermal solver: CONVERGED
  Solve time: 99.61s
  Peak temperature: 50.87 °C
  Thermal resistance: 1.034971 K/W

=== Summary ===
Candidates processed: 2
Best thermal resistance: 1.029610 K/W
Best candidate: candidate_02_diamond_2d_s1045

Smoke test PASSED!
```

### Run on Stage 4 Outputs

```bash
# Run on full Stage 4 results
python src/stage5_thermal/cli.py run results/stage4_sim_full --output results/stage5_thermal_full

# Run with top-k selection
python src/stage5_thermal/cli.py run results/stage4_sim_full --output results/stage5_thermal_top5 --top-k 5

# Run with family filter
python src/stage5_thermal/cli.py run results/stage4_sim_full --output results/stage5_thermal_diamond --family diamond_2d
```

## Thermal Boundary Conditions

Stage 5 uses **matched thermal boundary conditions** for fair comparison:

```python
{
    'heat_flux_w_m2': 1e6,          # 1 MW/m² heat flux (chip side)
    'inlet_temperature_c': 25.0,     # 25°C coolant inlet
    'k_solid_w_m_k': 200.0,          # Aluminum thermal conductivity
    'k_fluid_w_m_k': 0.6,            # Water thermal conductivity
    'rho_fluid_kg_m3': 1000.0,       # Water density
    'cp_fluid_j_kg_k': 4180.0,       # Water specific heat
    'mu_fluid_pa_s': 0.001,          # Water viscosity
    'use_flow_informed_h': True      # Use Stage 4 velocity for convection
}
```

## Thermal Solver Method

### Steady-State Heat Conduction

Solves: ∇·(k∇T) + h·(T - T_ref) = q'''

where:
- k: thermal conductivity field (solid/fluid)
- h: convective heat transfer coefficient (flow-informed)
- T_ref: coolant reference temperature
- q''': volumetric heat generation (from boundary heat flux)

### Convective Coupling

Estimates local convective coefficient from Stage 4 velocity using simplified correlation:

h ~ (k/L) × Re^0.8 × Pr^0.4

where:
- Re: Reynolds number from local velocity
- Pr: Prandtl number from fluid properties
- L: characteristic length scale (voxel size)

### Discretization

- Finite-difference method on voxel grid
- 7-point stencil for 3D Laplacian
- Direct sparse solver (scipy.sparse.linalg.spsolve)
- Harmonic mean of conductivities at interfaces

## Metrics and Labeling

### SIMULATED Thermal Quantities

From Stage 5 thermal solver:

```json
{
    "thermal_simulated_quantities": {
        "temperature_statistics": {
            "T_max_c": 50.87,
            "T_mean_c": 37.94,
            "T_solid_max_c": 50.87,
            "T_fluid_mean_c": 29.53,
            "label": "SIMULATED",
            "method": "thermal_field_statistics"
        },
        "thermal_resistance": {
            "thermal_resistance_k_w": 1.034971,
            "delta_T_max_c": 25.87,
            "heat_input_w": 25.0,
            "label": "SIMULATED",
            "method": "thermal_resistance_calculation"
        },
        "uniformity": {
            "coefficient_of_variation": 0.089,
            "temperature_spread_c": 21.34,
            "label": "SIMULATED",
            "method": "temperature_uniformity_analysis"
        }
    }
}
```

### FLOW_SIMULATED Quantities

Carried forward from Stage 4:

- Pressure drop (Pa)
- Flow rate (m³/s, L/min)
- Hydraulic resistance (Pa·s/m³)
- Velocity statistics
- Flow uniformity

### GEOMETRIC Quantities

Carried forward from Stage 3:

- Porosity
- Domain volume
- Fluid volume

## Output Structure

Stage 5 creates structured outputs:

```
results/stage5_thermal_smoke/
├── candidate_01_diamond_2d_s1127/
│   ├── temperature_field.npy          # Temperature field array
│   ├── thermal_metrics.json           # All thermal metrics
│   ├── provenance.json                # Traceability chain
│   ├── boundary_conditions.json       # Applied BCs
│   └── solver_info.json               # Solver convergence info
├── candidate_02_diamond_2d_s1045/
│   └── ... (same structure)
├── thermal_comparison.json            # Comparison metrics
├── thermal_comparison_summary.md      # Human-readable summary
├── stage5_summary.json                # High-level summary
└── run_manifest.json                  # Execution metadata
```

## Tests

Run Stage 5 tests:

```bash
pytest tests/test_stage5_thermal.py -v
```

**Test coverage:**
- Case loading from Stage 4 (3 tests)
- Thermal boundary conditions (3 tests)
- Thermal solver (2 tests)
- Metrics computation (2 tests)
- Comparison framework (3 tests)
- End-to-end integration (1 test)

**Total: 14 tests, all passing**

## Stage 5 vs Stage 4

| Aspect | Stage 4 | Stage 5 |
|--------|---------|---------|
| **Physics** | Flow only (pressure, velocity) | Flow + Thermal (temperature) |
| **Solver** | Pressure Poisson | Heat conduction + convection |
| **Primary Metric** | Hydraulic resistance | Thermal resistance |
| **Coupling** | None | Flow-informed convection |
| **Validation Focus** | Pressure drop, flow rate | Peak temperature, thermal R_th |

## Limitations and Future Work

### Current Limitations

1. **No fluid energy equation**: Coolant temperature assumed constant at T_inlet
2. **Simplified convection**: Correlation-based, not full CHT
3. **No radiation**: May be significant for high-temperature applications
4. **No turbulence**: Reynolds number effects simplified
5. **Uniform materials**: No graded or composite materials
6. **Steady-state only**: No transient thermal response

### Future Improvements (Stage 5+)

- Implement fluid energy equation for conjugate heat transfer
- Add turbulence modeling for improved convection accuracy
- Include radiation heat transfer for high-temperature cases
- Transient thermal simulation for time-dependent loads
- Graded material property support
- Experimental validation against bench test data

## Quantity Labeling Honesty

Stage 5 maintains strict quantity labeling:

- **SIMULATED**: Quantities computed from thermal solver with defined BCs
- **FLOW_SIMULATED**: Quantities from Stage 4 flow solver
- **GEOMETRIC**: Quantities from Stage 3 geometry only
- **NOT_COMPUTED**: Quantities not yet implemented

This labeling prevents confusion about what is truly validated vs. proxy/estimate.

## References

- Heat conduction discretization: Finite-difference method
- Convective correlation: Dittus-Boelter correlation (turbulent flow)
- Solver: scipy.sparse.linalg.spsolve (direct sparse solver)
- Stage 4 flow validation: docs/stage4_simulation.md
