---
id: I03
tipo: idea
titulo: "Red de operadoras revendedoras y consolidación de grupos"
area: modelo
estado: analizada
prioridad: alta
riesgo_legal: medio
fase: F2
origen: [A08, A20]
depende_de: [I01, I09, I21]
relacionadas: [I11, I27, I28]
confianza: media
tags: [idea, modelo, nanturia]
---
# I03 · Red de operadoras revendedoras y consolidación de grupos

> **Origen (audios):** [[A08 Vender via operadoras nacionales y consolidar grupos|A08]] [[A20 Precios entre operadoras y co-venta para llenar bus|A20]] · **Área:** modelo · **Prioridad:** alta · **Riesgo legal:** medio · **Fase:** F2 · **Confianza del análisis:** media
> **Depende de:** [[I01 Modelo en cadena con operadoras aliadas|I01]] [[I09 Precio decreciente por tamano de grupo escalera de precios|I09]] [[I21 Rutas sin dueno ficha unica y multiples proveedores|I21]]
> **Relacionadas:** [[I11 Paridad de precios y transporte desde distintas ciudades|I11]] [[I27 Co-venta entre guias de una ciudad para llenar el bus pooling|I27]] [[I28 Enlaces de pago y de ruta compartibles marketing viral|I28]]

## Resumen fiel de lo dicho
No trabajar con guías sueltos sino con operadoras de todo el país: suben las rutas por sector, las operadoras toman el link y venden. Ejemplo: Guayaquil vende 5 personas, Cuenca 2, Quito 1, Machala 1, Guayaquil otras 2 → el mismo día se arma el grupo en Méndez. La plataforma le da trabajo al guía.

## Problema
**Liquidez de salidas**: ninguna ciudad aporta suficiente demanda por sí sola para llenar una salida; el mínimo operativo no se cumple.

## Análisis
- Es el **mecanismo central de liquidez** del marketplace (múltiples canales de demanda sobre una misma oferta).
- Legalmente, las operadoras revendedoras son *agencias* (pueden intermediar; una agencia puede representar a otras, Art. 15 lit. h → 🟡); la operación la hace la operadora local.
- Riesgos: guerra de precios entre revendedoras ([[I11 Paridad de precios y transporte desde distintas ciudades|I11]]), sobre-reserva de cupos, conciliación de pagos multi-actor, disputas de atribución.

## Mejora propuesta
- Objeto **Salida compartida**: `Salida(ruta, fecha, cupo_max, minimo, tiers_precio, operador, estado)`; los canales reservan **cupos** (allotment) o venden contra disponibilidad en tiempo real.
- **Precio de lista único por salida**, independiente del canal; la revendedora gana una **comisión fija** (propuesta 10-15 % del PVP, [[N04 Decisiones abiertas#D07 Comisión por canal|D07]]) en vez de alterar el precio.
- **Cutoff T-48 h**: si no se alcanza el mínimo → mover de fecha o devolver (mensaje automático).
- **Panel de revendedora**: ver cupos, reservar, link personalizado con atribución, liquidación mensual/quincenal.
- Notificaciones push a canales cuando una salida está a ≤ 2 cupos del mínimo («falta 1 para confirmar»).

## Reglas de negocio (especificación)
```text
precio_publico(salida) = f(n_confirmados)   # NO depende del canal
comision_canal = pct_canal * precio_publico * n_pax_aportados
SI now >= salida.fecha - 48h Y n_confirmados < minimo ENTONCES estado = "reprogramar_o_reembolsar"
```

## Riesgos
[[N08 Registro de riesgos#R06 Arranque en frío sin oferta ni demanda|R06]] arranque en frío · [[N08 Registro de riesgos#R07 Dependencia de pocas operadoras ancla|R07]] · [[N08 Registro de riesgos#R04 Desintermediación o ventas cerradas fuera de la plataforma|R04]].

## Métricas de éxito
% de salidas que alcanzan el mínimo ≥ 70 % (objetivo piloto); ocupación media ≥ 60 %; share de ventas por canal.

## Por verificar
[[N09 Verificaciones pendientes#V02 Requisitos exactos para ser agencia y costos|V02]], [[N09 Verificaciones pendientes#V06 Legalidad de comisiones a colaboradores y de links de venta de guías|V06]].

## Próximos pasos
Prototipar la salida compartida con una sola ruta y 2 operadoras reales ([[N07 Hoja de ruta por fases|N07]], fase F2).

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
