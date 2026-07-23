"""Explicit Beta posterior for laboratory recovery observations.

Diagnostic by default: pipeline returns posterior but does NOT override unit
library recoveries unless caller applies calibrate_units results manually.
Energy/reagent Normal-Inverse-Gamma is NOT implemented.
"""
from dataclasses import dataclass
import math


@dataclass
class BetaPosterior:
    alpha: float = 2.0
    beta: float = 2.0

    def update(self, recovery, weight=1.0):
        r = min(1.0, max(0.0, float(recovery)))
        self.alpha += r * weight
        self.beta += (1 - r) * weight
        return self

    @property
    def mean(self):
        return self.alpha / (self.alpha + self.beta)

    def interval95(self):
        # Normal approximation to Beta; sufficient for screening lab counts.
        m = self.mean
        n = self.alpha + self.beta
        sd = math.sqrt(max(1e-12, m * (1 - m) / (n + 1)))
        return (max(0.0, m - 1.96 * sd), min(1.0, m + 1.96 * sd))


def posterior_recovery(observations, prior=(2.0, 2.0)):
    """observations: [{"recovery": 0..1, "weight": optional}]."""
    post = BetaPosterior(*prior)
    for o in observations:
        post.update(o["recovery"], o.get("weight", 1.0))
    lo, hi = post.interval95()
    return {
        "alpha": round(post.alpha, 3),
        "beta": round(post.beta, 3),
        "mean": round(post.mean, 4),
        "interval95": [round(lo, 4), round(hi, 4)],
        "role": "diagnostic_lab_posterior",
        "applied_to_tea": False,
    }


def calibrate_units(observations):
    """Group lab observations by unit and ion, returning posterior recovery."""
    grouped = {}
    for o in observations:
        key = f"{o['unit']}::{o['ion']}"
        grouped.setdefault(key, []).append(o)
    return {k: posterior_recovery(v) for k, v in grouped.items()}
