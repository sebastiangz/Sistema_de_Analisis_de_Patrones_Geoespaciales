from math import isfinite

import geopandas as gpd
from pyproj import Geod


EQUAL_AREA_CRS = 'EPSG:6933'

def calculate_area_km2(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Función Pura: Calcula el área y la añade como nueva columna."""
    if df.crs is None:
        raise ValueError("The GeoDataFrame must have a defined CRS.")
    df_copy = df.copy()
    df_copy['area_km2'] = df_copy.geometry.to_crs(EQUAL_AREA_CRS).area / 1_000_000
    return df_copy

def calculate_distance_from_point_km(
    df: gpd.GeoDataFrame, reference_point: tuple[float, float]
) -> gpd.GeoDataFrame:
    """Add centroid-to-reference distances in kilometers without modifying df.

    ``reference_point`` is a (longitude, latitude) pair in EPSG:4326.
    """
    if df.crs is None:
        raise ValueError("The GeoDataFrame must have a defined CRS.")
    try:
        coordinates = tuple(reference_point)
    except TypeError as error:
        raise ValueError("reference_point must contain longitude and latitude.") from error
    if len(coordinates) != 2:
        raise ValueError("reference_point must contain longitude and latitude.")

    try:
        longitude, latitude = (float(value) for value in coordinates)
    except (TypeError, ValueError) as error:
        raise ValueError("reference_point must contain numeric longitude and latitude.") from error

    if (
        not isfinite(longitude)
        or not isfinite(latitude)
        or not -180 <= longitude <= 180
        or not -90 <= latitude <= 90
    ):
        raise ValueError("reference_point must contain valid longitude and latitude.")

    centroids = df.geometry.to_crs(EQUAL_AREA_CRS).centroid.to_crs('EPSG:4326')
    _, _, meters = Geod(ellps='WGS84').inv(
        [longitude] * len(df), [latitude] * len(df),
        centroids.x.to_list(), centroids.y.to_list(),
    )
    return df.assign(distance_km=[value / 1_000 for value in meters])

def calculate_distance_km(df: gpd.GeoDataFrame, longitude: float, latitude: float) -> gpd.GeoDataFrame:
    """Calcula la distancia geodésica desde un punto WGS 84 al centroide."""
    return calculate_distance_from_point_km(df, (longitude, latitude))
