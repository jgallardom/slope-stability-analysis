"""
Core stability calculation module.
Contains all the mathematical computations for slope stability analysis.
"""

import numpy as np

def calculate_ground_surface(x, height, slope_angle):
    """Calculate ground surface y-coordinate at given x."""
    slope_rad = np.radians(slope_angle)
    x_slope = height / np.tan(slope_rad)
    
    if x <= 0:
        return height
    elif x <= x_slope:
        return height - x * np.tan(slope_rad)
    else:
        return 0

def compute_slice_properties(x, center, radius, height, slope_angle, dx):
    """Compute geometric properties of a slice."""
    discriminant = radius**2 - (x - center[0])**2
    if discriminant < 0:
        return None
        
    y_circle = center[1] - np.sqrt(discriminant)
    y_ground = calculate_ground_surface(x, height, slope_angle)
    
    if y_circle > y_ground:
        return None
        
    slice_height = y_ground - y_circle
    alpha = np.arctan2(center[1] - y_circle, center[0] - x)
    
    return slice_height, alpha, dx

def compute_fos(center, radius, c, phi, gamma, slope_angle, height, slices=30):
    """Calculate Factor of Safety using Method of Slices."""
    phi_rad = np.radians(phi)
    dx = 2 * radius / slices
    sum_moments = sum_weights = 0
    
    for x in np.arange(center[0] - radius, center[0] + radius, dx):
        slice_props = compute_slice_properties(x, center, radius, height, slope_angle, dx)
        if not slice_props:
            continue
            
        slice_height, alpha, dx = slice_props
        weight = gamma * slice_height * dx
        
        sum_moments += (c * dx / np.sin(alpha) + weight * np.sin(alpha) * np.tan(phi_rad))
        sum_weights += weight * np.cos(alpha)
    
    return np.inf if sum_weights == 0 else sum_moments / sum_weights

def find_critical_circle(params):
    """Find the critical failure circle with minimum Factor of Safety."""
    height = params['height']
    slope_angle = params['slopeAngle']
    x_slope = height / np.tan(np.radians(slope_angle))
    
    # Search grid parameters
    x_range = np.linspace(-height/2, x_slope + height/2, 20)
    y_range = np.linspace(height/2, height*2, 20)
    r_range = np.linspace(height/2, height*2, 10)
    
    min_fos = np.inf
    result = None
    
    for x, y, radius in [(x, y, r) for x in x_range for y in y_range for r in r_range]:
        try:
            fos = compute_fos((x, y), radius, params['cohesion'], params['friction'],
                            params['unitWeight'], slope_angle, height)
            if 0 < fos < min_fos:
                min_fos = fos
                result = ((x, y), radius, fos)
        except:
            continue
    
    if not result:
        raise ValueError("Could not find a valid failure surface. Check input parameters.")
    return result 