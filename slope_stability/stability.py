"""
Stability Analysis Module
-----------------------
Core stability calculations using the Method of Slices.
"""

import numpy as np
from . import compute_slice_properties, calculate_slice_forces

def compute_safety_factor(center, radius, params, num_slices=30):
    """Calculate Factor of Safety for a given failure surface."""
    # Unpack parameters
    height = params['height']
    slope_angle = params['slope_angle']
    cohesion = params['cohesion']
    friction = params['friction']
    unit_weight = params['unit_weight']
    
    # Initialize slice width and sums
    dx = 2 * radius / num_slices
    resisting_moment = driving_moment = 0
    
    # Analyze each slice
    for x in np.arange(center[0] - radius, center[0] + radius, dx):
        # Get slice geometry
        slice_data = compute_slice_properties(x, center, radius, height, slope_angle, dx)
        if not slice_data:
            continue
        
        # Calculate forces
        forces = calculate_slice_forces(slice_data, unit_weight, cohesion, friction)
        if not forces:
            continue
        
        # Add moments using correct keys returned by calculate_slice_forces
        resisting_moment += forces['resisting_force']*radius
        driving_moment += forces['weight']*slice_data['arm_length']

    # Return Factor of Safety
    return np.inf if driving_moment == 0 else -resisting_moment / driving_moment

def create_default_groups(params):
    """Generate a coarse grid of (x, y, r) values suitable for batch FoS runs.

    The grid is similar to the one used in ``find_critical_surface`` but
    returned as an explicit list rather than performing an internal search.
    """
    height = params['height']
    slope_angle = params['slope_angle']
    num_x = 10
    num_y = 10
    num_r = 5

    x_slope = height / np.tan(np.radians(slope_angle))
    x_vals = np.linspace(-height / 2, x_slope + height / 2, num_x)
    y_vals = np.linspace(height / 2, height * 2, num_y)
    r_vals = np.linspace(height / 2, height * 2, num_r)

    groups = []
    for x in x_vals:
        for y in y_vals:
            for r in r_vals:
                groups.append((x, y, r))
    return groups 

