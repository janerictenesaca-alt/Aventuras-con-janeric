---
id: N15
tipo: sintesis
titulo: "Mapa del proyecto y guia de colaboracion"
estado: analizada
fecha: 2026-10-24
tags: [nanturia, colaboracion, guia]
---
# N15 · Mapa del proyecto y guia de colaboracion

> Para quien se une al proyecto: qué es, cómo está organizado, por dónde empezar y cómo aportar sin romper nada. Léelo completo una vez (5 minutos).

## 1. Qué es Nanturia en una frase
[[N00 Resumen ejecutivo|N00]] resume el proyecto: una **agencia de viajes digital** que vende y respalda tours de aventura y cultura en Ecuador, partiendo de Morona Santiago. Esta bóveda es su «cerebro»: de dónde salieron las ideas, qué dice la ley, qué está decidido y qué falta.

## 2. Cómo está organizado
| Carpeta o nota | Qué contiene | Para quién |
|---|---|---|
| Notas `N00` a `N16` (raíz) | Síntesis: resumen, modelo, marco legal, hallazgos, decisiones, finanzas, arquitectura, hoja de ruta, riesgos, verificaciones y tablero | Todos |
| `ideas/` | 35 ideas analizadas (`I01`–`I35`), cada una con análisis, mejora, reglas y riesgos | Negocio y producto |
| `audios/` | 27 audios con transcripción literal (`A01`–`A27`): la fuente original de cada idea | Quien quiera ver el origen |
| `plantillas/` | Plantillas para audios, ideas, decisiones y reuniones | Quien aporta |
| `sitio web/` | (solo si existe en tu copia) auditoría y cerebro del proyecto del sitio | Desarrollo |

## 3. Por dónde empezar según tu rol
| Rol | Lee primero |
|---|---|
| Dueño y decisiones | [[N00 Resumen ejecutivo\|N00]], [[N04 Decisiones abiertas\|N04]], [[N16 Tablero de pendientes\|N16]] |
| Legal y contabilidad | [[N02 Marco legal Ecuador\|N02]], [[N03 Hallazgos criticos\|N03]], [[N09 Verificaciones pendientes\|N09]] |
| Desarrollo | [[N06 Arquitectura de plataforma\|N06]], [[N14 Estado actual del sitio web\|N14]], [[N07 Hoja de ruta por fases\|N07]] |
| Operación (guías, rutas, equipos) | [[I18 Automatizacion documental legal por ruta\|I18]], [[I22 Biblioteca de rutas precreadas y onboarding\|I22]], [[I30 Marco legal de los guias ambitos y plan de habilitacion\|I30]], [[I13 Incumplimiento del guia no activa el tour o no se presenta\|I13]] |
| Marketing y alianzas | [[I24 QR en hoteles atribucion de origen y comision\|I24]], [[I28 Enlaces de pago y de ruta compartibles marketing viral\|I28]], [[I31 Estrategia de confianza frente a las grandes plataformas\|I31]], [[I05 Alianzas ancla Cueva de los Tayos Mateo y empresa de Hernan\|I05]] |
| Finanzas y precios | [[N05 Modelo financiero y precios\|N05]], [[I09 Precio decreciente por tamano de grupo escalera de precios\|I09]], [[I10 Estructura de precios comision y pago justo al guia\|I10]] |

## 4. Cómo leer una nota de idea
- La cabecera indica los audios de origen, el área, la prioridad, el riesgo legal, la fase (F0–F3, ver [[N07 Hoja de ruta por fases|N07]]) y la confianza del análisis.
- Siempre tiene las mismas secciones: resumen fiel de lo dicho, problema, análisis, mejora propuesta, reglas de negocio, riesgos, métricas, por verificar y próximos pasos.
- Los datos legales llevan un nivel de certeza: 🟢 leído en el texto oficial · 🟡 fuente secundaria o versión anterior · 🔴 no verificado (ver [[N02 Marco legal Ecuador|N02]]).
- Los identificadores (`A##`, `I##`, `H##`, `D##`, `R##`, `V##`, `N##`) son únicos y no se reutilizan.

