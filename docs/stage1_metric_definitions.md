# Stage 1 Metric Definitions

**Status:** Stage 1 implementation complete.

This document defines all metrics computed by the Stage 1 2D cold-plate evaluation engine.

## Critical Honesty Requirements

**All metrics are explicitly categorized as:**
- **GEOMETRIC**: Real geometric properties derived directly from 2D masks
- **FLOW_PROXY**: Dimensionless flow-related proxies (NOT real pressure drop, velocity, or flow rate)
- **HEAT_PROXY**: Dimensionless heat-transfer-adjacent proxies (NOT real thermal resistance or heat transfer coefficient)

**Proxy metrics:**
- Are clearly labeled with `_proxy` suffix in field names
- Include documented assumptions and limitations
- Do NOT claim to predict real physical performance without CFD/FEA

## Metric Schema Version

Current version: `1.0.0`

Version is tracked in all output manifests for reproducibility.

## GEOMETRIC METRICS (Real Quantities)

### porosity
- **Category:** GEOMETRIC
- **Units:** dimensionless (0 to 1)
- **Description:** Open-area fraction (fluid region / total area)
- **Is Proxy:** NO
- **Formula:** `sum(mask) / total_pixels`
- **Assumptions:**
  - 2D cross-section
  - Binary mask (0=solid, 1=fluid)
- **Limitations:**
  - Does not account for 3D geometry or wall thickness in z-direction

### min_fluid_feature_px
- **Category:** GEOMETRIC
- **Units:** pixels
- **Description:** Minimum fluid feature size (approximate)
- **Is Proxy:** NO
- **Method:** Distance transform approximation
- **Assumptions:**
  - 2D cross-section
  - Distance transform approximation
- **Limitations:**
  - Approximate measure
  - Pixel resolution dependent
  - Does not predict manufacturable feature size without process capability data

### min_solid_feature_px
- **Category:** GEOMETRIC
- **Units:** pixels
- **Description:** Minimum solid feature size (approximate)
- **Is Proxy:** NO
- **Method:** Distance transform approximation
- **Assumptions:**
  - 2D cross-section
  - Distance transform approximation
- **Limitations:**
  - Approximate measure
  - Pixel resolution dependent
  - Does not predict structural integrity

### solid_continuity_islands
- **Category:** GEOMETRIC
- **Units:** count
- **Description:** Number of disconnected solid regions
- **Is Proxy:** NO
- **Method:** Connected component labeling (8-connectivity)
- **Assumptions:**
  - 2D cross-section
  - 8-connectivity for component detection
- **Limitations:**
  - Does not predict structural integrity or load-bearing capacity
  - 2D disconnected regions may be connected in 3D

### wetted_perimeter_proxy
- **Category:** GEOMETRIC
- **Units:** pixels
- **Description:** Fluid-solid interface length in 2D (proxy for wetted perimeter)
- **Is Proxy:** YES
- **Method:** Gradient-based interface detection
- **Assumptions:**
  - 2D cross-section
  - Interface approximated by gradient magnitude
- **Limitations:**
  - NOT true 3D wetted perimeter
  - Does not account for surface roughness
  - Pixel-based approximation introduces discretization error

## FLOW PROXY METRICS (Dimensionless)

### flow_connectivity_score
- **Category:** FLOW_PROXY
- **Units:** dimensionless (0 to 1)
- **Description:** Proxy for flow connectivity (0 = disconnected, 1 = fully connected)
- **Is Proxy:** YES
- **Formula:** `1.0 if fully_connected else 1.0 / num_components`
- **Assumptions:**
  - 2D topology
  - No flow physics (viscosity, Reynolds number, etc.)
- **Limitations:**
  - **NOT a real flow rate or velocity**
  - Does not account for viscosity, Reynolds number, or flow regime
  - Purely topological measure
  - Does not predict pressure drop or flow distribution

### dead_zone_fraction
- **Category:** FLOW_PROXY
- **Units:** dimensionless (0 to 1)
- **Description:** Fraction of fluid region disconnected from inlet-outlet path
- **Is Proxy:** YES
- **Method:** Flood-fill from inlet to outlet
- **Assumptions:**
  - 2D topology
  - Flood-fill connectivity (no flow physics)
- **Limitations:**
  - Does not account for flow stagnation in connected regions
  - **NOT a predictor of actual recirculation zones**
  - Requires CFD to identify real stagnation

### hydraulic_diameter_proxy
- **Category:** FLOW_PROXY
- **Units:** pixels
- **Description:** Hydraulic diameter proxy: `4 * Area / Perimeter`
- **Is Proxy:** YES
- **Formula:** `4 * fluid_area / wetted_perimeter`
- **Assumptions:**
  - 2D cross-section
  - Uniform cross-section along flow path
- **Limitations:**
  - **NOT a true hydraulic diameter in 3D**
  - Does not capture variation along flow path
  - Assumes constant cross-section (invalid for serpentine or graded structures)

### hydraulic_resistance_proxy
- **Category:** FLOW_PROXY
- **Units:** dimensionless
- **Description:** Dimensionless hydraulic resistance proxy (higher = more resistance)
- **Is Proxy:** YES
- **Formula:** `(perimeter / area) / (porosity + epsilon)`
- **Assumptions:**
  - 2D geometry
  - Heuristic based on porosity and perimeter
  - No Reynolds number dependence
