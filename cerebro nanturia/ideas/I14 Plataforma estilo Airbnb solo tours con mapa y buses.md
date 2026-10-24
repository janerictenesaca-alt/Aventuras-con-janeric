---
id: I14
tipo: idea
titulo: "Plataforma estilo Airbnb solo para tours, con mapa y horarios de buses"
area: producto
estado: analizada
prioridad: alta
riesgo_legal: bajo
fase: F1
origen: [A02, A06]
depende_de: [I15, I18]
relacionadas: [I25, I31, I32]
confianza: media
tags: [idea, producto, nanturia]
---
# I14 · Plataforma estilo Airbnb solo para tours, con mapa y horarios de buses

> **Origen (audios):** [[A02 Sitio web tipo Airbnb bot intermediario y cobros|A02]] [[A06 Alianzas Mateo Hernan y sitio tipo Airbnb con buses|A06]] · **Área:** producto · **Prioridad:** alta · **Riesgo legal:** bajo · **Fase:** F1 · **Confianza del análisis:** media
> **Depende de:** [[I15 Modo turista y modo guia asistente de creacion de rutas|I15]] [[I18 Automatizacion documental legal por ruta|I18]]
> **Relacionadas:** [[I25 Complementos de hospedaje y transporte aceptar u omitir|I25]] [[I31 Estrategia de confianza frente a las grandes plataformas|I31]] [[I32 MVP concierge sitio basico tours cargados prueba y error|I32]]

## Resumen fiel de lo dicho
El sitio debe parecerse a Airbnb (interactivo, visual) pero vendiendo **solo tours**, no hospedajes; con mapa y con horarios de buses de todo el Ecuador. La parte visual es clave.

## Problema
Una experiencia de descubrimiento y compra confiable para el turista, con la información práctica de llegada.

## Análisis
- Patrón Airbnb = búsqueda con mapa + tarjetas con fotos + filtros + reseñas + calendario. Es replicable con tecnología estándar.
- **Horarios de buses de todo el país**: no se identificó una fuente pública única y actualizada; mantenerla manualmente es costoso y se desactualiza → riesgo de promesas falsas al turista ([[N09 Verificaciones pendientes#V14 Fuentes y licencias de horarios de buses|V14]]).
- El canal virtual tiene contenido mínimo obligatorio (registro de turismo, LUAF, dirección, teléfono, seguridad, políticas) → [[N03 Hallazgos criticos#H08 Requisitos obligatorios del canal virtual|H08]].
- Alcance excesivo en v1 (3D, buses nacionales, bot, internacional) es el principal riesgo de ejecución ([[N08 Registro de riesgos#R08 Complejidad excesiva del MVP|R08]]).

## Mejora propuesta
- **MVP**: home con buscador, mapa (OpenStreetMap/Leaflet o Mapbox), tarjetas de tours, filtros (modalidad, dificultad, duración, precio, fecha, idioma), ficha de tour con galería, mapa, qué incluye/no incluye, política de cancelación, reseñas verificadas, calendario y botón de reserva.
- **Cómo llegar**: empezar con **3 corredores** hacia Morona Santiago (Cuenca, Quito, Guayaquil) con horarios verificados a mano y fecha de «última verificación» visible; ampliar por demanda.
- **SEO**: una URL por ruta, datos estructurados (schema.org `TouristTrip`/`Product`), versión en inglés.
- **Pie de página legal** con registro/LUAF, dirección, teléfono, términos y protección de datos ([[N03 Hallazgos criticos#H08 Requisitos obligatorios del canal virtual|H08]]).
- Rendimiento móvil primero (la mayoría de guías y turistas usan celular).

## Reglas de negocio (especificación)
```text
Pagina.footer MUST incluir: registro_turismo, LUAF, direccion_fisica, email, telefono_24h_asistencia,
  politica_cobro_cancelacion_reembolso, politica_datos, declaracion_responsabilidad
```

## Riesgos
[[N08 Registro de riesgos#R08 Complejidad excesiva del MVP|R08]], [[N08 Registro de riesgos#R10 Reputación por una mala experiencia temprana|R10]].

## Métricas de éxito
Tiempo de carga móvil < 3 s; conversión visita→reserva ≥ 1,5 % (objetivo inicial); % de rutas con ficha completa = 100 %.

## Por verificar
[[N09 Verificaciones pendientes#V14 Fuentes y licencias de horarios de buses|V14]].

## Próximos pasos
Wireframes de home/ficha/checkout; elegir stack ([[N06 Arquitectura de plataforma|N06]]).

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
