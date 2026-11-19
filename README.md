# 🌍 Sistema de Análisis de Patrones Geoespaciales (SAPG)

> **Proyecto Final de Programación Funcional**

---

## 📋 Información del Proyecto

| Concepto | Detalle |
| :--- | :--- |
| **Universidad** | Universidad de Colima |
| **Facultad** | Ingeniería en Computación Inteligente |
| **Materia** | Programación Funcional |
| **Profesor** | Sebastián González Zepeda |
| **Estudiantes** | Miguel Alejandro Marcial Victorino y Diego Eduardo Araujo Manrique |
| **Semestre** | 3º Semestre |

---

## 🚀 Descripción

Este sistema permite la ingesta de datos geoespaciales (GeoJSON/Shapefiles) para realizar análisis automatizados. El núcleo del proyecto se basa en la **composición de funciones** y **pipelines** de datos, evitando estados mutables y garantizando un flujo de información limpio y testeable.

### ✨ Características Principales
* **Carga de Datos Modular:** Soporte para archivos locales y remotos (ZIP/GeoJSON).
* **Cálculo Geométrico Puro:** Transformaciones de datos (como cálculo de áreas en $km^2$) mediante funciones puras.
* **Filtrado Funcional (Currying):** Uso de funciones de orden superior para crear filtros dinámicos (por continente, tipo de zona, etc.).
* **Visualización Interactiva:** Generación automática de mapas HTML con `Folium`.

---

## 🛠️ Arquitectura Técnica (Paradigma Funcional)

El proyecto demuestra los siguientes conceptos clave de la materia:

1.  **Pipelines (`toolz.pipe`):** El procesamiento no es secuencial imperativo, sino un flujo de transformaciones.
2.  **Funciones Puras:** En `src/transforms.py`, las funciones no tienen efectos secundarios; entran datos y salen datos nuevos.
3.  **Inmutabilidad:** Se generan copias de los DataFrames (`df.copy()`) para no alterar los datos originales.
4.  **Currying:** En `src/analysis.py`, funciones como `filter_by_continent` devuelven otras funciones preparadas para el pipeline.

---

## 📂 Estructura del Repositorio

```text
.
├── data/
│   └── input/          # Datos de entrada (ej. mapa.geojson)
├── src/                # Código Fuente (Módulos)
│   ├── __init__.py
│   ├── geospatial.py   # Carga de datos (IO)
│   ├── transforms.py   # Transformaciones puras
│   ├── analysis.py     # Lógica de negocio y filtros
│   ├── pipeline.py     # Flujo ejecutable de análisis
│   └── visualization.py # Generación de mapas
├── tests/              # Pruebas Unitarias
│   ├── test_analysis.py
│   ├── test_geospatial.py
│   ├── test_pipeline.py
│   └── test_transforms.py
├── .gitignore
├── requirements.txt    # Dependencias del proyecto
├── PRESENTACION_FINAL.md # Guion y demo para la exposición
└── README.md           # Documentación
```

### Distancia desde un punto de referencia

`calculate_distance_from_point_km(gdf, (longitud, latitud))` en
`src/transforms.py` devuelve una copia del GeoDataFrame con la columna
`distance_km`, calculada desde el centroide de cada geometría al punto indicado.
El GeoDataFrame debe tener un CRS definido. Las mediciones se realizan en la
zona UTM estimada para el punto de referencia y la entrada conserva su CRS.

## Demo rápida

Instala las dependencias y ejecuta el analisis con el GeoJSON de ejemplo:

```powershell
python -m pip install -r requirements.txt
python -m src.pipeline --zone-type Comercial --top-n 2 --reference-point -103.35 19.2
```

El comando calcula `area_km2`, filtra por `tipo_zona`, conserva las zonas con
mayor area, agrega `distance_km` desde la coordenada opcional y guarda un mapa
interactivo en `outputs/mapa_analisis.html`. Puedes cambiar la entrada y salida
con `--input` y `--output`; para omitir la distancia, quita `--reference-point`.
Si el filtro no encuentra zonas, el comando informa el error en vez de guardar
un mapa vacio.

## Instalación, opciones y pruebas

