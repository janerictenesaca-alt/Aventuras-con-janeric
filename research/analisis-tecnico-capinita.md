# Análisis técnico de Capinita y plan para lograr el mismo resultado con código propio

Fecha: 2026-10-23. Fuente: HTML, 6 hojas CSS y 15 bundles JS (1,2 MB) servidos públicamente, más cabeceras HTTP, `robots.txt` y `sitemap.xml`. Solo lectura del código que el sitio entrega a cualquier visitante; no se accedió a nada privado ni se llamó a ninguna API más allá de lo que hace la página al cargarse. **[M]** medido en el código/cabeceras · **[I]** inferido · **[H]** hipótesis no verificable desde fuera.
Regla: esto sirve para **entender cómo se logra el resultado**. Nuestro producto debe tener código, nombres, textos, imágenes y datos propios; no se copia nada de Capinita.

## 1. Arquitectura observada
| Capa | Qué se ve | Evidencia |
|---|---|---|
| Framework | Next.js con App Router y componentes de servidor; páginas prerenderizadas | `X-Nextjs-Prerender`, `/_next/static`, payload RSC en el HTML [M] |
| Alojamiento | Vercel (CDN, HTTPS, HSTS) | `Server: Vercel`, `X-Vercel-Cache: HIT` [M] |
| Estilos | Tailwind CSS; fuentes Montserrat e Inter; tema claro/oscuro | CSS con `--tw-*`, `font-family` [M] |
| Carruseles | Swiper | 142 referencias en los bundles [M] |
| Mapas | Leaflet con teselas OpenStreetMap; ruteo con el servicio público `routing.openstreetmap.de` (OSRM) | referencias a Leaflet, OSM y la URL de ruteo [M] |
| Autenticación | Auth.js / NextAuth (correo + contraseña y Google) y validación con zod | cadenas `next-auth`, `authjs.dev`, `zod` [M] |
| Imágenes | Subdominio propio `img.capinita.com` (tours, lugares, PDF de itinerarios) y Cloudinary | URLs en los bundles [M] |
| Datos viales | Función de servidor que consulta el servicio web público del ECU 911 y guarda el resultado en caché 300 s | `fetch` con `next:{revalidate:300}` [M] |
| Analítica | Google Analytics (gtag) | script en el HTML [M] |
| Base de datos y panel | No visibles; rutas `/perfil` y `/administrador` (privadas) | `robots.txt` [M]; motor de base de datos **[H]** |

Hallazgo útil: la página dice "actualizada cada minuto" pero el código cachea 5 minutos (300 s) [M]. Lo cierto es "hasta 5 minutos".

## 2. Modelo de datos deducido (nombres de campos en el payload) [M/I]
- **Ruta/salida:** `rutaId`, `origen`, `destino`, `origenUrl`, `destinoUrl`, `tipoRuta` (intercantonal, interprovincial…), `distancia`, `duracion`, `hora`, `salida_estacion`, `precio`, `esDePaso`, `disponibilidad`, `reserva`, `observacion`, `tramo`, `canton`.
- **Cooperativa:** `cooperativaId`, `nombre`, `descripcion`, `imagen`, `destacado`, sucursales, comodidades, redes.
- **Estado vial:** `ecu`/`ecuId` (vínculo con el reporte oficial), `descripcion`, `observacion`, provincia, cantón, estado, ruta alterna, `latitud`, `longitud`.
- **Lugar/Tour:** `titulo`, `imagen`, `precio`, `duracion`, `destacado`, `canton`.
Relaciones [I]: Región > Provincia > Cantón > Lugar; Terminal ↔ Cooperativa ↔ Ruta ↔ Salida; Estado vial ↔ Ruta por tramo.

## 3. Cómo se comporta [I]
- Las páginas de detalle se generan a partir de la ruta de la URL (`/ruta/origen-a-destino`, `/cooperativa-de-transporte/<slug>`), con datos desde servidor, y se sirven prerenderizadas con revalidación periódica.
- Los botones "Consultar/Comprar" arman un enlace de WhatsApp con texto precargado; no hay pasarela de pago.
- El mapa dibuja la línea de la ruta pidiendo el trazado a un servidor OSRM público y pinta paradas.
- Estado vial: lista del ECU 911 filtrable por provincia/estado (`?consulta=provincia`).

