# Stage 7 Post-Run Data Ingest Checklist

**Document ID:** STAGE7-DI-001  
**Date:** 2026-03-06  
**Status:** READY FOR USE  
**Candidate:** candidate_02_diamond_2d_s1045  
**Companion documents:** ARTIFACT_LAYOUT.md, DATA_SCHEMA_STAGE7.md,
BENCHTOP_EXECUTION_CHECKLIST.md  

> **Purpose:** Define exactly what must be saved back to the repository after
> each test session.  Complete this checklist immediately after leaving the
> bench.  Do not defer data ingest to the next day.

---

## 1. Immediate Post-Session Actions (Before Leaving Bench)

| # | Action | Done? |
|---|--------|-------|
| 1.1 | Copy all DAQ files (CSV timeseries) from the acquisition computer to a designated portable drive or network share | ☐ |
| 1.2 | Verify file counts: number of CSV files matches number of test runs completed | ☐ |
| 1.3 | Open one timeseries CSV and confirm all 10 columns are present and non-empty | ☐ |
| 1.4 | Copy any bench photos (specimen, fixture, TIM application, damage if any) | ☐ |
| 1.5 | Record end-of-session ambient temperature in the run sheet | ☐ |
| 1.6 | Complete the end-of-session record in RUN_SHEET_CANDIDATE_02.md | ☐ |

---

## 2. Files to Commit to the Repository

All files below go under `results/stage7_benchtop/` following the layout
in ARTIFACT_LAYOUT.md.  Commit each group as a separate git commit with
a descriptive message.  Do not bulk-commit everything in one commit.

### 2.1 Pre-Test Characterization (Phase A)

Commit group label: `data(stage7): Phase A pre-test characterization S7-C02-001`

| # | File | Where to commit | Required? |
|---|------|----------------|----------|
| 2.1.1 | `A-02_mass.json` | `results/stage7_benchtop/test_data/phase_A/` | Required |
| 2.1.2 | `A-03_dimensions.json` | `results/stage7_benchtop/test_data/phase_A/` | Required |
| 2.1.3 | `A-04_powder_evac.json` | `results/stage7_benchtop/test_data/phase_A/` | Required |
| 2.1.4 | `A-05_leak_test.json` | `results/stage7_benchtop/test_data/phase_A/` | Required |
| 2.1.5 | `A-01_ct_scan.json` (reference to external CT report) | `results/stage7_benchtop/test_data/phase_A/` | Required |
| 2.1.6 | `ct_report_S7-C02-001.pdf` (if < 10 MB) | `results/stage7_benchtop/fabrication/specimen_S7-C02-001/ct_scan/` | Required if size allows |
| 2.1.7 | `ct_measurements_S7-C02-001.json` | `results/stage7_benchtop/fabrication/specimen_S7-C02-001/ct_scan/` | Required |

### 2.2 Calibration Records

Commit group label: `data(stage7): instrument calibration records`

| # | File | Where to commit | Required? |
|---|------|----------------|----------|
| 2.2.1 | `fixture_loss_cal.json` | `results/stage7_benchtop/calibration/` | Required |
| 2.2.2 | `thermocouple_cal.json` (day-of ice-bath and boiling-point results) | `results/stage7_benchtop/calibration/` | Required |
| 2.2.3 | `pressure_cal.json` (day-of zero check results) | `results/stage7_benchtop/calibration/` | Required |
| 2.2.4 | `flow_meter_cal.json` (bucket-test result) | `results/stage7_benchtop/calibration/` | Required |
| 2.2.5 | `power_meter_cal.json` (zero check result) | `results/stage7_benchtop/calibration/` | Required |

### 2.3 Timeseries Data (Per Run)

Commit group label: `data(stage7): Phase B timeseries data S7-C02-001`
(one commit per phase if multiple phases run in same session)

| # | File | Where to commit | Required? |
|---|------|----------------|----------|
| 2.3.1 | `B-01-R1_timeseries.csv` | `results/stage7_benchtop/test_data/phase_B/` | Required |
| 2.3.2 | `B-01-R2_timeseries.csv` | `results/stage7_benchtop/test_data/phase_B/` | Required |
| 2.3.3 | `B-01-R3_timeseries.csv` | `results/stage7_benchtop/test_data/phase_B/` | Required |
| 2.3.4 | Additional repeats B-01-R4, R5 if collected | `results/stage7_benchtop/test_data/phase_B/` | Optional |
| 2.3.5 | `B-02-R1_timeseries.csv`, `B-02-R2_timeseries.csv` (same-day repeatability) | `results/stage7_benchtop/test_data/phase_B/` | Optional |
| 2.3.6 | Phase C timeseries files if collected | `results/stage7_benchtop/test_data/phase_C/` | Optional |

