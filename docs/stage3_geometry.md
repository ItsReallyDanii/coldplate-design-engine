# Stage 3: 3D Geometry Promotion and Meshing Readiness

## Overview

Stage 3 promotes top Stage 2 candidates from 2D proxy representations to true 3D parametric geometry with mesh-ready exports and validation.

**IMPORTANT:** Stage 3 does NOT prove thermal-hydraulic superiority. Stage 3 does NOT replace CFD/CHT. Stage 3 provides geometry artifacts for Stage 4 simulation.

## Scope

Stage 3 takes ranked candidates from Stage 2 inverse design and:

1. **Loads** top-k candidates from `best_candidates.csv`
2. **Promotes** 2D families to deterministic 3D parametric geometry
3. **Exports** mesh-ready artifacts (STL, raw volume)
4. **Validates** geometry quality and mesh readiness
5. **Records** full provenance from Stage 2 through 3D generation

## 2D to 3D Family Mappings

### Channel Families

| Stage 2 Family | Stage 3 Method | Description |
|----------------|----------------|-------------|
| `straight_channel` | Extruded 3D | Straight channels extruded in Z direction |
| `serpentine_channel` | Extruded 3D | Serpentine channels extruded in Z direction |
| `pin_fin` | 3D cylindrical array | Cylindrical pin-fin obstacles in regular array |

### TPMS Families

| Stage 2 Family | Stage 3 Method | Description |
|----------------|----------------|-------------|
| `gyroid_2d` | 3D implicit TPMS | True 3D gyroid from implicit surface equation |
| `diamond_2d` | 3D implicit TPMS | True 3D diamond (Schwarz-D) from implicit surface equation |
| `primitive_2d` | 3D implicit TPMS | True 3D primitive (Schwarz-P) from implicit surface equation |

**Note:** TPMS families labeled as "2D proxy" in Stage 1-2 become true 3D triply periodic minimal surfaces in Stage 3 using implicit field equations:

- **Gyroid:** `sin(x)cos(y) + sin(y)cos(z) + sin(z)cos(x) = threshold`
- **Diamond:** `sin(x)sin(y)sin(z) + sin(x)cos(y)cos(z) + cos(x)sin(y)cos(z) + cos(x)cos(y)sin(z) = threshold`
- **Primitive:** `cos(x) + cos(y) + cos(z) = threshold`

## Exports

Stage 3 generates for each candidate:

1. **STL file** - ASCII STL mesh from marching cubes (mesh-ready for CFD/FEA)
2. **Raw volume** - Binary 3D numpy array (`.npy`) with metadata
3. **Provenance record** - JSON with full traceability
4. **Validation report** - JSON with geometry checks

## Validation Checks

Stage 3 validates geometry quality:

- **Connectivity** - Checks if fluid region is connected
- **Component count** - Counts disconnected fluid/solid regions
- **Feature sizes** - Estimates minimum channel diameter and wall thickness
- **Bounding box** - Verifies dimensions and volume
- **STL feasibility** - Estimates triangle count

**Pass criteria:**
- Porosity in valid range (0 < p < 1)
- Minimum feature sizes above threshold (default 0.1mm)
- Optional: single connected fluid region

## Provenance

Stage 3 records full traceability:

```json
{
  "stage2_source": {
    "rank": 1,
    "family": "diamond_2d",
    "seed": 1127,
    "total_score": 2049.64,
    "params": {...},
    "metrics": {...}
  },
  "promotion": {
    "volume_metadata": {...},
    "success": true
  },
  "validation": {...},
  "exports": {
    "stl": "path/to/geometry.stl",
    "raw": "path/to/volume.npy"
  }
}
```

## Limitations

- **NOT a thermal-hydraulic validation** - Stage 3 generates geometry only
- **NOT a CFD result** - No flow or thermal analysis performed
- **NOT a manufacturability check** - Basic geometric sanity only
- **NOT a performance proof** - Stage 2 scores are proxy-based

Stage 4 (CFD) is required for real thermal-hydraulic claims.

## Stage 3 Gate Criteria

Stage 3 **PASS** requires:

- ✓ Top Stage 2 candidates loaded successfully
- ✓ At least one channel family promoted to 3D
- ✓ At least one TPMS family promoted to 3D
- ✓ Geometry exports created reproducibly
- ✓ Validation checks executed and pass for majority
- ✓ Results reproducible from provenance records
- ✓ Documentation accurate
- ✓ Tests pass

Stage 3 **FAIL** if:

- ✗ 3D promotion is non-deterministic
- ✗ Exports are broken or unusable
- ✗ No validation exists
- ✗ Commands don't work
- ✗ Overclaiming CFD/physical readiness

## Configuration Parameters

See `configs/stage3_default.yaml`:

```yaml
stage2_results: results/stage2_inverse/best_candidates.csv
top_k: 5  # Number of candidates to promote
resolution: 100  # Grid resolution (nx=ny=nz)
height_mm: 2.0  # Height of 3D geometry
voxel_size_mm: 0.1  # Voxel size for validation
min_feature_size_mm: 0.1  # Minimum feature threshold
output_dir: results/stage3_geometry
```

## Output Structure

```
results/stage3_geometry/
├── run_manifest.json          # Run metadata
├── summary.md                  # Human-readable summary
├── summary.json                # Machine-readable summary
└── candidate_01_diamond_2d_s1127/
    ├── geometry/
    │   ├── geometry.stl        # Mesh-ready STL
    │   ├── volume.npy          # Raw 3D volume
    │   └── volume_metadata.json # Volume metadata
    ├── validation/
    │   └── validation_report.json
    └── provenance.json         # Full traceability
```

## Next Stage

Stage 4 (CFD simulation) will use these geometry artifacts to run matched-constraint flow and thermal simulations.
