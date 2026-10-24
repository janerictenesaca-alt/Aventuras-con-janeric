---
id: I35
tipo: idea
titulo: "Agente de ventas con IA (bot de ventas 24/7)"
area: producto
estado: analizada
prioridad: media
riesgo_legal: medio
fase: F3
origen: [A02, A03]
depende_de: [I14, I17, I16]
relacionadas: [I34, I31]
confianza: media
tags: [idea, producto, nanturia]
---
# I35 · Agente de ventas con IA (bot de ventas 24/7)

> **Origen (audios):** [[A02 Sitio web tipo Airbnb bot intermediario y cobros|A02]] [[A03 Exceso de documentacion y almacenamiento|A03]] · **Área:** producto · **Prioridad:** media · **Riesgo legal:** medio · **Fase:** F3 · **Confianza del análisis:** media
> **Depende de:** [[I14 Plataforma estilo Airbnb solo tours con mapa y buses|I14]] [[I17 Flujo de reserva con confirmacion de disponibilidad|I17]] [[I16 Bot intermediario cliente guia y prevencion de fuga de datos|I16]]
> **Relacionadas:** [[I34 Expansion nacional primero internacional despues|I34]] [[I31 Estrategia de confianza frente a las grandes plataformas|I31]]

## Resumen fiel de lo dicho
Poner bots que puedan **vender productos sin necesidad de un operador físico**; el bot del sitio responde al turista, consulta al guía y avanza hacia el pago.

## Problema
Atender consultas 24/7 en varios idiomas con poco personal.

## Análisis
- Un agente conversacional puede resolver el 70-80 % de consultas repetitivas (precios, qué incluye, disponibilidad), pero **no debe prometer seguridad ni salud** ni inventar datos: errores aquí tienen consecuencias legales.
- Debe operar sobre **datos estructurados** (fichas de ruta, calendario, tarifas) con herramientas controladas, no sobre texto libre.
- Aun con agente automático la agencia sigue obligada a tener **oficina física** y **teléfono de asistencia** ([[N03 Hallazgos criticos#H10 Oficina física obligatoria para la agencia|H10]], [[N03 Hallazgos criticos#H09 Teléfono de emergencia 24 h y chat sin contacto directo|H09]]).

## Mejora propuesta
- **Agente con herramientas**: `buscar_rutas`, `ver_disponibilidad`, `cotizar_precio`, `crear_link_de_reserva`, `explicar_politicas`, `escalar_a_humano`.
- **Guardarraíles**: respuestas citando la ficha; sin consejos médicos; advertencias de riesgo obligatorias; registro de conversaciones.
- **Canales**: web y WhatsApp Business; ES/EN.
- **Traspaso a humano** ante quejas, accidentes o cotizaciones de grupo.
- Evaluación continua con conversaciones reales (calidad, exactitud, conversión).

## Reglas de negocio (especificación)
```text
agente.responde SOLO con datos de: ficha_ruta, calendario, tarifas, politicas
SI intencion IN {queja, accidente, salud, grupo>16} ENTONCES escalar_a_humano
toda cotizacion incluye: politica_cancelacion + nivel_riesgo + registro/LUAF de la agencia
```

## Riesgos
[[N08 Registro de riesgos#R10 Reputación por una mala experiencia temprana|R10]], [[N08 Registro de riesgos#R09 Protección de datos personales|R09]], [[N08 Registro de riesgos#R15 Bloqueo de canales de mensajería o pagos|R15]].

## Por verificar
[[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]], [[N09 Verificaciones pendientes#V13 Condiciones de WhatsApp Business API|V13]].

## Próximos pasos
Postergar a F3; mientras tanto, recopilar las preguntas reales de clientes.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
