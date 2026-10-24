---
id: I13
tipo: idea
titulo: "Incumplimiento del guía (no activa el tour o no se presenta)"
area: operación
estado: analizada
prioridad: alta
riesgo_legal: medio
fase: F1
origen: [A09, A10, A11]
depende_de: [I07, I02]
relacionadas: [I17, I20]
confianza: alta
tags: [idea, operacion, nanturia]
---
# I13 · Incumplimiento del guía (no activa el tour o no se presenta)

> **Origen (audios):** [[A09 Flujo de consulta al guia y reembolso|A09]] [[A10 Doble pago y fondo de respaldo|A10]] [[A11 Documentacion por actividad y modelo operadora vs guia|A11]] · **Área:** operación · **Prioridad:** alta · **Riesgo legal:** medio · **Fase:** F1 · **Confianza del análisis:** alta
> **Depende de:** [[I07 Pagos retencion de fondos split y fondo de respaldo|I07]] [[I02 Solo un medio traslado de responsabilidad al guia|I02]]
> **Relacionadas:** [[I17 Flujo de reserva con confirmacion de disponibilidad|I17]] [[I20 Asignacion automatica de guia cupos y desbordamiento|I20]]

## Resumen fiel de lo dicho
Si el guía ya retiró el dinero y no llega (borrachera, resaca u otra causa), el cliente pierde el tour, se enoja y reclama; Nanturia devuelve y reclama al guía. Preguntas: ¿quién se hace cargo? ¿cómo se le cobra al guía?

## Problema
Evitar la falla y, si ocurre, reparar rápido al cliente y recuperar el costo.

## Análisis
- **Prevención > reparación.** Ejercer bajo influjo de alcohol está **prohibido** (Reglamento de Guianza 2025, Art. 48 lit. k 🟢) y es causal de sanción: debe reflejarse en términos y strikes.
- El modelo de retención de pagos ([[I07 Pagos retencion de fondos split y fondo de respaldo|I07]]) elimina el problema de «ya retiró el dinero».
- Quien responde ante el cliente es Nanturia ([[N03 Hallazgos criticos#H06 La plataforma responde ante el cliente|H06]]); la recuperación contra el guía es contractual.

## Mejora propuesta
- **Confirmaciones activas del guía**: T-48 h y T-24 h; el día del servicio, **check-in** con ubicación (o escaneo de QR en punto de encuentro) ≥ 30 min antes.
- **Pool de suplentes (standby)**: guías elegibles del cantón con opción de aceptar en < 2 h.
- **Sistema de strikes** y reputación visible para el sistema (no para el público en detalle).
- **Compensación al cliente**: reembolso 100 % o nueva fecha + crédito simbólico.
- **Alcoholímetro/declaración**: política de tolerancia cero; reporte del cliente con evidencia.
- **Fianza liviana**: retención de 5-10 % de payouts hasta cierto saldo de garantía por guía.

## Reglas de negocio (especificación)
```text
T-48h: guia.confirmar() ; SI no_responde a T-36h ENTONCES notificar(suplentes)
T-0 (servicio - 30min): guia.check_in() ; SI falta ENTONCES activar(suplente) AND avisar(cliente)
SI falla_confirmada ENTONCES refund 100% AND strike++ AND cargo_proveedor
```

## Riesgos
[[N08 Registro de riesgos#R03 Falla del proveedor por no presentarse|R03]], [[N08 Registro de riesgos#R10 Reputación por una mala experiencia temprana|R10]], [[N08 Registro de riesgos#R16 Calidad desigual de guías y rutas|R16]].

## Métricas de éxito
Fallas de guía < 1 % de salidas; tiempo medio de reemplazo < 2 h.

## Próximos pasos
Definir el contrato del guía con strikes; piloto de check-in por WhatsApp.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
