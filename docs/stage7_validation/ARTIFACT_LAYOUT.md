# Stage 7 Artifact Layout

**Document ID:** STAGE7-AL-001  
**Date:** 2026-03-06  
**Status:** PROPOSED  
**Companion to:** DATA_SCHEMA_STAGE7.md  

---

## 1. Purpose

Define the directory structure, naming conventions, and provenance chain for all Stage 7 artifacts. Every file produced during Stage 7 must be traceable to its source (simulation prediction, fabrication batch, test run).

---

## 2. Directory Structure

```
results/stage7_benchtop/
├── README.md                                  # Summary of campaign and status
├── simulation_reference/
│   ├── simulation_reference_candidate_02.json # Snapshot of Stage 3-6 predictions
│   └── pipeline_git_sha.txt                   # Git SHA of pipeline code used
│
├── fabrication/
│   ├── build_log.md                           # AM build parameters and notes
│   ├── specimen_S7-C02-001/
│   │   ├── pretest_S7-C02-001.json            # Pre-test characterization
│   │   ├── ct_scan/
│   │   │   ├── ct_report_S7-C02-001.pdf       # CT scan report
│   │   │   └── ct_measurements_S7-C02-001.json# Extracted dimensional data
│   │   └── photos/
│   │       ├── as_built_front.jpg
│   │       └── as_built_side.jpg
│   └── specimen_S7-C02-002/                   # (If second specimen fabricated)
│       └── ...
│
├── test_data/
│   ├── phase_A/                               # Pre-test characterization runs
│   │   ├── A-01_ct_scan.json                  # Reference to CT scan
│   │   ├── A-02_mass.json
│   │   ├── A-03_dimensions.json
│   │   ├── A-04_powder_evac.json
│   │   └── A-05_leak_test.json
│   │
│   ├── phase_B/                               # Nominal condition
│   │   ├── B-01-R1_timeseries.csv
│   │   ├── B-01-R1_summary.json
│   │   ├── B-01-R2_timeseries.csv
│   │   ├── B-01-R2_summary.json
│   │   ├── B-01-R3_timeseries.csv
│   │   ├── B-01-R3_summary.json
│   │   ├── B-02-R1_timeseries.csv
│   │   ├── B-02-R1_summary.json
│   │   ├── B-02-R2_timeseries.csv
│   │   └── B-02-R2_summary.json
│   │
│   ├── phase_C/                               # Power sweep
│   │   ├── C-01-R1_timeseries.csv
│   │   ├── C-01-R1_summary.json
│   │   ├── C-01-R2_timeseries.csv
│   │   ├── C-01-R2_summary.json
│   │   ├── C-02-R1_timeseries.csv
│   │   ├── C-02-R1_summary.json
│   │   ├── C-02-R2_timeseries.csv
│   │   └── C-02-R2_summary.json
│   │
│   ├── phase_D/                               # Flow sweep
│   │   ├── D-01-R1_timeseries.csv
│   │   ├── D-01-R1_summary.json
│   │   ├── D-01-R2_timeseries.csv
│   │   ├── D-01-R2_summary.json
│   │   ├── D-02-R1_timeseries.csv
│   │   ├── D-02-R1_summary.json
│   │   ├── D-02-R2_timeseries.csv
│   │   ├── D-02-R2_summary.json
│   │   ├── D-03-R1_timeseries.csv
│   │   ├── D-03-R1_summary.json
│   │   ├── D-03-R2_timeseries.csv
│   │   └── D-03-R2_summary.json
│   │
│   └── phase_E/                               # Post-test characterization
│       ├── E-01_leak_test.json
│       ├── E-02_mass.json
│       └── E-03_ct_scan.json                  # (Optional)
│
├── analysis/
│   ├── campaign_summary.json                  # Aggregate results, pass/fail
│   ├── comparison_plots/
│   │   ├── Rth_measured_vs_predicted.png
│   │   ├── dP_measured_vs_predicted.png
│   │   └── power_sweep_linearity.png
│   └── stage7_verdict.md                      # Final pass/fail determination
│
└── calibration/
    ├── thermocouple_cal.json
    ├── pressure_cal.json
    ├── flow_meter_cal.json
    └── power_meter_cal.json
```

---

## 3. Naming Conventions

### 3.1 Test IDs

Format: `{Phase}-{Test Number}-R{Repeat}`

| Component | Values | Example |
|-----------|--------|---------|
| Phase | A, B, C, D, E | B |
| Test number | 01, 02, 03... | 01 |
| Repeat | R1, R2, R3... | R1 |
| Full ID | | B-01-R1 |

