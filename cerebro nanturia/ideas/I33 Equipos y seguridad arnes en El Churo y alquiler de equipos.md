---
id: I33
tipo: idea
titulo: "Equipos y seguridad: arnés en El Churo y alquiler de equipos"
area: operación
estado: analizada
prioridad: media
riesgo_legal: medio
fase: F0
origen: [A25]
depende_de: [I19]
relacionadas: [I10, I18]
confianza: media
tags: [idea, operacion, nanturia]
---
# I33 · Equipos y seguridad: arnés en El Churo y alquiler de equipos

> **Origen (audios):** [[A25 Precios de city tour aventura y trekking|A25]] · **Área:** operación · **Prioridad:** media · **Riesgo legal:** medio · **Fase:** F0 · **Confianza del análisis:** media
> **Depende de:** [[I19 Almacenamiento documental nube fisica NAS y registro de equipos|I19]]
> **Relacionadas:** [[I10 Estructura de precios comision y pago justo al guia|I10]] [[I18 Automatizacion documental legal por ruta|I18]]

## Resumen fiel de lo dicho
En el trekking a El Churo la bajada es tan empinada que la gente puede resbalar; por eso conviene comprar arneses de escalada y colocarlos a cada persona. Trekking a $40 todo incluido (~$20 para el guía); si el guía alquila arnés u otros equipos, el precio se ajusta para mantener el equilibrio.

## Problema
Reducir el riesgo de caída en un tramo empinado sin disparar el precio ni el riesgo legal.

## Análisis
- Si el tramo exige arnés y cuerda, la actividad pasa de «caminata» a **trabajo con técnicas de montaña**; el senderismo puede requerir equipo especializado de montaña (Reglamento de Aventura, Anexo 7 🟢), pero el guía debe estar acreditado para la modalidad y se aplican las exigencias de equipo y revisión previa firmada.
- El arnés es un **activo regulado**: ficha técnica, codificación, mantenimiento, vida útil, descarte ([[I19 Almacenamiento documental nube fisica NAS y registro de equipos|I19]]).
- Una cuerda/arnés mal usada puede *aumentar* el riesgo; la mejor solución puede ser **ingeniería de sendero** (escalones, pasamanos, anclajes fijos) y no equipo individual.
- «Ajustar el precio» según el equipo alquilado confunde al cliente.

## Mejora propuesta
- **Evaluación técnica del tramo** (por guía acreditado en la modalidad) y decisión: pasamanos/línea de vida fija, o arnés con asegurador.
- **Precio**: incluir el equipo en el precio base y **mostrar desglose**; opcional «upgrade» solo si el cliente quiere equipo propio extra.
- **Equipo codificado** con QR, checklist antes de cada uso y registro de horas.
- Actualizar el **plan de contingencia** con rescate en pendiente y punto de evacuación.
- Consentimiento informado específico del riesgo de caída.

## Reglas de negocio (especificación)
```text
ruta.requiere_arnes => modalidad_efectiva = evaluar(senderismo | escalada | canyoning) ; exigir guia.acreditado(modalidad_efectiva)
equipo.uso => registrar(codigo, fecha, guia, checklist_firmado)
```

## Riesgos
[[N08 Registro de riesgos#R02 Siniestro grave sin cobertura suficiente|R02]], [[N08 Registro de riesgos#R14 Daño al patrimonio o conflicto con comunidades|R14]], [[N08 Registro de riesgos#R16 Calidad desigual de guías y rutas|R16]].

## Por verificar
[[N09 Verificaciones pendientes#V11 Límites de grupo por modalidad y por área protegida para las 16 rutas|V11]] (modalidad efectiva del tramo y ratio de guías).

## Próximos pasos
Visita técnica con un guía acreditado en montaña; decidir y documentar.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
