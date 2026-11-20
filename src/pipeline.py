"""Análisis municipal para una propuesta de distribución local en Colima."""

import argparse
from functools import partial
from pathlib import Path

from toolz import pipe

from src.analysis import filter_by_max_distance, filter_by_property
from src.geospatial import load_geojson
from src.transforms import calculate_area_km2, calculate_distance_km
from src.visualization import visualize_map


DATASET = Path(__file__).resolve().parents[1] / 'data/input/colima.geojson'
LONGITUDE, LATITUDE = -103.724, 19.243


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--radio-km', type=float, default=60)
    parser.add_argument('--salida', type=Path, default=Path('data/output/colima.html'))
    args = parser.parse_args()

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
    ).sort_values('distance_km')
    if result.empty:
        parser.exit(1, 'El radio indicado no incluye ningún centroide municipal.\n')

    visualize_map(result, location=[LATITUDE, LONGITUDE], zoom_start=9, output_filename=args.salida)
    print(result[['nomgeo', 'area_km2', 'distance_km']].round(2).to_string(index=False))
    print(f'Mapa guardado en {args.salida}')


if __name__ == '__main__':
    main()
