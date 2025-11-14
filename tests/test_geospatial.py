# Prueba que la carga de datos funcione
import pytest
import geopandas as gpd
from src.geospatial import load_geojson

# Usamos una URL de prueba que sabemos que funciona
URL_DATA_GOOD = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"

def test_load_geojson_returns_geodataframe():
    result_gdf = load_geojson(URL_DATA_GOOD)
    assert isinstance(result_gdf, gpd.GeoDataFrame)
    assert not result_gdf.empty

print("Archivo 'tests/test_geospatial.py' CREADO.")
