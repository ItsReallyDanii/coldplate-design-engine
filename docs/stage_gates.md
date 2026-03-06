# Stage Gates

**Stage: 0 / 0.5 — only Stage 0 and Stage 0.5 gates are currently active.**

Each stage has defined entry criteria (prerequisites), deliverables, and exit criteria
(what must be true before proceeding to the next stage). Gates must be reviewed and
signed off before code for the next stage is merged.

---

## Stage 0 — Repository scaffold and problem definition

**Entry criteria:** none (initial stage).

**Deliverables:**
- [ ] Repository directory structure created.
- [ ] `docs/target_spec.md` completed with primary objective and preliminary constraints.
- [ ] `docs/baselines_spec.md` identifying baseline categories and comparison metrics.
- [ ] `docs/literature_review_checklist.md` drafted.
- [ ] `docs/stage_gates.md` (this file) drafted.

**Exit criteria:**
- All Stage 0 deliverables checked off above.
- No fabricated quantitative claims in any document.

---

## Stage 0.5 — Literature review and constraint finalization

**Entry criteria:** Stage 0 complete.

**Deliverables:**
- [ ] Literature review checklist (`docs/literature_review_checklist.md`) completed
      with citations for all high-priority items.
- [ ] Preliminary constraints in `docs/target_spec.md` replaced with confirmed values
      supported by literature or application requirements.
- [ ] Baseline parameter tables in `docs/baselines_spec.md` populated with values
      drawn from literature.
- [ ] Claim audit entries created in `claim_audit_v2/` for any quantitative statements
      introduced.

**Exit criteria:**
- All Stage 0.5 deliverables checked off above.
- Each quantitative claim in documentation has a corresponding audit entry.
- No uncited performance claims remain in any document.

---

## Stage 1 — 2-D surrogate modeling and parameter sweeps (`src/stage1_2d/`)

**Entry criteria:** Stage 0.5 complete; baseline parameters confirmed.

**Deliverables:**
- [ ] 2-D thermal-hydraulic model implemented and validated against at least one
      literature case.
- [ ] Parameter sweep across channel / pore geometry variables executed.
- [ ] Surrogate model (e.g., response surface, Gaussian process) fitted to sweep data.
- [ ] Sensitivity analysis identifying dominant design variables.
- [ ] Baseline simulation results stored in `baselines/`.

**Exit criteria:**
- Surrogate model cross-validation error documented and acceptable.
- Dominant variables identified and rationale recorded.

---

## Stage 2 — Inverse-design formulation (`src/stage2_inverse/`)

**Entry criteria:** Stage 1 complete; surrogate model validated.

**Deliverables:**
- [ ] Inverse-design problem formally posed (objective, constraints, design variables).
- [ ] Optimization algorithm selected and justified.
- [ ] Proof-of-concept optimization run on surrogate model completed.
- [ ] Candidate geometry (or geometry family) identified.

**Exit criteria:**
- Candidate geometry outperforms all baselines on surrogate model under matched
  constraints.
- Design is physically realizable within stated feature-resolution constraint.

---

## Stage 3 — 3-D geometry generation and meshing (`src/stage3_geometry/`)

**Entry criteria:** Stage 2 complete; candidate geometry defined.

**Deliverables:**
- [ ] 3-D parametric geometry model generated from Stage 2 output.
- [ ] Mesh generated and quality metrics (skewness, aspect ratio) documented.
- [ ] Geometry stored in `data/` in a version-controlled, reproducible format.

**Exit criteria:**
- Mesh quality meets solver requirements for Stage 4.
- Geometry is reproducible from stored parameters without manual intervention.

---

## Stage 3.5 — Physical-model corrections and validation (`src/stage35_physical/`)

**Entry criteria:** Stage 3 complete; mesh ready.

**Deliverables:**
- [ ] Physical model assumptions reviewed against literature.
- [ ] Any model corrections (e.g., effective conductivity, Forchheimer term) documented
      and justified.
- [ ] Sensitivity of results to model assumptions quantified.

**Exit criteria:**
- Physical model assumptions documented with literature support.
- Model sensitivity within acceptable bounds.

---

## Stage 4 — CFD simulation (`src/stage4_cfd/`)

**Entry criteria:** Stage 3.5 complete.

**Deliverables:**
- [ ] CFD solver configured and mesh imported.
- [ ] Mesh-independence study completed and documented.
- [ ] Candidate geometry and all baselines simulated under identical boundary conditions.
- [ ] Results stored in `results/` with full provenance (solver version, settings, mesh).

**Exit criteria:**
- Mesh-independence criterion satisfied (< 1% change in primary metric on refinement).
- Candidate geometry performance advantage confirmed (or refuted) relative to baselines.
- All claims in `claim_audit_v2/` updated to reflect CFD results.

---

## Stage 5 — FEA structural validation (`src/stage5_fea/`)

**Entry criteria:** Stage 4 complete; candidate geometry confirmed thermally.

**Deliverables:**
- [ ] Thermal and pressure loads from Stage 4 applied to structural FEA model.
- [ ] Maximum stress and deflection documented against allowable limits.
- [ ] Design modified if structural limits are exceeded; iterate with Stage 3 if necessary.

**Exit criteria:**
- Structural safety factors documented and within specification.
- No unresolved structural failure modes.
- Final design package (geometry, simulation results, claim audit) complete.
