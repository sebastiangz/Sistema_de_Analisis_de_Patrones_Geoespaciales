# Presentación final: Sistema de Análisis de Patrones Geoespaciales

Guion de exposición sugerido para 5–7 minutos. Las afirmaciones de mercado se
marcan como hipótesis porque todavía no se han validado con clientes.

## Diapositiva 1 — ¿Qué hace SAPG?

**Sistema de Análisis de Patrones Geoespaciales (SAPG)**

- Toma zonas geográficas de un archivo GeoJSON.
- Calcula área aproximada, filtra por tipo y ordena las zonas más grandes.
- Muestra el resultado en un mapa interactivo que puede abrirse en un navegador.

**Guion:** “SAPG convierte un conjunto de zonas geográficas en un resultado
filtrado y un mapa que se puede explorar. Esta presentación muestra el flujo
actual con los datos de ejemplo incluidos en el repositorio.”

## Diapositiva 2 — Problema y usuario propuesto

- **Necesidad que buscamos atender:** comparar zonas espaciales sin tener que
  encadenar manualmente lectura, cálculos, filtros y visualización.
- **Usuario inicial propuesto:** analistas de planeación urbana o de bienes
  raíces que ya cuentan con polígonos y atributos en GeoJSON.
- **Propuesta de valor a validar:** obtener un mapa y una tabla de áreas,
  distancias y atributos con un solo comando reproducible.

**Guion:** “Este usuario y beneficio son una propuesta inicial, no el resultado
de entrevistas o ventas. Para validar la oportunidad, el siguiente paso sería
entrevistar a usuarios potenciales y probar con sus propios datos.”

## Diapositiva 3 — Flujo y programación funcional

```text
GeoJSON
  → carga y validación de CRS
  → área en km²
  → distancia opcional al punto de referencia
  → filtro por tipo de zona
  → selección de las N zonas más grandes
  → mapa HTML interactivo
```

- `toolz.pipe` compone las transformaciones en el orden del análisis.
- Las funciones de cálculo y filtrado devuelven copias; las pruebas verifican
  que no se agreguen columnas ni se alteren filas de la entrada.
- El cálculo métrico reproyecta a una zona UTM local; el mapa se entrega en
  coordenadas geográficas WGS 84.

**Guion:** “El orden del pipeline es explícito. Si falta el CRS, las
coordenadas no son válidas o el filtro no encuentra resultados, se informa el
error en vez de continuar con una salida vacía.”

## Diapositiva 4 — Demostración en vivo

Desde la raíz del proyecto:

```powershell
python -m src.pipeline --zone-type Comercial --top-n 2 --reference-point -103.35 19.2
```

El comando imprime el resumen y genera `outputs/mapa_analisis.html`. Abrir ese
archivo en el navegador para mostrar los polígonos, colores, atributos y
encuadre automático.

Resultado obtenido con el archivo de ejemplo:

| Zona | Tipo | Área aproximada (km²) | Distancia aproximada (km) |
| :--- | :--- | ---: | ---: |
| zona_A | Comercial | 116.371 | 5.535 |
| zona_C | Comercial | 116.326 | 15.266 |

**Guion:** “El punto de referencia se expresa como longitud y latitud. Las
distancias se miden desde el centroide de cada polígono. Estos valores
corresponden a los tres registros de demostración, no a una base inmobiliaria
oficial.”

## Diapositiva 5 — Validación técnica

- **15 pruebas automatizadas aprobadas** con `python -m pytest -q`.
- Incluyen transformaciones, CRS ausente, coordenadas inválidas, filtros sin
  coincidencias, inmutabilidad y generación de mapa.
- La prueba de carga usa un archivo local temporal: no depende de la red.
- La ejecución real del comando produjo el HTML de salida.

**Guion:** “El análisis y la generación del HTML se ejecutan localmente. Para
ver el mapa completo en el navegador se requiere Internet, pues sus recursos y
teselas base se cargan desde servicios externos.”

## Diapositiva 6 — Viabilidad: hipótesis y validación pendiente

- **Beneficio propuesto:** ahorrar pasos manuales al preparar comparaciones
  espaciales preliminares.
- **Modelo de ingreso por explorar:** cobro por proyecto o reporte para equipos
  pequeños; todavía no está probado ni implementado.
- **Validación necesaria:** entrevistar a usuarios, acordar formatos y unidades
  de los datos, comparar el resultado con su proceso actual y medir si pagarían
  por usarlo.

**Guion:** “No afirmamos que haya clientes ni ingresos. La viabilidad comercial
es una hipótesis y necesita validarse antes de presentarse como resultado.”

## Diapositiva 7 — Límites y siguiente paso

- El GeoJSON de demostración tiene solo tres zonas y no documenta fuente ni
  unidad para `valor_estimado`.
- UTM local está pensada para el ejemplo regional; no es una solución de
  medición global ni para geometrías que abarcan muchas zonas.
- El mapa es un archivo HTML, no una aplicación web con usuarios, base de datos
  o actualización automática.
- **Siguiente paso:** probar con un conjunto de datos autorizado, más amplio y
  con CRS, fuente y unidades documentados.

**Guion:** “El producto técnico funciona de extremo a extremo con el ejemplo.
La calidad y utilidad de futuros análisis dependerán de incorporar datos
reales, documentados y adecuados al área de estudio.”

## Antes de exponer

1. Instalar dependencias con `python -m pip install -r requirements.txt`.
2. Ejecutar `python -m pytest -q` y guardar el resultado para mostrar las
   15 pruebas aprobadas.
3. Ejecutar el comando de la diapositiva 4 y abrir
   `outputs/mapa_analisis.html`.
4. Si el aula no tiene Internet, explicar que el análisis y el HTML se generan
   localmente, pero la visualización puede no cargar sus recursos externos.
5. Si el equipo se divide la exposición, asignar los módulos según el trabajo
   real de cada integrante; no atribuir contribuciones que no se hayan hecho.
