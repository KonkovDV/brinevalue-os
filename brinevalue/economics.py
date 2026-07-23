"""Techno-economic model with the metrics investors actually use.

Upgrade v0.2.0:
- Adds ROROI and production cost per tonne Li2CO3-equivalent ($/t), the decision
  metric in DLE TEAs (Nikfar et al. ACS 2026; Salton Sea Nature Commun. 2026
  benchmark: ~$10,000-22,000/t). Li -> Li2CO3 factor 5.323 (MW 73.89/13.88).
- Adds K, B, I product prices and a Li2CO3 price-scenario sweep
  (11 scenarios in Nikfar 2026). Treatment cost is 5-15% of production cost
  (Chen et al. DWT 2025), used as a sanity band.
Defaults are screening estimates, all overridable. Frozen in docs/ECONOMICS.md.
"""
PRODUCT_PRICE = {"Li": 5500.0, "Br": 260.0, "Sr": 180.0, "K": 60.0, "B": 400.0, "I": 3000.0}
# Explicit unit for PRODUCT_PRICE keys (screening placeholders, not offtake quotes).
PRICE_UNIT = "RUB_per_kg_element"
REAGENT_PRICE = 45.0
ENERGY_PRICE = 6.5
DAYS = 330
FX_RUB_USD = 90.0
LI_TO_LI2CO3 = 5.323
LI2CO3_PRICE_SCENARIOS_USD_T = [8000, 10000, 12000, 15000, 18000, 20000, 22000, 25000, 30000, 40000, 50000]
# All-in processing cost floor beyond explicit reagent/energy (labour, membranes,
# sorbent replacement, waste, maintenance). Calibrated so a typical Li~150 mg/L
# stream lands in the Salton Sea benchmark band (~$10-22k/t Li2CO3).
PROCESS_COST_FLOOR_RUB_M3 = 320.0


def annual_product_kg(brine, flowsheet):
    out = {}
    for ion, rec in flowsheet["recovery"].items():
        mg_per_l = brine.ions.get(ion, 0.0)
        out[ion] = mg_per_l * (brine.flow * 1000.0) * rec * DAYS / 1e6  # kg/yr
    return out


def economics(brine, flowsheet, prices=None, discount=0.15, years=10):
    p = {**PRODUCT_PRICE, **(prices or {})}
    vol_yr = brine.flow * DAYS
    brine.validate()
    prod_raw = annual_product_kg(brine, flowsheet)
    # Reported production values are rounded to 6 decimals and the revenue is
    # calculated from the same displayed values, preventing audit drift.
    prod = {k: round(v, 6) for k, v in prod_raw.items()}
    revenue_components = {i: prod[i] * p.get(i, 0.0) for i in prod}
    revenue = sum(revenue_components.values())
    opex = (flowsheet["reagent_kg_per_m3"] * REAGENT_PRICE
            + flowsheet["kwh_per_m3"] * ENERGY_PRICE
            + PROCESS_COST_FLOOR_RUB_M3) * vol_yr
    # capex with economies of scale on throughput + unit-count complexity;
    # calibrated to realistic DLE plant costs (see docs/ECONOMICS.md)
    capex = (6.0e7 + 3.0e4 * (vol_yr ** 0.7)) * (0.6 + 0.05 * len(flowsheet["units"]))
    net_yr = revenue - opex
    npv = -capex + sum(net_yr / (1 + discount) ** t for t in range(1, years + 1))
    roroi = (net_yr * years - capex) / capex if capex else None
    # production cost per tonne Li2CO3-equivalent (USD/t) if Li is recovered
    li_kg = prod.get("Li", 0.0); li2co3_t = li_kg * LI_TO_LI2CO3 / 1000.0
    annualized_capex = capex * discount / (1 - (1 + discount) ** -years)
    prod_cost_usd_t = ((opex + annualized_capex) / FX_RUB_USD / li2co3_t) if li2co3_t > 0 else None
    return dict(revenue_rub_yr=round(revenue), opex_rub_yr=round(opex),
                capex_rub=round(capex), net_rub_yr=round(net_yr), npv_rub=round(npv),
                roroi=round(roroi, 2) if roroi is not None else None,
                li2co3_t_yr=round(li2co3_t, 1),
                prod_cost_usd_t=round(prod_cost_usd_t) if prod_cost_usd_t else None,
                product_kg_yr=prod,
                revenue_components_rub_yr={k: round(v, 2) for k, v in revenue_components.items()},
                price_unit=PRICE_UNIT,
                economics_grade="screening_placeholder",
                payback_yr=round(capex / net_yr, 2) if net_yr > 0 else None)


def price_scenarios(brine, flowsheet, scenarios=None):
    """NPV vs Li2CO3 price. Returns list of (usd_per_t, npv_rub)."""
    out = []
    for usd_t in (scenarios or LI2CO3_PRICE_SCENARIOS_USD_T):
        li_price_rub_kg = usd_t / LI_TO_LI2CO3 * FX_RUB_USD / 1000.0
        ec = economics(brine, flowsheet, prices={"Li": li_price_rub_kg})
        out.append(dict(li2co3_usd_t=usd_t, npv_rub=ec["npv_rub"]))
    return out
