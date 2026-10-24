---
id: I28
tipo: idea
titulo: "Enlaces de pago y de ruta compartibles (marketing viral)"
area: crecimiento
estado: analizada
prioridad: alta
riesgo_legal: medio
fase: F1
origen: [A12, A23]
depende_de: [I07]
relacionadas: [I24, I03, I09]
confianza: media
tags: [idea, crecimiento, nanturia]
---
# I28 · Enlaces de pago y de ruta compartibles (marketing viral)

> **Origen (audios):** [[A12 Tours internacionales reserva y confianza|A12]] [[A23 Asignacion automatica cupos y rutas precreadas|A23]] · **Área:** crecimiento · **Prioridad:** alta · **Riesgo legal:** medio · **Fase:** F1 · **Confianza del análisis:** media
> **Depende de:** [[I07 Pagos retencion de fondos split y fondo de respaldo|I07]]
> **Relacionadas:** [[I24 QR en hoteles atribucion de origen y comision|I24]] [[I03 Red de operadoras revendedoras y consolidacion de grupos|I03]] [[I09 Precio decreciente por tamano de grupo escalera de precios|I09]]

## Resumen fiel de lo dicho
Los cobros se hacen por **links**: un guía le da el link al cliente para que pague, y el cliente ve la página (publicidad automática). Los guías pueden compartir links de rutas de colegas y la venta se hace por link.

## Problema
Convertir cada transacción en adquisición de nuevos usuarios y facilitar la venta por WhatsApp.

## Análisis
- Un **link de pago/reserva** pre-llenado (ruta, fecha, tamaño de grupo, referente) es una herramienta potente y barata.
- **Legal** → [[N03 Hallazgos criticos#H03 El guía no puede hacer agenciamiento turístico|H03]]: el guía no puede hacer «agenciamiento turístico» (Art. 48 lit. h, Guianza 2025 🟢). Si el guía solo *comparte* un link y la venta/cobro/contrato lo hace la agencia (Nanturia), se parece más a un referido; si el guía «vende» y cobra por su cuenta, el riesgo sube. Definir con criterio jurídico ([[N09 Verificaciones pendientes#V06 Legalidad de comisiones a colaboradores y de links de venta de guías|V06]]).
- El link debe contener la marca/ruta y el vendedor de registro (Nanturia), con factura emitida por la agencia.

## Mejora propuesta
- **Link con carrito**: `https://<dominio>/r/<ruta>?g=<n>&ref=<guia>&fecha=<yyyy-mm-dd>`, abre el checkout con precio por escalera ([[I09 Precio decreciente por tamano de grupo escalera de precios|I09]]).
- **Pago en 2 pasos** (fee de reserva ahora, saldo después) ([[I08 Reserva no reembolsable|I08]]).
- **Vista previa enriquecida** (Open Graph) para WhatsApp/Instagram.
- **Atribución** al referente y panel de comisión por canal ([[I24 QR en hoteles atribucion de origen y comision|I24]], [[N04 Decisiones abiertas#D07 Comisión por canal|D07]]).
- **Compartir para bajar el precio** (viralidad, [[I09 Precio decreciente por tamano de grupo escalera de precios|I09]]).
- Facturación por la agencia; el guía solo recibe su payout.

## Reglas de negocio (especificación)
```text
link = {ruta, fecha, n_pax, referente_id, canal}
checkout.vendedor_registro = Nanturia  # NUNCA el guia
SI referente.tipo == "guia" ENTONCES comision = take_rate("link_guia") # sujeto a V06
```

## Riesgos
[[N08 Registro de riesgos#R01 Incumplimiento normativo de agencia, intermediación y guías|R01]], [[N08 Registro de riesgos#R04 Desintermediación o ventas cerradas fuera de la plataforma|R04]].

## Por verificar
[[N09 Verificaciones pendientes#V06 Legalidad de comisiones a colaboradores y de links de venta de guías|V06]].

## Próximos pasos
Piloto manual: generar links por WhatsApp para 5 guías y medir conversión.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
