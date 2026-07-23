# Academic methods (honest labels)

1. **State propagation and component mass ledger**: pretreatment changes Mg/Li;
   ledger tracks feed / recovered / **waste_removed** / residual / closure.
   Near-zero algebraic closure is a **bookkeeping invariant**, not independent
   physical-model validation. Pilot KPI must use measured streams.
2. **Lab Beta posterior (diagnostic)**: `bayes.py` updates recovery posteriors from
   batch observations. **Not applied** to TEA / unit library unless the caller wires it.
   Normal-Inverse-Gamma for energy/reagent is **not implemented**.
   Correct claim: «прототип диагностического Bayesian update recovery».
3. **Robust decision governance**: nominal NPV is not enough. `P(NPV>0)`, QC,
   and scheme_stability demote `pilot`/`scale`. Under placeholder TEA, governed
   output is capped at **`pilot`** (`raw_decision` may still show `scale`).
4. **Greedy measurement ranking** (`doe.py`): ranks which **feed measurement** most
   reduces NPV **standard deviation** (`npv_std_reduction_rub`). **Not** Bayesian
   optimization and **not** process batch DoE (sorption/regeneration/purity).
5. **Monte Carlo**: independent lognormal perturbations of composition and flow
   (not correlated; CAPEX/OPEX/recovery/prices not varied).
6. **Evidence levels**: synthetic screening ≠ lab ≠ pilot ≠ field.
7. **Surrogate RF**: reproduces synthetic labels (high CV R² ≠ field accuracy);
   does not accelerate main MC/DoE path.

Next research-grade upgrades: Pitzer/PHREEQC SI, apply posteriors to unit
likelihoods, site-calibrated CAPEX/OPEX, real offtake prices, process batch DoE.
