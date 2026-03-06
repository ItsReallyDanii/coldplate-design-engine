# Target Specification

**Stage: 0 / 0.5 — definition only; no validated results exist.**

## Target statement

"Design an internal porous core / channel architecture for a direct-to-chip liquid-cooling cold plate that improves thermal-hydraulic performance over standard channel and TPMS baselines under matched constraints."

## Target component

- Direct-to-chip cold plate with a die-footprint internal volume reserved for an engineered porous core or structured channel network.
- Single-phase inlet/outlet interface; external manifold and facility loop are out of scope for Stage 0 / 0.5.
- Materials: conductive metal cold plate (e.g., copper-class alloys) assumed; exact grade to be set later.

## Target application

- High-power compute packages requiring direct-to-chip liquid cooling with constrained pressure budget and controlled junction temperatures.
- Evaluation is limited to cold-plate internal architecture; socket, lid, and board-level integration are treated as boundary conditions.

## Primary objectives

- Improve junction-to-coolant thermal resistance relative to straight-channel and TPMS baselines under matched heat load, flow, and pressure budget.
- Preserve or reduce pumping power relative to baselines while maintaining acceptable temperature uniformity across the die footprint.
- Keep the design space open to structured channels, porous cores, TPMS lattices, and later `topology_opt` candidates without locking geometry specifics at Stage 0.
- Maintain manufacturability-aware feature sizing and connectivity sufficient for robust flow distribution; exact limits will be literature-backed at Stage 0.5.

## Non-goals

- No claims of quantitative performance uplift in Stage 0 / 0.5.
- No manifold, facility loop, or packaging design.
- No cost, sourcing, or reliability qualification in this stage.
- No coolant chemistry optimization beyond a single-phase assumption.

## Stage-0 locked assumptions

- Single-phase liquid coolant is assumed; deionized water is the default placeholder until Stage 0.5 literature review locks a coolant specification.
- Baseline families for comparison are limited to straight/serpentine/pin-fin channel layouts and TPMS lattices (gyroid/diamond/primitive); `topology_opt` baselines are reserved for later-stage comparison.
- All evaluations will use matched constraints: identical heat load, footprint, inlet/outlet locations, and pressure-drop budget across baselines and candidates.
- Parameter sweeps, not single-point baselines, will be used to map performance trends before any claims are made.
- No feature dimensions, flow rates, or pressure targets are locked at Stage 0; they will be set using literature-backed ranges at Stage 0.5.

## Tracked design hypothesis

**Spatially varying porosity / functionally graded internal structures** are tracked as a candidate design direction under investigation. This hypothesis proposes that non-uniform thermal loads (e.g., localized hotspots) and mechanical constraints may be addressed by grading internal structure porosity or feature density across the die footprint, rather than using a uniform lattice or channel spacing throughout.

This approach is **not yet validated**. It is a candidate method that will be evaluated against uniform and segmented TPMS baselines when Stage 2-4 simulation results become available. The hypothesis does not replace or supersede the target statement, which remains geometry-agnostic.

### What is NOT yet claimed

- No quantitative performance uplift from graded structures has been demonstrated.
- No claim is made that graded structures outperform segmented or zoned TPMS lattices under realistic constraints.
- No claim is made regarding manufacturability, powder evacuation, or flow stability of graded internal structures.
- No claim is made that graded structures are a superior or preferable design solution; they are one candidate approach under test.
