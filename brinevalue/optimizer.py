"""Enumerate candidate flowsheets, TEA, Pareto, and governed recommendations.

`recommend()` always applies QC + uncertainty governance. NPV-only thresholds
are exposed as `raw_decision` and must not be used alone for pilot/scale.
"""
from .process import evaluate_flowsheet
from .economics import economics

CANDIDATES = {
    "Li_sorption": ["desulfurization", "softening", "dle_sorption_li", "li_carbonate_finish"],
    "Li_solvent": ["desulfurization", "softening", "dle_solvent_extraction_li", "li_carbonate_finish"],
    "Li_electro": ["desulfurization", "mg_rejection_ec", "dle_electrodialysis_li", "li_carbonate_finish"],
    "Li_membrane": ["desulfurization", "softening", "nf_membrane", "ro_concentration", "li_carbonate_finish"],
    "Br_electro": ["desulfurization", "electrochemical_br"],
    "Sr_precip": ["desulfurization", "softening", "precipitation_sr"],
    "LiBr_combo": ["desulfurization", "softening", "nf_membrane", "electrochemical_br", "li_carbonate_finish"],
    "FullComponent": [
        "desulfurization", "softening", "evaporation_concentration", "nf_membrane",
        "electrochemical_br", "k_recovery", "b_recovery", "precipitation_sr", "li_carbonate_finish",
    ],
}
# FullComponent: multi-product screening chain via NF Li passage + finish;
# not a complete industrial multi-DLE topology (no dedicated Li-selective extraction unit).

SCHEME_STABILITY_MIN = 0.60


def screen(brine, prices=None):
    rows = []
    for name, units in CANDIDATES.items():
        fs = evaluate_flowsheet(brine, units)
        ec = economics(brine, fs, prices)
        rows.append(dict(scheme=name, **fs, **ec))
    rows.sort(key=lambda r: r["npv_rub"], reverse=True)
    return rows


def _dominated(a, b):
    ge = b["npv_rub"] >= a["npv_rub"] and b["capex_rub"] <= a["capex_rub"] and b["opex_rub_yr"] <= a["opex_rub_yr"]
    gt = b["npv_rub"] > a["npv_rub"] or b["capex_rub"] < a["capex_rub"] or b["opex_rub_yr"] < a["opex_rub_yr"]
    return ge and gt


def pareto_front(rows):
    return [a for a in rows if not any(_dominated(a, b) for b in rows if b is not a)]


def _npv_decision(npv: float) -> str:
    if npv <= 0:
        return "no_go"
    if npv < 5e7:
        return "lab"
    if npv < 3e8:
        return "pilot"
    return "scale"


def govern_decision(raw_decision, qc, qgate, robust):
    """Map NPV-raw decision through sample QC, P(NPV>0), and scheme stability.

    Under screening_placeholder TEA, governed output never returns ``scale``:
    high NPV maps at most to ``pilot`` (candidate for pilot *design*), not
    investment-grade scale-up authorization.
    """
    decision = raw_decision
    bal = qc.get("balance_error_pct")
    bal_f = float(bal) if bal is not None else 999.0
    if qc.get("reject_sample") or bal_f > 25.0:
        return "no_go", "non_decision_grade"
    if bal_f > 10.0 or not qgate.get("pass", False):
        if decision in ("pilot", "scale", "lab"):
            decision = "lab"
        sample_grade = "non_decision_grade"
    else:
        sample_grade = "decision_grade"
    p = float(robust.get("p_npv_positive", 0.0))
    if p < 0.25:
        decision = "no_go"
    elif p < 0.75 and decision in ("pilot", "scale"):
        decision = "lab"
    # Scheme instability: do not pilot/scale if best scheme flips often
    stab = robust.get("scheme_stability") or {}
    top_share = max(stab.values()) if stab else 1.0
    if top_share < SCHEME_STABILITY_MIN and decision in ("pilot", "scale"):
        decision = "lab"
        sample_grade = "non_decision_grade" if sample_grade == "decision_grade" else sample_grade
    # Placeholder TEA must not authorize industrial scale-up.
    if decision == "scale":
        decision = "pilot"
    return decision, sample_grade


def recommend(brine, prices=None, n_robust=200, seed=42):
    """Governed recommendation (advisory). Always prefer this over NPV-only logic."""
    from .chemistry import ionic_balance, scaling_risk
    from .quality import quality_gate
    from .uncertainty import robust_screen
    from .economics import tea_scenarios

    rows = screen(brine, prices)
    pareto = pareto_front(rows)
    # Prefer highest-NPV Pareto member when available; else overall NPV rank.
    best = max(pareto, key=lambda r: r["npv_rub"]) if pareto else rows[0]
    raw_decision = _npv_decision(best["npv_rub"])
    qc = ionic_balance(brine)
    si, flags, si_meta = scaling_risk(brine)
    scaling_for_gate = flags if si_meta.get("si_reliable") else None
    qgate = quality_gate(brine, best, qc, scaling_for_gate)
    if not si_meta.get("si_reliable", False):
        qgate = {
            **qgate,
            "warnings": list(qgate.get("warnings", [])) + ["davies_si_unreliable_I_gt_0.5"],
        }
    robust = robust_screen(brine, prices, n=n_robust, seed=seed)
    decision, sample_grade = govern_decision(raw_decision, qc, qgate, robust)
    return dict(
        decision=decision,
        raw_decision=raw_decision,
        sample_grade=sample_grade,
        best=best,
        pareto=pareto,
        ranked=rows,
        qc=qc,
        quality_gate=qgate,
        robust=robust,
        scaling_index=si,
        scaling_risk=flags,
        si_meta=si_meta,
        tea_scenarios=tea_scenarios(brine, best),
        selection_note="best = max NPV on Pareto front; decision still governed by QC+P(NPV>0)+stability",
        decision_note=(
            "governed decision capped at pilot under screening_placeholder TEA; "
            "raw_decision may still show scale from NPV thresholds alone"
        ),
    )
