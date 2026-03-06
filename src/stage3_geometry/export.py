"""Geometry export utilities.

Exports 3D volumes to mesh-ready file formats (STL, VTK).
"""

import numpy as np
import os
from typing import Dict, Any, Optional


def export_stl_from_volume(
    volume: np.ndarray,
    filepath: str,
    voxel_size: float = 0.1
) -> bool:
    """Export 3D binary volume to STL file using marching cubes.
    
    Args:
        volume: 3D binary array (nz, ny, nx) where 1=fluid, 0=solid
        filepath: Output STL file path
        voxel_size: Size of each voxel in mm
        
    Returns:
        True if export succeeded, False otherwise
    """
    try:
        from skimage import measure
        
        # Run marching cubes on the volume
        # We want surface of fluid region (value=1)
        verts, faces, normals, values = measure.marching_cubes(
            volume, level=0.5, spacing=(voxel_size, voxel_size, voxel_size)
        )
        
        # Write STL file (ASCII format)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(f"solid geometry\n")
            
            for face in faces:
                # Get vertices of this triangle
                v0, v1, v2 = verts[face[0]], verts[face[1]], verts[face[2]]
                
                # Calculate normal
                edge1 = v1 - v0
                edge2 = v2 - v0
                normal = np.cross(edge1, edge2)
                norm = np.linalg.norm(normal)
                if norm > 1e-10:
                    normal = normal / norm
                else:
                    normal = np.array([0, 0, 1])
                
                f.write(f"  facet normal {normal[0]:.6e} {normal[1]:.6e} {normal[2]:.6e}\n")
                f.write(f"    outer loop\n")
                f.write(f"      vertex {v0[0]:.6e} {v0[1]:.6e} {v0[2]:.6e}\n")
                f.write(f"      vertex {v1[0]:.6e} {v1[1]:.6e} {v1[2]:.6e}\n")
                f.write(f"      vertex {v2[0]:.6e} {v2[1]:.6e} {v2[2]:.6e}\n")
                f.write(f"    endloop\n")
                f.write(f"  endfacet\n")
            
            f.write(f"endsolid geometry\n")
        
        print(f"Exported STL to {filepath} ({len(faces)} triangles)")
        return True
        
    except Exception as e:
        print(f"STL export failed: {e}")
        return False


def export_raw_volume(
    volume: np.ndarray,
    filepath: str,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """Export raw volume data as numpy array.
    
    Args:
        volume: 3D binary array
        filepath: Output .npy file path
        metadata: Optional metadata to save alongside
        
    Returns:
        True if export succeeded
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save volume
        np.save(filepath, volume)
        print(f"Exported raw volume to {filepath}")
        
        # Save metadata if provided
        if metadata:
            import json
            metadata_path = filepath.replace('.npy', '_metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Raw volume export failed: {e}")
        return False


def get_volume_info(volume: np.ndarray) -> Dict[str, Any]:
    """Get basic information about a 3D volume.
    
    Args:
        volume: 3D binary array
        
    Returns:
        Dictionary with volume statistics
    """
    return {
        'shape': volume.shape,
        'dtype': str(volume.dtype),
        'porosity': float(np.mean(volume)),
        'fluid_voxels': int(np.sum(volume)),
        'solid_voxels': int(np.prod(volume.shape) - np.sum(volume)),
        'total_voxels': int(np.prod(volume.shape)),
    }
