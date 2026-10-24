---
id: I16
tipo: idea
titulo: "Bot intermediario cliente↔guía y prevención de fuga de datos"
area: producto
estado: analizada
prioridad: media
riesgo_legal: medio
fase: F2
origen: [A02, A09]
depende_de: [I17]
relacionadas: [I13, I28]
confianza: media
tags: [idea, producto, nanturia]
---
# I16 · Bot intermediario cliente↔guía y prevención de fuga de datos

> **Origen (audios):** [[A02 Sitio web tipo Airbnb bot intermediario y cobros|A02]] [[A09 Flujo de consulta al guia y reembolso|A09]] · **Área:** producto · **Prioridad:** media · **Riesgo legal:** medio · **Fase:** F2 · **Confianza del análisis:** media
> **Depende de:** [[I17 Flujo de reserva con confirmacion de disponibilidad|I17]]
> **Relacionadas:** [[I13 Incumplimiento del guia no activa el tour o no se presenta|I13]] [[I28 Enlaces de pago y de ruta compartibles marketing viral|I28]]

## Resumen fiel de lo dicho
Cuando el cliente compra, un bot debe reenviar el mensaje al guía y el guía responder al bot y el bot al cliente, sin interacción directa. Además, evitar el ingreso de datos personales y números de contacto dentro de los chats.

## Problema
Proteger el negocio (que no se cierren ventas fuera) y los datos personales.

## Análisis
- Es la práctica habitual de marketplaces (mensajería enmascarada).
- **Tensión operativa y legal** → [[N03 Hallazgos criticos#H09 Teléfono de emergencia 24 h y chat sin contacto directo|H09]]: la norma exige entregar un teléfono de emergencia disponible 24/7 (Art. 7 num. 12, 🟡). Ese número debe ser **de Nanturia** (línea de coordinación), no el del guía, para no romper el diseño.
- El día del servicio hace falta coordinar el punto de encuentro: aislar totalmente al guía del cliente puede ser contraproducente.
- WhatsApp Business exige plantillas aprobadas y opt-in ([[N09 Verificaciones pendientes#V13 Condiciones de WhatsApp Business API|V13]]).

## Mejora propuesta
- **Chat dentro de la plataforma + WhatsApp** (misma conversación), con detección de teléfonos, correos y links (regex + ML liviano) y mensaje de advertencia.
- **Ventana de liberación**: el día del servicio, número proxy temporal o grupo de coordinación gestionado por Nanturia.
- **SLA del guía** (responder en ≤ 2 h en horario) con escalamiento a un operador humano.
- Registro de conversaciones (evidencia ante disputas) con retención definida ([[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]]).
- Incentivos legítimos contra la fuga: garantía Nanturia, seguro, reseñas verificadas, herramientas gratis.

## Reglas de negocio (especificación)
```text
SI mensaje CONTIENE patron(telefono|email|url|"escribeme al") ENTONCES bloquear + advertir
chat.liberacion = servicio.fecha - 6h  (proxy temporal)  HASTA servicio.fecha + 12h
guia.sla_respuesta <= 2h (horario 07:00-21:00) ; SI excede ENTONCES escalar(operador)
```

## Riesgos
[[N08 Registro de riesgos#R04 Desintermediación o ventas cerradas fuera de la plataforma|R04]], [[N08 Registro de riesgos#R15 Bloqueo de canales de mensajería o pagos|R15]], [[N08 Registro de riesgos#R09 Protección de datos personales|R09]].

## Por verificar
[[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]], [[N09 Verificaciones pendientes#V13 Condiciones de WhatsApp Business API|V13]].

## Próximos pasos
Prototipar con un único canal (WhatsApp Business) y 5 guías.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
