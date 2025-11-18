import streamlit as st
import pandas as pd
import plotly.express as px

# ============================
#   CARGA DE DATOS
# ============================
@st.cache_data
def load_data():
    df = pd.read_csv("data/owid-co2-data.csv")
    return df

df = load_data()

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

st.plotly_chart(fig1, use_container_width=True)

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
st.plotly_chart(fig2, use_container_width=True)
