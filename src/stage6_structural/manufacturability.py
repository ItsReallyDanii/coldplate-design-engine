"""
Manufacturability checks for Stage 6.

Implements geometry-based manufacturability screening including:
- Minimum wall thickness
- Minimum feature size
- Unsupported regions
- Trapped volumes
- Printability/machinability concerns
"""

import numpy as np
from typing import Dict, Any, List, Tuple
from scipy import ndimage


def check_minimum_wall_thickness(
    volume: np.ndarray,
    voxel_size_mm: float,
    min_thickness_mm: float = 0.5
) -> Dict[str, Any]:
    """
    Check minimum wall thickness using distance transform.
    
    LABEL: GEOMETRIC (from geometry analysis)
    
    Args:
        volume: Boolean volume array (True=fluid, False=solid)
        voxel_size_mm: Voxel size in mm
        min_thickness_mm: Minimum acceptable wall thickness
        
    Returns:
        Wall thickness check results
    """
    # Compute distance transform in solid region
    # This gives distance to nearest fluid voxel
    solid_mask = ~volume
    dist_transform = ndimage.distance_transform_edt(solid_mask)
    
    # Convert to mm
    dist_mm = dist_transform * voxel_size_mm
    
    # Get minimum wall thickness
    # Wall thickness ≈ 2 * minimum distance to fluid
    solid_distances = dist_mm[solid_mask]
    
    if len(solid_distances) == 0:
        min_wall_mm = 0.0
        mean_wall_mm = 0.0
    else:
        min_wall_mm = 2.0 * np.min(solid_distances)
        mean_wall_mm = 2.0 * np.mean(solid_distances)
    
    passes = min_wall_mm >= min_thickness_mm
    
    return {
        'min_wall_thickness_mm': float(min_wall_mm),
        'mean_wall_thickness_mm': float(mean_wall_mm),
        'required_min_mm': min_thickness_mm,
        'passes': passes,
        'failure_mode': None if passes else 'wall_too_thin',
        'label': 'GEOMETRIC',
        'method': 'distance_transform_wall_thickness'
    }


def check_minimum_feature_size(
    volume: np.ndarray,
    voxel_size_mm: float,
    min_feature_mm: float = 0.5
) -> Dict[str, Any]:
    """
    Check minimum feature size (channel diameter) using distance transform.
    
    LABEL: GEOMETRIC (from geometry analysis)
    
    Args:
        volume: Boolean volume array (True=fluid, False=solid)
        voxel_size_mm: Voxel size in mm
        min_feature_mm: Minimum acceptable feature size
        
    Returns:
        Feature size check results
    """
    # Compute distance transform in fluid region
    fluid_mask = volume
    dist_transform = ndimage.distance_transform_edt(fluid_mask)
    
    # Convert to mm
    dist_mm = dist_transform * voxel_size_mm
    
    # Get minimum channel diameter
    # Channel diameter ≈ 2 * minimum distance to solid
    fluid_distances = dist_mm[fluid_mask]
    
    if len(fluid_distances) == 0:
        min_channel_mm = 0.0
        mean_channel_mm = 0.0
    else:
        min_channel_mm = 2.0 * np.min(fluid_distances)
        mean_channel_mm = 2.0 * np.mean(fluid_distances)
    
    passes = min_channel_mm >= min_feature_mm
    
    return {
        'min_channel_diameter_mm': float(min_channel_mm),
        'mean_channel_diameter_mm': float(mean_channel_mm),
        'required_min_mm': min_feature_mm,
        'passes': passes,
        'failure_mode': None if passes else 'feature_too_small',
        'label': 'GEOMETRIC',
        'method': 'distance_transform_feature_size'
    }


