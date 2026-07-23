"""Explainable HTML report for a single stream (advisory screening)."""
DECISION_RU = {
    "no_go": "NO-GO (не инвестировать)",
    "lab": "ЛАБОРАТОРНАЯ ПРОВЕРКА",
    "pilot": "ПИЛОТ",
    "scale": "МАСШТАБИРОВАНИЕ",
}


def _si_item(k, v, meta):
    if v is None:
        return f"<li>{k}: SI=n/a (не decision-grade; I&gt;0.5 или модель вне области)</li>"
    flag = "⚠ риск" if v > 0 else "ok"
    return f"<li>{k}: SI={v} {flag}</li>"


def html_report(res, brine, sens=None, doe=None):
    b = res["best"]
    rub = lambda x: f"{x:,.0f}".replace(",", " ") if x is not None else "-"
    rows = "".join(
        f"<tr><td>{r['scheme']}</td><td>{r['recovery']}</td><td>{rub(r['npv_rub'])}</td>"
        f"<td>{rub(r['capex_rub'])}</td><td>{rub(r['opex_rub_yr'])}</td>"
        f"<td>{r.get('prod_cost_usd_t') or '-'}</td><td>{r.get('roroi')}</td></tr>"
        for r in res["ranked"]
    )
    si = res.get("scaling_index") or {}
    meta = res.get("si_meta") or {}
    si_html = "".join(_si_item(k, v, meta) for k, v in si.items())
    if meta.get("si_transparency"):
        si_html += "<li class=muted>transparency (не для решений): " + ", ".join(
            f"{k}={v}" for k, v in meta["si_transparency"].items()
        ) + "</li>"
    if meta.get("note"):
        si_html += f"<li class=muted>{meta['note']}</li>"
    sens_html = ""
    if sens:
        sens_html = (
            "<h3>Чувствительность NPV (эластичность, one-at-a-time)</h3><ul>"
            + "".join(f"<li>{k}: {v}</li>" for k, v in sens["elasticity"].items())
            + "</ul>"
        )
    doe_html = ""
    if doe:
        method = doe.get("method", "greedy_uncertainty_reduction")
        doe_html = (
            f"<h3>План лабораторных опытов ({method})</h3><ol>"
            + "".join(
                f"<li>{e['experiment']} → ↓шум NPV до {rub(e['npv_std_after'])} руб</li>"
                for e in doe["plan"]
            )
            + "</ol>"
        )
    grade = b.get("economics_grade", "screening_placeholder")
    sample = res.get("sample_grade", "unknown")
    synthetic = "synthetic" in str(brine.name).lower()
    data_tag = "СИНТЕТИЧЕСКИЕ ДАННЫЕ" if synthetic else "ВХОД ПОЛЬЗОВАТЕЛЯ (не промысловой архив)"
    return f"""<!doctype html><html lang=ru><meta charset=utf-8>
<title>BrineValue OS - {brine.name}</title>
<style>body{{font-family:system-ui,Arial;margin:40px;color:#111;max-width:1000px}}
h1{{margin:0}}table{{border-collapse:collapse;width:100%;margin:16px 0}}
td,th{{border:1px solid #ccc;padding:6px 10px;text-align:left;font-size:13px}}
.badge{{display:inline-block;padding:6px 14px;border-radius:8px;color:#fff;font-weight:700}}
.scale{{background:#0a4}}.pilot{{background:#2f6fe0}}.lab{{background:#e59b00}}.no_go{{background:#c33}}
.muted{{color:#666;font-size:13px}}.warn{{background:#fff3cd;padding:10px;border:1px solid #e0c36a}}</style>
<h1>BrineValue OS <span class=muted>v0.5.2</span></h1>
<p class="warn"><b>{data_tag}</b> · economics_grade={grade} · sample_grade={sample} ·
advisory screening · НЕ цифровой двойник · НЕ FEED · НЕ battery-grade · IRR не реализован</p>
<p class=muted>Поток: {brine.name} · дебит {brine.flow} м3/сут · TDS {brine.tds():.0f} мг/л · Mg/Li {res.get('mg_li')} ·
Ksp при 25°C (T brine={brine.temp}°C не корректирует SI)</p>
<p>Решение: <span class="badge {res['decision']}">{DECISION_RU[res['decision']]}</span>
<span class=muted>(raw NPV: {res.get('raw_decision')})</span></p>
<p>Лучшая схема (Pareto/NPV): <b>{b['scheme']}</b>, NPV {rub(b['npv_rub'])} руб,
себестоимость Li-allocated {b.get('prod_cost_usd_t') or '-'} $/т Li2CO3,
simple payback {b.get('simple_payback_yr') or b.get('payback_yr')} лет</p>
<p class=muted>Цепочка: {' -> '.join(b['units'])}</p>
<h3>Риски солеотложения (Davies SI; decision-grade только при I≤0.5)</h3><ul>{si_html}</ul>
<h3>Сравнение техсхем</h3>
<table><tr><th>Схема</th><th>Извлечение</th><th>NPV, руб</th><th>CAPEX</th><th>OPEX/год</th><th>$/т Li2CO3</th><th>ROROI</th></tr>{rows}</table>
{sens_html}{doe_html}
<p class=muted>BrineValue OS v0.5.2 · Apache-2.0 · intended local deploy ·
Pitzer/PHREEQC required before pilot SI · GitHub: KonkovDV/brinevalue-os</p></html>"""
