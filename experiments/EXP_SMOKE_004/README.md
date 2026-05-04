# EXP_SMOKE_004

Non-uniform heat map screening: does TPMS distributed cooling improve under hotspots?

## Why this experiment

SMOKE_003 showed serpentine beats diamond under uniform heating. But uniform
heating inherently advantages geometries with channels parallel to the heated face.
Real chip loads are non-uniform. This experiment tests whether TPMS's distributed
fluid network handles hotspots better than channel-based designs.

## Heat map cases

1. uniform: same as SMOKE_003 (baseline comparison)
2. center_hotspot: Gaussian at domain center, peak/mean ~3
3. off_center_hotspot: Gaussian at (nx/4, ny/4), between serpentine passes
4. dual_hotspot: two Gaussians at (1/3, 1/3) and (2/3, 2/3)

Total watts are normalized across all cases.

## How to reproduce

```bash
cd coldplate-design-engine
python experiments/EXP_SMOKE_004/run_exp_smoke_004.py
```

## Labels

SCREENING_ONLY / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED
