# Baselines Specification

**Stage: 0 / 0.5 — specification only; no baseline simulations have been run.**

---

## Purpose

This document defines the three baseline geometry categories against which any
proposed inverse-designed geometry will be evaluated. All comparisons must be
conducted under matched operating constraints (see `docs/target_spec.md`).

---

## Baseline categories

### 1. Straight / parallel channels (`baselines/channels/`)

Standard machined microchannels with rectangular cross-section.

| Parameter | Placeholder value | Source |
|-----------|------------------|--------|
| Channel width | TBD (µm) | To be set at Stage 1 |
| Channel depth | TBD (µm) | To be set at Stage 1 |
| Fin width | TBD (µm) | To be set at Stage 1 |
| Number of channels | TBD | To be set at Stage 1 |
| Aspect ratio | TBD | Derived |

Rationale: represents current industry standard for direct-to-chip cooling.

---

### 2. TPMS-based lattice (`baselines/tpms/`)

Triply periodic minimal surface (TPMS) geometry, e.g. Schwartz-P or Gyroid,
used as a structured open-cell porous medium.

| Parameter | Placeholder value | Source |
|-----------|------------------|--------|
| Surface type | TBD (Gyroid / Schwartz-P) | To be selected at Stage 1 |
| Unit cell size | TBD (mm) | To be set at Stage 1 |
| Porosity | TBD | To be set at Stage 1 |
| Wall thickness | TBD (µm) | Derived from unit cell and porosity |

Rationale: represents the current state-of-the-art in AM-fabricated porous cold plates.

---

### 3. Topology-optimized channels (`baselines/topology_opt/`)

Density-based or level-set topology optimization applied to 2-D or 3-D channel
layout, optimizing for thermal resistance subject to pressure-drop constraint.

| Parameter | Placeholder value | Source |
|-----------|------------------|--------|
| Optimization method | TBD (SIMP / level-set) | To be selected at Stage 1 |
| Volume fraction | TBD | To be set at Stage 1 |
| Penalization factor | TBD | To be set at Stage 1 |
| Resolution | TBD (elements) | To be set at Stage 1 |

Rationale: represents an optimization-informed reference point distinct from
hand-designed geometries.

---

## Comparison metrics

All baselines and candidate designs are evaluated on the same set of metrics
under identical boundary conditions.

| Metric | Symbol | Unit | Notes |
|--------|--------|------|-------|
| Junction-to-coolant thermal resistance | R_th | K/W | Primary metric |
| Pressure drop | ΔP | kPa | Constrained to match baseline |
| Coefficient of performance | COP | W_heat / W_pump | Secondary metric |
| Maximum surface temperature | T_max | °C | Safety constraint |
| Temperature non-uniformity | ΔT_surface | K | Uniformity metric |

---

## Notes

- Baseline geometry files (CAD, mesh, or parametric definitions) belong in the
  respective `baselines/` subdirectory.
- No baseline simulation data exists at Stage 0 / 0.5. Populate at Stage 1.
- Any deviation from the matched-constraint comparison protocol must be
  documented in `claim_audit_v2/`.
