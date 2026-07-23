"""One-at-a-time elasticity of best-scheme NPV to each input."""
import copy
from .optimizer import screen

VARY = {"Li": 0.2, "Mg": 0.2, "Br": 0.2, "Sr": 0.2, "K": 0.2, "B": 0.2, "flow": 0.2}


def _npv(brine, prices):
    return screen(brine, prices)[0]["npv_rub"]


def sensitivity(brine, prices=None):
    base = _npv(brine, prices); out = {}
    for key, frac in VARY.items():
        b2 = copy.deepcopy(brine)
        if key == "flow":
            b2.flow *= (1 + frac)
        else:
            b2.ions[key] = b2.ions.get(key, 0.0) * (1 + frac)
        hi = _npv(b2, prices)
        out[key] = round(((hi - base) / abs(base) if base else 0.0) / frac, 3)
    ranked = dict(sorted(out.items(), key=lambda kv: abs(kv[1]), reverse=True))
    return dict(base_npv=base, elasticity=ranked)
