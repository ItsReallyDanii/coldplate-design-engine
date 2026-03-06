"""
Configuration constants for Stage 3 geometry generation.

Centralized parameters for voxel resolution and physical sizing.
Updated 2026-03-06 for manufacturability remediation.
"""

# Voxel discretization parameters
# REMEDIATION v1: Changed from 0.1mm to 0.25mm to achieve 0.5mm minimum features
# Rationale: min_feature_mm = 2 voxels × voxel_size_mm
#            0.5mm = 2 × 0.25mm ✓
VOXEL_SIZE_MM = 0.25  # Physical size of each voxel (mm)

# Resolution settings for different run modes
# Smoke test: Fast screening with minimal candidates
SMOKE_RESOLUTION = 20  # Grid resolution (nx=ny=nz) for smoke tests
SMOKE_DOMAIN_MM = SMOKE_RESOLUTION * VOXEL_SIZE_MM  # 20 × 0.25mm = 5.0mm

# Full run: Higher resolution for production candidates
DEFAULT_RESOLUTION = 40  # Grid resolution for full runs
DEFAULT_DOMAIN_MM = DEFAULT_RESOLUTION * VOXEL_SIZE_MM  # 40 × 0.25mm = 10.0mm

# Physical height (Z-direction)
DEFAULT_HEIGHT_MM = 2.0  # Coldplate thickness (mm)

# Feature size expectations
# These are DERIVED from voxel size, not independently configurable
EXPECTED_MIN_FEATURE_MM = 2 * VOXEL_SIZE_MM  # 2 voxels minimum = 0.5mm
EXPECTED_MIN_WALL_MM = 2 * VOXEL_SIZE_MM     # 2 voxels minimum = 0.5mm

# Validation thresholds
# Match Stage 6 manufacturability requirements
MIN_FEATURE_SIZE_MM = 0.5  # Minimum acceptable feature (channel) size
MIN_WALL_THICKNESS_MM = 0.5  # Minimum acceptable wall thickness

# Remediation history
REMEDIATION_VERSION = "v1"
REMEDIATION_REASON = "manufacturability_feature_size"
PRIOR_VOXEL_SIZE_MM = 0.1  # Previous value (failed 0.5mm requirement)
PRIOR_SMOKE_RESOLUTION = 50  # Previous smoke test resolution


def get_smoke_config():
    """Get smoke test configuration dictionary."""
    return {
        'resolution': SMOKE_RESOLUTION,
        'voxel_size_mm': VOXEL_SIZE_MM,
        'height_mm': DEFAULT_HEIGHT_MM,
        'domain_mm': SMOKE_DOMAIN_MM,
        'expected_min_feature_mm': EXPECTED_MIN_FEATURE_MM,
    }


def get_full_config():
    """Get full run configuration dictionary."""
    return {
        'resolution': DEFAULT_RESOLUTION,
        'voxel_size_mm': VOXEL_SIZE_MM,
        'height_mm': DEFAULT_HEIGHT_MM,
        'domain_mm': DEFAULT_DOMAIN_MM,
        'expected_min_feature_mm': EXPECTED_MIN_FEATURE_MM,
    }


def get_remediation_info():
    """Get remediation provenance information."""
    return {
        'version': REMEDIATION_VERSION,
        'reason': REMEDIATION_REASON,
        'prior_voxel_size_mm': PRIOR_VOXEL_SIZE_MM,
        'prior_smoke_resolution': PRIOR_SMOKE_RESOLUTION,
        'new_voxel_size_mm': VOXEL_SIZE_MM,
        'new_smoke_resolution': SMOKE_RESOLUTION,
        'expected_min_feature_mm': EXPECTED_MIN_FEATURE_MM,
    }


def validate_configuration():
    """
    Validate that configuration meets manufacturability requirements.
    
    Returns:
        Tuple of (is_valid, messages)
    """
    messages = []
    is_valid = True
    
    # Check minimum feature size achievable
    achievable_min_mm = 2 * VOXEL_SIZE_MM
    if achievable_min_mm < MIN_FEATURE_SIZE_MM:
        messages.append(
            f"WARNING: Achievable min feature ({achievable_min_mm:.3f}mm) "
            f"< required ({MIN_FEATURE_SIZE_MM}mm)"
        )
        is_valid = False
    elif achievable_min_mm == MIN_FEATURE_SIZE_MM:
        messages.append(
            f"OK: Achievable min feature ({achievable_min_mm:.3f}mm) "
            f"= required ({MIN_FEATURE_SIZE_MM}mm) (exactly at limit)"
        )
    else:
        messages.append(
            f"OK: Achievable min feature ({achievable_min_mm:.3f}mm) "
            f"> required ({MIN_FEATURE_SIZE_MM}mm) "
            f"(margin: {achievable_min_mm - MIN_FEATURE_SIZE_MM:.3f}mm)"
        )
    
    # Check domain size reasonable
    if SMOKE_DOMAIN_MM < 1.0:
        messages.append(f"WARNING: Smoke domain too small ({SMOKE_DOMAIN_MM:.1f}mm)")
        is_valid = False
    elif SMOKE_DOMAIN_MM > 20.0:
        messages.append(f"WARNING: Smoke domain too large ({SMOKE_DOMAIN_MM:.1f}mm)")
        is_valid = False
    else:
        messages.append(f"OK: Smoke domain size = {SMOKE_DOMAIN_MM:.1f}mm")
    
    # Check resolution not too coarse
    if SMOKE_RESOLUTION < 10:
        messages.append(f"WARNING: Resolution too coarse ({SMOKE_RESOLUTION})")
        is_valid = False
    else:
        messages.append(f"OK: Smoke resolution = {SMOKE_RESOLUTION}")
    
    return is_valid, messages


if __name__ == '__main__':
    """Configuration validation check."""
    print("=== Stage 3 Geometry Configuration ===")
    print(f"Voxel size: {VOXEL_SIZE_MM} mm")
    print(f"Smoke resolution: {SMOKE_RESOLUTION}")
    print(f"Smoke domain: {SMOKE_DOMAIN_MM:.1f} mm")
    print(f"Full resolution: {DEFAULT_RESOLUTION}")
    print(f"Full domain: {DEFAULT_DOMAIN_MM:.1f} mm")
    print(f"\nExpected min feature: {EXPECTED_MIN_FEATURE_MM} mm")
    print(f"Required min feature: {MIN_FEATURE_SIZE_MM} mm")
    
    print("\n=== Validation ===")
    is_valid, messages = validate_configuration()
    for msg in messages:
        print(f"  {msg}")
    
    if is_valid:
        print("\n✓ Configuration valid")
    else:
        print("\n✗ Configuration has warnings")
        exit(1)
