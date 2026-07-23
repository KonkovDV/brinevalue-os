# Academic methods added in v0.4.0

1. **State propagation and component mass ledger**: pretreatment changes the
   downstream Mg/Li and scaling context; every recovered component has feed,
   recovered, residual and closure terms.
2. **Bayesian lab calibration**: Beta posterior for recovery observations with
   an interval, grouped by unit and ion. It is deliberately conservative and
   does not infer a full mechanistic model from a handful of tests.
3. **Robust decision governance**: nominal NPV is not enough. `P(NPV>0)` under
   uncertainty and QC gates can demote a nominal `scale` to `lab` or `no_go`.
4. **Evidence levels**: claims are separated into screening correlations,
   laboratory posterior, and field/pilot validation. No battery-grade claim
   is accepted without impurity analytics and product specification.

The next research-grade upgrade is a full Pitzer/PHREEQC equilibrium layer and
Bayesian calibration of unit-operation likelihoods from time-stamped batch and
continuous experiments.
