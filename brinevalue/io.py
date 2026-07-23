"""CSV/Excel import + reproducible synthetic streams (Li/K/Br/B/Sr/I)."""
import pandas as pd, numpy as np
from .chemistry import Brine, IONS, NEUTRAL

ALL_SPECIES = list(IONS) + list(NEUTRAL)


def brine_from_row(row, name="stream"):
    ions = {i: float(row[i]) for i in ALL_SPECIES if i in row and pd.notna(row[i])}
    return Brine(ions=ions, flow=float(row.get("flow", 1000)),
                 temp=float(row.get("temp", 25)), ph=float(row.get("ph", 6.5)),
                 org=float(row.get("org", 0)), name=str(row.get("name", name)),
                 unc={"Li": 0.3, "Mg": 0.25, "Br": 0.3, "Sr": 0.3, "K": 0.3, "B": 0.3, "flow": 0.2})


def load_table(path):
    df = pd.read_excel(path) if str(path).endswith(("xlsx", "xls")) else pd.read_csv(path)
    return [brine_from_row(r, f"stream_{i}") for i, r in df.iterrows()]


def synthetic_streams(n=8, seed=0):
    rng = np.random.default_rng(seed)
    out = []
    for i in range(n):
        ions = dict(Na=rng.uniform(1e4, 6e4), K=rng.uniform(800, 4800), Ca=rng.uniform(2000, 3e4),
                    Mg=rng.uniform(200, 6000), Sr=rng.uniform(50, 1500), Ba=rng.uniform(1, 300),
                    Li=rng.uniform(20, 200), Cl=rng.uniform(4e4, 1.3e5), SO4=rng.uniform(50, 3000),
                    HCO3=rng.uniform(100, 1500), Br=rng.uniform(50, 250), B=rng.uniform(100, 500),
                    I=rng.uniform(5, 80))
        out.append(Brine(ions={k: round(v, 1) for k, v in ions.items()},
                         flow=round(rng.uniform(300, 4000)), temp=round(rng.uniform(20, 80), 1),
                         ph=round(rng.uniform(5.5, 7.5), 2), org=round(rng.uniform(8, 30), 1),
                         name=f"synthetic_{i}",
                         unc={"Li": 0.3, "Mg": 0.25, "Br": 0.3, "Sr": 0.3, "K": 0.3, "B": 0.3, "flow": 0.2}))
    return out
