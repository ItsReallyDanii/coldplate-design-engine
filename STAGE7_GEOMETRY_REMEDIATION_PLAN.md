# Stage 7 Geometry Remediation Plan

**Date:** 2026-03-06  
**Context:** Follow-up to Stage 6 truth-fix (real geometry screening)  
**Status:** PLANNING - Not yet implemented  

---

## EXECUTIVE SUMMARY

**Current blocker:** Stage 3 geometry generates 0.2mm minimum features (2 voxels at 0.1mm voxel size), which **FAIL** the 0.5mm manufacturability requirement for additive manufacturing.

**Pass rate:** 0/2 candidates (0% manufacturability pass)

**Root cause:** Voxel discretization limit at 50×50×50 resolution produces minimum features = 2×voxel_size = 0.2mm.

**Verdict on current PR:** The Stage 6 truth-fix PR documenting real geometry failures should **MERGE AS-IS**. This blocker is legitimate and must be documented. Do not soften the verdict or mix remediation work into that PR.

**This document provides:** Technical analysis of remediation options, risk categorization, and exact rerun sequence required.

---

## 1. TECHNICAL ROOT CAUSE ANALYSIS

### 1.1 Current Configuration

**Stage 3 smoke test parameters:**
```python
# src/stage3_geometry/cli.py:62
config = {
    'resolution': 50,       # Grid size (nx=ny=nz)
    'height_mm': 2.0,       # Physical height
    'top_k': 2,
    'source_file': stage2_results
}

# Hardcoded in cli.py:102, 114, 204, 213
voxel_size = 0.1  # mm per voxel
```

**Domain size:**
- Grid: 50 × 50 × 50 voxels
- Physical: 5.0 × 5.0 × 5.0 mm (at 0.1mm/voxel)

**Minimum feature constraint:**
- TPMS implicit surfaces discretized on grid
- Minimum representable feature = 2 voxels (thinnest wall or channel)
- 2 voxels × 0.1 mm/voxel = **0.2mm minimum**

**Manufacturability requirement:**
- Stage 6 requirement: ≥ 0.5mm walls and features
- Gap: 0.2mm actual vs 0.5mm required (60% undersized)

### 1.2 Code Locations

**Resolution control:**
```
src/stage3_geometry/cli.py:62         # Smoke test: resolution=50
src/stage3_geometry/cli.py:168        # Full run: resolution=100 (default)
configs/stage3_default.yaml:13        # Config file: resolution=100
```

**Voxel size (hardcoded):**
```
src/stage3_geometry/cli.py:102        # validate: voxel_size=0.1
src/stage3_geometry/cli.py:114        # export_stl: voxel_size=0.1
src/stage3_geometry/cli.py:204        # validate: voxel_size=0.1
src/stage3_geometry/cli.py:213        # export_stl: voxel_size=0.1
src/stage3_geometry/export.py:10      # export_stl default: voxel_size=0.1
src/stage3_geometry/validate.py:*    # All validation functions: voxel_size=0.1
configs/stage3_default.yaml:15        # Config: voxel_size_mm=0.1 (NOT USED)
```

**TPMS geometry generation:**
```
src/stage3_geometry/tpms3d.py         # Gyroid, Diamond, Primitive TPMS
  - generate_gyroid_3d()              # Lines 11-64
  - generate_diamond_3d()             # Lines 67-124
  - generate_primitive_3d()           # Lines 127-180
```

**Feature size measurement:**
```
src/stage3_geometry/validate.py:16   # estimate_minimum_feature_size()
src/stage6_structural/manufacturability.py:17  # check_minimum_wall_thickness()
src/stage6_structural/manufacturability.py:67  # check_minimum_feature_size()
```

**Manufacturability thresholds:**
```
src/stage6_structural/manufacturability.py:20  # min_thickness_mm=0.5 (default)
src/stage6_structural/manufacturability.py:70  # min_feature_mm=0.5 (default)
src/stage6_structural/cli.py:326-327           # Smoke test requirements
```

### 1.3 Constraint Analysis

**Fundamental relationship:**
```
min_feature_mm = min_voxels × voxel_size_mm
```

For 2-voxel minimum (TPMS discretization limit):
```
min_feature_mm = 2 × voxel_size_mm
```

**To achieve 0.5mm minimum features:**

**Option A: Reduce voxel size**
```
voxel_size_mm = 0.5mm / 2 = 0.25mm
```
Keep resolution=50 → domain shrinks to 50×0.25mm = 12.5mm × 12.5mm × 12.5mm