## 5. Cómo aportar
1. **Audio o idea nueva:** crea una nota con «Plantilla audio» (siguiente número libre, por ejemplo `A28`) y pega la transcripción literal.
2. **Análisis:** crea la idea con «Plantilla idea» (por ejemplo `I36`) y regístrala en [[N10 Matriz audio a idea|N10]].
3. **Decisión:** agrega una sección `D14` en [[N04 Decisiones abiertas|N04]] con la «Plantilla decision» y una casilla en [[N16 Tablero de pendientes|N16]].
4. **Verificación pendiente:** agrega `V18` en [[N09 Verificaciones pendientes|N09]].
5. **Reunión:** usa «Plantilla reunion» y enlaza las decisiones que salgan.

Reglas de oro:
- Una idea por nota. Edita la original; **no dupliques** notas. El original vive en la carpeta del PC y GitHub es solo su respaldo ([[N13 Convenciones del cerebro#7. Fuente única y respaldo (sin duplicados)|N13 §7]]).
- Enlaza con `[[nombre exacto del archivo]]`.
- Nombres de archivo sin acentos y sin los caracteres `: ? * " < > |`.
- Nunca escribas aquí claves, contraseñas, tokens, teléfonos, correos, documentos de identidad ni datos de clientes.

Para usar las plantillas: Ajustes → Plugins principales → activa «Plantillas» y fija la carpeta de plantillas en `plantillas`.

## 6. Cómo ver el grafo sin perderse
Abre la vista gráfica y pulsa el engranaje:
- **Filtros:** activa «Solo archivos existentes» y desactiva «Huérfanos» (así no se ven las plantillas sueltas).
- **Grupos → Nuevo grupo**, uno por tipo, cada uno con su color: `path:ideas` (ideas) · `path:audios` (audios) · `path:"sitio web"` (sitio web). Si tu versión admite propiedades, también sirven `[tipo:idea]`, `[tipo:audio]` y `[tipo:sintesis]`.
- Para entender una nota concreta, ábrela y usa el **grafo local** (menú de los tres puntos de la nota → «Abrir grafo local») con profundidad 1 o 2.
- Si el grafo del sitio domina la pantalla, excluye `path:"sitio web"` en el filtro de búsqueda del grafo con `-path:"sitio web"`.

## 7. Rutina de revisión semanal (propuesta, 15 minutos)
1. Abre [[N16 Tablero de pendientes|N16]]: marca lo hecho y completa responsable y fecha de lo que sigue.
2. Pasa a «tomada» las decisiones cerradas y anota quién decidió y cuándo.
3. Convierte las ideas sueltas de la semana en audios (`A##`) o ideas (`I##`).
4. Revisa la fecha de última verificación de las normas en [[N02 Marco legal Ecuador|N02]] ([[N03 Hallazgos criticos#H13 Autoridad en transición y vigencia de textos|H13]]).

## 8. Responsables (completar)
| Área | Responsable | Cómo contactar |
|---|---|---|
| Decisiones del proyecto | | |
| Legal | | |
| Contabilidad e impuestos | | |
| Desarrollo del sitio | | |
| Operación de rutas y guías | | |
| Marketing y alianzas | | |

> No escribas teléfonos ni correos si esta bóveda se comparte o se sube a un repositorio público.

## 9. Cómo se unen las notas del sitio web
Las notas del cerebro del sitio (auditoría y proyecto) se copian a `sitio web/` con la herramienta `herramientas/cerebro.mjs`, que además convierte `I##` y `H##` en enlaces y valida que no haya enlaces rotos. Instrucciones en `herramientas/leeme-herramientas`. Convenciones de formato en [[N13 Convenciones del cerebro|N13]].
