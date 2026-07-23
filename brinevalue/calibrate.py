"""Model calibration from lab batch results. Fits a single multiplicative
correction per unit recovery by least squares on observed vs predicted.
"""
import numpy as np
from .process import UNIT_LIBRARY


def calibrate_recovery(observations):
    """observations: list of dicts {unit, ion, predicted, observed}.
    Returns per-(unit,ion) correction factor = observed/predicted (robust mean).
    """
    from collections import defaultdict
    ratios = defaultdict(list)
    for o in observations:
        if o["predicted"]:
            ratios[(o["unit"], o["ion"])].append(o["observed"] / o["predicted"])
    return {k: round(float(np.median(v)), 3) for k, v in ratios.items()}


def apply_correction(flowsheet_recovery, corrections, unit_ion_map=None):
    out = dict(flowsheet_recovery)
    for (unit, ion), f in corrections.items():
        if ion in out:
            out[ion] = round(min(1.0, out[ion] * f), 3)
    return out
