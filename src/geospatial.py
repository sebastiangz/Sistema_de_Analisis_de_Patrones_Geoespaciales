# Modulo para cargar datos
from pathlib import Path

import geopandas as gpd


def load_geojson(filepath: str | Path) -> gpd.GeoDataFrame:
    """Load a geospatial dataset and let read errors surface to the caller."""
    return gpd.read_file(str(filepath))
