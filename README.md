# coldplate-design-engine

**Status: Stage 0 / Stage 0.5 — repository scaffold and documentation only.**
No CFD code, FEA code, optimization code, or result files are present at this stage.

---

## Project summary

Inverse design of porous internal geometries for direct-to-chip liquid-cooling cold plates.
The objective is to improve thermal-hydraulic performance over standard channel and TPMS
baselines under matched operating constraints, without violating manufacturability bounds.

This is an R&D repository structured for staged development. Each stage has defined entry
and exit criteria documented in `docs/stage_gates.md`.

---

## Repository layout

```
coldplate-design-engine/
├── README.md                      # This file
├── LICENSE
│
├── docs/
│   ├── target_spec.md             # Problem statement, constraints, and performance targets
│   ├── baselines_spec.md          # Baseline geometry types and comparison metrics
│   ├── stage_gates.md             # Gate criteria and deliverables per stage
│   └── literature_review_checklist.md  # Literature survey task list
│
├── src/
│   ├── stage1_2d/                 # Stage 1: 2-D surrogate modeling and parameter sweeps
│   ├── stage2_inverse/            # Stage 2: inverse-design formulation
│   ├── stage3_geometry/           # Stage 3: 3-D geometry generation and meshing
│   ├── stage35_physical/          # Stage 3.5: physical-model corrections and validation
│   ├── stage4_cfd/                # Stage 4: CFD solver interface and post-processing
│   └── stage5_fea/                # Stage 5: FEA structural validation
│
├── baselines/
│   ├── channels/                  # Straight / parallel-channel baseline definitions
│   ├── tpms/                      # TPMS baseline geometry definitions
│   └── topology_opt/              # Topology-optimization baseline definitions
│
├── claim_audit_v2/                # Audit log for performance claims and literature traceability
├── data/                          # Raw measurement and simulation input data
├── results/                       # Simulation and analysis outputs
└── thermal_sponge_ref/            # Reference material for thermal-sponge literature
```

---

## Staged development overview

| Stage | Focus | Status |
|-------|-------|--------|
| 0 / 0.5 | Scaffold, literature review, target specification | **Active** |
| 1 | 2-D surrogate modeling and parameter sweeps | Not started |
| 2 | Inverse-design formulation | Not started |
| 3 | 3-D geometry generation and meshing | Not started |
| 3.5 | Physical-model corrections and validation | Not started |
| 4 | CFD simulation | Not started |
| 5 | FEA structural validation | Not started |

See `docs/stage_gates.md` for entry and exit criteria per stage.

---

## Contributing

Follow the claim audit protocol in `claim_audit_v2/` before adding any
quantitative performance claims. All claims must be traceable to peer-reviewed
literature or internally verified simulation data.
