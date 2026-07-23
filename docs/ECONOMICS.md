# ECONOMICS.md

Screening TEA placeholders. **Not** FEED, **not** offtake quotes, **not** tax/logistics model.

## Outputs
| Metric | Definition | Implemented? |
|---|---|---|
| Revenue | Σ product_kg_yr × price (same rounded kg as displayed) | Yes |
| OPEX | (reagent + energy + process floor) × m³/yr × opex_factor | Yes (proxy) |
| CAPEX | throughput^0.7 + unit-count proxy × capex_factor | Yes (placeholder) |
| NPV | −CAPEX + Σ net/(1+r)^t | Yes |
| ROROI | (net×years − CAPEX)/CAPEX | Yes — **undiscounted, not IRR** |
| IRR | — | **`not_implemented`** |
| Simple payback | CAPEX/net if net>0 | Yes |
| $/t Li₂CO₃ | (OPEX+ann.CAPEX)/FX/li2co3_t | Yes — **Li-allocated, no co-product credit** by default; net-of-coproducts also reported |
| Price sweep | NPV vs Li₂CO₃ USD/t | Yes |
| tea_scenarios | conservative / base / optimistic | Yes — conservative applies Li −40%, CAPEX +50%, OPEX +50%, discount 18% |

## Defaults (`PRICE_UNIT = RUB_per_kg_element`)
Li 5500, Br 260, Sr 180, K 60, B 400, I 3000 (I priced but **no recovery unit**).
Days=330, FX=90 RUB/USD, discount=15%, years=10, process floor=320 RUB/m³.

## Governance
Positive nominal NPV is insufficient. `recommend()` demotes using QC, P(NPV>0), and scheme_stability.
`economics_grade = screening_placeholder` on every result.
**Governed decision never returns `scale`** while TEA remains placeholder; at most `pilot` (pilot-design candidate). `raw_decision` may still show NPV-only `scale`.

Decision NPV thresholds (raw only): ≤0 no_go; <50M lab; <300M pilot; else scale — **not** customer hurdle rates.

## Tests
`test_economics_*`, `test_economics_revenue_components_close`, `test_negative_price_rejected`.
