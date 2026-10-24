---
id: I11
tipo: idea
titulo: "Paridad de precios entre operadoras y transporte desde distintas ciudades"
area: precios
estado: analizada
prioridad: media
riesgo_legal: medio
fase: F2
origen: [A20]
depende_de: [I03, I09]
relacionadas: [I27, I25]
confianza: media
tags: [idea, precios, nanturia]
---
# I11 · Paridad de precios entre operadoras y transporte desde distintas ciudades

> **Origen (audios):** [[A20 Precios entre operadoras y co-venta para llenar bus|A20]] · **Área:** precios · **Prioridad:** media · **Riesgo legal:** medio · **Fase:** F2 · **Confianza del análisis:** media
> **Depende de:** [[I03 Red de operadoras revendedoras y consolidacion de grupos|I03]] [[I09 Precio decreciente por tamano de grupo escalera de precios|I09]]
> **Relacionadas:** [[I27 Co-venta entre guias de una ciudad para llenar el bus pooling|I27]] [[I25 Complementos de hospedaje y transporte aceptar u omitir|I25]]

## Resumen fiel de lo dicho
Operadoras de ciudades distintas que venden el mismo tour en Morona Santiago tendrían precios diferentes por el costo de transporte (Cuenca ≠ Guayaquil), generando competencia desleal. Se propone un convenio con una empresa de transporte para reunir grupos de varias ciudades, que las operadoras cobren lo mismo y se repartan el valor del grupo, o que cada una ofrezca sus servicios, pero manteniendo un valor igual. Pide una lógica más estructurada.

## Problema
Competencia por precio entre revendedoras y costos de transporte heterogéneos.

## Análisis
- La disparidad nace al **mezclar** dos productos: el tour en destino y el traslado desde el origen.
- Un acuerdo entre competidoras para fijar precios iguales puede constituir práctica restrictiva (revisar la Ley Orgánica de Regulación y Control del Poder de Mercado, 🔴 no verificado) → mejor que **la plataforma publique una lista única** de precios fijada por el proveedor del servicio y no un pacto entre revendedoras.
- Un transportista no puede intermediar (Disp. Gen. 2ª, 🟡) pero sí ser proveedor registrado de transporte turístico.

## Mejora propuesta
- **Desacoplar**: (1) *Tour base* con precio único en destino; (2) *Traslado* como producto aparte con tarifa **por asiento y por ciudad de origen** (costo de bus / ocupación esperada).
- **Punto de encuentro en destino** como opción por defecto (el cliente llega por su cuenta o con el bus compartido).
- **Bus compartido**: convenio con una cooperativa de transporte turístico registrada; asientos vendidos por la plataforma; liquidación automática por asiento ([[I27 Co-venta entre guias de una ciudad para llenar el bus pooling|I27]]).
- **Reparto de ingresos** por pasajero aportado (no por acuerdo de precios).

## Reglas de negocio (especificación)
```text
PVP_tour(salida) = f(n)  # igual para todo canal
PVP_traslado(origen) = costo_bus(origen) / ocupacion_estimada(origen) * (1 + margen)
```

## Riesgos
[[N08 Registro de riesgos#R01 Incumplimiento normativo de agencia, intermediación y guías|R01]], [[N08 Registro de riesgos#R13 Margen insuficiente por precio mal calibrado|R13]].

## Por verificar
[[N09 Verificaciones pendientes#V15 Normas de transporte turístico y alojamiento si se venden como complementos|V15]], criterio de competencia (abogado).

## Próximos pasos
Cotizar bus Guayaquil-Cuenca-Quito → Morona Santiago con 2 cooperativas.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
