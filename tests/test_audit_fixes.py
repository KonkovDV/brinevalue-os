"""Regression tests for INDUSTRIX audit v0.5.2 fixes."""
import math
from brinevalue.chemistry import Brine, ionic_balance, scaling_risk
from brinevalue.economics import economics
from brinevalue.process import evaluate_flowsheet
from brinevalue.pipeline import analyze
from brinevalue.report import html_report
from brinevalue.optimizer import recommend
from brinevalue.doe import propose_experiments


def _b(**kw):
    ions = dict(
        Na=20000, Cl=35000, Ca=4000, Mg=800, Li=190, Br=250, Sr=900,
        K=4000, B=500, SO4=400, HCO3=300,
    )
    return Brine(ions=ions, flow=4000, unc={"Li": 0.3, "flow": 0.2}, name="synthetic_audit", **kw)


def test_nan_concentration_rejected():
    try:
        Brine(ions={"Li": float("nan")}, flow=1000).validate()
        assert False
    except ValueError:
        pass


def test_report_handles_unreliable_si():
    b = _b()
    res = analyze(b, with_doe=False, with_scenarios=False)
    html = html_report(res, b)
    assert "v0.5.2" in html
    assert "СИНТЕТИЧЕСКИЕ" in html
    assert "n/a" in html or "не decision-grade" in html


def test_evaporation_boosts_dle_recovery():
    b = _b()
    r0 = evaluate_flowsheet(b, ["dle_sorption_li"])["recovery"]["Li"]
    r1 = evaluate_flowsheet(b, ["evaporation_concentration", "dle_sorption_li"])["recovery"]["Li"]
    assert r1 > r0


def test_waste_removed_in_mass_ledger():
    fs = evaluate_flowsheet(_b(), ["desulfurization", "dle_sorption_li"])
    assert "waste_removed_kg_yr" in fs["mass_balance"]
    assert fs["mass_balance"]["waste_removed_kg_yr"].get("SO4", 0) > 0
    assert max(abs(x) for x in fs["mass_balance"]["closure_kg_yr"].values()) < 1e-6


def test_negative_price_rejected():
    fs = evaluate_flowsheet(_b(), ["dle_sorption_li", "li_carbonate_finish"])
    try:
        economics(_b(), fs, prices={"Li": -10})
        assert False
    except ValueError:
        pass


def test_doe_not_labeled_bayesian_opt():
    plan = propose_experiments(_b(), k=2, n=40)
    assert plan["bayesian_optimization"] is False
    assert plan["method"] == "greedy_uncertainty_reduction"


def test_posterior_diagnostic_only():
    r = analyze(
        _b(),
        with_doe=False,
        with_scenarios=False,
        lab_observations=[{"unit": "dle_sorption_li", "ion": "Li", "recovery": 0.7}],
    )
    assert r["posterior_role"] == "diagnostic_only_not_applied_to_tea"
    assert r["posterior"]


def test_severe_organics_blocks_scale():
    b = _b(org=6000)
    assert recommend(b, n_robust=40)["decision"] != "scale"


def test_governed_never_returns_scale_under_placeholder_tea():
    """Even rich streams: governed decision capped at pilot while TEA is placeholder."""
    b = _b()
    r = recommend(b, n_robust=40)
    assert r["decision"] in {"no_go", "lab", "pilot"}
    assert r["decision"] != "scale"
    assert "decision_note" in r


def test_doe_reports_std_reduction_field():
    plan = propose_experiments(_b(), k=2, n=40)
    assert plan["process_batch_doe"] is False
    assert "npv_std_reduction_rub" in plan["plan"][0]
