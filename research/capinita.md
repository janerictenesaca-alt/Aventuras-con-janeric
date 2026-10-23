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


## Metodología — REA, herramientas, errores aprendidos y avance medido (2026-10-23)
*Sección acumulativa de metodología. Etiquetas: **[O]** observado · **[M]** medido · **[I]** inferido · **[NV]** no verificado.*

### 1. Herramientas y versiones registradas
| Herramienta | Versión / origen | Uso | Estado |
|---|---|---|---|
| **REA** (servidor MCP `rea`) | **`rea-agents@6.5.0`**, versión fijada en el registro del servidor (`npx -y rea-agents@6.5.0 mcp`) [M]; el skill instalado cita la misma versión | Inspección pasiva de la página, análisis estático del JavaScript, trazado de funciones | En uso; **no se instaló ni actualizó nada** |
| Proveedores REA usados | `rea-cdp-browser` v2, `rea-web-script-export` v1, `rea-analysis-view` v1 [M] | Captura de la página, exportación de scripts, vistas de la evidencia | En uso |
| Skill `reverse-engineer-anything` | Instalado localmente; carga comprobada (0 observaciones abiertas del registro) | Guía de ruta de trabajo: página → recursos → módulos | En uso |
| Skill `task-observer` | Instalado localmente | Registro de observaciones | Sin entradas nuevas |
| Chrome (para REA y clipper) | 155.0.8059.86, modo headless con perfil temporal [M] | Páginas, capturas y depuración local | En uso |
| Brave | Instalado; probado como navegador del clipper | Alternativa si Chrome falla | Probado una vez |
| Node.js | v24.20.0 [M] | Clipper | En uso |
| Claude Code | 2.1.309 (paquete npm global) [M] | Entorno | — |
| Extensión Claude in Chrome | Conectada, pero **bloquea todos los dominios** ("blocked by your site permissions") | Navegador integrado | **No utilizable**; causa fuera de nuestro alcance |
| `browser-use` | Demonio no arranca: falta la depuración remota activada en el navegador del usuario | Alternativa | No utilizable sin acción del usuario |
| WebFetch, `curl`, Python 3.13 | Del entorno | Lectura pública, cabeceras, análisis de datos | En uso |
| **Clipper propio** `research/herramientas/clipper.mjs` | Creado en este proyecto (solo lectura, bloquea peticiones no-GET y la analítica del sitio) | Fichas por página | En uso; parcheado hoy para registrar qué peticiones bloquea |

**Cambios realizados en herramientas:** ninguna instalación ni actualización externa; no se tocó configuración global. Solo se creó y ajustó el clipper dentro del repositorio autorizado. **Mejor combinación para inspeccionar una aplicación web** [I, basada en lo probado]: (1) `curl`/WebFetch para `robots.txt`, sitemap y cabeceras; (2) Chrome aparte con el clipper para fichas, capturas y móvil; (3) REA `inspect_web_page` con scripts → `export_web_scripts` → `analyze_javascript_application` (resumen) → `inspect_analysis_view`/`trace_application_feature` con semilla exacta para módulos y funciones.

### 2. Resultados del análisis con REA (página de estado vial y ficha de ruta)
- **Observado [M]:** 100 scripts exportados y analizados sin fallos de lectura; 278 441 nodos de sintaxis; **319 módulos** reconocidos (fábricas de módulos de Webpack/Rspack); 1 010 hallazgos; la cobertura del grafo es **parcial** (56 946 desconocidos semánticos), por lo que **la ausencia de un dato no significa que no exista**.
- **Peticiones en el código:** 24 relaciones de petición retenidas; el único destino absoluto identificado con certeza es el **servicio del ECU 911** (`fetch` con revalidación de 300 s). El trazado con semilla de ese texto devolvió 1 coincidencia (tipo "endpoint"), 817 nodos, 1 531 aristas y 31 caminos terminales (1 098 hechos observados, 1 502 inferidos) [M].
- **Huellas:** Next.js (alta), React (media) [O]. Sin mapas de código públicos; sin herramientas WebMCP; sin Electron.
- **Limitación importante:** REA no ejecuta el JavaScript ni confirma que una relación estática ocurra en ejecución. Las funciones por módulo siguen siendo **hipótesis**, salvo las que se confirmaron por red.
- Los scripts exportados se usaron solo para el análisis y **se borraron**; no se reutiliza ningún recurso de Capinita.

