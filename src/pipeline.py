"""Executable end-to-end geospatial analysis pipeline."""

import argparse
from pathlib import Path

import geopandas as gpd
from toolz import pipe

from src.analysis import filter_by_property, get_top_n_areas
from src.geospatial import load_geojson
from src.transforms import calculate_area_km2, calculate_distance_from_point_km
from src.visualization import visualize_map


def run_analysis(
    input_path: str | Path,
    output_path: str | Path,
    zone_type: str | None = None,
    top_n: int = 5,
    reference_point: tuple[float, float] | None = None,
) -> gpd.GeoDataFrame:
    """Run the project analysis and save an interactive map as HTML."""
    data = load_geojson(str(input_path))
    if data.empty:
        raise ValueError(f"No features were found in '{input_path}'.")
    if data.crs is None:
        raise ValueError(f"The input dataset '{input_path}' must have a defined CRS.")

    transforms = [calculate_area_km2]
    if reference_point is not None:
        transforms.append(
            lambda frame: calculate_distance_from_point_km(frame, reference_point)
        )
    if zone_type is not None:
        transforms.append(filter_by_property("tipo_zona", zone_type))
    transforms.append(get_top_n_areas(top_n))

    result = pipe(data, *transforms)
    if result.empty:
        raise ValueError("No features matched the selected filters.")

    visualize_map(result, output_filename=str(output_path))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze geospatial zones and create a map.")
    parser.add_argument(
        "--input",
        default="data/input/mapa.geojson",
        help="Input GeoJSON path (default: data/input/mapa.geojson).",
    )
    parser.add_argument(
        "--output",
        default="outputs/mapa_analisis.html",
        help="Output HTML map path (default: outputs/mapa_analisis.html).",
    )
    parser.add_argument(
        "--zone-type",
        help="Optional value to filter the tipo_zona property, such as Comercial.",
    )
    parser.add_argument("--top-n", type=int, default=5, help="Number of largest zones to keep.")
    parser.add_argument(
        "--reference-point",
        type=float,
        nargs=2,
        metavar=("LONGITUDE", "LATITUDE"),
        help="Optional reference coordinate pair for distance_km.",
    )
    args = parser.parse_args(argv)

    result = run_analysis(
        input_path=args.input,
        output_path=args.output,
        zone_type=args.zone_type,
        top_n=args.top_n,
        reference_point=tuple(args.reference_point) if args.reference_point else None,
    )
    print(f"Map saved to: {args.output}")
    summary_columns = [
        column
        for column in ("id", "tipo_zona", "valor_estimado", "area_km2", "distance_km")
        if column in result.columns
    ]
    print(result[summary_columns].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
