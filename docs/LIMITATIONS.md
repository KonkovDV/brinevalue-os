# LIMITATIONS.md

| Area | Status |
|---|---|
| Davies activity | Decision SI only I≤0.5; else transparency only |
| Ksp temperature | None (25 °C constants) |
| H2S / oil / fouling | Not modeled (QC warnings for org) |
| Pitzer/PHREEQC | Not integrated |
| IRR | Not implemented |
| Inflation / tax / logistics | None |
| Lab/validation CAPEX | Not in TEA |
| Iodine recovery unit | Missing (price + tracking exist) |
| Bayesian optimization | Not present (greedy measurement ranking only) |
| Process batch DoE | Not present (feed-assay ranking only) |
| Posterior→TEA coupling | Diagnostic only |
| Surrogate→MC | Not wired |
| Correlated composition uncertainty | Not implemented (independent draws) |
| Field / customer archive data | None in repo |
| Battery-grade product | Explicitly not claimed |
| Digital twin | Explicitly not claimed |
| Governed `scale` decision | Demoted to `pilot` under screening_placeholder TEA |
| Mass-ledger closure | Algebraic invariant ≠ physics accuracy |