Se requiere Python 3.10 o posterior. Instala las dependencias desde la raíz:

```powershell
python -m pip install -r requirements.txt
```

Opciones del comando:

| Opción | Uso |
| :--- | :--- |
| `--input RUTA` | GeoJSON de entrada (por defecto `data/input/mapa.geojson`). |
| `--output RUTA` | HTML de salida (por defecto `outputs/mapa_analisis.html`). |
| `--zone-type TIPO` | Filtra `tipo_zona`, por ejemplo `Comercial` o `Residencial`. |
| `--top-n N` | Número positivo de zonas más grandes que se conservarán. |
| `--reference-point LONGITUD LATITUD` | Añade distancia al punto en EPSG:4326. |

Para analizar todas las zonas sin distancias, ejecuta `python -m src.pipeline`.
El programa valida CRS y parámetros; errores de lectura, columnas ausentes o
filtros sin coincidencias se notifican en lugar de producir una salida vacía.
Los mapas bajo `outputs/` se ignoran en Git.

Ejecuta las pruebas desde la raíz:

```powershell
python -m pytest -q
```

Las pruebas usan GeoJSON temporales locales y cubren transformaciones,
inmutabilidad, validación de entradas, integración del pipeline y generación
del mapa, sin descargar datos de prueba.

## Metodología y alcance

El GeoJSON de ejemplo usa coordenadas geográficas WGS 84 [1]. Las áreas y
distancias se calculan después de proyectar las geometrías a una zona UTM local,
ya que las áreas de GeoPandas se expresan en las unidades del CRS y no deben
calcularse directamente en grados [2]–[4]. El mapa reproyecta las geometrías a
EPSG:4326 y las presenta como capa GeoJSON de Folium [6]. `toolz.pipe` compone
las transformaciones en una secuencia reproducible [5].

El archivo de demostración contiene tres zonas. No documenta la fuente ni la
unidad de `valor_estimado`; por ello, el valor se muestra solo como atributo y
no debe interpretarse como una tasación oficial ni como evidencia de mercado.
El ejemplo prueba el flujo técnico, no valida todavía un producto comercial ni
la adecuación a los datos de una empresa.
La proyección local es adecuada para este ejemplo regional, no para calcular
con precisión áreas o distancias globales. Para visualizar el HTML se requiere
Internet, ya que el mapa y las teselas base usan recursos externos.

## Referencias

[1] H. Butler, M. Daly, A. Doyle, S. Gillies, S. Hagen, and T. Schaub,
“The GeoJSON Format,” RFC 7946, Aug. 2016. doi: 10.17487/RFC7946.
[Online]. Available: https://www.rfc-editor.org/rfc/rfc7946

[2] GeoPandas Developers, “Projections,” *GeoPandas Documentation*.
[Online]. Available: https://geopandas.org/en/stable/docs/user_guide/projections.html
(accessed Nov. 19, 2026).

[3] GeoPandas Developers, “geopandas.GeoSeries.area,” *GeoPandas API Reference*.
[Online]. Available: https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.area.html
(accessed Nov. 19, 2026).

[4] GeoPandas Developers, “geopandas.GeoDataFrame.estimate_utm_crs,”
*GeoPandas API Reference*. [Online]. Available:
https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.estimate_utm_crs.html
(accessed Nov. 19, 2026).

[5] Toolz Developers, “Composability,” *Toolz Documentation*. [Online]. Available:
https://toolz.readthedocs.io/en/latest/composition.html (accessed Nov. 19, 2026).

[6] Python Visualization, “Using GeoJson,” *Folium User Guide*. [Online].
Available: https://python-visualization.github.io/folium/latest/user_guide/geojson/geojson.html
(accessed Nov. 19, 2026).

## Presentación

El guion de exposición, con demo en vivo, resultados de ejemplo, propuesta de
valor pendiente de validar y limitaciones, está en
[PRESENTACION_FINAL.md](PRESENTACION_FINAL.md).

El diálogo aparte para un video dirigido a una empresa —presentando SAPG como
piloto por validar y sin afirmar resultados comerciales no medidos— está en
[GUION_VIDEO_COMERCIAL.md](GUION_VIDEO_COMERCIAL.md).
