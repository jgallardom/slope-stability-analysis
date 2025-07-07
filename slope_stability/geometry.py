"""
Slope Geometry Module
--------------------
Handles basic geometric calculations for slope stability analysis.
"""

import numpy as np
def calculate_ground_surface(x, height, slope_angle):
    """Calculate y-coordinate of ground surface at point x."""
    slope_rad = np.radians(slope_angle)
    x_slope = height / np.tan(slope_rad)
    
    if x <= 0:
        return height
    elif x <= x_slope:
        return height - x * np.tan(slope_rad)
    else:
        return 0

