---
id: I17
tipo: idea
titulo: "Flujo de reserva con confirmación de disponibilidad"
area: producto
estado: analizada
prioridad: alta
riesgo_legal: bajo
fase: F1
origen: [A09]
depende_de: [I15]
relacionadas: [I13, I16, I20]
confianza: alta
tags: [idea, producto, nanturia]
---
# I17 · Flujo de reserva con confirmación de disponibilidad

> **Origen (audios):** [[A09 Flujo de consulta al guia y reembolso|A09]] · **Área:** producto · **Prioridad:** alta · **Riesgo legal:** bajo · **Fase:** F1 · **Confianza del análisis:** alta
> **Depende de:** [[I15 Modo turista y modo guia asistente de creacion de rutas|I15]]
> **Relacionadas:** [[I13 Incumplimiento del guia no activa el tour o no se presenta|I13]] [[I16 Bot intermediario cliente guia y prevencion de fuga de datos|I16]] [[I20 Asignacion automatica de guia cupos y desbordamiento|I20]]

## Resumen fiel de lo dicho
El turista pregunta por el tour en el sitio; el bot consulta al guía si está disponible; si el guía acepta, el cliente recibe la aceptación y continúa al pago.

## Problema
Evitar vender cupos que no existen sin frenar la conversión.

## Análisis
- El esquema «solicitar → esperar aceptación → pagar» es lento y pierde ventas, sobre todo con clientes extranjeros y diferencias horarias.
- Lo ideal: **disponibilidad publicada** (reserva instantánea) y «solicitud» solo para fechas no publicadas.

## Mejora propuesta
- **Calendario de disponibilidad** por guía/operadora (bloques, cupos, mínimos).
- **Reserva instantánea** con *hold* de cupo de 15-30 min durante el pago.
- **Solicitud** para fechas fuera de calendario, con respuesta en ≤ 2 h y expiración automática.
- Métrica de **tiempo de respuesta** que alimenta el ranking ([[I23 Ranking y visibilidad de guias operadoras y colaboradores|I23]]).
- Máquina de estados clara y trazable.

## Reglas de negocio (especificación)
```text
Reserva.estado:
  cotizada -> solicitada -> aceptada -> pagada -> confirmada -> en_curso -> completada
  ramas: cancelada_cliente | cancelada_proveedor | no_show | reembolsada | disputa
hold_cupo: 20 min ; SI no_pago ENTONCES liberar_cupo
solicitud.expira = 2h
```

## Métricas de éxito
Conversión de solicitud→pago ≥ 40 %; tasa de reservas instantáneas ≥ 70 %.

## Próximos pasos
Diagramar estados en [[N06 Arquitectura de plataforma|N06]]; definir tiempos con guías piloto.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
