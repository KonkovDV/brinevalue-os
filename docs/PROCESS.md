# PROCESS.md

Screening unit library. Literature citations are **analogs**, not code replications.

## Mass path
`mg/L × m³/d × recovery × 330 d/yr / 1e6 = kg/yr` (element basis).

Recovery fractions multiply sequentially for the **same** ion; independent ions stay
independent fractions of **feed** mass. Cannot create mass.

## Removals vs product
`remove` lowers downstream state and contributes `waste_removed_kg_yr`.
Ledger: feed = recovered + waste_removed + residual (±1e-6 closure).

## Evaporation
Concentrates ions, reduces flow, multiplies `preconcentrate`. DLE sorption/SX get a
modest screening boost `min(0.08, 0.025*log10(cf))`. Not a validated Alshammari replica.

## Honesty
- NF/RO “recovery” conflates passage × yield (see code notes).
- H2S/organics not removed by desulfurization unit.
- `li_carbonate_finish` is conversion proxy — not product certificate.
- Evidence grade: `screening_synthetic` on flowsheet results.
