"""CSV/Excel import + reproducible synthetic streams (Li/K/Br/B/Sr/I)."""
import pandas as pd, numpy as np
from .chemistry import Brine, IONS, NEUTRAL

ALL_SPECIES = list(IONS) + list(NEUTRAL)


def _finite_nonneg(value, label, default=None):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        if default is not None:
            return float(default)
        raise ValueError(f"missing value for {label}")
    try:
        fv = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"non-numeric value for {label}: {value!r}") from exc
    if not np.isfinite(fv):
        raise ValueError(f"non-finite value for {label}")
    if fv < 0:
        raise ValueError(f"negative value for {label}")
    return fv


def brine_from_row(row, name="stream"):
    ions = {}
    for i in ALL_SPECIES:
        if i in row and pd.notna(row[i]):
            ions[i] = _finite_nonneg(row[i], i)
    temp = 25.0
    if "temp" in row and pd.notna(row.get("temp")):
        try:
            temp = float(row["temp"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"non-numeric value for temp: {row['temp']!r}") from exc
    ph = 6.5
    if "ph" in row and pd.notna(row.get("ph")):
        try:
            ph = float(row["ph"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"non-numeric value for ph: {row['ph']!r}") from exc
    b = Brine(
        ions=ions,
        flow=_finite_nonneg(row.get("flow", 1000), "flow", 1000),
        temp=temp,
        ph=ph,
        org=_finite_nonneg(row.get("org", 0), "org", 0),
        name=str(row["name"]) if "name" in row and pd.notna(row.get("name")) else str(name),
        unc={"Li": 0.3, "Mg": 0.25, "Br": 0.3, "Sr": 0.3, "K": 0.3, "B": 0.3, "flow": 0.2},
    )
    b.validate(strict_species=True)
    return b


def load_table(path):
    path_s = str(path)
    if path_s.lower().endswith(("xlsx", "xls")):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"empty table: {path}")
    out = []
    errors = []
    for i, r in df.iterrows():
        try:
            out.append(brine_from_row(r, f"stream_{i}"))
        except (TypeError, ValueError) as exc:
            errors.append(f"row {i}: {exc}")
    if not out:
        raise ValueError("no valid rows in table: " + "; ".join(errors[:5]))
    if errors:
        # Partial load is useful for screening; surface issues on stderr-like print path via CLI.
        import sys
        print(f"warning: skipped {len(errors)} invalid row(s): {errors[0]}", file=sys.stderr)
    return out


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
