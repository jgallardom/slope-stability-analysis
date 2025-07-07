"""\nSlope Stability Analysis Package\n---------------------------------\nProvides modular components for geometric calculations, slice analysis, stability evaluation and visualization.\n\nHaving this file makes the directory an explicit Python package so that intra-package\nrelative imports (e.g. 'from .geometry import ...') resolve correctly when the\nmodules are imported with 'import slope_stability ...' or run via\n'python -m slope_stability.some_module'.\n"""

from .compute_slice_properties import compute_slice_properties
from .calculate_slice_forces import calculate_slice_forces

__all__ = ['compute_slice_properties', 'calculate_slice_forces'] 