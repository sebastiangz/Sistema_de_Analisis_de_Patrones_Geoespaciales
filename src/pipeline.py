"""Análisis municipal para una propuesta de distribución local en Colima."""

import argparse
from functools import partial
from math import isfinite
from pathlib import Path

from toolz import pipe

from src.analysis import (
    filter_by_max_distance,
    filter_by_property,
    group_by_distance,
    summarize_distance_groups,
)
from src.geospatial import load_geojson
from src.transforms import calculate_area_km2, calculate_distance_km
from src.visualization import visualize_map


DATASET = Path(__file__).resolve().parents[1] / 'data/input/colima.geojson'
LONGITUDE, LATITUDE = -103.724, 19.243


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--radio-km', type=float, default=60, help='Distancia máxima en km (60 por defecto).')
    parser.add_argument('--salida', type=Path, default=Path('data/output/colima.html'), help='Ruta del mapa HTML.')
    args = parser.parse_args()
    if not isfinite(args.radio_km) or args.radio_km < 0:
        parser.error('--radio-km debe ser un número finito mayor o igual que cero.')

    result = pipe(
        str(DATASET),
        load_geojson,
        filter_by_property('cve_ent', '06'),
    )
    if result.empty:
        parser.exit(1, 'No se encontraron áreas municipales de Colima en el GeoJSON.\n')

    result = pipe(
        result,
        calculate_area_km2,
        partial(calculate_distance_km, longitude=LONGITUDE, latitude=LATITUDE),
        filter_by_max_distance(args.radio_km),
        group_by_distance,
    ).sort_values('distance_km')
    if result.empty:
        parser.exit(1, 'El radio indicado no incluye ningún centroide municipal.\n')

    visualize_map(
        result,
        output_filename=args.salida,
        tiles=None,
        reference_point=(LATITUDE, LONGITUDE),
    )
    print(result[['nomgeo', 'area_km2', 'distance_km', 'distance_band']].round(2).to_string(index=False))
    print('\nResumen por distancia')
    print(summarize_distance_groups(result).round(2).to_string())
    print(f'Mapa guardado en {args.salida}')


if __name__ == '__main__':
    main()
