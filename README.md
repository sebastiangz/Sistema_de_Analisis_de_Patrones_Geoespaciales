# 🌍 1: Sistema de Análisis de Patrones Geoespaciales

## 📋 Descripción del Proyecto

Sistema desarrollado con **programación funcional** para procesar, analizar y visualizar datos geoespaciales, identificando patrones territoriales mediante el uso de funciones puras, inmutabilidad y composición funcional.

**Universidad de Colima - Ingeniería en Computación Inteligente**  
**Materia**: Programación Funcional  
**Profesor**: Gonzalez Zepeda Sebastian  
**Semestre**: Agosto 2025 - Enero 2026

---

## 🎯 Objetivos

- Aplicar **funciones de orden superior** (map, filter, reduce) en procesamiento de datos geográficos
- Implementar **funciones puras** sin efectos secundarios
- Utilizar **inmutabilidad** en estructuras de datos espaciales
- Practicar **composición funcional** para pipelines de transformación
- Desarrollar **lazy evaluation** para optimizar cálculos geoespaciales
- Crear **funciones currying** para parametrización flexible

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.11+
- **Paradigma**: Programación Funcional
- **Librerías**:
  - `functools` - Herramientas funcionales
  - `toolz` - Utilidades funcionales avanzadas
  - `geopandas` - Procesamiento de datos geoespaciales
  - `shapely` - Geometrías y operaciones espaciales
  - `folium` - Visualización de mapas interactivos

---

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/analisis-geoespacial-funcional.git
cd analisis-geoespacial-funcional

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### requirements.txt
```
geopandas>=0.14.0
shapely>=2.0.0
folium>=0.15.0
toolz>=0.12.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
```

---

## 🚀 Uso del Sistema

```python
from src.geospatial import load_geojson, analyze_patterns

# Cargar datos geoespaciales
data = load_geojson('datos/mapa.geojson')

# Pipeline funcional de análisis
result = (data
    .pipe(filter_by_property('type', 'polygon'))
    .pipe(calculate_areas)
    .pipe(detect_clusters)
    .pipe(generate_statistics))

# Visualizar resultados
visualize_map(result, output='mapa_resultado.html')
```

---

## 📂 Estructura del Proyecto

```
analisis-geoespacial-funcional/
├── src/
│   ├── __init__.py
│   ├── geospatial.py       # Funciones de procesamiento geoespacial
│   ├── transforms.py       # Transformaciones funcionales
│   ├── analysis.py         # Análisis de patrones
│   └── visualization.py    # Generación de visualizaciones
├── data/
│   ├── input/              # Datos de entrada (GeoJSON, Shapefiles)
│   └── output/             # Resultados procesados
├── tests/
│   ├── test_geospatial.py
│   ├── test_transforms.py
│   └── test_analysis.py
├── docs/
│   ├── arquitectura.md
│   └── ejemplos.md
├── notebooks/
│   └── exploracion.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔑 Características Principales

### 1. Funciones Puras
```python
def calculate_area(geometry):
    """Calcula área sin modificar la geometría original"""
    return geometry.area

def filter_by_area(min_area):
    """Función curried para filtrar por área"""
    return lambda geom: geom.area >= min_area
```

### 2. Composición Funcional
```python
from functools import reduce
from toolz import pipe, compose

# Pipeline de transformación
process_geodata = pipe(
    load_geojson,
    filter_valid_geometries,
    transform_crs,
    calculate_metrics,
    generate_report
)
```

### 3. Inmutabilidad
```python
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class GeoPoint:
    lat: float
    lon: float
    properties: dict
```

---

## 📊 Funcionalidades Implementadas

- ✅ Carga y validación de datos geoespaciales
- ✅ Transformación de sistemas de coordenadas
- ✅ Cálculo de métricas espaciales (área, perímetro, distancias)
- ✅ Detección de clusters mediante análisis funcional
- ✅ Generación de estadísticas descriptivas
- ✅ Visualización interactiva con mapas
- ✅ Exportación de resultados en múltiples formatos

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest tests/

# Tests con cobertura
pytest --cov=src tests/

# Tests específicos
pytest tests/test_geospatial.py -v
```

---

## 📈 Pipeline de Desarrollo

### Semana 1: Fundamentos (30 Oct - 5 Nov)
- Configuración del entorno
- Implementación de funciones básicas de carga
- Transformaciones CRS funcionales

### Semana 2: Análisis Avanzado (6 Nov - 12 Nov)
- Detección de patrones territoriales
- Algoritmos de clustering funcional
- Métricas espaciales composables

### Semana 3: Visualización (13 Nov - 19 Nov)
- Generación de mapas interactivos
- Dashboard de análisis
- Documentación completa

---

## 🌟 Componente de Emprendimiento

**Aplicación Real**: Sistema de análisis territorial para empresas de bienes raíces, permitiendo identificar zonas de alto valor comercial mediante análisis de patrones geoespaciales.

**Propuesta de Valor**:
- Toma de decisiones basada en datos espaciales
- Identificación de oportunidades de inversión
- Análisis predictivo de crecimiento urbano

---

## 📚 Referencias

- **Functools Documentation**: https://docs.python.org/3/library/functools.html
- **GeoPandas**: https://geopandas.org/
- **Shapely User Manual**: https://shapely.readthedocs.io/
- **Toolz Documentation**: https://toolz.readthedocs.io/

---

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es parte del curso de Programación Funcional de la Universidad de Colima.

---

## ✉️ Contacto

**Autor**: [Tu Nombre]  
**Email**: [tu-email@ucol.mx]  
**GitHub**: [@tu-usuario](https://github.com/tu-usuario)

---

## 🏆 Criterios de Evaluación

- **Funciones Puras (30%)**: Ausencia de efectos secundarios, determinismo
- **Composición Funcional (25%)**: Pipeline elegante, reutilización
- **Inmutabilidad (20%)**: Estructuras inmutables, manejo correcto
- **Testing (15%)**: Cobertura de pruebas, casos edge
- **Documentación (10%)**: README claro, comentarios útiles
