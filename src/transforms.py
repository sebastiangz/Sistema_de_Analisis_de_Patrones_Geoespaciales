# Modulo para transformaciones puras
import geopandas as gpd

def calculate_area_km2(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Función Pura: Calcula el área y la añade como nueva columna."""
    df_copy = df.copy()
    df_copy['area_km2'] = df_copy.geometry.to_crs('EPSG:3395').area / 1_000_000
    return df_copy

print("Archivo src/transforms.py creado.")
