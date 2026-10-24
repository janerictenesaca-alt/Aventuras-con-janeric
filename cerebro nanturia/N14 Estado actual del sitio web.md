---
id: N14
tipo: sintesis
titulo: "Estado actual del sitio web"
estado: analizada
fecha: 2026-10-24
tags: [nanturia, sitio-web, auditoria]
---
# N14 · Estado actual del sitio web

> **Fuente y confianza 🟡:** resumen final que dio Claude en PowerShell al auditar el sitio con el prompt de 6 partes ([[N13 Convenciones del cerebro|N13]] describe las convenciones). Lo conozco por una **captura de pantalla** del 2026-10-24 (06:40); **no he visto el código ni las notas S00–S12**, que están en el PC de Janeric. Cuando esas notas se unan a esta bóveda (ver `herramientas/leeme-herramientas`), esta nota debe reemplazarse por enlaces a S00–S12.

## 1. Cómo se hizo la auditoría y tres observaciones de proceso
- Se pegó el prompt en 6 partes (`prompts/partes/`); la herramienta devolvió el resumen y generó notas en `cerebro-sitio-web\` (nombres ASCII).
- **Escritura fuera de lo permitido:** el prompt limitaba la escritura a `cerebro-sitio-web\`, pero el resumen dice que además añadió **5 líneas a `curso/bitacora.md`**. Probablemente obedece a una regla propia del proyecto (bitácora); conviene revisar con `git diff curso/bitacora.md`. El resto del código quedó intacto, según el informe.
- **El cerebro de negocio no estaba en ese PC**: por eso `I01–I35` y `H01–H13` aparecen como texto y no como enlaces → se resuelve con `herramientas/cerebro.mjs` (comando `fusionar`).
- **No medido** (el prompt prohibía instalar paquetes y usar la red): cobertura de pruebas, Lighthouse, vulnerabilidades de dependencias y variables de Vercel → quedaron como «no determinado». Si se quiere, un segundo paso con permiso explícito para `npm audit` y Lighthouse.
- La **Parte C del sitio sigue en pausa hasta que Janeric escriba ADELANTE**: las mejoras que toquen diseño esperan esa orden; solo los textos se pueden corregir sin tocar el diseño.

## 2. Foto técnica (según la auditoría)
| Aspecto | Hallazgo reportado |
|---|---|
| Naturaleza | Demo estática de cliente: **sin servidor, base de datos, cuentas, pagos ni chat** |
| Stack | Next.js 16.3.5 · React 19.2.4 · Tailwind 4 · TypeScript |
| Tamaño | 2 890 líneas en `app/src` |
| Funciones visibles | Portada · búsqueda con filtros en la URL · 5 tours y 3 lugares con ficha · panel de precio **sin cobro** · panel del guía de ejemplo (guarda solo en el navegador) · SEO/WhatsApp por interruptor |
| Secretos en el código | No se encontraron |

## 3. Cobertura frente a las 35 ideas
**0 % implementadas · 29 % parciales (10) · 71 % ausentes (25).** Parciales nombradas en el resumen: captación ([[I14 Plataforma estilo Airbnb solo tours con mapa y buses|I14]], [[I28 Enlaces de pago y de ruta compartibles marketing viral|I28]], [[I31 Estrategia de confianza frente a las grandes plataformas|I31]]) y demo del guía ([[I15 Modo turista y modo guia asistente de creacion de rutas|I15]], [[I30 Marco legal de los guias ambitos y plan de habilitacion|I30]]); los otros 5 parciales están en S00. Es el resultado esperable para una demo: el sitio es un **escaparate**, todavía no un sistema transaccional.

## 4. Cumplimiento de H01–H13
2 cumplen · 2 parciales · **8 incumplen** · 1 no determinado (detalle por hallazgo en S07). Referencia: [[N03 Hallazgos criticos|N03]]. No es asesoría legal.

## 5. Los cinco riesgos graves y a qué corresponden
| # | Riesgo reportado | Se relaciona con |
|---|---|---|
| 1 | La portada promete «pago protegido con pasarela» y «contacto directo», que **no existen** (`app/src/app/page.tsx:30-37`) | [[N03 Hallazgos criticos#H06 La plataforma responde ante el cliente\|H06]], [[I31 Estrategia de confianza frente a las grandes plataformas\|I31]]; publicidad veraz (Art. 7 num. 5, 🟡) |
| 2 | El pie no muestra registro de turismo, LUAF, dirección física ni teléfono 24 h; no hay términos, privacidad ni cancelación | [[N03 Hallazgos criticos#H01 Intermediación solo vía agencia de viajes registrada\|H01]], [[N03 Hallazgos criticos#H08 Requisitos obligatorios del canal virtual\|H08]], [[N03 Hallazgos criticos#H09 Teléfono de emergencia 24 h y chat sin contacto directo\|H09]], [[N03 Hallazgos criticos#H10 Oficina física obligatoria para la agencia\|H10]]; [[N04 Decisiones abiertas#D02 Estructura habilitante agencia propia o venta bajo agencia aliada\|D02]] |
| 3 | El asistente del guía permite cupo hasta 99 y no pide modalidad ni operador | [[N03 Hallazgos criticos#H02 Aventura solo vía agencia, el guía no puede operar directo\|H02]], [[N03 Hallazgos criticos#H04 Tope de grupo de 16 y límites por modalidad\|H04]]; [[I15 Modo turista y modo guia asistente de creacion de rutas\|I15]], [[I20 Asignacion automatica de guia cupos y desbordamiento\|I20]] |
| 4 | Sin servidor ni base de datos: la reserva es un botón apagado y «enviar a revisión» no llega a nadie | [[I17 Flujo de reserva con confirmacion de disponibilidad\|I17]]; [[N08 Registro de riesgos#R08 Complejidad excesiva del MVP\|R08]] |
| 5 | Datos del guía (nombre, celular, correo) en `localStorage` sin aviso ni forma de borrarlos; sin cabeceras de seguridad | [[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías\|V10]], [[N08 Registro de riesgos#R09 Protección de datos personales\|R09]]; [[N06 Arquitectura de plataforma\|N06]] (requisitos no funcionales) |

## 6. Acciones propuestas por la auditoría y mi lectura
| # | Acción (esfuerzo S/M/L) | Mi lectura |
|---|---|---|
| 1 | Corregir los textos de la portada (S) | **Hacer primero.** Si el sitio ya está publicado, hoy mismo. Además «contacto directo» **contradice el modelo** (chat enmascarado, [[I16 Bot intermediario cliente guia y prevencion de fuga de datos\|I16]]), no solo es falso. |
| 2 | Completar el pie y crear páginas legales revisadas por abogado (M) | Depende de [[N04 Decisiones abiertas#D02 Estructura habilitante agencia propia o venta bajo agencia aliada\|D02]]: **no se pueden inventar** registro, LUAF ni dirección. Hasta decidir, rotular el sitio como informativo y no habilitar reservas. |
| 3 | Montar PostgreSQL con acciones de servidor (M) | **Posponer a F1.** Para el piloto concierge basta que cada solicitud llegue a Janeric (WhatsApp/correo) y quede en una hoja ([[I32 MVP concierge sitio basico tours cargados prueba y error\|I32]]). |
| 4 | Reemplazar el botón apagado por una solicitud de reserva que guarde en servidor y avise (M) | Sí, en versión mínima sin base de datos propia; publicar **junto con** el pie legal real. |
| 5 | Pago con retención y dividido + modalidad, tope de cupo y pólizas (L) | Separar: (a) modalidad + tope + operador en el asistente (S/M, ya, [[N03 Hallazgos criticos#H02 Aventura solo vía agencia, el guía no puede operar directo\|H02]]/[[N03 Hallazgos criticos#H04 Tope de grupo de 16 y límites por modalidad\|H04]]); (b) pasarela con retención = F1 tras [[N04 Decisiones abiertas#D05 Proveedor de pagos y custodia de fondos\|D05]] y [[N09 Verificaciones pendientes#V08 Proveedor de pagos split retención payouts y tarjetas extranjeras\|V08]] ([[I07 Pagos retencion de fondos split y fondo de respaldo\|I07]]); (c) pólizas = [[I29 Seguros y requisitos de las plataformas globales\|I29]]. |

## 7. Orden recomendado
1. Decidir [[N04 Decisiones abiertas#D01 Nombre comercial|D01]] y [[N04 Decisiones abiertas#D02 Estructura habilitante agencia propia o venta bajo agencia aliada|D02]] (nombre y vehículo legal). Es el verdadero cuello de botella: no es de código.
2. Corregir textos de portada ([[N03 Hallazgos criticos#H06 La plataforma responde ante el cliente|H06]], [[N03 Hallazgos criticos#H08 Requisitos obligatorios del canal virtual|H08]]).
3. Asistente del guía: modalidad, tope de cupo y operador, leyendo los parámetros de la sección 8 (config, no constantes) → [[N03 Hallazgos criticos#H02 Aventura solo vía agencia, el guía no puede operar directo|H02]], [[N03 Hallazgos criticos#H04 Tope de grupo de 16 y límites por modalidad|H04]], [[N03 Hallazgos criticos#H13 Autoridad en transición y vigencia de textos|H13]].
4. Aviso de privacidad y botón «borrar mis datos»; cabeceras de seguridad ([[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]]).
5. Pie legal con datos reales + páginas de términos, privacidad y cancelación (validadas por abogado, [[N09 Verificaciones pendientes#V07 Derecho de retracto y reserva no reembolsable|V07]]).
6. Solicitud de reserva → WhatsApp/correo/hoja; solo tras el paso 5.
7. F1: base de datos, pasarela con retención, payouts, pólizas ([[N07 Hoja de ruta por fases|N07]]).

## 8. Parámetros legales como configuración (para [[N03 Hallazgos criticos#H04 Tope de grupo de 16 y límites por modalidad|H04]] y [[N03 Hallazgos criticos#H13 Autoridad en transición y vigencia de textos|H13]])
Valores tomados de los textos oficiales leídos (🟢); confirmar límites por sitio y área protegida en [[N09 Verificaciones pendientes#V11 Límites de grupo por modalidad y por área protegida para las 16 rutas|V11]] y la operación directa del guía local en [[N09 Verificaciones pendientes#V04 Escalera de licencias y ámbito de guías|V04]].
```json
{
  "_fuente": "Reglamento de Guianza 2025 (Disp. Gen. 2.a y 4.a) y Reglamento de Operacion Turistica de Aventura 2020 (anexos)",
  "_verificado_el": "2026-10-24",
  "tope_general_por_guia": 16,
  "modalidades": {
    "senderismo":            { "max_por_guia": 8, "operacion_directa_guia": "si" },
    "cabalgata":             { "max_por_guia": 8, "edad_minima": 6, "operacion_directa_guia": "por_verificar" },
    "exploracion_de_cuevas": { "max_por_guia": null, "pendiente": "leer anexo 5", "operacion_directa_guia": "por_verificar" },
    "cicloturismo_con_vehiculo_de_apoyo": { "max_por_guia": 16, "operacion_directa_guia": "por_verificar" },
    "canyoning":             { "max_por_guia": 4, "separacion_entre_grupos_min": 15, "operacion_directa_guia": "no" },
    "escalada_multilargo":   { "max_por_guia": 2, "operacion_directa_guia": "no" },
    "escalada_deportiva":    { "max_por_guia": 4, "operacion_directa_guia": "no" },
    "montanismo":            { "max_por_guia": 2, "max_media_montana": 6, "edad_minima": 12, "operacion_directa_guia": "no" },
    "rafting":               { "max_por_balsa_mas_guia": { "12.5_pies": 5, "13_pies": 6, "14_pies": 7, "16_pies": 9 }, "rio_clase_referencia": "III", "embarcaciones_minimas": 2, "operacion_directa_guia": "no" }
  }
}
```

## 9. Las preguntas abiertas de la auditoría y dónde se responden
| Pregunta | Dónde |
|---|---|
| ¿Método de cobro, % de anticipo y comisión, pasarela? | [[N04 Decisiones abiertas#D05 Proveedor de pagos y custodia de fondos\|D05]], [[N04 Decisiones abiertas#D07 Comisión por canal\|D07]], [[N09 Verificaciones pendientes#V08 Proveedor de pagos split retención payouts y tarjetas extranjeras\|V08]], [[N05 Modelo financiero y precios\|N05]] |
| ¿Qué entidad vende y factura? (razón social, registro, LUAF, dirección, correo, teléfono 24 h) | [[N04 Decisiones abiertas#D02 Estructura habilitante agencia propia o venta bajo agencia aliada\|D02]], [[N09 Verificaciones pendientes#V02 Requisitos exactos para ser agencia y costos\|V02]], [[N09 Verificaciones pendientes#V03 Si un portal que vende tours sin operarlos califica como agencia de viajes\|V03]] |
| ¿Qué abogado y contador? ¿Dónde se guardan las reservas de forma segura? | [[N09 Verificaciones pendientes\|N09]] (V01–V09), [[N04 Decisiones abiertas#D12 Almacenamiento documental\|D12]], [[I19 Almacenamiento documental nube fisica NAS y registro de equipos\|I19]], [[N06 Arquitectura de plataforma\|N06]] |
| ¿Guías en nómina o independientes? | [[N04 Decisiones abiertas#D13 Relación con los guías independientes o en nómina\|D13]], [[N09 Verificaciones pendientes#V17 Relación contractual con los guías independiente o en dependencia\|V17]] |
| ¿Cuáles son las 3 rutas y zonas del piloto? | [[N04 Decisiones abiertas#D09 Modalidades y cantones del piloto\|D09]], [[I22 Biblioteca de rutas precreadas y onboarding\|I22]] |
| ¿Qué números de WhatsApp de empresa? | [[N09 Verificaciones pendientes#V13 Condiciones de WhatsApp Business API\|V13]], [[I16 Bot intermediario cliente guia y prevencion de fuga de datos\|I16]], [[N03 Hallazgos criticos#H09 Teléfono de emergencia 24 h y chat sin contacto directo\|H09]] |

## 10. Siguientes pasos
1. Unir las notas S00–S12 y el cerebro del proyecto con esta bóveda: `herramientas/cerebro.mjs fusionar` (instrucciones en `herramientas/leeme-herramientas`).
2. Revisar la escritura en `curso/bitacora.md`.
3. Decidir [[N04 Decisiones abiertas#D01 Nombre comercial|D01]] y [[N04 Decisiones abiertas#D02 Estructura habilitante agencia propia o venta bajo agencia aliada|D02]]; responder las preguntas de la sección 9.
