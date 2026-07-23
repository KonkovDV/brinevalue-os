"""Uncertainty-aware decision layer.

Samples measured concentrations and flow with **independent** lognormal
perturbations (one multiplier per variable; no cross-ion correlation matrix),
then reruns the transparent first-principles screen. The output is a decision
risk report, not a black-box forecast: P(NPV>0), quantiles, and scheme stability.
Not a full robust project-economics model (CAPEX/OPEX/recovery/prices fixed).
"""
import copy
import numpy as np
from .optimizer import screen

VARS = ["Li", "Br", "Sr", "K", "B", "I", "Mg", "flow"]

def _sample(b, rng):
    s = copy.deepcopy(b)
    for k in VARS:
        rel = float(b.unc.get(k, 0.20))
        mult = max(0.01, rng.lognormal(mean=-0.5*rel*rel, sigma=rel))
        if k == "flow": s.flow *= mult
        else: s.ions[k] = s.ions.get(k, 0.0) * mult
    return s


def robust_screen(brine, prices=None, n=400, seed=0):
    rng = np.random.default_rng(seed)
    npvs, schemes = [], []
    for _ in range(n):
        rows = screen(_sample(brine, rng), prices)
        npvs.append(rows[0]["npv_rub"]); schemes.append(rows[0]["scheme"])
    x = np.asarray(npvs, dtype=float)
    q = np.quantile(x, [0.05, 0.5, 0.95])
    vals, counts = np.unique(schemes, return_counts=True)
    order = np.argsort(counts)[::-1]
    return {
        "n": int(n), "seed": int(seed), "p_npv_positive": round(float(np.mean(x > 0)), 3),
        "npv_p05_rub": int(q[0]), "npv_median_rub": int(q[1]), "npv_p95_rub": int(q[2]),
        "scheme_stability": {str(vals[i]): round(float(counts[i]/n), 3) for i in order},
        "decision_confidence": "high" if (np.mean(x > 0) >= .9 or np.mean(x > 0) <= .1) else "medium",
        "perturbation": "independent_lognormal_composition_and_flow",
    }
