"""Streamlit interface for the geospatial analysis pipeline."""

import json
from pathlib import Path

import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium

from src.analysis import summarize_distance_groups
from src.geospatial import load_geojson
from src.pipeline import DATASET, REFERENCE_POINT, analyze_geodataframe
from src.visualization import visualize_map


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_ZONES = ROOT / "data/input/mapa.geojson"


def read_uploaded_geojson(contents: bytes) -> gpd.GeoDataFrame:
    """Read an uploaded RFC 7946 FeatureCollection without writing it to disk."""
    try:
        document = json.loads(contents)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("El archivo no contiene un JSON válido.") from error

    if not isinstance(document, dict) or document.get("type") != "FeatureCollection":
        raise ValueError("Sube un GeoJSON FeatureCollection en coordenadas WGS 84.")
    features = document.get("features")
    if not isinstance(features, list) or not features:
        raise ValueError("El GeoJSON no contiene entidades para analizar.")

    try:
        return gpd.GeoDataFrame.from_features(features, crs="EPSG:4326")
    except (TypeError, ValueError, KeyError) as error:
        raise ValueError("No se pudieron leer las geometrías del GeoJSON.") from error


def _reference_point_for_data(data: gpd.GeoDataFrame) -> tuple[float, float]:
    bounds = data.to_crs("EPSG:4326").total_bounds
    return (float((bounds[0] + bounds[2]) / 2), float((bounds[1] + bounds[3]) / 2))


def _show_resources() -> None:
    st.sidebar.divider()
    st.sidebar.markdown("**Proyecto y documentación**")
    st.sidebar.markdown(
        "[Repositorio](https://github.com/sebastiangz/Sistema_de_Analisis_de_Patrones_Geoespaciales) · "
        "[README](https://github.com/sebastiangz/Sistema_de_Analisis_de_Patrones_Geoespaciales/blob/main/README.md)"
    )
    st.sidebar.markdown(
        "[Presentación](https://github.com/sebastiangz/Sistema_de_Analisis_de_Patrones_Geoespaciales/blob/main/PRESENTACION_FINAL.md) · "
        "[Guion de video](https://github.com/sebastiangz/Sistema_de_Analisis_de_Patrones_Geoespaciales/blob/main/GUION_VIDEO_COMERCIAL.md)"
    )


