---
id: I20
tipo: idea
titulo: "Asignación automática de guía, cupos y desbordamiento"
area: producto
estado: analizada
prioridad: media
riesgo_legal: bajo
fase: F2
origen: [A23]
depende_de: [I21, I17]
relacionadas: [I13, I23]
confianza: media
tags: [idea, producto, nanturia]
---
# I20 · Asignación automática de guía, cupos y desbordamiento

> **Origen (audios):** [[A23 Asignacion automatica cupos y rutas precreadas|A23]] · **Área:** producto · **Prioridad:** media · **Riesgo legal:** bajo · **Fase:** F2 · **Confianza del análisis:** media
> **Depende de:** [[I21 Rutas sin dueno ficha unica y multiples proveedores|I21]] [[I17 Flujo de reserva con confirmacion de disponibilidad|I17]]
> **Relacionadas:** [[I13 Incumplimiento del guia no activa el tour o no se presenta|I13]] [[I23 Ranking y visibilidad de guias operadoras y colaboradores|I23]]

## Resumen fiel de lo dicho
Si un cliente compra una ruta, la plataforma debe asignar automáticamente al guía que la subió. Por ley se pueden llevar «hasta 15» por guía; si se llena, la plataforma «salta 7 días» al siguiente guía del cantón y le pregunta si quiere hacerla; si no puede, se le cargan todos los clientes al mismo guía. El creador recibe la primera notificación. Otros guías pueden compartir la ruta.

## Problema
Distribuir demanda entre guías respetando capacidad legal y calidad.

## Análisis
- **Capacidad real**: el tope general de grupo es **16** (Reglamento de Guianza 2025, Disp. Gen. 2ª 🟢) y puede ser menor por sitio o área protegida; además el Reglamento de Aventura fija **ratios por modalidad** (ej.: canyoning 1-4 por guía; cabalgata 1-8; senderismo 1-8; rafting 5-9 + guía por balsa según tamaño) → [[N03 Hallazgos criticos#H04 Tope de grupo de 16 y límites por modalidad|H04]]. Por tanto «15» debe ser un parámetro calculado, no una constante.
- «**Cargar todos al mismo guía**» (más del tope) **es incumplimiento**. La alternativa correcta es abrir una segunda salida/guía u ofrecer otra fecha.
- «Saltar 7 días» es ambiguo: puede ser una ventana de espera o una fecha alternativa; para el turista 7 días de espera es excesivo.

## Mejora propuesta
- **Asignación en cascada**: (1) creador de la ruta con ventana exclusiva (ej. 3 h) → (2) pool elegible ordenado por puntaje → (3) difusión a todos los elegibles → (4) si nadie acepta, ofrecer fecha alterna al cliente.
- **Elegibilidad** automática (clasificación/ámbito, registro vigente, no suspendido, disponibilidad, capacidad, conocimiento de la ruta).
- **Capacidad por salida** = mín(16, límite de sitio, ratio de modalidad × guías asignados).
- Si la demanda supera la capacidad: **abrir salida B** (segundo guía) o lista de espera.

## Reglas de negocio (especificación)
```text
capacidad(salida) = min(16, limite_sitio(ruta), ratio_modalidad(ruta) * n_guias_asignados)
SI n_reservas > capacidad ENTONCES crear_salida_adicional() O lista_espera
elegible(guia, ruta) = clasificacion_cubre(modalidad, canton) AND registro_vigente AND NOT suspendido AND disponible AND certificado_ruta
cascada: creador (3h exclusiva) -> pool por puntaje (3h) -> broadcast (6h) -> fecha_alterna
```

## Riesgos
[[N08 Registro de riesgos#R16 Calidad desigual de guías y rutas|R16]], [[N08 Registro de riesgos#R03 Falla del proveedor por no presentarse|R03]].

## Por verificar
[[N09 Verificaciones pendientes#V11 Límites de grupo por modalidad y por área protegida para las 16 rutas|V11]].

## Próximos pasos
Tabla de ratios por modalidad y límites por sitio para las 16 rutas ([[N02 Marco legal Ecuador|N02]]).

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
