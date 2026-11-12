# Prueba que el cálculo de área funcione
import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.geometry import Point
from src.transforms import calculate_area_km2, calculate_distance_from_point_km

@pytest.fixture
def sample_gdf() -> gpd.GeoDataFrame:
    poly = Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])
    gdf = gpd.GeoDataFrame({'id': [1], 'geometry': [poly]}, crs='EPSG:4326')
    return gdf

def test_calculate_area_km2_creates_column(sample_gdf):
    result_gdf = calculate_area_km2(sample_gdf)
    assert 'area_km2' in result_gdf.columns


def test_calculate_distance_from_point_km_uses_centroid_and_preserves_input():
    gdf = gpd.GeoDataFrame(
        {
            'id': [1],
            'geometry': [Polygon([(0.9, -0.1), (1.1, -0.1), (1.1, 0.1), (0.9, 0.1)])],
        },
        crs='EPSG:4326',
    )

    result = calculate_distance_from_point_km(gdf, (0, 0))

    assert result.loc[0, 'distance_km'] == pytest.approx(111.3, abs=0.2)
    assert 'distance_km' not in gdf.columns
    assert result.crs == gdf.crs


def test_calculate_distance_from_point_km_requires_crs():
    gdf = gpd.GeoDataFrame({'geometry': [Point(1, 0)]})

    with pytest.raises(ValueError, match='defined CRS'):
        calculate_distance_from_point_km(gdf, (0, 0))


print("Archivo 'tests/test_transforms.py' CREADO.")
