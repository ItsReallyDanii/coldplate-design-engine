# EXP_SMOKE_005

Graded-threshold diamond TPMS: heat-map-conditioned geometry.

## Grading formula

```
threshold_2d[i,j] = th_base + alpha * (1 - normalized_heatmap[i,j])
volume[i,j,k] = diamond_field[i,j,k] > threshold_2d[i,j]
```

alpha = 0.3, th_base calibrated per heatmap for ~0.47 porosity.

## How to run
```bash
cd coldplate-design-engine
python experiments/EXP_SMOKE_005/run_exp_smoke_005.py
```

## Labels
SCREENING_ONLY / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED
