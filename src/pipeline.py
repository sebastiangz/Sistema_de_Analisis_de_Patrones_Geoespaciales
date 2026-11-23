"""Análisis de zonas y cobertura municipal de Colima."""

import argparse
from functools import partial
from math import isfinite
from pathlib import Path

import geopandas as gpd
from toolz import pipe

from src.analysis import (
    filter_by_max_distance,
    filter_by_property,
    get_top_n_areas,
    group_by_distance,
    summarize_distance_groups,
)
from src.geospatial import load_geojson
from src.transforms import calculate_area_km2, calculate_distance_from_point_km
from src.visualization import visualize_map


DATASET = Path(__file__).resolve().parents[1] / 'data/input/colima.geojson'
REFERENCE_POINT = (-103.724, 19.243)


def run_analysis(
    input_path: str | Path,
    output_path: str | Path,
    zone_type: str | None = None,
    top_n: int = 5,
    reference_point: tuple[float, float] | None = None,
    *,
    max_distance_km: float | None = None,
) -> gpd.GeoDataFrame:
    """Compone las transformaciones y guarda el mapa HTML."""
    data = load_geojson(str(input_path))
    result = analyze_geodataframe(
        data,
        zone_type=zone_type,
        top_n=top_n,
        reference_point=reference_point,
        max_distance_km=max_distance_km,
    )

    map_options = {}
    if max_distance_km is not None:
        map_options = {'tiles': None, 'reference_point': reference_point[::-1]}
    visualize_map(result, output_filename=output_path, **map_options)
    return result


def analyze_geodataframe(
    data: gpd.GeoDataFrame,
    zone_type: str | None = None,
    top_n: int = 5,
    reference_point: tuple[float, float] | None = None,
    *,
    max_distance_km: float | None = None,
) -> gpd.GeoDataFrame:
    """Return analyzed features without modifying input data or writing files."""
    if data.empty:
        raise ValueError('No features were found in the input data.')
    if data.crs is None:
        raise ValueError('The input data must have a defined CRS.')

    operations = [calculate_area_km2]
    if reference_point is not None:
        operations.append(partial(calculate_distance_from_point_km, reference_point=reference_point))

    if max_distance_km is not None:
        if not isfinite(max_distance_km) or max_distance_km < 0:
            raise ValueError('El radio debe ser un número finito mayor o igual que cero.')
        if reference_point is None:
            raise ValueError('El análisis por radio requiere un punto de referencia.')
        operations.extend((
            filter_by_property('cve_ent', '06'),
            filter_by_max_distance(max_distance_km),
            group_by_distance,
        ))
    else:
        if zone_type is not None:
            operations.append(filter_by_property('tipo_zona', zone_type))
        operations.append(get_top_n_areas(top_n))

    result = pipe(data, *operations)
    if result.empty:
        if max_distance_km is not None:
            raise ValueError('El radio indicado no incluye ningún centroide municipal de Colima.')
        raise ValueError('No features matched the selected filters.')
    if max_distance_km is not None:
        result = result.sort_values('distance_km')

    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    municipal = parser.add_argument_group('Cobertura municipal de Colima')
    municipal.add_argument('--radio-km', type=float, help='Distancia máxima (60 km por defecto).')
    municipal.add_argument('--salida', type=Path, help='Ruta del mapa municipal.')
    demo = parser.add_argument_group('Demo configurable de zonas')
    demo.add_argument('--zonas', action='store_true', help='Ejecuta la demo con sus valores predeterminados.')
    demo.add_argument('--input', type=Path, help='GeoJSON de entrada de la demo.')
    demo.add_argument('--output', type=Path, help='Ruta del mapa de la demo.')
    demo.add_argument('--zone-type', help='Valor de la propiedad tipo_zona.')
    demo.add_argument('--top-n', type=int, help='Cantidad máxima de zonas (5 por defecto).')
    demo.add_argument('--reference-point', type=float, nargs=2, metavar=('LONGITUD', 'LATITUD'))
    args = parser.parse_args(argv)
    demo_options = (args.input, args.output, args.zone_type, args.top_n, args.reference_point)
    use_demo = args.zonas or any(option is not None for option in demo_options)
    if use_demo and (args.radio_km is not None or args.salida is not None):
        parser.error('Usa las opciones de cobertura municipal o las de la demo de zonas.')

    try:
        if use_demo:
            output = args.output or Path('outputs/mapa_analisis.html')
            result = run_analysis(
                args.input or Path('data/input/mapa.geojson'),
                output,
                zone_type=args.zone_type,
                top_n=5 if args.top_n is None else args.top_n,
                reference_point=tuple(args.reference_point) if args.reference_point else None,
            )
            columns = ('id', 'tipo_zona', 'valor_estimado', 'area_km2', 'distance_km')
            print(result[[column for column in columns if column in result]].to_string(index=False))
        else:
            output = args.salida or Path('data/output/colima.html')
            result = run_analysis(
                DATASET,
                output,
                reference_point=REFERENCE_POINT,
                max_distance_km=60 if args.radio_km is None else args.radio_km,
            )
            print(result[['nomgeo', 'area_km2', 'distance_km', 'distance_band']].round(2).to_string(index=False))
            print('\nResumen por distancia')
            print(summarize_distance_groups(result).round(2).to_string())
    except ValueError as error:
        parser.exit(1, f'{error}\n')

    print(f'Mapa guardado en {output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
