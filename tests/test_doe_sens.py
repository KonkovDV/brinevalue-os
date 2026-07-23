from brinevalue.chemistry import Brine
from brinevalue.doe import propose_experiments
from brinevalue.sensitivity import sensitivity
def _b():
    return Brine(ions=dict(Na=20000,Cl=35000,Ca=4000,Mg=1500,Li=150,Br=200,Sr=800,K=3000,B=300),flow=3000,
                 unc={"Li":0.3,"Mg":0.25,"Br":0.3,"Sr":0.3,"K":0.3,"B":0.3,"flow":0.2})
def test_doe_plan_len(): assert len(propose_experiments(_b(),k=4,n=50)["plan"])==4
def test_doe_reduces_variance():
    p=propose_experiments(_b(),k=4,n=60); assert p["plan"][-1]["npv_std_after"]<=p["base_npv_std"]
def test_sensitivity_fields(): assert len(sensitivity(_b())["elasticity"])>=5
