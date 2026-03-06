# Geometry Remediation Planning PR - Review Guide

## Quick Summary

**Purpose:** Planning and scaffolding for Stage 7 manufacturability blocker resolution  
**Status:** Implementation complete, no execution performed  
**Risk level:** LOW (parameters only, no algorithm changes)  

## What's Changed

### New Files (3)
1. **STAGE7_GEOMETRY_REMEDIATION_PLAN.md** (762 lines)
   - Technical root cause analysis
   - 5 remediation options evaluated
   - Recommended path with full justification
   - Complete rerun sequence

2. **STAGE7_GEOMETRY_REMEDIATION_SUMMARY.md** (471 lines)
   - Implementation summary
   - What was done vs. not done
   - Technical validation
   - Next steps roadmap

3. **src/stage3_geometry/config.py** (148 lines)
   - Centralized configuration module
   - Voxel size: 0.1mm → 0.25mm
   - Resolution: 50 → 20 (smoke), 100 → 40 (full)
   - Self-validating (confirms 0.5mm achievable)

### Modified Files (4)
1. **src/stage3_geometry/cli.py**
   - Import and use config module
   - Add remediation provenance tracking
   - Replace hardcoded voxel_size=0.1 with config value

2. **src/stage3_geometry/export.py**
   - Update default: voxel_size=0.1 → 0.25

3. **src/stage3_geometry/validate.py**
   - Update defaults: voxel_size=0.1 → 0.25
   - Update min_feature_size_mm=0.1 → 0.5

4. **configs/stage3_default.yaml**
   - Update resolution: 100 → 40
   - Update voxel_size_mm: 0.1 → 0.25
   - Update min_feature_size_mm: 0.1 → 0.5

## Review Checklist

### Code Quality
- [ ] Config module properly structured and documented
- [ ] CLI changes minimal and surgical
- [ ] All hardcoded 0.1 replaced with config reference
- [ ] No execution paths triggered (planning only)

### Technical Correctness
- [ ] Math correct: 2 voxels × 0.25mm = 0.5mm ✓
- [ ] Domain preserved: 20 × 0.25mm = 5.0mm ✓
- [ ] Provenance tracking included
- [ ] No false performance claims

### Documentation
- [ ] Planning document comprehensive
- [ ] Summary clear on what's implemented vs. proposed
- [ ] Next steps well-defined
- [ ] No softening of current BLOCK verdict

### Risk Assessment
- [ ] Changes categorized as LOW risk
- [ ] No algorithm modifications
- [ ] Easy to revert (config.py only)
- [ ] No new dependencies

## Testing Performed

```bash
# Configuration validates correctly
python src/stage3_geometry/config.py
# Output: ✓ Configuration valid

# CLI imports without errors
python src/stage3_geometry/cli.py --help
# Output: Usage message

# Integration test
python -c "
from stage3_geometry import config as geom_config
valid, _ = geom_config.validate_configuration()
assert valid, 'Config must be valid'
assert geom_config.VOXEL_SIZE_MM == 0.25
assert geom_config.EXPECTED_MIN_FEATURE_MM == 0.5
print('✓ All checks pass')
"
```

## What Was NOT Done (Intentional)

❌ No Stage 3 smoke test execution  
❌ No Stage 4/5/6 pipeline rerun  
❌ No actual feature size measurements  
❌ No verdict changes to existing documents  
❌ No claims about manufacturability passing  

**Reason:** Separation of concerns. This PR = planning + scaffolding. Next PR = execution + results.

## Expected Next PR

**Title:** "Execute geometry remediation pipeline and update verdict"

**Contents:**
- Run `python src/stage3_geometry/cli.py smoke`
- Run downstream pipeline (Stages 4, 5, 6)
- Measure actual feature sizes (expect ≥0.5mm)
- Create `STAGE7_READINESS_VERDICT_REMEDIATION.md`
- Document pass/fail based on real data

**Timeline:** ~15-20 minutes for execution and documentation

## Merge Recommendation

✓ **Approve and merge** if:
- Code changes are minimal and correct
- Configuration validates
- Documentation is comprehensive
- No false claims made

This PR sets up clean separation between:
1. Current truth (BLOCK due to 0.2mm features)
2. Planning (this PR)
3. Execution and new verdict (next PR)

## Questions?

See detailed analysis in:
- `STAGE7_GEOMETRY_REMEDIATION_PLAN.md` - Technical depth
- `STAGE7_GEOMETRY_REMEDIATION_SUMMARY.md` - Implementation summary

---

**Reviewer:** Please verify code only, no smoke test required for this PR.
