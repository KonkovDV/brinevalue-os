"""Techno-economic screening model (placeholders, not offtake quotes).

Metrics: NPV, undiscounted ROROI, simple payback. No IRR solver.
prod_cost_usd_t is Li-allocated (co-product revenue NOT credited) — labeled.
Defaults frozen in docs/ECONOMICS.md. economics_grade=screening_placeholder.
"""
import math

PRODUCT_PRICE = {"Li": 5500.0, "Br": 260.0, "Sr": 180.0, "K": 60.0, "B": 400.0, "I": 3000.0}
PRICE_UNIT = "RUB_per_kg_element"
REAGENT_PRICE = 45.0
ENERGY_PRICE = 6.5
DAYS = 330
FX_RUB_USD = 90.0
LI_TO_LI2CO3 = 5.323
LI2CO3_PRICE_SCENARIOS_USD_T = [8000, 10000, 12000, 15000, 18000, 20000, 22000, 25000, 30000, 40000, 50000]
PROCESS_COST_FLOOR_RUB_M3 = 320.0


def _validate_tea_inputs(prices, discount, years):
    if years is None or not math.isfinite(float(years)) or int(years) < 1:
        raise ValueError("years must be >= 1")
    if discount is None or not math.isfinite(float(discount)) or not (0.0 < float(discount) < 1.0):
        raise ValueError("discount must be in (0,1)")
    for k, v in (prices or {}).items():
        if v is None or not math.isfinite(float(v)) or float(v) < 0:
            raise ValueError(f"price for {k} must be finite and >= 0")


def annual_product_kg(brine, flowsheet):
    out = {}
    for ion, rec in flowsheet["recovery"].items():
        rec = float(rec)
        if not math.isfinite(rec) or rec < 0 or rec > 1:
            raise ValueError(f"recovery for {ion} must be in [0,1], got {rec}")
        mg_per_l = brine.ions.get(ion, 0.0)
        out[ion] = mg_per_l * (brine.flow * 1000.0) * rec * DAYS / 1e6  # kg/yr
    return out


def economics(brine, flowsheet, prices=None, discount=0.15, years=10,
              capex_factor=1.0, opex_factor=1.0):
    _validate_tea_inputs(prices, discount, years)
    years = int(years)
    discount = float(discount)
    capex_factor = float(capex_factor)
    opex_factor = float(opex_factor)
    if not math.isfinite(capex_factor) or capex_factor <= 0:
        raise ValueError("capex_factor must be finite and > 0")
    if not math.isfinite(opex_factor) or opex_factor <= 0:
        raise ValueError("opex_factor must be finite and > 0")
    p = {**PRODUCT_PRICE, **(prices or {})}
    for k, v in p.items():
        if v is None or not math.isfinite(float(v)) or float(v) < 0:
            raise ValueError(f"default/override price for {k} invalid")
    vol_yr = brine.flow * DAYS
    brine.validate()
    prod_raw = annual_product_kg(brine, flowsheet)
    prod = {k: round(v, 6) for k, v in prod_raw.items()}
    revenue_components = {i: prod[i] * p.get(i, 0.0) for i in prod}
    revenue = sum(revenue_components.values())
    opex = (
        flowsheet["reagent_kg_per_m3"] * REAGENT_PRICE
        + flowsheet["kwh_per_m3"] * ENERGY_PRICE
        + PROCESS_COST_FLOOR_RUB_M3
    ) * vol_yr * opex_factor
    capex = (6.0e7 + 3.0e4 * (vol_yr ** 0.7)) * (0.6 + 0.05 * len(flowsheet["units"])) * capex_factor
    if not math.isfinite(capex) or capex < 0:
        raise ValueError("CAPEX calculation produced invalid value")
    net_yr = revenue - opex
    npv = -capex + sum(net_yr / (1 + discount) ** t for t in range(1, years + 1))
    roroi = (net_yr * years - capex) / capex if capex else None
    li_kg = prod.get("Li", 0.0)
    li2co3_t = li_kg * LI_TO_LI2CO3 / 1000.0
    annualized_capex = capex * discount / (1 - (1 + discount) ** -years)
    prod_cost_usd_t = ((opex + annualized_capex) / FX_RUB_USD / li2co3_t) if li2co3_t > 0 else None
    co_product_rev = sum(v for k, v in revenue_components.items() if k != "Li")
    net_prod_cost_usd_t = None
    if li2co3_t > 0:
        net_prod_cost_usd_t = ((opex + annualized_capex - co_product_rev) / FX_RUB_USD / li2co3_t)
    return dict(
        revenue_rub_yr=round(revenue),
        opex_rub_yr=round(opex),
        capex_rub=round(capex),
        net_rub_yr=round(net_yr),
        npv_rub=round(npv),
        roroi=round(roroi, 2) if roroi is not None else None,
        roroi_definition="undiscounted (net_yr*years - capex)/capex — not IRR",
        li2co3_t_yr=round(li2co3_t, 1),
        prod_cost_usd_t=round(prod_cost_usd_t) if prod_cost_usd_t is not None else None,
        prod_cost_basis="li_allocated_no_coproduct_credit",
        prod_cost_net_of_coproducts_usd_t=round(net_prod_cost_usd_t) if net_prod_cost_usd_t is not None else None,
        product_kg_yr=prod,
        revenue_components_rub_yr={k: round(v, 2) for k, v in revenue_components.items()},
        price_unit=PRICE_UNIT,
        economics_grade="screening_placeholder",
        simple_payback_yr=round(capex / net_yr, 2) if net_yr > 0 else None,
        payback_yr=round(capex / net_yr, 2) if net_yr > 0 else None,  # alias; undiscounted
        irr="not_implemented",
        assumptions={
            "days_per_year": DAYS,
            "fx_rub_usd": FX_RUB_USD,
            "discount": discount,
            "years": years,
            "process_cost_floor_rub_m3": PROCESS_COST_FLOOR_RUB_M3,
            "capex_factor": capex_factor,
            "opex_factor": opex_factor,
            "inflation": "none",
            "tax_logistics": "none",
            "lab_validation_cost": "not_in_model",
        },
    )


