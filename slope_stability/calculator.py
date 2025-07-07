#controls the stability calculation
import numpy as np
from slope_stability.stability import compute_safety_factor,create_default_groups
def calculator(params):
    #define groups of radious and center coordinates
    groups = create_default_groups(params)
    min_fos = np.inf
    critical_circle = None
    # Evaluate FoS for each candidate
    for x, y, r in groups:
        try:
            fos = compute_safety_factor((x, y), r, params)
        except Exception:
            # Skip invalid slices / math domain errors
            continue
        #store the minimum FoS
        if 0 < fos < min_fos:
            min_fos = fos
            critical_circle = {'center': (x, y),'radius': r,'fos': fos}
    if critical_circle is None:
        raise ValueError("No valid failure surface found")
    return critical_circle