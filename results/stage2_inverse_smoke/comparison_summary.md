# Stage 2 Comparison Summary

## Methods Compared

### random_search

- Budget: 10 evaluations
- Valid candidates: 1
- Invalid candidates: 9
- Best score: 309.3427
- Top-1 mean: 309.3427 ± 0.0000
- Family distribution:
  - diamond_2d: 2
  - gyroid_2d: 2
  - pin_fin: 3
  - primitive_2d: 1
  - serpentine_channel: 1
  - straight_channel: 1

### genetic_algorithm

- Budget: 10 evaluations
- Valid candidates: 5
- Invalid candidates: 5
- Best score: 96.7678
- Top-5 mean: 96.3027 ± 0.5696
- Family distribution:
  - gyroid_2d: 3
  - primitive_2d: 6
  - serpentine_channel: 1

## Comparison

✗ **random_search** outperforms **genetic_algorithm**
  - This suggests inverse-design did NOT beat random search
  - Best score: 309.3427 vs 96.7678
  - **Stage 2 FAIL** - inverse design did not beat baseline

## Budget Fairness

✓ All methods used equal budget: 10 evaluations

## Validity Rates

- random_search: 10.0% valid (1/10)
- genetic_algorithm: 50.0% valid (5/10)

---

**Important Note**: All scores are based on Stage 1 proxy metrics.
These results do NOT establish real thermal or hydraulic superiority.
CFD and conjugate heat transfer analysis (Stages 3-4) are required for physical claims.
