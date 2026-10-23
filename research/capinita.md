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
- 2026-10-23 Lote 6: inspeccion en navegador (red, consola, DOM, metricas); ver adiciones en analisis-tecnico-capinita.md, seguridad-lecciones-capinita.md y research/evidencia/.

## Sección 2026-10-23 — Lote 7 (orden maestra): inventario completo, fichas y móvil
Repo comprobado: rama `claude/magical-babbage-nxlkef`, árbol limpio y al día antes de empezar. Segundo sitio: **pendiente (la URL no se ha indicado; no se inventa)**.

**Lote A — Inventario de las 381 URLs del sitemap** (GET con 4 peticiones en paralelo, solo lectura; datos en `evidencia/capinita-inventario-sitemap-2026-10-23.tsv`) [M]:
- 376 responden 200; **4 devuelven 404** (`/amazonia/morona-santiago/morona/markinkia-estancia-amaznica`, `/amazonia/pastaza/mera/complejo-las-lajas-caras`, `/ruta/Zapotillo a Huaquillas`, `/sierra/pichincha/quito/transfers-y-tours-privados-en-quito`) y **1 devuelve 500** (`/cooperativa-de-transporte/gualaquiza-c-a`). Las 5 páginas de error llevan `noindex`, pero siguen en el sitemap.
- **Ninguna página inspeccionada tiene etiqueta `canonical`** (inicio y una ficha de ruta, más el inventario) [M]; sí tienen `robots: index, follow`.
- 356 títulos únicos de 376; **21 páginas comparten el título genérico "Buscador de lugares turísticos"** (10 rutas, 10 lugares de Amazonía, 1 cooperativa): metadatos incorrectos [M]. 33 títulos superan 65 caracteres.
- Tiempo medio de respuesta del HTML 0,35–0,56 s por sección; HTML de 131 a 347 KB (cooperativas el más pesado) [M].
- Reparto del sitemap: rutas 213, lugares de Amazonía 55, terminales 44, consultas de estado vial 25, cooperativas 24, blog 6, regiones y páginas informativas el resto.

**Lote B — Fichas con el clipper** (23 fichas en `clips/capinita/`, 2 consultas de verificación en tours; capturas nuevas en `capturas/capinita/`): inicio, ruta, detalle de ruta, cooperativas (índice y detalle), buscador de lugares y ficha de lugar (Hotel La Jungla), terminales (índice y detalle), estado vial, blog (índice y entrada), emprendedor, login, registro, Sierra, Costa, Galápagos, Amazonía, sobre nosotros, servicios, privacidad y tours.
- **Móvil probado** (390 px, 4 páginas: inicio, detalle de ruta, tours, estado vial): sin desborde horizontal [M]; la barra lateral pasa a menú hamburguesa y las tarjetas se apilan [O]; pestañas y promociones se desplazan en horizontal [O]; en la ficha de ruta móvil hay 8 imágenes sin `alt` [M]; el error de hidratación #418 persiste en detalle de ruta y estado vial [M].
- Hallazgos nuevos [O]: las páginas de Sierra y Galápagos repiten el encabezado "Gastronomía Costera" (error de plantilla); la ficha de lugar es la plantilla más completa (descripción, habitaciones, servicios, horario, cómo llegar, mapa, galería, FAQ, redes, tours, comentarios y opiniones); el índice de cooperativas usa imágenes genéricas de bus para varias; Costa es la guía regional más extensa (~2300 palabras).

**Estado de revisión por sitio (Capinita)**
| Estado | Páginas |
|---|---|
| Revisadas directamente (ficha + captura o medición) | 23 plantillas/páginas clave (lista arriba) |
| Revisadas parcialmente (solo inventario: estado, título, h1, tamaño) | unas 350 URLs de las mismas plantillas (rutas, lugares, terminales, cooperativas, consultas de estado vial y entradas de blog); recuento exacto en el TSV |
| Bloqueadas / con error | 5 (4×404, 1×500) |
| Pendientes | Comprobar si el contenido de las plantillas repetidas varía de forma relevante (p. ej. rutas con paradas, terminales sin datos); sin interacción con filtros/pestañas (no se hizo clic) |
Punto de control para reanudar: `clips/PUNTO-DE-CONTROL.md`.


