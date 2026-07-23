"""Adversarial / red-team audit suite for BrineValue OS.

Run: python -m benchmark.redteam
Exit 0 if all checks pass; non-zero on failure.
Does not invent field data — synthetic attacks only.
"""
from __future__ import annotations

import copy
import math
import sys
import traceback

from brinevalue.chemistry import Brine, ionic_balance, scaling_risk
from brinevalue.economics import economics, PRODUCT_PRICE
from brinevalue.optimizer import recommend, screen, pareto_front
from brinevalue.process import evaluate_flowsheet
from brinevalue.pipeline import analyze
from brinevalue.report import html_report


def _base(**kw):
    ions = dict(
        Na=20000, Cl=35000, Ca=4000, Mg=800, Li=190, Br=250, Sr=900,
        K=4000, B=500, SO4=400, HCO3=300, Ba=40, I=20,
    )
    ions.update(kw.pop("ions_override", {}))
    return Brine(ions=ions, flow=kw.pop("flow", 4000), unc={"Li": 0.3, "flow": 0.2}, **kw)


def _expect(cond, msg, failures):
    if not cond:
        failures.append(msg)


def run():
    failures = []
    # Negative / non-finite inputs
    for bad in (
        dict(ions_override={"Li": -1}),
        dict(flow=-10),
        dict(ph=15),
        dict(temp=999),
        dict(ions_override={"Li": float("nan")}),
        dict(ions_override={"Na": float("inf")}),
        dict(org=-5),
    ):
        try:
            b = _base(**bad)
            b.validate()
            failures.append(f"validate should reject {bad}")
        except ValueError:
            pass

    # Zero flow: validate OK, quality fails
    z = _base(flow=0)
    z.validate()
    r = recommend(z, n_robust=20)
    _expect(r["decision"] in {"no_go", "lab"}, "zero flow must not scale", failures)

    # Empty / single ion
    try:
        Brine(ions={}, flow=100).validate()
        ionic_balance(Brine(ions={}, flow=100))
    except Exception:
        pass
    one = Brine(ions={"Li": 100}, flow=1000)
    qc = ionic_balance(one)
    _expect(qc["reject_sample"] or not qc["decision_grade"], "single-ion not decision-grade", failures)

    # Unbalanced
    bad_bal = _base(ions_override={"Cl": 200000})
    _expect(ionic_balance(bad_bal)["balance_error_pct"] > 10, "expected bad balance", failures)
    _expect(recommend(bad_bal, n_robust=20)["decision"] != "scale", "bad balance cannot scale", failures)

    # Extreme TDS / hypersaline SI
    hi = _base()
    si, flags, meta = scaling_risk(hi)
    _expect(meta["si_reliable"] is False, "hypersaline SI must be unreliable", failures)
    _expect(all(v is None for v in si.values()), "SI None when unreliable", failures)

    # Mg/Li = 0, Li = 0
    m0 = _base(ions_override={"Mg": 0})
    from brinevalue.chemistry import mg_li_ratio
    _expect(mg_li_ratio(m0) == 0.0, "Mg/Li=0", failures)
    l0 = _base(ions_override={"Li": 0})
    fs = evaluate_flowsheet(l0, ["dle_sorption_li"])
    _expect(fs["recovery"].get("Li", 0) >= 0, "Li=0 recovery non-negative", failures)

    # Recovery bounds
    fs = evaluate_flowsheet(_base(), ["dle_sorption_li", "li_carbonate_finish"])
    for ion, rec in fs["recovery"].items():
        _expect(0 <= rec <= 1, f"recovery bound {ion}={rec}", failures)
    _expect(max(abs(x) for x in fs["mass_balance"]["closure_kg_yr"].values()) < 1e-6, "mass closure", failures)

    # Economics guards
    fs = evaluate_flowsheet(_base(), ["dle_sorption_li", "li_carbonate_finish"])
    try:
        economics(_base(), fs, prices={"Li": -1})
        failures.append("negative price must raise")
    except ValueError:
        pass
    try:
        economics(_base(), fs, years=0)
        failures.append("years=0 must raise")
    except ValueError:
        pass
    ec = economics(_base(), fs, prices={"Li": 0})
    _expect(ec["irr"] == "not_implemented", "IRR not implemented label", failures)
    _expect(ec["economics_grade"] == "screening_placeholder", "econ grade", failures)

    # Pareto dominance-free
    rows = screen(_base())
    front = pareto_front(rows)
    for a in front:
        for b in front:
            if a is b:
                continue
            dom = (
                b["npv_rub"] >= a["npv_rub"]
                and b["capex_rub"] <= a["capex_rub"]
                and b["opex_rub_yr"] <= a["opex_rub_yr"]
                and (
                    b["npv_rub"] > a["npv_rub"]
                    or b["capex_rub"] < a["capex_rub"]
                    or b["opex_rub_yr"] < a["opex_rub_yr"]
                )
            )
            _expect(not dom, "Pareto member dominated", failures)

    # HTML report must not crash on hypersaline (SI None)
    res = analyze(_base(name="synthetic_redteam"), with_doe=False, with_scenarios=False)
    html = html_report(res, _base(name="synthetic_redteam"))
    _expect("v0.5.2" in html and "СИНТЕТИЧЕСКИЕ" in html, "report banners", failures)

    # Worst-case red-team economic overlays (decision must not freely scale)
    attacks = []
    base = _base()
    # Li low
    a = copy.deepcopy(base); a.ions["Li"] = 15; attacks.append(("low_Li", a))
    # flow half
    a = copy.deepcopy(base); a.flow = base.flow / 2; attacks.append(("half_flow", a))
    # high organics
    a = copy.deepcopy(base); a.org = 6000; attacks.append(("high_org", a))
    # high Mg/Li
    a = copy.deepcopy(base); a.ions["Mg"] = 20000; attacks.append(("high_Mg", a))
    # bad balance
    a = copy.deepcopy(base); a.ions["Cl"] *= 4; attacks.append(("bad_balance", a))
    for name, brine in attacks:
        d = recommend(brine, n_robust=30)["decision"]
        _expect(d in {"no_go", "lab", "pilot", "scale"}, f"attack {name} decision set", failures)
        if name in {"bad_balance", "high_org"}:
            _expect(d != "scale", f"attack {name} must not scale", failures)

    # Evaporation changes DLE recovery vs no evaporation
    b = _base()
    r1 = evaluate_flowsheet(b, ["dle_sorption_li"])["recovery"]["Li"]
    r2 = evaluate_flowsheet(b, ["evaporation_concentration", "dle_sorption_li"])["recovery"]["Li"]
    _expect(r2 >= r1, f"evaporation should not lower DLE recovery ({r1} -> {r2})", failures)

    print(f"REDTEAM: {len(failures)} failures")
    for f in failures:
        print("FAIL:", f)
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
