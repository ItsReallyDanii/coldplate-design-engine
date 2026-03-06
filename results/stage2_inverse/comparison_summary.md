# Stage 2 Comparison Summary

## Methods Compared

### random_search

- Budget: 100 evaluations
- Valid candidates: 9
- Invalid candidates: 91
- Best score: 1233.3149
- Top-9 mean: 787.9077 ± 301.5345
- Family distribution:
  - diamond_2d: 20
  - gyroid_2d: 11
  - pin_fin: 17
  - primitive_2d: 18
  - serpentine_channel: 24
  - straight_channel: 10

### genetic_algorithm

- Budget: 100 evaluations
- Valid candidates: 67
- Invalid candidates: 33
- Best score: 2049.6435
- Top-10 mean: 1981.6940 ± 22.6498
- Family distribution:
  - diamond_2d: 78
  - gyroid_2d: 4
  - pin_fin: 2
  - primitive_2d: 3
  - serpentine_channel: 10
  - straight_channel: 3

## Comparison

✓ **genetic_algorithm** outperforms **random_search**
  - Best score: 2049.6435 vs 1233.3149
  - Improvement: 66.19%
  - **Stage 2 PASS candidate** (pending full validation)

## Budget Fairness

✓ All methods used equal budget: 100 evaluations

## Validity Rates

- random_search: 9.0% valid (9/100)
- genetic_algorithm: 67.0% valid (67/100)

---

**Important Note**: All scores are based on Stage 1 proxy metrics.
These results do NOT establish real thermal or hydraulic superiority.
CFD and conjugate heat transfer analysis (Stages 3-4) are required for physical claims.
