# Modulo para visualizar mapas
from pathlib import Path

import folium
import geopandas as gpd

from src.analysis import DISTANCE_BANDS


BAND_COLORS = dict(zip(DISTANCE_BANDS, ('#17365d', '#326a96', '#83b7d2')))


def visualize_map(
    gdf: gpd.GeoDataFrame,
    location: list | None = None,
    zoom_start: int = 3,
    output_filename: str | Path | None = None,
    *,
    tiles: str | None = 'OpenStreetMap',
    reference_point: tuple[float, float] | None = None,
):
    """Genera un mapa interactivo de Folium, adaptándose a las columnas disponibles."""
    if gdf.empty:
        return
    gdf = gdf.to_crs('EPSG:4326') if gdf.crs is not None else gdf
    west, south, east, north = gdf.total_bounds
    if location is None:
        location = [(south + north) / 2, (west + east) / 2]

    m = folium.Map(location=location, zoom_start=zoom_start, tiles=tiles, control_scale=True)

    labels = {
        'nomgeo': 'Municipio', 'cvegeo': 'Clave INEGI',
        'NAME': 'Nombre', 'CONTINENT': 'Continente',
        'id': 'Zona', 'tipo_zona': 'Tipo de zona', 'valor_estimado': 'Valor estimado',
        'area_km2': 'Área (km²)', 'distance_km': 'Distancia al centro de distribución (km)',
        'distance_band': 'Grupo de distancia',
    }
    fields = [field for field in labels if field in gdf.columns]
    aliases = [labels[field] for field in fields]
    metrics = [field for field in ('area_km2', 'distance_km') if field in gdf.columns]
    style = {}
    if 'distance_band' in gdf.columns:
        style = {
            'style_function': lambda feature: {
                'fillColor': BAND_COLORS[feature['properties']['distance_band']],
                'fillOpacity': 0.82, 'color': '#fff', 'weight': 1.5,
            },
            'highlight_function': lambda feature: {'color': '#13283e', 'weight': 3},
        }
        legend = ''.join(
            f'<li><span style="display:inline-block;width:12px;height:12px;'
            f'margin-right:8px;background:{color}"></span>{label}</li>'
            for label, color in BAND_COLORS.items()
        )
        m.get_root().html.add_child(folium.Element(
            '<style>.folium-map{background:#eaf0f4}</style>'
            '<aside style="position:fixed;top:12px;right:12px;z-index:1000;background:#fff;'
            'color:#17365d;padding:12px 16px;border-radius:8px;'
            'box-shadow:0 1px 6px #0003;font:14px/1.5 system-ui">'
            '<strong>Colima · Distancia al centro</strong>'
            f'<ul style="list-style:none;padding:0;margin:6px 0 0">{legend}</ul>'
            '<small>Fuente cartográfica · INEGI</small></aside>'
        ))
    folium.GeoJson(
        gdf.round(dict.fromkeys(metrics, 2)).to_json(),
        tooltip=folium.GeoJsonTooltip(fields=fields, aliases=aliases) if fields else None,
        popup=folium.GeoJsonPopup(fields=fields, aliases=aliases) if fields else None,
        **style,
    ).add_to(m)

    if reference_point is not None:
        latitude, longitude = reference_point
        folium.CircleMarker(
            reference_point, radius=6, color='#fff', weight=2,
            fill=True, fill_color='#9a3412', fill_opacity=1,
            tooltip='Centro de distribución hipotético',
        ).add_to(m)
        m.fit_bounds(
            [[min(south, latitude), min(west, longitude)],
             [max(north, latitude), max(east, longitude)]],
            padding=(24, 24), max_zoom=12,
        )

    if output_filename is not None:
        output = Path(output_filename)
        output.parent.mkdir(parents=True, exist_ok=True)
        m.save(str(output))
    return m
