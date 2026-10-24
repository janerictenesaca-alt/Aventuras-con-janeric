---
id: I26
tipo: idea
titulo: "Rutas digitales 3D, datos de ruta de pago y explicaciones de pago"
area: producto
estado: analizada
prioridad: baja
riesgo_legal: medio
fase: F3
origen: [A24]
depende_de: [I14, I15]
relacionadas: [I34, I31]
confianza: media
tags: [idea, producto, nanturia]
---
# I26 · Rutas digitales 3D, datos de ruta de pago y explicaciones de pago

> **Origen (audios):** [[A24 Rutas digitales 3D y contenido de pago|A24]] · **Área:** producto · **Prioridad:** baja · **Riesgo legal:** medio · **Fase:** F3 · **Confianza del análisis:** media
> **Depende de:** [[I14 Plataforma estilo Airbnb solo tours con mapa y buses|I14]] [[I15 Modo turista y modo guia asistente de creacion de rutas|I15]]
> **Relacionadas:** [[I34 Expansion nacional primero internacional despues|I34]] [[I31 Estrategia de confianza frente a las grandes plataformas|I31]]

## Resumen fiel de lo dicho
La plataforma tendría rutas digitales: foto/video y una vista 3D navegable (como Google Maps) de lugares como cascadas, **gratis**; pero el **cómo llegar** (sendero, mapa, direcciones) tendría costo para quien quiera ir sin guía. En sitios arqueológicos (petroglifos), las imágenes se ven gratis, pero al hacer clic en una zona aparece la explicación **de pago** (o por suscripción). Pide madurar la idea.

## Problema
Generar ingresos complementarios y marketing con contenido digital.

## Análisis
- **Marketing:** vistas 360/3D son excelentes para SEO y conversión; el valor está en que el turista «ya estuvo ahí» virtualmente.
- **Cómo llegar de pago:** los GPX gratis existen (Wikiloc, AllTrails); la disposición a pagar es baja a menos que la ruta esté verificada, actualizada y con información de seguridad. Además, vender instrucciones para ir *sin guía* a zonas de riesgo traslada riesgo y puede chocar con reglas de áreas protegidas, permisos de comunidades/propietarios y la lógica de seguridad de la propia plataforma ([[N08 Registro de riesgos#R14 Daño al patrimonio o conflicto con comunidades|R14]], [[N09 Verificaciones pendientes#V12 Permisos de acceso a sitios, comunidades y patrimonio|V12]]).
- **Patrimonio:** publicar ubicación exacta de petroglifos puede facilitar vandalismo o saqueo; coordinar con la comunidad y el ente de patrimonio ([[N09 Verificaciones pendientes#V12 Permisos de acceso a sitios, comunidades y patrimonio|V12]]).
- **Modelo de monetización:** micro-pagos y suscripción funcionan mejor con contenido recurrente y de alto valor (audioguías, mapas offline).

## Mejora propuesta
- **Fase 3.** Antes, usar tomas 360 **gratis** como activo de marketing.
- **Pase de ruta**: pago único de bajo monto (hipótesis $3-8) para ruta verificada + mapa offline + checklist de seguridad + aviso de responsabilidad; **gratis con la reserva de un tour**.
- **Audioguía/explicación**: contenido interpretativo multilingüe con hotspots (de pago o por suscripción «Explorador» mensual/anual).
- Para sitios sensibles: **precisión reducida** de coordenadas públicas y acceso solo con guía local autorizado.
- Tecnología: fotos 360 + visor web (Pannellum/Marzipano) o recorrido 3D; hotspots con texto/audio; paywall simple.
- **Validación previa**: encuesta de intención de compra y pre-venta antes de invertir en producción 3D.

## Reglas de negocio (especificación)
```text
contenido.nivel: gratis = {foto, video, 360}; pago = {gpx_verificado, mapa_offline, audioguia, explicaciones}
SI ruta.sensible == true ENTONCES coordenadas_publicas = aproximadas ; acceso = solo_con_guia
```

## Riesgos
[[N08 Registro de riesgos#R14 Daño al patrimonio o conflicto con comunidades|R14]], [[N08 Registro de riesgos#R08 Complejidad excesiva del MVP|R08]], [[N08 Registro de riesgos#R02 Siniestro grave sin cobertura suficiente|R02]].

## Por verificar
[[N09 Verificaciones pendientes#V12 Permisos de acceso a sitios, comunidades y patrimonio|V12]].

## Próximos pasos
Capturar una cascada en 360 con cámara económica y medir interés; no desarrollar paywall todavía.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
