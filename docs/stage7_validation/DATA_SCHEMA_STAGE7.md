# Stage 7 Data Schema

**Document ID:** STAGE7-DS-001  
**Date:** 2026-03-06  
**Status:** PROPOSED  
**Companion to:** BENCHTOP_VALIDATION_PLAN.md, ARTIFACT_LAYOUT.md  

---

## 1. Purpose

Define the data formats, field names, and provenance metadata for all Stage 7 benchtop validation artifacts. All data files must conform to these schemas to enable automated comparison against simulation predictions.

---

## 2. Time-Series Data (Per Run)

### 2.1 File Format

- **Format:** CSV, UTF-8 encoded, Unix line endings (LF).
- **Header:** First row is column names.
- **Delimiter:** Comma.
- **Missing values:** Empty field (no sentinel values like -999).
- **Timestamp:** Seconds from heater power-on (float, 3 decimal places).

### 2.2 Column Definitions

| Column | Type | Units | Description |
|--------|------|-------|-------------|
| `timestamp_s` | float | s | Time since heater power-on |
| `T_in_C` | float | °C | Inlet coolant temperature |
| `T_out_C` | float | °C | Outlet coolant temperature |
| `T_heater_C` | float | °C | Heater surface temperature |
| `T_top_C` | float | °C | Cold plate top surface temperature |
| `P_in_Pa` | float | Pa | Inlet static pressure |
| `P_out_Pa` | float | Pa | Outlet static pressure |
| `Q_LPM` | float | LPM | Volumetric flow rate |
| `P_elec_W` | float | W | Electrical power to heater |

### 2.3 Example

```csv
timestamp_s,T_in_C,T_out_C,T_heater_C,T_top_C,P_in_Pa,P_out_Pa,Q_LPM,P_elec_W
0.000,25.01,25.02,25.05,25.03,101825.3,101325.0,43.8,0.00
1.000,25.01,25.03,28.44,25.10,101830.1,101325.2,43.9,25.02
2.000,25.02,25.05,31.22,25.18,101828.7,101324.8,43.8,25.01
```

---

## 3. Run Summary Record (Per Run)

### 3.1 File Format

- **Format:** JSON, UTF-8, indented (2 spaces).
- **One file per test run.**

### 3.2 Schema

```json
{
  "schema_version": "1.0.0",
  "test_id": "string — e.g., B-01-R1",
  "candidate_id": "string — e.g., candidate_02_diamond_2d_s1045",
  "phase": "string — A|B|C|D|E",
  "date": "string — ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)",
  "operator": "string",
  "conditions": {
    "P_elec_setpoint_W": "float",
    "T_in_setpoint_C": "float",
    "flow_target": "string — description of flow target"
  },
  "measured_means": {
    "P_elec_W": "float — mean over steady-state window",
    "T_in_C": "float",
    "T_out_C": "float",
    "T_heater_C": "float",
    "T_top_C": "float",
    "P_in_Pa": "float",
    "P_out_Pa": "float",
    "Q_LPM": "float"
  },
  "derived": {
    "dP_Pa": "float — P_in - P_out",
    "R_th_KW": "float — (T_heater - T_in) / P_elec",
    "R_hyd_Pasm3": "float — dP / Q (converted to m³/s)",
    "energy_balance": "float — (T_out - T_in) * mdot * cp / P_elec"
  },
  "quality": {
    "steady_state_met": "boolean",
    "max_T_drift_Cmin": "float — max temperature drift in recording window",
    "energy_balance_closure_pct": "float",
    "notes": "string — free text"
  },
  "provenance": {
    "geometry_source": "string — path to Stage 3 geometry artifact",
    "simulation_source": "string — path to Stage 5/6 results",
    "fabrication_batch": "string — AM build identifier",
    "specimen_id": "string — physical specimen label",
    "ct_scan_id": "string — pre-test CT scan identifier",
    "timeseries_file": "string — relative path to CSV"
  }
}
```

### 3.3 Example