## 4. Qué haría falta para lograr el mismo resultado con código original
### Pila propuesta (original)
- **Next.js (App Router) + TypeScript + Tailwind** en Vercel o similar: misma ventaja de SEO y velocidad, pero con diseño y componentes propios.
- **PostgreSQL** (por ejemplo vía Supabase o Neon) con un ORM tipado; esquema propio (ver §2, con nombres nuestros).
- **MapLibre GL o Leaflet** con teselas de un proveedor con licencia clara (no depender del servidor demo de OSRM, que no es para producción: autoalojar OSRM/Valhalla o usar un proveedor de pago).
- **Auth.js** con Google y correo; **zod** para validar formularios.
- **Almacenamiento de imágenes propio** (Cloudinary, R2 o S3) con optimización.
- **Capa de datos viales** con caché y registro de la fecha real del dato, **respetando los términos de uso del ECU 911** (hay que verificarlos o pedir permiso antes de usar su servicio; no se asume que esté permitido).
### Módulos y orden de construcción (MoSCoW)
1. **Must:** esquema de datos; directorio de rutas/salidas con buscador por origen y destino; fichas de ruta, cooperativa y terminal; diseño móvil primero; SEO (sitemap correcto, metadatos, datos estructurados).
2. **Should:** estado vial con fuente y hora visibles; mapa de ruta; cuentas y reseñas moderadas; alta y reclamo de negocios con verificación; panel de administración propio.
3. **Could:** tours con solicitud de reserva estructurada; blog/guías por región; tema oscuro; notificaciones.
4. **Won't (por ahora):** pagos en línea y app nativa.
### Mejoras sobre lo observado (diferenciación)
Filtros en el buscador (hora, precio, tipo, cooperativa); fecha de última verificación en cada horario; páginas propias de lugar y de tour (no PDF); paginadores correctos; sitemap sin duplicados y `robots.txt` bien configurado; accesibilidad (alt, contraste, teclado); medir Core Web Vitals.

## 5. Riesgos y huecos
- No se pudo ver el backend ni la base de datos (privados): el esquema es una deducción.
- Origen y licencia de los datos de horarios y precios: Capinita parece recopilarlos de las cooperativas; los nuestros deben obtenerse con permiso o propios.
- Uso del servicio del ECU 911 y de teselas/ruteo públicos: revisar términos.
- Aún sin revisar: móvil real, Sierra/Costa/Galápagos, ~360 fichas del sitemap y el segundo sitio de referencia.

---
## Adición 2026-10-23 — Inspección en navegador (solo lectura)
Método: Chrome aparte (headless, perfil temporal, 1366×900) controlado por el protocolo de depuración; se registraron red, consola, excepciones y DOM durante la carga normal de 6 páginas públicas (`/`, `/ruta`, `/ruta/gualaquiza-a-morona`, `/estado-vial-ecuador`, `/tours`, `/buscador-de-lugares-turisticos`). No se hizo clic en nada que modificara datos, no se enviaron formularios y no se descargó ni reutilizó ningún recurso. Evidencia cruda (solo URLs y métricas): `research/evidencia/capinita-inspeccion-navegador-2026-10-23.json`. **[C]** comprobado en la inspección · **[I]** inferido.

