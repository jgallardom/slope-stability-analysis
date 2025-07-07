"""
Slice Properties Calculator
-------------------------
Computes geometric properties of a single slice in the method of slices.
"""

import numpy as np
from .geometry import calculate_ground_surface

def compute_slice_properties(x, center, radius, height, slope_angle, dx):
    """Compute geometric properties of a single slice.
    
    Args:
        x: x-coordinate of slice center
        center: (x,y) coordinates of circle center
        radius: radius of failure circle
        height: slope height
        slope_angle: slope angle in degrees
        dx: slice width
    
    Returns:
        Dictionary containing slice properties including:
        - height: vertical height of slice
        - theta: angle between vertical and radius (radians)
        - base_length: actual length of slice base
        - area: slice area 
        - arm_length: perpendicular distance from weight line to center
    """
    # Check if x is within circle bounds
    discriminant = radius**2 - (x - center[0])**2
    if discriminant < 0:
        return None
        
    # Calculate slice boundaries
    y_circle = center[1] - np.sqrt(discriminant)
    y_ground = calculate_ground_surface(x, height, slope_angle)
    
    if y_circle > y_ground:
        return None

    dx_from_center = x - center[0]
    dy_from_center = y_circle - center[1]
    theta = np.arctan2(dx_from_center, -dy_from_center)  
    
    # Calculate base endpoints
    dx_half = dx/2
    base_left_x = x - dx_half
    base_right_x = x + dx_half
    
    # Get y-coordinates of base endpoints using circle equation
    disc_left = radius**2 - (base_left_x - center[0])**2
    disc_right = radius**2 - (base_right_x - center[0])**2
    
    if disc_left < 0 or disc_right < 0:
        return None
        
    base_left_y = center[1] - np.sqrt(disc_left)
    base_right_y = center[1] - np.sqrt(disc_right)
    
    # Calculate actual base length using endpoints
    base_length = np.sqrt((base_right_x - base_left_x)**2 + 
                         (base_right_y - base_left_y)**2)
    
    # Calculate slice height and area
    slice_height = y_ground - y_circle
    
    # Calculate perpendicular distance from weight line to center (moment arm)
    arm_length = x - center[0]  # Horizontal distance from center to weight line
    
    return {
        'height': slice_height,
        'theta': theta,  # Angle from vertical to radius
        'base_length': base_length,
        'area': slice_height * dx,
        'arm_length': arm_length
    } 