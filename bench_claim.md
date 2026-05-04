# bench_claim.md — Strongest Honest Testable Claim

**Date:** 2026-03-30  
**Evidence standard:** Per AGENT_MISSION.md  

---

## Strongest Honest Claim (one paragraph)

This pipeline generates a diamond TPMS cold-plate geometry from a 2D proxy optimization, promotes it to 3D at 20³ resolution (0.25 mm voxels), runs a simplified Darcy-permeability flow solver and conduction-based thermal solver on a 5 mm domain, and produces structural/manufacturability screening verdicts that pass analytical thresholds. The strongest honest testable claim is: **"A single diamond TPMS cold plate fabricated from the pipeline's geometry will conduct coolant without leaking and produce a measurable thermal resistance within one order of magnitude (0.1× to 10×) of the simulation's prediction."**

Evidence label: **ASSUMED** — no bench data exists.

---

## One Stronger Claim It Does NOT Yet Earn

> "The pipeline can predict cold-plate thermal resistance within 2× of measured values."

**Why not:** The locked simulation reference (SIMREF-C02-001) documents:
- Simulation domain is 2 mm; fabrication target is 5 mm (non-linear scaling uncharacterized)
- Stage 4 flow rate of 44 LPM is **non-physical** (implies 183 m/s through 4 mm²)
- Darcy permeability k=10⁻⁶ m² assigned to fluid voxels has no empirical basis
- The 2× band is aspirational, not earned

---

## One Claim That Would Be Dishonest Right Now

> "The pipeline has been validated against experimental data and demonstrates quantitative thermal-hydraulic accuracy."

**Status:** NOT SUPPORTED. Zero experimental data points exist. Zero bench tests have been run. The pipeline has only been exercised on smoke-test-scale geometry.

---

## Claim Hierarchy

| Level | Claim | Status |
|-------|-------|--------|
| Earned | Pipeline code runs end-to-end and produces outputs | IMPLEMENTED |
| Earned | Geometry passes analytical manufacturability screening | IMPLEMENTED |
| Testable (next) | Fabricated geometry conducts coolant and has R_th within 10× of sim | REQUIRES TEST |
| Aspirational (not yet earned) | R_th prediction within 2× of measured | ASSUMED |
| Dishonest | Quantitative validation demonstrated | NOT SUPPORTED |
