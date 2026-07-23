# Changelog

## v0.5.2 — 2026-07-23
### Fixed
- HTML report crash when SI is `None` (hypersaline / I>0.5)
- Windows encoding crash writing HTML (`utf-8` + ASCII arrow)
- `NaN`/`Inf` concentrations passed `validate()`
- Evaporation claimed DLE boost but left recoveries unchanged
- Desulfurization claim of H2S/hydrocarbon removal (SO4 only)
- DoE labeled Bayesian; Bayes module claimed NIG without implementation
- Surrogate claimed MC acceleration without wiring
- API/report version drift (0.1.0 / 0.2.0 vs package)
- Pareto ignored for `best` selection
- Missing scheme_stability governance gate
- Negative prices / years=0 accepted by TEA
- XSS via unescaped HTML report fields
- Docker Compose public `0.0.0.0` binds; root container
- `tea_scenarios` conservative note claimed CAPEX/OPEX uplift without applying it
- Misnamed `variance_reduction_rub` (was std reduction)
- Uncertainty docstring claimed correlated perturbations (draws are independent)
- Governed `scale` under placeholder TEA (now capped at `pilot`)

### Added
- `waste_removed_kg_yr` in mass ledger
- `tea_scenarios` (conservative/base/optimistic) with real capex/opex factors
- `prod_cost_net_of_coproducts_usd_t`, IRR=`not_implemented`
- `benchmark/redteam.py`
- `artifacts/` demo report + JSON snapshot
- AppSec: API bounds, optional `BRINEVALUE_API_TOKEN`, loopback compose, non-root image
- Docs honesty pass + `docs/INDUSTRIX_APPLICATION_SYNC_2026_07_23.md`
- Full Apache-2.0 `LICENSE` text

## v0.5.1 — 2026-07-23
Packaging exclude `data*`, governed `recommend`, Davies SI gating, live benchmark.

## v0.5.0
INDUSTRIX readiness layer.
