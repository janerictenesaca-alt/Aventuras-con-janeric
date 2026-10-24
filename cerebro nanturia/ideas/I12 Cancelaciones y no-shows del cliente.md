---
id: I12
tipo: idea
titulo: "Cancelaciones y no-shows del cliente (pérdida propia por entradas prepagadas)"
area: operación
estado: analizada
prioridad: alta
riesgo_legal: bajo
fase: F1
origen: [A17]
depende_de: [I08]
relacionadas: [I07, I13]
confianza: alta
tags: [idea, operacion, nanturia]
---
# I12 · Cancelaciones y no-shows del cliente (pérdida propia por entradas prepagadas)

> **Origen (audios):** [[A17 Cancelaciones de clientes y perdida propia|A17]] · **Área:** operación · **Prioridad:** alta · **Riesgo legal:** bajo · **Fase:** F1 · **Confianza del análisis:** alta
> **Depende de:** [[I08 Reserva no reembolsable|I08]]
> **Relacionadas:** [[I07 Pagos retencion de fondos split y fondo de respaldo|I07]] [[I13 Incumplimiento del guia no activa el tour o no se presenta|I13]]

## Resumen fiel de lo dicho
Por tercera vez, Janeric pagó de su bolsillo las entradas de un grupo que canceló a último momento; la persona que recibe el pago ya había organizado todo y no devuelve el dinero. Pide solucionar esto.

## Problema
Costos hundidos (entradas, alimentación, logística) asumidos por el guía/Nanturia cuando el cliente cancela tarde o no se presenta.

## Análisis
- Es un problema de **asimetría de riesgo**: el guía prepaga y el cliente no tiene incentivo a avisar.
- Soluciones comunes: depósito proporcional al costo no recuperable, política escalonada, reconfirmación, lista de espera.

## Mejora propuesta
1. **Depósito ≥ costos no recuperables de la salida** (entradas, alimentos, alquiler); para grupos grandes, mayor.
2. **Regla de prepago**: nunca prepagar entradas sin reserva pagada.
3. **Reconfirmación T-24 h** por WhatsApp/correo («Confirma tu asistencia»); sin respuesta → liberar cupo o llamar.
4. **Lista de espera** para recuperar cupos cancelados.
5. **Anticipo al guía** para entradas desde el pago del cliente (no de su bolsillo) ([[I07 Pagos retencion de fondos split y fondo de respaldo|I07]]).
6. Reflejar el riesgo en tarifa (provisión por no-show).
7. **No-show**: retención del depósito; compensar al proveedor por costos documentados.

## Reglas de negocio (especificación)
```text
deposito_minimo(salida) = sum(costos_no_recuperables(salida)) + fee_reserva
SI no_show ENTONCES retener(deposito) AND pagar(proveedor, costos_documentados)
reconfirmacion: enviar a T-24h; SI sin_respuesta a T-12h ENTONCES alerta(operaciones)
```

## Métricas de éxito
Tasa de no-show < 5 %; pérdidas por no-show cubiertas al 100 % por depósitos.

## Próximos pasos
Aplicar ya mismo la regla de prepago y el depósito en el piloto manual.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
