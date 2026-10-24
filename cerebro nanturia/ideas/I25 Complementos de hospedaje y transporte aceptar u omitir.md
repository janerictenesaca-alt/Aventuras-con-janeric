---
id: I25
tipo: idea
titulo: "Complementos de hospedaje y transporte (aceptar u omitir)"
area: producto
estado: analizada
prioridad: media
riesgo_legal: medio
fase: F2
origen: [A22]
depende_de: [I17, I14]
relacionadas: [I11, I27, I10]
confianza: media
tags: [idea, producto, nanturia]
---
# I25 · Complementos de hospedaje y transporte (aceptar u omitir)

> **Origen (audios):** [[A22 Aliados de hospedaje y transporte|A22]] · **Área:** producto · **Prioridad:** media · **Riesgo legal:** medio · **Fase:** F2 · **Confianza del análisis:** media
> **Depende de:** [[I17 Flujo de reserva con confirmacion de disponibilidad|I17]] [[I14 Plataforma estilo Airbnb solo tours con mapa y buses|I14]]
> **Relacionadas:** [[I11 Paridad de precios y transporte desde distintas ciudades|I11]] [[I27 Co-venta entre guias de una ciudad para llenar el bus pooling|I27]] [[I10 Estructura de precios comision y pago justo al guia|I10]]

## Resumen fiel de lo dicho
Al terminar de comprar un tour, ofrecer «¿quieres que te reserve hotel?» con opciones sí/omitir; si acepta, ver lista de hoteles de la ciudad con precios y reservar. Lo mismo con transporte puerta a puerta. Los socios deben tener una interfaz muy simple («menos es más»).

## Problema
Aumentar el valor por reserva y facilitar la logística del turista sin construir un Airbnb.

## Análisis
- Las agencias pueden vender alojamiento y servicios turísticos y mediar en transporte turístico (Art. 15 lit. d y f, 🟡) → es legalmente coherente.
- El momento post-compra es el de mayor disposición a comprar complementos.
- Atención con [[N03 Hallazgos criticos#H12 Comisiones a hoteles y transporte y prohibición de intermediar|H12]]: alojamiento y transporte como *proveedores* son válidos; lo prohibido es operar/intermediar *a través* de ellos.
- La simplicidad del lado hotel es clave: no replicar la complejidad de Airbnb.

## Mejora propuesta
- **Una pantalla de complementos** tras el pago: «Agregar alojamiento / traslado» o «Omitir».
- **Lado hotel**: calendario mínimo (disponible/no), precio por noche, botón «confirmar» por WhatsApp o correo; sin motor de reservas complejo en v1.
- **Transporte**: proveedores registrados de transporte turístico; precio por pasajero y punto de recogida; reutiliza la tarifa por origen ([[I11 Paridad de precios y transporte desde distintas ciudades|I11]]).
- Las cancelaciones del complemento heredan la política del tour; comisión de intermediación 10-15 % (🔴 a negociar).
- Medición: tasa de aceptación del complemento.

## Reglas de negocio (especificación)
```text
checkout.post_pago: ofrecer(add_ons[hospedaje, transporte]) ; opcion "omitir" siempre visible
add_on.cancelacion = heredar(reserva_tour.politica) salvo acuerdo del proveedor
```

## Riesgos
[[N08 Registro de riesgos#R08 Complejidad excesiva del MVP|R08]], [[N08 Registro de riesgos#R10 Reputación por una mala experiencia temprana|R10]].

## Métricas de éxito
Aceptación de add-ons ≥ 20 %; ingresos por add-on / reserva.

## Por verificar
[[N09 Verificaciones pendientes#V15 Normas de transporte turístico y alojamiento si se venden como complementos|V15]].

## Próximos pasos
Acordar con 3 hoteles y 1 transportista del cantón piloto un formato de confirmación por WhatsApp.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
