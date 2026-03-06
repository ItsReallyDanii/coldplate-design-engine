# Stage 1 Execution Guide

**Status:** Stage 1 implementation complete and operational.

This document provides instructions for running the Stage 1 2D cold-plate evaluation engine.

## Prerequisites

```bash
# Install the package and dependencies
pip install -e .

# Install development dependencies (for running tests)
pip install -r requirements-dev.txt
```

## Quick Start: Smoke Test

Run a minimal smoke test to verify the installation:

```bash
python src/stage1_2d/cli.py smoke
```

This will:
- Generate one mask from each of the 6 baseline families
- Evaluate all metrics for each mask
- Save outputs to `results/stage1_2d_smoke/`
- Complete in under 5 seconds

Expected output:
```
============================================================
STAGE 1 SMOKE TEST
============================================================
Running Stage 1 sweep
Output directory: results/stage1_2d_smoke
Grid: 100x100
Families: ['straight_channel', 'serpentine_channel', 'pin_fin', 'gyroid_2d', 'diamond_2d', 'primitive_2d']
...
Completed 6 evaluations
Saved metrics CSV: results/stage1_2d_smoke/metrics.csv
Saved metrics JSONL: results/stage1_2d_smoke/metrics.jsonl
Saved manifest: results/stage1_2d_smoke/run_manifest.json
============================================================
SMOKE TEST COMPLETE: 6 evaluations
============================================================
```

## Running a Parameter Sweep

Use a configuration file to run a parameter sweep:

```bash
python src/stage1_2d/cli.py sweep configs/stage1_default.yaml
```

### Configuration File Format

See `configs/stage1_default.yaml` for a complete example.

```yaml
output_dir: "results/stage1_2d"

grid:
  nx: 200  # pixels
  ny: 200  # pixels
  dx: 1.0e-4  # meters (100 microns)
  dy: 1.0e-4  # meters (100 microns)

families:
  - straight_channel
  - serpentine_channel
  - pin_fin
  - gyroid_2d
  - diamond_2d
  - primitive_2d

param_ranges:
  straight_channel:
    num_channels: [2, 4, 8, 12]
    channel_width_fraction: [0.3, 0.4, 0.5, 0.6]
  
  serpentine_channel:
    channel_width_px: [8, 12, 16]
    turn_radius_px: [15, 20, 25]
    num_passes: [3, 5, 7]
  
  pin_fin:
    pin_diameter_px: [6, 10, 14]
    pin_spacing_px: [25, 35, 45]
    offset_rows: [true, false]
  
  gyroid_2d:
    wavelength_px: [20, 30, 40]
    threshold: [-0.1, 0.0, 0.1]
  
  diamond_2d:
    wavelength_px: [20, 30, 40]
    threshold: [-0.1, 0.0, 0.1]
  
  primitive_2d:
    wavelength_px: [20, 30, 40]
    threshold: [-0.1, 0.0, 0.1]

seed_start: 0
num_samples_per_config: 1
```

## Output Structure

After running a sweep, the output directory contains:

```
results/stage1_2d/
├── masks/
│   ├── straight_channel_s0.npy
│   ├── straight_channel_s1.npy
│   └── ...
├── results/
│   ├── straight_channel_s0.json
│   ├── straight_channel_s1.json
│   └── ...
├── metrics.csv           # All metrics in tabular format
├── metrics.jsonl         # All metrics in JSON Lines format
└── run_manifest.json     # Provenance and configuration
```

### Output Files