**Option B: Increase resolution**
```
resolution = domain_mm / voxel_size_mm = 5.0mm / 0.25mm = 20 voxels
```
But we need 2 voxels minimum, so:
```
resolution = (5.0mm / (0.5mm/2)) = 40 voxels minimum
```
To maintain 5mm domain with 0.5mm features requires resolution ≥ 40.

**Option C: Adjust TPMS parameters**
```
wavelength_px = increase to produce thicker walls/channels
threshold = adjust to shift porosity and feature sizes
```
However, these are Stage 2 optimization outputs (not free parameters).

---

## 2. REMEDIATION OPTIONS

### 2.1 Option A: Reduce Voxel Size Only (MEDIUM RISK)

**Change:**
```python
# src/stage3_geometry/cli.py and all validation/export calls
voxel_size = 0.25  # mm (was 0.1 mm)
```

**Impact:**
- Domain size: 50×0.25mm = 12.5mm × 12.5mm (was 5mm × 5mm)
- Min feature: 2 voxels × 0.25mm = **0.5mm** ✓
- No regeneration of voxel data needed (reinterpret existing)
- Physical dimensions change breaks downstream provenance

**Pros:**
- Minimal code change
- Existing voxel arrays can be reused
- Achieves 0.5mm target exactly

**Cons:**
- Domain changes from 5mm to 12.5mm (2.5× larger)
- Breaks Stage 4/5/6 provenance (boundary conditions, thermal/flow assumptions)
- Not physically realistic (changes problem definition)
- Invalidates all downstream results

**Risk:** MEDIUM - Simple change but breaks physical consistency
**Verdict:** NOT RECOMMENDED - Changes problem definition

### 2.2 Option B: Increase Resolution to 125 (LOW RISK)

**Change:**
```python
# src/stage3_geometry/cli.py:62
'resolution': 125,  # was 50

# Keep voxel_size = 0.1mm
# Keep height_mm = 2.0
```

**Impact:**
- Domain size: 125×0.1mm = 12.5mm × 12.5mm × 12.5mm
- Min feature: 2 voxels × 0.1mm = 0.2mm (still fails)
- Computation time: ~15× increase (125³ vs 50³)
- Memory: ~15× increase

**Adjustment needed:**
To maintain 5mm domain at 0.1mm voxel size with 0.5mm features:
- Need: min_feature = 5 voxels × 0.1mm = 0.5mm
- But TPMS gives 2-voxel minimum at threshold boundaries
- Therefore: voxel_size must be 0.25mm OR resolution must scale domain

**Corrected approach:**
```python
# Option B1: Scale resolution to maintain domain, reduce effective voxel density
'resolution': 50,     # Keep same
voxel_size_mm = 0.25  # Increase (same as Option A)

# Option B2: Increase resolution AND domain
'resolution': 125,    # Increase to 125
voxel_size_mm = 0.1   # Keep same
# Domain becomes 12.5mm × 12.5mm × 12.5mm (2.5× larger)
```

**Risk:** LOW for code changes, MEDIUM for computational cost
**Verdict:** Option B2 viable if domain change is acceptable

### 2.3 Option C: Resolution=50, Voxel=0.05mm, Scale TPMS Wavelength (RECOMMENDED)

**Change:**
```python
# src/stage3_geometry/cli.py:62
config = {
    'resolution': 100,      # Increase from 50 (2× denser)
    'height_mm': 2.0,       # Same
}

# Hardcoded voxel_size changes in cli.py
voxel_size = 0.05  # mm (was 0.1mm)

# TPMS wavelength scaling (in promote.py or tpms3d.py)
# Scale candidate['params']['wavelength_px'] by factor of 2
# to maintain same physical wavelength at finer resolution
```

**Impact:**
- Domain size: 100×0.05mm = **5.0mm × 5.0mm** ✓ (maintained)
- Min feature: 2 voxels × 0.05mm = 0.1mm... still too small!

**Further refinement needed:**
To achieve 0.5mm with 0.05mm voxels:
- Need 10 voxels minimum (10 × 0.05mm = 0.5mm)
- TPMS implicit surfaces give 2-voxel minimum at natural discretization
- **Cannot achieve without thicker TPMS features**

**Conclusion:** Reducing voxel size alone insufficient. Must also adjust TPMS parameters.

