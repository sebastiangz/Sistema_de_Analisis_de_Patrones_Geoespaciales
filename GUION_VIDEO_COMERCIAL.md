# Guion de video comercial — SAPG

**Duración sugerida:** 2–3 minutos  
**Audiencia:** empresa que trabaja con datos de ubicaciones, zonas o territorios  
**Reemplazar antes de grabar:** `[Tu nombre]`, `[Empresa]` y cualquier ejemplo
específico del negocio.

> Presentar SAPG como un prototipo para evaluar mediante un piloto. El proyecto
> aún no ha sido validado con clientes, y los tres polígonos incluidos son
> datos ilustrativos; no son resultados comerciales ni una medición de ahorro.

## 0:00–0:25 — Apertura

**[En cámara]**

“Hola, soy [Tu nombre]. Quiero mostrarles SAPG, un prototipo de análisis
geoespacial para equipos que necesitan explorar zonas, comparar superficies y
generar mapas a partir de sus propios datos. La pregunta que queremos validar
con [Empresa] es sencilla: ¿podemos reducir los pasos manuales entre recibir un
archivo geográfico y obtener un análisis útil para tomar decisiones?”

## 0:25–0:55 — La necesidad

**[Mostrar un archivo GeoJSON y luego la terminal]**

“Cuando la información llega como polígonos y atributos, preparar un análisis
suele requerir varios pasos: revisar el sistema de coordenadas, calcular
superficies, aplicar filtros y preparar una visualización. SAPG reúne ese flujo
en un proceso repetible. No asumimos que este sea exactamente el problema de
su equipo: proponemos comprobarlo con un caso de uso y datos que ustedes
autoricen.”

## 0:55–1:35 — Demostración

**[Compartir pantalla; ejecutar desde la raíz del proyecto]**

```powershell
python -m src.pipeline --zone-type Comercial --top-n 2 --reference-point -103.35 19.2
```

“El comando carga el GeoJSON, calcula el área aproximada con una proyección
local, filtra las zonas comerciales, conserva las dos superficies mayores y
calcula la distancia desde un punto de referencia. Después genera un mapa HTML
con polígonos coloreados y datos consultables. Aquí pueden cambiar el archivo,
el filtro, el número de resultados y la coordenada según el análisis.”

**[Abrir `outputs/mapa_analisis.html`; seleccionar un polígono]**

“En el mapa se ven las zonas que pasaron el filtro y, al seleccionarlas, sus
atributos, área y distancia.”

## 1:35–2:05 — Qué está probado y qué falta probar

**[Mostrar brevemente el resultado de pruebas]**

“La versión actual cuenta con pruebas automatizadas para los cálculos, las
validaciones, la inmutabilidad de los datos y la generación del mapa. La suite
actual pasa 15 pruebas. La demostración usa únicamente tres polígonos
ilustrativos; por eso, sus cifras no representan una tasación, un cliente ni un
beneficio económico comprobado.”

## 2:05–2:40 — Propuesta de piloto

**[En cámara o mostrar una diapositiva con tres pasos]**

“Nuestra propuesta no es pedirles que adopten una solución sin validarla.
Proponemos definir con ustedes un piloto pequeño: primero, elegir una pregunta
operativa concreta; segundo, usar un conjunto de datos autorizado con fuente,
licencia, CRS y unidades documentados; y tercero, comparar el resultado con el
proceso que utilizan hoy. Acordaríamos de antemano cómo evaluar precisión,
tiempo de preparación, facilidad de uso y requisitos de privacidad. Solo con
esa evidencia tendría sentido estimar costos o un modelo comercial.”

## 2:40–3:00 — Cierre y llamada a la acción

**[En cámara]**

“Si este flujo se relaciona con un proceso de su equipo, nos gustaría agendar
una conversación breve con la persona responsable de datos geográficos. En esa
sesión podemos revisar un caso de uso, confirmar requisitos de seguridad y
decidir si vale la pena preparar un piloto. ¿Podemos coordinar esa reunión?”

## Notas para grabar

- Usa el GeoJSON incluido solo para enseñar la interfaz; identifica sus datos
  como ilustrativos.
- No afirmes clientes, ventas, ahorro, precisión comercial ni retorno de
  inversión: todavía no se han medido.
- No uses información confidencial de una empresa sin autorización expresa.
- La generación del mapa es local, pero sus teselas y recursos web requieren
  Internet; no prometas operación completamente aislada o cumplimiento de
  seguridad empresarial antes de revisar esos requisitos.
- Para hablar de precio, alcance o ahorro, primero acuerda el piloto y mide el
  proceso con datos y criterios definidos por la empresa.
