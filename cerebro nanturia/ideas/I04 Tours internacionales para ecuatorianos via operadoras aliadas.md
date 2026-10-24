---
id: I04
tipo: idea
titulo: "Tours internacionales para ecuatorianos vía operadoras aliadas"
area: modelo
estado: analizada
prioridad: baja
riesgo_legal: medio
fase: F3
origen: [A06, A12]
depende_de: [I01, I07, I08]
relacionadas: [I05, I34]
confianza: media
tags: [idea, modelo, nanturia]
---
# I04 · Tours internacionales para ecuatorianos vía operadoras aliadas

> **Origen (audios):** [[A06 Alianzas Mateo Hernan y sitio tipo Airbnb con buses|A06]] [[A12 Tours internacionales reserva y confianza|A12]] · **Área:** modelo · **Prioridad:** baja · **Riesgo legal:** medio · **Fase:** F3 · **Confianza del análisis:** media
> **Depende de:** [[I01 Modelo en cadena con operadoras aliadas|I01]] [[I07 Pagos retencion de fondos split y fondo de respaldo|I07]] [[I08 Reserva no reembolsable|I08]]
> **Relacionadas:** [[I05 Alianzas ancla Cueva de los Tayos Mateo y empresa de Hernan|I05]] [[I34 Expansion nacional primero internacional despues|I34]]

## Resumen fiel de lo dicho
Aliarse con operadoras que vendan tours internacionales para ofrecerlos a ecuatorianos en el sitio. El cliente paga una reserva que nunca se devuelve (para que la aliada sepa que el cliente irá y para financiar la plataforma). La documentación de salida del país se ingresa por el sitio y llega a la aliada; se evita la oficina para generar un modelo 100 % online. Si la compra no se concreta, la aliada debería recibir algo.

## Problema
Ampliar el catálogo y los ingresos más allá del turismo receptivo local.

## Análisis
- Las agencias pueden organizar y comercializar paquetes en el exterior (turismo emisivo) y tramitar documentos de viaje (Art. 15 lit. b y j, 🟡).
- Es un segmento **maduro y competido** (agencias grandes, aerolíneas, OTAs); Nanturia no tiene ventaja diferencial y consumiría foco del core receptivo.
- Documentos de viaje = **datos sensibles** (pasaporte, salud, menores) → LOPDP ([[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]]).
- La combinación «reserva no reembolsable + trámite fallido» es la clásica fuente de reclamos ([[N03 Hallazgos criticos#H07 Reserva no reembolsable vs derechos del usuario y retracto|H07]]).

## Mejora propuesta
- **Posponer a F3.** Primero probar el core receptivo.
- Cuando se haga: Nanturia como *representante de ventas* de la aliada (Art. 15 lit. h) y la aliada como vendedor de registro → menor carga y responsabilidad.
- Separar dos cobros: **fee de servicio Nanturia** (no reembolsable, claramente rotulado) y **depósito de la aliada** (según la política de la aliada). Si el cliente no culmina, la aliada cobra su cargo de gestión pactado, Nanturia su fee.
- Formularios de viaje cifrados, con retención mínima y acceso restringido.

## Reglas de negocio (especificación)
```text
cobro_inicial = fee_nanturia (no reembolsable) + deposito_aliada (reembolsable segun politica_aliada)
SI compra_no_culmina POR cliente ENTONCES aliada.cobra(cargo_gestion_pactado)
```

## Riesgos
[[N08 Registro de riesgos#R09 Protección de datos personales|R09]], [[N08 Registro de riesgos#R10 Reputación por una mala experiencia temprana|R10]], [[N08 Registro de riesgos#R08 Complejidad excesiva del MVP|R08]].

## Por verificar
[[N09 Verificaciones pendientes#V01 Texto consolidado del Reglamento de Operación e Intermediación Turística|V01]], [[N09 Verificaciones pendientes#V07 Derecho de retracto y reserva no reembolsable|V07]], [[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]].

## Próximos pasos
Ninguno antes de cerrar F1; mantener la idea en backlog.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
