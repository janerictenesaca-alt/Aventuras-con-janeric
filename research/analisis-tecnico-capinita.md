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
