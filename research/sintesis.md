# Síntesis del producto (acumulativa)

Estado: **solo Capinita analizado**. El segundo sitio de referencia aún no se ha indicado (`<URL_SITIO_2>`), así que no hay comparativa entre sitios. Fecha: 2026-10-23. Confianza global: media (sin revisión visual ni móvil; contenido leído de segunda mano).

## 1. Tabla comparativa (fuente: research/capinita.md)
| Función / página | Capinita | Sitio 2 |
|---|---|---|
| Búsqueda de rutas origen→destino | Sí, solo 2 campos, sin filtros | pendiente |
| Horarios y precios por cooperativa | Sí, tablas con contacto WhatsApp | pendiente |
| Fichas de cooperativa y terminal | Sí (reseñas vacías) | pendiente |
| Estado vial en vivo | Sí (ECU 911, por provincia/estado) | pendiente |
| Directorio de lugares | Tarjetas + categorías; fichas rotas (404) | pendiente |
| Tours y reservas | 9 tours, reserva solo por WhatsApp | pendiente |
| Registro de negocios | Gratis, con validación manual | pendiente |
| Cuenta/login | Registro correo + Google | pendiente |
| Blog/guías por región | Sí, poco contenido | pendiente |

## 2. Mejores patrones (Capinita)
- Un solo lugar para transporte + turismo + estado vial, con URLs jerárquicas por región/provincia/cantón (bueno para SEO).
- Tabla de horarios con tipo (directo/de paso), precio y contacto directo por fila.
- Mensaje de WhatsApp prellenado con el tour y su enlace (cero fricción para reservar).
- Alta de negocios gratuita y "reclamar perfil" para cooperativas.

## 3. Descartar (con razón)
- Fichas con datos sin fecha de verificación → pérdida de confianza.
- Reserva 100 % por WhatsApp sin disponibilidad ni pago → no escala.
- Itinerarios en PDF externos → no indexables ni editables.
- Contadores de paginación erróneos y "Loading..." visibles → defectos de calidad.
- Cifras de impacto sin fuente.
- Bloques de tours repetidos y publicidad de servicios no relacionados dentro de las fichas.

## 4. Backlog MoSCoW (provisional, solo con Capinita)
- **Must:** buscador de rutas con filtros (hora, precio, cooperativa); fichas de ruta/cooperativa/terminal con fecha de última verificación; ficha propia de lugar y de tour dentro del sitio; diseño móvil primero; política de privacidad con derechos reales.
- **Should:** estado vial por provincia con fuente y hora; solicitud de reserva estructurada (no solo WhatsApp); reseñas moderadas; registro y reclamo de negocios con verificación.
- **Could:** notificaciones de estado vial; mapa interactivo; guías por región; varios idiomas.
- **Won't (por ahora):** pagos en línea; app nativa; marketplace de servicios de terceros.

## 5. Arquitectura propuesta (borrador)
Módulos: Transporte (rutas, cooperativas, terminales, horarios), Turismo (lugares, tours), Vialidad, Cuentas/Negocios, Contenido.
Modelo de datos: Región > Provincia > Cantón; Lugar; Terminal; Cooperativa; Ruta; Salida (horario + precio + cooperativa); Tour; Negocio; Usuario; Reseña; EstadoVial.
Pantallas: inicio, búsqueda de ruta, detalle, directorio, tours, estado vial, panel de negocio.

## 6. Stack
Recomendación provisional (detalle y justificación en research/analisis-tecnico-capinita.md): Next.js + TypeScript + Tailwind, PostgreSQL, MapLibre/Leaflet con ruteo autoalojado, Auth.js y almacenamiento de imágenes propio. Referencia medida: Capinita usa Next.js en Vercel, Tailwind, Leaflet/OSM, Auth.js y datos del ECU 911 con caché de 5 min. Compatibilidad con el proyecto actual: el repo solo tiene documentación, así que no hay stack previo que respetar; confirmar con el usuario.

## 7. Riesgos y decisiones pendientes
- Falta el sitio 2 y la revisión visual/móvil (Chrome bloqueó el dominio: hay que permitirlo en la extensión).
- Fuente y licencia de los datos viales (ECU 911) y de horarios por cooperativa.
- Originalidad: no copiar textos, imágenes, marcas ni datos de Capinita.
- Confianza: alta en lo medido con curl; media en el resto.

---
## Actualización 2026-10-23 — Lote 7 (solo Capinita; segundo sitio PENDIENTE)
Confianza: alta en inventario y mediciones (curl y navegador); media en la interpretación de funciones (sin interacción con filtros ni búsquedas).

