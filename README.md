# Sistema de Análisis de Patrones Geoespaciales (SAPG)

Proyecto final de Programación Funcional · Facultad de Ingeniería en Computación Inteligente, Universidad de Colima.

**Integrantes** · Miguel Alejandro Marcial Victorino y Diego Eduardo Araujo Manrique

**Profesor** · Sebastián González Zepeda

El sistema compara la cobertura de un centro de distribución hipotético en la ciudad de Colima. Calcula la superficie de cada municipio y la distancia desde el centro de distribución hasta su centroide. El resultado es una tabla de municipios, un resumen por distancia y un mapa interactivo.

## Interfaz visual

Para usar el análisis desde una interfaz gráfica en lugar de la terminal:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

La aplicación abre en el navegador. En **Cobertura municipal de Colima** puedes
cambiar el radio y explorar el mapa, los municipios, las áreas y los grupos de
distancia. En **Analizar GeoJSON** puedes usar el ejemplo o subir un
`FeatureCollection` GeoJSON en WGS 84, filtrar por `tipo_zona`, elegir cuántas
áreas mostrar y opcionalmente calcular distancias a un punto. Ambas vistas
permiten descargar la tabla CSV y el mapa HTML. Los archivos subidos se procesan
en memoria y no se guardan en el repositorio.

