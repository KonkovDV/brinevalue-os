from brinevalue.chemistry import (
    Brine, ionic_balance, scaling_risk, davies_gamma, mg_li_ratio, DAVIES_VALID_I_MAX,
)

def _b():
    # Dilute enough that Davies remains decision-grade (I <= 0.5).
    return Brine(
        ions=dict(
            Na=2000, Cl=3500, Ca=200, Mg=50, SO4=80, HCO3=50,
            Li=20, Br=30, Sr=40, Ba=5, K=100, B=30, I=5,
        ),
        flow=2000,
    )

def _hypersaline():
    return Brine(
        ions=dict(
            Na=20000, Cl=35000, Ca=5000, Mg=1500, SO4=800, HCO3=500,
            Li=120, Br=200, Sr=600, Ba=50, K=2000, B=300, I=40,
        ),
        flow=2000,
    )

def test_tds_positive():
    assert _b().tds() > 0

def test_balance_fields():
    q = ionic_balance(_b())
    assert "balance_error_pct" in q and "ionic_strength" in q
    assert "decision_grade" in q

def test_ionic_strength_positive():
    assert _b().ionic_strength() > 0

def test_davies_below_one():
    assert 0 < davies_gamma(2, 0.5) < 1

def test_davies_monovalent_gt_divalent():
    assert davies_gamma(1, 0.5) > davies_gamma(2, 0.5)

def test_scaling_has_halite():
    si, flags, meta = scaling_risk(_b())
    assert "Halite" in si and len(si) == 5
    assert meta["si_reliable"] is True

def test_activity_lowers_si():
    b = _b()
    assert b.ionic_strength() <= DAVIES_VALID_I_MAX
    si, _, meta = scaling_risk(b)
    assert meta["si_reliable"] is True
    assert si["CaSO4"] is not None and si["CaSO4"] < 10

def test_hypersaline_si_not_decision_grade():
    si, flags, meta = scaling_risk(_hypersaline())
    assert meta["si_reliable"] is False
    assert meta["davies_valid"] is False
    assert all(v is None for v in si.values())
    assert all(v is False for v in flags.values())
    assert "si_transparency" in meta

def test_mg_li_ratio():
    assert mg_li_ratio(_b()) > 0
