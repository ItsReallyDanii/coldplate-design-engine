# coldplate-design-engine

**Status:** Stage 0 complete; Stage 0.5 planning complete; **Stage 1 complete and operational; Stage 2 complete and PASS; Stage 3 complete and PASS; Stage 4 complete and PASS.** Literature population in progress (does not block execution).

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
| 2 | Inverse-design formulation | **Complete (PASS)** |
| 3 | 3-D geometry generation and meshing | **Complete (PASS)** |
| 3.5 | Physical-model corrections and validation | Pending |
| 4 | CFD simulation under matched constraints | **Complete (PASS)** |
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
pytest tests/test_stage1_*.py -v
```

**See full execution guide:** `docs/stage1_execution.md`

**See metric definitions:** `docs/stage1_metric_definitions.md`

**Baseline families implemented:**
- Straight channels
- Serpentine channels
- Pin-fin arrays
- TPMS-adjacent 2D proxies (gyroid-like, diamond-like, primitive-like)

**IMPORTANT:** Stage 1 metrics are screening tools only. Proxy metrics are clearly labeled and do NOT replace CFD/FEA. See metric definitions for limitations.

## Stage 2: Quick Start

Stage 2 implements inverse-design optimization on top of Stage 1 proxy metrics.

**Run smoke test:**
```bash
python src/stage2_inverse/cli.py smoke
```

**Run full comparison (random search vs genetic algorithm):**
```bash
python src/stage2_inverse/cli.py compare configs/stage2_default.yaml
```

**Run tests:**
```bash
pytest tests/test_stage2_*.py -v
```

**See full documentation:**
- `docs/stage2_inverse_design.md` - Problem formulation and objectives
- `docs/stage2_execution.md` - Execution guide and commands

**Stage 2 Results:**
- Genetic algorithm achieves **66.19% improvement** over random search
- Best scores: 2049.64 (GA) vs 1233.31 (random)
- Validity rates: 67% (GA) vs 9% (random)
- **Stage 2 gate: PASS**

**IMPORTANT:** Stage 2 operates on Stage 1 proxy metrics only. Results do NOT establish real thermal or hydraulic superiority. CFD validation (Stages 3-4) is required for physical claims.

## Stage 3: Quick Start

Stage 3 promotes top Stage 2 candidates to 3D parametric geometry with mesh-ready exports.

**Run smoke test:**
```bash
python src/stage3_geometry/cli.py smoke
```

**Run full promotion:**
```bash
python src/stage3_geometry/cli.py promote configs/stage3_default.yaml
```

**Run tests:**
```bash
pytest tests/test_stage3_*.py -v
```

**See full documentation:**
- `docs/stage3_geometry.md` - Stage 3 specification and family mappings
- `docs/stage3_execution.md` - Execution guide and commands

**Stage 3 Results:**
- **All 6 baseline families** promote to true 3D geometry
- TPMS families (gyroid, diamond, primitive) use true 3D implicit surface equations
- Channel families (straight, serpentine, pin-fin) use 3D extrusion/array generation
- Geometry exported as STL (mesh-ready) and raw volumes
- Validation checks confirm connectivity and feature sizes
- **Stage 3 gate: PASS**

**IMPORTANT:** Stage 3 generates 3D geometry only. Results do NOT establish thermal-hydraulic performance. CFD simulation (Stage 4) is required for flow and thermal claims.

## Stage 4: Quick Start

Stage 4 implements flow simulation validation on Stage 3 geometry. **Flow-only** at this stage; thermal coupling not yet implemented.

**Run smoke test:**
```bash
python src/stage4_sim/cli.py smoke
```

**Run on Stage 3 outputs:**
```bash
python src/stage4_sim/cli.py run results/stage3_geometry results/stage4_sim
```

**Run tests:**
```bash
pytest tests/test_stage4_*.py -v
```

**See full documentation:** `docs/stage4_simulation.md`

**Stage 4 Results:**
- **Flow simulation operational** on Stage 3 geometry
- Pressure drop and flow rate computed from actual solver
- Fair comparison under matched boundary conditions
- All quantities honestly labeled (SIMULATED vs GEOMETRIC vs NOT_COMPUTED)
- **Stage 4 gate: PASS**

**IMPORTANT:** Stage 4 provides **flow simulation only**. Thermal simulation not yet implemented. Results enable relative performance ranking but do NOT establish absolute thermal-hydraulic performance. All quantities are clearly labeled.

## Contributing

Follow the claim audit protocol in `claim_audit_v2/` before adding any quantitative performance claims. All claims must be traceable to peer-reviewed literature or internally verified simulation/bench data.
