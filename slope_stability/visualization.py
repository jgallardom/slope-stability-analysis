"""
Visualization Module
------------------
Handles all plotting and visualization for slope stability analysis.
"""

# Use non-interactive backend for thread-safe rendering (no GUI needed)
import matplotlib
import numpy as np
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64


def create_base_plot():
    """Create and configure the base plot."""
    plt.figure(figsize=(10, 8))
    plt.grid(True)
    plt.axis('equal')
    plt.xlabel('Distance (m)')
    plt.ylabel('Elevation (m)')

def plot_slope(height, slope_angle):
    """Plot the slope geometry."""
    x_slope = height / np.tan(np.radians(slope_angle))
    plt.plot([-height,0,x_slope,x_slope+height],[height,height,0,0],'k-', linewidth=2)


def plot_failure_circle(center, radius):
    """Plot the critical failure circle."""
    circle = plt.Circle(center, radius, fill=False, 
                       linestyle='--', color='r', 
                       label='Critical Surface')
    plt.gca().add_patch(circle)

def create_analysis_plot(height, slope_angle, critical_circle=None):
    """Create complete slope stability analysis visualization."""
    # Setup plot
    create_base_plot()
    
    # Plot slope geometry
    plot_slope(height, slope_angle)
    
    # Add failure circle if provided
    if critical_circle:
        plot_failure_circle(critical_circle['center'], 
                          critical_circle['radius'])
    
    plt.legend()
    
    # Convert plot to base64 image
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png', bbox_inches='tight')
    img_data.seek(0)
    plt.close()
    
    return 'data:image/png;base64,' + base64.b64encode(img_data.getvalue()).decode()

def create_slices_plot(height, slope_angle, center, radius, slices=30):
    """Create visualization showing the method of slices."""
    # Setup plot
    create_base_plot()
    
    # Plot basic geometry
    plot_slope(height, slope_angle)
    plot_failure_circle(center, radius)
    
    # Add slice lines
    dx = 2 * radius / slices
    for x in range(slices + 1):
        x_pos = center[0] - radius + x * dx
        if abs(x_pos - center[0]) <= radius:
            plt.plot([x_pos, x_pos], [0, height], 
                    'b--', linewidth=0.5, alpha=0.3)
    
    plt.legend()
    
    # Convert plot to base64 image
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png', bbox_inches='tight')
    img_data.seek(0)
    plt.close()
    
    return 'data:image/png;base64,' + base64.b64encode(img_data.getvalue()).decode() 