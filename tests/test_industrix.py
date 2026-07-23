from brinevalue.industrix import assess, ReadinessInput, pilot_gates
from brinevalue.chemistry import Brine
from brinevalue.pipeline import analyze

def test_public_mvp_not_pilot_ready():
    r=assess(); assert r["honest_stage"]=="screening+lab-design" and len(r["blockers"])>=2
def test_full_gates_defined():
    assert len(pilot_gates())==7 and pilot_gates()[-1]["id"]=="G7"
def test_custom_pilot_ready():
    r=assess(ReadinessInput(has_real_data=True,has_lab_validation=True)); assert r["honest_stage"]=="pilot-ready"
def test_pipeline_exposes_industrix():
    b=Brine(ions={"Li":100,"Mg":1000,"Br":300,"Sr":400,"Na":20000,"Cl":35000},flow=1000)
    assert "industrix" in analyze(b,with_doe=False)