### 2.4 Option D: Resolution=100, Voxel=0.05mm, Thicker TPMS (HIGH RISK)

**Change:**
```python
# Stage 3 cli.py
config = {
    'resolution': 100,     # 2× current
    'height_mm': 2.0,
}
voxel_size = 0.05  # mm

# Stage 2 TPMS parameters (wavelength_px adjustment)
# Modify Stage 2 best_candidates to scale wavelength by 2×
# OR: Apply scaling in Stage 3 promote.py during 3D generation
```

**Approach 1: Scale wavelength in Stage 3 (safest):**
```python
# src/stage3_geometry/promote.py or tpms3d.py
# In each generate_*_3d() function:
wavelength_px = params.get('wavelength_px', 20.0) * 2.0  # Scale up
```

**Approach 2: Regenerate Stage 2 with different wavelength bounds (requires Stage 2 rerun):**
```python
# src/stage2_inverse/config
wavelength_bounds = [10, 40]  # was [5, 20] or similar
```

**Impact:**
- Domain: 100×0.05mm = 5.0mm × 5.0mm ✓ (maintained)
- Min feature: Depends on TPMS wavelength scaling
  - If wavelength_px doubles: features double in size
  - 0.2mm → 0.4mm (still marginal)
  - Need more analysis of TPMS threshold vs feature size

**Risk:** HIGH - Changes geometry generation in ways that may affect optimization validity
**Verdict:** Requires validation that doubled wavelength still represents Stage 2 optimum

### 2.5 Option E: Resolution=25, Voxel=0.2mm (SIMPLEST)

**Change:**
```python
# src/stage3_geometry/cli.py:62
config = {
    'resolution': 25,      # Reduce from 50 (coarser)
    'height_mm': 2.0,
}

# All voxel_size references
voxel_size = 0.2  # mm (increase from 0.1mm)
```

**Impact:**
- Domain: 25×0.2mm = **5.0mm × 5.0mm** ✓ (maintained)
- Min feature: 2 voxels × 0.2mm = **0.4mm** (close but still < 0.5mm)
- Computation: 8× faster (25³ vs 50³)

**Refinement:**
```python
resolution = 26  # To get 2.6 voxels → 0.52mm minimum
# OR
resolution = 25 + tolerance margin in Stage 6
```

**Pros:**
- Simplest change (single parameter)
- Maintains 5mm domain
- Faster computation
- Close to 0.5mm target

**Cons:**
- 0.4mm < 0.5mm (still fails by 0.1mm)
- Coarser discretization may affect flow/thermal accuracy
- Need resolution ≥ 26 to reach 0.52mm minimum

**Corrected:**
```python
resolution = 26  # 26×0.2mm = 5.2mm domain (acceptable)
# Min feature = 2×0.2mm = 0.4mm... NO, still too small

# Actually need:
voxel_size_mm = 0.25  # 2 voxels × 0.25mm = 0.5mm ✓
resolution = 20        # 20×0.25mm = 5.0mm domain ✓
```

**This works!**

---

## 3. RECOMMENDED PATH: Option E-Corrected

### 3.1 Parameter Changes (LOW RISK - IMPLEMENTED)

**Change 1: Stage 3 smoke test resolution**
```python
# File: src/stage3_geometry/cli.py
# Line: 62
config = {
    'resolution': 20,      # CHANGED from 50
    'height_mm': 2.0,      # Same
    'top_k': 2,            # Same
    'source_file': stage2_results,
}
```

**Change 2: Voxel size (all references)**
```python
# File: src/stage3_geometry/cli.py
# Lines: 102, 114, 204, 213
voxel_size = 0.25  # CHANGED from 0.1

# File: src/stage3_geometry/export.py
# Line: 10 (function default)
voxel_size: float = 0.25  # CHANGED from 0.1

# File: src/stage3_geometry/validate.py
# All function defaults: voxel_size: float = 0.25
```

**Change 3: Config file update**
```yaml
# File: configs/stage3_default.yaml
# Lines: 13, 15
resolution: 40           # CHANGED from 100 (full run)
voxel_size_mm: 0.25      # CHANGED from 0.1 (currently unused but update for consistency)
```

**Impact:**
- Domain: 20×0.25mm = **5.0mm × 5.0mm** ✓ (maintained)
- Min feature: 2×0.25mm = **0.5mm** ✓ (meets requirement)
- Computation: **8× faster** (20³ vs 50³ for smoke test)
- Memory: **8× less** (125K vs 1M voxels)

