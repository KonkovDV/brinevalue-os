# INDUSTRIX_CLAIM_MAP.md

Project: **BrineValue OS** · Version **0.5.2** · GitHub: https://github.com/KonkovDV/brinevalue-os

| Criterion | Artifact | Honest claim |
|---|---|---|
| Engineering substance | `chemistry.py`, `process.py` | Screening ionic QC + unit correlations |
| Practical significance | `recommend` / HTML report | Advisory no-go/lab/pilot/scale |
| Novelty | multi-product screen + greedy DoE + robust P(NPV>0) | **Not** a digital twin; **not** Bayesian optimization |
| Import substitution / RU software | Python on-prem, Apache-2.0 | Intended local deploy; no field controller |
| Testability | `tests/`, `benchmark/`, `benchmark/redteam.py` | Synthetic gates; lab/field not yet done |
| User | process engineer / lab lead | Needs ICP/IC water analysis + offtake prices |
| Process | formation/produced water → Li/Br/Sr(+K/B) screening | |
| Loss addressed | wrong scale-up / missed no-go on poor brine | |
| Inputs | mg/L ions, m³/d, T, pH, org, uncertainty | |
| Algorithm | deterministic screen + MC robust + greedy VoI ranking | |
| Action | lab plan / no-go / pilot gate checklist | |
| KPI | P(NPV>0), balance error %, scheme stability, $/t screen | |
| Pilot scheme | `docs/PILOT_PLAN.md` | Requires Gazprom Neft anonymized archive |
| TRL / УГТ | screening MVP + lab-design | **Not** pilot-ready without data+lab |
| Investment need | lab campaign + Pitzer SI + site TEA | Not quantified here |

**Forbidden in application slides:** battery-grade, industrial accuracy, full digital twin, Pitzer (when Davies), Bayesian optimization (when greedy), customer NPV without site prices.
