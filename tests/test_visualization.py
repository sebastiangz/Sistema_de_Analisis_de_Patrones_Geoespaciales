import folium
import geopandas as gpd
from shapely.geometry import Point

from src.visualization import visualize_map


def test_visualize_map_saves_html_in_wgs84(tmp_path):
    data = gpd.GeoDataFrame(
        {'nomgeo': ['Colima'], 'area_km2': [10.125], 'distance_km': [5.125]},
        geometry=[Point(-103.7, 19.24)],
        crs='EPSG:4326',
    ).to_crs('EPSG:3857')
    output = tmp_path / 'mapas' / 'colima.html'

    result = visualize_map(data, output_filename=output)

    assert isinstance(result, folium.Map)
    html = output.read_text(encoding='utf-8')
    assert all(value in html for value in ('Colima', 'distance_km', 'area_km2', '-103.7'))
    assert data['distance_km'].iloc[0] == 5.125
