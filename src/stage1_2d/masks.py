"""Mask validation and processing utilities.

Validates binary masks for:
- Binary enforcement
- Shape consistency
- Connectivity
- Inlet/outlet conventions
"""

import numpy as np
from scipy import ndimage
from typing import Tuple, List
from .schemas import GridConfig


def validate_mask_shape(mask: np.ndarray, grid: GridConfig) -> None:
    """Validate mask has correct shape.
    
    Args:
        mask: Binary mask
        grid: Expected grid configuration
        
    Raises:
        ValueError: If shape is incorrect
    """
    expected_shape = (grid.ny, grid.nx)
    if mask.shape != expected_shape:
        raise ValueError(
            f"Mask shape {mask.shape} does not match grid {expected_shape}"
        )


def enforce_binary(mask: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """Enforce binary values in mask.
    
    Args:
        mask: Input mask (may have non-binary values)
        threshold: Threshold for binarization
        
    Returns:
        Binary mask with values 0 or 1
    """
    return (mask > threshold).astype(np.uint8)


def check_connectivity(
    mask: np.ndarray,
    connectivity: int = 2
) -> Tuple[bool, int, np.ndarray]:
    """Check if fluid region is connected.
    
    Args:
        mask: Binary mask (1 = fluid)
        connectivity: Connectivity type (1=4-neighbor, 2=8-neighbor)
        
    Returns:
        Tuple of (is_fully_connected, num_components, labeled_array)
    """
    # Label connected components in fluid region
    labeled, num_components = ndimage.label(mask, structure=ndimage.generate_binary_structure(2, connectivity))
    
    is_fully_connected = (num_components == 1) if mask.sum() > 0 else False
    
    return is_fully_connected, num_components, labeled


def compute_porosity(mask: np.ndarray) -> float:
    """Compute porosity (open-area fraction).
    
    Args:
        mask: Binary mask (1 = fluid)
        
    Returns:
        Porosity (0 to 1)
    """
    return mask.mean()


def compute_dead_zone_fraction(
    mask: np.ndarray,
    inlet_side: str = "left",
    outlet_side: str = "right"
) -> float:
    """Compute dead zone fraction (disconnected from inlet-outlet path).
    
    Args:
        mask: Binary mask (1 = fluid)
        inlet_side: Inlet side ("left", "right", "top", "bottom")
        outlet_side: Outlet side
        
    Returns:
        Dead zone fraction (0 to 1)
    """
    # Find connected region from inlet
    inlet_mask = np.zeros_like(mask)
    
    if inlet_side == "left":
        inlet_mask[:, 0] = mask[:, 0]
    elif inlet_side == "right":
        inlet_mask[:, -1] = mask[:, -1]
    elif inlet_side == "top":
        inlet_mask[0, :] = mask[0, :]
    elif inlet_side == "bottom":
        inlet_mask[-1, :] = mask[-1, :]
    
    # Flood fill from inlet
    structure = ndimage.generate_binary_structure(2, 2)  # 8-connectivity
    flooded = ndimage.binary_dilation(inlet_mask, structure=structure, mask=mask, iterations=-1)
    
    # Check if reaches outlet
    reaches_outlet = False
    if outlet_side == "left":
        reaches_outlet = flooded[:, 0].any()
    elif outlet_side == "right":
        reaches_outlet = flooded[:, -1].any()
    elif outlet_side == "top":
        reaches_outlet = flooded[0, :].any()
    elif outlet_side == "bottom":
        reaches_outlet = flooded[-1, :].any()
    
    if not reaches_outlet:
        # No connection from inlet to outlet
        return 1.0
    
    # Dead zones are fluid regions not in flooded area
    dead_zones = mask & (~flooded)
    
    if mask.sum() == 0:
        return 0.0
    
    return dead_zones.sum() / mask.sum()


def find_minimum_feature_size(mask: np.ndarray, is_fluid: bool = True) -> int:
    """Find minimum feature size (approximate).
    
    Uses distance transform to estimate minimum feature width.
    
    Args:
        mask: Binary mask
        is_fluid: If True, measure fluid features; if False, measure solid features
        
    Returns:
        Minimum feature size in pixels (approximate)
    """
    target_mask = mask if is_fluid else (1 - mask)
    
    if target_mask.sum() == 0:
        return 0
    
    # Distance transform gives distance to nearest boundary
    dist = ndimage.distance_transform_edt(target_mask)
    
    # Minimum feature size is approximately 2 * min(distance_to_boundary)
    # where min is taken over all non-zero regions
    min_feature = 2 * dist[target_mask > 0].min()
    
    return int(np.ceil(min_feature))


def compute_wetted_perimeter_proxy(mask: np.ndarray) -> float:
    """Compute wetted perimeter proxy (interface length).
    
    This is a 2D proxy based on the length of the fluid-solid interface.
    
    Args:
        mask: Binary mask (1 = fluid)
        
    Returns:
        Interface length in pixels (dimensionless proxy)
    """
    # Compute gradient magnitude at interfaces
    grad_y, grad_x = np.gradient(mask.astype(float))
    interface = np.sqrt(grad_x**2 + grad_y**2)
    
    # Sum interface length
    return interface.sum()


def check_solid_continuity(mask: np.ndarray) -> Tuple[bool, int]:
    """Check if solid region is continuous.
    
    Args:
        mask: Binary mask (1 = fluid, 0 = solid)
        
    Returns:
        Tuple of (is_continuous, num_disconnected_islands)
    """
    solid_mask = 1 - mask
    
    if solid_mask.sum() == 0:
        return True, 0
    
    # Label connected components in solid region
    labeled, num_components = ndimage.label(solid_mask)
    
    # Continuous if only one component
    is_continuous = (num_components == 1)
    
    return is_continuous, num_components


def validate_inlet_outlet_convention(
    mask: np.ndarray,
    inlet_side: str = "left",
    outlet_side: str = "right",
    min_open_fraction: float = 0.1
) -> Tuple[bool, List[str]]:
    """Validate inlet/outlet convention.
    
    Args:
        mask: Binary mask (1 = fluid)
        inlet_side: Expected inlet side
        outlet_side: Expected outlet side
        min_open_fraction: Minimum open fraction required at inlet/outlet
        
    Returns:
        Tuple of (is_valid, list_of_warnings)
    """
    warnings = []
    
    # Check inlet
    if inlet_side == "left":
        inlet_open = mask[:, 0].mean()
    elif inlet_side == "right":
        inlet_open = mask[:, -1].mean()
    elif inlet_side == "top":
        inlet_open = mask[0, :].mean()
    elif inlet_side == "bottom":
        inlet_open = mask[-1, :].mean()
    else:
        warnings.append(f"Unknown inlet side: {inlet_side}")
        return False, warnings
    
    if inlet_open < min_open_fraction:
        warnings.append(
            f"Inlet open fraction {inlet_open:.3f} < minimum {min_open_fraction}"
        )
    
    # Check outlet
    if outlet_side == "left":
        outlet_open = mask[:, 0].mean()
    elif outlet_side == "right":
        outlet_open = mask[:, -1].mean()
    elif outlet_side == "top":
        outlet_open = mask[0, :].mean()
    elif outlet_side == "bottom":
        outlet_open = mask[-1, :].mean()
    else:
        warnings.append(f"Unknown outlet side: {outlet_side}")
        return False, warnings
    
    if outlet_open < min_open_fraction:
        warnings.append(
            f"Outlet open fraction {outlet_open:.3f} < minimum {min_open_fraction}"
        )
    
    is_valid = len(warnings) == 0
    
    return is_valid, warnings


def load_and_validate_mask(
    mask: np.ndarray,
    grid: GridConfig,
    enforce_binary_threshold: float = 0.5,
    check_connectivity_flag: bool = True,
    inlet_side: str = "left",
    outlet_side: str = "right"
) -> Tuple[np.ndarray, List[str]]:
    """Load and validate a mask with all checks.
    
    Args:
        mask: Input mask
        grid: Grid configuration
        enforce_binary_threshold: Threshold for binary enforcement
        check_connectivity_flag: Whether to check connectivity
        inlet_side: Inlet side
        outlet_side: Outlet side
        
    Returns:
        Tuple of (validated_mask, list_of_warnings)
        
    Raises:
        ValueError: If critical validation fails
    """
    warnings = []
    
    # Validate shape
    validate_mask_shape(mask, grid)
    
    # Enforce binary
    validated_mask = enforce_binary(mask, enforce_binary_threshold)
    
    # Check connectivity
    if check_connectivity_flag:
        is_connected, num_components, _ = check_connectivity(validated_mask)
        if not is_connected:
            warnings.append(
                f"Fluid region has {num_components} disconnected components"
            )
    
    # Check inlet/outlet convention
    io_valid, io_warnings = validate_inlet_outlet_convention(
        validated_mask, inlet_side, outlet_side
    )
    warnings.extend(io_warnings)
    
    # Check for dead zones
    dead_zone_frac = compute_dead_zone_fraction(validated_mask, inlet_side, outlet_side)
    if dead_zone_frac > 0.1:
        warnings.append(f"High dead zone fraction: {dead_zone_frac:.3f}")
    
    return validated_mask, warnings
