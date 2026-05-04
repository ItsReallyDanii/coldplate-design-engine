# EXP_SMOKE_003: Claim Decision

## Labels

- SCREENING_ONLY
- NOT_FULL_CFD
- NOT_FULL_CHT
- NOT_VALIDATED

## Purpose

Fairness control. EXP_SMOKE_002 had wildly mismatched porosity (pin-fin 80-95%
vs diamond 49%). This experiment constrains all geometries to ~0.45-0.50 porosity.

## Can any design be called scientifically better?

**No.**

Same screening-only solver limitations as prior experiments. Porosity matching
removes ONE confound (fluid volume fraction) but does not address solver fidelity,
resolution adequacy, non-uniform heat maps, or physical validation.

## Interpretation tiers (unchanged)

- Sanity: diamond beats straight
- Screening signal: diamond beats serpentine AND pin-fin at matched porosity
- No claim without high-fidelity CFD/CHT and non-uniform heat maps

## What this experiment can show

Whether diamond TPMS geometry has an inherent thermal or hydraulic advantage
over simpler channel families when fluid volume fraction is controlled.

## What this experiment cannot show

Whether that advantage survives at higher resolution, under roughness,
or with a real CFD solver. Those are separate experiments.