### 1. Tabla comparativa ampliada (fuentes: `clips/INDICE.md`, `evidencia/capinita-inventario-sitemap-2026-10-23.tsv`)
| Página / función | Capinita | Evidencia | Sitio 2 |
|---|---|---|---|
| Inicio con buscador de lugares | Sí | `clips/capinita/inicio.md` | pendiente |
| Búsqueda de rutas (origen → destino) | Sí, sin filtros | `ruta.md` | pendiente |
| Ficha de ruta con horarios y mapa | Sí; 213 en el sitemap | `ruta-gualaquiza-a-morona.md` | pendiente |
| Ficha de cooperativa | Sí; 24; reseñas vacías | `cooperativa-de-transporte-16-de-agosto.md` | pendiente |
| Terminales | Índice y fichas; 44 | `terminal-terrestre*.md` | pendiente |
| Ficha de lugar (alojamiento, atractivo) | Plantilla rica; 55 en Amazonía | `amazonia-…-hotel-la-jungla.md` | pendiente |
| Estado vial | Por provincia; fuente ECU 911 | `estado-vial-ecuador.md` | pendiente |
| Regiones y blog | 4 guías + 5 artículos | `sierra.md`, `blog*.md` | pendiente |
| Registro, login y alta de negocio | Visibles (no usados) | `crear-cuenta.md`, `iniciar-sesion.md`, `promocionar-negocio-turistico.md` | pendiente |
| Versión móvil | Responsiva, sin desborde (4 páginas) | capturas `*-movil-*.png` | pendiente |

### 2. Patrones útiles añadidos (fuente: Capinita)
- **Plantilla de ficha de lugar completa** (descripción, servicios, horario, cómo llegar, mapa, galería, FAQ, redes, tours cercanos, comentarios) → buen modelo de contenido para destinos y alojamientos.
- **Sitemap con 381 URLs jerárquicas** que crecen con el catálogo (rutas, lugares, terminales) → buena base de SEO programático.
- **Móvil**: navegación lateral que se convierte en menú, tarjetas apiladas, pestañas desplazables.

### 3. A descartar (con motivo)
- Metadatos genéricos repetidos (21 páginas con el mismo título) y **sin etiqueta canonical** → perjudica el SEO.
- Páginas de error (404/500) incluidas en el sitemap.
- Plantillas con errores de contenido copiadas entre regiones ("Gastronomía Costera" en la Sierra y Galápagos).
- Imágenes sin `alt` en fichas dinámicas (8 en la ficha de ruta móvil).

### 4. Backlog MoSCoW (cambios por este lote)
- **Must (nuevo):** generar título, descripción y canonical únicos por página; sitemap que solo contenga URLs válidas; revisar automáticamente el sitemap contra errores 404/500 antes de publicar; texto alternativo obligatorio en toda imagen de contenido.
- **Should (nuevo):** plantilla de ficha de lugar completa; plantilla de región con contenido propio por región; pruebas de hidratación (zona horaria fija).
- **Could:** comentarios/opiniones moderados en lugares; favoritos y compartir.
- **Won't por ahora:** sin cambios.

### 5. Producto unificado (esbozo, sin cambios de arquitectura)
Se mantiene lo propuesto en las secciones 5 y 6 anteriores. Añadir: módulo de **contenido editorial por región** con plantilla validada, y un **verificador de integridad** (enlaces, sitemap, metadatos) que corra en cada despliegue.

### 6. Riesgos e hipótesis abiertas
- Segundo sitio sin URL: sin comparación entre referencias todavía.
- Sin interacción con filtros, búsquedas ni pestañas (no se hizo clic): comportamiento posterior a esas acciones no revisado.
- ~350 URLs revisadas solo por inventario; podría haber variantes de plantilla no vistas.
- Los datos de rutas y precios no tienen fecha de verificación visible: no se pueden dar como actuales.


---
## Actualización 2026-10-23 — Lote 1 de Airbnb Ecuador (segundo sitio) y comparación con Capinita
Confianza: media. De Airbnb solo se revisaron 7 páginas públicas (búsqueda, reserva y panel de anfitrión quedan fuera por `robots.txt` o por no tener cuenta) y la portada y el panel de precio se vieron incompletos. Fuentes: `research/airbnb.md`, `research/clips/airbnb/`, capturas en `research/capturas/airbnb/`.

