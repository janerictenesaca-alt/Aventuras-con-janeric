---
id: I29
tipo: idea
titulo: "Seguros y requisitos de las plataformas globales"
area: legal
estado: analizada
prioridad: alta
riesgo_legal: alto
fase: F0
origen: [A03, A18]
depende_de: []
relacionadas: [I01, I18, I31]
confianza: media
tags: [idea, legal, nanturia]
---
# I29 · Seguros y requisitos de las plataformas globales

> **Origen (audios):** [[A03 Exceso de documentacion y almacenamiento|A03]] [[A18 Seguros y plataformas globales|A18]] · **Área:** legal · **Prioridad:** alta · **Riesgo legal:** alto · **Fase:** F0 · **Confianza del análisis:** media
> **Relacionadas:** [[I01 Modelo en cadena con operadoras aliadas|I01]] [[I18 Automatizacion documental legal por ruta|I18]] [[I31 Estrategia de confianza frente a las grandes plataformas|I31]]

## Resumen fiel de lo dicho
Las plataformas como Airbnb y TripAdvisor venden experiencias pero es difícil entrar; se sospecha que por el seguro (¿$1 000 000 por actividad?), muy costoso. Un colega en Galápagos tiene ese tipo de seguro. Se pregunta cómo contratarlo y cómo, bajo la ley ecuatoriana más actualizada, se podría evitar la complejidad para los guías.

## Problema
Cobertura aseguradora que habilite ventas propias y en plataformas globales sin quebrar a los guías.

## Análisis
- **Ecuador (🟡):** fuentes secundarias indican que el Reglamento de Operación e Intermediación reformado (Acuerdo 2021-037) exige a agencias que operan aventura contar con **seguro de accidentes y de responsabilidad civil** que cubra a guías y turistas; no se encontró el monto en los textos leídos → [[N03 Hallazgos criticos#H11 Seguros obligatorios y monto sin verificar|H11]], [[N09 Verificaciones pendientes#V05 Seguros exigidos tipo monto y opciones de póliza paraguas|V05]].
- **Plataformas:** GetYourGuide exige seguro de responsabilidad general en todas las operaciones; Viator exige responsabilidad civil pública (PLI) para productos de alto riesgo y congela cuentas con documentación insuficiente; Airbnb Experiences exige los seguros que determine (🟡). El «$1 000 000» es una cifra típica de límite de cobertura: debe cotizarse, no asumirse.
- **No se puede evitar el seguro**; sí se puede **centralizarlo y abaratarlo**.

## Mejora propuesta
1. **Póliza paraguas (master policy) de Nanturia** con certificados por operador/ruta (consultar corredor de seguros).
2. **Exigir póliza propia** a cada operadora aliada y verificarla (vigencia, límites, exclusiones por modalidad).
3. **Micro-seguro de accidentes por persona** incluido en el precio (cotizar; hipótesis de costo bajo por pax).
4. **Seguro de viaje opcional** para turistas extranjeros (comisión).
5. **Verificación automática** de vigencia (fecha de vencimiento, alertas, bloqueo de ventas si vence).
6. Cuestionario para el corredor: modalidades cubiertas, límites por ocurrencia/agregado, deducibles, exclusiones, territorialidad, requisitos de guías.

## Reglas de negocio (especificación)
```text
venta.bloqueada SI poliza.vencida(operador) O poliza.no_cubre(modalidad)
alerta_vencimiento: 30, 15, 7 dias antes
```

## Riesgos
[[N08 Registro de riesgos#R02 Siniestro grave sin cobertura suficiente|R02]], [[N08 Registro de riesgos#R01 Incumplimiento normativo de agencia, intermediación y guías|R01]].

## Por verificar
[[N09 Verificaciones pendientes#V05 Seguros exigidos tipo monto y opciones de póliza paraguas|V05]].

## Próximos pasos
Pedir 3 cotizaciones (corredor nacional, la aseguradora del colega de Galápagos, una aseguradora de la competencia).

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
