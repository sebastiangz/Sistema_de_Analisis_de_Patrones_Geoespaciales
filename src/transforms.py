# Modulo para transformaciones puras
import geopandas as gpd
from shapely.geometry import Point

def calculate_area_km2(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Función Pura: Calcula el área y la añade como nueva columna."""
    df_copy = df.copy()
    df_copy['area_km2'] = df_copy.geometry.to_crs('EPSG:3395').area / 1_000_000
    return df_copy


def calculate_distance_from_point_km(
    df: gpd.GeoDataFrame, reference_point: tuple[float, float]
) -> gpd.GeoDataFrame:
    """Add centroid-to-reference distances in kilometers without modifying df.

    ``reference_point`` is a (longitude, latitude) pair in EPSG:4326.
    """
    if df.crs is None:
        raise ValueError("The GeoDataFrame must have a defined CRS.")

    reference = gpd.GeoDataFrame(
        geometry=[Point(reference_point)], crs="EPSG:4326"
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

print("Archivo src/transforms.py creado.")
