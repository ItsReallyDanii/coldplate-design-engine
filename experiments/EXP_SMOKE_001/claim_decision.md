# EXP_SMOKE_001: Claim Decision

## Labels

- SCREENING_ONLY
- NOT_FULL_CFD
- NOT_FULL_CHT
- NOT_VALIDATED

## Can any design be called scientifically better?

**No.**

This experiment is a bounded smoke test at toy resolution (20^3, 40^3)
using a Darcy-permeability flow model (NOT Navier-Stokes) and a simplified
conduction solver with convective coupling (NOT conjugate heat transfer).

The absolute flow values (velocity, flow rate) are non-physical due to the
permeability model. Only relative comparisons between geometries under
identical matched conditions carry any screening-level meaning.

## What can be stated

Under this specific bounded screening comparison:
- If one geometry showed lower T_peak_solid, it performed better *in this screen*.
- If one geometry showed lower thermal resistance, it performed better *in this screen*.
- Neither result constitutes evidence of superiority in a real thermal system.

## Bugs found

- **channels3d.py axis misalignment**: straight channel generator creates geometry
  perpendicular to the flow axis defined by mesh_or_grid.py. Must be fixed in repo
  before straight-channel baselines are valid.

## What would be required for a real claim

1. Fix axis alignment bug in channels3d.py
2. Resolution >= 100^3 with feature-resolved mesh
3. Navier-Stokes or Stokes-Brinkman flow solver
4. Conjugate heat transfer (fluid + solid energy equations)
5. Non-uniform heat map (hotspot loading)
6. >= 3 baseline families (straight, serpentine, pin-fin)
7. Mesh convergence study
8. Experimental validation or comparison with published correlations