- **Limitations:**
  - **NOT real pressure drop**
  - Does not include fluid properties (viscosity, density)
  - No turbulence or transition modeling
  - Purely geometric heuristic
  - **Requires CFD for real pressure drop prediction**

### tortuosity_proxy
- **Category:** FLOW_PROXY
- **Units:** dimensionless
- **Description:** Path tortuosity proxy based on geometric heuristic
- **Is Proxy:** YES
- **Method:** Inverse of normalized porosity (crude approximation)
- **Assumptions:**
  - 2D topology
  - Heuristic approximation
- **Limitations:**
  - **NOT a true flow path length ratio**
  - Does not follow streamlines
  - Crude approximation
  - **Real tortuosity requires streamline tracing from CFD**

### maldistribution_proxy
- **Category:** FLOW_PROXY
- **Units:** dimensionless
- **Description:** Flow maldistribution proxy based on channel width variance
- **Is Proxy:** YES
- **Method:** Coefficient of variation of distance field
- **Assumptions:**
  - 2D topology
  - Geometric approximation
- **Limitations:**
  - **NOT actual flow distribution**
  - Does not solve Navier-Stokes
  - Purely geometric variance measure
  - **Real flow distribution requires CFD**

## HEAT TRANSFER PROXY METRICS (Dimensionless)

### heat_exchange_area_proxy
- **Category:** HEAT_PROXY
- **Units:** pixels
- **Description:** Heat exchange area proxy (fluid-solid interface length)
- **Is Proxy:** YES
- **Method:** Same as wetted_perimeter_proxy
- **Assumptions:**
  - 2D interface
  - All interface participates equally in heat transfer
- **Limitations:**
  - **NOT actual heat transfer rate**
  - Does not account for convection coefficients (velocity-dependent)
  - Ignores thermal boundary layer development
  - No conjugate heat transfer modeling
  - **Requires CFD with conjugate heat transfer for real thermal resistance**

### wall_contact_density
- **Category:** HEAT_PROXY
- **Units:** dimensionless
- **Description:** Wall contact density (interface length / fluid area)
- **Is Proxy:** YES
- **Formula:** `wetted_perimeter / fluid_area`
- **Assumptions:**
  - 2D geometry
  - Uniform heat transfer coefficient
- **Limitations:**
  - **NOT actual thermal resistance**
  - Ignores flow velocity effects on convection coefficient
  - No thermal conductivity effects in solid or fluid
  - **Requires conjugate heat transfer simulation for real thermal resistance**

### thermal_path_uniformity_proxy
- **Category:** HEAT_PROXY
- **Units:** dimensionless (0 to 1)
- **Description:** Proxy for thermal path uniformity (0 = non-uniform, 1 = uniform)
- **Is Proxy:** YES
- **Method:** Geometric uniformity based on distance field variance
- **Assumptions:**
  - 2D geometry
  - Geometric uniformity approximation
- **Limitations:**
  - **NOT actual temperature uniformity**
  - Does not solve heat equation
  - Purely geometric measure
  - **Real temperature uniformity requires conjugate heat transfer CFD**

### spreading_proxy
- **Category:** HEAT_PROXY
- **Units:** dimensionless (0 to 1)
- **Description:** Thermal spreading proxy based on fluid distribution
- **Is Proxy:** YES
- **Method:** Spatial variance of fluid region centroids
- **Assumptions:**
  - 2D geometry
  - Uniform material properties
- **Limitations:**
  - **NOT actual spreading resistance**
  - Does not model conduction in solid
  - Purely geometric heuristic
  - **Real spreading resistance requires conjugate heat transfer modeling**

## What Stage 1 Metrics DO NOT Provide

Stage 1 metrics are **screening tools only**. They do NOT provide:

1. **Real thermal resistance** — Requires CFD with conjugate heat transfer
2. **Real pressure drop** — Requires CFD with appropriate turbulence model
3. **Real heat transfer coefficients** — Requires velocity and temperature field solutions
4. **Temperature uniformity** — Requires coupled fluid-solid heat transfer solution
5. **Flow distribution** — Requires Navier-Stokes solution
6. **Manufacturability validation** — Requires process capability data and geometric tolerance analysis
7. **Structural integrity** — Requires FEA with thermal and pressure loads
8. **3D performance prediction** — Stage 1 uses 2D cross-sections only

## Appropriate Use of Stage 1 Metrics

**Stage 1 metrics are appropriate for:**
- Rapid screening of baseline families (channels vs TPMS-like patterns)
- Identifying geometric trends across parameter sweeps
- Eliminating clearly infeasible designs (e.g., disconnected flow paths, extreme feature sizes)
- Generating hypotheses for further CFD/FEA investigation

**Stage 1 metrics are NOT appropriate for:**
- Claiming thermal or hydraulic superiority without CFD validation
- Predicting real-world cold-plate performance
- Justifying design freeze or manufacturing decisions
- Marketing or customer-facing performance claims

## Stage Gate Requirements

To pass Stage 1 and advance to Stage 2:
- All metrics must be computed without errors
- Output schema must match documented definitions
- Metric honesty discipline must be maintained (no mislabeled proxies)
- Parameter sweeps must be reproducible from config and seed

To claim real performance improvements:
- **Must advance to Stage 4 (CFD) minimum**
- Must include matched-constraint baseline comparisons
- Must demonstrate mesh independence
- Must document all assumptions and limitations
