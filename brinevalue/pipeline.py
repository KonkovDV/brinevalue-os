"""One-call analysis: QC -> scaling -> governed screen -> sensitivity -> DoE."""
from .chemistry import mg_li_ratio
from .optimizer import recommend
from .sensitivity import sensitivity
from .doe import propose_experiments
from .economics import price_scenarios
from .bayes import calibrate_units
from .industrix import assess as assess_industrix


def analyze(brine, prices=None, with_doe=True, with_scenarios=True, lab_observations=None):
    rec = recommend(brine, prices)
    posterior = calibrate_units(lab_observations) if lab_observations else {}
    industrix = assess_industrix()
    out = dict(
        stream=brine.name,
        qc=rec["qc"],
        mg_li=round(mg_li_ratio(brine), 2),
        scaling_index=rec["scaling_index"],
        scaling_risk=rec["scaling_risk"],
        si_meta=rec["si_meta"],
        quality_gate=rec["quality_gate"],
        robust=rec["robust"],
        sample_grade=rec["sample_grade"],
        posterior=posterior,
        industrix=industrix,
        decision=rec["decision"],
        raw_decision=rec["raw_decision"],
        best=rec["best"],
        pareto=rec["pareto"],
        ranked=rec["ranked"],
        sensitivity=sensitivity(brine, prices),
    )
    if with_doe:
        out["experiment_plan"] = propose_experiments(brine, prices, k=4, n=120)
    if with_scenarios:
        out["price_scenarios"] = price_scenarios(brine, rec["best"])
    return out
