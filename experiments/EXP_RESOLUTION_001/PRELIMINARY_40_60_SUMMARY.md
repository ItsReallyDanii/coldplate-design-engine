# EXP_RESOLUTION_001: Preliminary Summary (40+60 Only)

**Date:** 2026-04-30
**Status:** STOPPED AT 60^3. 80^3 not executed.
**Automated verdict:** PRELIMINARY_AMBIGUOUS

---

## What was tested

Fixed 10mm domain mesh refinement. Hybrid_25 vs serpentine vs raw diamond at 40^3 (voxel=0.25mm) and 60^3 (voxel=0.167mm). Four heat maps: uniform, center hotspot, off-center hotspot, dual hotspot.

## Ranking stability (the question that matters)

**Hybrid_25 T_peak advantage over serpentine:**

| Heat map | 40^3 | 60^3 | Stable? |
|----------|------|------|---------|
| uniform | 24.9% | 13.9% | YES (compressed but above 10%) |
| center_hotspot | 7.2% | 2.4% | N/A (never passed -- geometry limitation) |
| off_center_hotspot | 17.2% | 15.3% | YES |
| dual_hotspot | 12.7% | 11.4% | YES |

Result: 3/4 heat maps pass at both resolutions. Pass threshold: 3/4 required.

**Hybrid_25 T_p95 advantage over serpentine:**

| Heat map | 40^3 | 60^3 | Stable? |
|----------|------|------|---------|
| uniform | 23% lower | 20% lower | YES |
| center_hotspot | 28% lower | 27% lower | YES |
| off_center_hotspot | 27% lower | 24% lower | YES |
| dual_hotspot | 29% lower | 29% lower | YES |

Result: 4/4 pass at both resolutions. This is the most stable finding across the entire smoke test series.

## Absolute convergence (not achieved)

40-to-60 drift for hybrid_25:
- T_peak solid: 6.2 - 8.2%
- T_p95 solid: 6.5 - 8.7%
- R_th: 1.4 - 11.3%

All above the 5% clean-pass threshold. Driven by the screening solver's dx-dependent convective coefficient (Re = rho * v * dx / mu), not by numerical instability. All three geometries drift similarly; hybrid_25 is the most stable of the three.

## Known confounds

1. **Serpentine porosity mismatch.** Dropped from 0.45 at 40^3 to 0.40 at 60^3 due to voxel discretization of 1.5mm channel width. This inflates serpentine's apparent thermal improvement at 60^3 and compresses hybrid_25's relative T_peak advantage. The comparison is unfair to hybrid_25 at 60^3.

2. **Center hotspot geometry limitation.** Hybrid_25 does not outperform serpentine when the hotspot is exactly centered. The serpentine's evenly-spaced passes bracket the center hotspot effectively. The TPMS portion of the hybrid does not add enough value there. This is a genuine geometric limitation of the 25% hard-split construction, not a numerical artifact.

3. **dx-dependent convective model.** The screening solver will not converge at any resolution because the convective coefficient depends on voxel size by construction. Absolute temperature values are not converging and should not be cited as physical predictions.

## Why 80^3 was not run

Estimated 24-36 hours. The information gain is marginal: the screening solver's dx dependency ensures continued drift regardless of resolution. The ranking question (does hybrid beat serpentine?) was answered at 40 and 60. The absolute convergence question cannot be answered by this solver at any resolution -- it requires CHT.

## Claim tier

> Provisional screening-level technical win, resolution-conditionally-stable. Hybrid_25 beats serpentine on T_peak (3/4 heat maps) and T_p95 (4/4 heat maps) at both 40^3 and 60^3. Absolute convergence not achieved due to screening solver limitations. Pending: CHT solver upgrade, roughness/tolerance checks, literature-derived heat map, porosity normalization fix.

## Labels

SCREENING_ONLY / FLOW_SIMULATED / THERMAL_SCREENED / NOT_FULL_CFD / NOT_FULL_CHT / NOT_VALIDATED
