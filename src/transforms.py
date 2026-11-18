# Modulo para transformaciones puras
import math

import geopandas as gpd
from shapely.geometry import Point


def _estimate_utm_crs(df: gpd.GeoDataFrame):
    if df.crs is None:
        raise ValueError("The GeoDataFrame must have a defined CRS.")

    metric_crs = df.estimate_utm_crs()
    if metric_crs is None:
        raise ValueError("Could not determine a suitable UTM CRS for the GeoDataFrame.")
    return metric_crs


def calculate_area_km2(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Función Pura: Calcula el área y la añade como nueva columna."""
    metric_crs = _estimate_utm_crs(df)
    df_copy = df.copy()
    df_copy["area_km2"] = df.to_crs(metric_crs).geometry.area / 1_000_000
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
        not math.isfinite(longitude)
        or not math.isfinite(latitude)
        or not -180 <= longitude <= 180
        or not -90 <= latitude <= 90
    ):
        raise ValueError("reference_point must contain valid longitude and latitude.")

    reference = gpd.GeoDataFrame(
        geometry=[Point(longitude, latitude)], crs="EPSG:4326"
    )
    metric_crs = reference.estimate_utm_crs()
    if metric_crs is None:
        raise ValueError("Could not determine a suitable UTM CRS for reference_point.")

    projected_df = df.to_crs(metric_crs)
    projected_reference = reference.to_crs(metric_crs).geometry.iloc[0]
    result = df.copy()
    result["distance_km"] = (
        projected_df.geometry.centroid.distance(projected_reference) / 1000
    )
    return result