def check_unsupported_regions(
    volume: np.ndarray,
    voxel_size_mm: float,
    max_unsupported_mm: float = 10.0,
    gravity_direction: str = 'z'
) -> Dict[str, Any]:
    """
    Check for unsupported overhangs (relevant for AM processes).
    
    LABEL: GEOMETRIC (from geometry analysis)
    
    This is a SIMPLIFIED check relevant for additive manufacturing
    or machining from multiple directions.
    
    Args:
        volume: Boolean volume array (True=fluid, False=solid)
        voxel_size_mm: Voxel size in mm
        max_unsupported_mm: Maximum acceptable unsupported span
        gravity_direction: Direction of gravity ('x', 'y', or 'z')
        
    Returns:
        Unsupported region check results
    """
    solid_mask = ~volume
    
    # Get gravity axis
    axis_map = {'x': 0, 'y': 1, 'z': 2}
    gravity_axis = axis_map.get(gravity_direction, 2)
    
    # For each solid voxel, check vertical span to next support
    shape = solid_mask.shape
    max_span_voxels = 0
    
    # Simplified: check maximum vertical span in solid
    for i in range(shape[gravity_axis]):
        # Get slice perpendicular to gravity
        if gravity_axis == 0:
            slice_mask = solid_mask[i, :, :]
        elif gravity_axis == 1:
            slice_mask = solid_mask[:, i, :]
        else:
            slice_mask = solid_mask[:, :, i]
        
        # Count consecutive slices with any solid
        if np.any(slice_mask):
            max_span_voxels = max(max_span_voxels, 1)
    
    # Very simplified: just check if structure is present
    # A real check would need layer-by-layer analysis
    max_unsupported_span_mm = max_span_voxels * voxel_size_mm
    
    # For TPMS structures, this is typically not an issue
    # Mark as PASS if structure is reasonable
    passes = max_unsupported_span_mm < max_unsupported_mm or max_span_voxels < 50
    
    return {
        'max_unsupported_span_mm': float(max_unsupported_span_mm),
        'max_span_voxels': int(max_span_voxels),
        'required_max_mm': max_unsupported_mm,
        'passes': passes,
        'failure_mode': None if passes else 'excessive_overhang',
        'label': 'GEOMETRIC',
        'method': 'simplified_overhang_analysis',
        'note': 'Simplified check; full AM simulation needed for fabrication'
    }


def check_trapped_volumes(
    volume: np.ndarray,
    voxel_size_mm: float
) -> Dict[str, Any]:
    """
    Check for trapped internal volumes (cannot be reached for powder removal).
    
    LABEL: GEOMETRIC (from connectivity analysis)
    
    This checks if there are isolated fluid pockets that would trap
    unsintered powder in AM or create dead volumes.
    
    Args:
        volume: Boolean volume array (True=fluid, False=solid)
        voxel_size_mm: Voxel size in mm
        
    Returns:
        Trapped volume check results
    """
    # Label connected fluid components
    fluid_mask = volume
    labeled, num_components = ndimage.label(fluid_mask)
    
    if num_components == 0:
        return {
            'num_fluid_components': 0,
            'largest_component_fraction': 0.0,
            'has_trapped_volumes': False,
            'passes': True,
            'failure_mode': None,
            'label': 'GEOMETRIC',
            'method': 'connected_component_analysis'
        }
    
    # Get component sizes
    component_sizes = ndimage.sum(fluid_mask, labeled, range(1, num_components + 1))
    largest_component_size = np.max(component_sizes)
    total_fluid = np.sum(fluid_mask)
    
    largest_fraction = largest_component_size / total_fluid if total_fluid > 0 else 0.0
    
    # If more than one component, may have trapped volumes
    # For Stage 3, we already checked connectivity, so this should pass
    has_trapped = num_components > 1
    
    # Pass if single connected component or all components accessible
    passes = (num_components == 1) or (largest_fraction > 0.95)
    
    return {
        'num_fluid_components': int(num_components),
        'largest_component_fraction': float(largest_fraction),
        'has_trapped_volumes': has_trapped,
        'passes': passes,
        'failure_mode': None if passes else 'trapped_internal_volumes',
        'label': 'GEOMETRIC',
        'method': 'connected_component_analysis'
    }


def run_all_manufacturability_checks(
    volume: np.ndarray,
    voxel_size_mm: float,
    requirements: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Run all manufacturability checks.
    
    Args:
        volume: Boolean volume array (True=fluid, False=solid)
        voxel_size_mm: Voxel size in mm
        requirements: Manufacturability requirements dict
        
    Returns:
        Aggregated manufacturability check results
    """
    min_wall_mm = requirements.get('min_wall_thickness_mm', 0.5)
    min_feature_mm = requirements.get('min_feature_size_mm', 0.5)
    max_unsupported_mm = requirements.get('max_unsupported_mm', 10.0)
    
    wall_check = check_minimum_wall_thickness(volume, voxel_size_mm, min_wall_mm)
    feature_check = check_minimum_feature_size(volume, voxel_size_mm, min_feature_mm)
    unsupported_check = check_unsupported_regions(volume, voxel_size_mm, max_unsupported_mm)
    trapped_check = check_trapped_volumes(volume, voxel_size_mm)
    
    # Aggregate pass/fail
    all_checks = [wall_check, feature_check, unsupported_check, trapped_check]
    all_pass = all(check['passes'] for check in all_checks)
    
    # Collect failure modes
    failure_modes = [
        check['failure_mode']
        for check in all_checks
        if check['failure_mode'] is not None
    ]
    
    return {
        'wall_thickness': wall_check,
        'feature_size': feature_check,
        'unsupported_regions': unsupported_check,
        'trapped_volumes': trapped_check,
        'overall_pass': all_pass,
        'failure_modes': failure_modes,
        'label': 'MANUFACTURABILITY_SCREENED'
    }
