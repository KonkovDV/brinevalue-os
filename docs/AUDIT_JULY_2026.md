# BrineValue OS: independent audit, July 2026

## Verdict
The MVP is a **screening and experiment-design system**, not a process simulator,
plant controller, product certificate, or investment-grade FEED. That is the
correct claim for UGT 3-4. Its differentiator is the decision loop:
**sample QC -> scaling risk -> multi-component flowsheet -> TEA -> uncertainty ->
minimal experiment plan -> calibration**.

## Evidence and competitive reality
- PARETO and WaterTAP prove that open produced-water optimization is credible,
but PARETO is primarily network/logistics and lithium screening; it is not a
multi-component recovery/product-quality twin.
- Commercial momentum is real: Element3 reported first lithium carbonate from
Permian wastewater (Feb 2025); Select/Mariana broke ground on a commercial
facility (Oct 2025); Select/LibertyStream announced a 1,000 t/y unit (Feb 2026);
Standard Lithium reported 1m barrels and 15,000 DLE cycles at its demo (Apr
2026); Altillion raised $5m seed for oilfield wastewater/critical-mineral
extraction (Jun 2026).
- Fresh literature makes one point non-negotiable: pretreatment, Mg/Li,
impurities, energy, water, product quality, and brine uncertainty dominate
headline lithium concentration. Therefore the MVP must never rank on Li alone.

## Hard gaps intentionally not hidden
1. Davies activity corrections are screening grade at high TDS; pilot must use
Pitzer/PHREEQC/Reaktoro and temperature-dependent thermodynamic data.
2. Unit operations are transparent correlations, not validated mass/energy
balances. Their recovery and reagent/energy coefficients must be calibrated
against batch and continuous tests.
3. NPV defaults are placeholders. A customer run must replace prices, FX,
energy, waste, labor, CAPEX, uptime, product specification and offtake.
4. Product-quality logic is a screen. Battery-grade/technical-grade claims need
impurity analytics and a product specification.
5. The current DoE is uncertainty reduction by Monte Carlo, not full Bayesian
optimization with a lab likelihood. The next upgrade is to ingest observations
and fit per-unit recovery distributions.

## Acceptance gates for a real pilot
- charge balance error <= 5% for decision-grade samples;
- duplicate/blank/spike QC passes; detection-limit flags preserved;
- 30-100 time-stamped analyses, not a single grab sample;
- mass closure for every unit operation and uncertainty intervals;
- recovery, selectivity, reagent, energy and waste measured on representative
brine, with at least 3 repeat batches per shortlisted scheme;
- no-go if robust P(NPV>0) < 0.75 or if product quality fails the agreed spec;
- pilot recommendation only if scheme stability >= 0.60 across uncertainty draws.

## INDUSTRIX mapping
- Engineering substance: chemistry, process library, TEA, uncertainty, tests.
- Practical value: ranked scheme plus action, not an AI score.
- Novelty: Li/Br/Sr/K/B/I co-product portfolio + experiment selection + local
Russian-data deployment.
- Testability: 12-16 week archive-to-lab-to-bench workflow with explicit gates.
