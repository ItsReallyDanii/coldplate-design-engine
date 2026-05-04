# bench_pass_fail.md — Pass / Ambiguous / Fail Thresholds

**Date:** 2026-03-30  
**Evidence standard:** Per AGENT_MISSION.md  
**Threshold basis:** ASSUMED (provisional) — see justification below  

---

## Why These Thresholds Differ from STAGE7_READINESS_VERDICT.md

The repo's existing verdict document quotes 2× for R_th and 3× for ΔP, based on earlier R_th ≈ 1.03 K/W predictions. However:

1. The **locked simulation reference** (SIMREF-C02-001) gives R_th = 11.27 K/W at 4 W on a **2 mm domain**
2. The **fabrication domain is 5 mm** — a 2.5× linear scaling with non-linear thermal/hydraulic consequences
3. The **Stage 4 flow rate (44 LPM) is documented as non-physical** — ΔP bands cannot be anchored to it
4. Contact resistance, surface roughness, and AM tolerances are unmodeled

The tighter bands are not defensible at this stage. The bands below reflect what the current pipeline evidence can actually support.

---

## Primary Observable: Thermal Resistance (R_th)

**Simulation reference:** R_th_sim = 11.27 K/W (SIMREF-C02-001, 4 W, 2 mm domain)

| Band | R_th range | Ratio to sim | Interpretation |
|------|-----------|-------------|----------------|
| **PASS** | 1.1 – 113 K/W | 0.1× – 10× | Pipeline captures order-of-magnitude physics. Geometry functions as cold plate. |
| **AMBIGUOUS** | 113 – 338 K/W | 10× – 30× | Significant discrepancy. Could be domain mismatch, contact resistance, or model error. Cannot distinguish cause without further investigation. |
| **FAIL** | > 338 K/W or unmeasurable | > 30× | Pipeline's physics model is fundamentally misleading at this geometry scale. |
| **IMMEDIATE STOP** | T_base > 150 °C at 4 W | — | Thermal runaway. Disconnect heater. Root cause before retry. |

**What PASS means:** The geometry works and the simulation is in the right ballpark. Justifies investment in higher-fidelity modeling.  
**What PASS does NOT mean:** The simulation is quantitatively accurate or production-ready.

---

## Secondary Observable: Pressure Drop (ΔP)

**Simulation reference:** ΔP = 1000 Pa (imposed boundary condition, not a prediction)

| Band | Observation | Interpretation |
|------|------------|----------------|
| **PASS** | Measurable, finite, stable ΔP at any flow rate | Geometry conducts coolant. Flow paths are open. |
| **AMBIGUOUS** | ΔP is noisy, drifting, or unstable | Possible flow instability, partial blockage, or air entrainment. |
| **FAIL** | Zero flow (specimen is blocked) or bypass (fluid not entering channels) | Powder entrapment, geometry closure, or port misalignment. |
| **IMMEDIATE STOP** | ΔP > 50 kPa at < 0.01 LPM | Complete blockage. Do not force flow. |

**Note:** Because the simulation's 1000 Pa is a boundary condition (not a prediction) and the simulated flow rate is non-physical, **no quantitative ΔP pass/fail band is defensible.** The test should instead produce a ΔP-vs-Q characteristic curve for comparison with future corrected simulations.

---

## Tertiary Observable: Structural Integrity

| Band | Observation | Interpretation |
|------|------------|----------------|
| **PASS** | No leaks at 2× operating pressure. No visible deformation. | Geometry is structurally sound for bench testing. |
| **FAIL** | Leak through cold plate body (not fittings). Visible deformation. | Fabrication defect or design failure. |

---

## Quaternary Observable: Flow Path Continuity

| Band | Observation | Interpretation |
|------|------------|----------------|
| **PASS** | Fluid passes through cold plate. Outlet temperature rises above inlet under heat load. | Internal channels are open and functional. |
| **AMBIGUOUS** | Fluid passes through but T_out ≈ T_in under heat load | Possible bypass flow — fluid not contacting heated surface. |
| **FAIL** | No fluid at outlet | Blocked channels. Powder entrapment. |

---

## Combined Verdict Logic

```
IF structural_integrity == FAIL:
    VERDICT = FAIL (fabrication/design defect)
    
ELIF flow_continuity == FAIL:
    VERDICT = FAIL (geometry non-functional)
    
ELIF R_th in PASS band AND ΔP == PASS:
    VERDICT = PASS (pipeline is directionally useful)
    
ELIF R_th in AMBIGUOUS band:
    VERDICT = AMBIGUOUS (further investigation needed)
    ACTION = Re-run simulation at fabrication domain, 
             add contact resistance, compare
    
ELIF R_th in FAIL band:
    VERDICT = FAIL (pipeline physics model misleading)
    ACTION = Root cause analysis required
```

---

## Disambiguation: Model Error vs Fabrication Error vs Setup Error

| Observation | Most likely cause | How to distinguish |
|------------|------------------|-------------------|
| R_th 5–10× sim, ΔP reasonable | Model error (permeability, convection) | Re-run sim with corrected domain; if still off, model is wrong |
| R_th > 30× sim, ΔP very high | Fabrication error (blocked channels) | µCT scan to check internal geometry |
| R_th > 30× sim, ΔP low | Setup error (poor thermal contact) | Re-mount with verified thermal interface |
| R_th matches but energy balance fails | Setup error (heat loss to environment) | Insulate fixture, repeat |
| No flow at all | Fabrication error (powder entrapment) | µCT scan; try flushing with compressed air |
