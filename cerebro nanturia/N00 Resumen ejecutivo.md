---
id: N00
tipo: sintesis
titulo: "Resumen ejecutivo"
estado: analizada
fecha: 2026-10-24
tags: [nanturia, resumen, indice]
---
# N00 · Resumen ejecutivo

> Cerebro de Nanturia · síntesis de 27 audios (A01–A27) analizados, contrastados con la normativa ecuatoriana y mejorados. Fecha de elaboración: 2026-10-24. Este documento **no es asesoría legal**: los puntos 🟡 y 🔴 deben verificarse ([[N09 Verificaciones pendientes|N09]]).

## 1. Tesis en una frase
Nanturia es una **agencia de viajes digital** —un marketplace vertical de tours de aventura y cultura en Ecuador, partiendo de Morona Santiago— que **vende, cobra, verifica y respalda** servicios operados por guías y operadoras habilitadas, y gana por comisión y fee de reserva.

## 2. Los cuatro dolores que aparecen en los audios
1. **Guías sin plataforma ni cobro** confiable ([[A02 Sitio web tipo Airbnb bot intermediario y cobros|A02]], [[A10 Doble pago y fondo de respaldo|A10]], [[A17 Cancelaciones de clientes y perdida propia|A17]]).
2. **Carga documental y legal por ruta**: un «proyecto» por cada ruta, seguros, planes de contingencia, registros de equipos ([[A03 Exceso de documentacion y almacenamiento|A03]], [[A11 Documentacion por actividad y modelo operadora vs guia|A11]], [[A13 Un proyecto por ruta 16 rutas|A13]], [[A18 Seguros y plataformas globales|A18]]).
3. **Pérdidas por cancelaciones y fallas** (del cliente y del guía) ([[A09 Flujo de consulta al guia y reembolso|A09]], [[A11 Documentacion por actividad y modelo operadora vs guia|A11]], [[A17 Cancelaciones de clientes y perdida propia|A17]]).
4. **Masa crítica**: ninguna ciudad llena una salida sola; hay que consolidar demanda ([[A08 Vender via operadoras nacionales y consolidar grupos|A08]], [[A20 Precios entre operadoras y co-venta para llenar bus|A20]]).

## 3. Cómo gana dinero (líneas de ingreso)
- Comisión por reserva (≈30 % canal propio; menor en canales de guía/operadora) → [[I10 Estructura de precios comision y pago justo al guia|I10]].
- Fee de reserva no reembolsable bien rotulado → [[I08 Reserva no reembolsable|I08]].
- Complementos: hospedaje, transporte, alquiler de equipos → [[I25 Complementos de hospedaje y transporte aceptar u omitir|I25]], [[I10 Estructura de precios comision y pago justo al guia|I10]].
- Contenido digital y suscripción (fase 3) → [[I26 Rutas digitales 3D datos de ruta de pago y explicaciones de pago|I26]].
- Servicio de habilitación y academia para guías → [[I30 Marco legal de los guias ambitos y plan de habilitacion|I30]], [[I22 Biblioteca de rutas precreadas y onboarding|I22]].

