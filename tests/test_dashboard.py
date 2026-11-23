import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src.dashboard import read_uploaded_geojson


def test_read_uploaded_geojson_parses_features_in_memory():
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"tipo_zona": "Comercial"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[-103.4, 19.2], [-103.3, 19.2], [-103.3, 19.3],
                         [-103.4, 19.3], [-103.4, 19.2]]
                    ],
                },
            }
        ],
    }

    result = read_uploaded_geojson(json.dumps(geojson).encode("utf-8"))

    assert len(result) == 1
    assert result.crs.to_epsg() == 4326
    assert result.loc[0, "tipo_zona"] == "Comercial"


@pytest.mark.parametrize(
    "contents, message",
    [
        (b"not json", "JSON"),
        (b'{"type": "Feature"}', "FeatureCollection"),
        (b'{"type": "FeatureCollection", "features": []}', "no contiene"),
    ],
)
def test_read_uploaded_geojson_reports_invalid_input(contents, message):
    with pytest.raises(ValueError, match=message):
        read_uploaded_geojson(contents)


def test_dashboard_renders_both_analysis_modes():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(str(app_path), default_timeout=30).run()

    assert not app.exception
    assert any("Cobertura municipal de Colima" in heading.value for heading in app.subheader)

    app.sidebar.radio[0].set_value("Analizar GeoJSON").run()

    assert not app.exception
    assert any("Análisis de zonas GeoJSON" in heading.value for heading in app.subheader)

    app.selectbox[0].set_value("Residencial").run()

    assert not app.exception
    assert any(metric.label == "Entidades" and metric.value == "1" for metric in app.metric)

    app.sidebar.radio[1].set_value("Subir GeoJSON").run()

    assert not app.exception
    assert any("Sube un archivo GeoJSON" in message.value for message in app.info)
