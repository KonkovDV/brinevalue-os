from brinevalue.chemistry import Brine
from brinevalue.process import evaluate_flowsheet
from brinevalue.bayes import posterior_recovery, calibrate_units
from brinevalue.pipeline import analyze

def b():
 return Brine(ions=dict(Na=25000,Cl=45000,Ca=4000,Mg=1000,Li=170,Br=800,Sr=900,Ba=60,SO4=600,HCO3=500,K=900),flow=3500,unc={"Li":.2,"Br":.2,"flow":.15})
def test_mass_balance_closure():
 fs=evaluate_flowsheet(b(),["dle_sorption_li","li_carbonate_finish"])
 assert max(abs(x) for x in fs["mass_balance"]["closure_kg_yr"].values()) < 1e-6
def test_state_propagation_changes_mgli():
 fs1=evaluate_flowsheet(b(),["dle_sorption_li"])
 fs2=evaluate_flowsheet(b(),["softening","dle_sorption_li"])
 assert fs2["recovery"]["Li"] >= fs1["recovery"]["Li"]
def test_beta_posterior():
 r=posterior_recovery([{"recovery":.8},{"recovery":.9},{"recovery":.85}])
 assert .60 < r["mean"] < .7 and len(r["interval95"])==2
def test_lab_calibration_groups():
 r=calibrate_units([{"unit":"dle_sorption_li","ion":"Li","recovery":.8},{"unit":"dle_sorption_li","ion":"Li","recovery":.9}])
 assert "dle_sorption_li::Li" in r
def test_governance_demotes_bad_qc():
 r=analyze(b(),with_doe=False); assert r["decision"] in {"no_go","lab","pilot"}; assert r["decision"] != "scale"


def test_input_validation_negative_and_ranges():
 from brinevalue.chemistry import ionic_balance
 bad=Brine(ions={"Li":-1},flow=1000)
 try: ionic_balance(bad); assert False
 except ValueError: pass
 bad=Brine(ions={},flow=1000,ph=15)
 try: ionic_balance(bad); assert False
 except ValueError: pass

def test_economics_revenue_components_close():
 from brinevalue.optimizer import screen
 from brinevalue.economics import economics
 r=screen(b())[0]; ec=economics(b(),r)
 assert abs(sum(ec["revenue_components_rub_yr"].values())-ec["revenue_rub_yr"]) <= 1
