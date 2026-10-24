---
id: I18
tipo: idea
titulo: "Automatización de la documentación legal por ruta («proyecto de ruta»)"
area: legal-operación
estado: analizada
prioridad: alta
riesgo_legal: alto
fase: F0
origen: [A03, A05, A11, A13]
depende_de: [I19]
relacionadas: [I01, I15, I22, I29]
confianza: alta
tags: [idea, legal-operacion, nanturia]
---
# I18 · Automatización de la documentación legal por ruta («proyecto de ruta»)

> **Origen (audios):** [[A03 Exceso de documentacion y almacenamiento|A03]] [[A05 Reducir friccion del guia al subir rutas|A05]] [[A11 Documentacion por actividad y modelo operadora vs guia|A11]] [[A13 Un proyecto por ruta 16 rutas|A13]] · **Área:** legal-operación · **Prioridad:** alta · **Riesgo legal:** alto · **Fase:** F0 · **Confianza del análisis:** alta
> **Depende de:** [[I19 Almacenamiento documental nube fisica NAS y registro de equipos|I19]]
> **Relacionadas:** [[I01 Modelo en cadena con operadoras aliadas|I01]] [[I15 Modo turista y modo guia asistente de creacion de rutas|I15]] [[I22 Biblioteca de rutas precreadas y onboarding|I22]] [[I29 Seguros y requisitos de las plataformas globales|I29]]

## Resumen fiel de lo dicho
Cada ruta exige un «proyecto» con coordenadas, mapas, plan de contingencia, plan de emergencias, términos y condiciones, seguro, fotos, etc.; hay 16 rutas pero no todas tienen proyecto. Hay que repetir lo mismo cada vez y conviene automatizarlo. Podría venderse sin eso, pero ante un accidente piden respaldos (ubicación de equipos, mantenimiento, fichas técnicas).

## Problema
Tiempo y costo de producir la documentación exigida por ruta, y riesgo de operar sin ella.

## Análisis
- **Lo que la norma exige** (Reglamento de Aventura 2020-005, Art. 10 🟢): *plan de operación y contingencia* por modalidad (calendario de inspecciones, características del destino, medidas de seguridad, condiciones de realización o suspensión, rutas alternas, condiciones físicas/edad mínima, croquis, programa, equipo, número de participantes, impacto ambiental, política de accidentes e incidentes con su registro, riesgos y procedimientos) y *plan de mantenimiento y reposición* de equipos (uso, fechas, mantenimiento, razones de descarte, comprobantes y manuales conservados, verificación visual firmada antes de cada uso). Además el **consentimiento informado** firmado (Anexo A) y comprobante de venta.
- No es sensato «vender sin eso»: un accidente sin documentación expone a sanciones y a responsabilidad civil/penal.
- Hay solo **~6 modalidades** relevantes para empezar (senderismo, exploración de cuevas, canyoning, rafting, cabalgata, cicloturismo): el trabajo es de *plantillas por modalidad* + *datos por ruta*.

## Mejora propuesta
- **Dossier de ruta** generado automáticamente (PDF versionado) a partir de datos estructurados: ficha, croquis/mapa, georreferencia (GPX/GeoJSON), plan de operación y contingencia, plan de mantenimiento, T&C, consentimiento informado, matriz de riesgos.
- **6 plantillas maestras** (una por modalidad) + 16 formularios de datos = 16 dossiers (en vez de 16 documentos desde cero).
- **Orden de ataque**: priorizar rutas por demanda y bajo riesgo (senderismo/cultural primero; cuevas y agua vía operadora aliada).
- **Checklist y semáforo** por ruta y por operador; **alertas de vigencia**.
- **Paquete de evidencia** exportable en 1 clic (para autoridad/aseguradora): dossier + registro de equipos + checklists firmados + bitácora de incidentes.

## Reglas de negocio (especificación)
```text
Dossier(ruta, modalidad) = render(plantilla[modalidad], datos_ruta) -> PDF + hash + version + fecha + firmante
ruta.publicable REQUIERE dossier.vigente AND consentimiento_informado.plantilla AND plan_mantenimiento.vigente
```

## Riesgos
[[N08 Registro de riesgos#R01 Incumplimiento normativo de agencia, intermediación y guías|R01]], [[N08 Registro de riesgos#R02 Siniestro grave sin cobertura suficiente|R02]], [[N08 Registro de riesgos#R16 Calidad desigual de guías y rutas|R16]].

## Por verificar
[[N09 Verificaciones pendientes#V11 Límites de grupo por modalidad y por área protegida para las 16 rutas|V11]], [[N09 Verificaciones pendientes#V16 Contenido de la imagen de requisitos mencionada en el audio A03|V16]].

## Próximos pasos
Escoger 3 rutas piloto; llenar el formulario de datos; generar el primer dossier a mano para validar la plantilla.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