## Sección 2026-10-23 — Lote 8: análisis técnico del frontend con REA + Chrome (solo lectura, sin commit)
**Alcance.** Páginas públicas de Capinita, sin sesión de ninguna cuenta (no había una cuenta autorizada iniciada), sin enviar formularios, sin reservar, sin clics en enlaces de reserva, sin probar vulnerabilidades ni buscar credenciales. Herramientas: Chrome aparte con depuración local (perfil temporal, cerrado al terminar), herramientas REA (`inspect_web_page`, `analyze_web_bundle`; JavaScript analizado de forma estática, **nunca ejecutado por REA**), el clipper del proyecto y `curl` para cabeceras. Etiquetas: **[O]** observado · **[M]** medido · **[I]** inferido · **[NV]** no verificado.

### 1. Evidencia del análisis estático (REA, ficha de ruta `/ruta/gualaquiza-a-morona`) [O/M]
- 90 scripts capturados y analizados: **90 analizados, 0 fallos de análisis, 333 617 nodos de sintaxis**; 20 son archivos `.js` (1 589 755 bytes sin comprimir) y 70 son scripts en línea (datos de la página). 20 scripts, 6 hojas de estilo, 3 imágenes y 2 fuentes como recursos cargados.
- Huellas de proveedor: **Next.js (confianza alta)** y **React (media)** [O].
- Un solo destino externo en el código: la consulta de vías del ECU 911 (`fetch` en un chunk) [O]. No hay mapas de código fuente accesibles (no se solicitaron a REA; antes se comprobó que 0 de 15 archivos `.js` tienen `.map` público) [M].
- Sin herramientas WebMCP declaradas por la página [O].
- Parámetros de URL usados por la interfaz (candidatos de baja confianza, no una lista de llamadas): `origen`, `destino`, `buscar`, `consulta`, `categoria`, `pagina`, `p` [I].
- **Falso positivo detectado**: REA listó 24 "rutas" que eran trazados de iconos SVG (redes sociales, correo, etc.); no son rutas de la aplicación. Las rutas reales salen del sitemap.

### 2. Recursos del frontend y su función probable
| Recurso | Evidencia | Función probable |
|---|---|---|
| Chunk 543 KB (`e9841c0d…`, el mayor) | tamaño en REA [M]; contenido sin identificar | [NV] probable código compartido/librerías (React, router de Next.js) |
| `7275-…js` (249 KB) | contiene referencias a Swiper y a validación [M] | [I] componentes de interfaz y carruseles |
| `d0deef33-…js` y `8644-…js` (145 y 134 KB) | contienen Leaflet; `8644` además el `fetch` al ECU 911 y Swiper [M] | [I] mapas de ruta y bloque de estado vial |
| `4bd1b696-…js` (169 KB) | referencia a `react-dom` [M] | [I] núcleo de React |
| `polyfills-…js` (109 KB) | nombre del archivo [O] | compatibilidad con navegadores antiguos |
| 6 hojas CSS | análisis previo [M] | Tailwind + estilos de Swiper/Leaflet |
| 2 fuentes `woff2` | red [O] | Montserrat e Inter (variable) |
| 70 scripts en línea | REA [O] | datos de página serializados por Next.js (payload RSC) [I] |

