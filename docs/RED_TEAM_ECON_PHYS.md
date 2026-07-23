# Red-team audit: economics and physical chemistry, 23 July 2026

## Findings fixed
- Negative concentrations, pH outside [0,14], unsupported temperature and
  negative flow were previously accepted. `Brine.validate()` now rejects them.
- Revenue could differ from the displayed rounded production values. Economics
  now calculates revenue from the displayed six-decimal production values and
  returns a component revenue ledger.

## Findings that remain by design
- Davies activity coefficients are not valid as a final model at hypersaline
  ionic strength. They are screening only; Pitzer/PHREEQC/Reaktoro is required
  before a pilot decision.
- Ksp values are fixed approximate 25 C values; temperature-dependent constants,
  complexes and oil-organic interactions are not modeled.
- Charge balance is a QC flag, not a mass-balance correction. A failed balance
  demotes the governed recommendation to LAB rather than silently adjusting ions.
- Unit operations use screening correlations. The mass ledger closes, but the
  recovery, selectivity, reagent, energy and waste coefficients require batch /
  continuous calibration.
- CAPEX, OPEX, FX, prices, uptime and discount rate are placeholders and must be
  supplied by the asset owner. NPV is decision support, not an investment case.

## Acceptance gates
1. Input validation passes.
2. Component mass-balance closure is <= 1e-6 kg/y in synthetic chains.
3. No recovery exceeds feed mass.
4. NPV is monotone in Li2CO3 price.
5. Revenue ledger closes to displayed production values.
6. Bad charge balance or low `P(NPV>0)` cannot yield a governed scale decision.
