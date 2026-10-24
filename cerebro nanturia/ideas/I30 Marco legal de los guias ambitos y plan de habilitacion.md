---
id: I30
tipo: idea
titulo: "Marco legal de los guías, ámbitos y plan de habilitación"
area: legal
estado: analizada
prioridad: alta
riesgo_legal: medio
fase: F0
origen: [A04, A19]
depende_de: []
relacionadas: [I06, I20, I21]
confianza: media
tags: [idea, legal, nanturia]
---
# I30 · Marco legal de los guías, ámbitos y plan de habilitación

> **Origen (audios):** [[A04 Licencias de guia y tramite engorroso|A04]] [[A19 Reclutar guias desde el catastro|A19]] · **Área:** legal · **Prioridad:** alta · **Riesgo legal:** medio · **Fase:** F0 · **Confianza del análisis:** media
> **Relacionadas:** [[I06 Reclutamiento de guias desde el Catastro Turistico|I06]] [[I20 Asignacion automatica de guia cupos y desbordamiento|I20]] [[I21 Rutas sin dueno ficha unica y multiples proveedores|I21]]

## Resumen fiel de lo dicho
Para guiar a pie en su cantón hay que ser guía local; para actividades de río, guía de aventura en la especialidad (rafting, canyoning…); para salir a otro cantón, guía nacional; y para operar en todo el país, se «fusionan» local + aventura + nacional. El trámite es engorroso; se busca hacerlo más rápido y ágil cumpliendo la ley.

## Problema
Entender qué puede operar cada guía y cómo acelerar su habilitación.

## Análisis
- Según el **Reglamento de Guianza del Ecuador Continental (2025)** (🟢) existen **5 clasificaciones** con vigencia de 4 años: Local; Nacional; Nacional Especializado en Patrimonio; Nacional Especializado en Aventura; **Guía de Turismo de Aventura**. El «Guía de Turismo de Aventura» requiere bachiller + competencias laborales + primeros auxilios en zonas agrestes (50 h) + certificación de habilidad (o curso) + nivel B1 y puede guiar **a nivel continental** en las modalidades acreditadas; el **Local** solo en el cantón para el cual se registró.
- **No aparece** en ese texto una cadena obligatoria «local → aventura → nacional» ni una «fusión de tres licencias» → [[N03 Hallazgos criticos#H05 Escalera de licencias distinta a la de los audios|H05]]. Puede ser el régimen anterior o una práctica local; conviene verificar con la autoridad ([[N09 Verificaciones pendientes#V04 Escalera de licencias y ámbito de guías|V04]]).
- Además, los guías de aventura **no pueden operar de forma directa** modalidades de aventura (salvo senderismo): deben hacerlo a través de una agencia declarada → [[N03 Hallazgos criticos#H02 Aventura solo vía agencia, el guía no puede operar directo|H02]].
- Nanturia **no puede acortar** la ley, pero sí **acompañar** el trámite.

## Mejora propuesta
- **Matriz de elegibilidad** guía × modalidad × territorio incorporada al sistema ([[I20 Asignacion automatica de guia cupos y desbordamiento|I20]]).
- **Servicio «Habilitación»** (oportunidad de ingreso): checklist de requisitos por clasificación, calendario de cursos autorizados (primeros auxilios 24/50 h, certificación de habilidad, B1), gestión del RUC y del registro.
- **Convenios** con centros de capacitación avalados; descuentos para guías de la red.
- **Alertas de vigencia** (4 años) y bloqueo automático al vencer.

## Reglas de negocio (especificación)
```text
ambito(local) = {canton_registro (+ areas protegidas del canton de domicilio)}
ambito(nacional | nacional_aventura | aventura) = territorio continental (modalidades acreditadas)
aventura (excepto senderismo) -> SOLO via agencia declarada ; guia no opera directo
vigencia(clasificacion) = 4 anios desde emision
```

## Riesgos
[[N08 Registro de riesgos#R01 Incumplimiento normativo de agencia, intermediación y guías|R01]], [[N08 Registro de riesgos#R11 Cambios regulatorios y transición institucional|R11]].

## Por verificar
[[N09 Verificaciones pendientes#V04 Escalera de licencias y ámbito de guías|V04]], [[N09 Verificaciones pendientes#V11 Límites de grupo por modalidad y por área protegida para las 16 rutas|V11]].

## Próximos pasos
Obtener la tabla de homologación y consultar a la oficina zonal de turismo; construir la matriz en la base de datos.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
