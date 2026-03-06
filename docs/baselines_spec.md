# Baselines Specification

**Stage: 0 / 0.5 — specification only; no baseline simulations have been run.**

Baseline evaluations will use parameter sweeps, not single-point baselines.

## Baseline families

- **Channels:** straight parallel channels, serpentine channels, pin-fin / interrupted channels (`baselines/channels/`).
- **TPMS lattices:** gyroid, diamond, primitive (`baselines/tpms/`).
- **Topology optimization:** reserved for later-stage comparison; used when `topology_opt` candidates become available (`baselines/topology_opt/`).

## Geometry parameters

- **Straight / serpentine / pin-fin channels:** channel width, height, pitch, land/fin thickness, fin pattern (straight vs serpentine turning radius), pin/interrupt spacing and shape, inlet/outlet distribution features.
- **TPMS lattices (gyroid/diamond/primitive):** unit cell size, wall thickness, porosity, orientation relative to flow direction, lattice thickness across the flow path, interface transitions to headers.
- **`topology_opt` (reserved):** design domain dimensions, filter radius, volume fraction target, penalization scheme, and minimum feature control will be defined once Stage 2-3 outputs exist.
- Parameter ranges will be swept to map sensitivity; no single nominal geometry represents a baseline.

## Operating conditions

- Single-phase liquid coolant with matched inlet temperature, mass flow rate, and pressure budget across all baselines.
- Heat load and die-footprint boundary conditions set to the target application; spatial heat-flux mapping will mirror the test case used for candidate designs.
- Conjugate heat transfer is assumed; solid material properties will be held consistent across baselines for fair comparison.

## Matched constraints

- Identical die-footprint, inlet/outlet locations, and overall cold-plate envelope.
- Common pressure-drop budget and pumping power accounting.
- Consistent manufacturing resolution assumptions (machining or AM) applied to all geometries.
- Mesh quality, turbulence/porous-model settings, and solver tolerances held constant within each study.

## Comparison metrics

- Junction-to-coolant thermal resistance.
- Pressure drop and pumping power at matched flow conditions.
- Coefficient of performance (heat removed per unit pumping power).
- Temperature uniformity across the die footprint and flow maldistribution indicators.
- Manufacturability compliance (minimum feature vs. assumed process capability).

## Acceptance criteria

- Baseline families and parameter sets are documented with sweep ranges sufficient to span literature-backed operating envelopes.
- CAD or parametric definitions for each family exist in `baselines/` and are reproducible without manual edits.
- Comparison metrics and matched-constraint settings are defined before any candidate vs. baseline study.
- `topology_opt` references remain documentation-only until an optimization output is available; no placeholder performance claims.

## Notes on future literature-backed parameter locking

- Stage 0.5 will replace open parameter ranges with literature-backed bounds (e.g., Reynolds number ranges, porosity bands, manufacturable wall thickness) and record citations in `claim_audit_v2/`.
- Baseline sweep grids will be pruned or refined using those locked ranges to ensure fair, defensible comparisons.
- Manufacturing constraints will be updated to reflect specific process limits (machining vs. AM) once cited.
