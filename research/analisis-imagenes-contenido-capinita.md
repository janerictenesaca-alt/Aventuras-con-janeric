# Imágenes y contenido de Capinita (2026-10-23)

Fuente: HTML de 7 páginas públicas (inicio, ruta, cooperativa, terminal, lugares, estado vial y tours) y peticiones de cabecera/primeros bytes a cada imagen. Solo se leyó lo que el sitio entrega a cualquier visitante. **[M]** medido · **[I]** inferido. Muestra: 69 referencias de imagen únicas, 34 medidas con éxito (12,7 MB en total).

## 1. Cómo sirve las imágenes
- **Etiqueta `<picture>` con 3 formatos de respaldo** (AVIF → WebP → PNG): 66 elementos `picture` y 198 `source` [M]. Los navegadores modernos eligen AVIF.
- **Dos orígenes:** archivos propios en la raíz del sitio (`/…webp`, `/tours/…png`) y un subdominio de medios `img.capinita.com` organizado por carpetas: `tours/`, `lugar-turistico/`, `cooperativa-de-transporte/`, `region-ecuador/`, `blogs/`. También hay un logo en Cloudinary y una foto externa de Unsplash [M].
- **No usa el optimizador de imágenes de Next.js** (no hay `/_next/image` ni `srcset` con anchos): sirve el mismo archivo a todos los tamaños de pantalla [M].
- **Carga diferida:** 113 de 145 `<img>` con `loading="lazy"`; 115 con `width`/`height` declarados (evita saltos de diseño); solo 1 con `fetchpriority` (la imagen principal) [M]. `sizes` solo en 5 imágenes [M].
- **Nombres de archivo descriptivos** con palabras clave (por ejemplo "terminal-terrestre-de-buses", "region-galapagos-insular-ecuador") y texto `alt` y `title` en todas (0 alt vacíos) [M]. Buen hábito para SEO, aunque hay errores de ortografía en `title` ("Coopertivas", "terretres") [M].
- **Caché:** `max-age=0, must-revalidate` en 32 de las medidas; solo 1 con `max-age=31536000` [M]. Las imágenes estáticas se revalidan en cada visita en vez de cachearse un año.

## 2. Formatos y pesos medidos [M]
| Formato | Imágenes | Peso total | Mediana | Máximo |
|---|---|---|---|---|
| WebP | 8 | 2,1 MB | 85 KB | 844 KB |
| PNG | 13 | 7,9 MB | 277 KB | 3,0 MB |
| AVIF | 7 | 0,8 MB | 95 KB | 206 KB |
| JPEG | 5 | 1,6 MB | 52 KB | 1,4 MB (foto externa de 5184×3456) |
| SVG | 1 | 2 KB | 2 KB | 2 KB |

Dimensiones habituales: tarjetas de lugar 700×1000; banners de tour 512×288; regiones 640×427 a 640×960; fondo del estado vial 1280×1707; un PNG de terminal de 2133×1200 pesa 3,0 MB [M].

## 3. Problemas detectados [M]
1. **PNG pesados:** 13 PNG suman 7,9 MB (63 % del total medido). Un banner de tour de 512×288 pesa ~330 KB en PNG; en AVIF/WebP pesaría una fracción.
2. **Mismo archivo para móvil y escritorio:** tarjetas de lugar de 700×1000 (1,2 MB en PNG, 0,8 MB en WebP) que se muestran a ~178–372 px de ancho.
3. **Foto externa de 1,4 MB** (5184×3456) servida desde Unsplash sin redimensionar.
4. **Respaldo PNG roto:** las referencias `.png` de `img.capinita.com` (lugares, iconos de cooperativa, banners de blog) devuelven **404**, mientras que `.avif` y `.webp` del mismo nombre existen (200). Solo se nota en navegadores muy antiguos [M].
5. **Fuentes duplicadas:** varias `<picture>` apuntan sus tres `source` al mismo `.webp` (AVIF y PNG declarados pero no usados) [M].
6. **Sin caché larga** (ver arriba).

## 4. Información que contiene el sitio [M/O]
| Tipo de contenido | Volumen (sitemap/páginas) | Campos principales |
|---|---|---|
| Rutas | 214 URLs | origen, destino, tipo (intercantonal/interprovincial), distancia, duración, salidas con hora, precio, cooperativa, directo/de paso, contacto, parada, observación |
| Cooperativas | 25 | nombre, descripción, galería, tipo de servicio, sucursales con contacto, comodidades, redes, reseñas, verificado |
| Terminales | 44 | dirección, cómo comprar, servicios, consejos, tabla de salidas |
| Lugares turísticos | 57 en Amazonía + Sierra/Costa/Galápagos | nombre, categoría, provincia, cantón, descripción, imagen, calificación |
| Tours | 9 | título, provincia, duración, precio, 3 puntos clave, PDF de itinerario |
| Estado vial | 25 consultas por provincia | tramo, estado, descripción, ruta alterna, fuente, fecha |
| Regiones | 4 | geografía, clima, cultura, gastronomía, fauna, FAQ |
| Blog | 5–6 | título, autor, fecha, categoría, tiempo de lectura |
| Legal/corporativo | 3 | privacidad, equipo, servicios profesionales |
Todos con URLs jerárquicas (`región/provincia/cantón/lugar`).

## 5. Recomendaciones para nuestro producto
- Usar **AVIF + WebP** con respaldo JPEG (no PNG para fotos), generar varios anchos con `srcset`/`sizes` y un optimizador (el de Next.js o un servicio de imágenes).
- **Un tamaño por uso:** miniaturas de ~400 px, héroe de ~1280 px; objetivo ≤150 KB por foto de tarjeta y ≤300 KB por héroe.
- **Caché larga** (`max-age=31536000, immutable`) para archivos con hash en el nombre.
- **Prioridad** (`fetchpriority="high"`) solo en la imagen principal; `lazy` en el resto, con `width`/`height` siempre.
- Mantener lo bueno: nombres descriptivos, `alt` útil y carpetas por tipo de contenido.
- Imágenes y textos propios (no reutilizar los de Capinita).

## 6. Límites
Se midieron 34 de 69 referencias (las demás eran 404 de respaldo PNG o URLs truncadas por el análisis); no se midió el peso real descargado por una página completa ni los Core Web Vitals (sin navegador). Pendiente: revisar el resto de fichas y el móvil real.
