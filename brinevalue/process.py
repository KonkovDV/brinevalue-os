"""Library of transparent unit operations for full-component recovery.

Evidence base (July 2026):
- Desulfurization + softening pretreatment mirrors the world-first 100 m3/d
  Li/K/Br/B industrial project (Chen et al., Desalination & Water Treatment 2025).
- Manganese-based sorbent DLE with Mg/Li penalty: YQ station field test
  (Miao et al., SPE 2024: hardness>20000, Mg~1200, Li~150 mg/L); adsorbent
  capacity up to 42 mg/g, selectivity alpha>25 (Disu et al., SPE 2025).
- Electrochemical Mg rejection: >99.98% Mg2+ rejection (Zhang et al., EST 2026).
- Chlorine-free electrochemical Br: zero-gap electrolyzer, >90% Br oxidation in
  12 min (Zhou et al., Materials 2026) - greener than Cl2 stripping.
- Solvent extraction / adsorption / NF+MD-crystallization TEA comparison
  (Nikfar et al., ACS Sust. Res. Manag. 2026).
- Evaporative pre-concentration raises halite SI and boosts DLE
  (Alshammari et al., SPE 2026).
Each unit returns recovery per element, reagent kg/m3, energy kWh/m3, note.
Correlations are screening-grade and frozen in docs/PROCESS.md.
"""
from .chemistry import Brine, mg_li_ratio


def desulfurization(b, p=None):
    # removes sulfate/H2S + hydrocarbons; protects sorbent, enables downstream
    return dict(kind="desulfurization", recovery={}, remove={"SO4": 0.7},
                reagent_kg_per_m3=0.15, kwh_per_m3=0.2,
                note="desulfur + de-oiling pretreatment (Chen 2025 industrial case)")


def softening(b, p=None):
    hardness = b.molar("Ca") + b.molar("Mg")
    return dict(kind="softening", recovery={}, remove={"Ca": 0.9, "Mg": 0.85, "Ba": 0.8},
                reagent_kg_per_m3=round(0.06 * hardness * 1000, 3), kwh_per_m3=0.3,
                note="lime-soda softening protects sorbent/membrane")


def mg_rejection_ec(b, p=None):
    # electrochemical Mg(OH)2 coproduction, >99.98% Mg rejection (Zhang EST 2026)
    return dict(kind="mg_rejection_ec", recovery={}, remove={"Mg": 0.999},
                reagent_kg_per_m3=0.0, kwh_per_m3=2.0,
                note=">99.98% Mg rejection, Mg(OH)2 coproduct, no reagent (Zhang 2026)")


def evaporation_concentration(b, p=None):
    # progressive evaporation raises halite SI, concentrates target ions ~3x
    return dict(kind="evaporation_concentration", recovery={}, concentrate=3.0,
                reagent_kg_per_m3=0.0, kwh_per_m3=8.0,
                note="pre-concentration boosts DLE, halite recovery (Alshammari 2026)")


def dle_sorption_li(b, p=None):
    # manganese-based sorbent; recovery penalized by Mg/Li and hardness
    r = mg_li_ratio(b)
    rec = max(0.35, 0.90 - min(0.5, max(0.0, (r - 3) * 0.03)))
    return dict(kind="dle_sorption_li", recovery={"Li": round(rec, 3)},
                reagent_kg_per_m3=0.4, kwh_per_m3=1.2,
                note=f"Mn-sorbent ~42 mg/g, Mg/Li={r:.1f} (Miao 2024, Disu 2025)")


def dle_solvent_extraction_li(b, p=None):
    # solvent extraction: less Mg-sensitive, higher reagent cost (Nikfar 2026)
    r = mg_li_ratio(b)
    rec = max(0.5, 0.88 - min(0.35, max(0.0, (r - 6) * 0.02)))
    return dict(kind="dle_solvent_extraction_li", recovery={"Li": round(rec, 3)},
                reagent_kg_per_m3=0.9, kwh_per_m3=0.8,
                note="solvent extraction, tolerant to Mg/Li (Nikfar 2026)")


def dle_electrodialysis_li(b, p=None):
    # electro-driven DLE (Park 2025 review; Kong Nat Commun 2025)
    return dict(kind="dle_electrodialysis_li", recovery={"Li": 0.85},
                reagent_kg_per_m3=0.05, kwh_per_m3=3.5,
                note="electro-driven DLE, low reagent, higher energy (Kong 2025)")


