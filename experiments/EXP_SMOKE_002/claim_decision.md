# EXP_SMOKE_002: Claim Decision

## Labels

- SCREENING_ONLY
- NOT_FULL_CFD
- NOT_FULL_CHT
- NOT_VALIDATED

## Can any design be called scientifically better?

**No.**

This experiment is a bounded screening test at toy resolution using a Darcy-permeability
flow model and a simplified conduction solver with convective coupling.

## Interpretation tiers

- **Sanity:** Diamond beats straight channel -> framework runs, not a result.
- **Screening signal:** Diamond beats serpentine AND pin-fin -> worth deeper investigation.
- **No claim yet:** No design is validated until high-fidelity CFD/CHT and non-uniform heat maps.

## Hydraulic vs thermal

Thermal advantage and hydraulic penalty must be tracked separately.
A design that cools better but restricts flow more may not be a net win
under a fixed pumping-power budget. This experiment uses fixed pressure drop,
not fixed pumping power. Results must be interpreted accordingly.

## What would be required for a real claim

1. Resolution >= 100^3
2. Navier-Stokes or Stokes-Brinkman solver
3. Conjugate heat transfer
4. Non-uniform heat maps (hotspot loading)
5. Mesh convergence study
6. Roughness/tolerance sensitivity
7. Comparison against topology-optimized reference baseline
8. Literature grounding
