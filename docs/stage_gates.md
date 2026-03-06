# Stage Gates

**Compact gate summary for staged development.**

| Stage | Purpose | Deliverable | Pass Gate | Kill Sign |
|-------|---------|-------------|-----------|-----------|
| 0 | Repository scaffold and target definition | Completed `target_spec.md`, `baselines_spec.md`, `stage_gates.md`, and `literature_review_checklist.md` shells | Target statement captured; baseline families and matched-constraint approach documented | Missing target statement or undefined comparison scope |
| 0.5 | Literature review and constraint locking | Cited checklist, locked parameter ranges, and updated documents with literature-backed constraints | All high-priority checklist items cited; matched-constraint settings and sweep plans defined | Uncited quantitative claims or unresolved operating constraints |
| 1 | 2-D surrogate modeling and parameter sweeps | Validated 2-D thermal-hydraulic model with sweep dataset and fitted surrogate | Surrogate error bounded; baselines mapped across sweeps | Model not validated or sweep coverage gaps |
| 2 | Inverse-design problem setup | Formal optimization problem and candidate geometry from surrogate runs | Candidate outperforms baselines on surrogate under matched constraints | Optimizer unstable or violates constraints |
| 3 | 3-D geometry generation and meshing | Parametric 3-D geometry and mesh quality report | Mesh meets solver quality targets and is reproducible | Geometry not reproducible or mesh fails quality checks |
| 3.5 | Physical-model corrections and validation | Documented model corrections (e.g., porous coefficients, effective properties) with sensitivity evidence | Corrections bounded and validated against literature | Unresolved model mismatch versus references |
| 4 | CFD simulation | CFD cases for candidate and baselines with mesh-independence study | Converged results meeting mesh-independence and matched boundary conditions | Solver divergence or unmatched comparison conditions |
| 5 | FEA structural validation | Structural model with applied thermal/pressure loads and results | Stresses and deflections within allowable limits | Overstress/deflection unresolved or unmodeled load paths |
| 6 | Prototype fabrication and bench test | Fabricated test articles and bench-test plan/results | Bench data collected, traceable, and consistent with documentation | Fabrication deviates from spec or tests not reproducible |
| 7 | System integration and reliability | Cold plate integrated into representative loop with reliability screening | Reliability metrics meet requirements; no unresolved failure modes | Persistent reliability failures or integration blockers |
| 8 | Release and handoff | Final design package with claim audit, data, and geometry artifacts | All prior gates closed; documentation and audit complete | Open audit items or unmet acceptance criteria |
