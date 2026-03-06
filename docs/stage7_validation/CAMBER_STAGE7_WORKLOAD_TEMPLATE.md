# Camber Stage 7 Workload Template

**Document ID:** STAGE7-CW-001  
**Date:** 2026-03-06  
**Status:** PROPOSED (DEFERRED — see Section 4)  
**Companion to:** BENCHTOP_VALIDATION_PLAN.md  

---

## 1. Purpose

This document provides a template for a Camber workload definition in case the team decides to use Camber for artifact management during Stage 7. It is included for completeness. Per the assessment in Section 4, Camber is **not recommended** for Stage 7.

---

## 2. Workload Definition (Template)

If Camber were used, the workload would be structured as follows:

### 2.1 Inputs

| Artifact | Source | Format |
|----------|--------|--------|
| Geometry volume | `results/stage3_geometry_smoke/candidate_02_diamond_2d_s1045/geometry/volume.npy` | NumPy array |
| Stage 3 metadata | `results/stage3_geometry_smoke/candidate_02_diamond_2d_s1045/metadata.json` | JSON |
| Flow metrics | `results/stage4_sim_smoke/candidate_02_diamond_2d_s1045/flow_metrics.json` | JSON |
| Thermal metrics | `results/stage5_thermal_smoke/candidate_02_diamond_2d_s1045/thermal_metrics.json` | JSON |
| Structural metrics | `results/stage6_structural_smoke/candidate_02_diamond_2d_s1045/structural_metrics.json` | JSON |
| Pipeline Git SHA | Repository HEAD at time of simulation | String |

### 2.2 Process Steps

| Step | Description | Automated? |
|------|------------|-----------|
| 1 | Export STL from voxel data (marching cubes) | Could automate |
| 2 | Package geometry + metadata for AM vendor | Manual |
| 3 | Receive fabricated specimen | Manual |
| 4 | Pre-test characterization (CT, mass, dimensions) | Manual |
| 5 | Execute test matrix | Manual |
| 6 | Collect time-series and run summaries | Semi-automated (DAQ) |
| 7 | Compute campaign summary | Could automate |
| 8 | Generate comparison plots | Could automate |
| 9 | Write verdict | Manual |

### 2.3 Outputs

| Artifact | Format | Destination |
|----------|--------|-------------|
| Campaign summary | JSON | `results/stage7_benchtop/analysis/campaign_summary.json` |
| Comparison plots | PNG | `results/stage7_benchtop/analysis/comparison_plots/` |
| Stage 7 verdict | Markdown | `results/stage7_benchtop/analysis/stage7_verdict.md` |

### 2.4 Reproducibility Requirements

| Requirement | How Camber would help | Current alternative |
|-------------|----------------------|---------------------|
| Pin simulation code version | Tag workload to Git SHA | `pipeline_git_sha.txt` in artifact layout |
| Track input→output lineage | Camber DAG | Provenance fields in JSON summaries |
| Re-run automated steps | Camber replay | Shell scripts + documented commands |
| Archive raw data | Camber storage | Git (small files) + external storage (large files) |

---

## 3. Effort Estimate

| Task | Without Camber | With Camber |
|------|---------------|-------------|
| Setup & config | 0 hours | 4–8 hours (learn tool, write workload) |
| Data collection | Same | Same (manual instrumentation) |
| Artifact tracking | 1–2 hours (manual JSON) | Automatic (after setup) |
| Post-processing | 2–4 hours (scripts) | 2–4 hours (same scripts, wrapped in Camber) |
| Total overhead | 0 | 4–8 hours net increase |

---

## 4. Should Camber Be Used Here?

**No.**

### Rationale

1. **Scale:** Stage 7 involves one candidate, one specimen (possibly two), and ~25 test runs. This is a small, linear campaign. Manual artifact tracking per ARTIFACT_LAYOUT.md and DATA_SCHEMA_STAGE7.md is sufficient.

2. **Overhead:** Setting up a Camber workload adds 4–8 hours of configuration with no reduction in test execution time. The test matrix is manually executed (physical instrumentation), so automation benefits are limited to post-processing.

3. **Reproducibility:** The provenance chain is already defined in the data schema (Git SHA, specimen IDs, run IDs). Camber would formalize this but does not add information that is not already captured.

4. **Team size:** At current scale (1–2 people), the coordination overhead that Camber addresses does not exist.

5. **Risk:** Introducing a new tool during a validation campaign adds process risk (learning curve, configuration errors) without corresponding validation benefit.

### When to Revisit

Camber becomes justified when:

- Multiple candidates are tested in parallel (Stage 8+).
- Multi-lot fabrication introduces build-to-build traceability needs.
- Team grows beyond 2–3 people and needs coordinated artifact handoff.
- Automated simulation-to-test comparison pipelines are built.

**Decision: DEFER to Stage 8 planning.**

---

## 5. Document Status

| Item | Status |
|------|--------|
| Workload template | PROPOSED — for reference only |
| Camber adoption | DEFERRED |

---

**End of document.**