### 2.4 Run Summary Records (Per Run)

Same commit as the corresponding timeseries files, or one commit per phase.

| # | File | Where to commit | Schema version | Required? |
|---|------|----------------|---------------|----------|
| 2.4.1 | `B-01-R1_summary.json` | `results/stage7_benchtop/test_data/phase_B/` | 1.0.0 | Required |
| 2.4.2 | `B-01-R2_summary.json` | Same | 1.0.0 | Required |
| 2.4.3 | `B-01-R3_summary.json` | Same | 1.0.0 | Required |
| 2.4.4 | Corresponding summary for any optional runs | — | 1.0.0 | Match data |

**Required fields in every run summary JSON** (from DATA_SCHEMA_STAGE7.md
Section 3):

```json
{
  "schema_version": "1.0.0",
  "test_id": "B-01-R1",
  "candidate_id": "candidate_02_diamond_2d_s1045",
  "specimen_id": "S7-C02-001",
  "phase": "B",
  "date": "<ISO 8601>",
  "operator": "<name>",
  "fabrication_batch": "<batch ID>",
  "ct_scan_id": "<CT scan ID>",
  "conditions": {
    "T_in_C": <float>,
    "P_elec_W": <float>,
    "delta_P_Pa": <float>,
    "Q_LPM": <float>,
    "T_amb_C": <float>
  },
  "derived": {
    "R_th_KW": <float>,
    "delta_P_Pa": <float>,
    "energy_balance_eta": <float>
  },
  "pass_fail": {
    "R_th": "PASS|FAIL",
    "delta_P": "PASS|FAIL",
    "energy_balance": "PASS|FAIL"
  },
  "steady_state_criterion": "T_heater < 0.5 degC/min for 5 min",
  "tim_type": "<type>",
  "tim_lot": "<lot>",
  "tim_contact_resistance_Kcm2W": <float>,
  "notes": ""
}
```

> **Required fields specific to this campaign (not in base schema):**
> `specimen_id`, `fabrication_batch`, `ct_scan_id`, `T_amb_C` in
> conditions, `tim_type`, `tim_lot`, `tim_contact_resistance_Kcm2W`.
> Add these to every run summary as campaign-level extensions under the
> `conditions` and top-level objects.

### 2.5 Simulation Reference Snapshot

Commit once, before the first test run.  Do not update after testing begins.

| # | File | Where to commit | Required? |
|---|------|----------------|----------|
| 2.5.1 | `simulation_reference_candidate_02.json` | `results/stage7_benchtop/simulation_reference/` | Required |
| 2.5.2 | `pipeline_git_sha.txt` | `results/stage7_benchtop/simulation_reference/` | Required |

`pipeline_git_sha.txt` content: the exact git commit SHA of the repo at
the time predictions are locked.  Record as a single line, no trailing
whitespace.

`simulation_reference_candidate_02.json` must include at minimum (per
DATA_SCHEMA_STAGE7.md Section 6, schema v1.1.0):

```json
{
  "schema_version": "1.1.0",
  "candidate_id": "candidate_02_diamond_2d_s1045",
  "stage3_source": "candidate_02_diamond_2d_s1045",
  "simulation_domain_mm": 2.0,
  "thermal_resistance_KW": 11.265617018419787,
  "peak_temperature_C": 70.062468073679156,
  "pressure_drop_Pa": 1000.0,
  "heat_flux_w_m2": 1000000.0,
  "total_power_w": 4.0,
  "porosity": 0.563375,
  "min_feature_size_mm": 0.5,
  "stage6_overall_pass": true,
  "pipeline_git_sha": "<sha>",
  "note_domain_mismatch": "Simulation domain is 2.0 mm; fabrication target is 5.0 mm. Predictions are not directly comparable at the same scale. Acceptance bands account for this."
}
```

### 2.6 Fabrication Records

Commit before test day; update after fabrication is complete.

| # | File | Where to commit | Required? |
|---|------|----------------|----------|
| 2.6.1 | `build_log.md` | `results/stage7_benchtop/fabrication/` | Required |
| 2.6.2 | Photos: `as_built_front.jpg`, `as_built_side.jpg` | `results/stage7_benchtop/fabrication/specimen_S7-C02-001/photos/` | Required (< 5 MB each) |
| 2.6.3 | `pretest_S7-C02-001.json` (pre-test characterization summary) | `results/stage7_benchtop/fabrication/specimen_S7-C02-001/` | Required |

