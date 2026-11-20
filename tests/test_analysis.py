# Prueba que los filtros curried funcionen
import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from src.analysis import (
    DISTANCE_BANDS,
    filter_by_max_distance,
    filter_by_property,
    get_top_n_areas,
    group_by_distance,
    summarize_distance_groups,
)

@pytest.fixture
def analysis_fixture() -> gpd.GeoDataFrame:
    # Datos de prueba para el análisis de bienes raíces
    poly1 = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    poly3 = Polygon([(2, 2), (2, 3), (3, 3), (3, 2)])
    data = {
        'id': ['A', 'C'],
        'tipo_zona': ['Comercial', 'Comercial'],
        'area_km2': [100.0, 200.0], # Áreas de prueba
        'geometry': [poly1, poly3]
    }
    return gpd.GeoDataFrame(data, crs='EPSG:4326')

def test_get_top_n_areas_curried(analysis_fixture):
    top_1_func = get_top_n_areas(n=1) # Probar currying
    result_gdf = top_1_func(analysis_fixture)
    assert len(result_gdf) == 1
    assert result_gdf['id'].iloc[0] == 'C'

def test_filter_by_max_distance_includes_boundary(analysis_fixture):
    source = analysis_fixture.assign(distance_km=[10, 20])
    result = filter_by_max_distance(10)(source)

    assert result['id'].tolist() == ['A']
    assert source['id'].tolist() == ['A', 'C']


def test_filter_by_property_selects_matching_rows(analysis_fixture):
    result = filter_by_property('id', 'C')(analysis_fixture)

    assert result['id'].tolist() == ['C']


def test_group_distances_and_summarize_selected_areas(analysis_fixture):
    source = analysis_fixture.iloc[[0, 0, 1, 1]].assign(distance_km=[20, 20.01, 40, 40.01])
    grouped = group_by_distance(source)

    near, middle, far = DISTANCE_BANDS
    assert grouped['distance_band'].tolist() == [near, middle, middle, far]
    assert 'distance_band' not in source.columns
    summary = summarize_distance_groups(grouped.iloc[:3])
    assert summary['municipios'].tolist() == [1, 2, 0]
    assert summary['area_total_km2'].tolist() == [100, 300, 0]
