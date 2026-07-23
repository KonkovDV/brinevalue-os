"""Streamlit UI. streamlit run brinevalue/dashboard.py"""
try:
    import streamlit as st
except Exception:
    st = None
if st is not None:
    import pandas as pd
    from .io import synthetic_streams
    from .pipeline import analyze
    st.set_page_config(page_title="BrineValue OS", layout="wide")
    st.title("BrineValue OS v0.5.2 — скрининг пластовых вод (advisory)")
    st.caption("Не цифровой двойник. Не FEED. Не battery-grade. Данные demo — синтетические.")
    streams = synthetic_streams(8)
    idx = st.selectbox("Поток", range(len(streams)), format_func=lambda i: streams[i].name)
    b = streams[idx]; res = analyze(b)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Решение", res["decision"].upper()); c2.metric("Схема", res["best"]["scheme"])
    c3.metric("NPV, руб", f"{res['best']['npv_rub']:,}"); c4.metric("$/т Li2CO3", res["best"].get("prod_cost_usd_t"))
    st.subheader("Ранжирование схем"); st.dataframe(pd.DataFrame(res["ranked"]))
    st.subheader("План опытов"); st.table(pd.DataFrame(res["experiment_plan"]["plan"]))
    st.subheader("Ценовые сценарии Li2CO3"); st.line_chart(pd.DataFrame(res["price_scenarios"]).set_index("li2co3_usd_t"))
