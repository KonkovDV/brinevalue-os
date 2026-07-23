"""INDUSTRIX readiness layer.

Maps the product to the public program pattern: engineering substance,
practical significance, novelty, testability, Russian/on-prem software,
explicit user/action/effect chain, and a pilot with go/no-go gates.
Scores are readiness heuristics, not a claim of selection.
"""
from dataclasses import dataclass

@dataclass
class ReadinessInput:
    has_physics: bool = True
    has_mass_balance: bool = True
    has_operator_output: bool = True
    has_measurable_kpi: bool = True
    has_narrow_user: bool = True
    has_pilot_protocol: bool = True
    has_real_data: bool = False
    has_lab_validation: bool = False
    has_on_prem: bool = True
    has_russian_stack_path: bool = True
    has_uncertainty: bool = True
    has_evidence_registry: bool = True


def assess(x=None):
    x = x or ReadinessInput()
    dimensions = {
        "engineering_substance": [x.has_physics, x.has_mass_balance],
        "practical_significance": [x.has_operator_output, x.has_measurable_kpi, x.has_narrow_user],
        "novelty": [x.has_uncertainty, x.has_evidence_registry],
        "testability": [x.has_pilot_protocol, x.has_real_data, x.has_lab_validation],
        "sovereignty": [x.has_on_prem, x.has_russian_stack_path],
    }
    scores = {k: round(100 * sum(v) / len(v), 1) for k,v in dimensions.items()}
    blockers = []
    if not x.has_real_data: blockers.append("нет обезличенного промышленного архива")
    if not x.has_lab_validation: blockers.append("нет повторных лабораторных опытов")
    if not x.has_mass_balance: blockers.append("нет component mass-balance")
    if not x.has_measurable_kpi: blockers.append("нет KPI и baseline")
    readiness = round(sum(scores.values()) / len(scores), 1)
    return {
        "scores": scores,
        "readiness": readiness,
        "blockers": blockers,
        "honest_stage": "screening+lab-design" if blockers else "pilot-ready",
        "scores_are_heuristics": True,
        "note": "Scores are checklist heuristics for readiness discussion, not INDUSTRIX selection proof.",
    }


def pilot_gates():
    return [
        {"id":"G1", "name":"Data QC", "pass":"charge balance <=5%, duplicates/blanks/spikes pass"},
        {"id":"G2", "name":"Representativeness", "pass":"30-100 time-stamped analyses + flow/temperature"},
        {"id":"G3", "name":"Process closure", "pass":"recovery, reagent, energy, waste and closure reported"},
        {"id":"G4", "name":"Lab evidence", "pass":">=3 repeat batches per shortlisted scheme"},
        {"id":"G5", "name":"Economics", "pass":"P(NPV>0)>=0.75 and explicit price/FX/offtake scenario"},
        {"id":"G6", "name":"Product", "pass":"impurity panel and agreed product specification pass"},
        {"id":"G7", "name":"Safety", "pass":"read-only advisory, no control path, local deployment"},
    ]