## 4. Lo que más cambió al contrastar con la norma
Los seis hallazgos críticos (detalle en [[N03 Hallazgos criticos|N03]]):
1. **Vender tours es «intermediación» y solo puede hacerla una agencia de viajes registrada**, con oficina física: Nanturia no puede ser «solo un sitio web» → [[N03 Hallazgos criticos#H01 Intermediación solo vía agencia de viajes registrada|H01]], [[N03 Hallazgos criticos#H10 Oficina física obligatoria para la agencia|H10]].
2. **Los guías de aventura no pueden operar de forma directa** rafting/canyoning (salvo senderismo): deben hacerlo vía una agencia → [[N03 Hallazgos criticos#H02 Aventura solo vía agencia, el guía no puede operar directo|H02]]. Esto **respalda tu idea de trabajar con operadoras**.
3. **La plataforma responde ante el cliente**; «reclámale al guía» no es defendible → [[N03 Hallazgos criticos#H06 La plataforma responde ante el cliente|H06]].
4. **El tope de grupo es 16 (no 15)** y mucho menor en varias modalidades (canyoning 4, cabalgata 8…) → [[N03 Hallazgos criticos#H04 Tope de grupo de 16 y límites por modalidad|H04]].
5. **Comisiones a hoteles y ventas por link de guías** tocan prohibiciones (alojamiento/alimentos/transporte no pueden intermediar; los guías no pueden hacer «agenciamiento») → [[N03 Hallazgos criticos#H03 El guía no puede hacer agenciamiento turístico|H03]], [[N03 Hallazgos criticos#H12 Comisiones a hoteles y transporte y prohibición de intermediar|H12]].
6. **La reserva no reembolsable** debe reconciliarse con los derechos del usuario y el retracto → [[N03 Hallazgos criticos#H07 Reserva no reembolsable vs derechos del usuario y retracto|H07]].

## 5. Recomendación en cinco movimientos
1. **Resolver el vehículo legal** (agencia propia o venta bajo agencia aliada) antes de cobrar al público → [[N04 Decisiones abiertas#D02 Estructura habilitante agencia propia o venta bajo agencia aliada|D02]].
2. **Piloto concierge de 8-12 semanas** con 3 rutas y proceso manual detrás → [[I32 MVP concierge sitio basico tours cargados prueba y error|I32]], [[N07 Hoja de ruta por fases|N07]].
3. **Cobrar con retención y pagar al guía a T+2**; así desaparece el problema «ya retiró el dinero» → [[I07 Pagos retencion de fondos split y fondo de respaldo|I07]].
4. **Seguro**: póliza paraguas y/o exigir póliza a cada operadora → [[I29 Seguros y requisitos de las plataformas globales|I29]].
5. **Dossier de ruta por plantillas** (6 modalidades, 16 rutas) en vez de 16 proyectos desde cero → [[I18 Automatizacion documental legal por ruta|I18]].

## 6. Mapa de ideas (generado desde las 35 notas)
| ID | Idea | Área | Prioridad | Riesgo legal | Fase |
|---|---|---|---|---|---|
| [[I01 Modelo en cadena con operadoras aliadas\|I01]] | Modelo en cadena con operadoras aliadas | modelo | alta | medio | F0 |
| [[I02 Solo un medio traslado de responsabilidad al guia\|I02]] | «Solo un medio»: traslado de responsabilidad al guía | legal-modelo | alta | alto | F0 |
| [[I03 Red de operadoras revendedoras y consolidacion de grupos\|I03]] | Red de operadoras revendedoras y consolidación de grupos | modelo | alta | medio | F2 |
| [[I04 Tours internacionales para ecuatorianos via operadoras aliadas\|I04]] | Tours internacionales para ecuatorianos vía operadoras aliadas | modelo | baja | medio | F3 |
| [[I05 Alianzas ancla Cueva de los Tayos Mateo y empresa de Hernan\|I05]] | Alianzas ancla: Cueva de los Tayos (Mateo) y empresa de Hernán | modelo | alta | medio | F0 |
| [[I06 Reclutamiento de guias desde el Catastro Turistico\|I06]] | Reclutamiento de guías desde el Catastro Turístico | crecimiento | media | medio | F2 |
| [[I07 Pagos retencion de fondos split y fondo de respaldo\|I07]] | Pagos: retención de fondos, split y fondo de respaldo | pagos | alta | medio | F1 |
| [[I08 Reserva no reembolsable\|I08]] | Reserva no reembolsable | pagos | alta | alto | F1 |
| [[I09 Precio decreciente por tamano de grupo escalera de precios\|I09]] | Precio decreciente por tamaño de grupo («escalera de precios») | precios | alta | bajo | F1 |
| [[I10 Estructura de precios comision y pago justo al guia\|I10]] | Estructura de precios, comisión y pago justo al guía | precios | alta | bajo | F0 |
| [[I11 Paridad de precios y transporte desde distintas ciudades\|I11]] | Paridad de precios entre operadoras y transporte desde distintas ciudades | precios | media | medio | F2 |
| [[I12 Cancelaciones y no-shows del cliente\|I12]] | Cancelaciones y no-shows del cliente (pérdida propia por entradas prepagadas) | operación | alta | bajo | F1 |
| [[I13 Incumplimiento del guia no activa el tour o no se presenta\|I13]] | Incumplimiento del guía (no activa el tour o no se presenta) | operación | alta | medio | F1 |
| [[I14 Plataforma estilo Airbnb solo tours con mapa y buses\|I14]] | Plataforma estilo Airbnb solo para tours, con mapa y horarios de buses | producto | alta | bajo | F1 |
| [[I15 Modo turista y modo guia asistente de creacion de rutas\|I15]] | Modo turista y modo guía; asistente de creación de rutas | producto | alta | bajo | F1 |
| [[I16 Bot intermediario cliente guia y prevencion de fuga de datos\|I16]] | Bot intermediario cliente↔guía y prevención de fuga de datos | producto | media | medio | F2 |
| [[I17 Flujo de reserva con confirmacion de disponibilidad\|I17]] | Flujo de reserva con confirmación de disponibilidad | producto | alta | bajo | F1 |
| [[I18 Automatizacion documental legal por ruta\|I18]] | Automatización de la documentación legal por ruta («proyecto de ruta») | legal-operación | alta | alto | F0 |
| [[I19 Almacenamiento documental nube fisica NAS y registro de equipos\|I19]] | Almacenamiento documental («nube física»/NAS) y registro de equipos con QR | operación | media | bajo | F0 |
| [[I20 Asignacion automatica de guia cupos y desbordamiento\|I20]] | Asignación automática de guía, cupos y desbordamiento | producto | media | bajo | F2 |
| [[I21 Rutas sin dueno ficha unica y multiples proveedores\|I21]] | Rutas sin dueño: ficha única y múltiples proveedores | producto | media | medio | F2 |
| [[I22 Biblioteca de rutas precreadas y onboarding\|I22]] | Biblioteca de rutas precreadas y onboarding («departamento de creación de rutas») | crecimiento | alta | bajo | F0 |
| [[I23 Ranking y visibilidad de guias operadoras y colaboradores\|I23]] | Ranking y visibilidad de guías, operadoras y colaboradores | producto | media | bajo | F2 |
| [[I24 QR en hoteles atribucion de origen y comision\|I24]] | Códigos QR en hoteles, atribución de origen y comisión a colaboradores | crecimiento | alta | alto | F0 |
| [[I25 Complementos de hospedaje y transporte aceptar u omitir\|I25]] | Complementos de hospedaje y transporte (aceptar u omitir) | producto | media | medio | F2 |
| [[I26 Rutas digitales 3D datos de ruta de pago y explicaciones de pago\|I26]] | Rutas digitales 3D, datos de ruta de pago y explicaciones de pago | producto | baja | medio | F3 |
| [[I27 Co-venta entre guias de una ciudad para llenar el bus pooling\|I27]] | Co-venta entre guías de una ciudad para llenar el bus (pooling de transporte) | modelo | media | medio | F2 |
| [[I28 Enlaces de pago y de ruta compartibles marketing viral\|I28]] | Enlaces de pago y de ruta compartibles (marketing viral) | crecimiento | alta | medio | F1 |
| [[I29 Seguros y requisitos de las plataformas globales\|I29]] | Seguros y requisitos de las plataformas globales | legal | alta | alto | F0 |
| [[I30 Marco legal de los guias ambitos y plan de habilitacion\|I30]] | Marco legal de los guías, ámbitos y plan de habilitación | legal | alta | medio | F0 |
| [[I31 Estrategia de confianza frente a las grandes plataformas\|I31]] | Estrategia de confianza frente a Booking, Airbnb, TripAdvisor y Viator | crecimiento | alta | bajo | F0 |
| [[I32 MVP concierge sitio basico tours cargados prueba y error\|I32]] | MVP concierge: sitio básico, tours cargados, prueba y error | estrategia | alta | bajo | F0 |
| [[I33 Equipos y seguridad arnes en El Churo y alquiler de equipos\|I33]] | Equipos y seguridad: arnés en El Churo y alquiler de equipos | operación | media | medio | F0 |
| [[I34 Expansion nacional primero internacional despues\|I34]] | Expansión: nacional primero, internacional después | estrategia | media | medio | F3 |
| [[I35 Agente de ventas con IA\|I35]] | Agente de ventas con IA (bot de ventas 24/7) | producto | media | medio | F3 |

## 7. Decisiones que debes tomar primero
Las cinco más urgentes de [[N04 Decisiones abiertas|N04]]: [[N04 Decisiones abiertas#D01 Nombre comercial|D01]] nombre · [[N04 Decisiones abiertas#D02 Estructura habilitante agencia propia o venta bajo agencia aliada|D02]] estructura habilitante · [[N04 Decisiones abiertas#D03 Modelo operativo operador de registro o intermediario puro|D03]] modelo operativo · [[N04 Decisiones abiertas#D04 Política de reserva y reembolsos|D04]] política de reserva/reembolso · [[N04 Decisiones abiertas#D05 Proveedor de pagos y custodia de fondos|D05]] proveedor de pagos.

## 8. Qué está verificado y qué no
- 🟢 Leído en texto oficial: Reglamento de Guianza 2025; Reglamento de Operación Turística de Aventura 2020.
- 🟡 Texto de versión anterior o fuente secundaria: Reglamento de Operación e Intermediación (2021-011, reformado por 2021-037); seguros; pasarelas; LOPDP; políticas de plataformas globales.
- 🔴 No verificado: derecho de retracto, tributación, competencia, comisiones de mercado.
- Pendiente del autor: final del audio [[A20 Precios entre operadoras y co-venta para llenar bus|A20]]; imagen de requisitos mencionada en [[A03 Exceso de documentacion y almacenamiento|A03]]; nombre definitivo ([[N04 Decisiones abiertas#D01 Nombre comercial|D01]]).

## 9. Cómo navegar
- Entrada para colaboradores: [[N15 Mapa del proyecto y guia de colaboracion|N15]] · pendientes: [[N16 Tablero de pendientes|N16]].
- Lienzo: [[N01 Lienzo del modelo de negocio|N01]] · Marco legal: [[N02 Marco legal Ecuador|N02]] · Hallazgos: [[N03 Hallazgos criticos|N03]] · Decisiones: [[N04 Decisiones abiertas|N04]] · Precios: [[N05 Modelo financiero y precios|N05]] · Arquitectura: [[N06 Arquitectura de plataforma|N06]] · Hoja de ruta: [[N07 Hoja de ruta por fases|N07]] · Riesgos: [[N08 Registro de riesgos|N08]] · Verificaciones: [[N09 Verificaciones pendientes|N09]] · Trazabilidad: [[N10 Matriz audio a idea|N10]] · Glosario: [[N11 Glosario y correcciones de transcripcion|N11]] · Fuentes: [[N12 Fuentes|N12]] · Convenciones (para unir con el cerebro del sitio web): [[N13 Convenciones del cerebro|N13]] · Estado actual del sitio web: [[N14 Estado actual del sitio web|N14]] · **Mapa y guía de colaboración: [[N15 Mapa del proyecto y guia de colaboracion|N15]]** · **Tablero de pendientes: [[N16 Tablero de pendientes|N16]]** · **Decisiones del piloto (propuesta): [[N17 Decisiones del piloto propuesta|N17]]**.
