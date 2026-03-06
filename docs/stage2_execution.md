# Stage 2 Execution Guide

## Quick Start

### 1. Smoke Test (5 seconds)
```bash
python src/stage2_inverse/cli.py smoke
```

This runs a minimal test with:
- Grid: 50x50
- Budget: 10 evaluations per method
- Output: `results/stage2_inverse_smoke/`

### 2. Full Comparison (default config)
```bash
python src/stage2_inverse/cli.py compare configs/stage2_default.yaml
```

This runs a full comparison with:
- Grid: 100x100
- Budget: 100 evaluations per method
- Output: `results/stage2_inverse/`

### 3. Single Method Optimization
```bash
# Run genetic algorithm only
python src/stage2_inverse/cli.py optimize configs/stage2_default.yaml

# Or modify config to run random search
# Edit configs/stage2_default.yaml: method: random
```

## Configuration

### Config File Format (YAML)

```yaml
# Grid configuration
grid:
  nx: 100        # Grid width in pixels
  ny: 100        # Grid height in pixels
  dx: 0.0001     # Cell width in meters
  dy: 0.0001     # Cell height in meters

# Optimization settings
budget: 100            # Number of evaluations
seed: 42               # Random seed for reproducibility
method: genetic        # "random" or "genetic"
population_size: 20    # For genetic algorithm

# Output
output_dir: results/stage2_inverse
```

### Available Configs
- `configs/stage2_smoke.yaml`: Quick test (50x50, budget 10)
- `configs/stage2_default.yaml`: Full run (100x100, budget 100)

## Output Files

After running, the output directory contains:

### Results Files
- `random_search_results.jsonl`: All random search evaluations
- `genetic_algorithm_results.jsonl`: All GA evaluations
- Each line is a JSON object with:
  - `family`: Geometry family
  - `params`: Parameter values
  - `total_score`: Overall score
  - `is_valid`: Whether constraints satisfied
  - `metrics`: All Stage 1 metrics
  - `objective_breakdown`: Contribution from each objective term
  - `constraint_violations`: Any violated constraints

### Best Candidates
- `random_best.csv`: Top 10 from random search
- `genetic_best.csv`: Top 10 from genetic algorithm  
- `best_candidates.csv`: Combined top 20 from both methods

CSV columns include:
- `rank`, `method`, `family`
- `total_score`, `is_valid`
- `param_*`: All parameters
- Key metrics: `porosity`, `heat_exchange_area_proxy`, `hydraulic_resistance_proxy`, etc.

### Comparison
- `comparison.json`: Structured comparison data
- `comparison_summary.md`: Human-readable summary with verdict
- Includes:
  - Best scores by method
  - Validity rates
  - Budget fairness check
  - Winner determination
  - PASS/FAIL assessment

### Provenance
- `run_manifest.json`: Complete run metadata
  - Timestamp, git SHA
  - Search space definition
  - Objective function configuration
  - Budget and seed
  - Number of evaluations

## Commands Reference

### Smoke Test
```bash
python src/stage2_inverse/cli.py smoke
```
- Runs minimal test
- Uses small grid (50x50)
- Budget: 10 per method
- Fast execution (~10 seconds)

### Optimize
```bash
python src/stage2_inverse/cli.py optimize <config.yaml>
```
- Runs single optimization method
- Method specified in config file
- Saves results and manifest

### Compare
```bash
python src/stage2_inverse/cli.py compare <config.yaml>
```
- Runs both random search and genetic algorithm
- Equal budget for fair comparison
- Generates comparison summary
- **Use this for Stage 2 validation**

## Running Tests

### All Stage 2 Tests
```bash
pytest tests/test_stage2_*.py -v
```

Expected: 56 tests passing

### Test Categories
- `test_stage2_objectives.py`: Objective and constraint tests (15 tests)
- `test_stage2_search_space.py`: Search space tests (15 tests)
- `test_stage2_methods.py`: Sampler and optimizer tests (15 tests)
- `test_stage2_io.py`: I/O and comparison tests (12 tests)

### With Coverage
```bash
pytest tests/test_stage2_*.py --cov=src/stage2_inverse --cov-report=html
```

## Interpreting Results

### Comparison Summary

The `comparison_summary.md` file provides:

1. **Method Statistics**: Budget, valid count, best score, top-k distribution
2. **Winner**: Which method achieved better best score
3. **Improvement**: Percentage improvement
4. **Budget Fairness**: Confirms equal budget used
5. **Validity Rates**: Fraction of candidates satisfying constraints

### Stage 2 Verdict

**PASS if**:
- Genetic algorithm best score > random search best score
- Under equal evaluation budget
- Results reproducible with documented seeds

**FAIL if**:
- Random search equals or beats genetic algorithm
- Unequal budgets used
- Metrics mislabeled as physical quantities

### Proxy Metric Interpretation

Remember:
- `heat_exchange_area_proxy`: Interface length, NOT heat transfer rate
- `hydraulic_resistance_proxy`: Geometric heuristic, NOT pressure drop
- Scores are dimensionless and relative
- No real-world thermal claims can be made from Stage 2 alone

## Troubleshooting

### Low Validity Rates
If both methods have <10% valid candidates:
- Check parameter bounds in `search_space.py`
- Grid may be too small (try 100x100 or larger)
- Constraints may be too strict

### Genetic Algorithm Not Converging
- Increase population size (try 30-50)
- Increase budget (try 200+)
- Check mutation/crossover rates

### Determinism Issues
- Ensure same seed used
- Seeds are documented in manifest
- Random search seed: `seed`
- Genetic algorithm seed: `seed + 1000`

## Performance

### Timing Estimates (100x100 grid)
- Single evaluation: ~0.2-0.5 seconds
- Budget 100 (both methods): ~1-2 minutes
- Smoke test: ~5-10 seconds

### Memory
- Typical run: <500 MB
- Stores all results in memory during run
- Written to disk at end

## Next Steps After Stage 2

1. Review `comparison_summary.md`
2. If PASS: Advance to Stage 3 (3D geometry promotion)
3. If FAIL: Investigate parameter bounds, constraints, or try different optimization method
4. Extract best candidates from `best_candidates.csv`
5. Prepare for CFD validation (Stage 4)

## Example Workflow

```bash
# 1. Quick smoke test
python src/stage2_inverse/cli.py smoke

# 2. Check results
cat results/stage2_inverse_smoke/comparison_summary.md

# 3. Full comparison
python src/stage2_inverse/cli.py compare configs/stage2_default.yaml

# 4. Review full results
cat results/stage2_inverse/comparison_summary.md
head -20 results/stage2_inverse/best_candidates.csv

# 5. Run tests
pytest tests/test_stage2_*.py -v

# 6. If PASS, proceed to Stage 3
```

## Reference: Stage 1 Integration

Stage 2 uses Stage 1 as black-box evaluator:
1. Generate mask with Stage 1 generators
2. Evaluate with Stage 1 metrics
3. Score with Stage 2 objective function
4. Track and compare results

No Stage 1 code is modified or duplicated.
