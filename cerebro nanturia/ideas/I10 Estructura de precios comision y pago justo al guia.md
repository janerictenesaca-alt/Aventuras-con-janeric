---
id: I10
tipo: idea
titulo: "Estructura de precios, comisión y pago justo al guía"
area: precios
estado: analizada
prioridad: alta
riesgo_legal: bajo
fase: F0
origen: [A03, A15, A25]
depende_de: [I09]
relacionadas: [I07, I11, I33]
confianza: media
tags: [idea, precios, nanturia]
---
# I10 · Estructura de precios, comisión y pago justo al guía

> **Origen (audios):** [[A03 Exceso de documentacion y almacenamiento|A03]] [[A15 Costo del guia y margen|A15]] [[A25 Precios de city tour aventura y trekking|A25]] · **Área:** precios · **Prioridad:** alta · **Riesgo legal:** bajo · **Fase:** F0 · **Confianza del análisis:** media
> **Depende de:** [[I09 Precio decreciente por tamano de grupo escalera de precios|I09]]
> **Relacionadas:** [[I07 Pagos retencion de fondos split y fondo de respaldo|I07]] [[I11 Paridad de precios y transporte desde distintas ciudades|I11]] [[I33 Equipos y seguridad arnes en El Churo y alquiler de equipos|I33]]

## Resumen fiel de lo dicho
Al guía se le pagarían unos $30-40 por salida; sobre eso Nanturia ganaría ~30 % (algo más o menos). City tour a pie/vehículo: $20-25 por persona. En aventura el guía gana ~$15 por persona más lo que alquile en equipos. Trekking: $40 todo incluido, de los cuales ~$20 serían del guía; si alquila arnés se ajusta el precio. Además, todos deben cobrar «acorde a lo que consideran que está bien cobrado».

## Problema
Definir un modelo de precios que sea competitivo para el turista, atractivo para el guía y rentable para Nanturia.

## Análisis
- El **30 % de comisión** es del orden de lo que se reporta en marketplaces turísticos (🔴 no verificado oficialmente; un reporte de usuario cita ~30 % en GetYourGuide). Debe cubrir pasarela (≈3-5 %), plataforma, marketing, soporte, provisión de incidentes y margen.
- Un solo porcentaje para todos los canales **incentiva la desintermediación**: el guía que trae su propio cliente paga lo mismo que por uno de Nanturia.
- «Pagar lo que cada uno considera justo» y «precio dinámico» se contraponen si el guía fija el precio final: conviene que el guía fije su **tarifa neta mínima** y la plataforma calcule el PVP.

## Mejora propuesta
- **Comisión por canal** ([[N04 Decisiones abiertas#D07 Comisión por canal|D07]]): ~30 % cliente captado por Nanturia · ~20 % cliente traído con el link del propio guía · 10-15 % reventa por operadora · colaboradores/hoteles: fee de referido a definir tras revisión legal ([[N03 Hallazgos criticos#H12 Comisiones a hoteles y transporte y prohibición de intermediar|H12]]).
- **Líneas de ingreso separadas**: tour (comisión), equipos (alquiler con precio fijo transparente, Art. 15 lit. m 🟡), add-ons ([[I25 Complementos de hospedaje y transporte aceptar u omitir|I25]]), fee de reserva ([[I08 Reserva no reembolsable|I08]]).
- **Tarifa neta mínima del proveedor** + PVP calculado ([[I09 Precio decreciente por tamano de grupo escalera de precios|I09]]); mostrar al guía el desglose (qué recibe, qué retiene Nanturia, por qué).
- **Costeo por ruta**: costo directo (guía, entradas, transporte, alimentación, depreciación de equipos, seguro por persona) + costo de plataforma.

## Reglas de negocio (especificación)
```text
take_rate(canal): organico_nanturia=0.30 | link_guia=0.20 | reventa_operadora=0.10..0.15 | referido_colaborador=TBD
PVP = (neto_proveedor_total) / (1 - take_rate) / n
neto_proveedor_total = G(n) + costos_variables + alquiler_equipos (si aplica)
```

## Riesgos
[[N08 Registro de riesgos#R13 Margen insuficiente por precio mal calibrado|R13]], [[N08 Registro de riesgos#R04 Desintermediación o ventas cerradas fuera de la plataforma|R04]].

## Por verificar
Benchmarks de comisión ([[N09 Verificaciones pendientes#V08 Proveedor de pagos split retención payouts y tarjetas extranjeras|V08]] para costo de pasarela; investigación de mercado propia).

## Próximos pasos
Hoja de costeo por ruta; validar con 3 guías el neto mínimo aceptable.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
