"""
Core stability calculation module.
Contains all the mathematical computations for slope stability analysis.
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)

def calculate_ground_surface(x, height, slope_angle):
    """Calculate ground surface y-coordinate at given x."""
    try:
        slope_rad = np.radians(slope_angle)
        x_slope = height / np.tan(slope_rad)
        
        if x <= 0:
            return height
        elif x <= x_slope:
            return height - x * np.tan(slope_rad)
        else:
            return 0
    except Exception as e:
        logger.error(f"Error in calculate_ground_surface: {str(e)}")
        raise

def compute_slice_properties(x, center, radius, height, slope_angle, dx):
    """Compute geometric properties of a slice."""
    try:
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
    except Exception as e:
        logger.error(f"Error in compute_slice_properties: {str(e)}")
        raise

def compute_fos(center, radius, c, phi, gamma, slope_angle, height, slices=30):
    """Calculate Factor of Safety using Method of Slices."""
    try:
        phi_rad = np.radians(phi)
        dx = 2 * radius / slices
        sum_moments = sum_weights = 0
        
        for x in np.arange(center[0] - radius, center[0] + radius, dx):
            slice_props = compute_slice_properties(x, center, radius, height, slope_angle, dx)
            if not slice_props:
                continue
                
            slice_height, alpha, dx = slice_props
            weight = gamma * slice_height * dx
            
            # Check for division by zero
            if np.abs(np.sin(alpha)) < 1e-10:
                logger.warning(f"Near-zero sin(alpha) encountered at x={x}")
                continue
                
            sum_moments += (c * dx / np.sin(alpha) + weight * np.sin(alpha) * np.tan(phi_rad))
            sum_weights += weight * np.cos(alpha)
        
        if sum_weights == 0:
            logger.warning("sum_weights is zero, returning infinity")
            return np.inf
            
        fos = sum_moments / sum_weights
        logger.debug(f"Computed FOS: {fos}")
        return fos
    except Exception as e:
        logger.error(f"Error in compute_fos: {str(e)}")
        raise

def find_critical_circle(c, phi, gamma, slope_angle, height):
    """Find the critical failure circle with minimum Factor of Safety."""
    try:
        logger.debug(f"Starting critical circle search with parameters: "
                    f"c={c}, phi={phi}, gamma={gamma}, slope_angle={slope_angle}, height={height}")
        
        x_slope = height / np.tan(np.radians(slope_angle))
        min_fos = np.inf
        result = None
        
        # Search grid parameters
        x_range = np.linspace(-height/2, x_slope + height/2, 20)
        y_range = np.linspace(height/2, height*2, 20)
        r_range = np.linspace(height/2, height*2, 10)
        
        search_count = 0
        valid_circles = 0
        
        for x, y, radius in [(x, y, r) for x in x_range for y in y_range for r in r_range]:
            search_count += 1
            try:
                fos = compute_fos((x, y), radius, c, phi, gamma, slope_angle, height)
                if 0 < fos < min_fos:
                    min_fos = fos
                    result = ((x, y), radius, fos)
                    valid_circles += 1
                    logger.debug(f"Found better circle: center=({x}, {y}), radius={radius}, FOS={fos}")
            except Exception as e:
                logger.warning(f"Failed to compute FOS for circle at ({x}, {y}): {str(e)}")
                continue
        
        logger.info(f"Searched {search_count} circles, found {valid_circles} valid ones")
        
        if not result:
            raise ValueError("Could not find a valid failure surface. Check input parameters.")
            
        logger.info(f"Found critical circle: center={result[0]}, radius={result[1]}, FOS={result[2]}")
        return result
    except Exception as e:
        logger.error(f"Error in find_critical_circle: {str(e)}")
        raise 