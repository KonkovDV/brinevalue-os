from brinevalue.chemistry import Brine
from brinevalue.process import evaluate_flowsheet
from brinevalue.economics import economics, annual_product_kg, price_scenarios
def _b():
    return Brine(ions=dict(Na=20000,Cl=35000,Ca=5000,Mg=1200,Li=150,Br=200,Sr=800,K=3000,B=300),flow=3000)
def _fs(b): return evaluate_flowsheet(b,["dle_sorption_li","li_carbonate_finish"])
def test_product_scales_with_flow():
    b=_b(); a=annual_product_kg(b,_fs(b)); b.flow*=2; assert annual_product_kg(b,_fs(b))["Li"]>a["Li"]
def test_npv_and_new_fields():
    ec=economics(_b(),_fs(_b())); assert set(["npv_rub","roroi","prod_cost_usd_t","li2co3_t_yr"])<=set(ec)
def test_prod_cost_positive():
    ec=economics(_b(),_fs(_b())); assert ec["prod_cost_usd_t"] is None or ec["prod_cost_usd_t"]>0
def test_zero_li_zero_revenue():
    b=Brine(ions=dict(Na=20000,Cl=35000,Li=0),flow=1000)
    assert economics(b,_fs(b))["revenue_rub_yr"]==0
def test_price_scenarios_monotone():
    b=_b(); ps=price_scenarios(b,_fs(b)); assert ps[-1]["npv_rub"]>ps[0]["npv_rub"]
