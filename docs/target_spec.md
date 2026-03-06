# Target Specification

**Stage: 0 / 0.5 — definition only; no validated results exist.**

---

## Primary objective

> "Design an internal porous core / channel architecture for a direct-to-chip liquid-cooling
> cold plate that improves thermal-hydraulic performance over standard channel and TPMS
> baselines under matched constraints."

---

## Scope

- Cold-plate form factor: direct-to-chip (die-area footprint, single-phase liquid cooling).
- Internal geometry: porous core or structured channel architecture (open design space).
- Comparison basis: matched inlet flow rate, inlet temperature, and pressure-drop budget.
- Performance metrics: reduction in junction-to-coolant thermal resistance and/or improvement
  in coefficient of performance (heat removed per unit pumping power).

## Out of scope for Stage 0 / 0.5

- Specific die power maps (to be defined at Stage 1 entry).
- Coolant selection (deionized water assumed as default; to be confirmed).
- Manifold and fitting design.
- Cost or supply-chain constraints.

---

## Constraints (preliminary)

These constraints are indicative. Final values are to be confirmed at Stage 1 entry gate.

| Parameter | Indicative bound | Notes |
|-----------|-----------------|-------|
| Pressure drop | ≤ 50 kPa | Matched to baseline for fair comparison |
| Coolant flow rate | TBD (l/min) | Set to match baseline operating point |
| Maximum wall temperature | TBD (°C) | Driven by device junction limit |
| Footprint | Die-area footprint | Exact dimensions TBD at Stage 1 |
| Feature resolution | ≥ 200 µm | Indicative machining / AM lower bound |
| Material | Copper or aluminum | To be confirmed |

---

## Performance targets (indicative)

Targets are not validated claims. They reflect design intent and will be revised
when baseline simulation data is available.

| Metric | Direction | Baseline reference |
|--------|-----------|-------------------|
| Junction-to-coolant thermal resistance | Minimize | Channel and TPMS baselines |
| Pressure drop (at matched flow) | ≤ baseline | Channel and TPMS baselines |
| Coefficient of performance | Maximize | Channel baseline |
| Temperature uniformity across die | Improve | Channel baseline |

---

## References

Populate via `docs/literature_review_checklist.md`. No quantitative claims are made here
that are not yet supported by reviewed literature or verified simulation data.
