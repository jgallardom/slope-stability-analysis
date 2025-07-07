"""
Slope Stability Web Application
-----------------------------
A simple web interface for slope stability analysis.
"""

from flask import Flask, render_template, request, jsonify
import os

from slope_stability.visualization import create_analysis_plot
from slope_stability.calculator import calculator
app = Flask(__name__)

# Ensure images directory exists
os.makedirs('static/images', exist_ok=True)

@app.route('/')
def index():
    """Render the main page."""
    # Read source code files
    code_files = {
        'geometry': open('slope_stability/geometry.py').read(),
        'compute_slice_properties': open('slope_stability/compute_slice_properties.py').read(),
        'calculate_slice_forces': open('slope_stability/calculate_slice_forces.py').read(),
        'stability': open('slope_stability/stability.py').read(),
        'visualization': open('slope_stability/visualization.py').read(),
        'app': open('app.py').read()
    }
    return render_template('code_view.html', code_files=code_files)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation request."""
    try:
        # Get input parameters
        params = {
            'height': float(request.form['height']),
            'slope_angle': float(request.form['slopeAngle']),
            'cohesion': float(request.form['cohesion']),
            'friction': float(request.form['friction']),
            'unit_weight': float(request.form['unitWeight'])
        }
       
        #CALCULATE
        result = calculator(params)


        # Create visualization
        plot_url = create_analysis_plot(
            params['height'], 
            params['slope_angle'], 
            result
        )
        
        return jsonify({
            'success': True,
            'fos': result['fos'],
            'center': {'x': result['center'][0], 'y': result['center'][1]},
            'radius': result['radius'],
            'plot_image': plot_url
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/code')
def code_view():
    """Display the Python code with syntax highlighting."""
    # Read the code files
    with open('slope_stability/compute_slice_properties.py', 'r') as f:
        compute_slice_properties_code = f.read()
    
    with open('slope_stability/calculate_slice_forces.py', 'r') as f:
        calculate_slice_forces_code = f.read()
    
    return render_template('code_view.html',
                          compute_slice_properties_code=compute_slice_properties_code,
                          calculate_slice_forces_code=calculate_slice_forces_code)

if __name__ == '__main__':
    app.run(debug=True) 