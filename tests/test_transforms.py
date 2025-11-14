# Prueba que el cálculo de área funcione
import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from src.transforms import calculate_area_km2

@pytest.fixture
def sample_gdf() -> gpd.GeoDataFrame:
    poly = Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])
    gdf = gpd.GeoDataFrame({'id': [1], 'geometry': [poly]}, crs='EPSG:4326')
    return gdf

def test_calculate_area_km2_creates_column(sample_gdf):
    result_gdf = calculate_area_km2(sample_gdf)
    assert 'area_km2' in result_gdf.columns

print("Archivo 'tests/test_transforms.py' CREADO.")
