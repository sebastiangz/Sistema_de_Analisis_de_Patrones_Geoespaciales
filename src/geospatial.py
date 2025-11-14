# Modulo para cargar datos
import geopandas as gpd

def load_geojson(filepath: str) -> gpd.GeoDataFrame:
    try:
        print(f"-> (Geo) Cargando datos desde {filepath}")
        return gpd.read_file(filepath)
    except Exception as e:
        print(f"Error al cargar el archivo {filepath}: {e}")
        return gpd.GeoDataFrame()

print("Archivo src/geospatial.py creado.")
