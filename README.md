# BrineValue OS v0.5.2

Открытый on-prem **инженерный скрининг-инструмент** пластовых/промысловых вод
(Li, Br, Sr, K, B; йод — tracking без recovery unit). Объяснимые физхим + TEA модели.
**Не** цифровой двойник, **не** FEED, **не** battery-grade, **не** инвестиционный кейс без цен актива.

> **Advisory only.** NPV/цены — `screening_placeholder` (`RUB_per_kg_element`).
> Davies SI decision-grade только при I≤0.5. Данные demo/benchmark — **синтетические**.
> Governed решение: `no_go` / `lab` / `pilot` (без `scale` при placeholder TEA).

GitHub: https://github.com/KonkovDV/brinevalue-os · License: Apache-2.0

## Одна команда
```bash
pip install -e ".[excel]"   # excel optional (openpyxl)
python -m brinevalue.cli demo --index 0 --report artifacts/demo_report.html
python -m brinevalue.cli screen data/streams.csv
python -m benchmark.run_benchmark
python -m benchmark.redteam
python run_tests.py          # 77 tests on current tree
```
API: `uvicorn brinevalue.api:app --host 127.0.0.1 --port 8000`  
UI: `streamlit run brinevalue/dashboard.py`  
Docker: `docker compose up` (binds **127.0.0.1** only; set `BRINEVALUE_API_TOKEN` for API auth).
AppSec plan: `docs/SECURITY_REMEDIATION_PLAN_2026_07_23.md`.
Заявка INDUSTRIX (синхронизация claims): `docs/INDUSTRIX_APPLICATION_SYNC_2026_07_23.md`.

## Конвейер
QC (баланс) → SI (Davies if I≤0.5) → перебор схем → TEA → P(NPV>0)+stability →
greedy **measurement** ranking → решение no-go/lab/pilot (governed).

`recommend()` всегда governed. Сырой NPV = `raw_decision` (может содержать scale).

## Версии
- **v0.5.2**: INDUSTRIX audit + AppSec harden — NaN guards, HTML SI/XSS escape, evaporation DLE boost,
  waste ledger, econ validation, scheme_stability gate, governed scale→pilot cap,
  honest Bayes/DoE/surrogate labels, redteam suite, loopback Docker, optional API token.
- **v0.5.1**: packaging, governed recommend, Davies gating, stale benchmark.
- **v0.5.0**: INDUSTRIX readiness layer.

Аудит: `docs/RED_TEAM_FULL_AUDIT_2026_07_23.md`, `docs/INDUSTRIX_AUDIT_REPORT_2026_07_23.md`,
`docs/INDUSTRIX_CLAIM_MAP.md`.
