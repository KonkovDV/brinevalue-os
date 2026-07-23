"""Surrogate-assisted techno-economic optimization.

Directly implements the surrogate-model approach validated in 2025-2026 for
produced-water valorization (Tiam et al., Water 2026, Permian Basin;
Scelfo et al., Desalination 2025, ultra-concentrated brine scale-up).

We sample brine compositions, evaluate the full physico-chemical + TEA model to
get best-scheme NPV, then fit a fast RandomForest surrogate over
[Li,Mg,Br,Sr,K,B,flow,TDS,temp,ph]. The surrogate accelerates Monte-Carlo
uncertainty propagation and sensitivity by orders of magnitude while the
explainable physics model remains the source of truth.
"""
import numpy as np
from .chemistry import Brine
from .optimizer import screen

FEATURES = ["Li", "Mg", "Br", "Sr", "K", "B", "flow", "TDS", "temp", "ph"]


def _features(b: Brine):
    return [b.ions.get("Li", 0), b.ions.get("Mg", 0), b.ions.get("Br", 0),
            b.ions.get("Sr", 0), b.ions.get("K", 0), b.ions.get("B", 0),
            b.flow, b.tds(), b.temp, b.ph]


def _random_brine(rng):
    ions = dict(Na=rng.uniform(1e4, 6e4), K=rng.uniform(200, 4800), Ca=rng.uniform(2000, 3e4),
                Mg=rng.uniform(200, 8000), Sr=rng.uniform(50, 1500), Ba=rng.uniform(1, 300),
                Li=rng.uniform(20, 200), Cl=rng.uniform(4e4, 1.3e5), SO4=rng.uniform(50, 3000),
                HCO3=rng.uniform(100, 1500), Br=rng.uniform(50, 250), B=rng.uniform(100, 500),
                I=rng.uniform(5, 80))
    return Brine(ions={k: round(v, 1) for k, v in ions.items()}, flow=round(rng.uniform(300, 4000)),
                 temp=round(rng.uniform(20, 80), 1), ph=round(rng.uniform(5.5, 7.5), 2))


def train_surrogate(n=400, seed=0):
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import cross_val_score
    rng = np.random.default_rng(seed)
    X, y = [], []
    for _ in range(n):
        b = _random_brine(rng)
        X.append(_features(b)); y.append(screen(b)[0]["npv_rub"])
    X = np.array(X); y = np.array(y)
    model = RandomForestRegressor(n_estimators=200, max_depth=14, random_state=seed, n_jobs=-1)
    cv = cross_val_score(model, X, y, cv=5, scoring="r2")
    model.fit(X, y)
    importances = dict(sorted(zip(FEATURES, model.feature_importances_),
                              key=lambda kv: kv[1], reverse=True))
    return dict(model=model, cv_r2_mean=round(float(cv.mean()), 3),
                cv_r2_std=round(float(cv.std()), 3), n=n,
                importances={k: round(float(v), 3) for k, v in importances.items()})


def predict_npv(model, brine):
    return float(model.predict([_features(brine)])[0])
