from brinevalue.chemistry import Brine
from brinevalue.process import UNIT_LIBRARY, evaluate_flowsheet
def _b(mg=1500):
    return Brine(ions=dict(Na=20000,Cl=35000,Ca=5000,Mg=mg,Li=120,Br=200,Sr=600,K=2000,B=300),flow=2000)
def test_library_size(): assert len(UNIT_LIBRARY)>=14
def test_flowsheet_recovery_bounded():
    fs=evaluate_flowsheet(_b(),["desulfurization","softening","dle_sorption_li","li_carbonate_finish"])
    assert 0<fs["recovery"]["Li"]<=1
def test_high_mgli_lowers_recovery():
    lo=evaluate_flowsheet(_b(400),["dle_sorption_li"])["recovery"]["Li"]
    hi=evaluate_flowsheet(_b(6000),["dle_sorption_li"])["recovery"]["Li"]
    assert lo>hi
def test_solvent_more_mg_tolerant():
    r_sorp=evaluate_flowsheet(_b(8000),["dle_sorption_li"])["recovery"]["Li"]
    r_solv=evaluate_flowsheet(_b(8000),["dle_solvent_extraction_li"])["recovery"]["Li"]
    assert r_solv>=r_sorp
def test_full_component_recovers_multi():
    fs=evaluate_flowsheet(_b(),["desulfurization","softening","evaporation_concentration","nf_membrane","electrochemical_br","k_recovery","b_recovery","precipitation_sr","li_carbonate_finish"])
    assert set(["Li","Br","K","B","Sr"]) <= set(fs["recovery"])
def test_energy_accumulates():
    assert evaluate_flowsheet(_b(),["softening","ro_concentration"])["kwh_per_m3"]>0
