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
│   └── visualization.py # Generación de mapas
├── tests/              # Pruebas Unitarias
│   ├── test_analysis.py
│   ├── test_geospatial.py
│   └── test_transforms.py
├── .gitignore
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación
```

### Distancia desde un punto de referencia

`calculate_distance_from_point_km(gdf, (longitud, latitud))` en
`src/transforms.py` devuelve una copia del GeoDataFrame con la columna
`distance_km`, calculada desde el centroide de cada geometría al punto indicado.
El GeoDataFrame debe tener un CRS definido. Las mediciones se realizan en la
zona UTM estimada para el punto de referencia y la entrada conserva su CRS.
