---
id: I19
tipo: idea
titulo: "Almacenamiento documental («nube física»/NAS) y registro de equipos con QR"
area: operación
estado: analizada
prioridad: media
riesgo_legal: bajo
fase: F0
origen: [A03, A07]
depende_de: []
relacionadas: [I18, I33]
confianza: media
tags: [idea, operacion, nanturia]
---
# I19 · Almacenamiento documental («nube física»/NAS) y registro de equipos con QR

> **Origen (audios):** [[A03 Exceso de documentacion y almacenamiento|A03]] [[A07 Nube fisica|A07]] · **Área:** operación · **Prioridad:** media · **Riesgo legal:** bajo · **Fase:** F0 · **Confianza del análisis:** media
> **Relacionadas:** [[I18 Automatizacion documental legal por ruta|I18]] [[I33 Equipos y seguridad arnes en El Churo y alquiler de equipos|I33]]

## Resumen fiel de lo dicho
Comprar una «nube física» conectada a la red. Y tener un lugar con todos los documentos y fotografías listos por si, ante un accidente, la policía pide respaldo del mantenimiento, fichas técnicas y codificación de los equipos.

## Problema
Tener evidencia ordenada, disponible y a salvo.

## Análisis
- «Nube física» ≈ **NAS** (almacenamiento en red). Un NAS por sí solo **no** protege de robo, incendio o falla simultánea: hace falta la regla **3-2-1** (3 copias, 2 medios distintos, 1 fuera de sitio).
- La norma exige conservar comprobantes y manuales de equipos y registrar su uso y mantenimiento (Reglamento de Aventura, Art. 10 lit. b 🟢).
- Datos personales de clientes (consentimientos firmados) → LOPDP ([[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]]).

## Mejora propuesta
- **Fase 0**: usar Drive/Dropbox con estructura estándar; **fase 1+**: NAS de 2 bahías (RAID 1) con respaldo cifrado a la nube.
- **Estructura**: `/rutas/{id}/dossier`, `/equipos/{codigo}/hoja-de-vida`, `/incidentes/{fecha}`, `/legal/{operador}`.
- **Hoja de vida del equipo con código QR**: fabricante, ficha técnica, fecha de compra, usos, mantenimientos, estado, baja. Al escanear antes de cada salida se completa el **checklist de revisión visual** (firma digital con fecha/hora/ubicación).
- **Retención**: definir con abogado (propuesta ≥ 5 años) y control de acceso por roles.
- Hash/sello de tiempo de documentos críticos.

## Reglas de negocio (especificación)
```text
Equipo(codigo, tipo, fabricante, ficha_tecnica, compra, usos[], mantenimientos[], estado, baja?)
salida.inicio REQUIERE checklist_equipos.firmado(guia, fecha, hora)
```

## Riesgos
[[N08 Registro de riesgos#R02 Siniestro grave sin cobertura suficiente|R02]], [[N08 Registro de riesgos#R09 Protección de datos personales|R09]].

## Por verificar
[[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]], plazo de retención.

## Próximos pasos
Crear la estructura de carpetas hoy; codificar y etiquetar el equipo actual (arneses, cascos, cuerdas).

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
