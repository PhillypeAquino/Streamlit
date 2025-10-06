from __future__ import annotations
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime

@st.cache_data(show_spinner=False)
def load_demo_data(rows: int = 5000) -> pd.DataFrame:
    """
    Gera dados sintéticos com colunas:
    - date (datetime64[ns])
    - category (A/B/C/D)
    - region (Norte/Sul/Leste/Oeste)
    - value (float)
    - qty (int)
    """
    rng = np.random.default_rng(90)
    dates = pd.date_range("2024-01-01", "2025-09-30", freq="D")
    categories = np.array(["A", "B", "C", "D"])
    regions = np.array(["Norte", "Sul", "Leste", "Oeste"])

    df = pd.DataFrame({
        "date": rng.choice(dates, size=rows, replace=True),
        "category": rng.choice(categories, size=rows, replace=True, p=[0.3,0.3,0.25,0.15]),
        "region": rng.choice(regions, size=rows, replace=True),
        "qty": rng.integers(1, 10, size=rows),
    })
    # valor com tendência + sazonalidade + ruído
    base = 50 + 10*np.sin(df["date"].dt.dayofyear * 2*np.pi / 365)
    noise = rng.normal(0, 10, size=rows)
    df["value"] = (base + noise) * df["qty"]
    df["value"] = df["value"].clip(lower=5).round(2)
    return df.sort_values("date").reset_index(drop=True)

def filter_data(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    start = pd.to_datetime(criteria["start"])
    end = pd.to_datetime(criteria["end"]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    mask = (
        (df["date"] >= start) &
        (df["date"] <= end) &
        (df["category"].isin(criteria["categories"])) &
        (df["region"].isin(criteria["regions"])) &
        (df["value"].between(criteria["value_min"], criteria["value_max"]))
    )
    return df.loc[mask].copy()

def compute_kpis(df: pd.DataFrame) -> dict:
    total = float(df["value"].sum()) if not df.empty else 0.0
    pedidos = int(df["qty"].sum()) if not df.empty else 0
    ticket = float(total / pedidos) if pedidos else 0.0

    # delta simples vs. 30 dias anteriores (se possível)
    if not df.empty:
        end = df["date"].max()
        start = end - pd.Timedelta(days=30)
        cur = df[(df["date"] > start) & (df["date"] <= end)]["value"].sum()
        prev = df[(df["date"] > start - pd.Timedelta(days=30)) & (df["date"] <= start)]["value"].sum()
        delta = (cur - prev) / prev * 100 if prev else 0.0
    else:
        delta = 0.0

    return {
        "Receita Total": {"value": f"R$ {total:,.2f}", "delta": f"{delta:+.1f}% vs. 30d"},
        "Pedidos": {"value": f"{pedidos:,}", "delta": None},
        "Ticket Médio": {"value": f"R$ {ticket:,.2f}", "delta": None},
    }