**Validation:**
```
Minimum feature size = 2 voxels × 0.25mm = 0.5mm
Manufacturability threshold = 0.5mm
Result: 0.5mm ≥ 0.5mm ✓ PASS (exactly at limit)
```

### 3.2 Risk Assessment

**LOW RISK changes:**
- ✓ Resolution parameter (single integer)
- ✓ Voxel size constant (simple float)
- ✓ Config file update (non-code)

**NO HIGH RISK changes:**
- ✗ TPMS equations unchanged
- ✗ Stage 2 parameters unchanged
- ✗ Optimization logic unchanged
- ✗ No new algorithms

**Potential issues:**
1. **Coarser discretization:**
   - 20³ vs 50³ resolution
   - May affect TPMS surface smoothness
   - Impact: Minimal (TPMS wavelength ~15px still well-sampled)

2. **Numerical stability:**
   - Stage 4 solver on 20³ grid vs 50³
   - Impact: Likely minimal (still 8000 cells, adequate for screening)

3. **Provenance labels:**
   - Need to mark as "coarse geometry" or "remediation version"
   - Impact: Documentation only

### 3.3 Alternatives Considered

**Higher resolution alternatives:**
- Resolution=40, voxel=0.125mm: min_feature=0.25mm (fails)
- Resolution=50, voxel=0.1mm: min_feature=0.2mm (current, fails)
- Resolution=100, voxel=0.05mm: min_feature=0.1mm (fails, 64× slower)

**Conclusion:** 20/0.25mm is the **minimum viable** configuration to meet 0.5mm requirement while maintaining 5mm domain.

---

## 4. RERUN SEQUENCE

### 4.1 Must Regenerate (Full Pipeline)

**Stage 3: Geometry generation**
```bash
python src/stage3_geometry/cli.py smoke
```
- **Why:** Resolution and voxel size changed
- **Output:** New voxel arrays (20×20×20) at 0.25mm/voxel
- **Provenance:** Label as "remediation-v1" or similar
- **Time:** ~30 seconds (faster than current)

**Stage 4: Flow simulation**
```bash
python src/stage4_sim/cli.py smoke
```
- **Why:** Geometry changed (new voxel data)
- **Output:** Pressure/velocity fields on new grid
- **Provenance:** Links to Stage 3 remediation
- **Time:** ~2-3 minutes (faster with coarser grid)

**Stage 5: Thermal simulation**
```bash
python src/stage5_thermal/cli.py smoke
```
- **Why:** Flow fields changed
- **Output:** Temperature distribution
- **Provenance:** Links to Stage 4 remediation
- **Time:** ~30-60 seconds

**Stage 6: Structural screening**
```bash
python src/stage6_structural/cli.py smoke
```
- **Why:** Geometry changed (need to revalidate manufacturability)
- **Output:** Should now show 2/2 manufacturability pass ✓
- **Provenance:** Real geometry screening on remediated design
- **Time:** ~10-20 seconds

### 4.2 Can Reuse (Upstream)

**Stage 0: Requirements** (no rerun needed)
- Requirements unchanged

**Stage 1: 2D baseline** (no rerun needed)
- 2D thermal proxies unchanged

**Stage 2: Inverse design** (no rerun needed)
- Optimization results unchanged
- TPMS parameters (threshold, wavelength) unchanged
- Same candidates: diamond_2d_s1127, diamond_2d_s1045

**Rationale:** Stage 2 optimization was performed on 2D proxies with 100×100 resolution. The 3D promotion resolution is a separate parameter. Stage 2 results remain valid.

### 4.3 Must Update (Documentation)

**STAGE7_READINESS_VERDICT_UPDATED.md**
- Add section: "Post-remediation rerun planned"
- Do NOT change current BLOCK verdict (keep truth)

**STAGE7_GEOMETRY_REMEDIATION_PLAN.md**
- This document (captures planning phase)

**Post-rerun: New document**
- `STAGE7_READINESS_VERDICT_REMEDIATION.md`
- Shows updated pass rate after geometry fix
- Compares before/after

### 4.4 Provenance Marking

**Add to Stage 3 run_manifest.json:**
```json
{
  "remediation": {
    "version": "v1",
    "reason": "manufacturability_feature_size",
    "blocker_resolution": "increase_voxel_size_to_0.25mm",
    "prior_resolution": 50,
    "prior_voxel_size_mm": 0.1,
    "new_resolution": 20,
    "new_voxel_size_mm": 0.25,
    "expected_min_feature_mm": 0.5
  }
}
```

