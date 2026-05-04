# EXP_SMOKE_003

Porosity-matched 4-geometry screening comparison.

## Why this experiment

EXP_SMOKE_002 had uncontrolled porosity: pin-fin was 80-95% fluid while
diamond was 49%. Pin-fin won everything trivially. This experiment fixes
all geometries to ~0.45-0.50 porosity so the comparison is geometry vs geometry,
not more-fluid vs less-fluid.

## How to reproduce

```bash
cd coldplate-design-engine
python experiments/EXP_SMOKE_003/run_exp_smoke_003.py
```

## Requirements

- Python 3.8+
- numpy, scipy

## Labels

SCREENING_ONLY / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED
