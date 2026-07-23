"""Library of transparent unit operations for full-component recovery.

Screening-grade correlations frozen in docs/PROCESS.md. Literature citations
are company-reported or peer-reviewed analogs — not replications of this code.
H2S and hydrocarbon removal are NOT modeled; only SO4 fraction is reduced.
"""
import math
from .chemistry import Brine, mg_li_ratio


def desulfurization(b, p=None):
    # Screening: SO4 only. H2S / hydrocarbons are quality-gate concerns, not mass removals.
    return dict(
        kind="desulfurization", recovery={}, remove={"SO4": 0.7},
        reagent_kg_per_m3=0.15, kwh_per_m3=0.2,
        note="SO4 reduction only (screening). H2S/organics not modeled — see quality.org gate",
    )


def softening(b, p=None):
    hardness = b.molar("Ca") + b.molar("Mg")
    return dict(kind="softening", recovery={}, remove={"Ca": 0.9, "Mg": 0.85, "Ba": 0.8},
                reagent_kg_per_m3=round(0.06 * hardness * 1000, 3), kwh_per_m3=0.3,
                note="lime-soda softening protects sorbent/membrane (screening correlation)")


def mg_rejection_ec(b, p=None):
    return dict(kind="mg_rejection_ec", recovery={}, remove={"Mg": 0.999},
                reagent_kg_per_m3=0.0, kwh_per_m3=2.0,
                note="electrochemical Mg rejection proxy (screening; Zhang EST 2026 analog, not calibrated)")


def evaporation_concentration(b, p=None):
    return dict(
        kind="evaporation_concentration", recovery={}, concentrate=3.0,
        reagent_kg_per_m3=0.0, kwh_per_m3=8.0,
        note="volume reduction + ion concentration; modest DLE boost via preconcentrate factor",
    )


def dle_sorption_li(b, p=None):
    r = mg_li_ratio(b)
    rec = max(0.35, 0.90 - min(0.5, max(0.0, (r - 3) * 0.03)))
    # Screening: pre-concentration raises effective loading proxy slightly (not Alshammari replica).
    cf = max(1.0, float(getattr(b, "preconcentrate", 1.0) or 1.0))
    boost = min(0.08, 0.025 * math.log10(cf)) if cf > 1.0 else 0.0
    rec = min(0.95, rec + boost)
    return dict(kind="dle_sorption_li", recovery={"Li": round(rec, 3)},
                reagent_kg_per_m3=0.4, kwh_per_m3=1.2,
                note=f"Mn-sorbent screening, Mg/Li={r:.1f}, preconcentrate={cf:.2f}")


def dle_solvent_extraction_li(b, p=None):
    r = mg_li_ratio(b)
    rec = max(0.5, 0.88 - min(0.35, max(0.0, (r - 6) * 0.02)))
    cf = max(1.0, float(getattr(b, "preconcentrate", 1.0) or 1.0))
    boost = min(0.05, 0.02 * math.log10(cf)) if cf > 1.0 else 0.0
    rec = min(0.95, rec + boost)
    return dict(kind="dle_solvent_extraction_li", recovery={"Li": round(rec, 3)},
                reagent_kg_per_m3=0.9, kwh_per_m3=0.8,
                note="solvent extraction screening, Mg-tolerant (Nikfar 2026 analog)")


def dle_electrodialysis_li(b, p=None):
    return dict(kind="dle_electrodialysis_li", recovery={"Li": 0.85},
                reagent_kg_per_m3=0.05, kwh_per_m3=3.5,
                note="electro-driven DLE screening (literature analog, not field-calibrated)")


def nf_membrane(b, p=None):
    tds = b.tds()
    return dict(kind="nf_membrane", recovery={"Li": 0.8, "Br": 0.75, "B": 0.6},
                reagent_kg_per_m3=0.05, kwh_per_m3=round(0.8 + tds / 1e5, 2),
                note="monovalent-selective NF screening (passage×yield conflated — see PROCESS.md)")


def ro_concentration(b, p=None):
    tds = b.tds()
    return dict(kind="ro_concentration", recovery={"Li": 0.95, "Br": 0.95, "Sr": 0.95, "K": 0.95},
                reagent_kg_per_m3=0.02, kwh_per_m3=round(2.5 + tds / 5e4, 2),
                note="RO concentration screening (passage×yield conflated)")


def electrochemical_br(b, p=None):
    return dict(kind="electrochemical_br", recovery={"Br": 0.9},
                reagent_kg_per_m3=0.02, kwh_per_m3=1.1,
                note="electrochemical Br screening (Zhou 2026 analog)")


def precipitation_sr(b, p=None):
    return dict(kind="precipitation_sr", recovery={"Sr": 0.8},
                reagent_kg_per_m3=0.5, kwh_per_m3=0.4, note="carbonate precipitation of Sr (screening)")


def k_recovery(b, p=None):
    return dict(kind="k_recovery", recovery={"K": 0.7},
                reagent_kg_per_m3=0.1, kwh_per_m3=1.5, note="KCl crystallization screening")


def b_recovery(b, p=None):
    return dict(kind="b_recovery", recovery={"B": 0.75},
                reagent_kg_per_m3=0.2, kwh_per_m3=0.6, note="boron-selective sorption screening")


def li_carbonate_finish(b, p=None):
    return dict(kind="li_carbonate_finish", recovery={"Li": 0.97},
                reagent_kg_per_m3=0.6, kwh_per_m3=0.9,
                note="Na2CO3 -> Li2CO3 conversion proxy — NOT battery-grade certification")


UNIT_LIBRARY = {
    "desulfurization": desulfurization, "softening": softening,
    "mg_rejection_ec": mg_rejection_ec, "evaporation_concentration": evaporation_concentration,
    "dle_sorption_li": dle_sorption_li, "dle_solvent_extraction_li": dle_solvent_extraction_li,
    "dle_electrodialysis_li": dle_electrodialysis_li, "nf_membrane": nf_membrane,
    "ro_concentration": ro_concentration, "electrochemical_br": electrochemical_br,
    "precipitation_sr": precipitation_sr, "k_recovery": k_recovery,
    "b_recovery": b_recovery, "li_carbonate_finish": li_carbonate_finish,
}


def evaluate_flowsheet(b: Brine, units):
    """Evaluate a chain with state propagation and a component mass ledger.

    Removal operations alter the downstream brine state (critical for Mg/Li).
    Recovery is a fraction of the original feed mass (cannot silently create product).
    Removed ions are tracked as waste_removed_kg_yr (not product).
    Screening model: no detailed hydraulics or thermodynamic equilibrium solver.
    """
    import copy
    b.validate()
    state = copy.deepcopy(b)
    state.preconcentrate = 1.0
    overall, reagent, energy, notes = {}, 0.0, 0.0, []
    removed_frac = {}
    for u in units:
        if u not in UNIT_LIBRARY:
            raise ValueError(f"unknown unit: {u}")
        res = UNIT_LIBRARY[u](state)
        for ion, frac in res.get("recovery", {}).items():
            frac = float(frac)
            if not (0.0 <= frac <= 1.0) or not math.isfinite(frac):
                raise ValueError(f"recovery out of [0,1] for {ion} in {u}: {frac}")
            overall[ion] = overall.get(ion, 1.0) * frac if ion in overall else frac
            if overall[ion] > 1.0 + 1e-9:
                raise ValueError(f"cumulative recovery >1 for {ion}")
        for ion, frac in res.get("remove", {}).items():
            frac = min(1.0, max(0.0, float(frac)))
            before = state.ions.get(ion, 0.0)
            state.ions[ion] = before * (1.0 - frac)
            removed_frac[ion] = 1.0 - (1.0 - removed_frac.get(ion, 0.0)) * (1.0 - frac)
        concentrate = float(res.get("concentrate", 1.0))
        if concentrate != 1.0:
            if concentrate <= 0 or not math.isfinite(concentrate):
                raise ValueError(f"invalid concentrate factor: {concentrate}")
            state.ions = {i: v * concentrate for i, v in state.ions.items()}
            state.flow = state.flow / concentrate
            state.preconcentrate = float(state.preconcentrate) * concentrate
        reagent += res["reagent_kg_per_m3"]
        energy += res["kwh_per_m3"]
        notes.append(f"{u}: {res['note']}")
    days = 330
    feed_kg_yr = {i: b.ions.get(i, 0.0) * b.flow * 1000.0 * days / 1e6 for i in b.ions}
    recovered_kg_yr = {i: feed_kg_yr.get(i, 0.0) * r for i, r in overall.items()}
    waste_removed_kg_yr = {i: feed_kg_yr.get(i, 0.0) * f for i, f in removed_frac.items()}
    residual_kg_yr = {
        i: max(0.0, feed_kg_yr.get(i, 0.0) - recovered_kg_yr.get(i, 0.0) - waste_removed_kg_yr.get(i, 0.0))
        for i in feed_kg_yr
    }
    closure = {
        i: round(
            recovered_kg_yr.get(i, 0.0) + residual_kg_yr.get(i, 0.0) + waste_removed_kg_yr.get(i, 0.0) - feed_kg_yr[i],
            6,
        )
        for i in feed_kg_yr
    }
    return dict(
        units=list(units),
        recovery={k: round(v, 3) for k, v in overall.items()},
        reagent_kg_per_m3=round(reagent, 3),
        kwh_per_m3=round(energy, 3),
        mass_balance={
            "feed_kg_yr": {k: round(v, 2) for k, v in feed_kg_yr.items()},
            "recovered_kg_yr": {k: round(v, 2) for k, v in recovered_kg_yr.items()},
            "waste_removed_kg_yr": {k: round(v, 2) for k, v in waste_removed_kg_yr.items()},
            "residual_kg_yr": {k: round(v, 2) for k, v in residual_kg_yr.items()},
            "closure_kg_yr": closure,
            "note": (
                "algebraic ledger invariant: feed ≈ recovered + waste_removed + residual; "
                "near-zero closure proves bookkeeping, NOT independent physical model accuracy"
            ),
        },
        notes=notes,
        evidence_grade="screening_synthetic",
    )