def main() -> None:
    st.set_page_config(
        page_title="SAPG · Análisis geoespacial",
        page_icon="🗺️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
          .block-container {padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1500px;}
          [data-testid="stMetric"] {
            background: #14334b; color: #fff; border: 1px solid #244e68;
            padding: .8rem 1rem; border-radius: .75rem;
          }
          [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
            color: #fff !important;
          }
          [data-testid="stMetricLabel"] p {color: #d6e5ee !important;}
          [data-testid="stMetricValue"] {font-size: 1.35rem;}
          .sapg-subtitle {color: #506273; margin-top: -.5rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("🗺️ SAPG · Análisis de Patrones Geoespaciales")
    st.markdown(
        '<p class="sapg-subtitle">Explora cobertura municipal y analiza tus propios polígonos GeoJSON.</p>',
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Configuración")
        mode = st.radio(
            "Análisis",
            ("Cobertura municipal de Colima", "Analizar GeoJSON"),
            help="Elige el análisis de cobertura de Colima o carga tus propios polígonos.",
        )

    if mode == "Cobertura municipal de Colima":
        data = load_geojson(DATASET)
        with st.sidebar:
            radius = st.slider(
                "Radio desde el centro (km)",
                min_value=5,
                max_value=100,
                value=60,
                step=5,
            )
        try:
            result = analyze_geodataframe(
                data,
                reference_point=REFERENCE_POINT,
                max_distance_km=float(radius),
            )
        except ValueError as error:
            st.error(str(error))
            st.stop()
        map_view = visualize_map(
            result,
            reference_point=REFERENCE_POINT[::-1],
        )
        grouped_summary = summarize_distance_groups(result)
        title = "Cobertura municipal de Colima"
        description = (
            f"Municipios a menos de {radius} km del punto de referencia "
            "(distancia geodésica entre centroides)."
        )
    else:
        with st.sidebar:
            source = st.radio("Datos", ("Ejemplo incluido", "Subir GeoJSON"))
            uploaded = None
            if source == "Subir GeoJSON":
                uploaded = st.file_uploader(
                    "Archivo GeoJSON",
                    type=("geojson", "json"),
                    help="Se procesa en memoria; usa archivos GeoJSON WGS 84 confiables.",
                )

        if source == "Subir GeoJSON":
            if uploaded is None:
                st.info("Sube un archivo GeoJSON para configurar el análisis.")
                _show_resources()
                return
            try:
                data = read_uploaded_geojson(uploaded.getvalue())
            except ValueError as error:
                st.error(str(error))
                st.stop()
            source_name = uploaded.name
        else:
            data = load_geojson(SAMPLE_ZONES)
            source_name = "mapa.geojson"

        if data.empty:
            st.error("El conjunto de datos no contiene entidades.")
            st.stop()
        if data.crs is None:
            st.error("El conjunto de datos debe declarar su CRS.")
            st.stop()

        with st.sidebar:
            st.caption(f"Fuente: {source_name} · CRS: {data.crs}")
            zone_type = None
            if "tipo_zona" in data.columns:
                zone_types = sorted(data["tipo_zona"].dropna().astype(str).unique())
                selection = st.selectbox("Tipo de zona", ["Todas", *zone_types])
                zone_type = None if selection == "Todas" else selection
            default_top_n = min(5, len(data))
            top_n = st.number_input(
                "Máximo de zonas por área",
                min_value=1,
                max_value=len(data),
                value=default_top_n,
                step=1,
            )
            include_distance = st.checkbox("Calcular distancia a un punto", value=True)
            reference_point = None
            if include_distance:
                default_longitude, default_latitude = _reference_point_for_data(data)
                st.caption("Punto de referencia · longitud / latitud WGS 84")
                longitude = st.number_input(
                    "Longitud",
                    min_value=-180.0,
                    max_value=180.0,
                    value=default_longitude,
                    step=0.01,
                    format="%.5f",
                )
                latitude = st.number_input(
                    "Latitud",
                    min_value=-90.0,
                    max_value=90.0,
                    value=default_latitude,
                    step=0.01,
                    format="%.5f",
                )
                reference_point = (longitude, latitude)

        try:
            result = analyze_geodataframe(
                data,
                zone_type=zone_type,
                top_n=int(top_n),
                reference_point=reference_point,
            )
        except ValueError as error:
            st.error(str(error))
            st.stop()
        map_view = visualize_map(result)
        grouped_summary = None
        title = "Análisis de zonas GeoJSON"
        description = f"{source_name} · {len(data):,} entidades disponibles."

    st.subheader(title)
    st.caption(description)
    metric_columns = st.columns(4)
    metric_columns[0].metric("Entidades", f"{len(result):,}")
    metric_columns[1].metric("Área total (km²)", f"{result['area_km2'].sum():,.0f}")
    if "distance_km" in result.columns:
        metric_columns[2].metric("Dist. media (km)", f"{result['distance_km'].mean():,.1f}")
        metric_columns[3].metric("Dist. max. (km)", f"{result['distance_km'].max():,.1f}")
    else:
        metric_columns[2].metric("CRS entrada", str(data.crs))
        metric_columns[3].metric("Filtro", "Todos" if mode == "Cobertura municipal de Colima" else zone_type or "Todos")

    map_tab, data_tab, guide_tab = st.tabs(("🗺️ Mapa", "📊 Datos", "ℹ️ Acerca del análisis"))
    with map_tab:
        st_folium(map_view, height=620, use_container_width=True, returned_objects=[])
    with data_tab:
        display_columns = [
            column
            for column in result.columns
            if column != result.geometry.name
        ]
        st.dataframe(
            result[display_columns],
            hide_index=True,
            width="stretch",
        )
        csv_bytes = result[display_columns].to_csv(index=False).encode("utf-8-sig")
        download_columns = st.columns(2)
        download_columns[0].download_button(
            "Descargar resultados CSV",
            data=csv_bytes,
            file_name="sapg_resultados.csv",
            mime="text/csv",
            width="stretch",
        )
        download_columns[1].download_button(
            "Descargar mapa HTML",
            data=map_view.get_root().render(),
            file_name="sapg_mapa.html",
            mime="text/html",
            width="stretch",
        )
        if grouped_summary is not None:
            st.markdown("#### Resumen de cobertura por distancia")
            st.dataframe(
                grouped_summary.reset_index(),
                hide_index=True,
                width="stretch",
            )
            chart_data = grouped_summary[["municipios"]].rename_axis("Grupo")
            st.bar_chart(chart_data, width="stretch")
    with guide_tab:
        st.markdown(
            """
            - **Cobertura municipal:** filtra los municipios de Colima por radio
              desde el punto de referencia y agrupa la cobertura en intervalos.
            - **GeoJSON:** calcula área, filtra zonas y ordena por superficie;
              opcionalmente calcula distancia desde cada centroide.
            - Las entradas se conservan; las transformaciones crean resultados
              nuevos. Las áreas usan la proyección equivalente y las distancias
              son geodésicas sobre WGS 84.
            - La base del mapa necesita conexión a Internet. Un GeoJSON cargado
              se procesa en memoria y no se guarda en el servidor.
            """
        )
        st.markdown("#### Grupos de distancia")
        if grouped_summary is not None:
            st.dataframe(
                grouped_summary.reset_index(),
                hide_index=True,
                width="stretch",
            )
        _show_resources()


if __name__ == "__main__":
    main()
