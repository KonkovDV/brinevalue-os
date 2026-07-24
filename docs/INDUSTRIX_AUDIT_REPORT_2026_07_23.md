# INDUSTRIX full audit report — BrineValue OS v0.5.2

**Date:** 2026-07-23  
**Repo:** https://github.com/KonkovDV/brinevalue-os  
**Python:** 3.13.7 · numpy 2.4.4 · pandas 3.0.2 · scipy 1.18.0 · scikit-learn 1.9.0

## 1. What was found (pre-fix evidence)
- CRITICAL: HTML report `TypeError` on SI=`None` (all synthetic hypersaline streams)
- CRITICAL: NaN ions passed validate; broke recommend
- CRITICAL: evaporation “boosts DLE” claim with identical recoveries
- HIGH: H2S/organics claimed in desulfurization notes but not modeled
- HIGH: DoE/Bayes/surrogate overclaims vs wiring
- HIGH: scheme_stability documented but not enforced
- HIGH: negative prices / years=0 accepted
- MEDIUM: version drift API/report; INDUSTRIX “twin” wording; I priced without unit

## 2. What was fixed
See `CHANGELOG.md` v0.5.2. Code + docs + `benchmark/redteam.py` + artifacts.

## 3. Still unconfirmed
- Any field brine from Gazprom Neft / peers
- Lab batch recoveries on site sorbent/membrane
- Pitzer SI / T-dependent Ksp
- Site CAPEX/OPEX/offtake
- IRR, tax, logistics, downtime economics beyond overlays
- Surrogate on real holdout streams

## 4. Actual measured results (this machine)
| Check | Result |
|---|---|
| `python run_tests.py` | **77/77 PASS** (current tree; regenerate claim on tag) |
| `python -m benchmark.redteam` | **0 failures** (adversarial suite; not “47/47 checks”) |
| `python -m benchmark.run_benchmark` | GATES PASS; typical mix no_go-dominant; governed `scale` absent (capped at pilot) |
| CLI `demo --report` | works (utf-8); decision often `lab` on synthetic |
| CLI `screen data/streams.csv` | runs; mostly `no_go`/`lab` |
| Excel import | works with openpyxl → `artifacts/streams_demo.xlsx` |
| FastAPI / Streamlit / Docker | code present; not claimed as production-hardened |

## 5. Synthetic results
All demo streams, benchmark, surrogate CV R², tea_scenarios multipliers, HTML demo.

## 6. Forbidden application claims
battery-grade · industrial accuracy · full digital twin · Pitzer-in-product · Bayesian optimization · AI black-box ranking · customer NPV without site prices · “13 scale” from stale files · pilot-ready without archive+lab

## 7. Data needed from customer / INDUSTRIX partner
Anonymized multi-well ion panels (incl. organics/H2S), flow history, lab ICP/IC QA, offtake prices, site power/reagent costs, downtime, existing pretreatment, product specs, environmental constraints.

## 8. Readiness
| Stage | Ready? |
|---|---|
| Public MVP (advisory screening) | **YES** (with honesty banners) |
| Lab verification | **READY TO START** (DoE ranking + Beta posterior diagnostic) |
| Stand/pilot | **NO** (needs data+lab+Pitzer SI) |
| Industrial operation | **NO** |

## 9. Commands
```bash
pip install -e ".[excel]"
python run_tests.py
python -m benchmark.run_benchmark
python -m benchmark.redteam
python -m brinevalue.cli demo --index 0 --report artifacts/demo_report.html
python -m brinevalue.cli screen data/streams.csv
```

## 10. Changed files (v0.5.2)
`brinevalue/*.py` (chemistry, process, economics, optimizer, report, doe, bayes, pipeline, quality, surrogate, api, cli, __init__), `tests/test_audit_fixes.py`, `benchmark/redteam.py`, `docs/*`, `README.md`, `CHANGELOG.md`, `pyproject.toml`, `artifacts/*`.