### 3.2 Specimen IDs

Format: `S7-C{candidate_number}-{sequence}`

| Component | Values | Example |
|-----------|--------|---------|
| Stage | S7 | S7 |
| Candidate | C01, C02 | C02 |
| Sequence | 001, 002... | 001 |
| Full ID | | S7-C02-001 |

### 3.3 File Names

Format: `{test_id}_{descriptor}.{ext}`

| Descriptor | Extension | Content |
|-----------|-----------|---------|
| timeseries | .csv | Raw time-series data |
| summary | .json | Per-run derived quantities |
| ct_scan | .json | CT measurement data |
| mass | .json | Mass measurement |
| dimensions | .json | External dimension measurement |
| leak_test | .json | Leak test result |
| powder_evac | .json | Powder evacuation check |

---

## 4. Provenance Chain

### 4.1 Traceability Flow

```
Stage 3 geometry (volume.npy)
  ↓ [geometry_source in run summary]
Stage 4 flow simulation (flow_metrics.json)
  ↓ [embedded in simulation_reference]
Stage 5 thermal simulation (thermal_metrics.json)
  ↓ [embedded in simulation_reference]
Stage 6 structural screening (structural_metrics.json)
  ↓ [embedded in simulation_reference]
Simulation reference snapshot (simulation_reference_candidate_02.json)
  ↓ [pipeline_git_sha links to exact code version]
STL export → AM fabrication → Physical specimen
  ↓ [fabrication_batch, specimen_id in run summary]
Pre-test CT scan → As-built characterization
  ↓ [ct_scan_id in run summary]
Test runs → Time-series + summary
  ↓ [test_id links to condition and repeat]
Campaign summary → Verdict
  ↓ [aggregates all run summaries]
Stage 7 verdict (stage7_verdict.md)
```

### 4.2 Immutable References

The following must be recorded before any test is run and must not change during the campaign:

| Reference | Where recorded | Purpose |
|-----------|---------------|---------|
| Pipeline Git SHA | `pipeline_git_sha.txt` | Exact code version for simulation predictions |
| Stage 3 geometry path | `simulation_reference_candidate_02.json` | Links physical specimen to digital geometry |
| Fabrication batch ID | `build_log.md`, all run summaries | Links specimen to AM build |
| Specimen ID | All run summaries, pre-test records | Links test data to physical part |
| CT scan ID | Pre-test record, all run summaries | Links dimensional data to specific scan |

### 4.3 What Gets Committed to Git

| Category | Committed? | Notes |
|----------|-----------|-------|
| Simulation reference | Yes | Snapshot of predictions, lightweight |
| Build log | Yes | Text, small |
| Pre-test characterization (JSON) | Yes | Structured data, small |
| CT scan images (DICOM/TIFF) | No | Too large; store externally, reference by ID |
| CT scan report (PDF) | Yes (if < 10 MB) | Summary document |
| Time-series CSV | Yes (if < 50 MB total) | Primary data |
| Run summaries (JSON) | Yes | Small, structured |
| Campaign summary | Yes | Aggregate |
| Verdict document | Yes | Final assessment |
| Calibration records | Yes | Small, essential for reproducibility |
| Photos | Yes (if < 5 MB each) | Specimen documentation |

---

## 5. Archival Rules

1. **No data deletion.** All test runs, including outliers and failed runs, are archived.
2. **Outlier runs** are tagged in their summary JSON (`"notes": "outlier — reason"`) but not removed from the dataset.
3. **Failed runs** (e.g., leak, equipment malfunction) are stored in a `_discarded/` subdirectory within their phase directory, with a note explaining the failure.
4. **Raw DAQ files** (native format from acquisition software) are stored alongside CSV conversions if format differs.

---

## 6. Integrity Checks

Before declaring the campaign complete, verify:

| Check | How |
|-------|-----|
| All run summaries present | Count JSON files vs test matrix |
| All time-series present | Count CSV files vs test matrix |
| Schema version consistent | All JSONs have `schema_version: "1.0.0"` |
| Provenance chain intact | Every run summary references valid specimen_id, ct_scan_id, fabrication_batch |
| No orphan files | Every file in test_data/ has a corresponding entry in campaign_summary.json |
| Git SHA matches | `pipeline_git_sha.txt` matches SHA in simulation reference |

---

## 7. Document Status

| Item | Status |
|------|--------|
| Layout definition | PROPOSED — this document |
| Directory creation | NOT STARTED |
| Artifact population | NOT STARTED |

---

**End of document.**
