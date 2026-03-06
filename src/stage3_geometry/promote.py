"""2D to 3D geometry promotion.

Maps Stage 2 2D proxy families to true 3D parametric geometry.
"""

import numpy as np
from typing import Tuple, Dict, Any, Optional
from . import channels3d, tpms3d


def promote_candidate_to_3d(
    candidate: Dict[str, Any],
    height_mm: float = 2.0,
    resolution: int = 100,
    grid_config: Optional[Dict[str, Any]] = None
) -> Tuple[Optional[np.ndarray], Optional[Dict[str, Any]], Optional[str]]:
    """Promote a Stage 2 candidate to 3D geometry.
    
    Args:
        candidate: Candidate dict from Stage 2 with family and params
        height_mm: Height of 3D geometry in mm
        resolution: Grid resolution for 3D volume
        grid_config: Optional grid configuration
        
    Returns:
        Tuple of (volume, metadata, error_message)
        volume is None if promotion fails
    """
    family = candidate['family']
    params = candidate['params']
    
    if grid_config is None:
        grid_config = {'nx': 100, 'ny': 100, 'dx': 0.0001, 'dy': 0.0001}
    
    try:
        if family == 'straight_channel':
            volume, metadata = channels3d.generate_straight_channel_3d(
                params, grid_config, height_mm, resolution
            )
        elif family == 'serpentine_channel':
            volume, metadata = channels3d.generate_serpentine_channel_3d(
                params, grid_config, height_mm, resolution
            )
        elif family == 'pin_fin':
            volume, metadata = channels3d.generate_pin_fin_3d(
                params, grid_config, height_mm, resolution
            )
        elif family == 'gyroid_2d':
            # Promote 2D proxy to true 3D gyroid TPMS
            volume, metadata = tpms3d.generate_gyroid_3d(
                params, grid_config, height_mm, resolution
            )
        elif family == 'diamond_2d':
            # Promote 2D proxy to true 3D diamond TPMS
            volume, metadata = tpms3d.generate_diamond_3d(
                params, grid_config, height_mm, resolution
            )
        elif family == 'primitive_2d':
            # Promote 2D proxy to true 3D primitive TPMS
            volume, metadata = tpms3d.generate_primitive_3d(
                params, grid_config, height_mm, resolution
            )
        else:
            return None, None, f"Unsupported family: {family}"
        
        # Add candidate provenance to metadata
        metadata['candidate_rank'] = candidate['rank']
        metadata['candidate_seed'] = candidate['seed']
        metadata['candidate_family'] = candidate['family']
        metadata['candidate_score'] = candidate['total_score']
        metadata['stage2_params'] = params
        
        return volume, metadata, None
        
    except Exception as e:
        return None, None, f"Promotion failed: {str(e)}"


def get_family_promotion_status() -> Dict[str, Dict[str, Any]]:
    """Get status of 3D promotion capability for each family.
    
    Returns:
        Dictionary mapping family name to promotion status
    """
    return {
        'straight_channel': {
            'supported': True,
            'method': 'extruded_3d',
            'description': 'Straight channels extruded in Z direction'
        },
        'serpentine_channel': {
            'supported': True,
            'method': 'extruded_3d',
            'description': 'Serpentine channels extruded in Z direction'
        },
        'pin_fin': {
            'supported': True,
            'method': '3d_cylindrical_array',
            'description': 'Cylindrical pin-fin obstacles in regular array'
        },
        'gyroid_2d': {
            'supported': True,
            'method': '3d_implicit_tpms',
            'description': 'True 3D gyroid TPMS from implicit surface equation'
        },
        'diamond_2d': {
            'supported': True,
            'method': '3d_implicit_tpms',
            'description': 'True 3D diamond (Schwarz-D) TPMS from implicit surface equation'
        },
        'primitive_2d': {
            'supported': True,
            'method': '3d_implicit_tpms',
            'description': 'True 3D primitive (Schwarz-P) TPMS from implicit surface equation'
        },
    }
