# EXP_SMOKE_001

Straight channel vs diamond TPMS -- bounded smoke comparison using the
repo's actual scipy.sparse.linalg.spsolve solver path.

## Bug discovered

The repo's `generate_straight_channel_3d` in `channels3d.py` creates channels
perpendicular to the flow axis defined in `mesh_or_grid.py`. This script runs
the repo generator as-is (exposing the bug) plus a corrected flow-aligned baseline.

## How to reproduce

```bash
cd coldplate-design-engine
python experiments/EXP_SMOKE_001/run_exp_smoke_001.py
```

## Requirements

- Python 3.8+
- numpy, scipy (from requirements.txt)

## Outputs

| File | Description |
|------|-------------|
| run_config.json | Experiment configuration, matched conditions, bug documentation |
| geometry_summary.json | Geometry metadata, porosity, connectivity check |
| flow_results.json | Flow metrics per geometry per resolution |
| thermal_results.json | Thermal metrics per geometry per resolution |
| comparison_summary.md | Side-by-side comparison table |
| claim_decision.md | What can and cannot be claimed |

## Labels

All results carry: SCREENING_ONLY / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED

## No repo files modified

This script is read-only with respect to the repo source code.
All outputs are written to this experiment directory only.
