app_ejercicio.py

import os
import streamlit as st
import streamlit as st
import plotly.express as px

from ejercicio_co2 import load_world_master, load_emissions, make_co2_map


@st.cache_data
def load_data(csv_path: str):
    return load_emissions(csv_path)


st.title("Emisiones de CO₂ en el mundo — Explorer")
st.write("Interfaz interactiva que muestra mapas y gráficos basados en el dataset de OWID.")

csv_path = "data/owid-co2-data.csv"
try:
    df = load_data(csv_path)
except Exception as e:
    st.error(f"No se pudo cargar el CSV de emisiones: {e}")
    st.stop()

world_master = load_world_master()

# Sidebar controls
st.sidebar.header("Controles")
years = sorted(df['year'].dropna().unique().astype(int).tolist())
year = st.sidebar.select_slider("Selecciona el año", options=years, value=years[-1])

per_capita = st.sidebar.checkbox("Mostrar per cápita (co2 per capita)", value=False)

# If per_capita selected, we need to compute co2 per capita if column exists
if per_capita and 'co2_per_capita' not in df.columns and 'co2_per_capita' not in df.columns:
    st.sidebar.info("El dataset no contiene columna 'co2_per_capita'. Se mostrará total de CO2.")
import streamlit as st
import plotly.express as px

from ejercicio_co2 import load_world_master, load_emissions, make_co2_map


@st.cache_data
def load_data(csv_path: str):
    return load_emissions(csv_path)


def main():
    st.title("Emisiones de CO₂ en el mundo — Explorer")
    st.write("Interfaz interactiva que muestra mapas y gráficos basados en el dataset de OWID.")

    # Mostrar enlace local para abrir la app (útil cuando se ejecuta remotamente)
    host = os.environ.get('STREAMLIT_SERVER_HOST', os.environ.get('HOST', 'localhost'))
    port = os.environ.get('STREAMLIT_SERVER_PORT', os.environ.get('PORT', '8501'))
    app_url = f"http://{host}:{port}"
    st.sidebar.markdown(f"<a href=\"{app_url}\" target=\"_blank\">Abrir la app en {app_url}</a>", unsafe_allow_html=True)

    csv_path = "data/owid-co2-data.csv"
    try:
        df = load_data(csv_path)
    except Exception as e:
        st.error(f"No se pudo cargar el CSV de emisiones: {e}")
        st.stop()

    world_master = load_world_master()

    # Sidebar controls
    st.sidebar.header("Controles")
    years = sorted(df['year'].dropna().unique().astype(int).tolist())
    year = st.sidebar.select_slider("Selecciona el año", options=years, value=years[-1])

    per_capita = st.sidebar.checkbox("Mostrar per cápita (co2 per capita)", value=False)

    # Map
    st.subheader(f"Mapa mundial de emisiones CO₂ — {year}")
    try:
        fig = make_co2_map(world_master, df, int(year))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generando el mapa: {e}")

    # Top 10 bar chart
    st.subheader(f"Top 10 países emisores en {year}")
    df_year = df[df['year'] == int(year)]
    if per_capita and 'co2_per_capita' in df_year.columns:
        value_col = 'co2_per_capita'
    else:
        value_col = 'co2'

    df_top10 = df_year.sort_values(value_col, ascending=False).head(10)
    if len(df_top10) == 0:
        st.info("No hay datos para el año seleccionado.")
    else:
        fig_bar = px.bar(df_top10, x='country', y=value_col, title=f'Top 10 emisores ({value_col}) in {year}')
        st.plotly_chart(fig_bar, use_container_width=True)

    st.write("Mapas guardados previamente: `map_co2_1751.html`, `map_co2_1851.html`, `map_co2_1951.html`, `map_co2_2024.html`.")
    st.markdown("Para abrir los HTML generados en el navegador, sirve el directorio con `python3 -m http.server 8000` y abre los enlaces:")
    st.markdown("- `http://localhost:8000/map_co2_1751.html`\n- `http://localhost:8000/map_co2_1851.html`\n- `http://localhost:8000/map_co2_1951.html`\n- `http://localhost:8000/map_co2_2024.html`")


if __name__ == '__main__':
    main()