def nf_membrane(b, p=None):
    tds = b.tds()
    return dict(kind="nf_membrane", recovery={"Li": 0.8, "Br": 0.75, "B": 0.6},
                reagent_kg_per_m3=0.05, kwh_per_m3=round(0.8 + tds / 1e5, 2),
                note="monovalent-selective NF, rejects divalent scale-formers")


def ro_concentration(b, p=None):
    tds = b.tds()
    return dict(kind="ro_concentration", recovery={"Li": 0.95, "Br": 0.95, "Sr": 0.95, "K": 0.95},
                reagent_kg_per_m3=0.02, kwh_per_m3=round(2.5 + tds / 5e4, 2),
                note="RO concentration, energy grows with TDS")


def electrochemical_br(b, p=None):
    # chlorine-free zero-gap electrolyzer, >90% Br oxidation (Zhou 2026)
    return dict(kind="electrochemical_br", recovery={"Br": 0.9},
                reagent_kg_per_m3=0.02, kwh_per_m3=1.1,
                note="chlorine-free electrochemical Br, >90% in 12 min (Zhou 2026)")


def precipitation_sr(b, p=None):
    return dict(kind="precipitation_sr", recovery={"Sr": 0.8},
                reagent_kg_per_m3=0.5, kwh_per_m3=0.4, note="carbonate precipitation of Sr")


def k_recovery(b, p=None):
    # potash-style crystallization from concentrated brine
    return dict(kind="k_recovery", recovery={"K": 0.7},
                reagent_kg_per_m3=0.1, kwh_per_m3=1.5, note="KCl crystallization")


def b_recovery(b, p=None):
    # boron sorption / extraction
    return dict(kind="b_recovery", recovery={"B": 0.75},
                reagent_kg_per_m3=0.2, kwh_per_m3=0.6, note="boron-selective sorption")


def li_carbonate_finish(b, p=None):
    return dict(kind="li_carbonate_finish", recovery={"Li": 0.97},
                reagent_kg_per_m3=0.6, kwh_per_m3=0.9, note="Na2CO3 -> Li2CO3 product")


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

    Removal operations alter the downstream brine state (critical for Mg/Li and
    scale-risk interactions). Recovery is tracked as a fraction of the original
    feed mass, so the ledger cannot silently create product. This remains a
    screening model: no detailed hydraulics or thermodynamic equilibrium solver.
    """
    import copy
    b.validate()
    state = copy.deepcopy(b)
    overall, reagent, energy, notes = {}, 0.0, 0.0, []
    for u in units:
        res = UNIT_LIBRARY[u](state)
        for ion, frac in res.get("recovery", {}).items():
            # sequential recovery fractions multiply for the same product;
            # distinct products remain independent fractions of feed.
            overall[ion] = overall.get(ion, 1.0) * frac if ion in overall else frac
        for ion, frac in res.get("remove", {}).items():
            state.ions[ion] = state.ions.get(ion, 0.0) * max(0.0, 1.0-frac)
        concentrate = res.get("concentrate", 1.0)
        if concentrate != 1.0:
            # concentration changes downstream selectivity but not feed mass;
            # flow is reduced to preserve mass continuity in the state.
            state.ions = {i: v*concentrate for i,v in state.ions.items()}
            state.flow = state.flow / concentrate
        reagent += res["reagent_kg_per_m3"]; energy += res["kwh_per_m3"]
        notes.append(f"{u}: {res['note']}")
    feed_kg_yr = {i: b.ions.get(i,0.0)*b.flow*1000.0*330/1e6 for i in b.ions}
    recovered_kg_yr = {i: feed_kg_yr.get(i,0.0)*r for i,r in overall.items()}
    residual_kg_yr = {i: max(0.0, feed_kg_yr.get(i,0.0)-recovered_kg_yr.get(i,0.0)) for i in feed_kg_yr}
    closure = {i: round(recovered_kg_yr.get(i,0.0)+residual_kg_yr.get(i,0.0)-feed_kg_yr[i], 6) for i in feed_kg_yr}
    return dict(units=list(units), recovery={k: round(v, 3) for k,v in overall.items()},
                reagent_kg_per_m3=round(reagent, 3), kwh_per_m3=round(energy, 3),
                mass_balance={"feed_kg_yr": {k: round(v,2) for k,v in feed_kg_yr.items()},
                              "recovered_kg_yr": {k: round(v,2) for k,v in recovered_kg_yr.items()},
                              "residual_kg_yr": {k: round(v,2) for k,v in residual_kg_yr.items()},
                              "closure_kg_yr": closure},
                notes=notes)
