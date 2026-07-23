from brinevalue.chemistry import Brine, ionic_balance, scaling_risk
from brinevalue.process import evaluate_flowsheet
from brinevalue.uncertainty import robust_screen
from brinevalue.quality import quality_gate

def b():
    return Brine(
        ions=dict(
            Na=25000, Cl=45000, Ca=4000, Mg=1000, Li=170, Br=800, Sr=900,
            Ba=60, SO4=600, HCO3=500, K=900,
        ),
        flow=3500,
        unc={"Li": 0.2, "Br": 0.2, "flow": 0.15},
    )

def test_robust_fields():
    r = robust_screen(b(), n=30)
    assert 0 <= r["p_npv_positive"] <= 1 and "scheme_stability" in r

def test_robust_reproducible():
    assert robust_screen(b(), n=25, seed=9) == robust_screen(b(), n=25, seed=9)

def test_quality_bad_balance():
    bb = b()
    bb.ions["Cl"] *= 2
    qc = ionic_balance(bb)
    si, flags, meta = scaling_risk(bb)
    scaling = flags if meta["si_reliable"] else None
    q = quality_gate(bb, qc=qc, scaling=scaling)
    assert q["pass"] is False
    assert q["sample_grade"] == "non_decision_grade"

def test_quality_product_screen():
    bb = b()
    fs = evaluate_flowsheet(bb, ["dle_sorption_li"])
    q = quality_gate(bb, fs, ionic_balance(bb), {})
    assert "Li2CO3_quality_screen" in q["product"]