Para dejar la interfaz accesible sin mantener tu computadora encendida, puedes
desplegarla gratis desde [Streamlit Community Cloud](https://share.streamlit.io):
inicia sesión con GitHub, selecciona este repositorio y la rama `main`, indica
`app.py` como archivo principal y pulsa **Deploy**. El repositorio es público;
no cargues información privada o que no tengas autorización para publicar.

## Ejecutar el análisis

Desde la raíz del repositorio, con Python 3.12:

```powershell
python -m pip install -r requirements.txt
python -m src.pipeline
python -m pytest -q
```

El comando usa un radio de **60 km** y guarda el mapa en `data/output/colima.html`. Abre el HTML en un navegador y selecciona un municipio para ver su nombre, clave INEGI, área y distancia. El análisis lee los datos del repositorio y el navegador carga Leaflet desde un CDN.

Para comparar con un radio de **25 km**:

```powershell
python -m src.pipeline --radio-km 25 --salida data/output/colima-25.html
```

El radio debe ser finito y mayor o igual que cero. Si el radio excluye todos los centroides, el programa informa el motivo y termina antes de escribir un mapa.

## Demo de zonas y GitHub Pages

La demo de zonas usa el mismo pipeline. Carga `data/input/mapa.geojson` por defecto, permite filtrar por `tipo_zona` y conserva las zonas de mayor área. Las opciones `--input`, `--output`, `--top-n` y `--reference-point` permiten ajustar la ejecución. Usa `--zonas` para ejecutar la demo con sus valores predeterminados.

```powershell
python -m src.pipeline --zone-type Comercial --top-n 2 --reference-point -103.35 19.2 --output web/mapa.html
```

El sitio está en [web/index.html](web/index.html). El [flujo de publicación](.github/workflows/deploy-pages.yml) ejecuta las pruebas, genera el mapa de zonas y prepara el sitio. Para publicar en el repositorio, selecciona **GitHub Actions** como fuente en **Settings → Pages**. La presentación y el guion están en [PRESENTACION_FINAL.md](PRESENTACION_FINAL.md) y [GUION_VIDEO_COMERCIAL.md](GUION_VIDEO_COMERCIAL.md).

## Datos y método

- [`data/input/colima.geojson`](data/input/colima.geojson) contiene las diez áreas municipales de Colima del Marco Geoestadístico del INEGI de diciembre de 2025. El archivo declara el sistema EPSG:6365 a nivel de colección para que GeoPandas interprete correctamente las coordenadas. El pipeline filtra por la clave estatal `06`. [Datos del INEGI](https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/06)
- El centro de distribución se ubica en **19.243° N, 103.724° O**. El área se calcula en la proyección equivalente EPSG:6933 y la distancia geodésica se calcula sobre WGS 84.
- [`data/input/mapa.geojson`](data/input/mapa.geojson) es el archivo de ejemplo de la base de 2025.

## Semana 3 · Agrupación y análisis de patrones

Después de aplicar el filtro por radio, `group_by_distance` usa `Series.map` para asignar un grupo a cada municipio. `summarize_distance_groups` cuenta los municipios y suma sus superficies por grupo con `groupby().agg()`. El resumen incluye los grupos vacíos y los mismos intervalos se reflejan en la leyenda del mapa.

| Grupo de distancia | Municipios a 25 km | Superficie a 25 km (km²) | Municipios a 60 km | Superficie a 60 km (km²) |
| --- | ---: | ---: | ---: | ---: |
| Hasta 20 km | 4 | 1,758.97 | 4 | 1,758.97 |
| Más de 20 y hasta 40 km | 1 | 499.91 | 4 | 1,710.86 |
| Más de 40 km | 0 | 0.00 | 0 | 0.00 |
| **Total** | **5** | **2,258.88** | **8** | **3,469.83** |

Los cuatro municipios más cercanos son Villa de Álvarez, Cuauhtémoc, Colima y Comala. A 25 km también entra Coquimatlán. Ampliar el radio a 60 km añade Ixtlahuacán, Minatitlán y Armería. El centroide más lejano de los ocho seleccionados queda a 38.68 km. Para un piloto de reparto, el grupo de hasta 20 km ofrece un conjunto inicial de municipios que se puede contrastar con rutas, tiempos de viaje y demanda.

El área total corresponde a los polígonos completos de los municipios seleccionados por su centroide. Las partes insulares pueden desplazar ese punto. Por ejemplo, el centroide calculado para Tecomán queda a 145.34 km. Para planear entregas se necesitan ubicaciones de entrega y datos de la red vial.

## Implementación por semana

| Semana | Evidencia |
| --- | --- |
| 1 · Cálculos geoespaciales | [`src/transforms.py`](src/transforms.py) calcula áreas y distancias y devuelve tablas nuevas. |
| 2 · Procesamiento funcional | [`src/pipeline.py`](src/pipeline.py) encadena operaciones con `toolz.pipe` y aplica filtros currificados por propiedad y distancia. |
| 3 · Agrupación y patrones | [`src/analysis.py`](src/analysis.py) clasifica por distancia y resume la cobertura. [Las pruebas](tests/test_analysis.py) verifican los límites de 20 y 40 km y los grupos vacíos. |
| 4 · Visualización y documentación | [`src/visualization.py`](src/visualization.py) exporta el HTML con Folium. El mapa incluye una leyenda, un marcador de referencia y detalles por municipio. |

## Punto de partida de 2025

Se ejecutó el commit `f3dbd2c` antes de modificar el proyecto.

- Pasaron dos de tres pruebas. La descarga de Natural Earth falló por resolución DNS y el mismo ZIP cargó desde una copia local.
- El flujo con `mapa.geojson` cargó los datos, filtró zonas comerciales y calculó sus áreas. Folium devolvió el mapa en memoria, pero el argumento `output_filename` no guardó el HTML.
- La última celda del cuaderno arrojó un `TypeError`. Al llamar a `get_top_n_areas()` dentro de la composición, se obtuvo la tabla de África.
- La base calculaba superficies con Mercator mundial y carecía del cálculo de distancias.

## Reparto propuesto de trabajo

| Módulo | Responsable propuesto | Pruebas |
| --- | --- | --- |
| Transformaciones | Miguel Alejandro Marcial Victorino | [`tests/test_transforms.py`](tests/test_transforms.py) |
| Análisis | Diego Eduardo Araujo Manrique | [`tests/test_analysis.py`](tests/test_analysis.py) |
| Visualización | Ambos integrantes | [`tests/test_visualization.py`](tests/test_visualization.py) |

## Referencias académicas

1. G. Molina León, M. Lischka y A. Breiter, “Mapping the Global South: Equal-Area Projections for Choropleth Maps”, *2020 IEEE Visualization Conference (VIS)*, pp. 91–95, 2020. Discute la elección de proyecciones equivalentes según el objetivo cartográfico. [Artículo en IEEE VIS](https://virtual.ieeevis.org/year/2020/paper_s-short-1236.html) · [DOI](https://doi.org/10.1109/VIS47514.2020.00025).
2. F. Lei, A. Fan, A. M. MacEachren y R. Maciejewski, “GeoLinter: A Linting Framework for Choropleth Maps”, *IEEE Transactions on Visualization and Computer Graphics*, vol. 30, núm. 2, pp. 1592–1607, 2024. Aporta criterios sobre clasificación, contraste y unidades en mapas temáticos. [Artículo en IEEE VIS](https://content-staging.ieeevis.org/year/2024/paper_v-tvcg-20233322372.html) · [DOI](https://doi.org/10.1109/TVCG.2023.3322372).
3. J. Dean y S. Ghemawat, “MapReduce: simplified data processing on large clusters”, *Communications of the ACM*, vol. 51, núm. 1, pp. 107–113, 2008. Describe cómo combinar transformaciones por registro con reducciones por grupo, el mismo patrón que aplica localmente el resumen municipal. [Artículo en ACM](https://dl.acm.org/doi/10.1145/1327452.1327492).
