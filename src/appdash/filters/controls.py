import streamlit as st
from datetime import date
from typing import Dict, Any
import pandas as pd

def _default_dates(df: pd.DataFrame):
    dmin = df["date"].min().date()
    dmax = df["date"].max().date()
    return dmin, dmax

def draw_filters(df) -> Dict[str, Any]:
    st.sidebar.header("Filtros")

    dmin, dmax = _default_dates(df)
    date_range = st.sidebar.date_input(
        "Período",
        value=(dmin, dmax),
        min_value=dmin,
        max_value=dmax,
        format="DD/MM/YYYY",
    )
    # Garante tupla (start, end)
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start, end = date_range
    else:
        start = end = date_range

    categories = sorted(df["category"].dropna().unique().tolist())
    regions = sorted(df["region"].dropna().unique().tolist())

    sel_cat = st.sidebar.multiselect("Categoria", categories, default=categories)
    sel_reg = st.sidebar.multiselect("Região", regions, default=regions)

    min_value = float(df["value"].min())
    max_value = float(df["value"].max())
    vmin, vmax = st.sidebar.slider(
        "Faixa de Valor",
        min_value=min_value, max_value=max_value,
        value=(min_value, max_value),
        step=1.0
    )

    return {
        "start": start,
        "end": end,
        "categories": sel_cat,
        "regions": sel_reg,
        "value_min": vmin,
        "value_max": vmax,
    }