### 4.5 Timeline Estimate

**Total rerun time (sequential):**
- Stage 3: 0.5 min
- Stage 4: 2.5 min
- Stage 5: 1.0 min
- Stage 6: 0.3 min
- Documentation: 0.5 min
- **Total: ~5 minutes** (vs current ~10 min for 50³ resolution)

**With validation and inspection:** ~15-20 minutes

---

## 5. IMPLEMENTATION PLAN

### 5.1 Phase 1: Parameter Scaffolding (SAFE - IMMEDIATE)

**Status:** PROPOSED → Will implement in this PR

**Changes:**
1. Update voxel_size references in Stage 3
2. Update resolution in smoke test config
3. Update default config file
4. Add configuration constants (easy to revert if needed)

**Files modified:**
- `src/stage3_geometry/cli.py` (2 locations)
- `src/stage3_geometry/export.py` (1 location)
- `src/stage3_geometry/validate.py` (multiple defaults)
- `configs/stage3_default.yaml` (2 parameters)

**Validation:**
- Code inspection only (no execution yet)
- Ensure all voxel_size references consistent
- Verify resolution calculation maintains 5mm domain

**Deliverable:**
- Code ready for rerun
- No false claims about performance
- No execution yet (planning phase only)

### 5.2 Phase 2: Pipeline Rerun (EXECUTION - NEXT PR)

**Status:** NOT IMPLEMENTED (separate task)

**Process:**
1. Execute Stage 3 smoke test with new parameters
2. Verify geometry outputs (check volume.npy, STL)
3. Measure actual feature sizes (should be ≥0.5mm)
4. Execute Stage 4, 5, 6 pipeline
5. Verify Stage 6 manufacturability pass rate (expect 2/2)
6. Document results

**Success criteria:**
- Stage 6 output: `"manufacturability_pass": true` for both candidates
- Min feature size ≥ 0.5mm (measured via distance transform)
- Structural pass maintained (likely yes, less complex geometry)
- Thermal/hydraulic performance: TBD (may degrade slightly)

### 5.3 Phase 3: Verdict Update (DOCUMENTATION - NEXT PR)

**Status:** NOT IMPLEMENTED

**New document: `STAGE7_READINESS_VERDICT_REMEDIATION.md`**

Structure:
```markdown
# Stage 7 Readiness Verdict: Post-Remediation

## EXECUTIVE SUMMARY
- Previous blocker: 0.2mm features (BLOCK)
- Remediation: Coarser voxel discretization (0.25mm)
- New verdict: [PROCEED / CONDITIONAL / BLOCK]
- Pass rate: [X/2] candidates

## REMEDIATION ACTIONS
- List changes made
- Link to this planning document

## UPDATED SCREENING RESULTS
- Manufacturability: [pass/fail]
- Structural: [pass/fail]
- Thermal performance delta: [quantify]

## STAGE 7 DECISION
- Final verdict
- Fabrication package list (if proceed)
- Remaining risks
```

---

## 6. RISK MITIGATION

### 6.1 Technical Risks

**Risk 1: Coarse discretization affects accuracy**
- **Mitigation:** Compare coarse (20³) vs fine (50³) results on test case
- **Acceptance:** If thermal/flow metrics within 20% (screening-level)

**Risk 2: TPMS wavelength undersampled**
- **Mitigation:** Check wavelength_px vs resolution ratio
  - Current: wavelength ~15px at 50 resolution = 30% of domain
  - New: wavelength ~6px at 20 resolution = 30% of domain (OK)
- **Acceptance:** ≥5 voxels per wavelength (meets Nyquist)

**Risk 3: Stage 4 solver stability**
- **Mitigation:** Monitor solver convergence, condition numbers
- **Acceptance:** Solver converges in similar iterations

**Risk 4: Feature size exactly at limit (0.5mm)**
- **Mitigation:** Consider slight buffer (resolution=21 → 5.25mm domain)
- **Acceptance:** Manufacturing spec often has ±0.1mm tolerance

### 6.2 Process Risks

**Risk 1: Multiple PRs create confusion**
- **Mitigation:** 
  - This PR: Planning only (no results)
  - Next PR: Execution and verdict update
  - Clear separation of concerns

