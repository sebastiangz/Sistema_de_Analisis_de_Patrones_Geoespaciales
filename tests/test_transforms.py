# Prueba que el cálculo de área funcione
import pytest
import geopandas as gpd
from shapely.geometry import Point, Polygon
from src.transforms import calculate_area_km2, calculate_distance_km

@pytest.fixture
def sample_gdf() -> gpd.GeoDataFrame:
    poly = Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])
    gdf = gpd.GeoDataFrame({'id': [1], 'geometry': [poly]}, crs='EPSG:4326')
    return gdf

def test_calculate_area_km2_creates_column(sample_gdf):
    result_gdf = calculate_area_km2(sample_gdf)
    assert result_gdf['area_km2'].iloc[0] == pytest.approx(1_224_832, rel=0.001)
    assert 'area_km2' not in sample_gdf.columns
    assert result_gdf.geometry.equals(sample_gdf.geometry)


def test_calculate_distance_km_preserves_input():
    source = gpd.GeoDataFrame(geometry=[Point(0, 0), Point(1, 0)], crs='EPSG:4326')
    source = source.to_crs('EPSG:3857')
    result = calculate_distance_km(source, longitude=0, latitude=0)

    assert result['distance_km'].tolist() == pytest.approx([0, 111.31949])
    assert 'distance_km' not in source.columns
    assert result.geometry.equals(source.geometry)
