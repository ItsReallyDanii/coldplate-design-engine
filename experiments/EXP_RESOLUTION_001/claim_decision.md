# EXP_RESOLUTION_001: Claim Decision (Updated)

## Labels

- SCREENING_ONLY
- NOT_FULL_CFD
- NOT_FULL_CHT
- NOT_VALIDATED

## Status

Stopped at 40^3 + 60^3. 80^3 not executed.
Automated verdict: PRELIMINARY_AMBIGUOUS.

## Important note

The current screening thermal model uses voxel size `dx` inside the convective coefficient estimate (Re = rho * v * dx / mu). This gate tested resolution stability of the SCREENING FORMULATION, not final physical CHT convergence. Final physical validation still requires laminar N-S + conjugate heat transfer where convective coefficients emerge from the solved flow field, not from a correlation applied per-voxel.

## What this gate showed

- The relative ranking (hybrid_25 beats serpentine on T_peak 3/4 and T_p95 4/4) survived 40-to-60 mesh refinement.
- The ranking did not degrade -- advantages compressed modestly but stayed above threshold on the same 3 heat maps that passed at 40^3.
- Center hotspot is a documented geometry limitation of hybrid_25 at both resolutions.
- Absolute convergence was not achieved (6-9% drift, driven by solver model, not instability).

## What this gate did not show

- Physical convergence of absolute temperature values.
- Whether advantages survive a CHT solver upgrade.
- Roughness or tolerance sensitivity.
- Performance against topology-optimized baselines (B5 deferred).
- Whether the porosity mismatch at 60^3 (serpentine 0.45->0.40) materially affected the comparison.

## Claim tier

> Provisional screening-level technical win, resolution-conditionally-stable. Pending CHT solver upgrade, roughness/tolerance checks, porosity normalization fix, and literature-derived heat map comparison.

## What was NOT claimed

- Publication-grade thermal numbers.
- Physical validation.
- Superiority over Microsoft/Corintis, Yeranee 2022, or any published result.
- MICROCOOL success.
