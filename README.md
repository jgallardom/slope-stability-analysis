# Slope Stability Analysis Web Application

A web-based application for performing slope stability analysis using the Method of Slices (Fellenius/Ordinary Method). The application finds the critical failure surface and calculates the minimum Factor of Safety for a given slope configuration.

## Features

- Interactive web interface for input parameters
- Real-time calculation of Factor of Safety
- Client-side input validation
- Responsive design for mobile and desktop
- Modern UI with Bootstrap styling

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/slope-stability-analysis.git
cd slope-stability-analysis
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Local Development

1. Start the Flask development server:
```bash
python app.py
```

2. Open a web browser and navigate to:
```
http://localhost:5000
```

3. Enter the slope parameters:
   - Slope Height (m)
   - Slope Angle (°)
   - Soil Cohesion (kPa)
   - Friction Angle (°)
   - Unit Weight (kN/m³)

4. Click "Calculate" to perform the analysis

### Deployment

The application is ready for deployment on platforms like Heroku or Render. It includes:

- Procfile for Heroku/Render deployment
- gunicorn as the production server
- Environment variable support for configuration

To deploy on Render:

1. Create a new Web Service
2. Connect your GitHub repository
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Deploy

## Project Structure

```
slope-stability-analysis/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
├── static/
│   ├── style.css         # Custom CSS styles
│   └── images/           # Generated plot images
├── templates/
│   └── input.html        # HTML template
└── slope_stability/
    └── calculator.py     # Stability calculation module
```

## Technical Details

The application implements the Ordinary Method of Slices (Fellenius Method) for slope stability analysis. It searches for the critical failure surface by:

1. Generating trial circles with different centers and radii
2. Computing the Factor of Safety for each circle
3. Finding the minimum Factor of Safety among all trials

The Factor of Safety is calculated as:
```
FOS = Resisting Moments / Driving Moments
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 