# Contenido definitivo para el análisis con currying
import geopandas as gpd

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

print("Archivo src/analysis.py creado.")
