"""Feed and product quality gates for a defensible pilot recommendation."""
from .chemistry import RECOVERABLE


def quality_gate(brine, flowsheet=None, qc=None, scaling=None):
    issues, warnings = [], []
    bal = qc.get("balance_error_pct") if qc else None
    if qc is not None and qc.get("reject_sample"):
        issues.append("ionic_balance_reject_sample")
    if qc is not None and bal is not None and bal > 10:
        issues.append("ionic_balance_error_gt_10pct")
    if qc is not None and bal is not None and bal > 25:
        issues.append("ionic_balance_error_gt_25pct_reject_sample")
    if brine.flow <= 0:
        issues.append("nonpositive_flow")
    if brine.temp < 0 or brine.temp > 150:
        warnings.append("temperature_outside_screening_range")
    if brine.org > 1000:
        warnings.append("high_organics_pre_treatment_required")
    if brine.org > 5000:
        issues.append("organics_gt_5000_mg_l")
    missing = [i for i in RECOVERABLE if i not in brine.ions]
    if missing:
        warnings.append("missing_optional_components:" + ",".join(missing))
    if scaling:
        risky = [k for k, v in scaling.items() if v]
        if risky:
            warnings.append("scaling_risk:" + ",".join(risky))
    product = {}
    if flowsheet:
        mgli = brine.molar("Mg") / max(brine.molar("Li"), 1e-12)
        product["Li2CO3_quality_screen"] = (
            "needs_polishing" if mgli > 10 or warnings else "screen_pass"
        )
        product["mg_li_ratio"] = round(mgli, 2)
        product["note"] = "screen_pass is NOT battery-grade certification"
    return {
        "pass": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "product": product,
        "sample_grade": "decision_grade" if len(issues) == 0 else "non_decision_grade",
    }
