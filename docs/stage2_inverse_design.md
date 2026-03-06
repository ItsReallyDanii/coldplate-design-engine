# Stage 2: Inverse-Design Formulation

## Overview

Stage 2 implements formal inverse-design optimization on top of the Stage 1 evaluation engine. This stage transforms the forward-evaluation system into an optimization framework that can search for improved cold plate designs.

**Important**: Stage 2 operates entirely on Stage 1 proxy metrics. Results do NOT establish real thermal or hydraulic superiority. CFD validation (Stages 3-4) is required for physical claims.

## Objectives

### Primary Objective
**Maximize `heat_exchange_area_proxy`**
- Proxy metric for heat transfer area
- Based on fluid-solid interface length in 2D
- Weight: 1.0
- **NOT actual heat transfer rate**

### Secondary Objective
**Minimize `hydraulic_resistance_proxy`**
- Dimensionless resistance proxy
- Based on geometric heuristics
- Weight: 0.5
- **NOT real pressure drop**

### Objective Function
```
total_score = (1.0 * heat_exchange_area_proxy) - (0.5 * hydraulic_resistance_proxy) - penalties
```

Higher score is better. Penalties are applied for constraint violations.

## Constraints

### Hard Constraints (must satisfy)
1. **Flow connectivity**: `flow_connectivity_score >= 0.5`
   - Flow must be reasonably connected from inlet to outlet
   - Violation = invalid candidate

2. **Porosity range**: `0.3 <= porosity <= 0.8`
   - Porosity must be in reasonable range for cold plates
   - Violation = invalid candidate

### Soft Constraints (penalized if violated)
3. **Dead zone limit**: `dead_zone_fraction <= 0.3`
   - Penalize excessive disconnected fluid regions
   - Penalty weight: 500.0

4. **Minimum feature size**: `min_fluid_feature_px >= 2.0`
   - Penalize features below manufacturing threshold
   - Penalty weight: 200.0

## Search Space

### Families
All 6 Stage 1 baseline families are available:
- Straight channels
- Serpentine channels
- Pin-fin arrays
- Gyroid 2D proxy
- Diamond 2D proxy
- Primitive 2D proxy

### Parameter Bounds

#### Straight Channel
- `num_channels`: [2, 10] integer
- `channel_width_fraction`: [0.2, 0.8] continuous

#### Serpentine Channel
- `channel_width_px`: [5, 20] continuous
- `turn_radius_px`: [10, 30] continuous
- `num_passes`: [2, 6] integer

#### Pin Fin
- `pin_diameter_px`: [4, 15] continuous
- `pin_spacing_px`: [15, 40] continuous
- `offset_rows`: [0, 1] discrete (boolean)

#### Gyroid 2D
- `wavelength_px`: [15, 50] continuous
- `threshold`: [-0.3, 0.3] continuous

#### Diamond 2D
- `wavelength_px`: [15, 50] continuous
- `threshold`: [-0.3, 0.3] continuous

#### Primitive 2D
- `wavelength_px`: [15, 50] continuous
- `threshold`: [-0.3, 0.3] continuous

## Optimization Methods

### Random Search Baseline
- Pure random sampling from search space
- Uniform distribution over families and parameters
- No learning or adaptation
- Serves as honest baseline for comparison

### Genetic Algorithm (Inverse-Design Method)
Chosen for Stage 2 because:
- Naturally handles parameterized families
- Works with mixed continuous/discrete/integer parameters
- Can explore multiple families simultaneously
- Simple, understandable, reproducible

**Algorithm parameters**:
- Population size: 20 (configurable)
- Elite fraction: 20%
- Mutation rate: 20% per parameter
- Crossover rate: 60%
- Selection: Tournament selection (size 3)

**Operations**:
1. **Initialization**: Random population across families
2. **Evaluation**: Score each candidate with objective function
3. **Selection**: Keep top 20% as elites
4. **Crossover**: Mix parameters from parents (same family) or pick one parent (different families)
5. **Mutation**: Gaussian noise for continuous, random flip/change for discrete/integer
6. **Repeat** until budget exhausted

## Comparison Framework

### Fair Comparison Requirements
- **Equal evaluation budget** for both methods
- Same search space and objective function
- Different random seeds to avoid bias
- Same grid configuration
- Same Stage 1 evaluator

### Metrics Tracked
- Best score found
- Top-k score distribution
- Validity rate (fraction passing hard constraints)
- Invalid candidate rate
- Family usage distribution
- Generation-by-generation progress (GA only)

### Success Criteria
Genetic algorithm must:
1. Achieve higher best score than random search
2. Under equal evaluation budget
3. For at least one nontrivial configuration
4. With reproducible results

## Limitations and Scope

### What Stage 2 IS
- Formal inverse-design problem formulation
- Parameterized family optimization
- Honest comparison against random baseline
- Proxy-based objective optimization

### What Stage 2 is NOT
- Real thermal optimization (requires CFD)
- Real pressure drop minimization (requires CFD)
- Manufacturing validation
- Structural validation
- Production-ready design

### Known Limitations
1. **Proxy metrics only**: No actual physics solved
2. **2D geometry**: Not true 3D cold plate behavior
3. **Parameterized families**: Limited to predefined geometries
4. **No gradients**: Cannot use gradient-based optimization
5. **Heuristic constraints**: Manufacturing constraints are simplified

## Stage 2 Gate Criteria

From `docs/stage_gates.md`:

**Pass Gate**:
- Candidate outperforms baselines on surrogate under matched constraints
- If graded structures pursued: model can generate controllable porosity field from input load map

**Applied to this implementation**:
- ✓ Genetic algorithm outperforms random search baseline
- ✓ Under equal evaluation budget (100 evals each)
- ✓ On proxy objective function
- ✓ With reproducible seeds
- ✓ Documented honestly with proxy labels

## Results Summary

See `results/stage2_inverse/comparison_summary.md` for full details.

**Key findings**:
- Genetic algorithm achieves **66.19% improvement** over random search
- Best scores: 2049.64 (GA) vs 1233.31 (random)
- Validity rates: 67% (GA) vs 9% (random)
- GA converges to diamond_2d family as preferred geometry
- Top-10 consistency: std dev 22.6 (GA) vs 301.5 (random)

## Next Steps

Stage 2 provides optimized proxy-based candidates. To advance:

1. **Stage 3**: Promote 2D geometry to 3D parametric CAD
2. **Stage 3.5**: Apply physical corrections (porous media, effective properties)
3. **Stage 4**: Run CFD with conjugate heat transfer
4. **Stage 5**: FEA structural validation
5. **Compare**: Inverse-designed candidate vs uniform TPMS baselines under matched constraints

Only after CFD validation can thermal and hydraulic superiority claims be made.
