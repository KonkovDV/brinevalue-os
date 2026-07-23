# PILOT_PLAN.md (12–16 weeks) — screening → lab → stand

**УГТ today:** screening MVP + lab-design tools. **Not** stand/pilot without site data.

**Title for application:** «Предлагаемый дизайн валидации с INDUSTRIX» / «Проект пилотной программы для объекта заказчика» — **not** «пилот для Газпром нефти» unless LOI exists.

1. Retro-screen 30–100 **anonymized** analyses (customer / INDUSTRIX partner archive); pick 3–5 streams.
2. Minimal **measurement** plan via `propose_experiments` (**greedy VoI ranking** of feed assays — not Bayesian opt, not process batch DoE).
3. Design real process batch DoE separately (pretreatment, extraction, elution, reagents, energy, product impurity, waste).
4. Calibrate recoveries with batch tests; Beta posterior is **diagnostic** until explicitly wired into TEA.
5. Upgrade SI to Pitzer/PHREEQC before any industrial scale discussion on hypersaline brine.
6. One scheme to stand pilot with go/no-go KPI (balance ≤5% pilot gate aspirational;
   code decision_grade currently ≤10% — align contractually before pilot).
7. Replace placeholder prices/CAPEX/OPEX/FX; never present screening NPV as FEED.
8. Governed software decision remains capped at **pilot** (design candidate) under `screening_placeholder` TEA.

KPI examples: ionic balance QA, measured recovery CI, P(NPV>0) after calibration,
product impurity panel (battery-grade only if specs met). Algebraic ledger closure
is a software invariant, not a lab accuracy KPI.
