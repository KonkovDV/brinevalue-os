# BrineValue OS v0.5.2

Открытый on-prem **инженерный скрининг-инструмент** пластовых/промысловых вод
(Li, Br, Sr, K, B). Объяснимые физхим + TEA модели. **Не** цифровой двойник,
**не** FEED, **не** battery-grade, **не** инвестиционный кейс без цен актива.

> **Advisory only.** NPV/цены — `screening_placeholder` (`RUB_per_kg_element`).
> Davies SI decision-grade только при I≤0.5. Данные demo/benchmark — **синтетические**.

GitHub: https://github.com/KonkovDV/brinevalue-os

## Одна команда
```bash
pip install -e ".[excel]"   # excel optional (openpyxl)
python -m brinevalue.cli demo --index 0 --report artifacts/demo_report.html
python -m brinevalue.cli screen data/streams.csv
python -m benchmark.run_benchmark
python -m benchmark.redteam
python run_tests.py
```
API: `uvicorn brinevalue.api:app --host 127.0.0.1 --port 8000`  
UI: `streamlit run brinevalue/dashboard.py`  
Docker: `docker compose up` (operator must not expose publicly without controls)

## Конвейер
QC (баланс) → SI (Davies if I≤0.5) → перебор схем → TEA → P(NPV>0)+stability →
greedy lab ranking → решение no-go/lab/pilot/scale.

`recommend()` всегда governed. Сырой NPV = `raw_decision`.

## Версии
- **v0.5.2**: full INDUSTRIX audit — NaN guards, HTML SI crash fix, evaporation DLE boost,
  waste ledger, econ validation, scheme_stability gate, honest Bayes/DoE/surrogate labels,
  redteam suite, artifacts.
- **v0.5.1**: packaging, governed recommend, Davies gating, stale benchmark.
- **v0.5.0**: INDUSTRIX readiness layer.

Аудит: `docs/RED_TEAM_FULL_AUDIT_2026_07_23.md`, `docs/INDUSTRIX_AUDIT_REPORT_2026_07_23.md`.
