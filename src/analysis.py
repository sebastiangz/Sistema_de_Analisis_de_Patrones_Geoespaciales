# Filtros y análisis geoespacial
from bisect import bisect_left

import geopandas as gpd
import pandas as pd


DISTANCE_LIMITS_KM = (20, 40)
DISTANCE_BANDS = ('Hasta 20 km', 'Más de 20 y hasta 40 km', 'Más de 40 km')

def filter_by_continent(continent_name: str):
    """Función Curried para filtrar el mapa mundial."""
    def inner_filter(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        return df[df['CONTINENT'] == continent_name].copy()
    return inner_filter

def get_top_n_areas(n: int = 5):
    """Función Curried para obtener el Top N de áreas."""
    def inner_analysis(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        if 'area_km2' not in df.columns:
            raise ValueError("El DataFrame debe tener la columna 'area_km2'.")
        return df.sort_values(by='area_km2', ascending=False).head(n)
    return inner_analysis

def filter_by_property(property_name: str, property_value: any):
    """Función Curried para filtrar el GeoJSON de bienes raíces."""
    def inner_filter(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        try:
            return df[df[property_name] == property_value].copy()
        except KeyError:
            return gpd.GeoDataFrame()
    return inner_filter

def filter_by_max_distance(max_km: float):
    """Devuelve un filtro que conserva filas a lo sumo a max_km."""
    def inner_filter(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        return df[df['distance_km'] <= max_km].copy()
    return inner_filter


def group_by_distance(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Asigna a cada municipio el grupo correspondiente a su distancia."""
    bands = df['distance_km'].map(
        lambda distance: DISTANCE_BANDS[bisect_left(DISTANCE_LIMITS_KM, distance)]
    )
    return df.assign(distance_band=bands)


def summarize_distance_groups(df: gpd.GeoDataFrame) -> pd.DataFrame:
    """Resume los municipios seleccionados y su superficie por grupo."""
    return (
        df.groupby('distance_band', sort=False)
        .agg(municipios=('area_km2', 'size'), area_total_km2=('area_km2', 'sum'))
        .reindex(DISTANCE_BANDS, fill_value=0)
        .rename_axis('grupo')
    )
