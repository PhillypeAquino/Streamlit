import streamlit as st
import pandas as pd

from utils.data import load_demo_data, filter_data, compute_kpis
from filters.controls import draw_filters
from components.layout import page_header, kpi_row
from components.charts import timeseries_sales, bar_by_category, heatmap_category_month

def main():
    st.set_page_config(page_title="Dashboard • Passo 1", layout="wide")

    # 1) Dados de exemplo (sintético)
    df = load_demo_data()

    # 2) Filtros (usam valores únicos do DF para opções)
    criteria = draw_filters(df)

    # 3) Aplicar filtros
    df_f = filter_data(df, criteria)

    # 4) Header + KPIs
    page_header("Resumo Geral", "Streamlit + Altair (modelo genérico)")
    kpis = compute_kpis(df_f)
    kpi_row(kpis)

    # 5) Charts
    st.altair_chart(timeseries_sales(df_f), use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(bar_by_category(df_f), use_container_width=True)
    with col2:
        st.altair_chart(heatmap_category_month(df_f), use_container_width=True)

    # 6) Tabela filtrada (debug/validação)
    with st.expander("Ver dados filtrados"):
        st.dataframe(df_f)

if __name__ == "__main__":
    main()
