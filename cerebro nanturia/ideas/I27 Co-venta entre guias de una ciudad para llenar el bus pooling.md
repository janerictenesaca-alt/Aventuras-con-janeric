---
id: I27
tipo: idea
titulo: "Co-venta entre guías de una ciudad para llenar el bus (pooling de transporte)"
area: modelo
estado: analizada
prioridad: media
riesgo_legal: medio
fase: F2
origen: [A20]
depende_de: [I03, I11]
relacionadas: [I25, I21]
confianza: media
tags: [idea, modelo, nanturia]
---
# I27 · Co-venta entre guías de una ciudad para llenar el bus (pooling de transporte)

> **Origen (audios):** [[A20 Precios entre operadoras y co-venta para llenar bus|A20]] · **Área:** modelo · **Prioridad:** media · **Riesgo legal:** medio · **Fase:** F2 · **Confianza del análisis:** media
> **Depende de:** [[I03 Red de operadoras revendedoras y consolidacion de grupos|I03]] [[I11 Paridad de precios y transporte desde distintas ciudades|I11]]
> **Relacionadas:** [[I25 Complementos de hospedaje y transporte aceptar u omitir|I25]] [[I21 Rutas sin dueno ficha unica y multiples proveedores|I21]]

## Resumen fiel de lo dicho
En ciudades grandes (ej. Guayaquil), varios guías venden el mismo tour (ej. Carihuairazo [Carihuerazo, por confirmar]); cada uno aporta 2-3 personas y entre todos llenan una buseta cuyo mínimo exige el transportista; al llegar, cada guía toma a su gente y empieza la actividad. Quieren automatizar la práctica: publicaciones automáticas, guías de la misma ciudad que puedan sumarse o no. El audio termina cortado («Esto mismo, pero hecho para…»).

## Problema
Un solo guía no alcanza el mínimo para pagar el bus; entre varios sí.

## Análisis
- Es una práctica de **consolidación de demanda** que se puede formalizar como **salida compartida con anfitrión** ([[I03 Red de operadoras revendedoras y consolidacion de grupos|I03]]).
- Aparecen reglas: ratio guía/turistas por modalidad y tope de 16 ([[N03 Hallazgos criticos#H04 Tope de grupo de 16 y límites por modalidad|H04]]), responsabilidad de cada guía/agencia por sus pasajeros, póliza de transporte, y que cada venta pase por una agencia ([[N03 Hallazgos criticos#H03 El guía no puede hacer agenciamiento turístico|H03]]).
- Costo del bus por asiento = tarifa transparente; el riesgo es que alguien no llene sus cupos y los demás subsidien.

## Mejora propuesta
- **Oferta de asientos** (seat marketplace): un organizador publica «Salida desde Guayaquil, bus de 18, mínimo 12»; otros guías/operadoras toman cupos con precio por asiento.
- **Compromiso con depósito**: quien reserva cupos paga una seña por asiento; se libera el cupo si no se llena a T-72 h.
- **Notificaciones opt-in** a guías/operadoras de la misma ciudad cuando hay salida abierta.
- **Liquidación automática** del bus entre participantes por asientos usados.
- **Separación** del tour y del traslado ([[I11 Paridad de precios y transporte desde distintas ciudades|I11]]).
- Cuando el audio completado aclare el final de la idea («Esto mismo, pero hecho para…»), actualizar esta nota.

## Reglas de negocio (especificación)
```text
Bus(origen, capacidad, minimo, costo_total, estado)
cupo.confirmado SI seña_pagada ; SI sum(confirmados) < minimo a T-72h ENTONCES liberar() Y reembolsar()
costo_asiento = costo_total / ocupacion_real  # tope: costo_total/minimo
```

## Riesgos
[[N08 Registro de riesgos#R06 Arranque en frío sin oferta ni demanda|R06]], [[N08 Registro de riesgos#R03 Falla del proveedor por no presentarse|R03]], [[N08 Registro de riesgos#R01 Incumplimiento normativo de agencia, intermediación y guías|R01]].

## Por verificar
[[N09 Verificaciones pendientes#V15 Normas de transporte turístico y alojamiento si se venden como complementos|V15]], [[N09 Verificaciones pendientes#V06 Legalidad de comisiones a colaboradores y de links de venta de guías|V06]].

## Próximos pasos
Pedir a Janeric el final del audio; modelar «Bus» como entidad en [[N06 Arquitectura de plataforma|N06]].

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
