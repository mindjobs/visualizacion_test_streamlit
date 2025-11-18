import os
import streamlit as st
import pandas as pd
import plotly.express as px

# ============================
#   CARGA DE DATOS
# ============================
DATA_PATH = "data/owid-co2-data.csv"


@st.cache_data
def load_data(path: str):
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    return df


df = load_data(DATA_PATH)
if df is None:
    st.title("Visualización Interactiva de Emisiones de CO₂")
    st.error(
        "No se encontró el archivo de datos `data/owid-co2-data.csv`."
    )
    st.write(
        "Descarga el dataset desde Our World in Data y colócalo en la carpeta `data/`:\\n"
        "`https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv`"
    )
    st.write("Opciones:")
    st.markdown("- Crea la carpeta `data/` en el proyecto y descarga el CSV allí.")
    st.markdown(
        "- O ejecuta en tu terminal: `mkdir -p data && curl -L -o data/owid-co2-data.csv https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv`"
    )
    st.stop()

# ============================
#   TÍTULO
# ============================
st.title("Visualización Interactiva de Emisiones de CO₂")
st.write("""
Aplicación desarrollada para la Tarea 2 del curso de Visual Analytics.
Basada en los datos de Our World In Data.
""")

# ============================
#   SIDEBAR
# ============================
st.sidebar.header("Controles")
year = st.sidebar.slider(
    "Selecciona el año",
    int(df["year"].min()),
    int(df["year"].max()),
    2020
)

# ============================
#   FILTRO POR AÑO
# ============================
df_year = df[df["year"] == year]

# ============================
#   GRÁFICO 1: TOP 10
# ============================
st.subheader(f"Top 10 países emisores de CO₂ en {year}")
df_top10 = df_year.sort_values("co2", ascending=False).head(10)

fig1 = px.bar(
    df_top10,
    x="country",
    y="co2",
    title=f"Emisiones de CO₂ en {year}",
    labels={"co2": "CO₂ (millones de toneladas)", "country": "País"}
)

st.plotly_chart(fig1, width='stretch')

# ============================
#   MÁS GRÁFICOS (ejemplo)
# ============================
paises = st.sidebar.multiselect(
    "Selecciona países para comparar",
    df["country"].unique(),
    ["Chile", "Argentina", "Brazil"]
)

df_sel = df[df["country"].isin(paises)]

st.subheader("Serie de tiempo: comparación entre países")
fig2 = px.line(
    df_sel,
    x="year",
    y="co2",
    color="country",
    title="Emisiones de CO₂ a lo largo del tiempo"
)
st.plotly_chart(fig2, width='stretch')
