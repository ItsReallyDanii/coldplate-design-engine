# AM Build Specification — candidate_02_diamond_2d_s1045

**Document ID:** STAGE7-AM-001  
**Date:** 2026-03-06  
**Status:** DRAFT — for vendor RFQ and order placement (OI-05)  
**Candidate:** candidate_02_diamond_2d_s1045 (Diamond TPMS, 2D-promoted)  
**Specimen IDs:** S7-C02-001 (primary), S7-C02-002 (repeat)  
**STL reference:** `results/stage7_benchtop/fabrication/candidate_02_solid_phase.stl`  
**STL manifest:** `results/stage7_benchtop/fabrication/stl_export_manifest.json`  
**Companion documents:** WAVE0_WAVE1_ACTION_PACKET.md (STAGE7-AP-001),
BENCHTOP_VALIDATION_PLAN.md, OPEN_ITEMS_CLOSURE_ORDER.md (STAGE7-OI-001)

> **Scope discipline:** This document introduces no new physics claims and
> no simulation results.  All geometry parameters are derived from existing
> Stage 3 and Stage 6 repository artifacts.  Laser and scan parameters are
> left as vendor-fill fields; the test team does not specify them.

---

## (a) Material

**Specified material:** Aluminum alloy within the vendor's qualified L-PBF
portfolio.  Al 6061 or Al 6082 equivalent is preferred; Al-Si10-Mg (AlSi10Mg)
is acceptable if the vendor's qualification data covers that alloy.

**Requirements:**

- Vendor must supply documented material qualification data covering the
  alloy used (tensile properties, porosity, and surface finish as built).
- Heat treatment: T6 stress relief per AMS 2770 or vendor equivalent after
  build; certificate of conformance required.
- Hardness: vendor to report as-built and post-heat-treat.

**Note:** The structural screening (Stage 6, STAGE7-AUD-001) was conducted
using literature properties for Aluminum 6061-T6 (E = 68.9 GPa,
yield = 276 MPa, allowable = 92 MPa at safety factor 3).  If an
alternate alloy is used, the screening margins must be re-evaluated before
test day.

---

## (b) Minimum Feature Requirement

**Minimum feature size:** ≤ 0.5 mm in the as-built condition.

**Basis:** The remediated Stage 3 geometry uses 0.25 mm voxel pitch,
giving 0.5 mm minimum feature size (2 voxels).  Stage 6 manufacturability
screening confirmed 0.5 mm minimum wall thickness and 0.5 mm minimum
channel diameter (results/stage6_structural_smoke/candidate_02…/structural_metrics.json).

**Vendor requirement:** The vendor must provide documented process capability
evidence demonstrating that their L-PBF process achieves ≤ 0.5 mm resolved
features in the specified aluminum alloy.  Acceptable evidence: published
process qualification report, certified test artifact results, or equivalent.

**Acceptance check:** A CT scan of the primary specimen (S7-C02-001) will be
used to verify internal feature dimensions post-build (OI-07 in
OPEN_ITEMS_CLOSURE_ORDER.md).  The repeat specimen (S7-C02-002) will be
CT scanned only if S7-C02-001 fails CT qualification (geometry deviation ≥ 50%)
or if the test team determines a second geometry verification is required.

---

## (c) Build Orientation

**Nominal orientation:** Specimen upright with coolant-channel axis vertical
(Z-axis of the STL aligned with the build Z-axis).  This minimizes internal
support contact with channel walls.

**Rationale:** The Diamond TPMS channel network is periodic and has no
strongly preferred flow direction.  Build orientation was selected to minimize
support material inside internal channels.

**Vendor confirmation required:** Prior to build start, vendor must confirm
the proposed build orientation based on their support-generation preview.
If an alternate orientation provides better support-removal access to internal
channels, vendor shall propose it in writing; test team must approve before
build proceeds.

**Critical note on channel directionality:** The STL was generated with X/Y
as the 2D plane of the Diamond pattern and Z as the extruded height direction.
If the vendor rotates the STL, the channel orientation relative to the coolant
flow direction will change.  Coordinate any orientation change with the test
team before slicing.

---

## (d) Support Strategy

**Internal channel supports:** Minimize support material inside internal
coolant channels.  Internal supports are difficult to remove and contaminate
the flow path.  If internal supports are unavoidable in the vendor's process,
vendor must flag this before accepting the order.

**External supports:** Standard external supports per vendor practice are
acceptable.

**Powder evacuation:**

- The specimen must have at least one clear powder evacuation access path
  to each internal channel void.
- Vendor must confirm powder evacuation is complete before shipping.
- Vendor must provide a written statement confirming powder removal
  (e.g., weight measurement before and after evacuation, or pressurized
  air blow-out with visual inspection under magnification).
- **Specimens with un-evacuated internal powder must not be shipped.**
  Residual powder blocks coolant flow and causes erroneous flow measurements.

**Inlet/outlet ports:**

- The solid-phase STL (`candidate_02_solid_phase.stl`) represents the
  closed solid body with internal channel voids.  Two inlet/outlet ports
  must be added before slicing.
- Port geometry: rectangular or circular apertures on the top face (Z-max)
  and bottom face (Z-min) of the specimen, aligned with the channel openings
  visible in the STL.  Minimum port area: 1 mm² per port.
- Vendor shall propose port geometry based on their visual inspection of
  the STL and confirm with the test team before slicing.

---

## (e) Post-Processing

| Step | Requirement |
|------|------------|
| Support removal | All external supports removed; internal channel area cleaned per §(d) above |
| Heat treatment | T6 stress relief per AMS 2770 or vendor-qualified equivalent; certificate of conformance supplied |
| Surface finish | Bead blast (Al oxide medium, ≤ 150 µm grit) on external surfaces; internal channels left as-built |
| Inspection | Visual inspection of external surfaces; report any visible cracking, delamination, or incomplete fusion |
| Pressure test (optional) | Vendor may perform a low-pressure leak check (≤ 15 kPa air) if in-house capability exists; result to be reported |

---

## (f) Acceptance Criteria

**Quantity:** Two (2) specimens.

| Specimen ID | Role |
|-------------|------|
| S7-C02-001 | Primary test specimen |
| S7-C02-002 | Repeat / backup |

**Acceptance criteria at time of shipment:**

1. Specimen serial number (S7-C02-001 or S7-C02-002) permanently marked on
   external surface (laser engraving or stamping).
2. External dimensions within ±0.1 mm of nominal 5.0 × 5.0 × 5.0 mm
   (vendor to measure and report).
3. Powder evacuation confirmed in writing by the vendor (see §(d)).
4. Certificate of conformance for T6 heat treatment supplied for each specimen.
5. Material qualification data (see §(a)) supplied.

**Rejection criteria (return to vendor):**

- Any specimen with un-evacuated internal powder.
- External dimensions out of ±0.2 mm tolerance.
- Visible cracks or delamination.
- Missing certificate of conformance.

---

## (g) Laser and Scan Parameters

**Vendor-fill fields.  The test team does not specify laser power, scan speed,
hatch spacing, layer thickness, or beam offset.**

Vendors shall use their standard process parameters qualified for the
specified alloy at the specified minimum feature size (≤ 0.5 mm).  Vendors
must supply a record of the nominal parameters used (for traceability);
these will be archived with the fabrication results but will not be used
as pass/fail criteria by the test team.

---

## Revision History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial release — OI-04 closure |

**End of document.**
