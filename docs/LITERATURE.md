# LITERATURE.md — карта доказательной базы (аудит на июль 2026)

Каждая модель BrineValue OS привязана к свежему источнику.

## Рынок и реальные кейсы
- **Standard Lithium + Equinor**, Smackover SWA: положительный DFS, 20.2% pre-tax IRR, 22 500 т/год Li2CO3, первая продукция 2028; 1 млн баррелей и 15 000 циклов DLE на демо (Q1 2026).
- **Select Water + Mariana Minerals**: первый коммерческий объект из пластовой воды в Техасе, ~3000 т/год, 2027.
- **SLB**: коммерческий запуск DLE-фильтрации (Reuters 2024).

## Термодинамика и солеотложение
- Davies (скрининг). Пилотный апгрейд — Pitzer ion-interaction: Dai, Kan, Tomson (SPE 2013/2016; J. Chem. Eng. Data 2014); Plummer & Parkhurst PHREEQE-Pitzer (1990); Doubra 2017.
- Shen et al. (SPE 2023/2024): барит при высоком Ca, HTHP.

## Извлечение и процессы
- **Chen et al., Desalination & Water Treatment 2025**: первый в мире пром. проект 100 м3/сут Li/K/Br/B; водоподготовка 5-15% себестоимости; Li 50-200, K 800-4800, Br 50-250, B 100-500 мг/л.
- **Miao et al., SPE 2024** (YQ station, 2400 м3/сут, Mg~1200, Li~150): Mn-сорбент, порог Li>=50 мг/л.
- **Disu et al., SPE 2025**: емкость сорбента до 42 мг/г, селективность alpha>25.
- **Zhang et al., EST 2026**: электрохимия, >99.98% отсечка Mg, Mg(OH)2 копродукт.
- **Zhou et al., Materials 2026**: бесхлорная электрохимия Br, >90% за 12 мин.
- **Kong et al., Nature Communications 2025**; **Park et al., Resources 2025**: электро-DLE, электродиализ/CDI.
- **Alshammari et al., SPE 2026**: стадийное испарение повышает halite SI и DLE.

## Технико-экономика
- **Nikfar et al., ACS Sust. Res. Manag. 2026**: CAPEX/OPEX/NPV/ROROI/PBP по 11 ценовым сценариям Li2CO3; сравнение solvent/adsorption/NF+MD.
- **Salton Sea, Nature Communications 2026**: себестоимость ~$10 000-22 000/т с учётом неопределённости.
- **Vanneste & Van der Bruggen, Applied Sciences 2026**: обзор TEA DLE.

## Surrogate-оптимизация
- **Tiam et al., Water 2026** (Permian): surrogate-assisted TEA валоризации пластовой воды.
- **Scelfo et al., Desalination 2025**: surrogate-based оптимизация и scale-up цепочки из ультраконцентрированного рассола.

## Открытые аналоги (что мы НЕ копируем)
- **project-pareto** (логистика воды + Li screening) и **watertap / reaktoro-pse** (строгая десалинация). BrineValue OS отличается многокомпонентным product-twin + активным планированием опытов + РФ-контекстом.
