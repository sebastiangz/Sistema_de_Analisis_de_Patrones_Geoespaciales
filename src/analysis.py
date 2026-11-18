# Contenido definitivo para el análisis con currying
from typing import Any

import geopandas as gpd

def filter_by_continent(continent_name: str):
    """Función Curried para filtrar el mapa mundial."""
    def inner_filter(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        if 'CONTINENT' not in df.columns:
            raise ValueError("El DataFrame debe tener la columna 'CONTINENT'.")
        return df[df['CONTINENT'] == continent_name].copy()
    return inner_filter

def get_top_n_areas(n: int = 5):
    """Función Curried para obtener el Top N de áreas."""
    def inner_analysis(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
            raise ValueError("n debe ser un entero positivo.")
        if 'area_km2' not in df.columns:
            raise ValueError("El DataFrame debe tener la columna 'area_km2'.")
        return df.sort_values(by='area_km2', ascending=False).head(n).copy()
    return inner_analysis

def filter_by_property(property_name: str, property_value: Any):
    """Función Curried para filtrar el GeoJSON de bienes raíces."""
    def inner_filter(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        if property_name not in df.columns:
            raise ValueError(f"El GeoDataFrame debe tener la columna '{property_name}'.")
        return df[df[property_name] == property_value].copy()
    return inner_filter
