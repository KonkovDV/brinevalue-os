# Red Team full audit — BrineValue OS

**Дата аудита:** 2026-07-23 (v0.5.0)  
**Ремедиация:** 2026-07-23 → **v0.5.1**  
**Объект:** `C:\plans\Industrix\brinevalue`  
**Метод:** код + `run_tests.py` + `benchmark.run_benchmark` + adversarial прогоны.  
**Не полевой отчёт.**

## Вердикт (после v0.5.1)

| Ось | Оценка |
|---|---|
| Как screening / lab-design MVP для INDUSTRIX | **8 / 10** |
| Как «цифровой двойник» / investment-grade TEA | **3 / 10** (by design) |
| Готовность к пилоту на объекте | **2 / 10** (нет реальных данных и лаб-валидации) |
| Честность документации vs код | **8.5 / 10** |

**Итог:** advisory-скрининг с governance. Не twin, не FEED, не investment case. Критические пункты аудита v0.5.0 закрыты в v0.5.1 (упаковка, stale benchmark, governed `recommend`, Davies SI gating, naming).

## Воспроизведение (целевое после ремедиации)

```text
pip install -e .
python run_tests.py
python -m benchmark.run_benchmark
# live decisions ожидаемо: no_go доминирует; scale редкий
```

## PASS / PARTIAL / FAIL — статус ремедиации

| Тема | Было (v0.5.0) | v0.5.1 |
|---|---|---|
| `pip install -e .` | FAIL (`data`+`brinevalue`) | FIXED — `packages.find` include `brinevalue*` |
| `BENCHMARK_RESULTS.txt` | FAIL stale scale=13 | FIXED — регенерирован из live |
| `recommend()` vs `analyze()` | PARTIAL 9/24 mismatch | FIXED — `recommend` всегда QC+robust; `raw_decision` отдельно |
| Davies при I>0.5 | FAIL γ≫1 → SI flags | FIXED — `si_reliable=False`, flags False, SI None for decisions |
| Balance >25% | soft `lab` | FIXED → `no_go` + `reject_sample` |
| Balance >10% | demote scale | KEPT → max `lab`, `non_decision_grade` |
| «Цифровой двойник» README/UI | PARTIAL | FIXED — screening tool wording |
| Цены/CAPEX placeholders | FAIL by design | LABELED — `PRICE_UNIT`, `economics_grade` |
| INDUSTRIX self-score | heuristic | LABELED — `scores_are_heuristics` |
| Git | FAIL | FIXED — init + commit v0.5.1 |
| Surrogate Li importance | PARTIAL messaging | OPEN — не меняли модель; docs only |
| Полевые данные / Pitzer | N/A | OPEN by design |

## Что разрешено говорить (INDUSTRIX)

- Открытый on-prem **скрининг и планирование лабораторных опытов**.  
- Цепочка: QC → скейлинг (Davies только I≤0.5) → схемы → TEA → P(NPV>0) → DoE.  
- Default ответ может быть **no-go / lab**.  
- Не контроллер / не сертификат / не FEED.

## Что запрещено говорить

- Полноценный цифровой двойник / Pitzer-валидированная термодинамика.  
- Battery-grade Li₂CO₃ из концентрации в модели.  
- NPV / prod_cost как инвестиционный кейс без цен актива.  
- Готовность к промысловому пилоту без архива и лаб-батчей.

## Соответствие docs

`docs/RED_TEAM_ECON_PHYS.md` и `AUDIT_JULY_2026.md` остаются честными про Davies/placeholders.
Этот файл фиксирует аудит + закрытие критических пунктов в **v0.5.1**.
