import streamlit as st

def page_header(title: str, subtitle: str | None = None):
    st.title(title)
    if subtitle:
        st.caption(subtitle)

def kpi_row(kpis: dict):
    cols = st.columns(len(kpis))
    for col, (label, meta) in zip(cols, kpis.items()):
        with col:
            st.metric(label, meta["value"], meta.get("delta"))
