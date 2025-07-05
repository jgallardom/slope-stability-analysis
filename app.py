"""
Slope Stability Analysis Web Application
--------------------------------------
This application calculates the Factor of Safety (FoS) for slope stability
using the Ordinary Method of Slices (Fellenius Method).

Main components:
1. Slope geometry calculations
2. Factor of Safety computation
3. Critical failure surface search
4. Web interface for input/output
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import os
from slope_stability.calculator import find_critical_circle

# Configure matplotlib to use Agg backend
plt.switch_backend('Agg')

app = Flask(__name__)

# Ensure the static/images directory exists
os.makedirs('static/images', exist_ok=True)

# ---- Slope Geometry Functions ----

def calculate_ground_surface(x, height, slope_angle):
    """
    Calculate the y-coordinate of ground surface at given x.
    
    Args:
        x: x-coordinate point
        height: slope height
        slope_angle: angle of slope in degrees
    
    Returns:
        y-coordinate of ground surface
    """
    slope_rad = np.radians(slope_angle)
    x_slope = height / np.tan(slope_rad)
    
    if x <= 0:
        return height
    elif x <= x_slope:
        return height - x * np.tan(slope_rad)
    else:
        return 0

# ---- Stability Analysis Functions ----

def compute_slice_properties(x, center, radius, height, slope_angle, dx):
    """
    Compute geometric properties of a slice.
    
    Args:
        x: x-coordinate of slice
        center: (x,y) coordinates of circle center
        radius: radius of failure circle
        height: slope height
        slope_angle: slope angle in degrees
        dx: width of slice
    
    Returns:
        tuple of (weight, alpha, base_length) or None if slice is invalid
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
        
    # Calculate slice properties
    slice_height = y_ground - y_circle
    alpha = np.arctan2(center[1] - y_circle, center[0] - x)
    
    return slice_height, alpha, dx

def compute_fos_slices(center, radius, c, phi, gamma, slope_angle, height, slices=30):
    """
    Calculate Factor of Safety using Method of Slices.
    
    Args:
        center: (x,y) coordinates of circle center
        radius: radius of failure circle
        c: cohesion (kPa)
        phi: friction angle (degrees)
        gamma: unit weight (kN/m³)
        slope_angle: slope angle (degrees)
        height: slope height (m)
        slices: number of slices to use
    
    Returns:
        Factor of Safety value
    """
    phi_rad = np.radians(phi)
    dx = 2 * radius / slices
    sum_moments = sum_weights = 0
    
    # Iterate through slices
    for x in np.arange(center[0] - radius, center[0] + radius, dx):
        slice_props = compute_slice_properties(x, center, radius, height, slope_angle, dx)
        if not slice_props:
            continue
            
        slice_height, alpha, dx = slice_props
        weight = gamma * slice_height * dx
        
        # Add slice contributions
        sum_moments += (c * dx / np.sin(alpha) + weight * np.sin(alpha) * np.tan(phi_rad))
        sum_weights += weight * np.cos(alpha)
    
    return np.inf if sum_weights == 0 else sum_moments / sum_weights

def find_critical_circle(c, phi, gamma, slope_angle, height):
    """
    Find the critical failure circle with minimum Factor of Safety.
    
    Args:
        c: cohesion (kPa)
        phi: friction angle (degrees)
        gamma: unit weight (kN/m³)
        slope_angle: slope angle (degrees)
        height: slope height (m)
    
    Returns:
        tuple of (center_coordinates, radius, factor_of_safety)
    """
    x_slope = height / np.tan(np.radians(slope_angle))
    min_fos, result = np.inf, None
    
    # Search grid parameters
    x_range = np.linspace(-height/2, x_slope + height/2, 20)
    y_range = np.linspace(height/2, height*2, 20)
    r_range = np.linspace(height/2, height*2, 10)
    
    # Search through all possible circles
    for x, y, radius in [(x, y, r) for x in x_range for y in y_range for r in r_range]:
        try:
            fos = compute_fos_slices((x, y), radius, c, phi, gamma, slope_angle, height)
            if 0 < fos < min_fos:
                min_fos, result = fos, ((x, y), radius, fos)
        except:
            continue
    
    if not result:
        raise ValueError("Could not find a valid failure surface. Check input parameters.")
    return result

# ---- Visualization Functions ----

def plot_slope_analysis(center, radius, params):
    """
    Create visualization of slope and failure surface.
    
    Args:
        center: (x,y) coordinates of critical circle center
        radius: radius of critical circle
        params: dictionary containing slope parameters
    
    Returns:
        path to saved image
    """
    plt.figure(figsize=(10, 8))
    
    # Plot slope geometry
    slope_rad = np.radians(params['slopeAngle'])
    x_slope = params['height'] / np.tan(slope_rad)
    
    plt.plot([0, x_slope], [params['height'], 0], 'k-', linewidth=2, label='Slope surface')
    plt.plot([-params['height']/2, 0], [params['height'], params['height']], 'k-', linewidth=2)
    plt.plot([x_slope, x_slope + params['height']/2], [0, 0], 'k-', linewidth=2)
    
    # Plot failure circle
    circle = plt.Circle(center, radius, fill=False, linestyle='--', color='r', label='Failure surface')
    plt.gca().add_patch(circle)
    
    plt.axis('equal')
    plt.grid(True)
    plt.xlabel('Distance (m)')
    plt.ylabel('Elevation (m)')
    plt.legend()
    
    # Save plot
    image_path = f'images/failure_surface_{np.random.randint(10000)}.png'
    plt.savefig(f'static/{image_path}')
    plt.close()
    
    return image_path

# ---- Web Routes ----

@app.route('/')
def index():
    """Render the input form."""
    return render_template('input.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation request and return results."""
    try:
        params = {
            'height': float(request.form['height']),
            'slopeAngle': float(request.form['slopeAngle']),
            'cohesion': float(request.form['cohesion']),
            'friction': float(request.form['friction']),
            'unitWeight': float(request.form['unitWeight'])
        }
        
        # Validate input parameters
        if params['height'] <= 0 or params['slopeAngle'] <= 0 or params['slopeAngle'] >= 90:
            raise ValueError("Invalid height or slope angle")
        if params['friction'] < 0 or params['friction'] >= 90:
            raise ValueError("Invalid friction angle")
        if params['cohesion'] < 0 or params['unitWeight'] <= 0:
            raise ValueError("Invalid cohesion or unit weight")
            
        center, radius, fos = find_critical_circle(params)
        
        return jsonify({
            'success': True,
            'center': {'x': float(center[0]), 'y': float(center[1])},
            'radius': float(radius),
            'fos': float(fos)
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': "Calculation error occurred"}), 500

if __name__ == '__main__':
    # Use environment variables for configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', False)
    app.run(host='0.0.0.0', port=port, debug=debug) 