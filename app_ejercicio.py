app_ejercicio.py

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Cargar datos
@st.cache_data
def load_data():
    # Usa el mismo CSV que tu notebook, pero desde la carpeta data/
    df = pd.read_csv("data/owid-co2-data.csv")
    return df

df = load_data()

# 2. Título y descripción
st.title("Emisiones de CO₂ en el mundo")
st.write("App desarrollada para la Tarea 2 del Magíster en Data Science (UDD).")

# 3. Controles en el sidebar
st.sidebar.header("Controles")
year = st.sidebar.slider(
    "Selecciona el año",
    int(df["year"].min()),
    int(df["year"].max()),
    2020
)

# 4. Filtrar por año
df_year = df[df["year"] == year]

# 5. Gráfico ejemplo: Top 10 países por emisiones
st.subheader(f"Top 10 países emisores de CO₂ en {year}")
df_top10 = df_year.sort_values("co2", ascending=False).head(10)

fig_bar = px.bar(
    df_top10,
    x="country",
    y="co2",
    title=f"Emisiones de CO₂ en {year}",
    labels={"co2": "Emisiones de CO₂ (Mt)", "country": "País"}
)
st.plotly_chart(fig_bar, use_container_width=True)

# Aquí abajo vas pegando las otras visualizaciones que ya hiciste en tu notebook:
# - Serie de tiempo para un país
# - Comparación entre varios países
# - Mapa, etc.