### 3. Errores encontrados, causa, solución y cómo evitarlos
| # | Error | Causa | Solución aplicada | Prevención |
|---|---|---|---|---|
| 1 | Extensión de Chrome: "blocked by your site permissions" para todos los dominios | Configuración/cuenta de la extensión (sin confirmar) o error conocido de la extensión | Chrome aparte con depuración local y clipper | Probar primero un sitio neutro para distinguir bloqueo global de bloqueo por sitio |
| 2 | `browser-use`: "DevToolsActivePort not found" | Depuración remota no activada en el navegador del usuario | No se activó (ajuste de seguridad del usuario) | Usar Chrome propio con puerto de depuración |
| 3 | Comandos largos de Bash fallaron ("unexpected EOF") | Comillas y heredocs mezclados en Git Bash | Escribir archivos con la herramienta de escritura y ejecutar scripts pequeños | Un archivo por script; evitar heredocs largos con comillas |
| 4 | Python no veía `/tmp` de Bash | Rutas distintas entre Bash y Python en Windows | Usar rutas absolutas de la carpeta temporal de la sesión | Rutas absolutas |
| 5 | Columnas mal asignadas en el primer inventario (títulos/h1 aparecían como números) | `curl -w` añadió columnas; se contó con índices equivocados | Recontar con cabecera etiquetada y repetir el análisis | Archivos TSV con cabecera y verificación de una fila antes de agregar |
| 6 | REA `analyze_web_bundle`: "expected true" | Parámetro obligatorio `include_script_sources: true` | Repetir con ese valor | Leer el esquema de la herramienta antes de llamar |
| 7 | Salidas de REA demasiado grandes (hasta 4 MB) | Capturas con fuentes y semillas amplias (`contains`) | Leer el archivo guardado con Python, solo claves y recuentos | Usar `detail: summary`, semillas exactas y vistas paginadas |
| 8 | REA listó 24 "rutas" que eran iconos | Trazados SVG detectados como rutas | Descartar; las rutas reales vienen del sitemap | No usar el campo "routes" de REA como inventario de páginas |
| 9 | Resúmenes parciales y numeración confusa de los términos de Airbnb | Documento largo con varias versiones y lectura por tramos | Releer por desplazamientos y separar versiones | Leer por tramos con un índice previo y marcar cada versión |
| 10 | Captura móvil recortada | Chrome sin ventana no baja de cierto ancho | Emular el dispositivo por protocolo de depuración | Emulación en lugar de tamaño de ventana |
| 11 | Portada y precios de Airbnb vacíos | El modo solo lectura bloquea las peticiones no-GET (registro, configuración) | Documentar la limitación; no se relajó la regla | Pedir autorización antes de permitir POST de configuración |
| 12 | `brave --version` abrió una ventana en la sesión de Brave del usuario | El ejecutable reutiliza la sesión abierta | Sin daño; se registró | No ejecutar el navegador del usuario solo para ver su versión |
| 13 | La huella del clipper mezcla escritorio y móvil | Misma clave de URL | Registrado como límite | Incluir el modo en la clave (mejora pendiente) |

### 4. Inventario explícito y avance medido (corte 2026-10-23)
**Cómo se calcula:** porcentaje = elementos con el nivel de evidencia indicado ÷ total del inventario de ese tipo. Niveles: **A** ficha con medición y, cuando aplica, captura; **B** solo inventario mínimo (estado HTTP, título, `h1`, tamaño); **E** error. **B no equivale a haber revisado el contenido.** No se declara 100 % de nada: el inventario podría no estar completo (páginas no enlazadas ni listadas, módulos de otras páginas).

| Inventario | Total | Con evidencia | Pendiente | Porcentaje y cálculo |
|---|---|---|---|---|
| **Páginas públicas conocidas** (381 del sitemap + 4 fuera del sitemap: tours, emprendedor, servicios, privacidad) | **385** | **A: 23** · B: 357 · E: 5 | contenido de 357 páginas de plantillas repetidas | A = 23/385 = **6,0 %**; B = 357/385 = **92,7 %**; E = 5/385 = **1,3 %**; A+B = **98,7 %** (de evidencia mínima, no de contenido) |
| **Plantillas de página identificadas** | 20 | 20 con ficha (A) | variantes no vistas | 20/20 de las identificadas; la lista puede estar incompleta |
| **Funciones identificadas** | 22 | 21 con evidencia de existencia (interfaz o red) · 5 con comportamiento comprobado por red (mapa y ruteo, estado vial ECU 911, precarga de páginas, sesión, analítica) | panel privado (1, sin acceso); funciones **no ejercidas** (búsquedas, filtros, formularios, favoritos, comentarios) | existencia 21/22 = **95,5 %**; comportamiento verificado 5/22 = **22,7 %**; ejercidas de extremo a extremo 0/22 = **0 %** |
| **Archivos JavaScript** (las 3 páginas con REA) | 20 | 20 analizados estáticamente · 8 con función probable asignada | 12 sin función asignada | 20/20 = 100 % analizados (de esas 3 páginas); función asignada 8/20 = **40 %** |
| **Hojas de estilo y fuentes** | 6 + 2 | 6 CSS leídas · 2 fuentes identificadas | — | 8/8 = 100 % de las cargadas en esas páginas |
| **Referencias de imagen** | 69 | 34 medidas (formato, peso, dimensiones) | 35 no medibles (27 respaldos PNG con 404 y 8 direcciones truncadas por el análisis) | 34/69 = **49,3 %** |
| **Destinos externos observados** | 9 (ECU 911, teselas y ruteo de OpenStreetMap, unpkg, Google Analytics y Tag Manager, imágenes propias, Unsplash, WhatsApp) | 9 observados | — | 9/9 de los vistos |

### 5. Cómo mejorar el método en el siguiente análisis
1. Incluir el modo (escritorio/móvil) en la huella y la clave del clipper.
2. Añadir al clipper un inventario de recursos por página (JavaScript, CSS, imágenes, hosts) para calcular los porcentajes automáticamente.
3. Extender REA a una muestra de plantillas distintas (ruta, cooperativa, lugar) para ampliar el inventario de módulos más allá de 3 páginas.
4. Si el usuario autoriza una cuenta de prueba o desbloquea la extensión: ejercer búsquedas y filtros en solo lectura y registrar su comportamiento.
5. Repetir el inventario del sitemap periódicamente para detectar cambios (estados, títulos, errores).

### 6. Aplicación a nuestra implementación (original)
Lo aprendido con REA refuerza el plan ya documentado: Next.js con componentes de servidor, carga de mapa solo donde se use, consulta de datos viales desde nuestro servidor con caché y fecha del dato, un presupuesto de JavaScript por página (hoy 1,6 MB sin comprimir en las páginas con mapa), y un inventario automático de recursos. Todo con código, nombres, textos, diseño e imágenes propios.
