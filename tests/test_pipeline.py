import geopandas as gpd
import pytest
from shapely.geometry import box

from src.pipeline import run_analysis


@pytest.fixture
def local_zones_file(tmp_path):
    zones = gpd.GeoDataFrame(
        {
            "id": ["small", "large-commercial", "large-residential"],
            "tipo_zona": ["Comercial", "Comercial", "Residencial"],
            "valor_estimado": [100_000, 500_000, 900_000],
            "geometry": [
                box(0.0, 0.0, 0.01, 0.01),
                box(0.1, 0.1, 0.2, 0.2),
                box(0.2, 0.2, 0.5, 0.5),
            ],
        },
        crs="EPSG:4326",
    )
    filepath = tmp_path / "zones.geojson"
    zones.to_file(filepath, driver="GeoJSON")
    return filepath


def test_run_analysis_composes_transform_filter_and_map(local_zones_file, tmp_path):
    output_path = tmp_path / "maps" / "analysis.html"

    result = run_analysis(
        input_path=local_zones_file,
        output_path=output_path,
        zone_type="Comercial",
        top_n=1,
        reference_point=(0, 0),
    )

    assert result["id"].tolist() == ["large-commercial"]
    assert result["area_km2"].iloc[0] > 0
    assert result["distance_km"].iloc[0] > 0
    assert output_path.is_file()
    assert "large-commercial" in output_path.read_text(encoding="utf-8")


def test_run_analysis_reports_when_filter_has_no_matches(local_zones_file, tmp_path):
    with pytest.raises(ValueError, match="No features matched"):
        run_analysis(
            input_path=local_zones_file,
            output_path=tmp_path / "empty.html",
            zone_type="Industrial",
        )

    assert not (tmp_path / "empty.html").exists()
