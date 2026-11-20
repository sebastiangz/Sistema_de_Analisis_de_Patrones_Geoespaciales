# 🌍 Sistema de Análisis de Patrones Geoespaciales (SAPG)

> **Proyecto Final de Programación Funcional**

## Análisis municipal de Colima

Desde la raíz del repositorio, instala las dependencias y genera el mapa.

```powershell
python -m pip install -r requirements.txt
python -m src.pipeline
python -m pytest -q
```

El comando imprime las áreas y distancias, ordenadas de menor a mayor distancia, y guarda el mapa interactivo en `data/output/colima.html`. Puedes cambiar el umbral y la ruta con `--radio-km 25 --salida data/output/colima-25.html`. El análisis usa el GeoJSON incluido y puede ejecutarse sin conexión. Al abrir el HTML, el navegador necesita Internet para cargar Leaflet y el mapa base.

La propuesta de emprendimiento es un servicio de distribución local con un centro hipotético en la ciudad de Colima (19.243° N, 103.724° O). El radio inicial de 60 km sirve para seleccionar municipios candidatos a una primera etapa de reparto. El pipeline mide la distancia geodésica en línea recta al centroide de cada área municipal. El área, calculada con una proyección equivalente, da contexto sobre la extensión de cada zona. La planeación de recorridos y tiempos de entrega requiere datos de la red vial.

Las diez áreas municipales provienen del Marco Geoestadístico del INEGI de diciembre de 2025. El archivo local declara también a nivel de colección el sistema EPSG:6365 indicado en las geometrías originales para que GeoPandas lo lea correctamente. [Descarga oficial del GeoJSON de Colima](https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/06) · [Documentación del servicio](https://www.inegi.org.mx/servicios/catalogounico/).

### Ejecución de la base de 2025

Se ejecutó el código del commit `f3dbd2c` antes de editar los módulos.

- Pasaron dos de tres pruebas. La prueba con la URL de Natural Earth falló por resolución DNS en el entorno de ejecución. Una copia local del mismo ZIP sí cargó correctamente.
- Con `mapa.geojson`, el flujo cargó los datos de ejemplo, filtró las zonas comerciales, calculó áreas y devolvió un mapa de Folium. El argumento `output_filename` no escribía el HTML.
- La celda final del cuaderno falló con `TypeError` al indexar el resultado. Ejecutar `get_top_n_areas()` en la composición devolvió la tabla de África correctamente.
- La base no calculaba distancias. El área usaba Mercator mundial, que distorsiona superficies.

### Reparto sugerido de trabajo

| Módulo | Responsable propuesto | Responsabilidad | Pruebas |
| --- | --- | --- | --- |
| `src/transforms.py` | Miguel Alejandro Marcial Victorino | Área y distancia sin modificar la entrada | `tests/test_transforms.py` |
| `src/analysis.py` | Diego Eduardo Araujo Manrique | Filtros currificados y orden por área | `tests/test_analysis.py` |
| `src/visualization.py` | Ambos integrantes | Capas y exportación HTML | `tests/test_visualization.py` |

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
│   ├── input/          # GeoJSON oficial de Colima y datos de ejemplo
│   └── output/         # Mapas generados
├── src/                # Código Fuente (Módulos)
│   ├── __init__.py
│   ├── geospatial.py   # Carga de datos (IO)
│   ├── pipeline.py     # Ejecución del análisis municipal
│   ├── transforms.py   # Transformaciones puras
│   ├── analysis.py     # Lógica de negocio y filtros
│   └── visualization.py # Generación de mapas
├── tests/              # Pruebas Unitarias
│   ├── test_analysis.py
│   ├── test_geospatial.py
│   ├── test_transforms.py
│   └── test_visualization.py
├── .gitignore
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación
```
