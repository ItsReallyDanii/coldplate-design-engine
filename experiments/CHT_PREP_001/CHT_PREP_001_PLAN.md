# CHT_PREP_001: OpenFOAM Proof-of-Life

**Date:** 2026-04-30
**Status:** PLAN + INFRASTRUCTURE PREP (no science claims)
**Goal:** Get chtMultiRegionFoam running on the simplest possible case -- serpentine, uniform heat flux, coarse mesh.

---

## 1. Environment Audit

| Tool | Status |
|------|--------|
| OpenFOAM | NOT INSTALLED |
| WSL | FOUND (C:\WINDOWS\system32\wsl.EXE) |
| Docker | FOUND (C:\Program Files\Docker\Docker\resources\bin\docker.EXE) |
| ParaView | NOT INSTALLED |

---

## 2. Installation Path Options

### Option A: WSL2 + Ubuntu + OpenFOAM (RECOMMENDED)

Fastest path to a working OpenFOAM environment on Windows. OpenFOAM runs natively on Linux; WSL2 provides a real Linux kernel.

```bash
# Step 1: Install Ubuntu on WSL2 (if not already)
wsl --install -d Ubuntu-22.04

# Step 2: Inside WSL Ubuntu, add OpenFOAM repository
sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key | apt-key add -"
sudo add-apt-repository http://dl.openfoam.org/ubuntu
sudo apt update

# Step 3: Install OpenFOAM v11 (or v2312 from openfoam.com)
sudo apt install openfoam11

# Step 4: Source OpenFOAM environment
echo "source /opt/openfoam11/etc/bashrc" >> ~/.bashrc
source ~/.bashrc

# Step 5: Verify
which chtMultiRegionFoam
blockMesh -help
```

Estimated time: 15-30 minutes.

Your Windows files are accessible from WSL at `/mnt/c/Users/slyki/...`

### Option B: Docker

```bash
# Pull OpenFOAM image
docker pull openfoam/openfoam11-paraview510

# Run interactive container with repo mounted
docker run -it -v "C:\Users\slyki\OneDrive\Desktop\coldplate-topgpbridge:/workspace" openfoam/openfoam11-paraview510
```

Pros: No WSL config needed. Clean isolation.
Cons: Slightly more friction for file I/O. ParaView inside Docker needs X11 forwarding.

### Option C: Cloud (Jules / GitHub Codespaces)

Use a Linux cloud VM. Install OpenFOAM there. Upload geometry STLs, run solver, download results.

Pros: No local install. Potentially more compute.
Cons: Latency. File transfer friction. Costs if using paid compute.

### Recommendation

**Option A (WSL2 + Ubuntu).** You already have WSL. OpenFOAM installs in one command. Files are shared. This is the standard path for OpenFOAM on Windows.

---

## 3. Pipeline: Voxel Geometry to OpenFOAM Case

```
[Voxel grid]              -- numpy uint8 array from screening pipeline
     |
     v
[export_stl.py]           -- marching cubes -> STL (solid-phase surface)
     |
     v
[STL file]                -- geometry.stl (watertight solid-phase mesh)
     |
     v
[blockMeshDict]           -- background hex grid covering 10mm domain
     |
     v
[snappyHexMeshDict]       -- snap/refine around STL to create body-fitted mesh
     |
     v
[OpenFOAM case]           -- system/, constant/, 0/ directories
     |                       fluid + solid regions defined
     v
[chtMultiRegionFoam]      -- solve coupled N-S + energy in both regions
     |
     v
[postProcess]             -- extract T_peak, T_p95, delta_P, Q_flow
```

---

## 4. Proof-of-Life Definition

### What "proof-of-life" means

The minimum demonstration that the pipeline works end-to-end:

1. STL exports without errors
2. blockMesh creates a hex background grid
3. snappyHexMesh creates a body-fitted mesh with fluid + solid regions
4. chtMultiRegionFoam starts and residuals decrease
5. Solution converges (residuals < 1e-4)
6. Post-processing extracts T_peak, delta_P

### Pass criteria

| Check | Pass condition |
|-------|----------------|
| STL export | File exists, > 1KB, valid solid/endsolid |
| blockMesh | Exits with no errors, reports cell count |
| snappyHexMesh | Exits with no errors, creates polyMesh for fluid and solid regions |
| checkMesh | No fatal errors (warnings OK for coarse mesh) |
| chtMultiRegionFoam | Runs for at least 100 iterations without diverging |
| Residuals | All below 1e-3 by end of run |
| T_peak extractable | postProcess or grep from log produces a temperature value |
| delta_P extractable | Pressure difference between inlet/outlet patches |

### Fail criteria

| Check | Fail condition |
|-------|----------------|
| STL not watertight | snappyHexMesh will fail to create regions |
| Mesh quality too low | checkMesh reports fatal errors (non-orthogonality > 85, etc.) |
| Solver diverges | Residuals increase monotonically |
| Regions not created | fluid/solid split fails |

### Geometry for proof-of-life

**Serpentine only.** Simplest geometry. If this works, diamond and hybrid will too (TPMS surfaces are smoother than channel walls).

**Uniform heat flux only.** Simplest BC. Non-uniform heat maps are a BC change, not a mesh change.

**Coarse mesh only.** ~200K cells. Enough to verify the pipeline works. Not enough for publication results.

---

## 5. Files to Create

### Already in this directory

| File | Status | Description |
|------|--------|-------------|
| CHT_PREP_001_PLAN.md | THIS FILE | Plan document |
| export_stl.py | TO CREATE | Voxel-to-STL conversion script |
| openfoam_case_template/ | TO CREATE | Template OpenFOAM case directory |

### OpenFOAM case structure (to create)

```
openfoam_case_template/
  system/
    blockMeshDict           -- background hex grid
    snappyHexMeshDict       -- snap to STL geometry
    controlDict             -- solver settings, timestep, endTime
    fvSchemes               -- discretization schemes
    fvSolution              -- solver tolerances
    decomposeParDict        -- parallel decomposition (if needed)
  constant/
    fluid/
      thermophysicalProperties   -- water properties
    solid/
      thermophysicalProperties   -- aluminum properties
    triSurface/
      serpentine.stl             -- geometry (copied from export)
  0/
    fluid/
      U                          -- velocity BC
      p_rgh                      -- pressure BC
      T                          -- temperature BC
    solid/
      T                          -- temperature BC (heat flux on bottom)
```

---

## 6. Estimated Timeline

| Step | Time |
|------|------|
| Install OpenFOAM via WSL2 | 30 min |
| Write export_stl.py + test | 30 min |
| Create OpenFOAM case template | 1-2 hrs |
| Run blockMesh + snappyHexMesh | 30 min (including debugging) |
| Run chtMultiRegionFoam (coarse) | 15-30 min compute |
| Verify outputs | 30 min |
| **Total to proof-of-life** | **3-5 hours** |

---

## 7. Labels

This is infrastructure validation. No science claims.

INFRASTRUCTURE / NOT_A_RESULT / NO_CLAIM
