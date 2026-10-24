---
id: I01
tipo: idea
titulo: "Modelo en cadena con operadoras aliadas"
area: modelo
estado: analizada
prioridad: alta
riesgo_legal: medio
fase: F0
origen: [A01, A03, A08, A11]
depende_de: [I29, I30]
relacionadas: [I02, I03, I05, I18]
confianza: media
tags: [idea, modelo, nanturia]
---
# I01 · Modelo en cadena con operadoras aliadas

> **Origen (audios):** [[A01 Operadoras aliadas en cadena|A01]] [[A03 Exceso de documentacion y almacenamiento|A03]] [[A08 Vender via operadoras nacionales y consolidar grupos|A08]] [[A11 Documentacion por actividad y modelo operadora vs guia|A11]] · **Área:** modelo · **Prioridad:** alta · **Riesgo legal:** medio · **Fase:** F0 · **Confianza del análisis:** media
> **Depende de:** [[I29 Seguros y requisitos de las plataformas globales|I29]] [[I30 Marco legal de los guias ambitos y plan de habilitacion|I30]]
> **Relacionadas:** [[I02 Solo un medio traslado de responsabilidad al guia|I02]] [[I03 Red de operadoras revendedoras y consolidacion de grupos|I03]] [[I05 Alianzas ancla Cueva de los Tayos Mateo y empresa de Hernan|I05]] [[I18 Automatizacion documental legal por ruta|I18]]

## Resumen fiel de lo dicho
Nanturia no puede operar en todo el país ni reunir los datos de cada ruta. Propone aliarse con operadoras que ya tienen la documentación y operan; Nanturia vende, cobra y les paga, formando una «cadena». Así se reduce el esfuerzo de ir ruta por ruta y se evitan responsabilidades. Duda si contratar a un tercero «está bien o está mal».

## Problema
- Cobertura geográfica: un solo equipo no puede levantar y mantener la documentación legal de rutas en todo el país ([[I18 Automatizacion documental legal por ruta|I18]]).
- Carga de responsabilidad civil y administrativa por actividades de riesgo.

## Análisis
- **Viabilidad legal: fuerte, con matices.** Para modalidades de aventura, el Reglamento de Guianza (2025) obliga a que los guías de aventura operen *a través de una agencia de servicios turísticos* declarada para aventura (Disp. Gen. 4ª) → [[N03 Hallazgos criticos#H02 Aventura solo vía agencia, el guía no puede operar directo|H02]]. Es decir, el modelo «operadora opera, guía trabaja para ella» no solo es válido: es el camino que la norma exige para rafting, canyoning, etc.
- Las agencias deben contratar solo proveedores registrados (Art. 17 y Art. 7 num. 6 y 15 del Reglamento de Operación e Intermediación, 🟡 numeración 2021-011) → Nanturia debe **verificar** el registro de cada aliada y guía.
- **La responsabilidad no desaparece**: quien vende responde ante el cliente (Art. 18-19 y 23) → [[N03 Hallazgos criticos#H06 La plataforma responde ante el cliente|H06]]. Lo que sí se logra es *trasladar el riesgo operativo por contrato* (indemnidad, pólizas, penalidades).
- La «cadena» añade puntos de falla (más actores = más cancelaciones potenciales) → [[I13 Incumplimiento del guia no activa el tour o no se presenta|I13]].

## Mejora propuesta
1. **Operador de registro (OR) por ruta**: toda ruta publicable tiene una agencia dual/operador turístico responsable de la operación, con documentos vigentes cargados y verificados.
2. **Contrato marco + anexo por ruta**: tarifa neta, ventana de pago (T+2), causales y penalidades de cancelación, póliza obligatoria, SLA de confirmación, cláusula de repetición.
3. **Due diligence estándar** (checklist de 12 puntos): registro de turismo, LUAF, póliza RC + accidentes, plan de operación y contingencia por modalidad, plan de mantenimiento, credenciales de guías, historial de incidentes.
4. **Scorecard de operadoras** (cumplimiento, reseñas, tiempo de respuesta, incidentes) que alimenta el ranking ([[I23 Ranking y visibilidad de guias operadoras y colaboradores|I23]]).
5. **Estrategia de arranque**: 2-3 operadoras ancla para modalidades de riesgo; guías directos solo para senderismo/cultural ([[I05 Alianzas ancla Cueva de los Tayos Mateo y empresa de Hernan|I05]], [[N04 Decisiones abiertas#D03 Modelo operativo operador de registro o intermediario puro|D03]]).
6. **Socios comunitarios**: los centros de turismo comunitario y los alojamientos pueden operar aventura dentro de sus linderos (Reglamento de Aventura, Art. 2 y Disp. Gen. 1.ª 🟢) → posibles operadores de registro en Morona Santiago, con sus propios documentos y pólizas ([[N03 Hallazgos criticos#H02 Aventura solo vía agencia, el guía no puede operar directo|H02]]).

## Reglas de negocio (especificación)
```text
Ruta.estado = "publicable" SI Y SOLO SI:
  existe OR con: registro_turismo vigente AND LUAF vigente AND poliza_RC vigente AND poliza_accidentes vigente
  AND plan_operacion_contingencia(modalidad) cargado AND plan_mantenimiento cargado
  AND existe >=1 guia con clasificacion que cubra (modalidad, canton)
Pago a OR: neto = PVP - take_rate(canal); liberar a T+2 despues de servicio.confirmado
```

## Riesgos
[[N08 Registro de riesgos#R07 Dependencia de pocas operadoras ancla|R07]] dependencia de pocas operadoras · [[N08 Registro de riesgos#R01 Incumplimiento normativo de agencia, intermediación y guías|R01]] incumplimiento normativo · conflicto de canal (la operadora vende directo).

## Métricas de éxito
- % de rutas con OR verificado = 100 % antes de publicar.
- Tasa de cumplimiento = servicios realizados / vendidos ≥ 97 %.
- Tiempo de onboarding de una operadora ≤ 7 días.

## Por verificar
[[N09 Verificaciones pendientes#V01 Texto consolidado del Reglamento de Operación e Intermediación Turística|V01]], [[N09 Verificaciones pendientes#V02 Requisitos exactos para ser agencia y costos|V02]], [[N09 Verificaciones pendientes#V03 Si un portal que vende tours sin operarlos califica como agencia de viajes|V03]].

## Próximos pasos
Listar operadoras del Catastro en Morona Santiago y provincias vecinas; entrevistar 5; redactar term sheet y contrato marco ([[N04 Decisiones abiertas#D03 Modelo operativo operador de registro o intermediario puro|D03]]).

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
