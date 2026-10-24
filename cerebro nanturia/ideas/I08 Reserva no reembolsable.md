---
id: I08
tipo: idea
titulo: "Reserva no reembolsable"
area: pagos
estado: analizada
prioridad: alta
riesgo_legal: alto
fase: F1
origen: [A12, A17, A27]
depende_de: [I12]
relacionadas: [I04, I07, I09]
confianza: media
tags: [idea, pagos, nanturia]
---
# I08 · Reserva no reembolsable

> **Origen (audios):** [[A12 Tours internacionales reserva y confianza|A12]] [[A17 Cancelaciones de clientes y perdida propia|A17]] [[A27 Reserva no reembolsable|A27]] · **Área:** pagos · **Prioridad:** alta · **Riesgo legal:** alto · **Fase:** F1 · **Confianza del análisis:** media
> **Depende de:** [[I12 Cancelaciones y no-shows del cliente|I12]]
> **Relacionadas:** [[I04 Tours internacionales para ecuatorianos via operadoras aliadas|I04]] [[I07 Pagos retencion de fondos split y fondo de respaldo|I07]] [[I09 Precio decreciente por tamano de grupo escalera de precios|I09]]

## Resumen fiel de lo dicho
La reserva es simbólica y **nunca se devuelve**: asegura al guía que los clientes vendrán y financia el mantenimiento de la plataforma. Las cancelaciones son gratuitas, pero la reserva no se reembolsa. En tours internacionales, la reserva garantiza a la operadora aliada.

## Problema
Reducir cancelaciones/no-shows y financiar costos fijos de plataforma sin castigar injustamente al cliente.

## Análisis
- **Valor:** actúa como señal de compromiso y cubre costos de adquisición y pasarela.
- **Tensión interna:** «cancelación gratis» y «reserva no se devuelve» se contradicen si no se define con precisión qué es cada cosa.
- **Tensión legal** → [[N03 Hallazgos criticos#H07 Reserva no reembolsable vs derechos del usuario y retracto|H07]]: el usuario tiene derecho a conocer *antes* las políticas de cobro, cancelación y reembolso (Art. 4 num. 3, 🟡); si el servicio no se presta por causa de la agencia procede reembolso o sustitución (Art. 19); además puede aplicar el derecho de retracto de la Ley Orgánica de Defensa del Consumidor (una fuente periodística menciona 15 días en el Art. 45; **no verificado** para servicios turísticos con fecha fija) → [[N09 Verificaciones pendientes#V07 Derecho de retracto y reserva no reembolsable|V07]].
- **Internacional:** el cliente extranjero con tarjeta puede disputar el cargo (contracargo) si la política no fue clara.

## Mejora propuesta
Separar en **dos conceptos**:
1. **Fee de reserva (service fee)**, no reembolsable, claramente rotulado (propuesta: monto fijo o 10-15 %), que se devuelve *solo* si falla Nanturia o el proveedor.
2. **Depósito del tour**, reembolsable según calendario: 100 % hasta T-72 h; 50 % entre T-72 h y T-24 h; 0 % después (calibrar con costos no recuperables, [[I12 Cancelaciones y no-shows del cliente|I12]]).
- Aceptación explícita de la política en el checkout (checkbox + marca de tiempo + IP) y copia por correo.
- Mensaje único y consistente: «Cancelación gratuita hasta 72 h antes. El fee de reserva ($X) no es reembolsable».
- Excepciones automáticas: clima/fuerza mayor (reprogramar o reembolsar menos costos no recuperables), mínimo de grupo no alcanzado (reembolso total).

## Reglas de negocio (especificación)
```text
SI causa_cancelacion IN {proveedor, nanturia, grupo_minimo_no_alcanzado} ENTONCES refund = 100% (incluye fee)
SI causa_cancelacion == cliente ENTONCES refund = deposito * tabla(T_hasta_servicio); fee = 0 refund
SI causa == fuerza_mayor ENTONCES opciones = {reprogramar, reembolso - costos_no_recuperables}
```

## Riesgos
[[N08 Registro de riesgos#R01 Incumplimiento normativo de agencia, intermediación y guías|R01]], [[N08 Registro de riesgos#R05 Contracargos y fraude de pago|R05]], [[N08 Registro de riesgos#R10 Reputación por una mala experiencia temprana|R10]].

## Por verificar
[[N09 Verificaciones pendientes#V07 Derecho de retracto y reserva no reembolsable|V07]].

## Próximos pasos
Redactar la política de cancelación en lenguaje claro y validarla con abogado ([[N04 Decisiones abiertas#D04 Política de reserva y reembolsos|D04]]); probarla con 20 clientes del piloto.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
