# Modulo para visualizar mapas
from pathlib import Path

import folium
import geopandas as gpd

def visualize_map(gdf: gpd.GeoDataFrame, location: list = None, zoom_start: int = 3, output_filename: str = None):
    """Genera un mapa interactivo de Folium, adaptándose a las columnas disponibles."""
    if gdf.empty:
        return
    gdf = gdf.to_crs('EPSG:4326') if gdf.crs is not None else gdf
    west, south, east, north = gdf.total_bounds
    if location is None:
        location = [(south + north) / 2, (west + east) / 2]

    m = folium.Map(location=location, zoom_start=zoom_start)
    
    labels = {
        'nomgeo': 'Municipio', 'cvegeo': 'Clave INEGI',
        'NAME': 'Nombre', 'CONTINENT': 'Continente',
        'id': 'Zona', 'tipo_zona': 'Tipo de zona', 'valor_estimado': 'Valor estimado',
        'area_km2': 'Área (km²)', 'distance_km': 'Distancia al centro de distribución (km)',
    }
    fields = [field for field in labels if field in gdf.columns]
    aliases = [labels[field] for field in fields]
    metrics = [field for field in ('area_km2', 'distance_km') if field in gdf.columns]
    folium.GeoJson(
        gdf.round(dict.fromkeys(metrics, 2)).to_json(),
        tooltip=folium.GeoJsonTooltip(fields=fields, aliases=aliases) if fields else None,
        popup=folium.GeoJsonPopup(fields=fields, aliases=aliases) if fields else None,
    ).add_to(m)

    if output_filename is not None:
        output = Path(output_filename)
        output.parent.mkdir(parents=True, exist_ok=True)
        m.save(str(output))
    return m
