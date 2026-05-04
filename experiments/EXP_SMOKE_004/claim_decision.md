# EXP_SMOKE_004: Claim Decision

## Labels

- SCREENING_ONLY
- NOT_FULL_CFD
- NOT_FULL_CHT
- NOT_VALIDATED

## Purpose

Heat-map sensitivity test. Does distributed TPMS cooling become more competitive
under non-uniform heating compared with channel-based baselines?

## Can any design be called scientifically better?

**No.**

Same screening-only solver limitations as prior experiments.
Heat maps are synthetic, not derived from real chip thermal measurements.

## What this experiment can show

- Whether diamond TPMS improves in relative rank under hotspot loading
- Whether serpentine's advantage weakens when hotspots miss channel passes
- Whether there's a heat-map-conditioned advantage worth pursuing

## What this experiment cannot show

- Performance under real chip heat maps
- Absolute thermal numbers (solver is screening-grade)
- Whether advantages survive at higher resolution or with roughness

## Heat map provenance

All non-uniform heat maps are SYNTHETIC_HEATMAP. They do not represent real
chip workloads. Conclusions about hotspot response are directional only.
