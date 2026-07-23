"""Screens the synthetic cohort + checks sanity gates and trains the surrogate,
asserting it explains the physics model (R2 gate). CI red team, exit code.
"""
import sys, json
from brinevalue.io import synthetic_streams
from brinevalue.chemistry import Brine
from brinevalue.pipeline import analyze
from brinevalue.doe import propose_experiments
from brinevalue.surrogate import train_surrogate


def main():
    streams = synthetic_streams(24, seed=7)
    decisions = {}
    for b in streams:
        d = analyze(b, with_doe=False, with_scenarios=False)["decision"]
        decisions[d] = decisions.get(d, 0) + 1
    poor = Brine(ions=dict(Na=20000,Cl=35000,Ca=25000,Mg=9000,Li=10,Br=30,Sr=40,K=300,B=80),flow=250)
    poor_nogo = analyze(poor, with_doe=False, with_scenarios=False)["decision"] == "no_go"
    rich = Brine(ions=dict(Na=20000,Cl=35000,Ca=3000,Mg=600,Li=190,Br=250,Sr=1000,K=4500,B=500),flow=4000,
                 unc={"Li":0.3,"Mg":0.25,"Br":0.3,"Sr":0.3,"K":0.3,"B":0.3,"flow":0.2})
    rich_ok = analyze(rich, with_doe=False, with_scenarios=False)["decision"] != "no_go"
    p = propose_experiments(rich, k=4, n=100)
    doe_ok = p["plan"][-1]["npv_std_after"] <= p["base_npv_std"]
    sur = train_surrogate(n=250, seed=7)
    surrogate_ok = sur["cv_r2_mean"] >= 0.7
    m = dict(n_streams=len(streams), decisions=decisions, poor_is_nogo=poor_nogo,
             rich_not_nogo=rich_ok, doe_reduces_variance=doe_ok,
             surrogate_cv_r2=sur["cv_r2_mean"], surrogate_importances=sur["importances"])
    print(json.dumps(m, ensure_ascii=False, indent=2))
    ok = poor_nogo and rich_ok and doe_ok and surrogate_ok and sum(decisions.values()) == len(streams)
    print("GATES:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