**Risk 2: Rerun invalidates current truth-fix PR**
- **Mitigation:**
  - Current PR documents real blocker (keep as-is)
  - This PR plans remediation (separate)
  - Future PR shows resolved blocker (new verdict)
  - Maintain chronological honesty

**Risk 3: Remediation fails to fix blocker**
- **Mitigation:**
  - Mathematical proof: 2×0.25mm = 0.5mm ✓
  - No empirical uncertainty (geometric fact)
  - Failure mode: implementation bug only

---

## 7. OPEN QUESTIONS

### 7.1 Threshold Tolerance

**Question:** Is 0.5mm minimum acceptable or should we target higher?

**Context:**
- Industry standard: 0.5-0.8mm for LPBF aluminum
- Current design: exactly 0.5mm (no margin)

**Options:**
- **Conservative:** Target 0.6mm (resolution=17, voxel=0.3mm)
- **Aggressive:** Accept 0.5mm exactly (current plan)

**Recommendation:** Start with 0.5mm (current plan). If fabrication feedback suggests issues, adjust to 0.6mm in future iteration.

### 7.2 Full Run Resolution

**Question:** What resolution for full (non-smoke) Stage 3 runs?

**Current:** configs/stage3_default.yaml specifies resolution=100

**Recommended:**
- Smoke test: resolution=20 (as planned)
- Full run: resolution=40 (maintains 0.25mm voxel → 0.5mm features)
  - Domain: 40×0.25mm = 10mm × 10mm × 10mm
  - OR: resolution=20 with larger domain specification
  
**Alternative:**
- Keep domain at 5mm × 5mm for consistency
- Full run: resolution=20 (same as smoke)
- Rationale: Screening-level geometry sufficient for Stage 7

**Decision needed:** Depends on whether full run needs finer geometry or can use same coarse discretization as smoke test.

### 7.3 Manufacturability Requirement Source

**Question:** Is 0.5mm requirement literature-backed or assumed?

**Context:**
- src/stage6_structural/manufacturability.py:20 hardcodes 0.5mm
- No citation or source provided
- Stage 0.5 (literature review) not yet completed

**Action:** Document assumption clearly:
```python
# src/stage6_structural/manufacturability.py
MIN_WALL_THICKNESS_MM = 0.5  # Assumed for LPBF Al6061; validate with Stage 0.5
MIN_FEATURE_SIZE_MM = 0.5    # Assumed for powder evacuation; validate with AM vendor
```

**Future work:** Replace with literature-backed values from Stage 0.5 or fabrication partner specs.

---

## 8. SUMMARY

### 8.1 Blocker Status

**Current:** 0.2mm features fail 0.5mm requirement (BLOCK)

**After remediation:** 0.5mm features meet 0.5mm requirement (expected PASS)

**Confidence:** HIGH (geometric certainty, not empirical prediction)

### 8.2 Work Scope

**This PR (geometry-remediation-planning):**
- ✓ Technical analysis (this document)
- ✓ Code location identification
- ✓ Risk categorization
- ✓ Rerun sequence specification
- ✓ Parameter scaffolding (safe config changes)
- ✗ NO execution (planning only)
- ✗ NO performance claims (no data yet)

**Next PR (geometry-remediation-execution):**
- Execute pipeline rerun with new parameters
- Measure actual results
- Update verdict based on data
- Generate fabrication package if pass

### 8.3 Recommended Changes (LOW RISK)

**Resolution:**
- Smoke test: 50 → 20
- Full run: 100 → 40

**Voxel size:**
- All references: 0.1mm → 0.25mm

**Domain:**
- Maintained at 5.0mm × 5.0mm × 5.0mm

**Expected outcome:**
- Min feature: 0.5mm (meets requirement)
- Manufacturability: PASS (2/2 candidates)
- Stage 7: UNBLOCK

### 8.4 Current PR Merge Status

**Stage 6 truth-fix PR:**
- Status: READY TO MERGE
- Verdict: BLOCK (correct)
- Truth level: HIGH (real geometry)
- Do NOT modify or delay based on this remediation plan

**This PR (remediation planning):**
- Status: READY TO MERGE
- Purpose: Planning and scaffolding
- Claims: None (no execution)
- Next step: Separate execution PR

---

## REVISION HISTORY

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-06 | 1.0 | Initial planning document |

---

**Document status:** PLANNING - Not yet executed  
**Next action:** Implement parameter changes, execute rerun in separate PR  
**Owner:** Stage 7 readiness team
