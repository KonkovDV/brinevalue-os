# INDUSTRIX 2026 submission/pilot checklist

## Before showing the MVP
- [ ] one named operational owner and one first stream;
- [ ] current process, loss/cost, input data, algorithm, action, KPI, pilot;
- [ ] repository opens with one command and includes a reproducible demo;
- [ ] every number tagged synthetic, literature, lab, company-reported or field;
- [ ] no unverified “battery-grade”, savings or field-accuracy claims.

## Demo script
1. Load 30-100 historical analyses and flow.
2. Reject a bad charge balance instead of hiding it.
3. Show scaling risks and Mg/Li.
4. Rank flowsheets and show Pareto + Li2CO3 price scenarios.
5. Show `P(NPV>0)`, scheme stability and the 3-5 experiments that reduce risk.
6. Produce a no-go/lab/pilot recommendation with mass-balance closure.

## Pilot go/no-go
The `pilot_gates()` function and `PILOT_PLAN.md` define the acceptance gates.
The product is not pilot-ready merely because a synthetic NPV is positive.
