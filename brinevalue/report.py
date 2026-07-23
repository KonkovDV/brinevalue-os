"""Explainable HTML report for a single stream."""
DECISION_RU = {"no_go": "NO-GO (не инвестировать)", "lab": "ЛАБОРАТОРНАЯ ПРОВЕРКА",
               "pilot": "ПИЛОТ", "scale": "МАСШТАБИРОВАНИЕ"}


def html_report(res, brine, sens=None, doe=None):
    b = res["best"]; rub = lambda x: f"{x:,.0f}".replace(",", " ") if x is not None else "-"
    rows = "".join(
        f"<tr><td>{r['scheme']}</td><td>{r['recovery']}</td><td>{rub(r['npv_rub'])}</td>"
        f"<td>{rub(r['capex_rub'])}</td><td>{rub(r['opex_rub_yr'])}</td>"
        f"<td>{r.get('prod_cost_usd_t') or '-'}</td><td>{r.get('roroi')}</td></tr>" for r in res["ranked"])
    si = res["scaling_index"]
    si_html = "".join(f"<li>{k}: SI={v} {'⚠ риск' if v>0 else 'ok'}</li>" for k, v in si.items())
    sens_html = ""
    if sens:
        sens_html = "<h3>Чувствительность NPV (эластичность)</h3><ul>" + \
            "".join(f"<li>{k}: {v}</li>" for k, v in sens["elasticity"].items()) + "</ul>"
    doe_html = ""
    if doe:
        doe_html = "<h3>План лабораторных опытов (активное планирование)</h3><ol>" + \
            "".join(f"<li>{e['experiment']} → ↓шум NPV до {rub(e['npv_std_after'])} руб</li>" for e in doe["plan"]) + "</ol>"
    return f"""<!doctype html><html lang=ru><meta charset=utf-8>
<title>BrineValue OS - {brine.name}</title>
<style>body{{font-family:system-ui,Arial;margin:40px;color:#111;max-width:1000px}}
h1{{margin:0}}table{{border-collapse:collapse;width:100%;margin:16px 0}}
td,th{{border:1px solid #ccc;padding:6px 10px;text-align:left;font-size:13px}}
.badge{{display:inline-block;padding:6px 14px;border-radius:8px;color:#fff;font-weight:700}}
.scale{{background:#0a4}}.pilot{{background:#2f6fe0}}.lab{{background:#e59b00}}.no_go{{background:#c33}}
.muted{{color:#666;font-size:13px}}</style>
<h1>BrineValue OS <span class=muted>v0.2.0</span></h1>
<p class=muted>Поток: {brine.name} · дебит {brine.flow} м3/сут · TDS {brine.tds():.0f} мг/л · Mg/Li {res.get('mg_li')} · advisory, требует лаб-валидации</p>
<p>Решение: <span class="badge {res['decision']}">{DECISION_RU[res['decision']]}</span></p>
<p>Лучшая схема: <b>{b['scheme']}</b>, NPV {rub(b['npv_rub'])} руб, себестоимость {b.get('prod_cost_usd_t') or '-'} $/т Li2CO3, payback {b.get('payback_yr')} лет</p>
<p class=muted>Цепочка: {' → '.join(b['units'])}</p>
<h3>Риски солеотложения (SI, с коэфф. активности Davies)</h3><ul>{si_html}</ul>
<h3>Сравнение техсхем</h3>
<table><tr><th>Схема</th><th>Извлечение</th><th>NPV, руб</th><th>CAPEX</th><th>OPEX/год</th><th>$/т Li2CO3</th><th>ROROI</th></tr>{rows}</table>
{sens_html}{doe_html}
<p class=muted>BrineValue OS v0.2.0 · Apache-2.0 · локально, без передачи данных наружу · SI — скрининг, в пилоте PhreeqPy/Reaktoro-Pitzer</p></html>"""
