# Capinita — registro de investigación

Sitio: https://www.capinita.com/ · Tipo: app web de turismo y transporte de Ecuador.
Leyenda: **[O]** observación directa · **[M]** medición propia (curl) · **[I]** inferencia.

## Sección 2026-10-23 — Lote 1

### Método y limitaciones
- Chrome (extensión) **bloqueó capinita.com** por permisos del sitio → no hubo navegación visual, ni capturas, ni vista móvil, ni consola/red. **Diseño visual (colores, tipografía, espaciado, móvil) NO revisado.**
- Alternativa: lectura de páginas públicas con WebFetch (resume el contenido con un modelo pequeño; datos de segunda mano, confianza media) y `curl` para cabeceras, robots y sitemap [M].
- No se inició sesión, no se envió ningún formulario, no se compró ni reservó nada.

### Índice de páginas y estado
Sitemap [M]: 381 URLs (`research/capinita-sitemap-urls-2026-10-23.txt`): /ruta/* 214, /amazonia/* 57, /terminal-terrestre/* 44, /estado-vial-ecuador 25, /cooperativa-de-transporte/* 25, /blog 6, /sierra 3, /costa, /galapagos, login, registro, buscador, sobre-nosotros.

| Página | Estado |
|---|---|
| / | revisada parcialmente (texto; captura guardada, sin revisar) |
| /ruta | revisada (texto + visual escritorio); móvil pendiente |
| /ruta/gualaquiza-a-morona (muestra) | revisada parcialmente |
| /cooperativa-de-transporte/16-de-agosto (muestra) | revisada parcialmente |
| /terminal-terrestre/ambato (muestra) | revisada parcialmente |
| /estado-vial-ecuador | revisada (texto + visual escritorio); móvil pendiente |
| /buscador-de-lugares-turisticos | revisada parcialmente |
| /tours | revisada (texto + visual escritorio); móvil pendiente |
| /amazonia | revisada parcialmente |
| /blog | revisada parcialmente |
| /promocionar-negocio-turistico | revisada parcialmente |
| /iniciar-sesion | revisada parcialmente (solo lo visible; sin autenticar) |
| /crear-cuenta | revisada parcialmente (solo lo visible; no enviado) |
| /sobre-nosotros, /politica-de-privacidad, /servicios-profesionales | revisada parcialmente |
| /amazonia/pastaza/mera/complejo-las-lajas-caras (ficha de lugar) | **bloqueada**: HTTP 404 aunque está en el sitemap [O] |
| /sierra, /costa, /galapagos, resto de /ruta, /terminal-terrestre, /cooperativa, /amazonia, 4 entradas de blog | pendiente (≈365 URLs) |

Punto de control: lote 1 = 15 páginas revisadas parcialmente, 1 bloqueada, resto pendiente.

### Hallazgos
**Propósito/público.** "Aplicación Web de turismo y transporte" que conecta rutas, destinos y transporte en Ecuador [O]. Público: viajeros nacionales/extranjeros y emprendedores turísticos [I].

**Arquitectura de información** [O]: menú Inicio · Tours · Rutas · Cooperativas · Lugares · Blog · Vialidad · Emprendedor; botón "Agregar Negocio"; buscador de lugares; pie con redes, privacidad, equipo, contratar. URLs jerárquicas región/provincia/cantón/lugar.

**Funciones** [O]:
- Rutas: buscador origen→destino; ficha con tipo, distancia, duración, tabla de horarios (salida, llegada, cooperativa, directo/de paso, precio, contacto WhatsApp, "recomendado"), paradas, mapa, estado vial.
- Cooperativas: sello "Verificado", rutas con km/tiempo/precio, sucursales con WhatsApp/teléfono, comodidades, reseñas (0), "Reclamar perfil".
- Terminales: dirección, cómo comprar pasajes, servicios, consejos, tabla de salidas.
- Estado vial: datos ECU 911 por provincia (`?consulta=azuay`), filtro por estado (cerrada/parcial/restricción), "se actualiza cada minuto"; CTA de cuenta para notificaciones.
- Lugares: tarjetas (imagen, categoría, nombre, provincia/cantón); categorías Balneario, Cascada, Hospedaje, Mirador, Aventura, Parque.
- Tours: 9 tours (Pastaza/Morona), $35–$780, sin filtros; "Ver detalles" = PDF externo; "Reservar" = WhatsApp con mensaje prellenado; sin pago en línea.
- Regiones (Costa/Sierra/Amazonía/Galápagos): páginas editoriales largas (geografía, clima, cultura, FAQ).
- Blog: 5 entradas de 2025, un solo autor, etiquetas.
- Cuenta: registro con nombre, correo, fecha de nacimiento, celular (+593), contraseña y repetir; botón Google. El login no mostró formulario en el contenido leído (carga dinámica) [I].
- Monetización [I]: leads por WhatsApp, servicios de desarrollo web ($100–$1500), apps de terceros promocionadas.

**Flujo de conversión.** Casi todo CTA termina en WhatsApp o PDF; el embudo sale de la plataforma [O].

**Fricciones/defectos** [O]: contadores de paginación contradictorios ("1 a 2 de 5" con 12 tarjetas; "1 a 2 de 1"); enlaces "Consultar" con `#`; teléfonos con solo "5930"; "Loading..." en estado vial; tours repetidos en varios bloques; pie "Rutas"→/sobre-nosotros; errores de ortografía; ficha de lugar del sitemap da 404; Yasuní marcado como Pastaza; cifras (150 mil usuarios, 250+ rutas vs "+50") sin respaldo; tarjetas de atractivos sin enlace; política sin derechos de acceso/eliminación ni contacto.

**Stack** [M]: Next.js (App Router, prerender, `/_next/static`) en Vercel (`Server: Vercel`, `X-Vercel-Cache: HIT`), HSTS activo, Google Analytics, medios en `img.capinita.com`. Sin CSP ni X-Frame-Options en las cabeceras leídas.

**Rendimiento (solo inicio, curl desde mi red)** [M]: TTFB 0.41 s, total 0.50 s, HTML 274 KB, 11 `<img>` en el HTML inicial, 29 con `lazy`. Core Web Vitals no medidos (sin navegador).

**SEO** [M]: `<title>` y meta description presentes; Open Graph con `og:locale es_EC` y logo; sitemap con 381 URLs que incluye duplicados (/ruta dos veces) y rutas con espacios/mayúsculas; **robots.txt apunta a `https://acme.com/sitemap.xml`** (plantilla sin cambiar); bloquea /perfil y /administrador.

**Accesibilidad visible** [M]: 0 imágenes con `alt=""` vacío en el HTML inicial; el resto no evaluado.

## Sección 2026-10-23 — Lote 1b: diseño desde el CSS público (sin navegador)
Chrome sigue bloqueado; esto sale de los 6 archivos CSS que sirve la página (129 KB) analizados con curl. Es **medición del código, no observación visual**: no sé cómo se ve la jerarquía ni el espaciado reales.
- Tipografía [M]: Montserrat (la más usada, 35 reglas) e Inter (fuente variable 100–900, `font-display: swap`).
- Color [M]: verde de marca `#16a34a` / `#22c55e` (paleta verde de Tailwind), sobre blanco `#fff` y grises (`#e5e7eb`, `#f4f4f4`, `#333`); rojo `#e4405f` (probablemente Instagram). Acento por defecto del carrusel `#007aff`.
- Framework de estilos [M]: Tailwind CSS (utilidades `--tw-*`, anillos y sombras) y carrusel Swiper.
- Puntos de corte [M]: 640, 768, 1024, 1280 y 1536 px (estándar de Tailwind); diseño adaptable mediante `min-width` (móvil primero) [I].
- Estilo [I]: tarjetas con sombra suave y bordes redondeados; fondo claro. Sin tema oscuro detectado.
- Pendiente: capturas, jerarquía visual, espaciado, estados de interacción y comportamiento móvil real.

## Sección 2026-10-23 — Lote 2: revisión visual (Chrome aparte, solo lectura)
Método: la extensión sigue bloqueada, así que abrí una instancia **separada** de Chrome en modo headless con perfil temporal (sin tu sesión) y tomé capturas de páginas públicas, 1366 px de ancho. Nada se envió ni se inició sesión. Capturas en `research/capturas/capinita/`: `tours-escritorio-1366.png`, `ruta-escritorio-1366.png`, `estado-vial-escritorio-1366.png`, `inicio-escritorio-1366.png` (esta última guardada pero **no revisada aún**) y `tours-movil-390.png`.
Estado: /tours, /ruta y /estado-vial-ecuador pasan a **revisadas visualmente en escritorio**; móvil sigue **pendiente** (ver límite).

**Observado en las capturas [O]**
- Estructura: barra lateral izquierda fija (Inicio, Tours con insignia "Nuevo", Rutas, Cooperativas, Lugares, Blog, Vialidad, Emprendedor), cabecera con botón verde "Agregar Negocio", búsqueda, interruptor de tema claro/oscuro y acceso a cuenta; columna derecha con tarjeta de tour destacado ($35) y "Últimos Blogs"; tarjeta "Rutas Ecuador" fija abajo a la izquierda.
- Estilo: fondo blanco, verde de marca para botones/acentos, títulos grandes en negrita con una palabra resaltada en verde (en /tours "Ecuador" en bloques de color y "NOSOTROS" sobre verde), insignias redondeadas, tarjetas con esquinas redondeadas y sombra suave, fotos con etiqueta de provincia y precio en amarillo.
- /tours: carruseles horizontales por categoría (Ecoturismo, Aventura, Selva y Bosques…), tarjeta con foto, duración en verde, 3 viñetas, "Ver Detalles" (secundario) y "Reservar" (verde). La tercera tarjeta queda cortada en el borde → indica scroll horizontal.
- /ruta: titular "Encuentra tu Ruta Ideal en Ecuador", dos selectores (origen, destino; destino deshabilitado hasta elegir origen) y botón "Buscar"; ilustración de bus y teléfono; 3 cifras (150 Mil+ usuarios, 15 Mill+ alcance, 250+ rutas); 3 tarjetas degradadas de apps de terceros (verde, morado, azul) que compiten con el buscador; sección con capturas de tabla de cooperativas y mapa de ruta con instrucciones paso a paso.
- /estado-vial-ecuador: buscador único + filtro por estado; sello "Datos en tiempo real"; tarjetas por tramo con etiqueta de estado ("Parcialmente Habilitada" en ámbar), descripción en mayúsculas, **ruta alterna** en recuadro verde, fuente (`ECU_911_CUENCA`) y fecha del reporte; botones para compartir (Facebook, WhatsApp, Messenger, X); marca de actualización "22 de octubre del 2026, 11:57 pm".
- Contradicción [O]: se anuncia "actualizada cada minuto", pero los tramos visibles tienen fechas de reporte del 20, 17 y 6 de octubre (pueden ser avisos aún vigentes, no necesariamente datos viejos) [I].
- Ortografía: "Ruta refugion Volcán Sangay" visible en una tarjeta de tour.
- Texto en MAYÚSCULAS largo en estado vial: lectura más difícil [I].

**Límite de la captura móvil** [M]: Chrome headless no baja de cierto ancho mínimo de ventana, y en `tours-movil-390.png` el contenido aparece cortado por la derecha. Esa imagen **no es fiable** como vista móvil; no saco conclusiones de ella. Para el móvil real hace falta la extensión desbloqueada o emulación de dispositivo por CDP.

**Ideas para nuestro producto [I]**: estado vial con ruta alterna y fuente visible por tarjeta es un patrón útil; evitar publicidad de terceros encima del buscador; destino deshabilitado hasta elegir origen es correcto pero faltan filtros; no repetir los textos en mayúsculas.

## Sección 2026-10-23 — Lote 3: ventanas y código
- Informe de cada ventana: `research/informe-ventanas-capinita.md` (17 capturas de escritorio en `research/capturas/capinita/`).
- Análisis del código público y plan original: `research/analisis-tecnico-capinita.md`. Stack medido: Next.js (App Router) en Vercel, Tailwind, Swiper, Leaflet + OSM + OSRM público, Auth.js + zod, Cloudinary e `img.capinita.com`, y consulta al servicio web del ECU 911 con caché de 300 s.
- Estado de páginas: revisadas visualmente en escritorio inicio, tours, rutas, detalle de ruta, cooperativas, detalle de cooperativa, terminales (índice), lugares, estado vial, Amazonía, blog (entrada), emprendedor, login y registro. Capturadas sin revisar: Sierra, Costa, Galápagos, Sobre nosotros, Servicios, detalle de terminal. Pendiente: móvil real y ~360 fichas.
- 2026-10-23 Lote 4: ver research/analisis-imagenes-contenido-capinita.md (formatos, pesos y contenido).
- 2026-10-23 Lote 5: ver research/seguridad-lecciones-capinita.md (revision pasiva y lista de verificacion de seguridad).
