from brinevalue.io import synthetic_streams
from brinevalue.calibrate import calibrate_recovery, apply_correction
from brinevalue.pipeline import analyze
def test_synthetic_count(): assert len(synthetic_streams(8))==8
def test_synthetic_has_kb():
    b=synthetic_streams(4)[0]; assert "K" in b.ions and "B" in b.ions
def test_analyze_end_to_end():
    r=analyze(synthetic_streams(4)[0]); assert "decision" in r and "price_scenarios" in r
def test_calibrate_factor():
    assert calibrate_recovery([dict(unit="dle_sorption_li",ion="Li",predicted=0.8,observed=0.6)])[("dle_sorption_li","Li")]==0.75
def test_apply_correction():
    assert apply_correction({"Li":0.8},{("dle_sorption_li","Li"):0.75})["Li"]==0.6