### 1. Tabla comparativa de funciones
| Función | Capinita | Airbnb Ecuador | Evidencia |
|---|---|---|---|
| Modelo de búsqueda | Origen → destino (transporte) y buscador de lugares | Dónde + fechas + quién, con calendario | `capinita/ruta.md`; `airbnb/inicio.md` |
| Página de destino con SEO | Guías regionales largas y fichas | `/<ciudad>/stays` con estadísticas, mejor valorados y servicios | `capinita/sierra.md`; `airbnb/quito-ecuador-stays.md` |
| Ficha de oferta | Ficha de lugar y de ruta/cooperativa | Ficha con galería, servicios, calendario, reseñas, mapa y panel de reserva | `capinita/amazonia-…hotel-la-jungla.md`; `airbnb/rooms-….md` |
| Confianza | Sello "verificado" y reseñas vacías | Puntuación, número de reseñas, "Favorito entre huéspedes", denuncia del anuncio | idem |
| Reserva | Botón a WhatsApp con mensaje prellenado | Panel integrado (fechas y huéspedes); flujo no revisado | `capinita/tours.md`; `airbnb/rooms-….md` |
| Estado en tiempo real | Estado vial (ECU 911) | No aplica | `capinita/estado-vial-ecuador.md` |
| Ayuda al usuario | Sin centro de ayuda | Centro de ayuda con buscador y artículos | `airbnb/help.md` |
| Alta de oferentes | "Agregar negocio" en 4 pasos | "Conviértete en anfitrión" (no revisado) | `capinita/promocionar-negocio-turistico.md` |
| Móvil | Responsivo | Una columna, tarjeta de búsqueda a todo el ancho | capturas `*-movil-*.png` |
| Seguridad en cabeceras | Sin CSP/XFO | CSP de 12 directivas, XFO, HSTS preload, anti-bots | `airbnb.md`; `seguridad-lecciones-capinita.md` |

### 2. Mejores patrones por fuente
- **Airbnb:** buscador con tres campos y calendario; ficha con jerarquía clara (galería, resumen, puntuación, anfitrión, destacados, servicios, calendario, reseñas, ubicación); sello de calidad basado en datos; página de destino que mezcla estadísticas del propio inventario con oferta destacada; centro de ayuda; texto y rótulos cortos.
- **Capinita:** estado vial con fuente y ruta alterna; horarios y precios de transporte por cooperativa; contacto directo por WhatsApp; guías regionales y SEO por jerarquía geográfica.

### 3. Qué descartar (con motivo)
- **De Airbnb:** telemetría excesiva (decenas de peticiones de registro por página) → peso y privacidad; traducción automática sin control del autor → errores de contenido; páginas muy pesadas en imágenes sin texto alternativo → accesibilidad.
- **De Capinita:** lo ya listado (títulos repetidos, sin canonical, errores 404/500 en sitemap, botones desactivados).

### 4. Backlog MoSCoW unificado (cambios por este lote)
- **Must:** buscador con ubicación, fechas y personas cuando se ofrezcan reservas; ficha de oferta con galería, servicios, calendario, mapa y reseñas; puntuación y número de reseñas reales (sin cifras inventadas); texto alternativo en todas las fotos.
- **Should:** páginas de destino con estadísticas calculadas con nuestros propios datos; sello de calidad con criterios públicos; centro de ayuda; solicitud de reserva estructurada (fechas y personas) antes de integrar pagos.
- **Could:** calendario con disponibilidad; denuncia de anuncios; traducción asistida con revisión humana.
- **Won't (por ahora):** pagos integrados; programa de anfitriones completo; copiar cualquier cifra, texto o diseño de Airbnb.

### 5. Producto unificado (esbozo)
Plataforma de turismo y transporte con dos ejes: **(1) Transporte** (rutas, cooperativas, terminales, estado vial) y **(2) Alojamientos y experiencias** (fichas con galería, servicios, calendario y reseñas). Búsqueda unificada: "dónde" + fechas + personas para estadías; origen → destino para transporte. Modelo de datos adicional: Alojamiento, Habitación, Servicio (amenidad), Disponibilidad, Reseña, Anfitrión/Negocio, Solicitud de reserva. Todo con diseño, textos, nombres, código e imágenes propios.

### 6. Stack
Sin cambios respecto a lo ya propuesto (Next.js + TypeScript + Tailwind, PostgreSQL, mapa cargado bajo demanda, Auth.js). Añadir: encabezados de seguridad al nivel de los observados en Airbnb (CSP estricta, `X-Frame-Options`, HSTS con `includeSubDomains` y `preload`), y un presupuesto de peticiones de telemetría.

### 7. Riesgos, hipótesis y datos pendientes
- Airbnb: faltan búsqueda, reserva y panel de anfitrión (fuera de `robots.txt` o sin cuenta); portada y precio vistos incompletos; no se analizó su JavaScript con REA.
- Modelo de negocio, comisiones y reglas de reserva de Airbnb: no verificados.
- Cualquier cifra de Airbnb (alquileres, reseñas) es una afirmación suya, no verificada por nosotros.
