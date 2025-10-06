import altair as alt
import pandas as pd

def timeseries_sales(df: pd.DataFrame) -> alt.Chart:
    base = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("yearmonth(date):T", title="Mês"),
        y=alt.Y("sum(value):Q", title="Receita (Σ)"),
        color=alt.Color("region:N", title="Região"),
        tooltip=[
            alt.Tooltip("yearmonthdate(date):T", title="Data"),
            alt.Tooltip("region:N", title="Região"),
            alt.Tooltip("sum(value):Q", title="Receita Σ", format=",.2f"),
        ],
    )
    return base.properties(title="Receita por Mês (por Região)").interactive()

def bar_by_category(df: pd.DataFrame) -> alt.Chart:
    base = alt.Chart(df).mark_bar().encode(
        x=alt.X("category:N", title="Categoria", sort="-y"),
        y=alt.Y("sum(value):Q", title="Receita (Σ)"),
        tooltip=[
            alt.Tooltip("category:N", title="Categoria"),
            alt.Tooltip("sum(value):Q", title="Receita Σ", format=",.2f"),
        ],
    )
    return base.properties(title="Receita por Categoria").interactive()

def heatmap_category_month(df: pd.DataFrame) -> alt.Chart:
    # Agregado por mês x categoria
    agg = df.assign(month=df["date"].dt.to_period("M").dt.to_timestamp())
    base = alt.Chart(agg).mark_rect().encode(
        x=alt.X("yearmonth(month):T", title="Mês"),
        y=alt.Y("category:N", title="Categoria"),
        color=alt.Color("sum(value):Q", title="Receita Σ"),
        tooltip=[
            alt.Tooltip("yearmonth(month):T", title="Mês"),
            alt.Tooltip("category:N", title="Categoria"),
            alt.Tooltip("sum(value):Q", title="Receita Σ", format=",.2f"),
        ],
    )
    return base.properties(title="Heatmap: Categoria x Mês").interactive()
