# CHEMISTRY.md

Screening-grade aqueous chemistry. Not PHREEQC/Pitzer. Not temperature-corrected.

## Units
| Quantity | Unit | Notes |
|---|---|---|
| Ion concentrations | mg/L | Assumed density ≈ 1 kg/L for mol/L conversion |
| Flow | m³/day | |
| Temperature | °C | Stored; **not** used in Ksp (Ksp @ 25 °C) |
| pH | — | Used only in simplified CO₃ from HCO₃ |
| Organics `org` | mg/L | Quality gate only; **not** a process removal |

## Formulas (with tests)

| Formula | Sense | Units | Source / assumption | Applicability | Test |
|---|---|---|---|---|---|
| `molar = mg/L / 1000 / MW` | Convert to mol/L | mol/L | Density≈1 | Screening | `test_ionic_strength_positive` |
| `I = 0.5 Σ m_i z_i²` | Ionic strength | mol/L | Standard | Screening | `test_ionic_strength_positive` |
| Davies γ | Activity coeff. | — | Davies 1938; valid ~I≤0.5 (USGS PHREEQC FAQ) | **Decision SI only if I≤0.5** | `test_davies_*`, `test_hypersaline_si_not_decision_grade` |
| Charge balance error % | QC | % | \|cat−an\|/(cat+an)·100 | >10% non-decision; >25% reject | `test_balance_fields`, `test_severe_balance_is_nogo` |
| SI = log10(IAP/Ksp) | Scaling screen | — | Ksp 25 °C constants | Flags only when `si_reliable` | `test_scaling_has_halite` |
| Mg/Li | Selectivity penalty driver | molar | Process correlations | Li>0 else 1e9 | `test_mg_li_ratio` |

## Limits (honest)
- Davies numerical clamp I≤6 is **overflow protection**, not validity extension.
- No H₂S speciation; desulfurization removes SO₄ fraction only.
- No organics/oil sorption fouling model beyond QC warnings.
- Hypersaline formation water: use Pitzer / PHREEQC / Reaktoro before pilot.