def price_scenarios(brine, flowsheet, scenarios=None):
    """NPV vs Li2CO3 price. Returns list of {usd_per_t, npv_rub}.

    Conversion (consistent with li2co3_t = li_kg * LI_TO_LI2CO3 / 1000):
    RUB/kg Li = (USD/t Li2CO3) * LI_TO_LI2CO3 * FX_RUB_USD / 1000.
    """
    out = []
    for usd_t in (scenarios or LI2CO3_PRICE_SCENARIOS_USD_T):
        li_price_rub_kg = float(usd_t) * LI_TO_LI2CO3 * FX_RUB_USD / 1000.0
        ec = economics(brine, flowsheet, prices={"Li": li_price_rub_kg})
        out.append(dict(li2co3_usd_t=usd_t, npv_rub=ec["npv_rub"]))
    return out


def tea_scenarios(brine, flowsheet, prices=None):
    """Conservative / base / optimistic screening overlays (synthetic multipliers).

    When ``prices`` is provided (e.g. from ``recommend``), base and relative
    Li overlays start from that map instead of silently resetting to PRODUCT_PRICE.
    """
    base_prices = {**PRODUCT_PRICE, **(prices or {})}
    base = economics(brine, flowsheet, prices=base_prices)
    li0 = float(base_prices.get("Li", PRODUCT_PRICE["Li"]))
    # Conservative: -40% Li price, +50% CAPEX, +50% OPEX, higher discount
    cons_prices = {**base_prices, "Li": li0 * 0.6}
    cons = economics(
        brine, flowsheet, prices=cons_prices, discount=0.18,
        capex_factor=1.5, opex_factor=1.5,
    )
    # Optimistic: +30% Li price, lower discount
    opt_prices = {**base_prices, "Li": li0 * 1.3}
    opt = economics(brine, flowsheet, prices=opt_prices, discount=0.12)
    return {
        "conservative": {
            "npv_rub": cons["npv_rub"],
            "note": "Li price -40%, CAPEX +50%, OPEX +50%, discount 18%",
        },
        "base": {
            "npv_rub": base["npv_rub"],
            "note": "caller prices" if prices else "default placeholders",
        },
        "optimistic": {"npv_rub": opt["npv_rub"], "note": "Li price +30%, discount 12%"},
        "evidence_grade": "synthetic_screening",
    }