**masks/** - Binary masks as NumPy arrays (`.npy` files)
- Load with `np.load(path)`
- Shape: `(ny, nx)`, dtype: `uint8`, values: `{0, 1}`
- 0 = solid, 1 = fluid

**results/** - Individual evaluation results (JSON)
- One file per mask
- Contains all metrics, parameters, warnings

**metrics.csv** - Tabular metrics for all evaluations
- One row per mask
- Includes mask_id, family, parameters, all metric values
- Easy to load with pandas: `pd.read_csv('metrics.csv')`

**metrics.jsonl** - JSON Lines format (one JSON object per line)
- Complete evaluation results
- Preserves all metadata and warnings

**run_manifest.json** - Sweep provenance
- Timestamp
- Git SHA (if available)
- Configuration used
- Number of evaluations
- Metric schema version

## Running Tests

Run the test suite to verify correctness:

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_stage1_generators.py -v
pytest tests/test_stage1_metrics.py -v
pytest tests/test_stage1_sweep.py -v

# Run with coverage
pytest tests/ --cov=src/stage1_2d --cov-report=html
```

Expected result: All tests pass.

## Baseline Families

Stage 1 implements 6 baseline families:

### 1. Straight Channel
Parallel straight channels.

**Parameters:**
- `num_channels`: Number of channels (integer)
- `channel_width_fraction`: Channel width as fraction of pitch (0 to 1)

### 2. Serpentine Channel
Meandering channel with turns.

**Parameters:**
- `channel_width_px`: Channel width in pixels (integer)
- `turn_radius_px`: Turn radius in pixels (integer)
- `num_passes`: Number of horizontal passes (integer)

### 3. Pin-Fin
Obstacle array with circular pins.

**Parameters:**
- `pin_diameter_px`: Pin diameter in pixels (integer)
- `pin_spacing_px`: Center-to-center spacing in pixels (integer)
- `offset_rows`: Staggered pattern (boolean)

### 4. Gyroid 2D Proxy
**HONEST LABEL:** This is a 2D approximation using an implicit function that mimics gyroid topology. It is **NOT** a true 3D gyroid cross-section.

**Parameters:**
- `wavelength_px`: Characteristic wavelength in pixels (float)
- `threshold`: Threshold for binary conversion (-0.5 to 0.5, default: 0.0)

### 5. Diamond 2D Proxy
**HONEST LABEL:** This is a 2D approximation using an implicit function that mimics diamond topology. It is **NOT** a true 3D diamond cross-section.

**Parameters:**
- `wavelength_px`: Characteristic wavelength in pixels (float)
- `threshold`: Threshold for binary conversion (-0.5 to 0.5, default: 0.0)

### 6. Primitive 2D Proxy
**HONEST LABEL:** This is a 2D approximation using an implicit function that mimics primitive (Schwarz P) topology. It is **NOT** a true 3D primitive cross-section.

**Parameters:**
- `wavelength_px`: Characteristic wavelength in pixels (float)
- `threshold`: Threshold for binary conversion (-0.5 to 0.5, default: 0.0)

## Metrics

See `docs/stage1_metric_definitions.md` for complete metric definitions.

**Summary of metric categories:**
- **GEOMETRIC:** Real geometric properties (porosity, feature sizes, etc.)
- **FLOW_PROXY:** Dimensionless flow-related proxies (NOT real pressure drop)
- **HEAT_PROXY:** Dimensionless heat-transfer proxies (NOT real thermal resistance)

**All proxy metrics are clearly labeled with `_proxy` suffix.**

## Reproducibility

Sweeps are reproducible if:
1. Same configuration file
2. Same `seed_start` value
3. Same package version (check `run_manifest.json`)

The `run_manifest.json` records:
- Git SHA for code version
- Configuration used
- Metric schema version

## Performance

Approximate performance on a modern CPU:
- **Smoke test (6 masks, 100x100 grid):** < 5 seconds
- **Default sweep (200x200 grid, ~200 masks):** < 2 minutes
- **Large sweep (200x200 grid, 1000+ masks):** < 10 minutes

Memory usage: < 500 MB for typical sweeps.

## Limitations and Stage Gate

**Stage 1 does NOT provide:**
- Real thermal resistance (requires CFD)
- Real pressure drop (requires CFD)
- 3D performance prediction (uses 2D cross-sections only)
- Manufacturability validation (requires process data)

**Stage 1 outputs are screening tools only.**

To advance to Stage 2 (inverse design):
- [ ] Stage 1 sweep completes successfully
- [ ] At least 4 baseline families evaluated
- [ ] Metrics CSV and manifest generated
- [ ] All tests pass
- [ ] Metric honesty maintained (no mislabeled proxies)

To claim real performance improvements:
- **Must advance to Stage 4 (CFD) minimum**
- Must include matched-constraint comparisons
- Must demonstrate mesh independence

## Troubleshooting

**Issue:** Import errors when running CLI

**Solution:** Ensure package is installed: `pip install -e .`

---

**Issue:** Tests fail with module not found

**Solution:** Tests add `src/` to path automatically. Run from repo root: `pytest tests/`

---

**Issue:** Sweep produces no outputs

**Solution:** Check that `output_dir` is writable and configuration is valid YAML

---

**Issue:** TPMS proxies look disconnected

**Solution:** Adjust `threshold` parameter. Negative threshold → higher porosity.

---

**Issue:** Git SHA is None in manifest

**Solution:** Normal if not in a git repository. Does not affect functionality.

## Next Steps

After completing Stage 1:

1. **Analyze sweep results** - Identify trends in metrics across parameter ranges
2. **Filter candidates** - Eliminate geometries with disconnected flow or extreme features
3. **Plan Stage 2** - Define inverse design problem and optimization objectives
4. **Literature comparison** - Compare Stage 1 geometric metrics to literature baselines
5. **Advance to CFD** - Stage 4 required for real performance claims

Do NOT claim thermal or hydraulic superiority from Stage 1 metrics alone.
