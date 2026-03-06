# Stage 6 Execution Guide

## Quick Start

### Prerequisites

1. Stage 5 thermal validation must be complete
2. Python environment with numpy and scipy

### Smoke Test

```bash
# Verify Stage 6 is working
python src/stage6_structural/cli.py smoke
```

Expected runtime: ~10 seconds

## Full Execution

### Basic Run

```bash
python src/stage6_structural/cli.py run results/stage5_thermal_full \
    --output results/stage6_structural_full
```

### With Candidate Selection

```bash
# Top 5 candidates only
python src/stage6_structural/cli.py run results/stage5_thermal_full \
    --output results/stage6_structural_top5 \
    --top-k 5

# Specific family
python src/stage6_structural/cli.py run results/stage5_thermal_full \
    --output results/stage6_structural_diamond \
    --family diamond_2d
```

### With Material Selection

```bash
# Specify material (default: aluminum_6061)
python src/stage6_structural/cli.py run results/stage5_thermal_full \
    --output results/stage6_structural_al6061 \
    --material aluminum_6061
```

## Output Inspection

### Check Summary

```bash
# View overall summary
cat results/stage6_structural_full/stage6_summary.json | python -m json.tool

# View comparison table
cat results/stage6_structural_full/structural_comparison_summary.md
```

### Check Specific Candidate

```bash
# View candidate metrics
cat results/stage6_structural_full/candidate_01_diamond_2d_s1127/structural_metrics.json | python -m json.tool
```

## Interpreting Results

### Pass/Fail Status

Check `stage6_verdict.overall_pass` in metrics:
- `true`: Candidate passes screening, mechanically plausible
- `false`: Candidate fails, check `all_failure_modes`

### Structural Margins

Check `structural_screened_quantities.combined_stress.margin_of_safety`:
- Positive: Passes with margin
- Negative: Overstressed
- Higher is better (more robust)

### Failure Modes

Common failure modes:
- `pressure_overstress`: Pressure load exceeds allowable
- `thermal_overstress`: Thermal stress exceeds allowable
- `excessive_deflection`: Deflection too large
- `wall_too_thin`: Wall thickness below minimum
- `feature_too_small`: Channel diameter below minimum
- `trapped_internal_volumes`: Isolated fluid pockets

## Comparison Workflow

### 1. Run Screening

```bash
python src/stage6_structural/cli.py run results/stage5_thermal_full \
    --output results/stage6_structural_full
```

### 2. Review Summary

```bash
cat results/stage6_structural_full/structural_comparison_summary.md
```

Look for:
- Pass rate
- Best candidate
- Failure mode distribution

### 3. Inspect Best Candidate

```bash
BEST=$(jq -r '.best_candidate' results/stage6_structural_full/stage6_summary.json)
cat results/stage6_structural_full/${BEST}/structural_metrics.json | python -m json.tool
```

### 4. Compare Metrics

```bash
# Extract key metrics for all candidates
for d in results/stage6_structural_full/candidate_*/; do
    ID=$(basename $d)
    PASS=$(jq -r '.stage6_verdict.overall_pass' $d/structural_metrics.json)
    RTH=$(jq -r '.thermal_simulated_quantities.thermal_resistance.thermal_resistance_k_w' $d/structural_metrics.json)
    MARGIN=$(jq -r '.structural_screened_quantities.combined_stress.margin_of_safety' $d/structural_metrics.json)
    echo "$ID: Pass=$PASS, R_th=$RTH K/W, Margin=$MARGIN"
done
```

## Troubleshooting

### No Candidates Loaded

**Error:** `No candidates loaded!`

**Solution:**
- Verify Stage 5 directory path
- Check that Stage 5 has completed successfully
- Verify `stage5_summary.json` exists

### All Candidates Fail

**Error:** All candidates have `overall_pass: false`

**Investigation:**
1. Check failure modes in `structural_comparison.json`
2. Review structural margins
3. Consider if requirements are too strict

**Common causes:**
- Pressure loads too high
- Wall thickness too thin
- Temperature gradients too large

### Material Not Found

**Error:** `Unknown material: <name>`

**Solution:**
- Use `aluminum_6061` (currently only supported material)
- To add materials, edit `src/stage6_structural/material_models.py`

## Performance Notes

- **Runtime:** ~5-10 seconds per candidate
- **Memory:** Minimal (no large arrays stored)
- **Parallelization:** Sequential processing (can be parallelized in future)

## Customization

### Adjust Requirements

Edit requirements in `cli.py`:

```python
requirements = {
    'min_wall_thickness_mm': 0.5,  # Minimum wall thickness
    'min_feature_size_mm': 0.5,    # Minimum channel diameter
    'max_unsupported_mm': 10.0     # Maximum unsupported span
}
```

### Add Material

Edit `src/stage6_structural/material_models.py`:

```python
def get_custom_material() -> Dict[str, Any]:
    return {
        'name': 'Custom Material',
        'E_gpa': ...,
        'yield_strength_mpa': ...,
        # etc.
    }
```

### Adjust Safety Factor

Edit material properties in `material_models.py`:

```python
'safety_factor': 3.0,  # Adjust as needed
```

## Integration with Other Stages

### Input: Stage 5

Stage 6 requires:
- `stage5_summary.json`
- Per-candidate thermal metrics
- Provenance with Stage 3 geometry metadata

### Output: Future Stages

Stage 6 produces:
- Structural screening results
- Manufacturability pass/fail
- Ranked candidate list

Use for:
- Prototype candidate selection
- Full FEA planning
- Fabrication prioritization

## Validation

### Run Tests

```bash
# All Stage 6 tests
pytest tests/test_stage6_structural.py -v

# Specific test
pytest tests/test_stage6_structural.py::TestScreening::test_run_structural_screening -v
```

### Verify Outputs

```bash
# Check output schema
python -c "
import json
with open('results/stage6_structural_smoke/candidate_01_diamond_2d_s1127/structural_metrics.json') as f:
    data = json.load(f)
    assert 'structural_screened_quantities' in data
    assert 'manufacturability_screened_quantities' in data
    assert 'stage6_verdict' in data
    print('Schema valid!')
"
```

## Best Practices

1. **Always run smoke test first** to verify installation
2. **Review failure modes** to understand why candidates fail
3. **Compare structural margins** across candidates
4. **Check manufacturability** separately from structural
5. **Use top-k filtering** to focus on best performers
6. **Document assumptions** when interpreting results

## Limitations

Remember that Stage 6 is **screening only**:

- ✓ Identifies obviously bad designs
- ✓ Ranks candidates by mechanical plausibility
- ✓ Checks manufacturability constraints
- ✗ NOT certified structural validation
- ✗ NOT fabrication process simulation
- ✗ NOT long-term reliability prediction

**Always perform full FEA and fabrication validation before production.**
