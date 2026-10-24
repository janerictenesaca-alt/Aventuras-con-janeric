---
id: N07
tipo: sintesis
titulo: "Hoja de ruta por fases"
estado: analizada
fecha: 2026-10-24
tags: [nanturia, roadmap]
---
# N07 · Hoja de ruta por fases

> Las duraciones son estimaciones iniciales y dependen de [[N04 Decisiones abiertas#D02 Estructura habilitante agencia propia o venta bajo agencia aliada|D02]] (habilitación legal) y de la disponibilidad de Janeric.

## F0 · Fundaciones y piloto concierge (semanas 0-4 de preparación + 8-12 de piloto)
**Objetivo:** vender de forma legal y manual 3 rutas y aprender.
- Resolver vehículo legal ([[N04 Decisiones abiertas#D02 Estructura habilitante agencia propia o venta bajo agencia aliada|D02]]); cotizar póliza ([[I29 Seguros y requisitos de las plataformas globales|I29]]); abogado y contador ([[N09 Verificaciones pendientes|N09]]).
- Elegir 3 rutas ([[N04 Decisiones abiertas#D09 Modalidades y cantones del piloto|D09]]); dossiers por plantilla ([[I18 Automatizacion documental legal por ruta|I18]]); registro y checklist de equipos ([[I19 Almacenamiento documental nube fisica NAS y registro de equipos|I19]], [[I33 Equipos y seguridad arnes en El Churo y alquiler de equipos|I33]]).
- Sitio simple con requisitos de canal virtual ([[N03 Hallazgos criticos#H08 Requisitos obligatorios del canal virtual|H08]]); link de pago; confirmación por WhatsApp ([[I28 Enlaces de pago y de ruta compartibles marketing viral|I28]], [[I32 MVP concierge sitio basico tours cargados prueba y error|I32]]). Punto de partida real: demo estática sin servidor ni base de datos, ver [[N14 Estado actual del sitio web|N14]].
- QR en 5 hoteles solo para medición ([[I24 QR en hoteles atribucion de origen y comision|I24]]).
- Alianza ancla piloto ([[I05 Alianzas ancla Cueva de los Tayos Mateo y empresa de Hernan|I05]]).
- **Puerta F0→F1:** ≥ 30 reservas, ≥ 80 % de salidas sin incidentes, política de cancelación validada.

## F1 · MVP transaccional (meses 2-3)
**Objetivo:** automatizar el cuello de botella del piloto.
- Catálogo, fichas, mapa, ES/EN ([[I14 Plataforma estilo Airbnb solo tours con mapa y buses|I14]]); salidas compartidas y escalera de precios ([[I09 Precio decreciente por tamano de grupo escalera de precios|I09]], [[I17 Flujo de reserva con confirmacion de disponibilidad|I17]]).
- Pagos con retención y payouts ([[I07 Pagos retencion de fondos split y fondo de respaldo|I07]]); reglas de reserva y reembolso ([[I08 Reserva no reembolsable|I08]], [[I12 Cancelaciones y no-shows del cliente|I12]]).
- Panel de guía v1 y asistente de ruta ([[I15 Modo turista y modo guia asistente de creacion de rutas|I15]]); check-in y strikes ([[I13 Incumplimiento del guia no activa el tour o no se presenta|I13]]).
- **Puerta F1→F2:** conversión estable, reembolsos por falla < 2 %, margen de contribución por salida ≥ 20 %.

## F2 · Marketplace de proveedores (meses 4-6)
**Objetivo:** abrir la oferta a más guías y operadoras.
- Reclutamiento desde el catastro ([[I06 Reclutamiento de guias desde el Catastro Turistico|I06]]); habilitación y academia ([[I22 Biblioteca de rutas precreadas y onboarding|I22]], [[I30 Marco legal de los guias ambitos y plan de habilitacion|I30]]).
- Operadoras revendedoras y link con atribución ([[I03 Red de operadoras revendedoras y consolidacion de grupos|I03]], [[I28 Enlaces de pago y de ruta compartibles marketing viral|I28]]); salidas con pooling de transporte ([[I27 Co-venta entre guias de una ciudad para llenar el bus pooling|I27]], [[I11 Paridad de precios y transporte desde distintas ciudades|I11]]).
- Chat enmascarado ([[I16 Bot intermediario cliente guia y prevencion de fuga de datos|I16]]); reseñas y ranking ([[I23 Ranking y visibilidad de guias operadoras y colaboradores|I23]]); complementos ([[I25 Complementos de hospedaje y transporte aceptar u omitir|I25]]); asignación en cascada ([[I20 Asignacion automatica de guia cupos y desbordamiento|I20]]); rutas sin dueño ([[I21 Rutas sin dueno ficha unica y multiples proveedores|I21]]).
- **Puerta F2→F3:** ≥ 3 cantones con oferta activa, ≥ 50 % de salidas llenas.

## F3 · Escala y diferenciación (meses 7-12)
- Más cantones y clústeres ([[I34 Expansion nacional primero internacional despues|I34]]); agente de ventas ([[I35 Agente de ventas con IA|I35]]); canales globales ([[I31 Estrategia de confianza frente a las grandes plataformas|I31]]).
- Contenido digital y suscripción ([[I26 Rutas digitales 3D datos de ruta de pago y explicaciones de pago|I26]]); tours internacionales emisivos ([[I04 Tours internacionales para ecuatorianos via operadoras aliadas|I04]]).

## F4 · Auditoría de eficiencia del código (al cerrar cada fase y antes de lanzar)
**Objetivo:** que el sitio haga lo mismo con menos peso, menos costo y más velocidad, **sin cambiar su comportamiento**. Es una revisión recurrente, no un hito único.

**Reglas**
- Medir antes y después, en las mismas páginas y con las mismas condiciones. Si una mejora no mejora una medida, se descarta.
- Primero fijar el comportamiento con pruebas (mismos datos, mismo resultado); después optimizar.
- Cambios pequeños y reversibles, cada uno con tu aprobación (ADELANTE). Menos código no siempre es mejor: se elimina lo muerto o duplicado, no se compacta lo que está claro.

**Qué se revisa**
1. **Peso:** JavaScript por página, imágenes (formato, tamaño, carga diferida), fuentes, dependencias sin uso, código muerto, scripts de terceros.
2. **Velocidad:** en celular con conexión lenta, LCP < 2,5 s, INP < 200 ms y CLS < 0,1; páginas estáticas o en caché cuando no cambian; menos código en el navegador y más en el servidor.
3. **Costo:** transferencia de datos, ejecuciones de servidor, optimización de imágenes y base de datos, frente al plan de hosting ([[N09 Verificaciones pendientes#V18 Costos y condiciones del hosting del sitio|V18]], [[N08 Registro de riesgos#R17 Costos de infraestructura que crecen con el uso|R17]]).
4. **Organización:** duplicación, módulos demasiado grandes, nombres, y configuración en un solo lugar (límites legales, precios, textos).
5. **Seguridad y privacidad:** cabeceras, datos personales guardados, dependencias con vulnerabilidades conocidas.

**Entregable:** informe antes y después, con las cinco mejoras de mayor impacto, su esfuerzo y su riesgo. Para pedirlo: «ejecuta la auditoría de eficiencia de N07 F4».

## Indicadores por fase
| Indicador | F0 | F1 | F2 |
|---|---|---|---|
| Reservas/mes | ≥ 10 | ≥ 40 | ≥ 150 |
| Salidas ejecutadas sin incidentes | ≥ 80 % | ≥ 90 % | ≥ 95 % |
| Reembolsos por falla del proveedor | n/a | < 2 % | < 1 % |
| NPS | ≥ 50 | ≥ 55 | ≥ 60 |