```json
{
  "schema_version": "1.0.0",
  "test_id": "B-01-R1",
  "candidate_id": "candidate_02_diamond_2d_s1045",
  "phase": "B",
  "date": "2026-04-15T14:30:00Z",
  "operator": "J. Smith",
  "conditions": {
    "P_elec_setpoint_W": 25.0,
    "T_in_setpoint_C": 25.0,
    "flow_target": "Adjust pump to achieve dP ~ 1000 Pa"
  },
  "measured_means": {
    "P_elec_W": 25.02,
    "T_in_C": 25.01,
    "T_out_C": 25.18,
    "T_heater_C": 42.50,
    "T_top_C": 28.30,
    "P_in_Pa": 101830.0,
    "P_out_Pa": 101325.0,
    "Q_LPM": 43.8
  },
  "derived": {
    "dP_Pa": 505.0,
    "R_th_KW": 0.699,
    "R_hyd_Pasm3": 691780.0,
    "energy_balance": 0.93
  },
  "quality": {
    "steady_state_met": true,
    "max_T_drift_Cmin": 0.15,
    "energy_balance_closure_pct": 93.0,
    "notes": ""
  },
  "provenance": {
    "geometry_source": "results/stage3_geometry_smoke/candidate_02_diamond_2d_s1045/geometry/volume.npy",
    "simulation_source": "results/stage5_thermal_smoke/candidate_02_diamond_2d_s1045/thermal_metrics.json",
    "fabrication_batch": "BUILD-2026-04-01-A",
    "specimen_id": "S7-C02-001",
    "ct_scan_id": "CT-2026-04-10-001",
    "timeseries_file": "data/B-01-R1_timeseries.csv"
  }
}
```

---

## 4. Campaign Summary (Per Condition)

### 4.1 File Format

- **Format:** JSON, UTF-8, indented.
- **One file per test phase or one combined file.**

### 4.2 Schema

```json
{
  "schema_version": "1.0.0",
  "candidate_id": "string",
  "campaign_date_range": "string — YYYY-MM-DD to YYYY-MM-DD",
  "conditions": [
    {
      "condition_label": "string — e.g., nominal_25W",
      "P_elec_setpoint_W": "float",
      "flow_target": "string",
      "n_repeats": "integer",
      "results": {
        "R_th_KW": {
          "mean": "float",
          "std": "float",
          "ci95_lower": "float",
          "ci95_upper": "float"
        },
        "dP_Pa": {
          "mean": "float",
          "std": "float",
          "ci95_lower": "float",
          "ci95_upper": "float"
        },
        "Q_LPM": {
          "mean": "float",
          "std": "float",
          "ci95_lower": "float",
          "ci95_upper": "float"
        },
        "energy_balance": {
          "mean": "float",
          "std": "float"
        }
      },
      "comparison_to_simulation": {
        "R_th_ratio": "float — measured_mean / predicted",
        "R_th_predicted_KW": "float",
        "R_th_pass": "boolean — ratio in [0.5, 2.0]",
        "dP_ratio": "float — measured_mean / predicted",
        "dP_predicted_Pa": "float",
        "dP_pass": "boolean — ratio in [0.33, 3.0]"
      },
      "run_ids": ["string — list of test_id values included"]
    }
  ],
  "overall_verdict": {
    "R_th_pass": "boolean",
    "dP_pass": "boolean",
    "structural_integrity": "boolean",
    "geometry_fidelity": "boolean",
    "stage7_pass": "boolean"
  }
}
```

---

## 5. Pre-Test Characterization Record

### 5.1 File Format

- **Format:** JSON, UTF-8, indented.
- **One file per specimen.**

### 5.2 Schema

