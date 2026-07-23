from brinevalue.chemistry import Brine, ionic_balance
from brinevalue.optimizer import screen, pareto_front, recommend, CANDIDATES
from brinevalue.pipeline import analyze

def _rich():
    return Brine(
        ions=dict(Na=20000, Cl=35000, Ca=4000, Mg=800, Li=190, Br=250, Sr=900, K=4000, B=500, SO4=400, HCO3=300),
        flow=4000,
        unc={"Li": 0.3, "Mg": 0.25, "Br": 0.3, "flow": 0.2},
    )

def _poor():
    return Brine(
        ions=dict(Na=20000, Cl=35000, Ca=25000, Mg=9000, Li=15, Br=40, Sr=60, K=300, B=80, SO4=500, HCO3=200),
        flow=300,
        unc={"Li": 0.3, "flow": 0.2},
    )

def test_candidate_count():
    assert len(CANDIDATES) >= 8

def test_screen_ranked():
    rows = screen(_rich())
    assert rows[0]["npv_rub"] >= rows[-1]["npv_rub"]

def test_pareto_nonempty():
    assert len(pareto_front(screen(_rich()))) >= 1

def test_rich_not_nogo():
    assert recommend(_rich())["decision"] != "no_go"

def test_poor_is_nogo():
    assert recommend(_poor())["decision"] == "no_go"

def test_decision_in_set():
    assert recommend(_rich())["decision"] in {"no_go", "lab", "pilot", "scale"}

def test_recommend_exposes_governance_fields():
    r = recommend(_rich())
    assert "raw_decision" in r and "sample_grade" in r and "robust" in r
    assert "quality_gate" in r and "si_meta" in r

def test_recommend_matches_analyze_decision():
    b = _rich()
    assert recommend(b)["decision"] == analyze(b, with_doe=False, with_scenarios=False)["decision"]

def test_bad_balance_cannot_scale():
    b = _rich()
    b.ions["Cl"] *= 3  # destroy charge balance
    assert ionic_balance(b)["balance_error_pct"] > 10
    r = recommend(b)
    assert r["decision"] in {"lab", "no_go"}
    assert r["decision"] != "scale"
    assert r["sample_grade"] == "non_decision_grade"

def test_severe_balance_is_nogo():
    b = _rich()
    b.ions["Cl"] *= 5
    assert ionic_balance(b)["balance_error_pct"] > 25
    assert recommend(b)["decision"] == "no_go"
