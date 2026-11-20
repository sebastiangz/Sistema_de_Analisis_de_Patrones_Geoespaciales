# Prueba que los filtros curried funcionen
import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from src.analysis import filter_by_property, get_top_n_areas

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


def test_filter_by_property_is_curried_and_does_not_mutate_input(analysis_fixture):
    filter_commercial = filter_by_property("tipo_zona", "Comercial")

    result = filter_commercial(analysis_fixture)

    assert result["id"].tolist() == ["A", "C"]
    assert len(analysis_fixture) == 2
    assert result is not analysis_fixture


def test_filter_by_property_reports_missing_column(analysis_fixture):
    with pytest.raises(ValueError, match="missing|columna"):
        filter_by_property("unknown", "value")(analysis_fixture)


def test_get_top_n_areas_rejects_non_positive_count():
    with pytest.raises(ValueError, match="positivo"):
        get_top_n_areas(0)(gpd.GeoDataFrame())
