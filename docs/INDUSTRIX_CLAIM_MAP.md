# INDUSTRIX_CLAIM_MAP.md

Project: **BrineValue OS** · Version **0.5.2** · GitHub: https://github.com/KonkovDV/brinevalue-os

| Criterion | Artifact | Honest claim |
|---|---|---|
| Engineering substance | `chemistry.py`, `process.py` | Screening ionic QC + unit correlations; algebraic component ledger (bookkeeping, not plant validation) |
| Practical significance | `recommend` / HTML report | Advisory **no-go / lab / pilot** (governed; `scale` demoted under placeholder TEA; `raw_decision` may still show scale) |
| Novelty | multi-product screen + greedy measurement ranking + robust P(NPV>0) | **Not** a digital twin; **not** Bayesian optimization; **not** process batch DoE |
| Product set | UNIT_LIBRARY recovery paths | **Five** modeled products: Li, Br, Sr, K, B. **Iodine tracked/priced, no recovery unit** |
| Import substitution / RU software | Python on-prem, Apache-2.0 | Intended local deploy; no field controller |
| Testability | `tests/`, `benchmark/`, `benchmark/redteam.py` | On frozen release: **77** automated tests + synthetic benchmark + adversarial red-team suite (0 failures). Confirms software constraints, **not** field accuracy |
| User | process engineer / lab lead (primary); techno-economist (consumer of ranking) | Needs ICP/IC water analysis + offtake prices |
| Process | formation/produced water → Li/Br/Sr(+K/B) screening | |
| Loss addressed | wrong expensive lab/stand on poor brine; missed early no-go | |
| Inputs | mg/L ions, m³/d, T, pH, org, uncertainty | |
| Algorithm | deterministic screen + MC on composition/flow + greedy VoI measurement ranking | |
| Action | lab measurement plan / no-go / pilot-design gate checklist | |
| KPI | P(NPV>0), balance error % (QC), scheme stability, $/t screen | Do **not** claim mass-closure % as model accuracy |
| Pilot scheme | `docs/PILOT_PLAN.md` | Requires **customer** anonymized archive + one stream for lab (not a signed contract claim) |
| TRL / УГТ | software prototype + reproducible calculation contour | УГТ 4 for **software/calculation**; process correlations need lab calibration |
| Investment need | lab campaign + Pitzer SI + site TEA | See application budget breakdown (not quantified as FEED) |

**Approved short description (RU):** on-prem инженерная система предварительного screening и планирования лабораторной валидации — **не** цифровой двойник.

**Forbidden in application slides:** battery-grade, industrial accuracy, digital twin, Pitzer-in-product, Bayesian calibration workflow (when only diagnostic Beta), Bayesian optimization (when greedy), process DoE (when measurement ranking), customer NPV without site prices, iodine recovery unit, mass-balance closure as physics proof, «пилот для Газпром нефти» without LOI.
