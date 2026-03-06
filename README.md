# coldplate-design-engine

**Status:** Stage 0 complete; Stage 0.5 in progress. Documentation only—no CFD, FEA, or optimization results are present yet.

Inverse design of internal porous and channel architectures for direct-to-chip liquid-cooling cold plates, evaluated against matched channel and TPMS baselines. This repository is independent of Thermal-Sponge; `thermal_sponge_ref/` is reference material only.

## Repository layout

- `docs/` — target, baseline, stage-gate, and literature-review specifications.
- `baselines/` — reference geometry families (`channels/`, `tpms/`, `topology_opt/`).
- `src/` — staged code placeholders (`stage1_2d/`, `stage2_inverse/`, `stage3_geometry/`, `stage35_physical/`, `stage4_cfd/`, `stage5_fea/`).
- `claim_audit_v2/` — traceability for quantitative claims.
- `data/`, `results/` — inputs and outputs for future stages.
- `thermal_sponge_ref/` — literature reference archive; not shared code or results.

## Staged roadmap (summary)

| Stage | Focus | Status |
|-------|-------|--------|
| 0 | Scaffold, target, and baseline documentation | Complete |
| 0.5 | Literature review and constraint locking | In progress |
| 1 | 2-D surrogate modeling and parameter sweeps | Pending |
| 2 | Inverse-design formulation | Pending |
| 3 | 3-D geometry generation and meshing | Pending |
| 3.5 | Physical-model corrections and validation | Pending |
| 4 | CFD simulation under matched constraints | Pending |
| 5 | FEA structural validation | Pending |
| 6 | Prototype fabrication and bench testing | Pending |
| 7 | System integration and reliability screening | Pending |
| 8 | Release and handoff with audited claims | Pending |

See `docs/stage_gates.md` for detailed gate criteria.

## Contributing

Follow the claim audit protocol in `claim_audit_v2/` before adding any quantitative performance claims. All claims must be traceable to peer-reviewed literature or internally verified simulation/bench data.