### Qué se observó y qué función cumple
| Observado | Función | Evidencia |
|---|---|---|
| 49–67 peticiones por página: ~17–19 scripts propios, 6 hojas CSS, 2 fuentes, 8–23 imágenes, 13–19 `fetch` | Carga de la aplicación Next.js | red [C] |
| 11–13 `fetch` a `?_rsc=` de enlaces del menú y de blogs/cooperativas | **Precarga (prefetch) de páginas** de Next al ver los enlaces: navegación casi instantánea, a costa de peticiones extra | red [C] |
| 2 llamadas a `/api/auth/session` por página | Auth.js consulta si hay sesión iniciada (respuesta propia del sitio, la hace la propia página) | red [C] |
| `GET gtag/js` + `POST google-analytics.com/g/collect` (204) | Google Analytics 4 | red [C]; cookies `_ga`, `_ga_<id>` legibles por JS [C] |
| En `/estado-vial-ecuador`: `GET ecu911.gob.ec/Services/WSVias/ViasWeb.php?...&limit=200` | **El navegador del visitante consulta directamente al ECU 911** (200 registros, ordenados por provincia) | red [C] |
| En `/ruta/<x>`: `GET routing.openstreetmap.de/routed-car/route/v1/car/<lon,lat;lon,lat>` y teselas `a/b/c.tile.openstreetmap.org` + iconos de `unpkg.com/leaflet@1.7.1` | Mapa Leaflet que traza la ruta con OSRM público (coordenadas origen/destino en la URL) | red [C] |
| 9–15 imágenes de `img.capinita.com` por página; algunas respuestas **304** | Medios en subdominio propio con revalidación (el navegador pregunta y recibe "no modificado") | red [C] |
| Sin errores de consola; **1 excepción** `Minified React error #418` en `/ruta/gualaquiza-a-morona` y en `/estado-vial-ecuador` | Desajuste de hidratación (el HTML del servidor no coincide con lo que renderiza el cliente; típico de fechas/horas o contenido dependiente del navegador) | consola [C]; causa exacta [I] |
| `window.L` (Leaflet) existe en **todas** las páginas | El mapa se carga globalmente aunque solo la ruta lo use (peso innecesario) | DOM [C] |
| Sin `localStorage`; sin iframes; sin service worker registrado detectado | No guarda datos locales; sin contenido incrustado | DOM [C] |

### Métricas de carga (medición de una sola visita, no promedio) [C]
| Página | Nodos DOM | FCP | Evento load | Transferido |
|---|---|---|---|---|
| `/` | 1042 | 928 ms | 1,9 s | 2,0 MB |
| `/ruta` | 648 | 1,0 s | 1,1 s | 0,8 MB |
| `/ruta/<x>` | 1398 | 0,56 s | 0,85 s | 0,2 MB* |
| `/estado-vial-ecuador` | 1705 | 0,36 s | 0,53 s | 0,2 MB* |
| `/tours` | 736 | 0,23 s | 0,31 s | 1,9 MB |
| `/buscador-de-lugares-turisticos` | 846 | 0,40 s | 0,83 s | 0,2 MB* |
*parte servida desde la caché del navegador (304/disco), por eso transfiere menos. Resultado **bueno** de velocidad percibida; la carga de inicio y de tours supera 1,8 MB por las imágenes.

### Estructura y accesibilidad observadas [C]
- Una sola `<h1>` por página, `lang="es"`, un `<main>` y un `<nav>`, 77–158 SVG (iconos en línea). Etiquetas ARIA presentes.
- **Uso incorrecto de elementos semánticos:** en `/estado-vial-ecuador` hay 43 `<header>` y 43 `<footer>` (las tarjetas de cada tramo los usan como contenedores) y hasta 20 `<aside>`; esto confunde a lectores de pantalla.
- Un `<h1>` con saltos de línea y un guion suave oculto en "Turísticos" (texto con caracteres invisibles).

### Corrección a hallazgos anteriores
- Antes se escribió que la consulta del ECU 911 "se hace en el servidor". **La inspección demuestra que el navegador del visitante también llama a `ecu911.gob.ec`** (visible en la red de `/estado-vial-ecuador`). El código incluye además `next:{revalidate:300}`, que Next solo aplica en servidor; es posible que existan las dos vías (renderizado servidor y recarga en cliente). Lo comprobado: hay una petición directa desde el navegador [C].
- Consecuencia para nuestro diseño: **no exponer la dependencia directa** de un servicio externo en el cliente; consultarlo desde nuestro servidor con caché, validación y degradación elegante si el servicio falla.

### Lecciones técnicas para nuestro proyecto
1. Mantener el **prefetch** de Next pero limitarlo a los enlaces importantes (evitar 13 peticiones extra por página).
2. **Cargar Leaflet/MapLibre solo en las páginas con mapa** (importación dinámica).
3. Evitar errores de hidratación (#418): formatear fechas/horas igual en servidor y cliente (zona horaria fija `America/Guayaquil`).
4. Usar **ruteo propio o proveedor con licencia**; el servidor OSRM público no es para producción y envía coordenadas del usuario a un tercero.
5. Semántica HTML correcta (`<article>` para tarjetas, un solo `<header>`/`<footer>` de página).
6. Presupuesto de peso por página (ej. ≤ 1 MB inicial) con imágenes optimizadas.
7. Analítica con **consentimiento previo** antes de escribir cookies `_ga`.
