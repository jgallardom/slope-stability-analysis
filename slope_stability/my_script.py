"""
Slope Stability Analysis using Method of Slices (Fellenius Method)
"""

import numpy as np
import math
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, Optional

def compute_fos(x_center: float, y_center: float, radius: float, 
                cohesion: float, friction_angle: float, unit_weight: float) -> float:
    """
    Compute Factor of Safety for a given slip circle.
    
    Parameters:
    -----------
    x_center, y_center : float
        Coordinates of the circle center
    radius : float
        Radius of the slip circle
    cohesion : float
        Soil cohesion in kPa
    friction_angle : float
        Soil friction angle in degrees
    unit_weight : float
        Soil unit weight in kN/m³
        
    Returns:
    --------
    float
        Factor of Safety
    """
    # Convert friction angle to radians
    phi = math.radians(friction_angle)
    
    # Initialize sums for numerator and denominator
    resisting_moment = 0
    driving_moment = 0
    
    # Define slice parameters
    slice_width = 0.5  # meters
    x_start = x_center - radius
    x_end = x_center + radius
    
    # Analyze each slice
    for x in np.arange(x_start, x_end, slice_width):
        try:
            # Find points where circle intersects with slice
            y_square = radius**2 - (x - x_center)**2
            if y_square < 0:
                continue
            y = y_center - math.sqrt(y_square)
            
            # Calculate slice properties
            height = max(0, y)
            weight = height * slice_width * unit_weight
            
            # Calculate base angle
            dx = x - x_center
            dy = y - y_center
            alpha = math.atan2(dx, abs(dy))
            
            # Calculate length of slice base
            l = slice_width / math.cos(alpha)
            
            # Sum forces
            resisting_moment += (cohesion * l + weight * math.cos(alpha) * math.tan(phi))
            driving_moment += weight * math.sin(alpha)
            
        except (ValueError, ZeroDivisionError):
            continue
    
    # Compute factor of safety
    if abs(driving_moment) < 1e-10:
        return float('inf')
    
    return resisting_moment / driving_moment

def analyze_circle(params: Tuple) -> Optional[Tuple[float, float, float, float]]:
    """Helper function for parallel processing"""
    x, y, r, height, angle, cohesion, friction_angle, unit_weight = params
    try:
        fos = compute_fos(x, y, r, cohesion, friction_angle, unit_weight)
        if fos > 1.0:  # Only return physically possible solutions
            return (x, y, r, fos)
    except:
        pass
    return None

def find_critical_circle(height: float, angle: float, cohesion: float, 
                        friction_angle: float, unit_weight: float, 
                        quick_mode: bool = True) -> Tuple[float, float, float, float]:
    """
    Find the critical failure circle that gives the minimum Factor of Safety.
    Uses parallel processing and optimized search space.
    
    Parameters:
    -----------
    height : float
        Slope height in meters
    angle : float
        Slope angle in degrees
    cohesion : float
        Soil cohesion in kPa
    friction_angle : float
        Soil friction angle in degrees
    unit_weight : float
        Soil unit weight in kN/m³
    quick_mode : bool
        If True, uses a smaller search space for faster results
    
    Returns:
    --------
    tuple
        (x_center, y_center, radius, min_fos)
    """
    # Define optimized search grid based on slope geometry
    angle_rad = math.radians(angle)
    face_length = height / math.tan(angle_rad)
    
    # Reduced search space focusing on likely critical circle locations
    n_points = 10 if quick_mode else 20
    
    x_range = np.linspace(0, face_length * 1.5, n_points)
    y_range = np.linspace(height * 0.5, height * 1.5, n_points)
    r_range = np.linspace(height * 0.5, height * 1.2, n_points)
    
    # Create parameter combinations for parallel processing
    params = []
    for x in x_range:
        for y in y_range:
            for r in r_range:
                params.append((x, y, r, height, angle, cohesion, friction_angle, unit_weight))
    
    # Use parallel processing to analyze circles
    min_fos = float('inf')
    critical_circle = None
    
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(analyze_circle, params))
    
    # Find minimum FOS from valid results
    valid_results = [r for r in results if r is not None]
    if not valid_results:
        return None, None, None, None
    
    # Find the circle with minimum FOS
    critical_circle = min(valid_results, key=lambda x: x[3])
    return critical_circle

# Example usage
if __name__ == "__main__":
    # Example parameters
    height = 10  # meters
    angle = 45   # degrees
    cohesion = 10  # kPa
    friction = 30  # degrees
    unit_weight = 20  # kN/m³
    
    # Find critical circle
    x, y, r, fos = find_critical_circle(height, angle, cohesion, friction, unit_weight)
    print(f"Critical circle: center=({x:.2f}, {y:.2f}), radius={r:.2f}")
    print(f"Minimum Factor of Safety: {fos:.3f}") 