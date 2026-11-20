# Prueba que la carga de datos funcione
from pathlib import Path

import geopandas as gpd
from src.geospatial import load_geojson

DATASET = Path(__file__).resolve().parents[1] / 'data/input/colima.geojson'

def test_load_geojson_returns_geodataframe():
    result_gdf = load_geojson(str(DATASET))
    assert isinstance(result_gdf, gpd.GeoDataFrame)
    assert result_gdf.crs.to_epsg() == 6365
    assert result_gdf['cvegeo'].nunique() == len(result_gdf) == 10
    assert set(result_gdf['cve_ent']) == {'06'}

print("Archivo 'tests/test_geospatial.py' CREADO.")
