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
    fit_to_data = location is None
    if location is None:
        center = map_data.geometry.union_all().centroid
        location = [center.y, center.x]

    m = folium.Map(location=location, zoom_start=zoom_start, control_scale=True)
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

    zone_colors = {
        "Comercial": "#e76f51",
        "Residencial": "#457b9d",
    }

    def style_feature(feature: dict) -> dict:
        zone_type = feature.get("properties", {}).get("tipo_zona")
        color = zone_colors.get(zone_type, "#2a9d8f")
        return {
            "color": color,
            "fillColor": color,
            "fillOpacity": 0.45,
            "weight": 2,
        }

    geojson = folium.GeoJson(
        map_data,
        name="Zonas analizadas",
        style_function=style_feature,
        highlight_function=lambda _: {"weight": 4, "fillOpacity": 0.7},
    )
    if cols:
        folium.features.GeoJsonTooltip(fields=cols, aliases=cols).add_to(geojson)
        folium.features.GeoJsonPopup(fields=cols, aliases=cols).add_to(geojson)
    geojson.add_to(m)
    if fit_to_data:
        min_x, min_y, max_x, max_y = map_data.total_bounds
        m.fit_bounds([[min_y, min_x], [max_y, max_x]], padding=(20, 20))

    if output_filename is not None:
        output_path = Path(output_filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        m.save(str(output_path))

    return m