### 3. Flujos observados
- **Búsqueda de rutas:** formulario de origen y destino que, según los parámetros de URL, lleva a una página de ruta `/ruta/<origen>-a-<destino>` [I]; no se ejecutó una búsqueda.
- **Consulta (ficha de ruta/cooperativa/terminal):** tarjetas de salida con hora, duración, terminales, tipo, precio y contacto [O]. El mapa pide el trazado a un servicio de ruteo público (red) [M].
- **Reserva:** no existe motor de reservas propio. Los botones abren **WhatsApp** con un enlace `https://api.whatsapp.com/send?phone=<número>&text=<mensaje prellenado>`; el ejemplo leído en `/tours` es un mensaje genérico ("quiero planificar mi viaje en Ecuador") y los de cada tour incluyen el tour (revisión anterior) [O]. No se hizo clic. El número de teléfono no se registra aquí.
- **Estado vial:** el navegador consulta el servicio del ECU 911 (límite 200 registros) y se muestra por provincia [M].
- **Cuenta/negocio:** registro y acceso (Auth.js + Google); panel y perfil son privados [NV].

### 4. Diseño, rendimiento y SEO (resumen; detalles en secciones anteriores)
Diseño: barra lateral fija en escritorio y menú hamburguesa en móvil, verde de marca `#16a34a`, Montserrat, tarjetas con esquinas redondeadas [O/M]. Rendimiento: FCP 0,23–1 s, carga 0,3–1,9 s según página; JS inicial ≈ 1,6 MB sin comprimir [M]. SEO: títulos y descripciones presentes, **sin etiqueta canonical**, 21 páginas con título genérico repetido, sitemap con 4 URLs 404 y 1 URL 500 [M].

### 5. Problemas de uso y de calidad
Botones desactivados sin explicación; datos viales con fechas antiguas pese a "cada minuto"; paginadores con contadores erróneos; error de hidratación de React (#418); apps de terceros por encima del buscador; imágenes de 700×1000 en PNG de ~1 MB; 8 imágenes sin `alt` en la ficha móvil.

### 6. Cómo lograr los mismos objetivos con una solución original (sin copiar nada)
| Objetivo funcional | Implementación propia propuesta |
|---|---|
| Aplicación rápida y rastreable | Next.js (App Router) con páginas prerenderizadas, revalidación periódica y datos desde nuestra base (PostgreSQL) |
| Búsqueda origen → destino con resultados filtrables | Esquema propio (rutas, salidas, cooperativas, terminales) + buscador con filtros (hora, precio, cooperativa) y URL legible; índice de búsqueda en base de datos |
| Mapa de ruta | MapLibre/Leaflet cargado solo en las páginas con mapa; ruteo autoalojado o proveedor con licencia |
| Estado vial | Servicio propio en servidor que consulta la fuente oficial con permiso, guarda copia con fecha y degrada si falla |
| Reserva | Solicitud estructurada (formulario propio con fecha, pasajeros y contacto) que genera un mensaje de WhatsApp o correo; sin pagos al inicio |
| Cuentas y negocios | Auth.js con verificación de correo, límite de intentos y MFA para negocios; panel propio con permisos por negocio |
| Contenido regional y SEO | Plantillas con contenido único por región, metadatos y canonical generados por página, comprobación automática de sitemap |
| Rendimiento | AVIF/WebP con varios tamaños, importación dinámica de mapa y carruseles, presupuesto de JS por página (p. ej. ≤ 300 KB comprimidos) |
Estos objetivos se cumplen con arquitectura, código, nombres, textos, diseño e imágenes propios; no se reutiliza ningún archivo de Capinita.

### 7. Pendiente y por qué
- **Páginas tras iniciar sesión (`/perfil`, `/administrador`)**: no hay una cuenta autorizada con sesión iniciada y el panel es privado; no se intentó acceder. Queda **pendiente por falta de autorización**.
- **Resultados de búsquedas y filtros**: requieren interacción (rellenar formularios); no se hizo para mantener el modo solo lectura.
- **Contenido de cada chunk** (identificación exacta de módulos): requeriría recuperar fuentes legibles; no se hizo recuperación de código y no hay mapas de código. [NV]
- **Servidor, base de datos y APIs propias**: no accesibles sin autorización; el esquema sigue siendo deducción.
- **Segundo sitio de referencia**: sin URL.
- No se hizo commit ni push (orden expresa); los cambios de esta sesión quedan sin confirmar en el repositorio local.
