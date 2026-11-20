# Modulo para transformaciones puras
import geopandas as gpd
from pyproj import Geod


EQUAL_AREA_CRS = 'EPSG:6933'

def calculate_area_km2(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Función Pura: Calcula el área y la añade como nueva columna."""
    df_copy = df.copy()
    df_copy['area_km2'] = df_copy.geometry.to_crs(EQUAL_AREA_CRS).area / 1_000_000
    return df_copy

def calculate_distance_km(df: gpd.GeoDataFrame, longitude: float, latitude: float) -> gpd.GeoDataFrame:
    """Calcula la distancia geodésica desde un punto WGS84 al centroide."""
    centroids = df.geometry.to_crs(EQUAL_AREA_CRS).centroid.to_crs('EPSG:4326')
    _, _, meters = Geod(ellps='WGS84').inv(
        [longitude] * len(df), [latitude] * len(df),
        centroids.x.to_list(), centroids.y.to_list(),
    )
    return df.assign(distance_km=[value / 1_000 for value in meters])
