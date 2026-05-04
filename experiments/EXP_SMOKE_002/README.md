# EXP_SMOKE_002

4-geometry baseline screening comparison: straight channel, serpentine,
pin-fin, and diamond TPMS under matched conditions.

## How to reproduce

```bash
cd coldplate-design-engine
python experiments/EXP_SMOKE_002/run_exp_smoke_002.py
```

## Requirements

- Python 3.8+
- numpy, scipy

## Outputs

| File | Description |
|------|-------------|
| run_config.json | Configuration and matched conditions |
| geometry_summary.json | Geometry metadata, porosity, connectivity |
| flow_results.json | Flow metrics per geometry per resolution |
| thermal_results.json | Thermal metrics per geometry per resolution |
| comparison_summary.md | Side-by-side comparison table |
| claim_decision.md | What can and cannot be claimed |

## Labels

SCREENING_ONLY / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED

## No repo files modified

Read-only with respect to repo source. Outputs to this directory only.
