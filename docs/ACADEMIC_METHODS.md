# Academic methods (honest labels)

1. **State propagation and component mass ledger**: pretreatment changes Mg/Li;
   ledger tracks feed / recovered / **waste_removed** / residual / closure.
2. **Lab Beta posterior (diagnostic)**: `bayes.py` updates recovery posteriors from
   batch observations. **Not applied** to TEA unless the caller wires it.
   Normal-Inverse-Gamma for energy/reagent is **not implemented**.
3. **Robust decision governance**: nominal NPV is not enough. `P(NPV>0)`, QC,
   and scheme_stability demote `pilot`/`scale` to `lab`/`no_go`.
4. **Greedy uncertainty-reduction DoE** (`doe.py`): ranks which measurement most
   reduces NPV std. **Not** Bayesian optimization (no acquisition function).
5. **Evidence levels**: synthetic screening ≠ lab ≠ pilot ≠ field.

Next research-grade upgrades: Pitzer/PHREEQC SI, apply posteriors to unit
likelihoods, site-calibrated CAPEX/OPEX, real offtake prices.
