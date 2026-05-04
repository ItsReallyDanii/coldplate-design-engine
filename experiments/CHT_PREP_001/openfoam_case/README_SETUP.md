# OpenFOAM Case Setup Instructions

## Prerequisites

OpenFOAM 11 (or v2312) installed via WSL2 Ubuntu.

## Step-by-step

### 1. Export STL geometry (on Windows, in repo root)

```bash
cd coldplate-design-engine
python experiments/CHT_PREP_001/export_stl.py --geometry serpentine --resolution 40

# Copy STL to case directory
copy experiments\CHT_PREP_001\serpentine_solid.stl experiments\CHT_PREP_001\openfoam_case\constant\triSurface\
```

### 2. Enter WSL and navigate to the case

```bash
wsl
cd /mnt/c/Users/slyki/OneDrive/Desktop/coldplate-topgpbridge/coldplate-design-engine/experiments/CHT_PREP_001/openfoam_case

# Source OpenFOAM
source /opt/openfoam11/etc/bashrc
```

### 3. Generate background mesh

```bash
blockMesh
```

Expected: "End" with no errors, reports ~64000 cells.

### 4. Create body-fitted mesh (requires snappyHexMeshDict)

NOTE: snappyHexMeshDict is the most complex config file. For the proof-of-life,
an alternative approach is to use the blockMesh directly as a voxel-style mesh
(no snappyHexMesh) and assign regions based on the voxel geometry.

For snappyHexMesh approach:
```bash
snappyHexMesh -overwrite
```

For voxel-direct approach (simpler for proof-of-life):
Use setFields or topoSet to mark cells as fluid/solid based on a cellZone definition
derived from the voxel grid coordinates.

### 5. Split regions

```bash
splitMeshRegions -cellZones -overwrite
```

This creates separate polyMesh directories for fluid and solid regions.

### 6. Set boundary conditions

Copy 0/ templates to 0/fluid/ and 0/solid/ and set:
- Fluid inlet: fixedValue U, fixedValue T=298.15K
- Fluid outlet: zeroGradient
- Bottom wall (solid): fixedGradient T (heat flux = 1e6 W/m^2)
- All other walls: adiabatic (zeroGradient T)
- Fluid-solid interface: coupled (turbulentTemperatureCoupledBaffleMixed)

### 7. Set material properties

Create constant/fluid/thermophysicalProperties and constant/solid/thermophysicalProperties.

### 8. Run solver

```bash
chtMultiRegionFoam
```

### 9. Check convergence

```bash
grep "Time =" log.chtMultiRegionFoam | tail
foamLog log.chtMultiRegionFoam
```

### 10. Extract results

```bash
postProcess -func "fieldMinMax(T)" -region solid
postProcess -func "patchAverage(name=inlet, p_rgh)" -region fluid
```

## Known complexity

The hardest part is step 4-6: creating proper multi-region mesh with coupled BCs.
OpenFOAM's chtMultiRegionFoam tutorials (e.g., `$FOAM_TUTORIALS/heatTransfer/chtMultiRegionFoam/`)
provide working examples to copy from.

Recommended tutorial to study first:
```bash
ls $FOAM_TUTORIALS/heatTransfer/chtMultiRegionFoam/
```

Copy a tutorial, get it running, then swap the geometry.
