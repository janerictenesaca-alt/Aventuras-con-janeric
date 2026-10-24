---
id: I06
tipo: idea
titulo: "Reclutamiento de guías desde el Catastro Turístico"
area: crecimiento
estado: analizada
prioridad: media
riesgo_legal: medio
fase: F2
origen: [A19]
depende_de: [I30, I22]
relacionadas: [I15, I28]
confianza: media
tags: [idea, crecimiento, nanturia]
---
# I06 · Reclutamiento de guías desde el Catastro Turístico

> **Origen (audios):** [[A19 Reclutar guias desde el catastro|A19]] · **Área:** crecimiento · **Prioridad:** media · **Riesgo legal:** medio · **Fase:** F2 · **Confianza del análisis:** media
> **Depende de:** [[I30 Marco legal de los guias ambitos y plan de habilitacion|I30]] [[I22 Biblioteca de rutas precreadas y onboarding|I22]]
> **Relacionadas:** [[I15 Modo turista y modo guia asistente de creacion de rutas|I15]] [[I28 Enlaces de pago y de ruta compartibles marketing viral|I28]]

## Resumen fiel de lo dicho
Usar el catastro de guías (listado por provincia y categoría) para buscar guías automáticamente, contactarlos por WhatsApp (automático o en persona), presentarles el plan de negocio, incentivarlos a subir sus tours y así saber quién tiene la certificación exigida. Nanturia operaría como una operadora que vende tours donde exista un guía con licencia. Pide mejorar la idea.

## Problema
Cold start de la oferta + verificación de que cada guía cumple los requisitos legales.

## Análisis
- El **Catastro Turístico Nacional de Guías** existe y contiene al menos: código de registro, nombre, domicilio, clasificaciones, información de contacto (Reglamento de Guianza 2025, Art. 3 lit. d) 🟢.
- Contactar masivamente por WhatsApp con datos del catastro implica tratamiento de datos personales para marketing: finalidad, base legal, derecho de oposición (LOPDP) y políticas anti-spam de WhatsApp Business (opt-in, plantillas aprobadas) → [[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]], [[N09 Verificaciones pendientes#V13 Condiciones de WhatsApp Business API|V13]], [[N08 Registro de riesgos#R09 Protección de datos personales|R09]], [[N08 Registro de riesgos#R15 Bloqueo de canales de mensajería o pagos|R15]].
- El catastro sirve además para **verificar el registro** (requisito de contratar solo proveedores registrados).

## Mejora propuesta
- **Pipeline**: descarga/consulta del catastro → normalización → segmentación (cantón, clasificación, modalidad) → priorización por demanda esperada → contacto 1:1 de bajo volumen → onboarding.
- **Landing de guías** con verificación de código de registro y estado (activo/ratificado).
- **Incentivos «Guía fundador»**: comisión reducida 12 meses, visibilidad, dossier de ruta prellenado ([[I18 Automatizacion documental legal por ruta|I18]]).
- **Referidos entre guías** (un guía invita a otro; bono tras primera venta).
- **Alertas de vigencia**: cada clasificación dura 4 años (Art. 13) → recordatorios de renovación y bloqueo automático al vencer.

## Reglas de negocio (especificación)
```text
guia.activo = registro_turismo.estado == "activo/ratificado"
              AND fecha < registro.caducidad
              AND ruta.modalidad IN guia.clasificacion.modalidades
              AND ruta.canton IN guia.ambito (local: solo su canton)
              AND RUC.activo
```

## Riesgos
[[N08 Registro de riesgos#R09 Protección de datos personales|R09]], [[N08 Registro de riesgos#R15 Bloqueo de canales de mensajería o pagos|R15]], baja conversión, datos desactualizados.

## Métricas de éxito
Tasa de respuesta ≥ 15 %; guías activos verificados por cantón piloto ≥ 10; costo de adquisición por guía.

## Por verificar
[[N09 Verificaciones pendientes#V04 Escalera de licencias y ámbito de guías|V04]], [[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]], [[N09 Verificaciones pendientes#V13 Condiciones de WhatsApp Business API|V13]].

## Próximos pasos
Descargar el catastro del cantón piloto; probar 30 contactos manuales; medir.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
