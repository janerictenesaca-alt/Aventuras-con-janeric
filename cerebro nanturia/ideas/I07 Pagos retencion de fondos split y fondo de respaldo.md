---
id: I07
tipo: idea
titulo: "Pagos: retención de fondos, split y fondo de respaldo"
area: pagos
estado: analizada
prioridad: alta
riesgo_legal: medio
fase: F1
origen: [A02, A03, A09, A10, A11]
depende_de: [I08, I13]
relacionadas: [I02, I12, I28]
confianza: media
tags: [idea, pagos, nanturia]
---
# I07 · Pagos: retención de fondos, split y fondo de respaldo

> **Origen (audios):** [[A02 Sitio web tipo Airbnb bot intermediario y cobros|A02]] [[A03 Exceso de documentacion y almacenamiento|A03]] [[A09 Flujo de consulta al guia y reembolso|A09]] [[A10 Doble pago y fondo de respaldo|A10]] [[A11 Documentacion por actividad y modelo operadora vs guia|A11]] · **Área:** pagos · **Prioridad:** alta · **Riesgo legal:** medio · **Fase:** F1 · **Confianza del análisis:** media
> **Depende de:** [[I08 Reserva no reembolsable|I08]] [[I13 Incumplimiento del guia no activa el tour o no se presenta|I13]]
> **Relacionadas:** [[I02 Solo un medio traslado de responsabilidad al guia|I02]] [[I12 Cancelaciones y no-shows del cliente|I12]] [[I28 Enlaces de pago y de ruta compartibles marketing viral|I28]]

## Resumen fiel de lo dicho
El cliente haría un **doble pago** (uno al guía y otro al sitio). Si el guía no activa el tour, Nanturia necesitaría un dinero de respaldo para devolver lo que «el guía se robó», y luego cobrárselo al guía (descontándolo del siguiente tour o con días de gracia). Además se quiere automatizar los cobros por transferencias y depósitos y que todos reciban un pago justo.

## Problema
Evitar que el dinero del cliente quede en manos del guía antes del servicio y gestionar reembolsos sin quebrar la caja.

## Análisis
- **La causa raíz es pagar al guía antes de prestar el servicio.** Si Nanturia retiene el pago hasta la ejecución, el problema «el guía se llevó el dinero» desaparece; el fondo de respaldo pasa a cubrir solo contracargos y reintegros residuales.
- **Doble pago = mala idea**: agrega fricción para el cliente, expone al riesgo de fuga (el guía cobra fuera) y no protege al cliente.
- Pasarelas en Ecuador (🟡 por verificar): PayPhone anuncia «Payment Split» (se habilita previa validación; el negocio debe calificar como marketplace/e-commerce); Kushki obtuvo estatus de agregador de pagos en Ecuador. No se confirmó split en Datafast/PlacetoPay → [[N09 Verificaciones pendientes#V08 Proveedor de pagos split retención payouts y tarjetas extranjeras|V08]].
- Encuadre jurídico: si Nanturia *vende* como agencia, el cobro es ingreso propio y el pago al proveedor es costo; si actuara como *mandatario* que cobra por cuenta de terceros podría tocar regulación de pagos/servicios financieros → [[N09 Verificaciones pendientes#V09 Tratamiento tributario|V09]], consultar abogado y contador.

## Mejora propuesta
**Waterfall de pagos** (un solo pago visible para el cliente):
1. Cliente paga 100 % (o fee de reserva + saldo) a Nanturia.
2. Nanturia reconoce su comisión al confirmarse el servicio.
3. **Payout al proveedor a T+2** tras el check-in del servicio.
4. **Anticipo opcional** (≤ 30 % del neto) para costos de entrada, solo a proveedores con buen puntaje ([[I12 Cancelaciones y no-shows del cliente|I12]]).
5. **Fondo de contingencia** = 2× la exposición mensual esperada (ver tabla en [[N05 Modelo financiero y precios|N05]]).
6. **Compensación automática**: cualquier cargo al proveedor se descuenta de sus próximos payouts; si no hay saldo, plazo de gracia de 7 días y luego suspensión.
7. **Strikes**: 1.ª falla advertencia, 2.ª suspensión de 30 días, 3.ª baja.

## Reglas de negocio (especificación)
```text
payout.fecha = servicio.fecha + 2 dias   # solo SI servicio.estado == "completado"
payout.monto = neto_proveedor - sum(cargos_pendientes)
fondo_contingencia >= 2 * ventas_mensuales * tasa_falla_estimada
SI proveedor.saldo < 0 Y dias_en_mora > 7 ENTONCES proveedor.estado = "suspendido"
```

## Riesgos
[[N08 Registro de riesgos#R05 Contracargos y fraude de pago|R05]] contracargos · [[N08 Registro de riesgos#R03 Falla del proveedor por no presentarse|R03]] · [[N08 Registro de riesgos#R15 Bloqueo de canales de mensajería o pagos|R15]] bloqueo de pasarela · [[N08 Registro de riesgos#R13 Margen insuficiente por precio mal calibrado|R13]].

## Métricas de éxito
Reembolsos por falla del proveedor < 2 % de las ventas; días de caja ≥ 30; contracargos < 0,5 %.

## Por verificar
[[N09 Verificaciones pendientes#V08 Proveedor de pagos split retención payouts y tarjetas extranjeras|V08]], [[N09 Verificaciones pendientes#V09 Tratamiento tributario|V09]].

## Próximos pasos
Pedir a PayPhone y Kushki: split, retención, payouts, comisiones, tarjetas extranjeras ([[N04 Decisiones abiertas#D05 Proveedor de pagos y custodia de fondos|D05]]).

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
