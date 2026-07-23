"""Ionic balance, ionic strength, activity-corrected saturation indices.

Screening grade only. Davies activity model is treated as valid for ionic
strength I <= 0.5 mol/L (USGS PHREEQC FAQ / geothermal database reviews).
Above that, SI numbers are not used for decisions; pilot-grade work requires
Pitzer / PHREEQC / Reaktoro (see docs/CHEMISTRY.md).

Ksp values are 25 C screening constants — temperature dependence is NOT applied.
"""
from dataclasses import dataclass, field
import math

# ion -> (charge, molar mass g/mol). B ~neutral H3BO3: tracked, not charge-balanced.
IONS = {
    "Na": (1, 22.99), "K": (1, 39.10), "Ca": (2, 40.08), "Mg": (2, 24.31),
    "Sr": (2, 87.62), "Ba": (2, 137.33), "Li": (1, 6.94),
    "Cl": (-1, 35.45), "SO4": (-2, 96.06), "HCO3": (-1, 61.02),
    "Br": (-1, 79.90), "I": (-1, 126.90),
}
NEUTRAL = {"B": 10.81}
# Products with a recovery path in UNIT_LIBRARY. I is tracked/priced but has no unit yet.
RECOVERABLE = ["Li", "Br", "Sr", "K", "B"]
TRACKED_OPTIONAL = ["I"]

KSP = {"CaCO3": 10**-8.48, "CaSO4": 10**-4.58, "BaSO4": 10**-9.97, "SrSO4": 10**-6.63}
LOG_KSP_HALITE = 1.58
A_DH = 0.509
# Davies strictly documented to ~0.5; beyond this SI must not drive decisions.
DAVIES_VALID_I_MAX = 0.5
# Numerical clamp only — does NOT extend validity; gamma may be non-physical above 0.5.
DAVIES_NUMERICAL_I_CLAMP = 6.0
KSP_REFERENCE_TEMP_C = 25.0


@dataclass
class Brine:
    """Concentrations in mg/L. flow m3/day. temp C, ph, org mg/L (hydrocarbons)."""
    ions: dict
    flow: float = 1000.0
    temp: float = 25.0
    ph: float = 6.5
    org: float = 0.0
    name: str = "stream"
    unc: dict = field(default_factory=dict)
    # Transient process state (not serialized as lab input).
    preconcentrate: float = 1.0

    def molar(self, sp):
        mm = IONS[sp][1] if sp in IONS else NEUTRAL[sp]
        return self.ions.get(sp, 0.0) / 1000.0 / mm

    def tds(self):
        return sum(self.ions.get(i, 0.0) for i in list(IONS) + list(NEUTRAL))

    def ionic_strength(self):
        I = 0.0
        for i in IONS:
            I += self.molar(i) * IONS[i][0] ** 2
        return 0.5 * I

    def validate(self):
        for label, val in (("flow", self.flow), ("temp", self.temp), ("ph", self.ph), ("org", self.org)):
            if val is None or not math.isfinite(float(val)):
                raise ValueError(f"{label} must be finite")
        if self.flow < 0:
            raise ValueError("flow must be non-negative")
        if not (0.0 <= self.ph <= 14.0):
            raise ValueError("pH must be in [0,14]")
        if not (-50.0 <= self.temp <= 250.0):
            raise ValueError("temperature outside supported range")
        if self.org < 0:
            raise ValueError("org must be non-negative")
        bad = []
        for k, v in self.ions.items():
            if v is None or (isinstance(v, float) and not math.isfinite(v)) or float(v) < 0:
                bad.append(k)
            elif not math.isfinite(float(v)):
                bad.append(k)
        if bad:
            raise ValueError(f"negative, missing, or non-finite concentrations: {bad}")
        return True


def davies_gamma(z, I):
    """Davies activity coefficient (screening). Valid guidance: I <= 0.5.

    At higher I the formula can yield gamma > 1 (non-physical for this use);
    callers must check DAVIES_VALID_I_MAX / scaling_risk meta before decisions.
    Numerical clamp at DAVIES_NUMERICAL_I_CLAMP is for overflow only, not validity.
    """
    Ic = max(0.0, min(float(I), DAVIES_NUMERICAL_I_CLAMP))
    s = math.sqrt(Ic)
    log_g = -A_DH * z * z * (s / (1 + s) - 0.3 * Ic)
    return 10 ** log_g


def ionic_balance(b: Brine):
    b.validate()
    cat = sum(b.molar(i) * IONS[i][0] for i in IONS if IONS[i][0] > 0)
    an = sum(b.molar(i) * -IONS[i][0] for i in IONS if IONS[i][0] < 0)
    denom = cat + an
    if denom <= 0 or not math.isfinite(denom):
        err = float("nan")
    else:
        err = abs(cat - an) / denom * 100
    finite = math.isfinite(err)
    err_r = round(err, 2) if finite else None
    reject = (not finite) or (finite and err > 25.0)
    decision_grade = finite and err <= 10.0
    return {
        "cations_eq": round(cat, 5) if math.isfinite(cat) else None,
        "anions_eq": round(an, 5) if math.isfinite(an) else None,
        "ionic_strength": round(b.ionic_strength(), 3),
        "balance_error_pct": err_r,
        "acceptable": decision_grade,
        "decision_grade": decision_grade,
        "reject_sample": reject,
        "density_assumption": "mg/L treated as approx. mol/L at density~1 kg/L (screening)",
    }


def _si(iap, ksp):
    return round(math.log10(iap / ksp), 2) if iap > 0 else -99.0


def scaling_risk(b: Brine):
    """Return (si, flags, meta).

    If ionic strength > DAVIES_VALID_I_MAX, SI values are returned for
    transparency but flags are all False and meta.si_reliable is False so
    downstream gates do not treat them as actionable scaling evidence.
    Ksp are 25 C constants regardless of brine.temp.
    """
    b.validate()
    I = b.ionic_strength()
    reliable = I <= DAVIES_VALID_I_MAX
    meta = {
        "ionic_strength": round(I, 3),
        "davies_valid_i_max": DAVIES_VALID_I_MAX,
        "davies_valid": reliable,
        "si_reliable": reliable,
        "activity_model": "davies" if reliable else "davies_out_of_range",
        "ksp_reference_temp_c": KSP_REFERENCE_TEMP_C,
        "brine_temp_c": b.temp,
        "temp_dependence": "none_screening",
        "upgrade": "Pitzer/PHREEQC/Reaktoro required for pilot-grade SI",
    }
    if abs(b.temp - KSP_REFERENCE_TEMP_C) > 5.0:
        meta["temp_warning"] = (
            f"brine.temp={b.temp} C differs from Ksp reference {KSP_REFERENCE_TEMP_C} C; "
            "SI not temperature-corrected"
        )
    a = lambda sp: davies_gamma(abs(IONS[sp][0]), I) * b.molar(sp)
    ca, sr, ba = a("Ca"), a("Sr"), a("Ba")
    so4, hco3, na, cl = a("SO4"), a("HCO3"), a("Na"), a("Cl")
    co3 = hco3 * 10 ** (b.ph - 10.33)
    si_calc = {
        "CaCO3": _si(ca * co3, KSP["CaCO3"]),
        "CaSO4": _si(ca * so4, KSP["CaSO4"]),
        "BaSO4": _si(ba * so4, KSP["BaSO4"]),
        "SrSO4": _si(sr * so4, KSP["SrSO4"]),
        "Halite": _si(na * cl, 10 ** LOG_KSP_HALITE),
    }
    if reliable:
        flags = {k: v > 0 for k, v in si_calc.items()}
        si = si_calc
    else:
        flags = {k: False for k in si_calc}
        si = {k: None for k in si_calc}
        meta["si_transparency"] = si_calc
        meta["note"] = (
            f"I={I:.2f} > {DAVIES_VALID_I_MAX}: SI not decision-grade; "
            "use Pitzer/PHREEQC before pilot"
        )
    return si, flags, meta


def mg_li_ratio(b: Brine):
    li = b.molar("Li")
    return (b.molar("Mg") / li) if li > 0 else 1e9
