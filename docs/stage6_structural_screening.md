# Stage 6: Structural and Manufacturability Screening

**Status:** IMPLEMENTED AND FUNCTIONAL

Stage 6 provides LIGHTWEIGHT but REAL structural and manufacturability screening to determine if candidates from Stage 5 are mechanically plausible enough to justify prototype fabrication.

## What Stage 6 Does

Stage 6 implements **reduced-order structural screening** using analytical approximations:

1. Loads Stage 5 thermal validation outputs
2. Defines mechanical load cases (pressure + thermal)
3. Performs geometric manufacturability checks
4. Estimates structural stresses and deflections using analytical methods
5. Compares candidates under matched material assumptions
6. Outputs reproducible screening results with honest quantity labeling

## Scope and Limitations

### What IS Screened (HONEST)

**Manufacturability Checks (GEOMETRIC):**
- Minimum wall thickness (distance transform)
- Minimum feature size (distance transform)
- Unsupported regions (simplified overhang analysis)
- Trapped volumes (connectivity analysis)

**Structural Screening (ANALYTICAL):**
- Pressure stress (thin-wall pressure vessel theory)
- Thermal stress (constrained thermal expansion)
- Deflection (simplified plate bending theory)
- Combined loading (linear superposition)

All structural quantities are **labeled as ANALYTICAL** or **STRUCTURAL_SCREENED** to distinguish from full FEA.

### What is NOT Validated (LIMITATIONS)

- **Full FEA**: This is NOT certified structural validation
- **Long-term reliability**: No fatigue or creep analysis
- **Fabrication readiness**: Full manufacturing validation still required
- **Complex phenomena**: No buckling, dynamic loads, or contact mechanics
- **Stress concentrations**: Simplified factors used

Stage 6 is **NOT** a replacement for full structural FEA. It provides:
- Screening-level mechanical plausibility assessment
- Manufacturability constraint checking
- Relative structural comparison across candidates
- Identification of obviously problematic designs

Stage 6 does **NOT** provide:
- Production-ready structural certification
- Quantitative long-term reliability predictions
- Fabrication process validation
- Detailed stress field distributions

## Structural Screening Method

### Pressure Loading

Uses **thin-wall pressure vessel theory** as an UPPER BOUND:

```
σ_hoop ≈ (p * r) / t
```

Where:
- `p` = internal pressure (from flow simulation)
- `r` = effective radius (from domain size)
- `t` = effective wall thickness (from geometry)
- Stress concentration factor: k_t = 2.0 (conservative for cellular structures)

**Label:** ANALYTICAL (simplified approximation)

### Thermal Loading

Uses **constrained thermal expansion** theory:

```
σ_thermal = E * α * ΔT / (1 - ν)
```

Where:
- `E` = Young's modulus
- `α` = coefficient of thermal expansion
- `ΔT` = temperature difference (from thermal simulation)
- `ν` = Poisson's ratio
- Constraint factor: 0.5 (reduced constraint for cellular structures)

**Label:** ANALYTICAL (simplified approximation)

### Deflection Estimation

Uses **simplified plate bending theory**:

```
δ ≈ C * (p * L^4) / (E * t^3)
```

Where:
- `C` = plate coefficient (~0.0026 for simply supported)
- `L` = characteristic span
- Allowable: L/360 (serviceability limit)

**Label:** ANALYTICAL (simplified approximation)

### Combined Loading

Uses **linear superposition** (conservative):

```
σ_combined = σ_pressure + σ_thermal
```

Checks against allowable stress with safety factor.

**Label:** ANALYTICAL (superposition approximation)

## Manufacturability Checks

### Wall Thickness

**Method:** Distance transform in solid region

- Minimum wall thickness = 2 × min distance to fluid
- Requirement: ≥ 0.5 mm (adjustable)

**Label:** GEOMETRIC (from geometry analysis)

### Feature Size

**Method:** Distance transform in fluid region

- Minimum channel diameter = 2 × min distance to solid
- Requirement: ≥ 0.5 mm (adjustable)

**Label:** GEOMETRIC (from geometry analysis)

### Trapped Volumes

**Method:** Connected component analysis

- Checks for isolated fluid pockets
- Pass if single connected component or >95% in largest component

**Label:** GEOMETRIC (from connectivity analysis)

### Unsupported Regions

**Method:** Simplified overhang analysis

- Checks for excessive unsupported spans (relevant for AM)
- Simplified check (full AM simulation needed for fabrication)

**Label:** GEOMETRIC (simplified analysis)

## Material Properties

### Aluminum 6061-T6

**Standard cold plate material:**

- Young's modulus: 68.9 GPa
- Yield strength: 276 MPa
- Poisson's ratio: 0.33
- Thermal expansion: 23.6 × 10⁻⁶ /K
- Safety factor: 3.0 (conservative for screening)
- Allowable stress: 92 MPa (yield / safety factor)

**Label:** LITERATURE (from ASM Metals Handbook)

## Execution

### Quick Start (Smoke Test)

```bash
# Run smoke test on Stage 5 smoke outputs
python src/stage6_structural/cli.py smoke
```

**Expected output:**
```
=== Stage 6 Structural Screening ===
Loading Stage 5 candidates...
Loaded 2 candidates

[1/2] Screening candidate_02_diamond_2d_s1045...
  Status: PASS
  Structural margin: 0.80

[2/2] Screening candidate_01_diamond_2d_s1127...
  Status: PASS
  Structural margin: 0.75

=== Summary ===
Candidates processed: 2
Candidates PASS: 2
Pass rate: 100.0%
Best candidate: candidate_02_diamond_2d_s1045

Smoke test PASSED!
```

### Run on Stage 5 Outputs

```bash
# Run on full Stage 5 results
python src/stage6_structural/cli.py run results/stage5_thermal_full --output results/stage6_structural_full

# Run with top-k selection
python src/stage6_structural/cli.py run results/stage5_thermal_full --output results/stage6_structural_top5 --top-k 5

# Run with family filter
python src/stage6_structural/cli.py run results/stage5_thermal_full --output results/stage6_structural_diamond --family diamond_2d

# Run with different material
python src/stage6_structural/cli.py run results/stage5_thermal_full --output results/stage6_structural_al6061 --material aluminum_6061
```

## Outputs

Stage 6 produces the following outputs:

### Per-Candidate Results

**`{candidate_id}/structural_metrics.json`:**
- Structural screening results (stress, deflection)
- Manufacturability check results
- Material properties
- Stage 6 verdict (PASS/FAIL)
- Carried-forward thermal and flow metrics
- Provenance tracking

### Comparison Results

**`structural_comparison.json`:**
- Ranked candidates by combined performance
- Pass rates and failure mode statistics
- Performance ranges for passing candidates

**`structural_comparison_summary.md`:**
- Human-readable comparison table
- Failure mode breakdown
- Best candidate identification

### Manifests

**`run_manifest.json`:**
- Execution metadata
- Input/output directories
- Processing statistics

**`stage6_summary.json`:**
- Overall Stage 6 summary
- Pass rates
- Best candidate

## Quantity Labeling

Stage 6 uses HONEST labeling to distinguish sources:

- **STRUCTURAL_SCREENED:** Structural screening outputs from this stage
- **MANUFACTURABILITY_SCREENED:** Manufacturability checks from this stage
- **ANALYTICAL:** Analytical approximations (not full FEA)
- **GEOMETRIC:** Geometry-derived quantities
- **LITERATURE:** Material properties from handbooks
- **SIMULATED:** Carried from Stage 5 (thermal solver)
- **FLOW_SIMULATED:** Carried from Stage 4 (flow solver)

## Pass/Fail Criteria

### Structural Pass

Candidate passes structural screening if:
- Pressure stress < allowable (with safety factor)
- Thermal stress < allowable
- Deflection < L/360
- Combined stress < allowable

### Manufacturability Pass

Candidate passes manufacturability if:
- Wall thickness ≥ minimum requirement
- Feature size ≥ minimum requirement
- No excessive unsupported regions
- No trapped volumes

### Overall Pass

Candidate passes overall if:
- Passes structural screening AND
- Passes manufacturability screening

## Stage 6 Verdict

Stage 6 provides a PRELIMINARY SCREENING verdict:

**PASS:** Candidate shows no obvious mechanical absurdity or manufacturability blockers. Proceed with confidence that prototype fabrication is mechanically reasonable, subject to full validation.

**FAIL:** Candidate shows clear structural or manufacturability issues. Do NOT proceed to prototype fabrication without redesign.

**IMPORTANT:** Stage 6 PASS does NOT certify:
- Long-term reliability
- Production readiness
- Detailed stress distributions
- Fabrication process success

Stage 6 is a **gate** to prevent obviously bad designs from consuming prototype resources. Full FEA and fabrication validation are still required before production.

## Testing

Run Stage 6 tests:

```bash
# Run all Stage 6 tests
pytest tests/test_stage6_structural.py -v

# Run specific test class
pytest tests/test_stage6_structural.py::TestScreening -v

# Run with coverage
pytest tests/test_stage6_structural.py --cov=src/stage6_structural
```

## Dependencies

Stage 6 requires:
- numpy (numerical operations)
- scipy (distance transforms, ndimage)
- Standard library (json, os, sys, argparse)

## Next Steps

After Stage 6 screening:

1. **Review screening results:** Examine failure modes and margins
2. **Select candidates:** Choose best performers for prototype
3. **Full FEA validation:** Perform detailed structural FEA (future stage)
4. **Fabrication planning:** Develop manufacturing process (future stage)
5. **Prototype testing:** Build and test physical articles (future stage)

## References

- Ashby, M.F., "Materials Selection in Mechanical Design"
- Roark's Formulas for Stress and Strain
- ASM Metals Handbook (Aluminum 6061-T6 properties)
- ASME Boiler and Pressure Vessel Code (safety factors)
