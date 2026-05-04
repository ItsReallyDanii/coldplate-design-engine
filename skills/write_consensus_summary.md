# write_consensus_summary.md

## Purpose
Merge outputs from the role agents into one final, audited summary.

## Input Files
- `bench_claim.md`
- `bench_measurement_plan.md`
- `bench_pass_fail.md`
- `bench_hidden_assumptions.md`
- `claim_attack.md`
- `professor_ask.md`
- `lab_resource_request.md`
- `timeline_and_scope.md`

## Output File
- `consensus_summary.md`

## Required Sections
### 1. Agreed Claim
One paragraph only.

### 2. Agreed Minimum Measurements
Bullet list of required measurements only.

### 3. Agreed Controls
Bullet list of conditions that must be matched.

### 4. Agreed Interpretation Bands
Table with observable, success band, ambiguous band, failure band, interpretation.

### 5. Agreed Lab Ask
One paragraph only.

### 6. Unresolved Disagreements
Short bullets.

### 7. Explicit Non-Claims
Short bullets.

## Merge Rules
- Prefer narrower claims over broader ones
- Prefer fewer measurements if interpretation is preserved
- Prefer explicit thresholds over prose
- Preserve disagreements; do not blur them away
- If a threshold cannot be defended, label it provisional

