# -*- coding: utf-8 -*-
"""Script limpio para generar mapas de emisiones CO2 por país.

Este archivo reemplaza la versión exportada desde Colab y elimina
magias de notebook. Usa el shapefile incluido en geopandas
(`naturalearth_lowres`) y el CSV `data/owid-co2-data.csv`.
Genera archivos HTML con los mapas (uno por año).
"""

import os
import sys
import geopandas as gpd
import pandas as pd
import plotly.express as px


def load_world_master():
    # Intentar usar el dataset incluido en geopandas; si la versión
    # de geopandas del contenedor no expone `datasets`, usar
    # un GeoJSON público (que incluye ISO_A3).
    try:
        # algunas versiones antiguas de geopandas tienen datasets.get_path
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    except Exception:
        # Fallback: GeoJSON público con ISO_A3
        url = 'https://datahub.io/core/geo-countries/r/countries.geojson'
        world = gpd.read_file(url)

    # Normalizar columna de código ISO3 (puede llamarse 'iso_a3', 'ISO_A3',
    # o 'ISO3166-1-Alpha-3' dependiendo de la fuente)
    if 'iso_a3' in world.columns:
        world = world.rename(columns={'iso_a3': 'code'})
    elif 'ISO_A3' in world.columns:
        world = world.rename(columns={'ISO_A3': 'code'})
    elif 'ISO3166-1-Alpha-3' in world.columns:
        world = world.rename(columns={'ISO3166-1-Alpha-3': 'code'})
    elif 'iso' in world.columns:
        world = world.rename(columns={'iso': 'code'})

    world['code'] = world['code'].astype(str).str.upper()

    # Intentar nombres estándar
    name_col = 'name' if 'name' in world.columns else ('ADMIN' if 'ADMIN' in world.columns else 'country')

    world_master = (
        world[[ 'code', name_col, 'geometry']]
        .drop_duplicates(subset=['code'])
        .rename(columns={name_col: 'country'})
        .set_index('code')
    )

    # Asegurar índices únicos (puede haber múltiples geometrías por el mismo ISO)
    world_master = world_master[~world_master.index.duplicated(keep='first')]

    return world_master


def load_emissions(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV de emisiones no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)

    # Columnas esperadas en owid-co2-data: 'iso_code', 'year', 'co2'
    if 'iso_code' in df.columns:
        df = df.rename(columns={'iso_code': 'code'})
    elif 'Code' in df.columns:
        df = df.rename(columns={'Code': 'code'})

    if 'year' not in df.columns:
        # intentar detectar la columna año si tiene otro nombre
        for c in df.columns:
            if c.lower() == 'year':
                df = df.rename(columns={c: 'year'})
                break

    # Encontrar columna de emisiones CO2
    co2_candidates = [c for c in df.columns if c.lower() == 'co2' or 'co2' in c.lower()]
    if len(co2_candidates) == 0:
        # buscar primera columna numérica que no sea country/code/year
        candidates = [c for c in df.columns if c not in ('country', 'code', 'year')]
        co_col = None
        for c in candidates:
            if pd.api.types.is_numeric_dtype(df[c]):
                co_col = c
                break
        if co_col is None:
            raise ValueError('No se encontró columna de emisiones CO2 en el CSV')
    else:
        co_col = co2_candidates[0]


    df = df.rename(columns={co_col: 'co2'})

    # Si hay columnas duplicadas con el mismo nombre (p. ej. varias columnas
    # que contienen 'co2' renombradas a 'co2'), consolidarlas tomando el
    # primer valor no nulo por fila.
    from collections import Counter
    col_counts = Counter(df.columns.tolist())
    dupes = [c for c, cnt in col_counts.items() if cnt > 1]
    for d in dupes:
        # localizar todas las columnas con nombre d
        idxs = [i for i, c in enumerate(df.columns) if c == d]
        if len(idxs) <= 1:
            continue
        # combinar por primera no-nula a lo largo de las columnas duplicadas
        combined = df.iloc[:, idxs].bfill(axis=1).iloc[:, 0]
        # eliminar las columnas duplicadas y asignar la combinada
        cols_to_drop = [df.columns[i] for i in idxs[1:]]
        df = df.drop(columns=cols_to_drop)
        df[d] = combined

    # Normalizar códigos
    if 'code' in df.columns:
        df['code'] = df['code'].astype(str).str.upper()
        df = df[df['code'].str.len() == 3]

    # Mantener columnas relevantes
    keep = [c for c in ('country', 'code', 'year', 'co2') if c in df.columns]
    return df[keep]


def make_co2_map(world_master, df_co2, year):
    co2_year = (
        df_co2[df_co2['year'] == year]
        .groupby('code', as_index=False)['co2']
        .sum()
        .set_index('code')
    )

    world_y = world_master.join(co2_year, how='left')

    g_with = world_y[world_y['co2'].notna()].reset_index()
    g_no = world_y[world_y['co2'].isna()].reset_index()

    # GeoJSON con propiedades: usar reset_index para que 'code' sea una propiedad
    geojson_world = world_master.reset_index()[['code', 'country', 'geometry']].__geo_interface__

    fig = px.choropleth(
        g_with,
        geojson=geojson_world,
        locations='code',
        color='co2',
        hover_name='country',
        featureidkey='properties.code',
        projection='natural earth',
        color_continuous_scale='Reds'
    )

    fig_grey = px.choropleth(
        g_no,
        geojson=geojson_world,
        locations='code',
        featureidkey='properties.code',
        color_discrete_sequence=['#d0d0d0'],
        hover_name='country',
        projection='natural earth'
    )

    for trace in fig_grey.data:
        trace.showlegend = False
        fig.add_trace(trace)

    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(
        title_text=f'CO₂ emissions by country in {year}',
        title_x=0.5,
        width=900,
        height=600
    )

    return fig


def main():
    world_master = load_world_master()
    csv_path = os.path.join('data', 'owid-co2-data.csv')
    try:
        df = load_emissions(csv_path)
    except Exception as e:
        print(f"Error cargando CSV de emisiones: {e}")
        sys.exit(1)

    years = [1751, 1851, 1951, 2024]
    for y in years:
        try:
            fig = make_co2_map(world_master, df, y)
            out_html = f'map_co2_{y}.html'
            fig.write_html(out_html)
            print(f"Guardado mapa {out_html}")
        except Exception as e:
            print(f"Error generando mapa para {y}: {e}")


if __name__ == '__main__':
    main()