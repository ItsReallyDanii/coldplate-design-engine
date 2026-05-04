# EXP_RESOLUTION_001

Fixed-domain mesh convergence gate for HYBRID_001. Staged and resumable.

## Domain
- Physical: 10.0mm cube (fixed)
- Resolutions: 40^3 (0.25mm), 60^3 (0.167mm), 80^3 (0.125mm)

## Staged execution

```bash
# Stage 1: 40+60 locally (~90 min)
python experiments/EXP_RESOLUTION_001/run_exp_resolution_001.py --max-resolution 60

# Stage 2: 80 overnight (skips 40/60)
python experiments/EXP_RESOLUTION_001/run_exp_resolution_001.py --only-resolution 80 --resume

# Or all at once:
python experiments/EXP_RESOLUTION_001/run_exp_resolution_001.py

# Background (Windows):
start /b python experiments/EXP_RESOLUTION_001/run_exp_resolution_001.py --only-resolution 80 --resume > exp_res_80.log 2>&1

# Background (Linux/Mac):
nohup python experiments/EXP_RESOLUTION_001/run_exp_resolution_001.py --only-resolution 80 --resume > exp_res_80.log 2>&1 &
```

## Labels
SCREENING_ONLY / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED
