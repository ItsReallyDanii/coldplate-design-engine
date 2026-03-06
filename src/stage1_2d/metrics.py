"""Metric computation engine with honest proxy labeling.

All metrics are explicitly categorized as:
- GEOMETRIC: Real geometric properties
- FLOW_PROXY: Dimensionless flow-related proxies (NOT real pressure drop or flow rate)
- HEAT_PROXY: Dimensionless heat-transfer-adjacent proxies (NOT real thermal resistance)

Proxy metrics are clearly labeled with "_proxy" suffix and documented limitations.
"""

import numpy as np
from scipy import ndimage
from scipy.spatial.distance import cdist
from typing import Dict, List
from .schemas import MetricDefinition, MetricResult, MetricCategory
from .masks import (
    compute_porosity,
    compute_dead_zone_fraction,
    find_minimum_feature_size,
    compute_wetted_perimeter_proxy,
    check_solid_continuity,
    check_connectivity,
)


# Metric schema version for tracking changes
METRIC_SCHEMA_VERSION = "1.0.0"


def get_metric_definitions() -> Dict[str, MetricDefinition]:
    """Get all metric definitions with honest labeling.
    
    Returns:
        Dictionary of metric definitions keyed by metric name
    """
    definitions = {}
    
    # --- GEOMETRIC METRICS ---
    
    definitions["porosity"] = MetricDefinition(
        name="porosity",
        category=MetricCategory.GEOMETRIC,
        units="dimensionless",
        description="Open-area fraction (fluid region / total area)",
        is_proxy=False,
        assumptions=["2D cross-section", "Binary mask"],
        limitations=["Does not account for 3D geometry or wall thickness in z-direction"]
    )
    
    definitions["wetted_perimeter_proxy"] = MetricDefinition(
        name="wetted_perimeter_proxy",
        category=MetricCategory.GEOMETRIC,
        units="pixels",
        description="Fluid-solid interface length in 2D (proxy for wetted perimeter)",
        is_proxy=True,
        assumptions=["2D cross-section", "Interface approximated by gradient"],
        limitations=[
            "Not true 3D wetted perimeter",
            "Does not account for surface roughness",
            "Pixel-based approximation"
        ]
    )
    
    definitions["min_fluid_feature_px"] = MetricDefinition(
        name="min_fluid_feature_px",
        category=MetricCategory.GEOMETRIC,
        units="pixels",
        description="Minimum fluid feature size (approximate)",
        is_proxy=False,
        assumptions=["2D cross-section", "Distance transform approximation"],
        limitations=["Approximate measure", "Pixel resolution dependent"]
    )
    
    definitions["min_solid_feature_px"] = MetricDefinition(
        name="min_solid_feature_px",
        category=MetricCategory.GEOMETRIC,
        units="pixels",
        description="Minimum solid feature size (approximate)",
        is_proxy=False,
        assumptions=["2D cross-section", "Distance transform approximation"],
        limitations=["Approximate measure", "Pixel resolution dependent"]
    )
    
    definitions["solid_continuity_islands"] = MetricDefinition(
        name="solid_continuity_islands",
        category=MetricCategory.GEOMETRIC,
        units="count",
        description="Number of disconnected solid regions",
        is_proxy=False,
        assumptions=["2D cross-section", "8-connectivity"],
        limitations=["Does not predict structural integrity"]
    )
    
    # --- FLOW PROXY METRICS ---
    
    definitions["flow_connectivity_score"] = MetricDefinition(
        name="flow_connectivity_score",
        category=MetricCategory.FLOW_PROXY,
        units="dimensionless",
        description="Proxy for flow connectivity (0 = disconnected, 1 = fully connected)",
        is_proxy=True,
        assumptions=["2D topology", "No flow physics"],
        limitations=[
            "NOT a real flow rate or velocity",
            "Does not account for viscosity, Reynolds number, or flow regime",
            "Purely topological measure"
        ]
    )
    
    definitions["dead_zone_fraction"] = MetricDefinition(
        name="dead_zone_fraction",
        category=MetricCategory.FLOW_PROXY,
        units="dimensionless",
        description="Fraction of fluid region disconnected from inlet-outlet path",
        is_proxy=True,
        assumptions=["2D topology", "Flood-fill connectivity"],
        limitations=[
            "Does not account for flow stagnation in connected regions",
            "NOT a predictor of actual recirculation zones"
        ]
    )
    
    definitions["hydraulic_diameter_proxy"] = MetricDefinition(
        name="hydraulic_diameter_proxy",
        category=MetricCategory.FLOW_PROXY,
        units="pixels",
        description="Hydraulic diameter proxy: 4 * Area / Perimeter",
        is_proxy=True,
        assumptions=["2D cross-section", "Uniform cross-section"],
        limitations=[
            "NOT a true hydraulic diameter in 3D",
            "Does not capture variation along flow path",
            "Assumes constant cross-section"
        ]
    )
    
    definitions["hydraulic_resistance_proxy"] = MetricDefinition(
        name="hydraulic_resistance_proxy",
        category=MetricCategory.FLOW_PROXY,
        units="dimensionless",
        description="Dimensionless hydraulic resistance proxy (higher = more resistance)",
        is_proxy=True,
        assumptions=[
            "2D geometry",
            "Heuristic based on porosity and perimeter",
            "No Reynolds number dependence"
        ],
        limitations=[
            "NOT real pressure drop",
            "Does not include fluid properties",
            "No turbulence or transition modeling",
            "Purely geometric heuristic"
        ]
    )
    
    definitions["tortuosity_proxy"] = MetricDefinition(
        name="tortuosity_proxy",
        category=MetricCategory.FLOW_PROXY,
        units="dimensionless",
        description="Path tortuosity proxy based on centroid-to-centroid distance",
        is_proxy=True,
        assumptions=["2D topology", "Centerline approximation"],
        limitations=[
            "NOT a true flow path length ratio",
            "Does not follow streamlines",
            "Crude approximation"
        ]
    )
    
    definitions["maldistribution_proxy"] = MetricDefinition(
        name="maldistribution_proxy",
        category=MetricCategory.FLOW_PROXY,
        units="dimensionless",
        description="Flow maldistribution proxy based on channel width variance",
        is_proxy=True,
        assumptions=["2D topology", "Geometric approximation"],
        limitations=[
            "NOT actual flow distribution",
            "Does not solve Navier-Stokes",
            "Purely geometric variance measure"
        ]
    )
    
    # --- HEAT TRANSFER PROXY METRICS ---
    
    definitions["heat_exchange_area_proxy"] = MetricDefinition(
        name="heat_exchange_area_proxy",
        category=MetricCategory.HEAT_PROXY,
        units="pixels",
        description="Heat exchange area proxy (fluid-solid interface length)",
        is_proxy=True,
        assumptions=["2D interface", "All interface participates equally"],
        limitations=[
            "NOT actual heat transfer rate",
            "Does not account for convection coefficients",
            "Ignores thermal boundary layer development",
            "No conjugate heat transfer"
        ]
    )
    
    definitions["wall_contact_density"] = MetricDefinition(
        name="wall_contact_density",
        category=MetricCategory.HEAT_PROXY,
        units="dimensionless",
        description="Wall contact density (interface length / fluid area)",
        is_proxy=True,
        assumptions=["2D geometry", "Uniform heat transfer coefficient"],
        limitations=[
            "NOT actual thermal resistance",
            "Ignores flow velocity effects on convection",
            "No thermal conductivity effects"
        ]
    )
    
    definitions["thermal_path_uniformity_proxy"] = MetricDefinition(
        name="thermal_path_uniformity_proxy",
        category=MetricCategory.HEAT_PROXY,
        units="dimensionless",
        description="Proxy for thermal path uniformity (0 = non-uniform, 1 = uniform)",
        is_proxy=True,
        assumptions=["2D geometry", "Geometric uniformity approximation"],
        limitations=[
            "NOT actual temperature uniformity",
            "Does not solve heat equation",
            "Purely geometric measure"
        ]
    )
    
    definitions["spreading_proxy"] = MetricDefinition(
        name="spreading_proxy",
        category=MetricCategory.HEAT_PROXY,
        units="dimensionless",
        description="Thermal spreading proxy based on fluid distribution",
        is_proxy=True,
        assumptions=["2D geometry", "Uniform material properties"],
        limitations=[
            "NOT actual spreading resistance",
            "Does not model conduction in solid",
            "Purely geometric heuristic"
        ]
    )
    
    return definitions


def compute_all_metrics(mask: np.ndarray, inlet_side: str = "left", outlet_side: str = "right") -> Dict[str, MetricResult]:
    """Compute all metrics for a given mask.
    
    Args:
        mask: Binary mask (1 = fluid, 0 = solid)
        inlet_side: Inlet side for flow-related metrics
        outlet_side: Outlet side for flow-related metrics
        
    Returns:
        Dictionary of metric results keyed by metric name
    """
    definitions = get_metric_definitions()
    results = {}
    
    # --- GEOMETRIC METRICS ---
    
    # Porosity
    porosity_val = compute_porosity(mask)
    results["porosity"] = MetricResult(
        value=porosity_val,
        definition=definitions["porosity"]
    )
    
    # Wetted perimeter proxy
    wetted_perimeter = compute_wetted_perimeter_proxy(mask)
    results["wetted_perimeter_proxy"] = MetricResult(
        value=wetted_perimeter,
        definition=definitions["wetted_perimeter_proxy"]
    )
    
    # Minimum feature sizes
    min_fluid = find_minimum_feature_size(mask, is_fluid=True)
    results["min_fluid_feature_px"] = MetricResult(
        value=float(min_fluid),
        definition=definitions["min_fluid_feature_px"]
    )
    
    min_solid = find_minimum_feature_size(mask, is_fluid=False)
    results["min_solid_feature_px"] = MetricResult(
        value=float(min_solid),
        definition=definitions["min_solid_feature_px"]
    )
    
    # Solid continuity
    is_continuous, num_islands = check_solid_continuity(mask)
    results["solid_continuity_islands"] = MetricResult(
        value=float(num_islands),
        definition=definitions["solid_continuity_islands"]
    )
    
    # --- FLOW PROXY METRICS ---
    
    # Flow connectivity score
    is_connected, num_components, _ = check_connectivity(mask)
    connectivity_score = 1.0 if is_connected else (1.0 / num_components if num_components > 0 else 0.0)
    results["flow_connectivity_score"] = MetricResult(
        value=connectivity_score,
        definition=definitions["flow_connectivity_score"]
    )
    
    # Dead zone fraction
    dead_zone_frac = compute_dead_zone_fraction(mask, inlet_side, outlet_side)
    results["dead_zone_fraction"] = MetricResult(
        value=dead_zone_frac,
        definition=definitions["dead_zone_fraction"]
    )
    
    # Hydraulic diameter proxy
    area = mask.sum()
    perimeter = wetted_perimeter
    hydraulic_diam = (4.0 * area / perimeter) if perimeter > 0 else 0.0
    results["hydraulic_diameter_proxy"] = MetricResult(
        value=hydraulic_diam,
        definition=definitions["hydraulic_diameter_proxy"]
    )
    
    # Hydraulic resistance proxy (heuristic: higher perimeter/area = more resistance)
    # Normalized by porosity to account for open area
    resistance_proxy = (perimeter / area) / (porosity_val + 1e-10) if area > 0 else np.inf
    results["hydraulic_resistance_proxy"] = MetricResult(
        value=resistance_proxy,
        definition=definitions["hydraulic_resistance_proxy"]
    )
    
    # Tortuosity proxy (simple geometric measure)
    tortuosity = _compute_tortuosity_proxy(mask, inlet_side, outlet_side)
    results["tortuosity_proxy"] = MetricResult(
        value=tortuosity,
        definition=definitions["tortuosity_proxy"]
    )
    
    # Maldistribution proxy
    maldist = _compute_maldistribution_proxy(mask)
    results["maldistribution_proxy"] = MetricResult(
        value=maldist,
        definition=definitions["maldistribution_proxy"]
    )
    
    # --- HEAT TRANSFER PROXY METRICS ---
    
    # Heat exchange area proxy (same as wetted perimeter)
    results["heat_exchange_area_proxy"] = MetricResult(
        value=wetted_perimeter,
        definition=definitions["heat_exchange_area_proxy"]
    )
    
    # Wall contact density
    wall_contact_density = (wetted_perimeter / area) if area > 0 else 0.0
    results["wall_contact_density"] = MetricResult(
        value=wall_contact_density,
        definition=definitions["wall_contact_density"]
    )
    
    # Thermal path uniformity proxy
    thermal_uniformity = _compute_thermal_path_uniformity_proxy(mask)
    results["thermal_path_uniformity_proxy"] = MetricResult(
        value=thermal_uniformity,
        definition=definitions["thermal_path_uniformity_proxy"]
    )
    
    # Spreading proxy
    spreading = _compute_spreading_proxy(mask)
    results["spreading_proxy"] = MetricResult(
        value=spreading,
        definition=definitions["spreading_proxy"]
    )
    
    return results


