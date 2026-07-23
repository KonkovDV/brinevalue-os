"""BrineValue OS — open on-prem screening tool for produced/formation water.

Explainable physico-chemical + techno-economic + surrogate models. Advisory only:
no field control; all results require laboratory validation. Not a plant digital
twin, not FEED, not a product certificate.
"""
__version__ = "0.5.2"
from .chemistry import (
    Brine, ionic_balance, scaling_risk, mg_li_ratio, davies_gamma,
    DAVIES_VALID_I_MAX, KSP_REFERENCE_TEMP_C,
)
from .process import UNIT_LIBRARY, evaluate_flowsheet
from .economics import economics, price_scenarios, tea_scenarios, PRODUCT_PRICE, PRICE_UNIT
from .optimizer import screen, pareto_front, recommend, govern_decision
from .surrogate import train_surrogate, predict_npv
from .doe import propose_experiments
from .sensitivity import sensitivity
from .pipeline import analyze
