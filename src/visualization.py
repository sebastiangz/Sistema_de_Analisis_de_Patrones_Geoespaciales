# Modulo para visualizar mapas
import folium
import geopandas as gpd

def visualize_map(gdf: gpd.GeoDataFrame, location: list = None, zoom_start: int = 3, output_filename: str = None):
    """Genera un mapa interactivo de Folium, adaptándose a las columnas disponibles."""
    if gdf.empty:
        return
    if location is None:
        try:
            center = gdf.unary_union.centroid
            location = [center.y, center.x]
        except Exception:
            location = [0, 0]

    m = folium.Map(location=location, zoom_start=zoom_start)
    
    cols = [col for col in ['NAME', 'CONTINENT', 'area_km2'] if col in gdf.columns]
    if not cols:
        cols = [col for col in ['id', 'tipo_zona', 'valor_estimado', 'area_km2'] if col in gdf.columns]

    if cols:
        folium.GeoJson(
            gdf,
            tooltip=folium.features.GeoJsonTooltip(fields=cols, aliases=cols),
            popup=folium.features.GeoJsonPopup(fields=cols, aliases=cols)
        ).add_to(m)

    return m

print("Archivo src/visualization.py creado.")