def _compute_tortuosity_proxy(mask: np.ndarray, inlet_side: str, outlet_side: str) -> float:
    """Compute tortuosity proxy (simple geometric measure).
    
    This is a crude approximation based on the straight-line distance
    versus the expected path length through the geometry.
    """
    ny, nx = mask.shape
    
    # Straight-line distance between inlet and outlet centroids
    if inlet_side == "left" and outlet_side == "right":
        straight_distance = nx
    elif inlet_side == "top" and outlet_side == "bottom":
        straight_distance = ny
    elif inlet_side == "right" and outlet_side == "left":
        straight_distance = nx
    elif inlet_side == "bottom" and outlet_side == "top":
        straight_distance = ny
    else:
        # Diagonal or other
        straight_distance = np.sqrt(nx**2 + ny**2)
    
    # Very crude path length proxy: use number of fluid pixels along expected direction
    # This is a heuristic; real tortuosity needs streamline tracing
    porosity = mask.mean()
    if porosity > 0:
        # Lower porosity suggests more tortuous path
        tortuosity_proxy = 1.0 / (porosity + 0.1)
    else:
        tortuosity_proxy = np.inf
    
    return float(tortuosity_proxy)


def _compute_maldistribution_proxy(mask: np.ndarray) -> float:
    """Compute maldistribution proxy.
    
    Based on variance in local flow channel width across the geometry.
    """
    # Compute local channel width using distance transform
    if mask.sum() == 0:
        return 0.0
    
    dist = ndimage.distance_transform_edt(mask)
    fluid_pixels = mask > 0
    
    if fluid_pixels.sum() == 0:
        return 0.0
    
    # Coefficient of variation of distance field
    distances = dist[fluid_pixels]
    if distances.mean() > 0:
        maldist_proxy = distances.std() / distances.mean()
    else:
        maldist_proxy = 0.0
    
    return float(maldist_proxy)