```json
{
  "schema_version": "1.0.0",
  "specimen_id": "string",
  "candidate_id": "string",
  "fabrication_batch": "string",
  "date": "string — ISO 8601",
  "ct_scan": {
    "scan_id": "string",
    "resolution_um": "float",
    "wall_thickness_measured_mm": {
      "min": "float",
      "mean": "float",
      "max": "float"
    },
    "channel_diameter_measured_mm": {
      "min": "float",
      "mean": "float",
      "max": "float"
    },
    "porosity_measured_pct": "float",
    "geometry_deviation_pct": "float — max deviation from design",
    "fidelity_pass": "boolean — deviation < 30%"
  },
  "mass": {
    "dry_mass_g": "float",
    "expected_mass_g": "float — from design porosity and material density",
    "deviation_pct": "float"
  },
  "external_dimensions_mm": {
    "length": "float",
    "width": "float",
    "height": "float"
  },
  "powder_evacuation": {
    "mass_before_cleaning_g": "float",
    "mass_after_cleaning_g": "float",
    "residual_pct": "float",
    "pass": "boolean — residual < 0.5%"
  },
  "leak_test": {
    "pressure_applied_Pa": "float",
    "hold_time_min": "float",
    "leak_detected": "boolean"
  }
}
```

---

## 6. Simulation Reference Record

For traceability, include a snapshot of simulation predictions alongside test data.

### 6.1 Schema

```json
{
  "schema_version": "1.0.0",
  "candidate_id": "string",
  "pipeline_git_sha": "string",
  "stage3": {
    "voxel_size_mm": "float",
    "resolution": "integer",
    "domain_mm": ["float", "float", "float"],
    "porosity": "float",
    "min_wall_thickness_mm": "float",
    "min_feature_size_mm": "float"
  },
  "stage4": {
    "pressure_drop_Pa": "float",
    "flow_rate_m3s": "float",
    "flow_rate_LPM": "float",
    "hydraulic_resistance_Pasm3": "float",
    "label": "FLOW_SIMULATED"
  },
  "stage5": {
    "thermal_resistance_KW": "float",
    "peak_temperature_C": "float",
    "mean_temperature_C": "float",
    "label": "SIMULATED"
  },
  "stage6": {
    "structural_pass": "boolean",
    "manufacturability_pass": "boolean",
    "combined_stress_MPa": "float",
    "margin_of_safety": "float",
    "structural_label": "STRUCTURAL_SCREENED",
    "manufacturability_label": "MANUFACTURABILITY_SCREENED"
  }
}
```

---

## 7. Quantity Labels

All reported quantities must carry a label indicating their provenance:

| Label | Meaning | Example |
|-------|---------|---------|
| `SIMULATED` | Output of Stage 5 thermal solver (analytical) | R_th = 11.27 K/W |
| `FLOW_SIMULATED` | Output of Stage 4 flow solver (analytical) | Q = 44.02 LPM |
| `STRUCTURAL_SCREENED` | Output of Stage 6 structural screening (analytical) | σ_combined = 55.7 MPa |
| `MANUFACTURABILITY_SCREENED` | Output of Stage 6 manufacturability check | min_wall = 0.5 mm |
| `LITERATURE` | From published literature or material data sheet | E = 68.9 GPa |
| `MEASURED` | From Stage 7 benchtop test instrumentation | R_th = (measured value) |
| `DERIVED` | Calculated from MEASURED quantities | ΔP = P_in − P_out |
| `CT_MEASURED` | From pre-test CT scan | wall_thickness = (CT value) |

---

## 8. File Naming Convention

See ARTIFACT_LAYOUT.md for the complete directory structure. File names follow this pattern:

```
{test_id}_{descriptor}.{ext}
```

Examples:

- `B-01-R1_timeseries.csv` — Time-series data for test B-01, repeat 1
- `B-01-R1_summary.json` — Run summary for test B-01, repeat 1
- `campaign_summary.json` — Aggregate campaign results
- `pretest_S7-C02-001.json` — Pre-test characterization for specimen S7-C02-001
- `simulation_reference_candidate_02.json` — Simulation predictions snapshot

---

## 9. Versioning

- Schema version follows semver (`major.minor.patch`).
- Current version: `1.0.0`.
- Breaking changes (column removal, type change) increment major version.
- Additive changes (new optional columns) increment minor version.
- All files include `schema_version` field for forward compatibility.

---

## 10. Document Status

| Item | Status |
|------|--------|
| Schema definition | PROPOSED — this document |
| Implementation (DAQ config) | NOT STARTED |
| Validation (test data against schema) | NOT STARTED |

---

**End of document.**
