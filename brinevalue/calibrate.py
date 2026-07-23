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
    """Apply per-(unit, ion) correction factors to overall recovery.

    ``unit_ion_map`` optional ``{ion: unit}`` selects which unit's factor applies
    when several units could correct the same ion. Without a map, if multiple
    factors exist for one ion, their **median** is used (avoids stacking).
    """
    out = dict(flowsheet_recovery)
    by_ion = {}
    for (unit, ion), f in corrections.items():
        if unit_ion_map is not None and unit_ion_map.get(ion) != unit:
            continue
        by_ion.setdefault(ion, []).append(float(f))
    for ion, factors in by_ion.items():
        if ion not in out:
            continue
        factor = factors[0] if len(factors) == 1 else float(np.median(factors))
        out[ion] = round(min(1.0, out[ion] * factor), 3)
    return out
