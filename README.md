# coldplate-design-engine

![Status](https://img.shields.io/badge/status-stage--7--conditional--proceed-orange)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Validation](https://img.shields.io/badge/validation-claim--audited-blueviolet)
![Hardware](https://img.shields.io/badge/hardware--validation-not--yet--performed-lightgrey)

**A stage-gated inverse-design pipeline for TPMS-inspired liquid cold plates.**

`coldplate-design-engine` explores internal porous and channel architectures for direct-to-chip liquid cooling. The project implements a staged workflow from target specification and 2D surrogate screening through inverse design, 3D geometry generation, flow simulation, thermal screening, structural/manufacturability screening, and bench-readiness planning.

The current result is **not hardware validation**. It is a bounded, claim-audited computational pipeline that produces candidate geometries, screening metrics, and a Stage 7 prototype-readiness assessment.

---

## Current status

**Stage 7 readiness: CONDITIONAL PROCEED**

Stages 1–6 are implemented and documented as PASS/complete under their scoped criteria. Stage 7 has been assessed as **CONDITIONAL PROCEED**, blocked by one critical requirement:

> Actual Stage 3 geometry must be loaded into Stage 6 manufacturability screening before any prototype decision is final.

No fabricated prototype has been tested yet. No experimental thermal-hydraulic validation is claimed.

---

## Why this exists

Liquid cold plates are constrained by competing objectives:

- maximize heat transfer area
- preserve flow connectivity
- reduce hydraulic resistance
- avoid dead zones
- satisfy manufacturability limits
- survive thermal and pressure loading

This repository turns that into a staged design pipeline where every major claim is assigned a scope:

- **GEOMETRIC**
- **SIMULATED**
- **FLOW_SIMULATED**
- **ANALYTICAL**
- **SCREENING**
- **NOT_COMPUTED**
- **NOT_VALIDATED**

The goal is not to pretend screening models are physical proof. The goal is to prevent weak evidence from being promoted into strong claims.

---

## Pipeline overview

```text
Target specification
    ↓
2D surrogate geometry screening
    ↓
Inverse design optimization
    ↓
3D geometry generation and STL export
    ↓
Flow simulation under matched constraints
    ↓
Thermal screening with flow-informed coupling
    ↓
Structural and manufacturability screening
    ↓
Prototype readiness assessment
```

---

## Stage-gate summary

| Stage | Focus | Implementation | Tests | Status |
|---|---|---:|---:|---|
| 0 / 0.5 | Target specification, literature, constraints | Docs | — | Complete |
| 1 | 2D surrogate screening | 11 modules | 48 | PASS |
| 2 | Inverse design optimization | 9 modules | 56 | PASS |
| 3 | 3D geometry generation + STL export | 10 modules | 29 | PASS |
| 3.5 | Physical corrections / documented modeling updates | Docs | — | Complete |
| 4 | Flow simulation using Darcy-style screening solver | 10 modules | 24 | PASS |
| 5 | Thermal screening with flow-informed coupling | 10 modules | 14 | PASS |
| 6 | Structural + manufacturability screening | 10 modules | 25 | PASS |
| 7 | Prototype readiness assessment | Docs | — | CONDITIONAL PROCEED |

Total extracted source/test inventory:

- **60 source modules**
- **206 test functions**
- **17 test files**
- staged packages across `stage1_2d` through `stage6_structural`

---

## Implemented design families

Stage 1 and Stage 3 support matched baseline and TPMS-inspired geometry families:

| Family | Type | Notes |
|---|---|---|
| Straight channel | Channel baseline | Simple direct-flow baseline |
| Serpentine channel | Channel baseline | Longer path / increased contact |
| Pin-fin array | Channel/feature baseline | Discrete internal obstacles |
| Gyroid | TPMS-inspired | 3D implicit surface generation |
| Diamond | TPMS-inspired | 3D implicit surface generation |
| Primitive | TPMS-inspired | 3D implicit surface generation |

Stage 3 promotes selected 2D candidates into 3D geometry and mesh-ready exports.

---

## Key candidate results

Two diamond-family candidates reached Stage 7 readiness assessment.

| Metric | `candidate_01_diamond_2d_s1127` | `candidate_02_diamond_2d_s1045` | Label |
|---|---:|---:|---|
| Thermal resistance | 1.0350 K/W | **1.0296 K/W** | SCREENING |
| Peak temperature | 50.87 °C | **50.74 °C** | SCREENING |
| Pressure drop | 1000 Pa | 1000 Pa | IMPOSED BC |
| Flow rate | 105.4 LPM | **108.0 LPM** | SIMULATED / non-physical absolute scale |
| Combined stress | 32.4 MPa | **32.3 MPa** | ANALYTICAL |
| Allowable stress | 92 MPa | 92 MPa | Literature material property |
| Margin of safety | 1.84× | **1.85×** | ANALYTICAL |
| Deflection | 0.00002 mm | 0.00002 mm | ANALYTICAL |
| Temperature uniformity CV | 12.2% | **12.1%** | SCREENING |
| Fluid connectivity | **97.4%** | 97.3% | GEOMETRIC |
| Manufacturability | UNKNOWN | UNKNOWN | Requires real geometry screening |
| Overall status | CONDITIONAL | CONDITIONAL | Stage 7 |

**Priority candidate:** `candidate_02_diamond_2d_s1045`

It is the current preferred candidate because it has the best thermal resistance, lowest peak temperature, highest simulated flow rate, and slightly higher analytical structural margin within the screened set.

---

## What is proven vs not proven

### Supported by the repository

| Claim | Status |
|---|---|
| The stage-gated pipeline runs from 2D screening through structural/manufacturability assessment | Supported |
| Genetic algorithm inverse design improves proxy objective score over random search | Supported |
| Six baseline/TPMS geometry families are implemented | Supported |
| Two diamond candidates passed analytical structural screening | Supported |
| Candidate 02 is the current best screened candidate | Supported |
| Stage 7 readiness is conditional, not complete | Supported |
| Claim labels distinguish geometry, simulation, analytical screening, and validation status | Supported |

### Not claimed

| Claim | Status |
|---|---|
| Hardware validation has been completed | Not supported |
| Fabricated prototype exists | Not supported |
| Bench testing has been performed | Not supported |
| Full Navier-Stokes CFD is implemented | Not supported |
| Full conjugate heat transfer is implemented | Not supported |
| Fluid energy equation is solved | Not supported |
| Full FEA structural validation is implemented | Not supported |
| Real-geometry manufacturability is confirmed | Not supported |
| Production readiness is established | Not supported |

---

## Solver and model boundaries

| Stage | Method | What it is | What it is not |
|---|---|---|---|
| Stage 4 flow | Darcy-style permeability solver | Comparative flow screening | Full Navier-Stokes CFD |
| Stage 5 thermal | Steady-state conduction + flow-informed convective coupling | Thermal screening | Full conjugate heat transfer |
| Stage 6 structural | Analytical stress and manufacturability formulas | Plausibility screening | Finite element analysis |
| Stage 7 readiness | Documentation and decision gate | Prototype-readiness planning | Experimental validation |

These boundaries are intentional. The repository is designed to keep early-stage engineering claims honest.

---

## Quick start

Install dependencies:

```bash
pip install -e .
pip install -r requirements-dev.txt
```

Run Stage 1 smoke test:

```bash
python src/stage1_2d/cli.py smoke
```

Run Stage 2 inverse-design comparison:

```bash
python src/stage2_inverse/cli.py compare configs/stage2_default.yaml
```

Promote candidates to 3D geometry:

```bash
python src/stage3_geometry/cli.py promote configs/stage3_default.yaml
```

Run Stage 4 flow simulation:

```bash
python src/stage4_sim/cli.py run results/stage3_geometry results/stage4_sim
```

Run Stage 5 thermal screening:

```bash
python src/stage5_thermal/cli.py run results/stage4_sim_full --output results/stage5_thermal
```

Run Stage 6 structural/manufacturability screening:

```bash
python src/stage6_structural/cli.py run results/stage5_thermal --output results/stage6_structural
```

Run tests:

```bash
python -m pytest tests/ -q
```

---

## Repository layout

```text
coldplate-design-engine/
├── baselines/
│   ├── channels/
│   ├── tpms/
│   └── topology_opt/
├── claim_audit_v2/
├── configs/
├── data/
├── docs/
├── results/
├── src/
│   ├── stage1_2d/
│   ├── stage2_inverse/
│   ├── stage3_geometry/
│   ├── stage35_physical/
│   ├── stage4_sim/
│   ├── stage5_thermal/
│   └── stage6_structural/
├── tests/
├── STAGE6_INDEPENDENT_VERIFICATION.md
├── STAGE7_READINESS_VERDICT.md
├── bench_claim.md
├── bench_measurement_plan.md
├── bench_pass_fail.md
└── README.md
```

---

## Main evidence files

| File | Purpose |
|---|---|
| `docs/target_spec.md` | Target, scope, and non-goals |
| `docs/stage_gates.md` | Stage-gate plan and pass/kill criteria |
| `docs/stage2_verdict.md` | Stage 2 inverse-design verdict |
| `docs/stage3_verdict.md` | Stage 3 geometry verdict |
| `docs/STAGE4_VERDICT.md` | Flow simulation scope and verdict |
| `docs/STAGE5_VERDICT.md` | Thermal screening scope and verdict |
| `docs/STAGE6_VERDICT.md` | Structural/manufacturability screening verdict |
| `STAGE6_INDEPENDENT_VERIFICATION.md` | Independent verification of Stage 6 |
| `STAGE7_READINESS_VERDICT.md` | Stage 7 conditional readiness assessment |
| `bench_claim.md` | Earned/testable/dishonest claim hierarchy |
| `bench_measurement_plan.md` | Proposed bench validation procedure |
| `bench_hidden_assumptions.md` | Known modeling assumptions |
| `claim_audit_v2/` | Claim traceability and audit material |

---

## Stage 7 readiness

Stage 7 is currently **CONDITIONAL PROCEED**.

The two screened diamond candidates are plausible enough to justify the next readiness step, but the current blocker is real-geometry manufacturability.

Required before prototype decision:

1. Load actual Stage 3 voxel geometry into Stage 6.
2. Re-run structural/manufacturability screening on real geometry.
3. Verify at least one candidate passes manufacturability.
4. Generate final fabrication-ready geometry.
5. Proceed to bench planning only after the real-geometry gate passes.

Planned bench validation target:

- directional agreement, not quantitative production certification
- thermal agreement within broad bounds
- hydraulic agreement within broad bounds
- no leak or structural failure
- evidence suitable for model refinement

---

## Technical paper target

This repository is being prepared as a short technical methods paper:

> **A Stage-Gated Inverse-Design Pipeline for TPMS-Inspired Liquid Cold Plates**

The paper will frame this project as a bounded engineering workflow, not a finished hardware product.

---

## Citation

Suggested citation:

```text
Sleiman, D. (2026). coldplate-design-engine: A Stage-Gated Inverse-Design Pipeline for TPMS-Inspired Liquid Cold Plates. GitHub repository.
https://github.com/ItsReallyDanii/coldplate-design-engine
```

---

## Claim policy

Do not add or promote quantitative performance claims unless they are traceable to one of:

1. internally verified simulation output,
2. documented analytical screening,
3. committed benchmark/test output,
4. peer-reviewed literature,
5. future experimental bench data.

Simulation results must remain labeled as simulation or screening results. Analytical screening must not be described as FEA. Stage 7 conditional readiness must not be described as hardware validation.

---

## Current verdict

`coldplate-design-engine` is a serious stage-gated engineering research artifact.

It has:

- implemented staged design logic,
- multiple geometry families,
- inverse-design optimization,
- 3D TPMS geometry generation,
- flow and thermal screening,
- structural/manufacturability checks,
- claim-audited documentation,
- and a clear next gate toward bench validation.

It has **not** yet produced experimental hardware validation.

That distinction is the project’s strength.
