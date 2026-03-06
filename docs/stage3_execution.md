# Stage 3 Execution Guide

## Prerequisites

1. **Complete Stage 2** - Stage 3 requires Stage 2 outputs
2. **Install dependencies** - Ensure all packages are installed

```bash
pip install -e .
pip install -r requirements-dev.txt
```

3. **Verify Stage 2 outputs exist:**

```bash
ls results/stage2_inverse/best_candidates.csv
```

## Quick Start

### 1. Smoke Test (Recommended First Step)

Run a minimal test with top 2 candidates at low resolution:

```bash
python src/stage3_geometry/cli.py smoke
```

**Expected output:**
- Promotes 2 candidates at resolution=50
- Generates STL and raw volume files
- Runs validation checks
- Creates summary report
- Output: `results/stage3_geometry_smoke/`

**Success indicators:**
- No errors during execution
- STL files created (check file sizes > 0)
- Summary shows 2/2 successful
- Validation checks pass

### 2. Full Promotion

Run full promotion with default configuration:

```bash
python src/stage3_geometry/cli.py promote configs/stage3_default.yaml
```

**Default configuration:**
- Top 5 candidates
- Resolution: 100
- Height: 2.0 mm
- Output: `results/stage3_geometry/`

**Time estimate:** ~2-5 minutes for 5 candidates at resolution 100

### 3. Custom Configuration

Create a custom config file:

```yaml
# my_stage3_config.yaml
stage2_results: results/stage2_inverse/best_candidates.csv
top_k: 10
resolution: 120
height_mm: 2.5
family_filter: diamond_2d  # Optional: only promote diamond family
output_dir: results/stage3_custom
```

Run with custom config:

```bash
python src/stage3_geometry/cli.py promote my_stage3_config.yaml
```

### 4. Validation

Validate existing Stage 3 outputs:

```bash
python src/stage3_geometry/cli.py validate configs/stage3_default.yaml
```

## Commands Reference

### `smoke` - Smoke Test

```bash
python src/stage3_geometry/cli.py smoke
```

- No arguments required
- Uses hardcoded smoke test parameters
- Output: `results/stage3_geometry_smoke/`

### `promote` - Full Promotion

```bash
python src/stage3_geometry/cli.py promote <config_file>
```

**Required argument:**
- `<config_file>` - Path to YAML configuration file

**Configuration options:**
- `stage2_results` - Path to best_candidates.csv
- `top_k` - Number of candidates to promote (default: 5)
- `resolution` - Grid resolution (default: 100)
- `height_mm` - Geometry height in mm (default: 2.0)
- `family_filter` - Optional family filter (e.g., 'diamond_2d')
- `valid_only` - Only promote valid candidates (default: true)
- `output_dir` - Output directory path

### `validate` - Validate Outputs

```bash
python src/stage3_geometry/cli.py validate <config_file>
```

- Loads existing summary.json from output_dir
- Reports pass/fail counts
- No regeneration of geometry

## Interpreting Results

### Summary Report

Check `summary.md` in output directory:

```markdown
# Stage 3 Geometry Promotion Summary

**Candidates Processed:** 5

## Promotion Results

- **Successful:** 5/5
- **Failed:** 0/5

## Candidate Details

| Rank | Family | Seed | Status | Porosity | Connected | Min Feature (mm) |
|------|--------|------|--------|----------|-----------|------------------|
| 1 | diamond_2d | 1127 | ✓ | 0.555 | Yes | 0.200 |
...
```

**Key metrics:**
- **Status** - ✓ = success, ✗ = failed
- **Porosity** - Volume fraction of fluid (should be 0.4-0.7 typically)
- **Connected** - Yes = single connected fluid region
- **Min Feature** - Minimum channel diameter in mm

### Provenance Records

Each candidate has a `provenance.json` with:

- Stage 2 source (rank, family, params, score)
- 3D promotion metadata
- Validation results
- Export paths

**Use for:**
- Reproducibility
- Tracing parameters
- Debugging failures

### STL Files

**Location:** `candidate_*/geometry/geometry.stl`

**Properties:**
- ASCII STL format
- Can be opened in MeshLab, ParaView, or mesh viewers
- Triangle count typically 50k-200k for resolution 100

**Use for:**
- Visual inspection
- CFD mesh generation (Stage 4)
- FEA mesh generation (Stage 5)

### Raw Volumes

**Location:** `candidate_*/geometry/volume.npy`

**Properties:**
- Binary numpy array (nz, ny, nx)
- Values: 0=solid, 1=fluid
- Can be loaded with `np.load()`

**Use for:**
- Analysis
- Regenerating exports
- Custom processing

## Troubleshooting

### "Stage 2 results not found"

**Problem:** `best_candidates.csv` missing

**Solution:** Run Stage 2 first:
```bash
python src/stage2_inverse/cli.py smoke  # or compare
```

### STL export fails

**Problem:** Volume too large for marching cubes

**Solution:** Reduce resolution in config:
```yaml
resolution: 50  # Lower resolution
```

### Validation fails

**Problem:** Geometry has disconnected regions or invalid porosity

**Solution:**
- Check Stage 2 parameters
- Try different candidates
- Adjust validation thresholds in config

### Out of memory

**Problem:** High resolution volumes exceed available RAM

**Solution:**
- Reduce resolution
- Process fewer candidates (`top_k: 3`)
- Increase system memory

## Running Tests

Run all Stage 3 tests:

```bash
pytest tests/test_stage3_*.py -v
```

Run specific test file:

```bash
pytest tests/test_stage3_promote.py -v
```

Run with coverage:

```bash
pytest tests/test_stage3_*.py --cov=src/stage3_geometry --cov-report=term
```

## Performance Notes

**Typical execution times** (on standard hardware):

| Operation | Resolution | Time |
|-----------|-----------|------|
| Single candidate | 50 | ~5-10 sec |
| Single candidate | 100 | ~30-60 sec |
| Single candidate | 150 | ~2-3 min |
| Smoke test (2 candidates @ 50) | 50 | ~20-30 sec |
| Full run (5 candidates @ 100) | 100 | ~3-5 min |

**Memory usage:**

- Resolution 50: ~few MB per candidate
- Resolution 100: ~10-20 MB per candidate
- Resolution 150: ~30-50 MB per candidate

**STL file sizes:**

- Resolution 50: ~10-30 MB
- Resolution 100: ~20-100 MB
- Resolution 150: ~50-200 MB

## Next Steps

After successful Stage 3:

1. **Inspect geometry** - Open STL files in mesh viewer
2. **Review validation** - Check summary.md for pass rates
3. **Select candidates** - Choose best geometries for CFD
4. **Prepare for Stage 4** - Stage 4 will use these STL files for CFD meshing

**Remember:** Stage 3 does not validate thermal-hydraulic performance. CFD (Stage 4) is required for flow and thermal claims.