### 2.7 Post-Test Records

Commit same day or next day after test.

| # | File | Where to commit | Required? |
|---|------|----------------|----------|
| 2.7.1 | `E-01_leak_test.json` | `results/stage7_benchtop/test_data/phase_E/` | Required |
| 2.7.2 | `E-02_mass.json` | `results/stage7_benchtop/test_data/phase_E/` | Required |
| 2.7.3 | `E-03_ct_scan.json` (optional post-test CT) | `results/stage7_benchtop/test_data/phase_E/` | Optional |
| 2.7.4 | Post-test photos if damage observed | `results/stage7_benchtop/fabrication/specimen_S7-C02-001/photos/` | If applicable |

### 2.8 Analysis and Campaign Summary

Commit after all run data is ingested and reviewed.

| # | File | Where to commit | Required? |
|---|------|----------------|----------|
| 2.8.1 | `campaign_summary.json` | `results/stage7_benchtop/analysis/` | Required |
| 2.8.2 | `stage7_verdict.md` | `results/stage7_benchtop/analysis/` | Required |
| 2.8.3 | `Rth_measured_vs_predicted.png` | `results/stage7_benchtop/analysis/comparison_plots/` | Required |
| 2.8.4 | `dP_measured_vs_predicted.png` | `results/stage7_benchtop/analysis/comparison_plots/` | Required |
| 2.8.5 | `power_sweep_linearity.png` (if Phase C completed) | `results/stage7_benchtop/analysis/comparison_plots/` | Optional |
| 2.8.6 | `README.md` campaign summary | `results/stage7_benchtop/` | Required |

---

## 3. Files That Must NOT Be Committed

| Category | Reason |
|----------|--------|
| Raw DAQ native-format files (if binary or proprietary format and > 50 MB) | Too large; store externally; reference by ID in run summary |
| CT DICOM / TIFF stacks | Too large; store externally; reference by CT scan ID |
| Intermediate computation scratch files | Not primary artifacts |
| Files with embedded credentials or network paths | Security |

---

## 4. Schema and Integrity Checks Before Push

Before pushing any commit, verify:

| # | Check | Method |
|---|-------|--------|
| 4.1 | All timeseries CSV files have 10 columns with correct headers | Open each file; check header row |
| 4.2 | All run summary JSON files have `schema_version: "1.0.0"` | `grep schema_version results/stage7_benchtop/test_data/**/*.json` |
| 4.3 | Every run summary references a valid `specimen_id` (S7-C02-001) | Manual review |
| 4.4 | Every run summary references a valid `ct_scan_id` | Manual review |
| 4.5 | `pipeline_git_sha.txt` matches the SHA in `simulation_reference_candidate_02.json` | `git log --oneline -1` vs file content |
| 4.6 | No file in `results/stage7_benchtop/` exceeds the size limits in ARTIFACT_LAYOUT.md Section 4.3 | `git diff --stat HEAD` or `du -sh` |
| 4.7 | All outlier or failed runs are present in `_discarded/` subdirectory (not deleted) | `ls results/stage7_benchtop/test_data/phase_*/_discarded/` |
| 4.8 | `campaign_summary.json` counts match the actual number of run files present | Manual cross-check |

---

## 5. Outlier and Failed-Run Handling

- **Outlier run:** Keep in the phase directory.  Add `"notes": "outlier — <reason>"` to
  the run summary JSON.  Include in campaign summary with outlier flag.
- **Failed run** (leak, equipment fault, aborted before steady state): Move to
  `_discarded/` subdirectory within the phase directory.  Create a one-line
  `_discarded/{test_id}_failure_note.txt` recording the reason.
- **No run data is deleted** under any circumstances.

---

## 6. Post-Ingest Sign-Off

| Item | Done? | Notes |
|------|-------|-------|
| All Phase A JSON files committed | ☐ | |
| All calibration records committed | ☐ | |
| All Phase B timeseries CSV committed | ☐ | |
| All Phase B run summary JSON committed | ☐ | |
| Optional phase data committed if collected | ☐ | |
| Simulation reference snapshot committed | ☐ | |
| Fabrication records committed | ☐ | |
| Phase E post-test records committed | ☐ | |
| Schema integrity checks passed | ☐ | |
| Campaign summary and verdict committed | ☐ | |
| PR opened for review | ☐ | |

Completed by: _____________________________  Date: _____________________________

---

## 7. Document Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-06 | Initial release |

**End of document.**
