"""Greedy uncertainty-reduction measurement ranking (NOT Bayesian optimization,
NOT a process batch DoE for sorption/regeneration/product quality).

Propagates input uncertainty to NPV by Monte Carlo, then greedily picks
which **input measurement** (each collapses one input's sigma) most reduces
NPV standard deviation. Sampling here uses independent Normal multipliers;
``robust_screen`` uses independent lognormals — rankings are explanatory, not
identical to the robust risk report. Explainable; no acquisition function.
For Beta lab posteriors see bayes.py (diagnostic unless applied).
"""
import copy
import numpy as np
from .optimizer import screen

UNCERTAIN = ["Li", "Mg", "Br", "Sr", "K", "B", "flow"]
EXPERIMENT = {
    "Li": "Точный анализ Li (ICP-MS)",
    "Mg": "Анализ жёсткости Mg/Ca",
    "Br": "Титрование Br",
    "Sr": "Анализ Sr",
    "K": "Анализ K",
    "B": "Анализ B (бор)",
    "flow": "Замер дебита потока",
}


def _sample_npv(brine, prices, rng, fixed):
    b2 = copy.deepcopy(brine)
    for k in UNCERTAIN:
        sigma = 0.0 if k in fixed else brine.unc.get(k, 0.25)
        factor = max(0.05, rng.normal(1.0, sigma))
        if k == "flow":
            b2.flow *= factor
        else:
            b2.ions[k] = b2.ions.get(k, 0.0) * factor
    return screen(b2, prices)[0]["npv_rub"]


def _std(brine, prices, fixed, n, seed):
    rng = np.random.default_rng(seed)
    return float(np.std([_sample_npv(brine, prices, rng, fixed) for _ in range(n)]))


def propose_experiments(brine, prices=None, k=4, n=150, seed=0):
    chosen, plan = [], []
    cur = _std(brine, prices, set(), n, seed)
    base = cur
    remaining = list(UNCERTAIN)
    for _ in range(min(k, len(remaining))):
        best = None
        for cand in remaining:
            s = _std(brine, prices, set(chosen) | {cand}, n, seed)
            if best is None or s < best[1]:
                best = (cand, s)
        cand, s = best
        std_reduction = round(cur - s)
        plan.append(
            dict(
                experiment=EXPERIMENT[cand],
                target=cand,
                npv_std_after=round(s),
                npv_std_reduction_rub=std_reduction,
                # Deprecated alias (was misnamed: value is std reduction, not variance).
                variance_reduction_rub=std_reduction,
            )
        )
        chosen.append(cand)
        remaining.remove(cand)
        cur = s
    return dict(
        method="greedy_uncertainty_reduction",
        bayesian_optimization=False,
        process_batch_doe=False,
        base_npv_std=round(base),
        plan=plan,
        note=(
            "Not Bayesian optimization and not process batch DoE; "
            "ranks which additional feed measurement most reduces NPV std"
        ),
    )
