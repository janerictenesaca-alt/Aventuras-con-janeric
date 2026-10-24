---
id: I02
tipo: idea
titulo: "«Solo un medio»: traslado de responsabilidad al guía"
area: legal-modelo
estado: analizada
prioridad: alta
riesgo_legal: alto
fase: F0
origen: [A01, A09, A11]
depende_de: [I01]
relacionadas: [I07, I13, I31]
confianza: alta
tags: [idea, legal-modelo, nanturia]
---
# I02 · «Solo un medio»: traslado de responsabilidad al guía

> **Origen (audios):** [[A01 Operadoras aliadas en cadena|A01]] [[A09 Flujo de consulta al guia y reembolso|A09]] [[A11 Documentacion por actividad y modelo operadora vs guia|A11]] · **Área:** legal-modelo · **Prioridad:** alta · **Riesgo legal:** alto · **Fase:** F0 · **Confianza del análisis:** alta
> **Depende de:** [[I01 Modelo en cadena con operadoras aliadas|I01]]
> **Relacionadas:** [[I07 Pagos retencion de fondos split y fondo de respaldo|I07]] [[I13 Incumplimiento del guia no activa el tour o no se presenta|I13]] [[I31 Estrategia de confianza frente a las grandes plataformas|I31]]

## Resumen fiel de lo dicho
Si el guía falla, Nanturia devuelve el dinero y reclama al guía; o alternativamente entrega los datos del guía para que el cliente le reclame directamente. «Nosotros somos solo un medio para que ellos puedan ofertar su servicio»: la responsabilidad sería de quien presta el servicio.

## Problema
Evitar que Nanturia asuma pérdidas o responsabilidad por fallas de terceros.

## Análisis
- **Choca con la norma.** La intermediación (mediación, organización y *venta*) solo puede hacerse mediante agencias de servicios turísticos (Art. 12) → [[N03 Hallazgos criticos#H01 Intermediación solo vía agencia de viajes registrada|H01]]; la agencia debe prestar la totalidad de servicios contratados y, si falla por su causa, reembolsar o sustituir (Art. 18-19); el canal virtual debe incluir una *declaración de responsabilidad* de la agencia (Art. 22 num. 5) y la agencia responde por veracidad y cumplimiento incluso en canales de terceros (Art. 23) → [[N03 Hallazgos criticos#H06 La plataforma responde ante el cliente|H06]]. (🟡 texto 2021-011; confirmar consolidado, [[N09 Verificaciones pendientes#V01 Texto consolidado del Reglamento de Operación e Intermediación Turística|V01]]).
- **Reputacional:** el público desconfía de plataformas pequeñas ([[A12 Tours internacionales reserva y confianza|A12]]); decir «reclámale a él» destruye confianza.
- **Datos personales:** entregar datos del guía para reclamos requiere base legal y proporcionalidad (LOPDP, [[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]]).
- Un modelo de verdad «solo medio» sería un directorio/publicidad *sin* venta ni cobro: se pierde el flujo de ingresos y el control de calidad.

## Mejora propuesta
**«Responsabilidad frente al cliente + repetición contra el proveedor»**:
1. Nanturia responde al cliente (reembolso o sustitución en ≤ 24 h) y *recobra* del proveedor por contrato: compensación contra payouts futuros, cláusula penal, garantía.
2. «Garantía Nanturia» como diferenciador comercial (confianza, [[I31 Estrategia de confianza frente a las grandes plataformas|I31]]).
3. Canal único de reclamos; **nunca** exponer teléfono ni ID del guía al cliente.
4. Seguro y pólizas del proveedor como primera línea ([[I29 Seguros y requisitos de las plataformas globales|I29]]).

## Reglas de negocio (especificación)
```text
SI servicio.no_prestado POR causa_proveedor ENTONCES
   refund_cliente = 100% (incluye reserva)  Y  crear cargo_proveedor = monto + penalidad
   Y proveedor.strikes += 1
NUNCA exponer proveedor.telefono / proveedor.documento al cliente
```

## Riesgos
[[N08 Registro de riesgos#R01 Incumplimiento normativo de agencia, intermediación y guías|R01]], [[N08 Registro de riesgos#R03 Falla del proveedor por no presentarse|R03]], [[N08 Registro de riesgos#R10 Reputación por una mala experiencia temprana|R10]].

## Por verificar
[[N09 Verificaciones pendientes#V01 Texto consolidado del Reglamento de Operación e Intermediación Turística|V01]], [[N09 Verificaciones pendientes#V03 Si un portal que vende tours sin operarlos califica como agencia de viajes|V03]], [[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]]. Pedir criterio escrito a un abogado de turismo.

## Próximos pasos
Redactar términos y condiciones con esta lógica; modelar «cargo_proveedor» en el ledger ([[N06 Arquitectura de plataforma|N06]]).

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
