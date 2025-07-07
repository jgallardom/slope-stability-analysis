# Slope Stability Analysis Web Application

A web-based tool for performing slope stability analysis using the Ordinary Method of Slices (Fellenius Method). This application helps engineers and geotechnical professionals analyze slope stability and calculate the Factor of Safety (FoS).

## Features

- Calculate Factor of Safety (FoS) for slope stability
- Interactive web interface for parameter input
- Visualization of slope geometry and failure surface
- Critical failure surface search
- Detailed calculation results
- View source code functionality

## Technical Details

The application uses:
- Python 3.11+
- Flask web framework
- NumPy for calculations
- Matplotlib for visualizations
- Gunicorn for production deployment

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jgallardom/slope-stability-analysis.git
cd slope-stability-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally

1. Start the Flask development server:
```bash
flask run
```

2. Open your browser and navigate to `http://localhost:5000`

## Deployment

This application is configured for deployment on Render.com. The necessary configuration files (`render.yaml`) are included in the repository.

## Input Parameters

   - Slope Height (m)
- Slope Angle (degrees)
- Soil Properties:
  - Cohesion (kPa)
  - Friction Angle (degrees)
   - Unit Weight (kN/m³)

## Output

- Factor of Safety (FoS)
- Visual representation of:
  - Slope geometry
  - Critical failure surface
  - Center of rotation
- Numerical results

## Code Structure

- `app.py`: Main Flask application
- `slope_stability/calculator.py`: Core calculation module
- `templates/`: HTML templates
- `static/`: CSS and images

## License

MIT License 