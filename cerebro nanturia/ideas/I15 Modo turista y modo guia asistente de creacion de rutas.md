---
id: I15
tipo: idea
titulo: "Modo turista y modo guía; asistente de creación de rutas"
area: producto
estado: analizada
prioridad: alta
riesgo_legal: bajo
fase: F1
origen: [A02, A05, A13, A21]
depende_de: [I18]
relacionadas: [I06, I14, I22]
confianza: alta
tags: [idea, producto, nanturia]
---
# I15 · Modo turista y modo guía; asistente de creación de rutas

> **Origen (audios):** [[A02 Sitio web tipo Airbnb bot intermediario y cobros|A02]] [[A05 Reducir friccion del guia al subir rutas|A05]] [[A13 Un proyecto por ruta 16 rutas|A13]] [[A21 Modo turista y modo guia creacion de rutas|A21]] · **Área:** producto · **Prioridad:** alta · **Riesgo legal:** bajo · **Fase:** F1 · **Confianza del análisis:** alta
> **Depende de:** [[I18 Automatizacion documental legal por ruta|I18]]
> **Relacionadas:** [[I06 Reclutamiento de guias desde el Catastro Turistico|I06]] [[I14 Plataforma estilo Airbnb solo tours con mapa y buses|I14]] [[I22 Biblioteca de rutas precreadas y onboarding|I22]]

## Resumen fiel de lo dicho
Debe haber un modo turista (simple) y un modo guía (más largo, con datos técnicos: coordenadas, fotos, dirección, mapa). Se necesita un formato o aplicación en el que el guía solo ingrese los datos que exige la ley; después de aprobada, la ruta se puede ofertar. También: subir información debe ser «súper fácil» y se pregunta cómo evitar que el guía tenga tantos «peros» para publicar.

## Problema
La barrera de entrada (documentación y datos técnicos) ahuyenta a los guías y retrasa la publicación de rutas.

## Análisis
- La documentación mínima proviene del Reglamento de Aventura (Art. 10): plan de operación y contingencia por modalidad, plan de mantenimiento, croquis, georreferencia, condiciones, edad mínima, política de accidentes, riesgos → [[I18 Automatizacion documental legal por ruta|I18]].
- Un buen asistente convierte «un proyecto de ruta» en **pasos cortos con ayuda contextual y plantillas**.
- Los guías ya trabajan con **audios** (como en este proceso): voz→texto reduce fricción.

## Mejora propuesta
**Asistente en 7 pasos** (guardado automático, uso móvil, modo sin conexión):
1. Modalidad y cantón (el sistema muestra los requisitos aplicables y quién puede operarla).
2. **Trazado en mapa** (dibujar o importar GPX; distancia, desnivel, puntos de interés calculados).
3. Ficha técnica (dificultad, duración, edad mínima, aptitud física, cupo según modalidad).
4. Seguridad (riesgos, puntos de evacuación, contactos de emergencia; plan de contingencia **autogenerado** desde plantilla por modalidad).
5. Equipo requerido y plan de mantenimiento ([[I19 Almacenamiento documental nube fisica NAS y registro de equipos|I19]]).
6. Fotos/video (mínimo 10, geolocalizadas).
7. Costos y disponibilidad.
- **Dictado por voz**: el guía describe la ruta en un audio; el sistema transcribe y prellena campos para revisión.
- **Estados**: borrador → en revisión (checklist automático + revisión humana) → publicada → suspendida.
- **Semáforo de completitud** por ruta (rojo/amarillo/verde).

## Reglas de negocio (especificación)
```text
Ruta.estado: borrador -> en_revision -> publicada | observada -> suspendida
publicable SI completitud >= 100% de campos obligatorios(modalidad) AND revision_humana == "ok"
```

## Riesgos
[[N08 Registro de riesgos#R16 Calidad desigual de guías y rutas|R16]] calidad desigual · [[N08 Registro de riesgos#R08 Complejidad excesiva del MVP|R08]].

## Métricas de éxito
Tiempo para completar una ruta ≤ 45 min; % de borradores que llegan a publicación ≥ 60 %.

## Próximos pasos
Diseñar el JSON de ruta ([[N06 Arquitectura de plataforma|N06]]) y probar el asistente con 3 rutas de Morona Santiago.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
