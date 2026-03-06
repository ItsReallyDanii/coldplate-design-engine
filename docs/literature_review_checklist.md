# Literature Review Checklist

**Stage: 0.5 — in progress.**

This checklist tracks literature survey tasks required before Stage 1 begins.
Each item should be resolved with at least one peer-reviewed citation.
Record citations in the corresponding audit entry in `claim_audit_v2/`.

Priority levels: **H** = high (blocks Stage 0.5 exit), **M** = medium, **L** = low.

---

## 1. Direct-to-chip liquid cooling fundamentals

| # | Topic | Priority | Status | Notes |
|---|-------|----------|--------|-------|
| 1.1 | Single-phase liquid cooling heat transfer fundamentals | H | [ ] | |
| 1.2 | Microchannel heat sink design and performance | H | [ ] | |
| 1.3 | Pressure-drop correlations for microchannels | H | [ ] | |
| 1.4 | Thermal resistance network modeling for cold plates | H | [ ] | |
| 1.5 | Direct-to-chip vs. immersion cooling trade-offs | M | [ ] | |

---

## 2. Baseline geometries

| # | Topic | Priority | Status | Notes |
|---|-------|----------|--------|-------|
| 2.1 | Straight parallel-channel microchannel baselines | H | [ ] | Required for baseline parameter values |
| 2.2 | TPMS geometry types (Gyroid, Schwartz-P, etc.) in heat transfer | H | [ ] | |
| 2.3 | TPMS cold plate fabrication via AM | M | [ ] | |
| 2.4 | Topology-optimized channel layouts for cooling | M | [ ] | |
| 2.5 | Comparison studies across channel / TPMS / topo-opt geometries | H | [ ] | |

---

## 3. Porous media and open-cell structures

| # | Topic | Priority | Status | Notes |
|---|-------|----------|--------|-------|
| 3.1 | Effective thermal conductivity of porous media | H | [ ] | |
| 3.2 | Permeability and Forchheimer coefficients for porous structures | H | [ ] | |
| 3.3 | Nusselt number correlations for porous channel flow | H | [ ] | |
| 3.4 | Metal foam heat exchangers | M | [ ] | |
| 3.5 | Thermal sponge / graded porous media concepts | M | [ ] | See also `thermal_sponge_ref/` |

---

## 4. Inverse design and optimization methods

| # | Topic | Priority | Status | Notes |
|---|-------|----------|--------|-------|
| 4.1 | Density-based topology optimization (SIMP) for fluid-thermal problems | H | [ ] | |
| 4.2 | Level-set methods for topology optimization | M | [ ] | |
| 4.3 | Surrogate-based optimization for thermal design | H | [ ] | |
| 4.4 | Gaussian process / Bayesian optimization for engineering design | M | [ ] | |
| 4.5 | Multi-objective optimization for thermal-hydraulic trade-offs | M | [ ] | |
| 4.6 | Adjoint methods for thermal-fluid sensitivity analysis | L | [ ] | |

---

## 5. CFD and FEA modeling

| # | Topic | Priority | Status | Notes |
|---|-------|----------|--------|-------|
| 5.1 | Navier-Stokes solvers for microfluidic geometries | H | [ ] | |
| 5.2 | Porous-medium CFD approaches (volume-averaging, REV) | H | [ ] | |
| 5.3 | Mesh-independence study practices | M | [ ] | |
| 5.4 | Conjugate heat transfer modeling | H | [ ] | |
| 5.5 | Structural analysis under thermal and pressure loads for cold plates | M | [ ] | |

---

## 6. Manufacturing constraints

| # | Topic | Priority | Status | Notes |
|---|-------|----------|--------|-------|
| 6.1 | CNC machining minimum feature size for copper cold plates | M | [ ] | |
| 6.2 | Selective laser melting / LPBF resolution for Al and Cu | M | [ ] | |
| 6.3 | Design-for-manufacture constraints on porous geometries | M | [ ] | |

---

## Completion criteria

Stage 0.5 exits when:
- All **H** priority items are checked with at least one citation each.
- No uncited quantitative claim from these topics appears in any project document.
