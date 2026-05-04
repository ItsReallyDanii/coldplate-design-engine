# run_parallel_role_review.md

## Purpose
Use this skill when the goal is to produce a **multi-role review** of a benchtop validation plan for `coldplate-design-engine`.

## Recommended Roles
Run the same repo and same mission through three roles:
1. Experimental Auditor
2. Skeptical Reviewer
3. Lab Manager / PI Lens

## Parallel vs Sequential
If the IDE supports parallel agents, run all three in parallel.
If not, run sequentially in this order:
1. Experimental Auditor
2. Skeptical Reviewer
3. Lab Manager / PI Lens

## Shared Prompt Frame
Every role gets the same high-level question:

> Given the current `coldplate-design-engine` repo state, determine the minimum benchtop data package needed to decide whether the current pipeline is directionally useful or misleading, and produce role-specific outputs without overclaiming.

## Reconciliation Procedure
After all three outputs exist:
1. Compare claims. If claims differ materially, the plan is underspecified.
2. Compare measurement lists. Anything present in only one role should be examined.
3. Compare pass/fail thresholds. If absent or inconsistent, stop and repair.
4. Compare resource requests. Strip anything not justified by the actual test.
5. Write `consensus_summary.md` with:
   - agreed testable claim
   - agreed measurement set
   - agreed controls
   - agreed pass/fail thresholds
   - agreed professor ask
   - unresolved disagreements

## Escalate If
- roles disagree on the core claim
- roles disagree on what counts as success
- no one can state the minimum measurement set
- the lab request requires resources beyond the defined test

