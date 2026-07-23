# Red-team audit: economics and physical chemistry

## Findings fixed (incl. v0.5.2)
- Negative / non-finite concentrations, pH, T, flow, org rejected by `Brine.validate()`.
- Revenue from displayed rounded production values + component ledger.
- SI=`None` no longer crashes HTML reports; Windows utf-8 report write.
- Evaporation now applies a modest screening DLE boost via `preconcentrate`.
- Desulfurization notes no longer claim H2S/hydrocarbon removal.
- TEA rejects negative prices and years < 1; IRR labeled `not_implemented`.
- Governance uses QC + P(NPV>0) + scheme_stability; Pareto drives `best`.
- DoE renamed to greedy uncertainty reduction; Bayes posterior diagnostic-only.

## Findings that remain by design
- Davies activity coefficients are not valid as a final model at hypersaline
  ionic strength. They are screening only; Pitzer/PHREEQC/Reaktoro is required
  before a pilot decision.
- Ksp values are fixed approximate 25 C values; temperature-dependent constants,
  complexes and oil-organic interactions are not modeled.
- Charge balance is a QC flag, not a mass-balance correction. A failed balance
  demotes the governed recommendation to LAB / NO-GO rather than silently adjusting ions.
- Unit operations use screening correlations. The mass ledger closes, but the
  recovery, selectivity, reagent, energy and waste coefficients require batch /
  continuous calibration.
- CAPEX, OPEX, FX, prices, uptime and discount rate are placeholders and must be
  supplied by the asset owner. NPV is decision support, not an investment case.

## Acceptance gates
1. Input validation passes (incl. NaN/Inf).
2. Component mass-ledger closure is ~0 by construction (algebraic invariant), not a
   physics-accuracy certificate. Pilot KPI must use measured streams.
3. No recovery exceeds feed mass.
4. NPV is monotone in Li2CO3 price.
5. Revenue ledger closes to displayed production values.
6. Bad charge balance, low `P(NPV>0)`, or unstable scheme cannot yield governed scale.
7. `python -m benchmark.redteam` exits 0.
