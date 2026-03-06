# Stage 7 Benchtop Validation Campaign — candidate_02_diamond_2d_s1045

**Campaign status:** NOT STARTED — fabrication not yet procured  
**Primary candidate:** candidate_02_diamond_2d_s1045 (Diamond TPMS, 2D-promoted)  
**Specimen IDs:** S7-C02-001 (primary), S7-C02-002 (repeat)  
**Target test date:** TBD — to be populated when AM vendor confirms delivery of S7-C02-001  
**Operator:** TBD  

---

## Simulation Reference Summary

| Quantity | Value | Source |
|----------|-------|--------|
| R_th (simulated) | 11.27 K/W | Stage 5 thermal smoke, 2 mm domain, Q_total = 4 W |
| ΔP (boundary condition) | 1000 Pa | Stage 4 inlet boundary condition |
| Acceptance band R_th | 5.63 – 22.53 K/W | 0.5× – 2.0× simulated |
| Acceptance band ΔP | 333 – 3000 Pa | 0.33× – 3.0× boundary condition |
| Simulation domain | 2.0 mm (not 5 mm) | See STAGE7-AUD-001, H-2 |
| Pipeline git SHA | 800bba1d1a1911e32fa0f053771068ebce83c970 | See simulation_reference/pipeline_git_sha.txt |

## Specimen Inventory

| Specimen ID | Role | Status |
|-------------|------|--------|
| S7-C02-001 | Primary test specimen | Not procured — awaiting OI-05 |
| S7-C02-002 | Repeat / backup specimen | Not procured — awaiting OI-05 |

## Companion Documents

| Document | Location |
|---------|----------|
| Benchtop Validation Plan | docs/stage7_validation/BENCHTOP_VALIDATION_PLAN.md |
| Artifact Checklist (Pre-Test) | docs/stage7_validation/ARTIFACT_CHECKLIST_PRE_TEST.md |
| Test Matrix | docs/stage7_validation/TEST_MATRIX.md |
| Open Items Closure Order | docs/stage7_validation/OPEN_ITEMS_CLOSURE_ORDER.md |
| Wave 0 / Wave 1 Action Packet | docs/stage7_validation/WAVE0_WAVE1_ACTION_PACKET.md |
| Data Schema (Stage 7) | docs/stage7_validation/DATA_SCHEMA_STAGE7.md |
| Instrumentation and Sensors | docs/stage7_validation/INSTRUMENTATION_AND_SENSORS.md |
| Preflight Verification | docs/stage7_validation/PREFLIGHT_VERIFICATION.md |
| Run Sheet (candidate_02) | docs/stage7_validation/RUN_SHEET_CANDIDATE_02.md |
| Benchtop Execution Checklist | docs/stage7_validation/BENCHTOP_EXECUTION_CHECKLIST.md |
| Post-Run Data Ingest Checklist | docs/stage7_validation/POST_RUN_DATA_INGEST_CHECKLIST.md |
| Audit Memo | docs/stage7_validation/STAGE7_VALIDATION_AUDIT_MEMO.md |
| AM Build Specification | docs/stage7_validation/AM_BUILD_SPECIFICATION.md |

## Simulation Reference Files

| File | Description |
|------|-------------|
| simulation_reference/simulation_reference_candidate_02.json | Locked prediction record (schema v1.1.0) |
| simulation_reference/pipeline_git_sha.txt | Pipeline SHA at time of prediction lock |
| fabrication/stl_export_manifest.json | STL watertight-check manifest (OI-03) |
| fabrication/candidate_02_solid_phase.stl | Watertight solid-phase STL for AM vendor |

## Campaign Verdict

| Phase | Status | R_th verdict | ΔP verdict |
|-------|--------|-------------|-----------|
| A — Pre-test | NOT STARTED | — | — |
| B — Nominal | NOT STARTED | — | — |
| C — Power sweep | NOT STARTED | — | — |

**Overall verdict:** NOT AVAILABLE — test has not been performed.

---

*Update this README after each phase is complete.*
