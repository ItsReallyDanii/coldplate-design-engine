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
