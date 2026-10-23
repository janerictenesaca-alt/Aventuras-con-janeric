# Airbnb Ecuador — registro de investigación

Sitio: https://www.airbnb.com.ec/ · Segundo sitio de referencia (indicado por el usuario el 2026-10-23) · Tipo: plataforma de alojamientos, experiencias y servicios.
Leyenda: **[O]** observado · **[M]** medido · **[I]** inferido · **[NV]** no verificado.

## Sección 2026-10-23 — Lote 1

### Método, reglas respetadas y límites
- Herramientas: Chrome aparte (perfil temporal, solo lectura) con el clipper del proyecto (`research/herramientas/clipper.mjs`), `curl` para `robots.txt`, sitemaps y cabeceras. La extensión de Claude en Chrome sigue bloqueada para cualquier dominio.
- **Se respetó `robots.txt`** [M]: no se visitaron rutas que prohíbe (p. ej. `/s/*/*`, que son los resultados de búsqueda, `/book/`, `/rooms/*/reviews`, `/rooms/*/photos`…). Por eso **no se revisaron los resultados de búsqueda ni el flujo de reserva**.
- **Protección anti-bots:** el sitio coloca una cookie de un servicio de protección contra bots (DataDome) [M]. No se intentó evadirla ni resolver desafíos; las 7 páginas cargaron sin desafío visible.
- Solo lectura: sin sesión, sin formularios, sin reservas. Para no modificar nada ni ensuciar su analítica, el clipper **bloquea las peticiones que no son GET**; en Airbnb eso bloqueó entre 18 y 63 peticiones por página (registro de eventos `tracking/jitney/logging/messages`, `marketing_event_tracking`, `get-data-layer-variables` y `client_configs`) [M]. Efecto probable: la portada y el panel de precio se ven incompletos en las capturas [I].
- Volumen muy bajo: 7 páginas y 2 repeticiones móviles, con pausas entre peticiones.

### Mapa del sitio (`robots.txt` y sitemap) [M]
- `robots.txt`: 779 líneas, 18 bloques de agentes; el sitemap maestro lista **174 subsitemaps comprimidos**: 139 de alojamientos (`homes`), y el resto de destinos, experiencias, servicios, centro de ayuda, centro de recursos, categorías, páginas de destino personalizadas, estancias mensuales y colecciones "Airbnb-friendly"/lujo. No se descargaron los de alojamientos (son masivos); es un inventario por categoría, no por URL.
- Plantillas de URL observadas: `/` · `/<ciudad>-<país>/stays` (destino) · `/rooms/<id>` (ficha de alojamiento) · `/experiences/<id>` · `/help` y `/help/article/<id>` · `/<ciudad>/services/<tipo>`.

### Índice de páginas y estado
| Página | Estado |
|---|---|
| `/` | revisada parcialmente (buscador y menú; el contenido principal no se mostró) |
| `/quito-ecuador/stays` | revisada (escritorio + móvil) |
| `/galapagos-islands-ecuador/stays` | revisada (escritorio) |
| `/rooms/1000005827033635211` (ejemplo en Suiza del sitemap) | revisada parcialmente (escritorio + móvil; panel de precio sin cargar) |
| `/experiences/6593888` | revisada (escritorio) |
| `/help` y `/help/article/2408` | revisadas (escritorio) |
| Resultados de búsqueda (`/s/…`) | **bloqueada por robots.txt**: no se visita |
| Reserva/pago (`/book/…`) y reseñas por separado | **bloqueadas por robots.txt / fuera del alcance** |
| Login, registro, perfil de anfitrión, panel de anfitrión | no revisadas (requieren cuenta; sin autorización) |
| Servicios (`/<ciudad>/services/…`), resto de destinos, centro de recursos | pendientes |
Fichas detalladas: `research/clips/airbnb/`. Capturas: `research/capturas/airbnb/`.

### Hallazgos
**Propuesta de valor y público** [O]: alojamientos, experiencias y servicios en todo el mundo; la propia página afirma "7 millones de alquileres" y "más de 220 países" (afirmaciones no verificadas) [NV]. Público: viajeros y anfitriones ("Conviértete en anfitrión").
**Navegación y buscador** [O]: pestañas Todo / Alojamientos / Experiencias / Servicios, enlace de anfitrión, cuenta y menú. **Buscador de tres campos** (dónde, fechas, quién) en un componente en forma de píldora, con calendario desplegable.
**Página de destino** `/quito-ecuador/stays` [O]: título, tarjeta de búsqueda con calendario, **bloque de estadísticas** (total de alquileres, reseñas verificadas, aptos para familias, mascotas, piscina, zonas de trabajo, wifi, valoración media), carrusel de alojamientos mejor valorados con puntuación y reseñas, "Favorito entre huéspedes", servicios populares, otras listas y destinos cercanos. Es una página pensada para posicionamiento y conversión en un mismo diseño. Aviso de **traducción automática** del contenido.
**Ficha de alojamiento** [O]: título, galería (5 fotos + todas las fotos), resumen de capacidad, puntuación y número de reseñas, sello de favorito, anfitrión y antigüedad, aspectos destacados, descripción con "mostrar más", dormitorios, servicios (51), calendario de dos meses, desglose de valoraciones por categoría (p. ej. limpieza), ubicación, "Denuncia este anuncio" y **panel de reserva** (llegada, salida, huéspedes y botón principal). Precio y desglose no se vieron [NV].
**Experiencias** [O]: pasos de lo que se hará, punto de encuentro, información del anfitrión, aspectos destacados y requisitos (huéspedes, accesibilidad).
**Centro de ayuda** [O]: buscador, artículos destacados (cancelaciones, pagos), categorías, contacto; artículos con secciones y relacionados.
**Diseño** [M/O]: fuente propia "Airbnb Cereal VF", texto rgb(34,34,34) sobre blanco, esquinas redondeadas de 8 px, botón principal con degradado rosa/rojo, muchas fotos grandes, tarjetas con puntuación; **móvil en una sola columna** con tarjeta de búsqueda a todo el ancho.
**Seguridad y cabeceras** [M]: servidor nginx, **política de seguridad de contenido con 12 directivas**, `X-Frame-Options: SAMEORIGIN`, **HSTS con `includeSubDomains` y `preload`**, cookies de sesión y experimentos en la primera carga, servicio anti-bots. (Contraste con Capinita: sin CSP ni XFO.)
**Tecnología** [M/I]: assets e imágenes desde un CDN propio (`a0.muscache.com`, 56–182 peticiones por página), un host de analítica/telemetría, contenido de ayuda desde un CMS externo; no se detectaron los indicadores de Next.js/React usados con Capinita (resultado no concluyente: no se analizaron los paquetes JavaScript con REA) [NV].
**Rendimiento/SEO** [M]: 55 imágenes en la página de Quito, 38 con carga diferida; **ninguna con texto alternativo** (55 de 55 sin `alt`) en esa página; títulos y descripciones presentes; sin errores de consola. No se midió FCP/LCP (el modo solo lectura bloquea parte de la carga) [NV].

### Pendiente y por qué
Búsqueda y reserva (prohibidas por `robots.txt`/sin cuenta); portada completa y precios (peticiones bloqueadas por el modo solo lectura; se podría probar permitiendo solo la configuración del cliente, con tu autorización); servicios, resto de destinos y análisis de JavaScript con REA (pendientes); panel de anfitrión (sin cuenta).