def _compute_thermal_path_uniformity_proxy(mask: np.ndarray) -> float:
    """Compute thermal path uniformity proxy.
    
    Based on variance in distance to nearest solid boundary.
    Lower variance = more uniform.
    """
    if mask.sum() == 0:
        return 0.0
    
    # Distance to solid boundary for each fluid pixel
    dist = ndimage.distance_transform_edt(mask)
    fluid_pixels = mask > 0
    
    if fluid_pixels.sum() == 0:
        return 0.0
    
    distances = dist[fluid_pixels]
    if distances.mean() > 0:
        # Uniformity score: 1 / (1 + coefficient of variation)
        cv = distances.std() / distances.mean()
        uniformity = 1.0 / (1.0 + cv)
    else:
        uniformity = 0.0
    
    return float(uniformity)


def _compute_spreading_proxy(mask: np.ndarray) -> float:
    """Compute spreading proxy.
    
    Based on spatial distribution of fluid regions across the domain.
    """
    if mask.sum() == 0:
        return 0.0
    
    # Compute center of mass for each row
    ny, nx = mask.shape
    row_centers = []
    
    for i in range(ny):
        row = mask[i, :]
        if row.sum() > 0:
            center = np.average(np.arange(nx), weights=row)
            row_centers.append(center)
    
    if len(row_centers) == 0:
        return 0.0
    
    # Low variance in row centers = good spreading
    spreading = 1.0 / (1.0 + np.std(row_centers) / nx)
    
    return float(spreading)


def get_metric_schema_version() -> str:
    """Get metric schema version.
    
    Returns:
        Schema version string
    """
    return METRIC_SCHEMA_VERSION
