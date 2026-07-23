# BrineValue OS

Открытый on-prem **инженерный скрининг-инструмент** пластовых/промысловых вод для выбора
рентабельных технологий извлечения Li, Br, Sr и сопутствующих компонентов.
Объяснимые физико-химические и техноэкономические модели, не «чёрный ящик AI».

> **Advisory only.** Требует лабораторной валидации. Не является полноценным цифровым
> двойником установки, не FEED, не сертификат продукта и не инвестиционный кейс.
> NPV и цены по умолчанию — placeholder (`RUB_per_kg_element`).

## Одна команда
```bash
pip install -e .
python -m brinevalue.cli demo --index 0 --report report.html
python -m brinevalue.cli screen data/streams.csv
python -m benchmark.run_benchmark   # sanity gates + exit code
python run_tests.py                 # тесты
```
API: `uvicorn brinevalue.api:app`. UI: `streamlit run brinevalue/dashboard.py`. `docker compose up`.

## Конвейер
анализ воды → ионный баланс + скейлинг (Davies только при I≤0.5) → перебор техсхем →
экономика/NPV → uncertainty P(NPV>0) → quality gates → решение no-go/lab/pilot/scale →
sensitivity → план лаб-опытов → калибровка.

`recommend()` всегда применяет governance (QC + P(NPV>0)). Сырой NPV-порог доступен
только как `raw_decision`.

Лицензия: Apache-2.0. Монетизация: открытое ядро + on-prem коннекторы, адаптация, валидация.

## Версии
- **v0.5.1**: red-team fixes — packaging, governed `recommend`, Davies SI gating, stale benchmark, honest naming.
- **v0.5.0**: INDUSTRIX readiness layer.
- **v0.4.0**: academic hardening (mass ledger, Bayesian posterior, robust governance).
- **v0.3.0**: uncertainty-aware P(NPV>0), quality gates.

Не смешиваем три уровня доказательности: синтетический скрининг, лабораторная
валидация, промысловой пилот. В промышленную заявку уходят только показатели
с указанным уровнем доказательности.

Аудит: `docs/RED_TEAM_FULL_AUDIT_2026_07_23.md`.
