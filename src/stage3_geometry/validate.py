"""Geometry validation and mesh-readiness checks.

Performs sanity checks on 3D geometry to assess mesh readiness.
"""

import numpy as np
from typing import Dict, Any, List, Tuple
from scipy import ndimage


def check_connectivity(volume: np.ndarray) -> Dict[str, Any]:
    """Check connectivity of fluid regions.
    
    Args:
        volume: 3D binary array (1=fluid, 0=solid)
        
    Returns:
        Dictionary with connectivity metrics
    """
    # Label connected components in fluid region
    labeled, num_components = ndimage.label(volume)
    
    # Find largest component
    if num_components > 0:
        component_sizes = [np.sum(labeled == i) for i in range(1, num_components + 1)]
        largest_component_size = max(component_sizes)
        largest_component_fraction = largest_component_size / np.sum(volume)
    else:
        largest_component_size = 0
        largest_component_fraction = 0
    
    return {
        'num_fluid_components': num_components,
        'largest_component_size': largest_component_size,
        'largest_component_fraction': largest_component_fraction,
        'is_connected': num_components == 1,
    }


def check_solid_connectivity(volume: np.ndarray) -> Dict[str, Any]:
    """Check connectivity of solid regions.
    
    Args:
        volume: 3D binary array (1=fluid, 0=solid)
        
    Returns:
        Dictionary with solid connectivity metrics
    """
    # Invert to check solid
    solid_volume = 1 - volume
    
    # Label connected components in solid region
    labeled, num_components = ndimage.label(solid_volume)
    
    # Find largest component
    if num_components > 0:
        component_sizes = [np.sum(labeled == i) for i in range(1, num_components + 1)]
        largest_component_size = max(component_sizes)
        largest_component_fraction = largest_component_size / np.sum(solid_volume)
    else:
        largest_component_size = 0
        largest_component_fraction = 0
    
    return {
        'num_solid_components': num_components,
        'largest_solid_component_size': largest_component_size,
        'largest_solid_component_fraction': largest_component_fraction,
        'solid_is_connected': num_components == 1,
    }


def estimate_minimum_feature_size(volume: np.ndarray, voxel_size: float = 0.1) -> Dict[str, Any]:
    """Estimate minimum feature size using distance transform.
    
    Args:
        volume: 3D binary array (1=fluid, 0=solid)
        voxel_size: Size of each voxel in mm
        
    Returns:
        Dictionary with feature size estimates
    """
    # Distance transform of fluid region
    fluid_dist = ndimage.distance_transform_edt(volume)
    
    # Distance transform of solid region
    solid_dist = ndimage.distance_transform_edt(1 - volume)
    
    # Estimate minimum channel width (2 * min distance in fluid)
    if np.sum(volume) > 0:
        min_channel_diameter_voxels = 2 * np.min(fluid_dist[volume > 0])
        min_channel_diameter_mm = min_channel_diameter_voxels * voxel_size
    else:
        min_channel_diameter_mm = 0
    
    # Estimate minimum wall thickness (2 * min distance in solid)
    if np.sum(1 - volume) > 0:
        min_wall_thickness_voxels = 2 * np.min(solid_dist[volume == 0])
        min_wall_thickness_mm = min_wall_thickness_voxels * voxel_size
    else:
        min_wall_thickness_mm = 0
    
    return {
        'min_channel_diameter_mm': float(min_channel_diameter_mm),
        'min_wall_thickness_mm': float(min_wall_thickness_mm),
        'min_channel_diameter_voxels': float(min_channel_diameter_voxels) if np.sum(volume) > 0 else 0,
        'min_wall_thickness_voxels': float(min_wall_thickness_voxels) if np.sum(1-volume) > 0 else 0,
    }


def check_bounding_box(volume: np.ndarray, voxel_size: float = 0.1) -> Dict[str, Any]:
    """Check bounding box dimensions.
    
    Args:
        volume: 3D binary array
        voxel_size: Size of each voxel in mm
        
    Returns:
        Dictionary with bounding box info
    """
    nz, ny, nx = volume.shape
    
    return {
        'dimensions_voxels': {'nx': nx, 'ny': ny, 'nz': nz},
        'dimensions_mm': {
            'x': nx * voxel_size,
            'y': ny * voxel_size,
            'z': nz * voxel_size
        },
        'total_volume_mm3': nx * ny * nz * (voxel_size ** 3),
    }


def validate_geometry(
    volume: np.ndarray,
    voxel_size: float = 0.1,
    min_feature_size_mm: float = 0.1,
    require_connected: bool = True
) -> Tuple[bool, Dict[str, Any], List[str]]:
    """Validate 3D geometry for mesh readiness.
    
    Args:
        volume: 3D binary array (1=fluid, 0=solid)
        voxel_size: Size of each voxel in mm
        min_feature_size_mm: Minimum acceptable feature size in mm
        require_connected: Whether to require single connected fluid region
        
    Returns:
        Tuple of (is_valid, validation_results, errors)
    """
    errors = []
    results = {}
    
    # Check basic properties
    results['porosity'] = float(np.mean(volume))
    if results['porosity'] <= 0 or results['porosity'] >= 1:
        errors.append(f"Invalid porosity: {results['porosity']}")
    
    # Check connectivity
    connectivity = check_connectivity(volume)
    results['connectivity'] = connectivity
    
    if require_connected and not connectivity['is_connected']:
        errors.append(f"Fluid region not connected ({connectivity['num_fluid_components']} components)")
    
    # Check solid connectivity
    solid_connectivity = check_solid_connectivity(volume)
    results['solid_connectivity'] = solid_connectivity
    
    # Check feature sizes
    feature_sizes = estimate_minimum_feature_size(volume, voxel_size)
    results['feature_sizes'] = feature_sizes
    
    if feature_sizes['min_channel_diameter_mm'] < min_feature_size_mm:
        errors.append(
            f"Channel too narrow: {feature_sizes['min_channel_diameter_mm']:.3f}mm "
            f"< {min_feature_size_mm}mm"
        )
    
    if feature_sizes['min_wall_thickness_mm'] < min_feature_size_mm:
        errors.append(
            f"Wall too thin: {feature_sizes['min_wall_thickness_mm']:.3f}mm "
            f"< {min_feature_size_mm}mm"
        )
    
    # Check bounding box
    bbox = check_bounding_box(volume, voxel_size)
    results['bounding_box'] = bbox
    
    is_valid = len(errors) == 0
    
    return is_valid, results, errors


def check_stl_export_feasible(volume: np.ndarray, max_triangles: int = 1000000) -> Tuple[bool, str]:
    """Check if STL export is feasible given volume size.
    
    Args:
        volume: 3D binary array
        max_triangles: Maximum acceptable triangle count
        
    Returns:
        Tuple of (is_feasible, message)
    """
    # Estimate triangle count (rough heuristic: ~2 triangles per surface voxel)
    # Count voxels at interfaces
    from scipy.ndimage import convolve
    
    # Simple edge detection kernel
    kernel = np.ones((3, 3, 3))
    kernel[1, 1, 1] = -26
    
    edges = np.abs(convolve(volume.astype(float), kernel, mode='constant'))
    surface_voxels = np.sum(edges > 0)
    estimated_triangles = surface_voxels * 2
    
    if estimated_triangles > max_triangles:
        return False, f"Too many triangles: ~{estimated_triangles} > {max_triangles}"
    
    return True, f"Estimated ~{estimated_triangles} triangles"
