from pathlib import Path

import folium
import geopandas as gpd

def visualize_map(
    gdf: gpd.GeoDataFrame,
    location: list[float] | None = None,
    zoom_start: int = 3,
    output_filename: str | Path | None = None,
) -> folium.Map:
    """Genera un mapa interactivo de Folium, adaptándose a las columnas disponibles."""
    if gdf.empty:
        raise ValueError("Cannot create a map from an empty GeoDataFrame.")
    if gdf.crs is None:
        raise ValueError("The GeoDataFrame must have a defined CRS to create a map.")
    map_data = gdf.to_crs("EPSG:4326")
    if location is None:
        center = map_data.geometry.union_all().centroid
        location = [center.y, center.x]

    m = folium.Map(location=location, zoom_start=zoom_start)
    
    property_candidates = (
        'NAME',
        'CONTINENT',
        'id',
        'tipo_zona',
        'valor_estimado',
        'area_km2',
        'distance_km',
    )
    cols = [
        col
        for col in property_candidates
        if col in map_data.columns
    ]
    if not cols:
        cols = [col for col in map_data.columns if col != map_data.geometry.name]

    geojson = folium.GeoJson(map_data, name="Features")
    if cols:
        folium.features.GeoJsonTooltip(fields=cols, aliases=cols).add_to(geojson)
        folium.features.GeoJsonPopup(fields=cols, aliases=cols).add_to(geojson)
    geojson.add_to(m)

    if output_filename is not None:
        output_path = Path(output_filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        m.save(str(output_path))

    return m
