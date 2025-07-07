"""
Slice Forces Calculator
---------------------
Calculates forces and moments for a single slice in the method of slices.
"""

import numpy as np

def calculate_slice_forces(slice_data, unit_weight, cohesion, friction_angle):
    """Calculate forces and moments for a slice.
    
    Forces and moments follow academic conventions:
    - Normal force = Weight·cos(θ), where θ is angle from vertical
    - Driving moment: Weight × perpendicular distance to center
    - Resisting moment: (Normal·tan(φ) + c·L) × radius
    
    Args:
        slice_data: Dictionary containing slice geometry
        unit_weight: Soil unit weight (kN/m³)
        cohesion: Soil cohesion (kPa)
        friction_angle: Soil friction angle (degrees)
    
    Returns:
        Dictionary containing:
        - weight: Total weight of slice
        - normal: Normal force on base
        - resisting_force: Total resisting force
        - theta: Angle between vertical and radius
    """
    if not slice_data:
        return None
        
    theta = slice_data['theta']  # Angle from vertical
    
    # Convert friction angle to radians
    phi_rad = np.radians(friction_angle)
    
    # Calculate weight and its moment arm
    weight = unit_weight * slice_data['area']
    arm_length = slice_data['arm_length']
    
    # Calculate normal force (N = W·cos(θ))
    # When θ = 0 (vertical radius), cos(θ) = 1, N = W
    # When θ = ±π/2 (horizontal radius), cos(θ) = 0, N = 0
    normal = weight * np.cos(theta)
    
    frictional_component = normal * np.tan(phi_rad)
    cohesive_component = cohesion * slice_data['base_length']
    
    # Total resisting force
    resisting_force = (frictional_component + cohesive_component)

    return {
        'weight': weight,
        'normal': normal,
        'resisting_force': resisting_force,
        'theta': theta
    } 