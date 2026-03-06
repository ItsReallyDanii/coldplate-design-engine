# coldplate-design-engine

**Status:** Stage 0 complete; Stage 0.5 planning complete; **Stage 1 implementation complete and operational.** Literature population in progress (does not block Stage 1 execution).

Inverse design of internal porous and channel architectures for direct-to-chip liquid-cooling cold plates, evaluated against matched channel and TPMS baselines. This repository is independent of Thermal-Sponge; `thermal_sponge_ref/` is reference material only.

**Tracked design hypothesis:** Functionally graded internal structures with spatially varying porosity fields are now tracked as a candidate design direction. This approach is not yet validated; it represents a hypothesis that non-uniform thermal and mechanical loading may benefit from graded internal structure. The target specification remains unchanged, and graded structures will be evaluated against uniform and segmented TPMS baselines when Stage 2-4 simulations become available.

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
| 0.5 | Literature review and constraint locking | Complete |
| 1 | 2-D surrogate modeling and parameter sweeps | **Complete** |
| 2 | Inverse-design formulation | Pending |
| 3 | 3-D geometry generation and meshing | Pending |
| 3.5 | Physical-model corrections and validation | Pending |
| 4 | CFD simulation under matched constraints | Pending |
| 5 | FEA structural validation | Pending |
| 6 | Prototype fabrication and bench testing | Pending |
| 7 | System integration and reliability screening | Pending |
| 8 | Release and handoff with audited claims | Pending |

See `docs/stage_gates.md` for detailed gate criteria.

## Stage 1: Quick Start

Stage 1 implements 2D baseline geometry generation, metric computation, and parameter sweeps.

**Run smoke test:**
```bash
pip install -e .
python src/stage1_2d/cli.py smoke
```

**Run parameter sweep:**
```bash
python src/stage1_2d/cli.py sweep configs/stage1_default.yaml
```

**Run tests:**
```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

**See full execution guide:** `docs/stage1_execution.md`

**See metric definitions:** `docs/stage1_metric_definitions.md`

**Baseline families implemented:**
- Straight channels
- Serpentine channels
- Pin-fin arrays
- TPMS-adjacent 2D proxies (gyroid-like, diamond-like, primitive-like)

**IMPORTANT:** Stage 1 metrics are screening tools only. Proxy metrics are clearly labeled and do NOT replace CFD/FEA. See metric definitions for limitations.

## Contributing

Follow the claim audit protocol in `claim_audit_v2/` before adding any quantitative performance claims. All claims must be traceable to peer-reviewed literature or internally verified simulation/bench data.
